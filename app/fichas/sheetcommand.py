import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from client import client

from app.utilities.warningmessages import send_warning
from app.utilities.configreader import ConfigReader
from database.DataBase import DataBase

from app.fichas.sheetcontroller import SheetController
from app.fichas.sheetmodel import SheetModel

skill_list = ["Acrobacia", "Atletismo", "Atuação", "Cavalgar", "Cura", "Diplomacia", "Enganação", "Fortitude", "Furtividade", "Iniciativa", "Intimidação", "Intuição", "Investigação", "Luta", "Percepção", "Pontaria", "Reflexos", "Sobrevivência", "Vontade", "+Perícias"]
slash_sheets_group = SlashCommandGroup("t20-ficha", "Registre, configure e edite sua ficha de personagem T20 no servidor.")

async def get_more_skills(ctx: discord.AutocompleteContext):
    try:
        user_id = ctx.interaction.user.id
        guild_id = ctx.interaction.guild.id
        user_sheets = DataBase.dbRef.child(f"Fichas:{guild_id}/P:{user_id}").get()
        active_sheet = user_sheets[f'Config:{user_id}']['ActiveSheet']
        oficios = user_sheets[active_sheet]["Ofícios"]
        if ctx.options['pericia'] == '+Perícias':
            return ["Adestramento", "Conhecimento", "Guerra", "Jogatina", "Ladinagem", "Misticismo", "Nobreza", f"Ofício1 ({oficios.get('Ofício_1', ' -- ')})", f"Ofício2 ({oficios.get('Ofício_2', ' -- ')})", f"Ofício3 ({oficios.get('Ofício_3', ' -- ')})", f"Ofício4 ({oficios.get('Ofício_4', ' -- ')})", f"Ofício5 ({oficios.get('Ofício_5', ' -- ')})", f"Ofício6 ({oficios.get('Ofício_6', ' -- ')})", f"Ofício7 ({oficios.get('Ofício_7', ' -- ')})", "Pilotagem", "Religião"]
        return []
    except Exception as e:
        print(e)
        if ctx.options['pericia'] == '+Perícias':
            return ["Adestramento", "Conhecimento", "Guerra", "Jogatina", "Ladinagem", "Misticismo", "Nobreza", "Ofício1", "Ofício2", "Ofício3", "Ofício4", "Ofício5", "Ofício6", "Ofício7", "Pilotagem", "Religião"]
        return []

async def get_character_list(ctx: discord.AutocompleteContext):
    try:
        user_id = ctx.interaction.user.id
        guild_id = ctx.interaction.guild.id
        user_sheets = DataBase.dbRef.child(f"Fichas:{guild_id}/P:{user_id}").get()

        character_list = list(user_sheets)
        character_list = [x for x in character_list if x != f'Config:{user_id}']
        return character_list
    except:
        return []

class SheetCommand(commands.Cog):
    sheets = slash_sheets_group
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.sheet_controller = SheetController()
        self.config = ConfigReader.get_config()

    @sheets.command(
        description="Lista as fichas que você possui, você pode escolher uma para manter como ativa."
    )
    async def ativar(self, interaction: discord.Interaction, personagem: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_character_list))):
        if not await self.__checkServer(interaction=interaction):
            return

        result = self.sheet_controller.activate_sheet(user=interaction.user, guild=interaction.guild, character=personagem)
        if not result:
            await send_warning(interaction, "ERROR", f'Falha ao ativar a ficha. Tente novamente.')
            return
        if result == "Sheet is already activated.":
            await send_warning(interaction, "CAUTION", f'A ficha **"{personagem}"** já está ativada.')
            return
        await send_warning(interaction, "SUCCESSFUL", f'Ficha **"{personagem}"** ativada com sucesso.')

    @sheets.command(
        description="Lista as fichas que você possui, você pode escolher uma para excluir."
    )
    async def excluir(self, interaction: discord.Interaction, personagem: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_character_list))):
        if not await self.__checkServer(interaction=interaction):
            return

        result = self.sheet_controller.delete_sheet(user=interaction.user, guild=interaction.guild, character=personagem)
        if not result:
            await send_warning(interaction, "ERROR", f'Falha ao excluir a ficha. Tente novamente.')
            return
        await send_warning(interaction, "SUCCESSFUL", f'Ficha **"{personagem}"** excluida com sucesso.')
    
    @sheets.command(
        description="Apresenta a ficha do personagem ativo."
    )
    async def enviar(self, interaction: discord.Interaction, botoes_visiveis: bool = True, invisivel: bool = True):
        if not await self.__checkServer(interaction=interaction):
            return
        
        embed, buttons = self.sheet_controller.view_sheet(user=interaction.user, guild=interaction.guild)
        buttons = None if not botoes_visiveis else buttons
        if not embed:
            await send_warning(interaction, "ERROR", "Erro ao apresentar a ficha. Você pode não possuir uma ficha registrada.")
            return
        await interaction.response.send_message("", embed=embed, view=buttons, ephemeral=invisivel)

    @sheets.command(
        description="Apaga todas as suas fichas do banco de dados."
    )
    async def limpar(self, interaction: discord.Interaction):
        if not await self.__checkServer(interaction=interaction):
            return
        
        self.sheet_controller.clear_sheets(user=interaction.user, guild=interaction.guild)
        await send_warning(interaction, "SUCCESSFUL", "Todas as fichas foram limpas com sucesso.")

    @sheets.command(
        description="Mostra todas as perícias do personagem ativo."
    )
    async def pericias(self, interaction: discord.Interaction, invisivel: bool = True):
        if not await self.__checkServer(interaction=interaction):
            return

        try:
            embed_pericias = self.sheet_controller.show_skills(user=interaction.user, guild=interaction.guild)
            if not embed_pericias:
                await send_warning(interaction, "ERROR", "Erro ao mostrar suas perícias. Você pode não possuir uma ficha registrada.")
                return
            await interaction.response.send_message("", embed=embed_pericias, ephemeral=invisivel)
        except Exception as e:
            print(e)
            await send_warning(interaction, "ERROR", "Falha ao mostrar as perícias. É possível que o texto tenha excedido o limite de 1024 caracteres.")

    @sheets.command(
        description="Muda a cor da listra à direita da Embed para o personagem ativo."
    )
    async def cor(self, interaction: discord.Interaction, cor: str):
        try:
            new_color = int(cor, 16)
            if not self.sheet_controller.change_color(user=interaction.user, guild=interaction.guild, new_color=new_color):
                await send_warning(interaction, "ERROR", "Erro ao mudar a cor da ficha. Você pode não possuir uma ficha registrada.")
                return
            await send_warning(interaction, "SUCCESSFUL", "Sucesso ao alterar a cor da ficha do personagem ativo atualmente.")
        except Exception as e:
            await send_warning(interaction, "ERROR", "Erro ao definir a cor, lembre-se que ela deve estar em hexadecimal (Exemplo: 0x800000).")
            print(e)

    @sheets.command(
        description="Apresenta a quantidade de fichas cada ND. Ao selecionar ND, apresenta as fichas do ND selecionado."
    )
    async def listar(self, interaction: discord.Interaction, nd: discord.Option(int, choices=range(0, 21)) = 0):
        embed, view = self.sheet_controller.list_server_sheets(guild=interaction.guild, nd=nd)
        await interaction.response.send_message("", embed=embed, view=view, ephemeral=True)

    @sheets.command(
        description="Faz uma rolagem de uma perícia conforme os bônus da ficha do personagem ativo."
    )
    async def rolar(self, interaction: discord.Interaction, pericia: discord.Option(str, choices=skill_list), outras_pericias: discord.Option(str, autocomplete=discord.utils.basic_autocomplete(get_more_skills)) = None, bonus: int = 0, metodo: discord.Option(str, choices=["Apenas um dado", "Dois dados e melhor resultado", "Dois dados e pior resultado"]) = "Apenas um dado"):
        if pericia == '+Perícias':
            pericia = outras_pericias

            if not pericia:
                await send_warning(interaction, "CAUTION", "Ao selecionar '+Perícias', você deve selecionar uma perícia em outro campo.")
                return
        
        embed = self.sheet_controller.roll_skill(user=interaction.user, guild=interaction.guild, pericia=pericia, bonus=bonus, metodo=metodo)
        if not embed:
            await send_warning(interaction, "CAUTION", "Erro ao realizar a rolagem. Pode ser que você não seja treinado em uma perícia onde é obrigatório ser treinado.")
            return
        await interaction.response.send_message("", embed=embed)
 
    @sheets.command(
        description="Adiciona ou atualiza uma ficha de personagem."
    )
    async def registrar(self, interaction: discord.Interaction, ficha: discord.Attachment, imagem: discord.Attachment = None):
        if not await self.__checkServer(interaction=interaction):
            return
        if not ficha.content_type == "application/pdf":
            await send_warning(interaction, "CAUTION", "Não foi possível reconhecer a ficha como um arquivo PDF.")
            return
        if imagem and not imagem.content_type.startswith("image/"):
            await send_warning(interaction, "CAUTION", "Não foi possível reconhecer a imagem como um arquivo de imagem.")
            return
        
        sheet_model = SheetModel()
        try:
            await interaction.response.defer(ephemeral=True)
            pdf = await ficha.read()
            sheet_values = self.sheet_controller.read_pdf(file=pdf, server_id=interaction.guild.id)
            imagem_url = imagem.proxy_url if imagem else None
            sheet_model.setSheet(guild_id=interaction.guild.id, sheet_values=sheet_values, imagem_url=imagem_url)

            sheet = sheet_model.getSheet()
            self.sheet_controller.send_sheet_to_database(sheet_values=sheet, character_name=sheet["Nome"], user=interaction.user, guild=interaction.guild)
            await send_warning(interaction, "SUCCESSFUL", "Ficha enviada com sucesso.", followup=True)

        except Exception as e:
            print(f"Erro ao enviar a ficha: {e}")
            await send_warning(interaction, "ERROR", "Erro ao enviar a ficha.", followup=True)

    @sheets.command(
        description="Lista todos os comandos e apresenta uma explicação do comando selecionado."
    )
    async def ajuda(self, interaction: discord.Interaction, comando: discord.Option(str, choices=[command.name for command in sheets.subcommands])):
        if not await self.__checkServer(interaction=interaction):
            return
        
        dict_commands = {
            "ativar": {
                "name": "Ativar Ficha",
                "description": "Lista as fichas que você possui, você pode escolher uma para manter como ativa. Uma ficha ativa pode ser modificada por outros comandos.",
                "giflink": "https://media.discordapp.net/attachments/1234193693775499314/1234200209387557016/Ativar.gif?ex=662fde04&is=662e8c84&hm=7a2d65525a961ee24a2d40e4e0ba8ef210f508ec1308472802c930c23b1d3d41&=&width=1201&height=675"
            },
            "excluir": {
                "name": "Excluir Ficha",
                "description": "Lista as fichas que você possui, você pode escolher uma para excluir.",
                "giflink": "https://media.discordapp.net/attachments/1234193693775499314/1234196214388494397/Excluir.gif?ex=662fda4b&is=662e88cb&hm=59241662f45b5c6405ed0bce12b378faf40d4ce3160dd7f83ca669c9994f79b7&=&width=1201&height=675"
            },
            "enviar": {
                "name": "Enviar Ficha ",
                "description": "Apresenta a ficha ativa no chat.\n- `botoes_visiveis`: Define se os botões de controle da ficha estarão visiveis (True) ou não estarão visiveis (False) ao enviar a ficha. | Padrão: True\n- `invisivel`: Define se a ficha estará visivel apenas para você (True) ou para todos no chat (False). | Padrão: True",
                "giflink": "https://media.discordapp.net/attachments/1234193693775499314/1234195346406641734/Enviar.gif?ex=662fd97c&is=662e87fc&hm=9a5054496bd24ae3e3287fcf42e2ab0a81596d1e568ed7704c9a040107f15cfa&=&width=1201&height=675"
            },
            "limpar": {
                "name": "Excluir Todas As Fichas",
                "description": "Exclui todas as fichas registradas do usuário.\n- `invisivel`: Define se a lista de perícias estará visivel apenas para você (True) ou para todos no chat (False). | Padrão: True",
                "giflink": "https://media.discordapp.net/attachments/1234193693775499314/1234197901140562023/Limpar.gif?ex=662fdbdd&is=662e8a5d&hm=b1e71915ed0a5f66480dfad7277f74faefaaf384cb853fb7b0c4db8696ab3947&=&width=1201&height=675"
            },
            "pericias": {
                "name": "Mostrar Perícias",
                "description": "Lista todas as perícias da ficha ativa e seus respectivos valores.\n- `invisivel`: Define se a lista de perícias estará visivel apenas para você (True) ou para todos no chat (False). | Padrão: True",
                "giflink": "https://media.discordapp.net/attachments/1234193693775499314/1234196975361064960/Pericias.gif?ex=662fdb01&is=662e8981&hm=64235369c09c2469d120b723c49c41d1af4e66918cb9e39e53fec238d131cbff&=&width=1201&height=675"
            },
            "cor": {
                "name": "Mudar Cor Da Ficha",
                "description": "Muda a cor da `embed` onde a ficha ativa é apresentada.\n- `cor`: A nova cor para a ficha. A cor deve ser representada em um valor hexadecimal após '0x', por exemplo: '0xF0F8FF' (AliceBlue).",
                "giflink": "https://media.discordapp.net/attachments/1234193693775499314/1234197901715050567/Mudar_cor.gif?ex=662fdbde&is=662e8a5e&hm=6fa5bfd7ff5d4673e9599ad531aa63ef431e255e82a18754134928b157666648&=&width=1201&height=675"
            },
            "listar": {
                "name": "Listar Todas As Fichas",
                "description": "Lista todas as fichas do servidor que estão registradas com o ND selecionado. Caso o valor de 'nd' seja 0, ao invés disso, lista a quantidade de fichas registradas em cada nd.\n- `nd`: O ND qual você deseja ver as fichas registradas. | Padrão: 0",
                "giflink": "https://media.discordapp.net/attachments/1234193693775499314/1234203701711999106/Listar.gif?ex=662fe144&is=662e8fc4&hm=68a69eefb5c06668597a562661096190b7a0b2f1b8d197a38fa0d401f56d3413&=&width=759&height=426"
            },
            "rolar": {
                "name": "Rolar Perícia",
                "description": "Faz uma rolagem de perícia conforme os bônus da ficha ativa. Ao selecionar um ofício, ele estará na ordem apresentada pelo comando */ficha pericias*.\n- `pericia`: A perícia a qual será realizada a rolagem. Você pode selecionar *+Perícias* para ver outras perícias no campo seguinte.\n- `outras_pericias`: Por uma limitação do discord, as pericias devem ser separadas em dois campos. Este campo possui apenas perícias onde é necessário ser treinado para realizar a rolagem.\n- `bonus`: O bônus numérico que será somado ao resultado final da perícia. | Padrão: 0\n- `metodo`: A maneira em que os dados serão rolados. | Padrão: Apenas um dado",
                "giflink": "https://media.discordapp.net/attachments/1234193693775499314/1234197029501014087/Rolar_Pericias.gif?ex=662fdb0e&is=662e898e&hm=9adf24cd3e38c930135ba75629eb052c4a4b36e0ec71845036b2523af4527463&=&width=605&height=339"
            },
            "registrar": {
                "name": "Registrar Perícia",
                "description": "Adiciona uma nova ficha ao banco de dados, ou então, atualiza uma ficha antiga que possua o mesmo nome. O nome da ficha é definido pelo campo do nome do personagem dentro do PDF.\n- `ficha`: O arquivo em PDF da ficha; deve ser usado o modelo mais recente do servidor.\n- `imagem`: Um arquivo de imagem com a imagem do personagem.",
                "giflink": "https://media.discordapp.net/attachments/1234193693775499314/1234193741972111421/Registrar.gif?ex=662fd7fe&is=662e867e&hm=8385c55e914b351e8ef43f62fe3e89b8822020a099838bdd030717be3462fb5a&=&width=1201&height=675"
            }
        }
        
        embed = discord.Embed(color=0x483D8B)
        embed.set_author(name=client.user.name, icon_url=client.user.avatar)
        embed.set_footer(text="Bot construido pelo inventor Kuro'McDowell. Para dúvidas, me contate!")
        embed.add_field(name=dict_commands[comando]["name"], value=dict_commands[comando]["description"], inline=False)
        embed.set_image(url=dict_commands[comando]["giflink"])
        await interaction.response.send_message("", embed=embed, ephemeral=True)

    async def __checkServer(self, interaction: discord.Interaction):
        guild_id = interaction.guild_id
        if str(guild_id) not in self.config:
            await send_warning(interaction, "CAUTION", "Você não pode usar este comando através do canal de mensagens privadas do bot, ou através de um servidor que não possui sistema de fichas ativado.")
            return False
        return True

def setup(bot: commands.Bot):
    bot.add_cog(SheetCommand(bot))
