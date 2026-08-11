# Kartbot

Fork do bot de discord feito originalmente por deagahelio e anteriormente mantido por riomccloud.

## Dependências

- Python 3.8+ (+ `discord.py`, `psutil`, `aiohttp`)
- `tmux`
- `stuff`

## Importante

- A partir do Ubuntu 24.04 o Python 3.10- não é mais suportado por padrão. Instalar o Python 3.9 através do código-fonte usando alt install para não conflitar com a versão do sistema é recomendado.

## Uso

- Crie um venv para o bot utilizando `python3.9 -m venv .venv`. Faça isso de preferência na mesma pasta onde está localizado o bot
- Execute o venv utilizando `source .venv/bin/activate`
- Instale as dependências do bot utilizando o `pip3 install -r requirements.txt`. Use esse comando na pasta raiz do repositório
- Copie o arquivo `kartbot_config.template.json` para `kartbot_config.json` e defina os valores apropriados
- Copie os arquivos `uglyhitfeed.lua` e `notify_skin_change0.lua` para a pasta `addons` do seu jogo
- Inicie o servidor usando `tmux new -d -s server /caminho/do/srb2kart -dedicated -file uglyhitfeed.lua notify_skin_change0.lua &`
- Execute `python3.9 kartbot.py`

## Nota sobre o hitfeed para o Discord

Para que os emojis funcionem no hitfeed do Discord é necessário que eles sejam configurados no addon `uglyhitfeed.lua`. No bloco `local function getDiscordEmoji(sprite)` você irá encontrar para cada linha um item diferente do jogo base. Para cada item um emoji precisa ser associado utilizando o ID do mesmo. A melhor forma de adicionar emojis para o Kartbot é através do portal de desenvoldor do Discord, na aba `Emojis`. Ao adicionar um emoji para um item você terá na coluna `ID DO EMOJI` o ID do emoji recém adicionado. Logo ao lado desse ID você terá um botão de copiar. Clicando nesse botão você irá copiar o emoji já formatado para o `uglyhitfeed` no seguinte formato: `<emoji:0123456789012345678>`. Cole ele por cima do modelo no addon. Por exemplo: para o item `Grow` você teria um emoji com o nome `Grow` e ID `<Grow:0123456789012345678>`. O ID desse emoji deve ser colado por cima de `<:KISGROW:>` no addon. 

## Configuração

Essas configurações são referentes ao arquivo `kartbot_config.json`

- `prefix` - Prefixo usado para os comandos do bot
- `token` - Token do bot


- `server_name` - Nome do servidor
- `tmux_name` - Nome do `tmux` do servidor
- `server_folder_path` - Caminho da pasta do servidor **com uma barra (/) no final!**
- `server_executable_name` - Nome do arquivo executável do servidor
- `server_script_path` - Caminho para o script que inicia o servidor
- `server_max_players` - Número máximo de jogadores do servidor (não influencia a funcionalidade do bot, é apenas exibido no `k!info`)
- `permission_error_message` - Mensagem a ser exibida no `k!race` e `k!battle` quando o usuário não tiver o cargo necessário
- `allowed_roles` - Lista de cargos que tem permissão aos [comandos de Admin](#admin)

- `log_path` - Caminho para o log do servidor - `/caminho/do/srb2kart/latest-log.txt`

- `chat_bridge` - Define se a ponte entre o Discord e o servidor será ativo ou não - `true` ou `false`
- `chat_bridge_channel_id` - ID do canal de ponte no Discord
- `bot_commands_channel_id` - ID do canal para comandos a serem enviados para dentro do jogo
- `track_images_url` - URL com as thumbnails dos mapas do servidor. Devem seguir o seguinte formato: `MAP01-kart.png`
- `webhook_url` - URL do webhook do canal de ponte no Discord
- `webhook_base_avatar_url` - URL com as thumbnails dos personagens do servidor.

## Comandos

- `k!ip` - Manda o IP do servidor
- `k!info` - Manda informações sobre o servidor e os jogadores conectados

## Admin

- `k!restart` - Reinicia o servidor
- `k!command|comando <comando>` - Executa um comando, por exemplo: `k!command map 01`

## Avançado

- Caso queira editar o IP dos servidores que aparecem no comando `k!ip` abra o `kartbot.py` no seu editor de texto preferido e a partir da `linha 63` você consegue definir o IP dos servidorees que serão exibidos através do comando

## Créditos

- `deagahelio` pela versão original do kartbot
- `riomccloud` por manter online um fork baseado na versão mais recente do `discord.py`
- `raphaelgoulart` por me ajudar com o webhook dos avatares e com as mensagens na ponte
- `Indev450` por me ajudar a implementar o suporte ao HITFEED na ponte e o suporte ao webhook dos avatares
