import discord

from database.DataBase import DataBase
from app.utilities.warningmessages import send_warning


class PlayerListPages(discord.ui.View):
    def __init__(self, pagina_atual=1, content=None, nd=0):
        super().__init__()
        self.paginaAtual = pagina_atual
        self.paginasTotais = 1
        self.content = content
        self.nd = nd
                
        back_button = discord.ui.Button(label="Anterior",
                                        style=discord.ButtonStyle.grey
                                        )
        next_button = discord.ui.Button(label="Próximo", 
                                        style=discord.ButtonStyle.grey
                                        )
        
        self.atualizarPagina()

        back_button.callback = self.button_callback_back
        next_button.callback = self.button_callback_next

        if self.paginaAtual == 1:
            back_button.disabled = True
        if self.paginaAtual == self.paginasTotais:
            next_button.disabled = True

        self.add_item(back_button)
        self.add_item(next_button)


    async def button_callback_back(self, interaction: discord.Interaction):
        self.paginaAtual -= 1
        self.atualizarPagina()
        await interaction.response.edit_message(content="", embed=self.embed, view=PlayerListPages(pagina_atual=self.paginaAtual, content=self.content))
        
    async def button_callback_next(self, interaction: discord.Interaction):
        self.paginaAtual += 1
        self.atualizarPagina()
        await interaction.response.edit_message(content="", embed=self.embed, view=PlayerListPages(pagina_atual=self.paginaAtual, content=self.content))

    def atualizarPagina(self):
        self.embed = discord.Embed(color=0x800000)
        if self.nd == 0:
            self.paginasTotais = 2
            for i in range(((self.paginaAtual-1)*10)+1, (self.paginaAtual*10)+1):
                qnt_characters = 0
                try:
                    qnt_characters = len(self.content[i])
                except:
                    pass

                self.embed.add_field(name=f"Nível do Personagem: {i}", value=f"Quantidade de personagens deste nível: {qnt_characters}", inline=False)
        else:
            qnt_characters = 0
            try:
                qnt_characters = len(self.content[self.nd])
            except:
                pass
            self.paginasTotais = (qnt_characters // 10) + 1
            texto_final = ''
            for i in range(((self.paginaAtual-1)*10), (self.paginaAtual*10)+1):
                try:
                    personagem = self.content[self.nd][i]
                except:
                    break
                texto_final += f"- {personagem}\n"
            self.embed.add_field(name=f"Personagens de {self.nd}° Nível:", value=texto_final, inline=False)
            if qnt_characters == 0:
                self.embed.add_field(name=f"Não há personagens neste nível.", value="", inline=False)
        self.embed.set_footer(text=f"Página atual: {self.paginaAtual}/{self.paginasTotais}")