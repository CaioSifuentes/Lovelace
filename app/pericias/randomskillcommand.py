import discord
from random import randint
from discord.ext import commands


class RandomSkillCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.slash_command(description='Escolhe uma perícia aleatória baseado na Tabela 6-6.')
    async def periciat20(self, interaction: discord.Interaction):
        desafio_buscas = {
            2: 'Misticismo',
            3: 'Adestramento',
            4: 'Conhecimento',
            5: 'Enganação',
            6: 'Cura',
            7: 'Iniciativa',
            8: 'Intimidação',
            9: 'Investigação',
            10: 'Reflexos',
            11: 'Atletismo',
            12: 'Percepção',
            13: 'Sobrevivência',
            14: 'Fortitude',
            15: 'Diplomacia',
            16: 'Furtividade',
            17: 'Acrobacia',
            18: 'Intuição',
            19: 'Vontade',
            20: 'Luta',
            21: 'Jogatina',
            22: 'Nobreza',
            23: 'Religião',
            24: 'Guerra'
        }
        dado_1 = randint(1, 12)
        dado_2 = randint(1, 12)
        pericia_aleatoria = desafio_buscas[dado_1 + dado_2]
        await interaction.response.send_message(f"> Rolando 2d12 → {dado_1} + {dado_2} = {(dado_1+dado_2)} "
                                                f"\n**{pericia_aleatoria}**")


def setup(bot: commands.Bot):
    bot.add_cog(RandomSkillCommand(bot))
