import discord
from discord import app_commands
from discord.ext import commands
import pymysql
import asyncio
from datetime import datetime, timedelta
from tabulate import tabulate  # Importer le module tabulate pour un affichage formaté
from typing import List  # Importation pour les types de retour

# Initialise le bot avec des intentions spécifiques pour les interactions et les messages
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Votre Token Bot (remplacez cette valeur par votre token réel)
TOKEN = 'MTI3MDM2MDczNjYzOTYxOTExNQ.G0-Xz-.-FoEbqYPy4HhddxhyYQBdqHdNPIX4OBbyLE-bA'

# Informations de connexion à la base de données
DB_HOST = 'mysql1.par1.adky.net'
DB_PORT = 3306
DB_USER = 'u19886_CrbcItQqu1'
DB_PASSWORD = 'rk=b.XyIqAm.EJ8ZIa@yPaHf'  # Remplacez par votre mot de passe
DB_NAME = 's19886_Bot'

# Fonction pour se connecter à la base de données
def connect_to_db():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# Fonction pour récupérer l'ID du salon et l'ID du message
def get_channel_and_message_id(item_type: str):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT ID_Salon, ID_Message FROM Message WHERE Nom = %s", (item_type,))
            result = cursor.fetchone()
            return result['ID_Salon'], result['ID_Message'] if result else (None, None)
    finally:
        connection.close()

# Fonction pour mettre à jour l'ID du message dans la table Message
def update_message_id(item_type: str, new_message_id):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE Message SET ID_Message = %s WHERE Nom = %s", (new_message_id, item_type))
            connection.commit()
    finally:
        connection.close()

# Fonction pour afficher la table "Armes" avec un formatage propre
async def display_armes_table(channel):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Armes")
            armes = cursor.fetchall()

            # Créer un tableau formaté
            headers = ["Nom", "Groupe", "Avec P", "Sans P"]
            table = [[arme['Nom'], arme['Groupe'] or "-", arme['AvecP'] or "-", arme['SansP'] or "-"] for arme in armes]

            # Ajouter un titre avec la date actuelle
            date_now = datetime.now().strftime('%d/%m/%Y')
            title = f"**Tableau Armes**\n**Date de mise à jour : {date_now}**\n"
            message_content = title + "```" + tabulate(table, headers=headers, tablefmt="grid") + "```"

            # Envoyer le message dans le salon
            sent_message = await channel.send(message_content)

            # Mettre à jour l'ID du message dans la base de données
            update_message_id("Armes", sent_message.id)
    finally:
        connection.close()

# Fonction pour afficher la table "Munitions" avec un formatage propre
async def display_munitions_table(channel):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Munitions")
            munitions = cursor.fetchall()

            # Créer un tableau formaté
            headers = ["Nom", "Groupe", "Prix"]
            table = [[munition['Nom'], munition['Groupe'] or "-", munition['Prix'] or "-"] for munition in munitions]

            # Ajouter un titre avec la date actuelle
            date_now = datetime.now().strftime('%d/%m/%Y')
            title = f"**Tableau Munitions**\n**Date de mise à jour : {date_now}**\n"
            message_content = title + "```" + tabulate(table, headers=headers, tablefmt="grid") + "```"

            # Envoyer le message dans le salon
            sent_message = await channel.send(message_content)

            # Mettre à jour l'ID du message dans la base de données
            update_message_id("Munitions", sent_message.id)
    finally:
        connection.close()

# Fonction pour afficher la table "Drogues" avec un formatage propre
async def display_drogues_table(channel):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Drogues")
            drogues = cursor.fetchall()

            # Créer un tableau formaté
            headers = ["Nom", "Groupe", "Prix Unité", "Prix 100", "Prix 1000"]
            table = [[drogue['Nom'], drogue['Groupe'] or "-", drogue['Prix_Unité'] or "-", drogue['Prix_100'] or "-", drogue['Prix_1000'] or "-"] for drogue in drogues]

            # Ajouter un titre avec la date actuelle
            date_now = datetime.now().strftime('%d/%m/%Y')
            title = f"**Tableau Drogues**\n**Date de mise à jour : {date_now}**\n"
            message_content = title + "```" + tabulate(table, headers=headers, tablefmt="grid") + "```"

            # Envoyer le message dans le salon
            sent_message = await channel.send(message_content)

            # Mettre à jour l'ID du message dans la base de données
            update_message_id("Drogues", sent_message.id)
    finally:
        connection.close()

# Fonction pour afficher la table "Outils" avec un formatage propre
async def display_outils_table(channel):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Outils")
            outils = cursor.fetchall()

            # Créer un tableau formaté
            headers = ["Nom", "Groupe", "Prix Unité", "Prix 100", "Prix 500"]
            table = [[outil['Nom'], outil['Groupe'] or "-", outil['Prix_Unité'] or "-", outil['Prix_100'] or "-", outil['Prix_500'] or "-"] for outil in outils]

            # Ajouter un titre avec la date actuelle
            date_now = datetime.now().strftime('%d/%m/%Y')
            title = f"**Tableau Outils**\n**Date de mise à jour : {date_now}**\n"
            message_content = title + "```" + tabulate(table, headers=headers, tablefmt="grid") + "```"

            # Envoyer le message dans le salon
            sent_message = await channel.send(message_content)

            # Mettre à jour l'ID du message dans la base de données
            update_message_id("Outils", sent_message.id)
    finally:
        connection.close()

# Fonction pour afficher la table "Ventes" avec un formatage propre
async def display_ventes_table(channel):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Ventes")
            ventes = cursor.fetchall()

            # Créer un tableau formaté
            headers = ["Nom", "Groupe", "Drogue"]
            table = [[vente['Nom'], vente['Groupe'] or "-", vente['Drogue'] or "-"] for vente in ventes]

            # Ajouter un titre avec la date actuelle
            date_now = datetime.now().strftime('%d/%m/%Y')
            title = f"**Tableau Ventes**\n**Date de mise à jour : {date_now}**\n"
            message_content = title + "```" + tabulate(table, headers=headers, tablefmt="grid") + "```"

            # Envoyer le message dans le salon
            sent_message = await channel.send(message_content)

            # Mettre à jour l'ID du message dans la base de données
            update_message_id("Ventes", sent_message.id)
    finally:
        connection.close()

# Événement qui se déclenche lorsque le bot est prêt
@bot.event
async def on_ready():
    print(f'{bot.user} est connecté à Discord!')

    try:
        synced = await bot.tree.sync()  # Synchroniser les commandes slash
        print(f"Commandes Slash synchronisées : {len(synced)}")
    except Exception as e:
        print(f"Erreur de synchronisation des commandes Slash : {e}")

    # Affichage des tableaux dans leurs salons respectifs
    for item_type in ["Armes", "Munitions", "Drogues", "Outils", "Ventes"]:
        channel_id, _ = get_channel_and_message_id(item_type)
        if channel_id:
            channel = bot.get_channel(channel_id)
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

# Commande slash pour afficher le stock
@bot.tree.command(name="stock", description="Affiche le stock actuel")
async def display_stock(interaction: discord.Interaction):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT item_name, quantity FROM Stock")
            stock_items = cursor.fetchall()
            stock_message = "**Stock actuel :**\n"
            for item in stock_items:
                stock_message += f"- {item['item_name']}: {item['quantity']}\n"
            
            # Envoyer un message éphémère
            await interaction.response.send_message(stock_message, ephemeral=True)
    finally:
        connection.close()

# Fonction timer pour les activités
async def timer(ctx, duration, message_content, author_name):
    end_time = datetime.now() + timedelta(minutes=duration)
    message = await ctx.send(f"{message_content}, finira à **{end_time.strftime('%Y-%m-%d %H:%M:%S')}** et fait par **{author_name}**")
    await asyncio.sleep(duration * 60)  # Attend la fin du minuteur
    try:
        await message.delete()  # Supprime le message du minuteur
    except discord.NotFound:
        pass

# Diminuer le stock d'un article spécifique
def decrease_stock(item_name, amount):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT quantity FROM Stock WHERE item_name = %s", (item_name,))
            result = cursor.fetchone()
            if result and result['quantity'] >= amount:
                new_quantity = result['quantity'] - amount
                cursor.execute("UPDATE Stock SET quantity = %s WHERE item_name = %s", (new_quantity, item_name))
                connection.commit()
                return True
            return False
    finally:
        connection.close()

# Démarrer un timer avec gestion de stock
async def start_timer(ctx, activity_name, first_duration, second_timer_duration=0, item_name=None):
    author_name = ctx.author.display_name  # Obtient le surnom de l'utilisateur
    first_message_content = f"Minuteur pour **{activity_name}** commencé par {author_name}"
    
    # Vérifier et diminuer le stock si nécessaire
    if item_name and not decrease_stock(item_name, 1):
        await ctx.send(f"Désolé, pas assez de stock pour {item_name}.")
        return

    if second_timer_duration > 0:
        second_message_content = f"Vous pourriez partir de {activity_name} par {author_name}"
        await asyncio.gather(
            timer(ctx, first_duration, first_message_content, author_name),
            timer(ctx, second_timer_duration, second_message_content, author_name)
        )
    else:
        await timer(ctx, first_duration, first_message_content, author_name)

# Commandes pour démarrer les activités et gérer le stock
@bot.command(name='atm')
async def atm(ctx):
    await ctx.message.delete()
    await start_timer(ctx, "ATM", 1.5 * 60, 0, item_name="clé ATM")

@bot.command(name='cam')
async def cambriolage(ctx):
    await ctx.message.delete()
    await start_timer(ctx, "Cambriolage", 1.5 * 60, 10, item_name="crochetage")
    
@bot.command(name='fle')
async def fleeca(ctx):
    await ctx.message.delete()
    await start_timer(ctx, "Fleeca", 48 * 60, 15, item_name="clée de banque")

@bot.command(name='ent')
async def entrepot(ctx):
    await ctx.message.delete()
    await start_timer(ctx, "Entrepot", 24 * 60, 15, item_name="thermite")

# Autres commandes de minuteur sans gestion de stock
@bot.command(name='sup')
async def superette(ctx):
    await ctx.message.delete()
    await start_timer(ctx, "Supérette", 1.5 * 60, 10)

@bot.command(name='cf')
async def coffre_fort(ctx):
    await ctx.message.delete()
    await start_timer(ctx, "Coffre-Fort", 1.5 * 60, 10)

@bot.command(name='bij')
async def bijouterie(ctx):
    await ctx.message.delete()
    await start_timer(ctx, "Bijouterie", 48 * 60, 15)

@bot.command(name='tra')
async def train(ctx):
    await ctx.message.delete()
    await start_timer(ctx, "Train", 24 * 60, 15)

# Commande champignon 
@bot.command(name='champ')
async def champignon(ctx):
    await ctx.message.delete()
    author_name = ctx.author.display_name
    message = await ctx.send(f"5 champignons plantés par {author_name}, finira dans **50 min**")
    await asyncio.sleep(3000)  # 50 min
    try:
        await message.delete()
    except discord.NotFound:
        pass
    final_message = await ctx.send(f"5 Champignons finis @here par {author_name}")
    await final_message.add_reaction("✅")

# Ajoutez un listener pour la réaction
@bot.event
async def on_reaction_add(reaction, user):
    if user != bot.user and str(reaction.emoji) == '✅':
        message = reaction.message
        if message.content.startswith("5 Champignons finis"):
            await message.delete()

# Fonction pour obtenir la liste des armes pour la commande slash
def get_arme_choices() -> List[str]:
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT Nom FROM Armes")
            armes = cursor.fetchall()
            return [arme['Nom'] for arme in armes]  # On renvoie une liste de noms
    finally:
        connection.close()

# Fonction pour obtenir la liste des munitions pour la commande slash
def get_munition_choices() -> List[str]:
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT Nom FROM Munitions")
            munitions = cursor.fetchall()
            return [munition['Nom'] for munition in munitions]  # On renvoie une liste de noms
    finally:
        connection.close()

# Fonction pour obtenir la liste des drogues pour la commande slash
def get_drogue_choices() -> List[str]:
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT Nom FROM Drogues")
            drogues = cursor.fetchall()
            return [drogue['Nom'] for drogue in drogues]  # On renvoie une liste de noms
    finally:
        connection.close()

# Fonction pour obtenir la liste des outils pour la commande slash
def get_outil_choices() -> List[str]:
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT Nom FROM Outils")
            outils = cursor.fetchall()
            return [outil['Nom'] for outil in outils]  # On renvoie une liste de noms
    finally:
        connection.close()

# Fonction pour obtenir la liste des ventes pour la commande slash
def get_vente_choices() -> List[str]:
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT Nom FROM Ventes")
            ventes = cursor.fetchall()
            return [vente['Nom'] for vente in ventes]  # On renvoie une liste de noms
    finally:
        connection.close()

# Commande pour mettre à jour la table Armes
@bot.tree.command(name="armes", description="Met à jour le tableau des armes")
@app_commands.describe(
    nom="Le nom de l'arme", 
    groupe="Le groupe de l'arme", 
    avec_p="Le prix avec P (ex: '100K')", 
    sans_p="Le prix sans P (ex: '200K')"
)
async def update_armes(
    interaction: discord.Interaction, 
    nom: str, 
    groupe: str = None, 
    avec_p: str = None,  # Changer en str
    sans_p: str = None   # Changer en str
):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            # Vérifie si l'arme existe déjà
            cursor.execute("SELECT * FROM Armes WHERE Nom = %s", (nom,))
            existing_arme = cursor.fetchone()

            if existing_arme:
                # Met à jour l'arme existante
                cursor.execute(
                    "UPDATE Armes SET Groupe = COALESCE(%s, Groupe), AvecP = COALESCE(%s, AvecP), SansP = COALESCE(%s, SansP) WHERE Nom = %s",
                    (groupe, avec_p, sans_p, nom)
                )
                connection.commit()

                # Récupérer l'ID du salon et de l'ancien message
                channel_id, old_message_id = get_channel_and_message_id("Armes")

                if channel_id:
                    channel = bot.get_channel(channel_id)
                    if old_message_id:
                        # Supprimer l'ancien message
                        old_message = await channel.fetch_message(old_message_id)
                        await old_message.delete()

                    # Afficher le tableau mis à jour
                    await display_armes_table(channel)

                # Envoyer une réponse éphémère
                await interaction.response.send_message(f"L'arme '{nom}' a été mise à jour avec succès.", ephemeral=True)
            else:
                # L'arme n'existe pas, envoyer un message d'erreur
                await interaction.response.send_message(f"L'arme '{nom}' n'existe pas dans la base de données.", ephemeral=True)
    finally:
        connection.close()

# Commande pour mettre à jour la table Munitions
@bot.tree.command(name="munitions", description="Met à jour le tableau des munitions")
@app_commands.describe(
    nom="Le nom de la munition", 
    groupe="Le groupe de la munition", 
    prix="Le prix de la munition (ex: '50K')"
)
async def update_munitions(
    interaction: discord.Interaction, 
    nom: str, 
    groupe: str = None, 
    prix: str = None  # Changer en str
):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            # Vérifie si la munition existe déjà
            cursor.execute("SELECT * FROM Munitions WHERE Nom = %s", (nom,))
            existing_munition = cursor.fetchone()

            if existing_munition:
                # Met à jour la munition existante
                cursor.execute(
                    "UPDATE Munitions SET Groupe = COALESCE(%s, Groupe), Prix = COALESCE(%s, Prix) WHERE Nom = %s",
                    (groupe, prix, nom)
                )
                connection.commit()

                # Récupérer l'ID du salon et de l'ancien message
                channel_id, old_message_id = get_channel_and_message_id("Munitions")

                if channel_id:
                    channel = bot.get_channel(channel_id)
                    if old_message_id:
                        # Supprimer l'ancien message
                        old_message = await channel.fetch_message(old_message_id)
                        await old_message.delete()

                    # Afficher le tableau mis à jour
                    await display_munitions_table(channel)

                # Envoyer une réponse éphémère
                await interaction.response.send_message(f"La munition '{nom}' a été mise à jour avec succès.", ephemeral=True)
            else:
                # La munition n'existe pas, envoyer un message d'erreur
                await interaction.response.send_message(f"La munition '{nom}' n'existe pas dans la base de données.", ephemeral=True)
    finally:
        connection.close()

# Commande pour mettre à jour la table Drogues
@bot.tree.command(name="drogues", description="Met à jour le tableau des drogues")
@app_commands.describe(
    nom="Le nom de la drogue", 
    groupe="Le groupe de la drogue", 
    prix_unité="Le prix par unité (ex: '100')",
    prix_100="Le prix pour 100 (ex: '10K')",
    prix_1000="Le prix pour 1000 (ex: '100K')"
)
async def update_drogues(
    interaction: discord.Interaction, 
    nom: str, 
    groupe: str = None, 
    prix_unité: str = None,  # Changer en str
    prix_100: str = None,    # Changer en str
    prix_1000: str = None    # Changer en str
):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            # Vérifie si la drogue existe déjà
            cursor.execute("SELECT * FROM Drogues WHERE Nom = %s", (nom,))
            existing_drogue = cursor.fetchone()

            if existing_drogue:
                # Met à jour la drogue existante
                cursor.execute(
                    "UPDATE Drogues SET Groupe = COALESCE(%s, Groupe), Prix_Unité = COALESCE(%s, Prix_Unité), Prix_100 = COALESCE(%s, Prix_100), Prix_1000 = COALESCE(%s, Prix_1000) WHERE Nom = %s",
                    (groupe, prix_unité, prix_100, prix_1000, nom)
                )
                connection.commit()

                # Récupérer l'ID du salon et de l'ancien message
                channel_id, old_message_id = get_channel_and_message_id("Drogues")

                if channel_id:
                    channel = bot.get_channel(channel_id)
                    if old_message_id:
                        # Supprimer l'ancien message
                        old_message = await channel.fetch_message(old_message_id)
                        await old_message.delete()

                    # Afficher le tableau mis à jour
                    await display_drogues_table(channel)

                # Envoyer une réponse éphémère
                await interaction.response.send_message(f"La drogue '{nom}' a été mise à jour avec succès.", ephemeral=True)
            else:
                # La drogue n'existe pas, envoyer un message d'erreur
                await interaction.response.send_message(f"La drogue '{nom}' n'existe pas dans la base de données.", ephemeral=True)
    finally:
        connection.close()

# Commande pour mettre à jour la table Outils
@bot.tree.command(name="outils", description="Met à jour le tableau des outils")
@app_commands.describe(
    nom="Le nom de l'outil", 
    groupe="Le groupe de l'outil", 
    prix_unité="Le prix par unité (ex: '10')",
    prix_100="Le prix pour 100 (ex: '1K')",
    prix_500="Le prix pour 500 (ex: '5K')"
)
async def update_outils(
    interaction: discord.Interaction, 
    nom: str, 
    groupe: str = None, 
    prix_unité: str = None,  # Changer en str
    prix_100: str = None,    # Changer en str
    prix_500: str = None     # Changer en str
):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            # Vérifie si l'outil existe déjà
            cursor.execute("SELECT * FROM Outils WHERE Nom = %s", (nom,))
            existing_outil = cursor.fetchone()

            if existing_outil:
                # Met à jour l'outil existant
                cursor.execute(
                    "UPDATE Outils SET Groupe = COALESCE(%s, Groupe), Prix_Unité = COALESCE(%s, Prix_Unité), Prix_100 = COALESCE(%s, Prix_100), Prix_500 = COALESCE(%s, Prix_500) WHERE Nom = %s",
                    (groupe, prix_unité, prix_100, prix_500, nom)
                )
                connection.commit()

                # Récupérer l'ID du salon et de l'ancien message
                channel_id, old_message_id = get_channel_and_message_id("Outils")

                if channel_id:
                    channel = bot.get_channel(channel_id)
                    if old_message_id:
                        # Supprimer l'ancien message
                        old_message = await channel.fetch_message(old_message_id)
                        await old_message.delete()

                    # Afficher le tableau mis à jour
                    await display_outils_table(channel)

                # Envoyer une réponse éphémère
                await interaction.response.send_message(f"L'outil '{nom}' a été mis à jour avec succès.", ephemeral=True)
            else:
                # L'outil n'existe pas, envoyer un message d'erreur
                await interaction.response.send_message(f"L'outil '{nom}' n'existe pas dans la base de données.", ephemeral=True)
    finally:
        connection.close()

# Commande pour mettre à jour la table Ventes
@bot.tree.command(name="ventes", description="Met à jour le tableau des ventes")
@app_commands.describe(
    nom="Le nom de la vente", 
    groupe="Le groupe de la vente", 
    drogue="Le nom de la drogue associée"
)
async def update_ventes(
    interaction: discord.Interaction, 
    nom: str, 
    groupe: str = None, 
    drogue: str = None  # Changer en str
):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            # Vérifie si la vente existe déjà
            cursor.execute("SELECT * FROM Ventes WHERE Nom = %s", (nom,))
            existing_vente = cursor.fetchone()

            if existing_vente:
                # Met à jour la vente existante
                cursor.execute(
                    "UPDATE Ventes SET Groupe = COALESCE(%s, Groupe), Drogue = COALESCE(%s, Drogue) WHERE Nom = %s",
                    (groupe, drogue, nom)
                )
                connection.commit()

                # Récupérer l'ID du salon et de l'ancien message
                channel_id, old_message_id = get_channel_and_message_id("Ventes")

                if channel_id:
                    channel = bot.get_channel(channel_id)
                    if old_message_id:
                        # Supprimer l'ancien message
                        old_message = await channel.fetch_message(old_message_id)
                        await old_message.delete()

                    # Afficher le tableau mis à jour
                    await display_ventes_table(channel)

                # Envoyer une réponse éphémère
                await interaction.response.send_message(f"La vente '{nom}' a été mise à jour avec succès.", ephemeral=True)
            else:
                # La vente n'existe pas, envoyer un message d'erreur
                await interaction.response.send_message(f"La vente '{nom}' n'existe pas dans la base de données.", ephemeral=True)
    finally:
        connection.close()

# Ajout des choix pour l'argument 'nom' de la commande slash /armes
@update_armes.autocomplete('nom')
async def armes_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    choices = get_arme_choices()
    filtered_choices = [
        app_commands.Choice(name=arme, value=arme)
        for arme in choices
        if current.lower() in arme.lower()
    ]
    return filtered_choices

# Ajout des choix pour l'argument 'nom' de la commande slash /munitions
@update_munitions.autocomplete('nom')
async def munitions_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    choices = get_munition_choices()
    filtered_choices = [
        app_commands.Choice(name=munition, value=munition)
        for munition in choices
        if current.lower() in munition.lower()
    ]
    return filtered_choices

# Ajout des choix pour l'argument 'nom' de la commande slash /drogues
@update_drogues.autocomplete('nom')
async def drogues_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    choices = get_drogue_choices()
    filtered_choices = [
        app_commands.Choice(name=drogue, value=drogue)
        for drogue in choices
        if current.lower() in drogue.lower()
    ]
    return filtered_choices

# Ajout des choix pour l'argument 'nom' de la commande slash /outils
@update_outils.autocomplete('nom')
async def outils_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    choices = get_outil_choices()
    filtered_choices = [
        app_commands.Choice(name=outil, value=outil)
        for outil in choices
        if current.lower() in outil.lower()
    ]
    return filtered_choices

# Ajout des choix pour l'argument 'nom' de la commande slash /ventes
@update_ventes.autocomplete('nom')
async def ventes_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    choices = get_vente_choices()
    filtered_choices = [
        app_commands.Choice(name=vente, value=vente)
        for vente in choices
        if current.lower() in vente.lower()
    ]
    return filtered_choices

# Exécution du bot
bot.run(TOKEN)
