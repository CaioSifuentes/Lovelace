from app.utilities.configreader import ConfigReader
pericias = ["Acrobacia", "Adestramento", "Atletismo", "Atuação", "Cavalgar", "Conhecimento", "Cura", "Diplomacia", "Enganação", "Fortitude", "Furtividade", "Guerra", "Iniciativa", "Intimidação", "Intuição", "Investigação", "Jogatina", "Ladinagem", "Luta", "Misticismo", "Nobreza", "Ofício1", "Ofício2", "Ofício3", "Ofício4", "Ofício5", "Ofício6", "Ofício7", "Percepção", "Pilotagem", "Pontaria", "Reflexos", "Religião", "Sobrevivência", "Vontade"]
oficios = ["Ofício_1", "Ofício_2", "Ofício_3", "Ofício_4", "Ofício_5", "Ofício_6", "Ofício_7"]

class SheetModel:
    def __init__(self) -> None:
        self.sheet = {
            "Color": 0x800000,
            "Nome": "",
            "Raça": "",
            "Divindade": "",
            "Origem": "",
            "Classe(s)": "",
            "ImagemURL": "",
            "PV": 0,
            "PVA": 0,
            "PM": 0,
            "PMA": 0,
            "CA": 0,
            "CD": 0,
            "ND": 0,
            "Perícias": {},
            "Ofícios": {}
        }

    def setSheet(self, guild_id, sheet_values, imagem_url=None):
        self.form = ConfigReader.get_config()[str(guild_id)]["PDFFormNames"]
        self.pericias = self.form[8:43]
        self.oficios = self.form[45:]
        
        self.sheet["Nome"] = sheet_values.get(self.form[0], '')[:32]
        self.sheet["Raça"] = sheet_values.get(self.form[1], '')[:32]
        if self.sheet["Raça"] == '':
            self.sheet["Raça"] = sheet_values.get('Raca', '')[:32]
        self.sheet["Origem"] = sheet_values.get(self.form[2], '')[:32]
        self.sheet["Classe(s)"] = sheet_values.get(self.form[3], '')[:100]
        self.sheet["ND"] = int(sheet_values.get(self.form[4], 0))
        self.sheet["Divindade"] = sheet_values.get(self.form[5], '')[:32]
        self.sheet["ImagemURL"] = imagem_url

        self.sheet["PV"] = int(sheet_values.get(self.form[6], 0))
        self.sheet["PVA"] = int(sheet_values.get(self.form[6], 0))
        self.sheet["PM"] = int(sheet_values.get(self.form[7], 0))
        self.sheet["PMA"] = int(sheet_values.get(self.form[7], 0))
        self.sheet["CA"] = int(sheet_values.get(self.form[43], 0))
        self.sheet["CD"] = int(sheet_values.get(self.form[44], 0))

        pericias_dict = {}
        for idx, pericia in enumerate(self.pericias):
            pericias_dict[self.pericias[idx]] = pericias[idx]

        oficios_dict = {}
        for idx, oficio in enumerate(self.oficios):
            oficios_dict[self.oficios[idx]] = oficios[idx]

        for chave, valor in sheet_values.items():
            if chave in self.pericias:
                self.sheet["Perícias"][pericias_dict[chave]] = valor
            if chave in self.oficios:
                self.sheet["Ofícios"][oficios_dict[chave]] = valor

    def getSheet(self):
        return self.sheet
