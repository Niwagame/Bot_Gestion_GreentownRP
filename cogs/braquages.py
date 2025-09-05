# cogs/braquages.py
import discord
from discord.ext import commands
from utils.timers import start_timer

class Braquages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # ATM : 30 minutes entre chaque (minuteur simple)
    # =========================
    @commands.command(name="atm")
    async def atm(self, ctx):
        await ctx.message.delete()
        await start_timer(ctx, "ATM", 30, police_wait_min=0)

    # =========================
    # Supérettes : 1h entre chaque + minuteur police 10 min
    # =========================
    @commands.command(name="sup")
    async def superette(self, ctx):
        await ctx.message.delete()
        await start_timer(ctx, "Supérette", 60, police_wait_min=10)

    # =========================
    # Fleeca : minuteur simple + police 10 min (PAS de vérifs)
    # =========================
    @commands.command(name="fle")
    async def fleeca(self, ctx):
        await ctx.message.delete()
        await start_timer(ctx, "Fleeca", 24 * 60, police_wait_min=10)

    # =========================
    # Conteneurs : 1h + police 10 min
    # =========================
    @commands.command(name="cont", aliases=["conteneurs"])
    async def conteneurs(self, ctx):
        await ctx.message.delete()
        await start_timer(ctx, "Conteneurs", 60, police_wait_min=10)

    # =========================
    # Cambriolage : 1h30 + police 10 min (PAS de vérifs)
    # =========================
    @commands.command(name="cam")
    async def cambriolage(self, ctx):
        await ctx.message.delete()
        await start_timer(ctx, "Cambriolage", 90, police_wait_min=10)

    # =========================
    # Coffre-fort : 1h30 + police 10 min
    # =========================
    @commands.command(name="cf")
    async def coffre_fort(self, ctx):
        await ctx.message.delete()
        await start_timer(ctx, "Coffre-Fort", 90, police_wait_min=10)

    # =========================
    # Entrepôt : 24h + police 10 min
    # =========================
    @commands.command(name="ent")
    async def entrepot(self, ctx):
        await ctx.message.delete()
        await start_timer(ctx, "Entrepot", 24 * 60, police_wait_min=10)

    # =========================
    # Train : 24h + police 10 min
    # =========================
    @commands.command(name="tra")
    async def train(self, ctx):
        await ctx.message.delete()
        await start_timer(ctx, "Train", 24 * 60, police_wait_min=10)

    # =========================
    # Bijouterie : 7 jours + police 10 min (PAS de vérifs)
    # =========================
    @commands.command(name="bij")
    async def bijouterie(self, ctx):
        await ctx.message.delete()
        await start_timer(ctx, "Bijouterie", 7 * 24 * 60, police_wait_min=10)

async def setup(bot):
    await bot.add_cog(Braquages(bot))
