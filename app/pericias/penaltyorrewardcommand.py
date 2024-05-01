import discord
from random import randint, choice
from discord.ext import commands


class PenaltyOrRewardCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.slash_command(description='Digite "C" para castigo ou "R" para recompensa.')
    async def castigorecompensa(self, interaction: discord.Interaction,
                                castigo_ou_recompensa: discord.Option(str, choices=['C', 'R'])):
        rolagem_d6 = randint(1, 6)
        lista_castigos = [
            '**Ruína Menor.** Você perde dinheiro ou itens, a sua escolha, em valor equivalente a um quarto do '
            'dinheiro inicial do seu nível (veja a página 140). Por exemplo, um personagem de 5º nível (dinheiro '
            'inicial T$ 2.000) perde T$ 500. Se não tiver como pagar, sofre um Abalo.',

            '**Abalo.** Você sofre uma derrota que abala sua confiança. Durante a próxima aventura, seus pontos de mana'
            ' máximos diminuem em 1 por nível de personagem (se você é um personagem de 5º nível com 15 PM, por exemplo'
            ', terá apenas 10 PM na próxima aventura).',

            '**Complicação.** Você sofre uma complicação, que irá afetá-lo em algum momento de sua carreira. Você '
            'pode ter feito um inimigo poderoso, contraído uma doença mágica etc. Em termos de jogo, durante a próxima '
            'aventura, você sofre uma penalidade em seus pontos de vida e pontos de mana máximos igual à metade do '
            'seu nível de personagem.',

            '**Ferimento.** Você sofre um ferimento severo, que demora a cicatrizar. Durante a próxima aventura, seu '
            'pontos de vida máximos diminuem em 1 por nível de personagem. Habilidades e magias de cura não funcionam '
            'contra este efeito.',

            '**Maldição.** Você sofre um efeito da magia Rogar Maldição na próxima aventura.',

            '**Ruína Maior.** Você perde dinheiro ou itens, a sua escolha, em valor equivalente a metade do '
            'dinheiro inicial do seu nível (veja a página 140). Por exemplo, um personagem de 5º nível (dinheiro '
            'inicial T$ 2.000) perde T$ 1000. Se não tiver como pagar, sofre um Abalo.'
        ]
        castigo_ou_recompensa = castigo_ou_recompensa.upper()[0]
        if castigo_ou_recompensa == 'C':
            castigo = lista_castigos[rolagem_d6 - 1]
            if castigo == lista_castigos[5 - 1]:
                maldicao_lista = ['Debilidade: O alvo fica esmorecido e não pode se comunicar ou lançar magias. '
                                  'Ainda reconhece seus aliados e pode segui-los e ajudá-los, mas sempre de maneira '
                                  'simplória. ',

                                  'Fraqueza: O alvo fica debilitado e lento.',

                                  'Isolamento: O alvo perde o uso de um de seus cinco sentidos a sua escolha. Se '
                                  'perder a visão, fica cego. Se perder a audição, fica surdo. Se perder o olfato ou '
                                  'paladar, não pode usar a habilidade faro. Se perder o tato, fica caído e não pode '
                                  'se levantar.'
                                  ]
                maldicao = choice(maldicao_lista)
                if maldicao == maldicao_lista[2]:
                    sentidos_lista = ['Visão', 'Audição', 'Olfato', 'Paladar', 'Tato']
                    sentido = choice(sentidos_lista)
                    await interaction.response.send_message(f"> 1d6 → ` {rolagem_d6} ` "
                                                            f"\n{castigo}"
                                                            f"\n"
                                                            f"\nA Maldição escolhida foi: \n> {maldicao}"
                                                            f"\n`Você perdeu: {sentido}.`")
                else:
                    await interaction.response.send_message(f"> 1d6 → ` {rolagem_d6} ` "
                                                            f"\n{castigo}"
                                                            f"\n"
                                                            f"\nA Maldição escolhida foi: \n> {maldicao}")

            else:
                await interaction.response.send_message(f"> 1d6 → ` {rolagem_d6} ` "
                                                        f"\n{castigo}")
        elif castigo_ou_recompensa == 'R':
            lista_recompensas = [
                '**Tesouro (Riqueza).** Você ganha uma riqueza. Role na tabela Tesouros (veja o Capítulo 8: '
                'Recompensas), na coluna de riquezas, na linha correspondente a seu nível.',

                '**Favor.**Você recebe um favor de um NPC ou organização, ou a promessa de um favor futuro, que o '
                'ajuda por uma cena. Em termos de regra, você recebe 1 Vale',

                '**Tesouro (Item).** Você ganha um item. Role na tabela Tesouros (veja o Capítulo 8: '
                'Recompensas), na coluna de itens, na linha correspondente a seu nível.',

                '**Informação.** Você recebe uma informação, como a localização de um tesouro, a identidade do traidor '
                'na corte, a resposta para um enigma mágico, a cura para um veneno sobrenatural etc. Em termos de '
                'jogo, você recebe 1 Vale.',

                '**Tesouro (Tesouro e Item).** Você ganha um bem material. Role na tabela Tesouros (veja o Capítulo 8: '
                'Recompensas), em ambas as colunas (Tesouro e Item), na linha correspondente a seu nível.',

                '**Poder.** Você recebe um benefício de treinamento, definido aleatoriamente.'
            ]
            recompensa = lista_recompensas[rolagem_d6 - 1]
            await interaction.response.send_message(f"> 1d6 → ` {rolagem_d6} ` "
                                                    f"\n{recompensa}")


def setup(bot: commands.Bot):
    bot.add_cog(PenaltyOrRewardCommand(bot))
