import discord

from database.DataBase import DataBase
from app.utilities.warningmessages import send_warning
from app.utilities.configreader import ConfigReader


class IntegerModal(discord.ui.Modal):
    def __init__(self, *args, user, guild, action=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.action = action
        self.user_id = user.id
        self.guild_id = guild.id
        self.active_sheet = DataBase.dbRef.child(f"Fichas:{self.guild_id}/P:{self.user_id}/").get()[f'Config:{self.user_id}']['ActiveSheet']
        self.sheet = DataBase.dbRef.child(f"Fichas:{self.guild_id}/P:{self.user_id}").get()[self.active_sheet]

        # Caixa de texto para o título
        self.add_item(discord.ui.InputText(label="Valor Numérico",
                                           max_length=10))


    async def callback(self, interaction: discord.Interaction):
        value = self.children[0].value
        if not value.isnumeric():
            await send_warning(interaction, "ERROR", "Valor inválido.")
            return
        
        if self.action == 'rpv':
            self.sheet['PVA'] = int(self.sheet['PVA']) - int(value)
        if self.action == 'cpv':
            self.sheet['PVA'] = int(self.sheet['PVA']) + int(value)
        if self.action == 'rpm':
            self.sheet['PMA'] = int(self.sheet['PMA']) - int(value)
        if self.action == 'cpm':
            self.sheet['PMA'] = int(self.sheet['PMA']) + int(value)

        DataBase.dbRef.child(f"Fichas:{self.guild_id}/P:{self.user_id}/{self.active_sheet}").update(self.sheet)

        from app.fichas.sheetcontroller import SheetController
        embed, buttons = SheetController().view_sheet(user=interaction.user, guild=interaction.guild)
        await interaction.response.edit_message(content="", embed=embed, view=buttons)
        
        
        
