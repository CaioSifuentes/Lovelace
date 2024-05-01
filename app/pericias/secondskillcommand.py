import discord
from random import randint
from discord.ext import commands


class SecondSkillCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.slash_command(description='Rola uma perícia aleatória, baseado nas regras de Busca do servidor.')
    async def segundapericiat20(self, interaction: discord.Interaction, quantidadetreinadas: int):
        if quantidadetreinadas < 0 or quantidadetreinadas > 23:
            await interaction.response.send_message(f"Campo de entrada inválido. Tente novamente.", ephemeral=True)
        else:
            limite_treinada = 23 - quantidadetreinadas
            rolagem_d23 = randint(1, 23)
            if rolagem_d23 <= limite_treinada:
                rolagem_dx = randint(1, quantidadetreinadas)
                await interaction.response.send_message(f"> Rolando 1d23, sendo {limite_treinada} ou menos = Treinada"
                                                        f"\n> {rolagem_d23} → Treinada!\n"
                                                        f"\n> Rolando 1d{quantidadetreinadas} → {rolagem_dx}"
                                                        f"\nQual a sua {rolagem_dx}° perícia treinada?")
            else:

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
                await interaction.response.send_message(f"> Rolando 1d23, sendo {limite_treinada} ou menos = Treinada"
                                                        f"\n> {rolagem_d23} → Não treinada!\n"
                                                        f"\n> Rolando 2d12 → {dado_1} + {dado_2} = {(dado_1 + dado_2)} "
                                                        f"\n{(dado_1 + dado_2)}: **{pericia_aleatoria}**")


def setup(bot: commands.Bot):
    bot.add_cog(SecondSkillCommand(bot))
