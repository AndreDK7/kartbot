# kartbot

Fork do bot de discord feito originalmente por deagahelio e anteriormente mantido por riomccloud.

## Dependências

- Python 3.8+ (+ `discord.py`, `psutil`)
- `tmux`
- `stuff`

## Importante

- A partir do Ubuntu 24.04 o Python 3.10- não é mais suportado por padrão. Instalar o Python 3.9 através do código-fonte usando alt install para não conflitar com a versão do sistema é recomendado.

## Uso

- Crie um venv para o bot utilizando `python3.9 -m venv .venv`. Faça isso de preferência na mesma pasta onde está localizado o bot
- Execute o venv utilizando `source .venv/bin/activate`
- Instale as dependências do bot utilizando o `pip3`
- Copie o arquivo `kartbot_config.template.json` para `kartbot_config.json` e defina os valores apropriados
- Inicie o servidor usando `tmux new -d -s server /caminho/do/srb2kart -dedicated &`
- Execute `python3.9 kartbot.py`

## Configuração

- `prefix` - Prefixo usado para os comandos do bot
- `description` - Descrição do bot que aparece no comando de ajuda
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

### Admin

- `k!restart` - Reinicia o servidor
- `k!command|comando <comando>` - Executa um comando, por exemplo: `k!command map 01`

