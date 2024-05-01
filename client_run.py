from client import client

from database.DataBase import DataBase
from app.utilities.configreader import ConfigReader

# Carrega todas as funções dentro de app.
extensionList = [
    'moderacao.report',
    'pericias.penaltyorreward',
    'pericias.randomskill',
    'pericias.secondskill',
    'recompensas.reward',
    'fichas.sheet' 
]
for extension in extensionList:
    client.load_extension("app." + extension + "command")

config = ConfigReader.get_config()

# Avisa se o Bot está Online e atualiza todos os botões de missão.
@client.event
async def on_ready():
    mensagemInicial = "SUCESSFUL: Bot de Testes está online." if ConfigReader.get_mode() else "SUCESSFUL: Lovelace chegou na guilda!"

    for server, server_config in config.items():
        try:
            guild = await client.fetch_guild(server)
            report_channel = client.get_channel(server_config['ReportChannel'])
            report_result = "404 Not Found" if not report_channel else "302 OK"
            print(f"Status ({guild.name}): \033[32mCanal de denúncias: {report_result}")
        except Exception as e:
            print(f"\033[31mERRO AO DEFINIR O ESTADO DO SERVIDOR DE ID {server}.")

    print(f'\033[32m{mensagemInicial:^15}')
    print('\033[33m=\033[m' * 50)

# Conecta ao banco de dados
db = DataBase()

# Excecuta o bot.
client.run(ConfigReader.get_token())
