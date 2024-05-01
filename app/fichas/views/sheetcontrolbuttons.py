import discord

from database.DataBase import DataBase
from app.utilities.warningmessages import send_warning

from app.fichas.views.integermodal import IntegerModal

class SheetControlButtons(discord.ui.View):
    def __init__(self, user, guild):
        super().__init__()
        self.user = user
        self.guild = guild

    @discord.ui.button(label="Reduzir Pontos de Vida",
                       style=discord.ButtonStyle.green,
                       emoji="💔")
    async def button_callback_rpv(self, button: discord.ui.button, interaction: discord.Interaction):
        modal = IntegerModal(title="Reduzindo Pontos de Vida", user=self.user, guild=self.guild, action='rpv')
        await interaction.response.send_modal(modal=modal)

    @discord.ui.button(label="Curar Pontos de Vida",
                       style=discord.ButtonStyle.green,
                       emoji="💖")
    async def button_callback_cpv(self, button: discord.ui.button, interaction: discord.Interaction):
        modal = IntegerModal(title="Curando Pontos de Vida", user=self.user, guild=self.guild, action='cpv')
        await interaction.response.send_modal(modal=modal)

    @discord.ui.button(label="Reduzir Pontos de Mana",
                       style=discord.ButtonStyle.grey,
                       emoji="🔹")
    async def button_callback_rpm(self, button: discord.ui.button, interaction: discord.Interaction):
        modal = IntegerModal(title="Reduzindo Pontos de Mana", user=self.user, guild=self.guild, action='rpm')
        await interaction.response.send_modal(modal=modal)

    @discord.ui.button(label="Curar Pontos de Mana",
                       style=discord.ButtonStyle.grey,
                       emoji="🔷")
    async def button_callback_cpm(self, button: discord.ui.button, interaction: discord.Interaction):
        modal = IntegerModal(title="Curando Pontos de Mana", user=self.user, guild=self.guild, action='cpm')
        await interaction.response.send_modal(modal=modal)

    @discord.ui.button(label="Restaurar PV e PM",
                       style=discord.ButtonStyle.blurple,
                       emoji="💉")
    async def button_callback_rpvpm(self, button: discord.ui.button, interaction: discord.Interaction):
        active_sheet = DataBase.dbRef.child(f"Fichas:{self.guild.id}/P:{self.user.id}/").get()[f'Config:{self.user.id}']['ActiveSheet']
        sheet = DataBase.dbRef.child(f"Fichas:{self.guild.id}/P:{self.user.id}").get()[active_sheet]

        sheet['PVA'] = sheet['PV']
        sheet['PMA'] = sheet['PM']

        DataBase.dbRef.child(f"Fichas:{self.guild.id}/P:{self.user.id}/{active_sheet}").update(sheet)

        from app.fichas.sheetcontroller import SheetController
        embed, buttons = SheetController().view_sheet(user=interaction.user, guild=interaction.guild)
        await interaction.response.edit_message(content="", embed=embed, view=buttons)