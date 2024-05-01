from json import load
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from app.utilities.configreader import ConfigReader


class DataBase:
    if ConfigReader.get_mode():
        with open('database/DataBaseConfig-dev.json', 'r') as dbConfig:
            serviceAccountKey, databaseOptions = load(dbConfig)
    else:
        with open('database/DataBaseConfig.json', 'r') as dbConfig:
            serviceAccountKey, databaseOptions = load(dbConfig)

    try:
        appCredential = credentials.Certificate(serviceAccountKey)
        defaultApp = firebase_admin.initialize_app(
            credential=appCredential,
            options=databaseOptions
        )
        print(f"\033[32mSUCESSFUL: Sucesso ao conectar no banco de dados.")
    except ValueError as e:
        print(f"\033[31mERROR: Erro ao conectar ao banco de dados: {e}")

    dbRef = db.reference(f"/")

