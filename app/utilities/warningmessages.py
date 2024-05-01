import discord

# Dicionário para armazenar as cores de cada 'Warning'.
WARNING_COLORS = {
    "ERROR": 0x8B0000,
    "CAUTION": 0xFFD700,
    "SUCCESSFUL": 0x00FA9A
}

async def send_warning(destination, warntype, message, followup=False, ephemeral=True):
    color = WARNING_COLORS.get(warntype.upper(), discord.Color.default())
    embed = discord.Embed(color=color)
    embed.add_field(name="", value=str(message))

    if isinstance(destination, discord.User):
        await destination.send(embed=embed)
            
    elif isinstance(destination, discord.commands.context.ApplicationContext) or isinstance(destination, discord.interactions.Interaction):
        if not followup:
            await destination.response.send_message(embed=embed, ephemeral=ephemeral)
        else:
            await destination.followup.send(embed=embed)
