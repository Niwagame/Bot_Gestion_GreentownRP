import os
import time
import asyncio
from datetime import datetime, timedelta
from typing import List, Optional, Tuple, Sequence

import discord
from discord import app_commands
from discord.ext import commands
import pymysql
from tabulate import tabulate

# =========================
# Config via variables d'environnement
# =========================
TOKEN = os.environ["DISCORD_TOKEN"]  # obligatoire → KeyError si manquant (mieux pour détecter les oublis)

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "greentown")
DB_USER = os.getenv("DB_USER", "botuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "botpass")

# =========================
# Discord intents & bot
# =========================
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # activer aussi côté portail si nécessaire
bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# DB helpers
# =========================
def _new_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )

def connect_to_db(max_attempts: int = 10, delay_s: float = 2.0):
    """Connexion DB avec retry simple."""
    attempts = 0
    while True:
        try:
            return _new_connection()
        except Exception as e:
            attempts += 1
            if attempts >= max_attempts:
                raise
            print(f"[DB] Non prête ({e!r}), tentative {attempts}/{max_attempts} dans {delay_s}s...")
            time.sleep(delay_s)

def db_fetchone(query: str, params: Optional[Sequence] = None):
    conn = connect_to_db()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchone()
    finally:
        conn.close()

def db_fetchall(query: str, params: Optional[Sequence] = None):
    conn = connect_to_db()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchall()
    finally:
        conn.close()

def db_execute(query: str, params: Optional[Sequence] = None):
    conn = connect_to_db()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            conn.commit()
    finally:
        conn.close()

# =========================
# Utilitaires Message/Salon
# =========================
def get_channel_and_message_id(item_type: str) -> Tuple[Optional[int], Optional[int]]:
    row = db_fetchone("SELECT ID_Salon, ID_Message FROM Message WHERE Nom = %s", (item_type,))
    if not row:
        return (None, None)
    return (row.get("ID_Salon"), row.get("ID_Message"))

def update_message_id(item_type: str, new_message_id: int) -> None:
    db_execute("UPDATE Message SET ID_Message = %s WHERE Nom = %s", (new_message_id, item_type))

async def delete_existing_messages(channel: discord.TextChannel, item_type: str) -> None:
    channel_id, message_id = get_channel_and_message_id(item_type)
    # On ne supprime que si c'est bien le même salon
    if channel_id and message_id and channel.id == channel_id:
        try:
            msg = await channel.fetch_message(message_id)
            await msg.delete()
        except discord.NotFound:
            pass

# =========================
# Rendu générique des tableaux
# =========================
async def send_table_for_item_type(
    channel: discord.TextChannel,
    item_type: str,
    sql: str,
    headers: Sequence[str],
    row_mapper,  # function(dict) -> list
    order_note: Optional[str] = None,
) -> None:
    rows = db_fetchall(sql)
    table = [row_mapper(r) for r in rows]
    date_now = datetime.now().strftime("%d/%m/%Y")

    title_lines = [f"**Tableau {item_type}**", f"**Date de mise à jour : {date_now}**"]
    if order_note:
        title_lines.append(order_note)
    title = "\n".join(title_lines) + "\n"

    content = title + "```" + tabulate(table, headers=headers, tablefmt="grid") + "```"
    msg = await channel.send(content)
    update_message_id(item_type, msg.id)

# Spécifiques (mais via la fonction générique ci-dessus)
async def display_armes_table(channel: discord.TextChannel):
    await send_table_for_item_type(
        channel,
        "Armes",
        "SELECT Nom, Groupe, AvecP, SansP FROM Armes ORDER BY ID",
        headers=["Nom", "Groupe", "Avec P", "Sans P"],
        row_mapper=lambda a: [a["Nom"], a.get("Groupe") or "-", a.get("AvecP") or "-", a.get("SansP") or "-"],
    )

async def display_munitions_table(channel: discord.TextChannel):
    await send_table_for_item_type(
        channel,
        "Munitions",
        "SELECT Nom, Groupe, Prix, Prix500 FROM Munitions ORDER BY Nom",
        headers=["Nom", "Groupe", "Prix", "Prix 500"],
        row_mapper=lambda m: [m["Nom"], m.get("Groupe") or "-", m.get("Prix") or "-", m.get("Prix500") or "-"],
    )

async def display_drogues_table(channel: discord.TextChannel):
    await send_table_for_item_type(
        channel,
        "Drogues",
        "SELECT Nom, Groupe, Prix_Unité, Prix_100, Prix_1000 FROM Drogues",
        headers=["Nom", "Groupe", "Prix Unité", "Prix 100", "Prix 1000"],
        row_mapper=lambda d: [d["Nom"], d.get("Groupe") or "-", d.get("Prix_Unité") or "-", d.get("Prix_100") or "-", d.get("Prix_1000") or "-"],
    )

async def display_outils_table(channel: discord.TextChannel):
    await send_table_for_item_type(
        channel,
        "Outils",
        "SELECT Nom, Groupe, Prix_Unité, Prix_100, Prix_500 FROM Outils",
        headers=["Nom", "Groupe", "Prix Unité", "Prix 100", "Prix 500"],
        row_mapper=lambda o: [o["Nom"], o.get("Groupe") or "-", o.get("Prix_Unité") or "-", o.get("Prix_100") or "-", o.get("Prix_500") or "-"],
    )

async def display_ventes_table(channel: discord.TextChannel):
    await send_table_for_item_type(
        channel,
        "Ventes",
        "SELECT Nom, Groupe, Drogue FROM Ventes ORDER BY Drogue ASC",
        headers=["Nom", "Groupe", "Drogue"],
        row_mapper=lambda v: [v["Nom"], v.get("Groupe") or "-", v.get("Drogue") or "-"],
    )

# =========================
# Événements
# =========================
@bot.event
async def on_ready():
    print(f"{bot.user} est connecté à Discord!")

    try:
        synced = await bot.tree.sync()
        print(f"Commandes Slash synchronisées : {len(synced)}")
    except Exception as e:
        print(f"Erreur de synchronisation des commandes Slash : {e}")

    # Affichage des tableaux selon la table Message (ID_Salon / ID_Message)
    for item_type in ["Armes", "Munitions", "Drogues", "Outils", "Ventes"]:
        channel_id, _ = get_channel_and_message_id(item_type)
        if not channel_id:
            continue
        channel = bot.get_channel(channel_id)
        if not isinstance(channel, discord.TextChannel):
            continue

        await delete_existing_messages(channel, item_type)
        if item_type == "Armes":
            await display_armes_table(channel)
        elif item_type == "Munitions":
            await display_munitions_table(channel)
        elif item_type == "Drogues":
            await display_drogues_table(channel)
        elif item_type == "Outils":
            await display_outils_table(channel)
        elif item_type == "Ventes":
            await display_ventes_table(channel)

# =========================
# Slash / stock
# =========================
@bot.tree.command(name="stock", description="Affiche le stock actuel")
async def display_stock(interaction: discord.Interaction):
    rows = db_fetchall("SELECT item_name, quantity FROM Stock")
    if not rows:
        await interaction.response.send_message("Aucun stock.", ephemeral=True)
        return

    lines = ["**Stock actuel :**"]
    lines += [f"- {r['item_name']}: {r['quantity']}" for r in rows]
    await interaction.response.send_message("\n".join(lines), ephemeral=True)

# =========================
# Timers & stock
# =========================
async def timer(ctx: commands.Context, duration_min: float, message_content: str, author_name: str):
    end_time = datetime.now() + timedelta(minutes=duration_min)
    msg = await ctx.send(f"{message_content}, finira à **{end_time.strftime('%Y-%m-%d %H:%M:%S')}** et fait par **{author_name}**")
    await asyncio.sleep(duration_min * 60)
    try:
        await msg.delete()
    except discord.NotFound:
        pass

def decrease_stock(item_name: str, amount: int) -> bool:
    row = db_fetchone("SELECT quantity FROM Stock WHERE item_name = %s", (item_name,))
    if row and row["quantity"] >= amount:
        new_q = row["quantity"] - amount
        db_execute("UPDATE Stock SET quantity = %s WHERE item_name = %s", (new_q, item_name))
        return True
    return False

async def start_timer(ctx: commands.Context, activity_name: str, first_duration: float, second_timer_duration: float = 0, item_name: Optional[str] = None):
    author_name = ctx.author.display_name
    if item_name and not decrease_stock(item_name, 1):
        await ctx.send(f"Désolé, pas assez de stock pour {item_name}.")
        return

    first_msg = f"Minuteur pour **{activity_name}** commencé par {author_name}"
    if second_timer_duration > 0:
        second_msg = f"Vous pourriez partir de {activity_name} par {author_name}"
        await asyncio.gather(
            timer(ctx, first_duration, first_msg, author_name),
            timer(ctx, second_timer_duration, second_msg, author_name),
        )
    else:
        await timer(ctx, first_duration, first_msg, author_name)

# =========================
# Commandes préfixées
# =========================
@bot.command(name="atm")
async def atm(ctx: commands.Context):
    await ctx.message.delete()
    await start_timer(ctx, "ATM", 1.5 * 60, 0, item_name="clé ATM")

@bot.command(name="cam")
async def cambriolage(ctx: commands.Context):
    await ctx.message.delete()
    await start_timer(ctx, "Cambriolage", 1.5 * 60, 10, item_name="crochetage")

@bot.command(name="fle")
async def fleeca(ctx: commands.Context):
    await ctx.message.delete()
    await start_timer(ctx, "Fleeca", 48 * 60, 15, item_name="clée de banque")

@bot.command(name="ent")
async def entrepot(ctx: commands.Context):
    await ctx.message.delete()
    await start_timer(ctx, "Entrepot", 24 * 60, 15, item_name="thermite")

@bot.command(name="sup")
async def superette(ctx: commands.Context):
    await ctx.message.delete()
    await start_timer(ctx, "Supérette", 1.5 * 60, 10)

@bot.command(name="cf")
async def coffre_fort(ctx: commands.Context):
    await ctx.message.delete()
    await start_timer(ctx, "Coffre-Fort", 1.5 * 60, 10)

@bot.command(name="bij")
async def bijouterie(ctx: commands.Context):
    await ctx.message.delete()
    await start_timer(ctx, "Bijouterie", 48 * 60, 15)

@bot.command(name="tra")
async def train(ctx: commands.Context):
    await ctx.message.delete()
    await start_timer(ctx, "Train", 24 * 60, 15)

@bot.command(name="champ")
async def champignon(ctx: commands.Context):
    await ctx.message.delete()
    author_name = ctx.author.display_name
    msg = await ctx.send(f"5 champignons plantés par {author_name}, finira dans **50 min**")
    await asyncio.sleep(50 * 60)
    try:
        await msg.delete()
    except discord.NotFound:
        pass
    final = await ctx.send(f"5 Champignons finis @here par {author_name}")
    await final.add_reaction("✅")

@bot.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User | discord.Member):
    if user != bot.user and str(reaction.emoji) == "✅":
        message = reaction.message
        if message.content.startswith("5 Champignons finis"):
            await message.delete()

# =========================
# Autocomplétions (DB → listes)
# =========================
def get_names(table: str) -> List[str]:
    rows = db_fetchall(f"SELECT Nom FROM {table}")
    return [r["Nom"] for r in rows]

def build_autocomplete(fetch_names_fn):
    async def _inner(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        choices = fetch_names_fn()
        return [
            app_commands.Choice(name=name, value=name)
            for name in choices
            if current.lower() in name.lower()
        ][:25]  # limite Discord
    return _inner

def get_arme_choices() -> List[str]: return get_names("Armes")
def get_munition_choices() -> List[str]: return get_names("Munitions")
def get_drogue_choices() -> List[str]: return get_names("Drogues")
def get_outil_choices() -> List[str]: return get_names("Outils")
def get_vente_choices() -> List[str]: return get_names("Ventes")

# =========================
# Slash de mise à jour (CRUD light)
# =========================
@bot.tree.command(name="armes", description="Met à jour le tableau des armes")
@app_commands.describe(nom="Nom", groupe="Groupe", avec_p="Prix avec P", sans_p="Prix sans P")
async def update_armes(interaction: discord.Interaction, nom: str, groupe: Optional[str] = None, avec_p: Optional[str] = None, sans_p: Optional[str] = None):
    existing = db_fetchone("SELECT 1 FROM Armes WHERE Nom = %s", (nom,))
    if not existing:
        await interaction.response.send_message(f"L'arme '{nom}' n'existe pas.", ephemeral=True)
        return
    db_execute(
        "UPDATE Armes SET Groupe = COALESCE(%s, Groupe), AvecP = COALESCE(%s, AvecP), SansP = COALESCE(%s, SansP) WHERE Nom = %s",
        (groupe, avec_p, sans_p, nom),
    )
    channel_id, old_id = get_channel_and_message_id("Armes")
    if channel_id:
        channel = bot.get_channel(channel_id)
        if isinstance(channel, discord.TextChannel):
            if old_id:
                try:
                    old_msg = await channel.fetch_message(old_id)
                    await old_msg.delete()
                except discord.NotFound:
                    pass
            await display_armes_table(channel)
    await interaction.response.send_message(f"L'arme '{nom}' a été mise à jour.", ephemeral=True)

@update_armes.autocomplete("nom")
async def armes_autocomplete(interaction: discord.Interaction, current: str):
    return await build_autocomplete(get_arme_choices)(interaction, current)

@bot.tree.command(name="munitions", description="Met à jour le tableau des munitions")
@app_commands.describe(nom="Nom", groupe="Groupe", prix="Prix", prix500="Prix pour 500")
async def update_munitions(interaction: discord.Interaction, nom: str, groupe: Optional[str] = None, prix: Optional[str] = None, prix500: Optional[str] = None):
    existing = db_fetchone("SELECT 1 FROM Munitions WHERE Nom = %s", (nom,))
    if not existing:
        await interaction.response.send_message(f"La munition '{nom}' n'existe pas.", ephemeral=True)
        return
    db_execute(
        "UPDATE Munitions SET Groupe = COALESCE(%s, Groupe), Prix = COALESCE(%s, Prix), Prix500 = COALESCE(%s, Prix500) WHERE Nom = %s",
        (groupe, prix, prix500, nom),
    )
    channel_id, old_id = get_channel_and_message_id("Munitions")
    if channel_id:
        channel = bot.get_channel(channel_id)
        if isinstance(channel, discord.TextChannel):
            if old_id:
                try:
                    old_msg = await channel.fetch_message(old_id)
                    await old_msg.delete()
                except discord.NotFound:
                    pass
            await display_munitions_table(channel)
    await interaction.response.send_message(f"La munition '{nom}' a été mise à jour.", ephemeral=True)

@update_munitions.autocomplete("nom")
async def munitions_autocomplete(interaction: discord.Interaction, current: str):
    return await build_autocomplete(get_munition_choices)(interaction, current)

@bot.tree.command(name="drogues", description="Met à jour le tableau des drogues")
@app_commands.describe(nom="Nom", groupe="Groupe", prix_unité="Prix unité", prix_100="Prix 100", prix_1000="Prix 1000")
async def update_drogues(interaction: discord.Interaction, nom: str, groupe: Optional[str] = None, prix_unité: Optional[str] = None, prix_100: Optional[str] = None, prix_1000: Optional[str] = None):
    existing = db_fetchone("SELECT 1 FROM Drogues WHERE Nom = %s", (nom,))
    if not existing:
        await interaction.response.send_message(f"La drogue '{nom}' n'existe pas.", ephemeral=True)
        return
    db_execute(
        "UPDATE Drogues SET Groupe = COALESCE(%s, Groupe), Prix_Unité = COALESCE(%s, Prix_Unité), Prix_100 = COALESCE(%s, Prix_100), Prix_1000 = COALESCE(%s, Prix_1000) WHERE Nom = %s",
        (groupe, prix_unité, prix_100, prix_1000, nom),
    )
    channel_id, old_id = get_channel_and_message_id("Drogues")
    if channel_id:
        channel = bot.get_channel(channel_id)
        if isinstance(channel, discord.TextChannel):
            if old_id:
                try:
                    old_msg = await channel.fetch_message(old_id)
                    await old_msg.delete()
                except discord.NotFound:
                    pass
            await display_drogues_table(channel)
    await interaction.response.send_message(f"La drogue '{nom}' a été mise à jour.", ephemeral=True)

@update_drogues.autocomplete("nom")
async def drogues_autocomplete(interaction: discord.Interaction, current: str):
    return await build_autocomplete(get_drogue_choices)(interaction, current)

@bot.tree.command(name="outils", description="Met à jour le tableau des outils")
@app_commands.describe(nom="Nom", groupe="Groupe", prix_unité="Prix unité", prix_100="Prix 100", prix_500="Prix 500")
async def update_outils(interaction: discord.Interaction, nom: str, groupe: Optional[str] = None, prix_unité: Optional[str] = None, prix_100: Optional[str] = None, prix_500: Optional[str] = None):
    existing = db_fetchone("SELECT 1 FROM Outils WHERE Nom = %s", (nom,))
    if not existing:
        await interaction.response.send_message(f"L'outil '{nom}' n'existe pas.", ephemeral=True)
        return
    db_execute(
        "UPDATE Outils SET Groupe = COALESCE(%s, Groupe), Prix_Unité = COALESCE(%s, Prix_Unité), Prix_100 = COALESCE(%s, Prix_100), Prix_500 = COALESCE(%s, Prix_500) WHERE Nom = %s",
        (groupe, prix_unité, prix_100, prix_500, nom),
    )
    channel_id, old_id = get_channel_and_message_id("Outils")
    if channel_id:
        channel = bot.get_channel(channel_id)
        if isinstance(channel, discord.TextChannel):
            if old_id:
                try:
                    old_msg = await channel.fetch_message(old_id)
                    await old_msg.delete()
                except discord.NotFound:
                    pass
            await display_outils_table(channel)
    await interaction.response.send_message(f"L'outil '{nom}' a été mis à jour.", ephemeral=True)

@update_outils.autocomplete("nom")
async def outils_autocomplete(interaction: discord.Interaction, current: str):
    return await build_autocomplete(get_outil_choices)(interaction, current)

@bot.tree.command(name="ventes", description="Met à jour le tableau des ventes")
@app_commands.describe(nom="Nom", groupe="Groupe", drogue="Drogue associée")
async def update_ventes(interaction: discord.Interaction, nom: str, groupe: Optional[str] = None, drogue: Optional[str] = None):
    existing = db_fetchone("SELECT 1 FROM Ventes WHERE Nom = %s", (nom,))
    if not existing:
        await interaction.response.send_message(f"La vente '{nom}' n'existe pas.", ephemeral=True)
        return
    db_execute(
        "UPDATE Ventes SET Groupe = COALESCE(%s, Groupe), Drogue = COALESCE(%s, Drogue) WHERE Nom = %s",
        (groupe, drogue, nom),
    )
    channel_id, old_id = get_channel_and_message_id("Ventes")
    if channel_id:
        channel = bot.get_channel(channel_id)
        if isinstance(channel, discord.TextChannel):
            if old_id:
                try:
                    old_msg = await channel.fetch_message(old_id)
                    await old_msg.delete()
                except discord.NotFound:
                    pass
            await display_ventes_table(channel)
    await interaction.response.send_message(f"La vente '{nom}' a été mise à jour.", ephemeral=True)

@update_ventes.autocomplete("nom")
async def ventes_autocomplete(interaction: discord.Interaction, current: str):
    return await build_autocomplete(get_vente_choices)(interaction, current)

# =========================
# Run
# =========================
bot.run(TOKEN)
