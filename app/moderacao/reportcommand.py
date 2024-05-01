import discord
from discord.ext import commands

from app.utilities.warningmessages import send_warning
from app.utilities.configreader import ConfigReader

from app.moderacao.views.reportmodal import ReportModal


class ReportCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.config = ConfigReader.get_config()

    @commands.slash_command(
            title='Denunciar Anônimamente',
            description='Denuncia um membro do servidor anônimamente e envia a denúncia à moderação.'
            )
    async def denunciar(self, interaction: discord.Interaction, user: discord.Member):
        server_id = interaction.guild_id
        if str(server_id) not in self.config:
            await send_warning(interaction, "CAUTION", "Você não pode denunciar um jogador através do canal de mensagens privadas do bot, ou através de um servidor que não possui sistema de denúncias ativado.")
            return


        reported_user = user.mention
        reported_user_name = user.name
        channel_id = self.config[str(server_id)]["ReportChannel"]

        modal = ReportModal(title=f"Denunciar {reported_user_name}", reported_user=reported_user, report_channel=channel_id)
        await interaction.response.send_modal(modal)

def setup(bot: commands.Bot):
    bot.add_cog(ReportCommand(bot))