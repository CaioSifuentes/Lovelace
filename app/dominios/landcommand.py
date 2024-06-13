import discord
from discord.ext import commands
from random import randint

from app.utilities.warningmessages import send_warning
from app.utilities.configreader import ConfigReader

from app.moderacao.views.reportmodal import ReportModal


class LandCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.config = ConfigReader.get_config()

    @commands.slash_command(
            title='Gerar Terreno de Domínio',
            description='Gera qual será o terreno de um domínio.'
            )
    async def terreno(self, interaction: discord.Interaction):
        land = randint(1, 7)
        water = randint(1, 4)
        table = {
            1: ("Colinas", "https://media.discordapp.net/attachments/1234193693775499314/1250939841240105011/Colinas.png?ex=666cc403&is=666b7283&hm=38787ae31e701ca45392cdf5200299f33ab4cc8c922d99ccdccede1e886c1f07&=&format=webp&quality=lossless&width=675&height=675"),
            2: ("Deserto", "https://media.discordapp.net/attachments/1234193693775499314/1250939841701744731/Deserto.png?ex=666cc403&is=666b7283&hm=ed2ccf4813ce041a2a12ee94cd865f1511f92f5a39d96397f9a855027298ede6&=&format=webp&quality=lossless&width=675&height=675"),
            3: ("Floresta", "https://media.discordapp.net/attachments/1234193693775499314/1250939842137821205/Florest.png?ex=666cc403&is=666b7283&hm=5e996f628f542a1fb3b1dd9ded04efeafa7fd9f946a571c3675e2ae61d0d5a55&=&format=webp&quality=lossless&width=675&height=675"),
            4: ("Montanhas", "https://media.discordapp.net/attachments/1234193693775499314/1250939842582286417/Montanhas.png?ex=666cc403&is=666b7283&hm=8131afb1b84e4fb2ffee6b679ce9005b39f6a98848979e4dc374e1454b90f364&=&format=webp&quality=lossless&width=675&height=675"),
            5: ("Pântano", "https://media.discordapp.net/attachments/1234193693775499314/1250939843001974875/Pantano.png?ex=666cc403&is=666b7283&hm=b4d24284f6bc334ea165dcc79b2b45a52a0df997b2b52dcdfe384caad7c193c0&=&format=webp&quality=lossless&width=675&height=675"),
            6: ("Planície", "https://media.discordapp.net/attachments/1234193693775499314/1250939843492577421/Planicies.png?ex=666cc404&is=666b7284&hm=f7d34ee49f4b5e1af80fd388b5059c8aaeabbe67ffbe5172475b53e083a9594f&=&format=webp&quality=lossless&width=675&height=675"),
            7: ("Subterrâneo", "https://media.discordapp.net/attachments/1234193693775499314/1250939844008607764/Subterraneo.png?ex=666cc404&is=666b7284&hm=5d61c6302cf5c50c0e19b4eae9b8f77f187f3bca249096bf7fd08d89043d8c4e&=&format=webp&quality=lossless&width=675&height=675")
        }

        if land not in [2, 7]:
            if water % 2 == 0:
                result = "O domínio **possui** conexão com rio/mar."
            else:
                result = "O domínio **não possui** conexão com rio/mar."
        else:
            if water == 4:
                result = "O domínio **possui** conexão com rio/mar."
            else:
                result = "O domínio **não possui** conexão com rio/mar."

        embed = discord.Embed(color=0x11FF44)
        embed.add_field(name="Tipo de Terreno", value=f"` {land} ` ⟵ [{land}] 1d7\nO domínio está localizado em: **{table[land][0]}**", inline=False)
        embed.add_field(name="Conexão com Rio/Mar", value=f"` {water} ` ⟵ [{water}] 1d4\n{result}", inline=False)
        try:
            embed.set_image(url=table[land][1])
        except:
            pass
        await interaction.response.send_message(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(LandCommand(bot))