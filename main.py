# main.py
import discord
from discord.ext import commands
from config import DISCORD_TOKEN

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_cogs():
    for ext in ("cogs.core", "cogs.braquages", "cogs.crud", "cogs.visas"):
        try:
            await bot.load_extension(ext)
        except Exception as e:
            print(f"Erreur de chargement {ext}: {e}")

@bot.event
async def setup_hook():
    await load_cogs()

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
