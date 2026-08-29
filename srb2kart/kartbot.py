import asyncio, discord, json, os, pathlib, psutil, re, subprocess, time, aiohttp
from discord.ext import commands
from discord import Webhook

# CARREGA O ARQUIVO DE CONFIGURAÇÃO

with open(
	str(pathlib.Path(__file__).parent.absolute()) + "/kartbot_config.json", "r"
) as f:
	config = json.loads(f.read())

class Player():
    def __init__(self, name, skin, color, spec):
        self.name = name
        self.skin = skin
        self.color = color
        self.spec = spec

players_s = [range(1,16)]
for x in range(1,16):
    players_s.insert(x, Player("", "default", "", True))

players_n = 0

# CARREGA REGRAS REGEX PARA DETECTAR ATOS NO ARQUIVO DE LOG

map_re = re.compile('Map is now "(.+)"')
node_re = re.compile(r"^\d+:\s+(.+) - \d+ - \d+")
action_re = re.compile(
	r"^((\*.+ entered the game\.)|(\*.+ left the game)|(\*.+ has joined the game \(node \d+\))|(\*.+ renamed to [^\n]+)|(\*.+ became a spectator\.)|(.+ has finished the race\.)|(.+ ran out of time\.)|(The round has ended\.)|(Speeding off to level\.\.\.))"
)

# CARREGA VARIÁVEL PARA LEITURA DO LOG

last_log_line = 0

# CARREGA AS DEFINIÇÕES DO BOT NO ARQUIVO DE CONFIGURAÇÃO

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=config["prefix"], intents=intents, help_command=None, case_insensitive=True)

# STATUS DO BOT NO DISCORD

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name="como um anel!"))
	if config["chat_bridge"]:
		bot.loop.create_task(chat_bridge())
		bot.loop.create_task(delete_tmp())

# CARGOS COM PERMISSÃO DE COMANDOS

def is_admin(ctx):
	for role in ctx.author.roles:
		if role.name in config["allowed_roles"]:
			return True
	return False

# COMANDO !IP

@bot.command()
async def ip(ctx):
	embed = discord.Embed(title="IPs dos servidores",
		description="Confira os endereços IP de servidores Ring Racers e SRB2Kart da nossa equipe e de parceiros da comunidade.",
		colour=0x000099E1)
	embed.add_field(name="Interlagos (Ring Racers)",
		value="```i.srb2kbr.com```",
		inline=False)
	embed.add_field(name="Jacarepaguá (SRB2Kart)",
		value="```j.srb2kbr.com```",
		inline=False)
	embed.add_field(name="Dr. Zap (SRB2Kart)",
		value="```zerolab.app```",
		inline=False)
	embed.set_thumbnail(url="https://wiki.srb2.org/w/images/c/c8/Sonic%26TailsPortrait.png")
	
	await ctx.send(embed=embed)

# COMANDO !INFO
# Trecho original por Deagahelio, Goulart e Fafabis

@bot.command()
async def info(ctx):
	status = "ON"
	uptime = 0 
	
	try:
		pid = int(
			subprocess.check_output(["pidof", config["server_executable_name"]]).split(
				b" "
			)[0]
		)
		process = psutil.Process(pid)
		uptime = time.time() - process.create_time()
	except subprocess.CalledProcessError:
		status = "OFF"
	
	state = 0
	players = []
	specs = []
	map_ = "???"
	mode = "???"

	if status == "ON":
		os.system(
			f"tmux send-keys -t {config['tmux_name']} \"nodes\" ENTER \"version\" ENTER"
		)

		await asyncio.sleep(0.5)

		for _ in range(5):
			with open(f"{config['log_path']}", "r", encoding='utf8', errors='ignore') as f:
				log = f.read().split("\n")[::-1]
				state = 0
				for line in log:
					if state == 0:
						if line.startswith("SRB2Kart"):
							state = 1
					elif state == 1:
						match = node_re.match(line)
						if match is not None:
							if line[-1] == ")":
								specs.append(match.group(1))
							else:
								players.append(match.group(1))
						elif line.startswith("$nodes"):
							state = 2
					elif state == 2:
						for line in log:
							match = map_re.match(line)
							if match is not None:
								map_ = match.group(1)
								break
						break
				if state == 2:
					break
				else:
					continue

		with open(f"{config['log_path']}", "r", encoding='utf8', errors='ignore') as f:
			log = f.read().split("\n")[::-1]
			for line in log:
				if line.startswith("[GAMETYPE] "):
					mode = line.split(" ")[1]
					break

	else:
		state = 2

	if state == 2:
		mapid = map_.split(":")[0]

		if len(players) + len(specs) == 0:
			formatted_players = "\u200B"
		else:
			formatted_players = "· " + "\n· ".join(
				players + list(map(lambda x: f"*{x}*", specs))
			)
		formatted_uptime = (
			f"{int(uptime/60/60):02}:{int(uptime/60%60):02}:{int(uptime%60):02}"
		)

		embed = discord.Embed(color=0x00FF00 if status == "ON" else 0xFF0000)
		embed.set_image(url=f"{config['track_images_url']}" + mapid + "-kart.png")
		embed.add_field(
			name="Status", value="✅ ON" if status == "ON" else "❌ OFF", inline=True
		)
		embed.add_field(name="Tempo ativo", value=formatted_uptime, inline=True)
		embed.add_field(name="\u200B", value="\u200B", inline=True)
		embed.add_field(name="CPU", value=f"{psutil.cpu_percent()}%", inline=True)
		embed.add_field(
			name="RAM", value=f"{psutil.virtual_memory().percent}%", inline=True
		)
		embed.add_field(name="\u200B", value="\u200B", inline=True)
		if status == "ON":
			embed.add_field(
				name=f"Jogadores {len(players)+len(specs)}/{config['server_max_players']}",
				value=discord.utils.escape_mentions(formatted_players),
				inline=False,
			)
			embed.add_field(name="Pista", value=map_, inline=True)

		await ctx.reply(embed=embed, mention_author=False)
	else:
		await ctx.reply(f"Não foi possível obter o status atual do {config['server_name']}.", mention_author=False)

# COMANDO !COMMAND

@bot.command(checks=[is_admin])
async def command(ctx, *, cmd):
	path = config["server_folder_path"] + f"tmp/tmp{ctx.message.id}.cfg"
	with open(path, "w") as f:
		f.write(cmd)
	os.system(
		f"tmux send-keys -t {config['tmux_name']} \"exec tmp/tmp{ctx.message.id}.cfg\" ENTER"
	)
	await ctx.send(f"O comando foi executado em {config['server_name']}.")

# COMANDO !RESTART

@bot.command(checks=[is_admin])
async def restart(ctx):
	os.system(f"pkill {config['server_executable_name']} && tmux kill-session -t {config['tmux_name']}")
	if (config["ban_txt_File"]): os.remove(config["ban_txt_File"])
	os.system(
		f"bash {config['server_script_path']}"
	)
	await ctx.send(f"O {config['server_name']} foi reiniciado.")

# PONTE SRB2KART-DISCORD
# Trecho original por Deagahelio, Goulart e Fafabis

async def chat_bridge():
	global players_n
	global last_log_line
	async with aiohttp.ClientSession() as session:

		while True:
			try:
				with open(f"{config['log_path']}", "r", encoding='utf8', errors='ignore') as f:
					log = [l.strip() for l in f.readlines()]
					if last_log_line != 0:
						for line in log[last_log_line:]:
							if action_re.match(line) is not None:
								if line.startswith("*") and line.endswith(")"):
									players_n += 1
									if players_n == 1:
										players_s[1].spec = False
								elif line.startswith("*") and line.endswith("left the game"):
									players_n -= 1
								elif line.startswith("*") and line.endswith("entered the game."):
									name = line[:-18][1:]
									for x in range(1,16):
										if players_s[x].name == name:
											players_s[x].spec = False
											break
								elif line.startswith("*") and line.endswith("became a spectator."):
									name = line[:-20][1:]
									for x in range(1,16):
										if players_s[x].name == name:
											players_s[x].spec = True
											break
								message = re.search(action_re, line).group(1).replace("*", "")
								# manipular o texto da mensagem aqui
								message = message.replace("entered the game", "entrou na corrida")
								message = message.replace("left the game", "saiu do jogo")
								message = message.replace("has joined the game", "entrou no jogo")
								message = message.replace("renamed to", "alterou o nome para")
								message = message.replace("became a spectator", "se tornou um espectador")
								message = message.replace("has finished the race", "terminou a corrida")
								message = message.replace("ran out of time", "ficou sem tempo")
								message = message.replace("The round has ended.", "**A corrida terminou!**")
								message = message.replace("Speeding off to level...", "**Acelerando para a próxima corrida!**")
								await bot.get_channel(config["chat_bridge_channel_id"]).send(
									discord.utils.escape_mentions(
										"*"
										+ message
										+ "*"
									)
								)
							elif line.startswith("[HITFEED] "):
								await bot.get_channel(config["chat_bridge_channel_id"]).send(
									"_" + line[10:].replace("_", "\_").replace("*","\*") + "_"
								)
							elif line.startswith("<") and not line.startswith("<~SERVER> [D]"):
								webhook_avatar_url = config["webhook_base_avatar_url"] + "default.png"
								gameUsername = (
									line.split(">")[0]
									.replace("<", "")
								)
								msg = (
									line.split(">")[1]
									.replace("@everyone","~~@~~everyone")
									.replace("@here","~~@~~here")
									.replace("_", "\_")
									.replace("*", "\*")
									.replace("`", "\`")
								)
								for x in range(1,16):
									if (players_s[x].name == gameUsername or "@" + players_s[x].name == gameUsername) and not players_s[x].spec:
										webhook_avatar_url = webhook_avatar_url[:-11] + players_s[x].skin + "_" + players_s[x].color + ".png"
										break
								webhook = Webhook.from_url(config["webhook_url"], session=session)
								try:
									await webhook.send(msg, username=gameUsername, avatar_url=webhook_avatar_url)
								except Exception as e:
									print(str(e))
									continue
							elif line.startswith("[CHAR] "):
								color = line.split("[CHAR_COLOR] ")[1].split(" [")[0]
								skin = line.split("[CHAR_SKIN] ")[1].split(" [NUMBER]")[0]
								name = line.split("[NAME] ")[1]
								num = int(line.split("[NUMBER]")[1].split("[NAME]")[0])
								players_s[num].name = name
								players_s[num].skin = skin
								players_s[num].color = color
							elif line.startswith("Map is now"):
								mapname = (
										line.split(":")[1]
										.replace("\"", "")
										)
								mapid = (
										line.split(":")[0]
										.replace("Map is now \"","")
										)
								embed = discord.Embed(color=0x000099E1)
								embed.title = mapid + ":" + mapname
								embed.set_image(url=f"{config['track_images_url']}" + mapid + "-kart.png")
								try:
									await bot.get_channel(
										config["chat_bridge_channel_id"]
									).send(embed=embed)
								except Exception as e:
									print(str(e))
									continue
							elif line.startswith("[RESULTS] "):
								with open(f"{config['log_path']}", "r", encoding='utf8', errors='ignore') as f:
									log = f.read().split("\n")[::-1]
		
								data = {
									"map": "???",
									"players": [],
								}
		
								players = list(
									filter(
										lambda x: x[-1] == "false" and x[-2] == "false",
										[player.split(":") for player in line.split(";")[1:-1]],
									)
								)
								for player in players:
									player[3] = int(player[3])
								contest = list(
									sorted(
										filter(lambda x: x[3] != 0, players), key=lambda x: x[3]
									)
								)
								no_contest = list(filter(lambda x: x[3] == 0, players))
								players = contest + no_contest
								results_left = []
								results_right = []
								for i, player in enumerate(players):
									node = int(player[0])
									time = int(player[3])
									place = min(i, len(contest)) + 1
									name = player[1]
		
									results_left.append(f"{place}. {name}")
									if time != 0:
										data_player = {
											"name": name,
											"time": time,
											"place": place,
										}
		
										data["players"].append(data_player)
		
										minutes = int(time / 35 / 60)
										seconds = int(time / 35 % 60)
										hundredths = int((time / 35) % 1 * 100)
										results_right.append(
											f"{minutes}' {seconds}'' {hundredths}"
										)
									else:
										results_right.append("-")
		
								embed = discord.Embed(color=0x00FF000)

								embed.add_field(
									name="Resultados",
									value="\n".join(results_left),
									inline=True,
								)
								embed.add_field(
									name="\u200B",
									value="\n".join(results_right),
									inline=True,
								)
								try:
									await bot.get_channel(
										config["chat_bridge_channel_id"]
									).send(embed=embed)
								except Exception as e:
									print(str(e))
									continue
					last_log_line = len(log)
				await asyncio.sleep(2)
			except:
				await asyncio.sleep(2)
				pass

# PONTE DISCORD-SRB2KART
# Trecho original por Deagahelio

@bot.event
async def on_message(message):
	if not message.content.startswith(config["prefix"]):
		if message.channel.id == config["chat_bridge_channel_id"]:
			if not message.author.bot:
				text = (
					message.clean_content.replace('"', "")
					.replace("ç", "c")
					.replace("á", "a")
					.replace("ã", "a")
					.replace("â", "a")
					.replace("à", "a")
					.replace("é", "e")
					.replace("ê", "e")
					.replace("í", "i")
					.replace("ó", "o")
					.replace("õ", "o")
					.replace("ô", "o")
					.replace("ú", "u")
					.replace("^", "")
					.replace("\n", "")
					.replace(";", "")
				)
				text = text.encode('ascii', 'ignore').decode('ascii') # Remover caracteres non-ASCII pro jogo não crashar lol
				path = config["server_folder_path"] + f"tmp/tmp{message.id}.cfg"
				with open(path, "w") as f:
					f.write(f"say [D] {message.author.name}: {text}")
				os.system(
					f"tmux send-keys -t {config['tmux_name']} \"exec tmp/tmp{message.id}.cfg\" ENTER"
				)
	elif message.channel.id == config["bot_commands_channel_id"] or (any(role.name in config["allowed_roles"] for role in message.author.roles)):
		await bot.process_commands(message)

# APAGAR ARQUIVOS TEMPORÁRIOS
# Trecho original por Deagahelio

async def delete_tmp():
	while True:
		files = [
			config["server_folder_path"] + "tmp/" + f
			for f in os.listdir(config["server_folder_path"] + "tmp")
		]
		files.sort(key=os.path.getctime)
		for f in files[:-3]:
			os.system("rm " + f)
		await asyncio.sleep(10)

# RODAR BOT

bot.run(config["token"])