import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

from app.recompensas.rewardfunctions import RewardFunctions
from app.utilities.warningmessages import send_warning

class RewardCommand(commands.Cog):
    reward = SlashCommandGroup("recompensa", "Gera recompensas de missões (ou eventos) conforme o sistema da guilda.")
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @reward.command(description='Gera uma recompensa de missão para T20.')
    async def t20(self, interaction: discord.Interaction, nd: discord.Option(int, choices=range(1, 21)), porcentagem: int, invisivel: bool = True):
        await send_warning(interaction, "SUCCESSFUL", RewardFunctions.t20(nd=nd, porcentagem=porcentagem), ephemeral=invisivel)

    @reward.command(description='Gera uma recompensa de missão para D&D.')
    async def dnd(self, interaction: discord.Interaction, na: discord.Option(int, choices=range(1, 21)), invisivel: bool = True):
        await send_warning(interaction, "SUCCESSFUL", RewardFunctions.dnd(na=na), ephemeral=invisivel)

def setup(bot: commands.Bot):
    bot.add_cog(RewardCommand(bot))
