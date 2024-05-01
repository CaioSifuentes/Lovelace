import PyPDF2
import discord
from math import floor
from random import randint
from io import BytesIO

from database.DataBase import DataBase
from app.utilities.configreader import ConfigReader

from app.fichas.views.sheetcontrolbuttons import SheetControlButtons
from app.fichas.views.playerlistpages import PlayerListPages


class SheetController:
    def __init__(self) -> None:
        self.config = ConfigReader.get_config()
    
    def generate_database_path(self, user, guild):
        return f"G:{guild.id}:T20/U:{user.id}"

    def get_active_sheet(self, user, guild):
        try:
            return DataBase.dbRef.child(self.generate_database_path(user, guild)).get()[f'C:{user.id}']['ActiveSheet']
        except:
            return False


    def activate_sheet(self, user, guild, character):
        try:
            path = self.generate_database_path(user, guild)
            user_sheets = DataBase.dbRef.child(path).get()
            if character == user_sheets[f'C:{user.id}']['ActiveSheet']:
                return "Sheet is already activated."
            
            user_sheets[f'C:{user.id}']['ActiveSheet'] = character
            DataBase.dbRef.child(path).update(user_sheets)
        except:
            return False

    def delete_sheet(self, user, guild, character):
        path = self.generate_database_path(user, guild)
        DataBase.dbRef.child(path + f"/{character}").delete()
    
    def view_sheet(self, user, guild):
        sheet = self.get_active_sheet(user, guild)
        if not sheet:
            return [None, None]

        embed = discord.Embed(color=sheet['Color'])
        embed.set_author(name = f"{sheet['Nome']} ND{sheet['ND']}", icon_url= user.avatar)
        if 'ImagemURL' in sheet:
            embed.set_image(url=sheet['ImagemURL'])
        embed.add_field(name="", value=f"**Raça:** {sheet['Raça']} | **Classe(s):** {sheet['Classe(s)']}\n**Divindade:** {sheet['Divindade']} | **Origem:** {sheet['Origem']}", inline=False)
        embed.add_field(name="", value=f"**💖 PV:** {sheet['PVA']}/{sheet['PV']} | **🧪 PM:** {sheet['PMA']}/{sheet['PM']}\n**Defesa:** {sheet['CA']} | **CD para Magias:** {sheet['CD']}", inline=False)

        buttons = SheetControlButtons(user=user, guild=guild)
        return embed, buttons
    
    def clear_sheets(self, user, guild):
        path = self.generate_database_path(user, guild)
        DataBase.dbRef.child(path).delete()
    
    def show_skills(self, user, guild):
        sheet = self.get_active_sheet(user, guild)
        if not sheet:
            return None
        
        embed = discord.Embed(color=sheet['Color'])
        embed.set_author(name = f"{sheet['Nome']} ND{sheet['ND']}", icon_url= user.avatar)

        final_list_1 = ''
        final_list_2 = ''
        lista_de_pericias = list(sheet['Perícias'].items())
        metade_lista = len(lista_de_pericias) // 2

        for pericia, valor_pericia in lista_de_pericias[:metade_lista]:
            numero_oficio = pericia[-1]
            nome_oficio = sheet['Ofícios'].get(f"Ofício_{numero_oficio}", "")
            pericia = f"Ofício{numero_oficio} ({nome_oficio})" if nome_oficio else pericia
            final_list_1 += f'- **{pericia}**: ` {valor_pericia} `\n'

        for pericia, valor_pericia in lista_de_pericias[metade_lista:]:
            numero_oficio = pericia[-1]
            nome_oficio = sheet['Ofícios'].get(f"Ofício_{numero_oficio}", "")
            pericia = f"Ofício{numero_oficio} ({nome_oficio})" if nome_oficio else pericia
            final_list_2 += f'- **{pericia}**: ` {valor_pericia} `\n'

        embed.add_field(name='', value=final_list_1)
        embed.add_field(name='', value=final_list_2)
        
        embed.set_footer(text="Digite `/fichas rolar <nome da perícia> <modificadores>` para realizar uma rolagem de perícia.")

        return embed
    
    def change_color(self, user, guild, new_color):
        path = self.generate_database_path(user, guild)
        sheet = self.get_active_sheet(user, guild)
        if not sheet:
            return None

        dict_color = {"Color": new_color}
        DataBase.dbRef.child(path + f"/{sheet['Nome']}").update(dict_color)

        return True
    
    def list_server_sheets(self, guild, nd=0):
        all_sheets = DataBase.dbRef.child(f"G:{guild.id}/").get()

        characters_by_nd = {}
        for usuario, personagens in all_sheets.items():
            for personagem, ficha in personagens.items():
                if not personagem == "C:" + usuario[2:]:
                    nd_personagem = ficha["ND"]
                    if nd_personagem not in characters_by_nd:
                        characters_by_nd[nd_personagem] = []
                    characters_by_nd[nd_personagem].append(personagem)

        view = PlayerListPages(content=characters_by_nd, nd=nd)
        embed = view.embed        

        return embed, view

    def roll_skill(self, user, guild, pericia, bonus, metodo):
        sheet = self.get_active_sheet(user, guild)
        if not sheet:
            return None
        
        if pericia.startswith("Ofício"):
            pericia = pericia[:7]
        
        skill_value = sheet["Perícias"][pericia]
        if not skill_value.isnumeric():
            return None

        if metodo == "Apenas um dado":
            roll_result = randint(1, 20)
            total = roll_result + int(skill_value) + int(bonus)
            roll_result = f"**{roll_result}**" if roll_result in [1, 20] else roll_result
            texto_final = f"` {total} ` ⟵ [{roll_result}] 1d20 + {skill_value} + {bonus}"
        elif metodo == "Dois dados e melhor resultado":
            roll = [randint(1, 20), randint(1, 20)]
            roll_result = max(roll)
            total = roll_result + int(skill_value) + int(bonus)
            roll_result = f"**{roll_result}**" if roll_result in [1, 20] else roll_result
            texto_final = f"` {total} ` ⟵ [~~{min(roll)}~~, {roll_result}] 2d20kh1 + {skill_value} + {bonus}"
        elif metodo == "Dois dados e pior resultado":
            roll = [randint(1, 20), randint(1, 20)]
            roll_result = min(roll)
            total = roll_result + int(skill_value) + int(bonus)
            roll_result = f"**{roll_result}**" if roll_result in [1, 20] else roll_result
            texto_final = f"` {total} ` ⟵ [~~{max(roll)}~~, {roll_result}] 2d20kl1 + {skill_value} + {bonus}"

        embed = discord.Embed(color=sheet['Color'])
        if pericia.startswith("Ofício"):
            numero_oficio = pericia[-1]
            nome_oficio = sheet['Ofícios'].get(f"Ofício_{numero_oficio}", "")
            if nome_oficio:
                pericia = f"Ofício ({nome_oficio})"
        embed.add_field(name=f"{sheet['Nome']} está rolando: {pericia}", value=texto_final)

        return embed
    
    def read_pdf(self, file, server_id):
        pdf = BytesIO(file)
        pdf_reader = PyPDF2.PdfReader(pdf)
        form_fields = pdf_reader.get_fields()
        if not form_fields:
            return None

        field_values = {}
        for field_name, field_data in form_fields.items():
            if field_name in self.config[str(server_id)]['PDFFormNames']:
                field_values[field_name] = field_data.get('/V', '')

        return field_values
    
    def send_sheet_to_database(self, sheet_values, character_name, user, guild):
        path = self.generate_database_path(user, guild)
        sheets = DataBase.dbRef.child(path).get()
        if sheets:
            if len(sheets) >= self.config[str(guild.id)]["SheetLimit"] and character_name not in sheets:
                return f"Não é possível adicionar mais do que {self.config[str(guild.id)]['SheetLimit']} fichas."
        else:
            base_configs = {'ActiveSheet': character_name}
            DataBase.dbRef.child(path).child(f"C:{user.id}").set(base_configs)

        DataBase.dbRef.child(path).child(f"{character_name}").set(sheet_values)
            