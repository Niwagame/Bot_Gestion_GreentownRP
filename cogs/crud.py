# cogs/crud.py
from typing import List, Optional

import discord
from discord import app_commands
from discord.ext import commands

from db import fetchall, fetchone, execute
from tables import (
    get_channel_and_message_id,
    display_armes_table,
    display_munitions_table,
    display_drogues_table,
    display_outils_table,
)

# =========================
# Helpers autocomplétion
# =========================
def _get_names(table: str) -> List[str]:
    rows = fetchall(f"SELECT Nom FROM {table}")
    return [r["Nom"] for r in rows]

def _build_autocomplete(fetch_names_fn):
    async def _inner(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        names = fetch_names_fn()
        return [
            app_commands.Choice(name=n, value=n)
            for n in names
            if current.lower() in n.lower()
        ][:25]
    return _inner

def _armes(): return _get_names("armes")
def _munitions(): return _get_names("munitions")
def _drogues(): return _get_names("drogues")
def _outils(): return _get_names("outils")


class Crud(commands.Cog):
    """Slash commands de mise à jour des tableaux (CRUD light)."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # =========================
    # /armes
    # =========================
    @app_commands.command(name="armes", description="Met à jour le tableau des armes")
    @app_commands.describe(
        nom="Nom de l'arme (doit exister)",
        groupe="Groupe (optionnel)",
        propre="Prix argent propre (optionnel)",
        sale="Prix argent sale (optionnel)",
    )
    async def armes(
        self,
        interaction: discord.Interaction,
        nom: str,
        groupe: Optional[str] = None,
        propre: Optional[str] = None,
        sale: Optional[str] = None,
    ):
        exists = fetchone("SELECT 1 FROM armes WHERE Nom=%s", (nom,))
        if not exists:
            await interaction.response.send_message(f"⛔ L'arme **{nom}** n'existe pas.", ephemeral=True)
            return

        execute(
            """UPDATE armes
               SET Groupe = COALESCE(%s, Groupe),
                   Propre = COALESCE(%s, Propre),
                   Sale   = COALESCE(%s, Sale)
             WHERE Nom=%s""",
            (groupe, propre, sale, nom),
        )

        channel_id, _ = get_channel_and_message_id("Armes")
        if channel_id:
            chan = self.bot.get_channel(channel_id)
            if isinstance(chan, discord.TextChannel):
                # Le refresh supprime l'ancien message et poste le nouveau (logique dans tables.py)
                await display_armes_table(chan)

        await interaction.response.send_message(f"✅ L'arme **{nom}** a été mise à jour.", ephemeral=True)

    @armes.autocomplete("nom")
    async def ac_armes(self, interaction: discord.Interaction, current: str):
        return await _build_autocomplete(_armes)(interaction, current)

    # =========================
    # /munitions
    # =========================
    @app_commands.command(name="munitions", description="Met à jour le tableau des munitions")
    @app_commands.describe(
        nom="Nom de la munition (doit exister)",
        groupe="Groupe (optionnel)",
        propre="Prix argent propre (optionnel)",
        sale="Prix argent sale (optionnel)",
    )
    async def munitions(
        self,
        interaction: discord.Interaction,
        nom: str,
        groupe: Optional[str] = None,
        propre: Optional[str] = None,
        sale: Optional[str] = None,
    ):
        exists = fetchone("SELECT 1 FROM munitions WHERE Nom=%s", (nom,))
        if not exists:
            await interaction.response.send_message(f"⛔ La munition **{nom}** n'existe pas.", ephemeral=True)
            return

        execute(
            """UPDATE munitions
               SET Groupe = COALESCE(%s, Groupe),
                   Propre  = COALESCE(%s, Propre),
                   Sale    = COALESCE(%s, Sale)
             WHERE Nom=%s""",
            (groupe, propre, sale, nom),
        )

        channel_id, _ = get_channel_and_message_id("Munitions")
        if channel_id:
            chan = self.bot.get_channel(channel_id)
            if isinstance(chan, discord.TextChannel):
                await display_munitions_table(chan)

        await interaction.response.send_message(f"✅ La munition **{nom}** a été mise à jour.", ephemeral=True)

    @munitions.autocomplete("nom")
    async def ac_munitions(self, interaction: discord.Interaction, current: str):
        return await _build_autocomplete(_munitions)(interaction, current)

    # =========================
    # /drogues
    # =========================
    @app_commands.command(name="drogues", description="Met à jour le tableau des drogues")
    @app_commands.describe(
        nom="Nom (doit exister)",
        groupe="Groupe (optionnel)",
        propre="Prix argent propre (optionnel)",
        sale="Prix argent sale (optionnel)",
    )
    async def drogues(
        self,
        interaction: discord.Interaction,
        nom: str,
        groupe: Optional[str] = None,
        propre: Optional[str] = None,
        sale: Optional[str] = None,
    ):
        exists = fetchone("SELECT 1 FROM drogues WHERE Nom=%s", (nom,))
        if not exists:
            await interaction.response.send_message(f"⛔ La drogue **{nom}** n'existe pas.", ephemeral=True)
            return

        execute(
            """UPDATE drogues
               SET Groupe = COALESCE(%s, Groupe),
                   Propre = COALESCE(%s, Propre),
                   Sale   = COALESCE(%s, Sale)
             WHERE Nom=%s""",
            (groupe, propre, sale, nom),
        )

        channel_id, _ = get_channel_and_message_id("Drogues")
        if channel_id:
            chan = self.bot.get_channel(channel_id)
            if isinstance(chan, discord.TextChannel):
                await display_drogues_table(chan)

        await interaction.response.send_message(f"✅ La drogue **{nom}** a été mise à jour.", ephemeral=True)

    @drogues.autocomplete("nom")
    async def ac_drogues(self, interaction: discord.Interaction, current: str):
        return await _build_autocomplete(_drogues)(interaction, current)

    # =========================
    # /outils
    # =========================
    @app_commands.command(name="outils", description="Met à jour le tableau des outils")
    @app_commands.describe(
        nom="Nom (doit exister)",
        groupe="Groupe (optionnel)",
        propre="Prix argent propre (optionnel)",
        sale="Prix argent sale (optionnel)",
    )
    async def outils(
        self,
        interaction: discord.Interaction,
        nom: str,
        groupe: Optional[str] = None,
        propre: Optional[str] = None,
        sale: Optional[str] = None,
    ):
        exists = fetchone("SELECT 1 FROM outils WHERE Nom=%s", (nom,))
        if not exists:
            await interaction.response.send_message(f"⛔ L'outil **{nom}** n'existe pas.", ephemeral=True)
            return

        execute(
            """UPDATE outils
               SET Groupe = COALESCE(%s, Groupe),
                   Propre = COALESCE(%s, Propre),
                   Sale   = COALESCE(%s, Sale)
             WHERE Nom=%s""",
            (groupe, propre, sale, nom),
        )

        channel_id, _ = get_channel_and_message_id("Outils")
        if channel_id:
            chan = self.bot.get_channel(channel_id)
            if isinstance(chan, discord.TextChannel):
                await display_outils_table(chan)

        await interaction.response.send_message(f"✅ L'outil **{nom}** a été mis à jour.", ephemeral=True)

    @outils.autocomplete("nom")
    async def ac_outils(self, interaction: discord.Interaction, current: str):
        return await _build_autocomplete(_outils)(interaction, current)


async def setup(bot: commands.Bot):
    await bot.add_cog(Crud(bot))
