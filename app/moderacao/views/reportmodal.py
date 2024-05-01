import discord
from client import client

from app.utilities.warningmessages import send_warning

class ReportModal(discord.ui.Modal):
    def __init__(self, reported_user: str, report_channel: int,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reported_user = reported_user
        self.report_channel = client.get_channel(report_channel)

        self.add_item(discord.ui.InputText(label="Escreva o motivo da denuncia:", 
                                           style=discord.InputTextStyle.long, 
                                           max_length=1024))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"Usuário Denunciado:", description=self.reported_user)
        embed.add_field(name="Motivo da denuncia:", value=self.children[0].value)

        await send_warning(interaction, "SUCCESSFUL", f"Usuário {self.reported_user} denunciado.\nA denuncia será revisada pelos supervisores adequados.")
        await self.report_channel.send(embed=embed)