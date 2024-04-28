import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio

# Initialise le bot avec des intentions spécifiques pour les interactions et les messages
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Votre Token Bot (remplacez cette valeur par votre token réel)
TOKEN = 'MTE5MzM0MDAwNDM3MDQ4OTQ0NQ.GsfA8O.GZOfBUF3N7ObNv3UsZYJhE4Yq2Ry7Q_LC-0kUA'

async def timer(ctx, duration, message_content):
    end_time = datetime.now() + timedelta(minutes=duration)
    message = await ctx.send(f"{message_content}, finira à **{end_time.strftime('%Y-%m-%d %H:%M:%S')}**")
    await asyncio.sleep(duration * 60)  # Attend la fin du minuteur
    try:
        await message.delete()  # Supprime le message du minuteur
    except discord.NotFound:
        pass

async def start_timer(ctx, activity_name, first_duration, second_timer_duration=0):
    first_message_content = f"Minuteur pour **{activity_name}** commencé"
    if second_timer_duration > 0:
        second_message_content = f"Vous pourriez partir de {activity_name}"
        await asyncio.gather(
            timer(ctx, first_duration * 60, first_message_content),
            timer(ctx, second_timer_duration, second_message_content)
        )
    else:
        await timer(ctx, first_duration * 60, first_message_content)

# Commande champignon 
@bot.command(name='champ')
async def champignon(ctx):
    await ctx.message.delete()
    message = await ctx.send("5 champignon planté, finira dans **50 min**")
    await asyncio.sleep(3000)  # 1 heure
    try:
        await message.delete()
    except discord.NotFound:
        pass
    final_message = await ctx.send("5 Champignon fini @here")
    await final_message.add_reaction("✅")

# Ajoutez un listener pour la réaction
@bot.event
async def on_reaction_add(reaction, user):
    if user != bot.user and str(reaction.emoji) == '✅':
        message = reaction.message
        if message.content.startswith("5 Champignon fini"):
            await message.delete()

@bot.command(name='atm')
async def atm(ctx):
    await ctx.message.delete()
    await start_timer(ctx, "ATM", 1.5, 0)

@bot.command(name='cam')
async def cambriolage(ctx):
    await ctx.message.delete()
    await start_timer(ctx, "Cambriolage", 1.5, 10)

@bot.command(name='sup')
async def superette(ctx):
    await ctx.message.delete()
    await start_timer(ctx, "Supérette", 1.5, 10)

@bot.command(name='cf')
async def coffre_fort(ctx):
    await ctx.message.delete()
    await start_timer(ctx, "Coffre-Fort", 1.5, 10)

@bot.command(name='ent')
async def entrepot(ctx):
    await ctx.message.delete()
    await start_timer(ctx, "Entrepot", 24, 15)

@bot.command(name='bij')
async def bijouterie(ctx):
    await ctx.message.delete()
    await start_timer(ctx, "Bijouterie", 48, 15)

@bot.command(name='fle')
async def fleeca(ctx):
    await ctx.message.delete()
    await start_timer(ctx, "Fleeca", 48, 15)

@bot.command(name='tra')
async def train(ctx):
    await ctx.message.delete()
    await start_timer(ctx, "Train", 24, 15)

@bot.event
async def on_ready():
    print(f'{bot.user} est connecté à Discord!')

# Exécution du bot
bot.run(TOKEN)
