import discord
from discord.ext.commands import Bot

# Cria a instância de 'client' do bot.
client = Bot(command_prefix=">>!", intents=discord.Intents.all())
