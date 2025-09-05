# cogs/visas.py
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

import discord
from discord import app_commands
from discord.ext import commands

from db import fetchall, fetchone, execute
from tables import (
    get_channel_and_message_id,
    update_message_id,
    build_visa_pages,  # fabrique les pages ANSI du tableau Visa
)

VALID_TYPES = ["travaille", "vacances","politique", "autre"]

ARROWS = {
    "first": "⏮️",
    "prev": "⬅️",
    "next": "➡️",
    "last": "⏭️",
}


def _parse_duration(d: str) -> timedelta:
    """
    Parse une durée compacte :
      - '1h' = 1 heure
      - '1d' = 1 jour
      - '1s' = 1 semaine
      - '1m' = 1 mois (~30 jours)
      - combinable: '1s3d12h'
    """
    d = (d or "").strip().lower()
    if not d:
        raise ValueError("Durée vide.")

    total = timedelta(0)
    num = ""
    i = 0
    while i < len(d):
        ch = d[i]
        if ch.isdigit():
            num += ch
            i += 1
            continue
        if not num:
            raise ValueError("Format durée invalide.")
        n = int(num)
        num = ""
        if ch == "h":
            total += timedelta(hours=n)
        elif ch == "d":
            total += timedelta(days=n)
        elif ch == "s":
            total += timedelta(days=7 * n)
        elif ch == "m":
            total += timedelta(days=30 * n)
        else:
            raise ValueError(f"Unité inconnue '{ch}' (utilise h,d,s,m).")
        i += 1

    if num:
        raise ValueError("Nombre sans unité à la fin (ajoute h/d/s/m).")

    if total.total_seconds() <= 0:
        raise ValueError("Durée doit être > 0.")
    return total


def _latest_visa_id(nom: str, prenom: str) -> Optional[int]:
    row = fetchone(
        """SELECT id FROM visas
           WHERE Nom=%s AND Prenom=%s
           ORDER BY DateValidite DESC
           LIMIT 1""",
        (nom, prenom),
    )
    return row["id"] if row else None


class Visas(commands.Cog):
    """Gestion des Visas (ajout / modification / suppression / recherche + pagination)."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # États de pagination en mémoire: message_id -> {"pages":[...], "page":0}
        self.paginators: Dict[int, Dict[str, Any]] = {}

    # -------------------------
    # Helpers d’affichage/pagination
    # -------------------------
    async def _refresh_visa_table_in_configured_channel(self) -> None:
        """Recrée le tableau Visa paginé dans le salon configuré via table Message."""
        chan_id, old_msg_id = get_channel_and_message_id("Visa")
        if not chan_id:
            return
        ch = self.bot.get_channel(chan_id)
        if not isinstance(ch, discord.TextChannel):
            return

        # Supprimer l'ancien message s'il existe
        if old_msg_id:
            try:
                old = await ch.fetch_message(old_msg_id)
                await old.delete()
            except discord.NotFound:
                pass

        # Construire les pages (texte ANSI)
        pages = build_visa_pages(per_page=15)
        if not pages:
            msg = await ch.send("Aucune donnée Visa.")
            update_message_id("Visa", msg.id)
            return

        # Envoyer la 1ère page
        msg = await ch.send(pages[0])
        update_message_id("Visa", msg.id)

        # Enregistrer l'état de pagination
        self.paginators[msg.id] = {"pages": pages, "page": 0}

        # Ajouter les réactions de navigation s'il y a plusieurs pages
        if len(pages) > 1:
            try:
                await msg.add_reaction(ARROWS["first"])
                await msg.add_reaction(ARROWS["prev"])
                await msg.add_reaction(ARROWS["next"])
                await msg.add_reaction(ARROWS["last"])
            except discord.HTTPException:
                pass

    async def _handle_pagination(self, reaction: discord.Reaction, user: discord.abc.User) -> None:
        """Gère les réactions de pagination sur le tableau Visa."""
        if user.bot:
            return
        msg = reaction.message
        state = self.paginators.get(msg.id)
        if not state:
            return

        emoji = str(reaction.emoji)
        pages: List[str] = state["pages"]
        cur = state["page"]
        last_idx = len(pages) - 1

        if emoji == ARROWS["first"]:
            new = 0
        elif emoji == ARROWS["prev"]:
            new = max(0, cur - 1)
        elif emoji == ARROWS["next"]:
            new = min(last_idx, cur + 1)
        elif emoji == ARROWS["last"]:
            new = last_idx
        else:
            return

        if new != cur:
            state["page"] = new
            try:
                await msg.edit(content=pages[new])
            except discord.NotFound:
                self.paginators.pop(msg.id, None)
                return

        try:
            await msg.remove_reaction(emoji, user)
        except discord.HTTPException:
            pass

    # -------------------------
    # Listeners (pagination)
    # -------------------------
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.abc.User):
        try:
            await self._handle_pagination(reaction, user)
        except Exception:
            pass

    # -------------------------
    # /visa_ajout
    # -------------------------
    @app_commands.command(name="visa_ajout", description="Ajoute ou met à jour un visa (durée ex: 12h, 3d, 1s, 1m).")
    @app_commands.describe(
        nom="Nom",
        prenom="Prénom",
        duree="Durée ex: 12h, 3d, 1s (semaine), 1m (mois). Combinable: ex 1s3d.",
        type="Type du visa (travaille, vacances,politique, autre)",
        valide="Visa valide ? (défaut: true)",
    )
    @app_commands.choices(
        type=[
            app_commands.Choice(name="travaille", value="travaille"),
            app_commands.Choice(name="vacances", value="vacances"),
            app_commands.Choice(name="politique", value="politique"),
            app_commands.Choice(name="autre", value="autre"),
        ]
    )
    async def visa_ajout(
        self,
        interaction: discord.Interaction,
        nom: str,
        prenom: str,
        duree: str,
        type: str,
        valide: Optional[bool] = True,
    ):
        try:
            delta = _parse_duration(duree)
        except ValueError as e:
            await interaction.response.send_message(f"⛔ Durée invalide : {e}", ephemeral=True)
            return

        date_validite = datetime.now() + delta
        delivre_par = interaction.user.display_name

        if type not in VALID_TYPES:
            await interaction.response.send_message("⛔ `type` doit être `travaille`, `vacances`, `politique` ou `autre`.", ephemeral=True)
            return

        existing_id = _latest_visa_id(nom, prenom)
        if existing_id:
            execute(
                """UPDATE visas
                   SET DateValidite=%s, Valide=%s, DelivrePar=%s, Type=%s
                 WHERE id=%s""",
                (date_validite, 1 if valide else 0, delivre_par, type, existing_id),
            )
            msg = f"✏️ Visa **mis à jour** pour **{prenom} {nom}** (jusqu'au {date_validite:%d/%m/%Y %H:%M})."
        else:
            execute(
                """INSERT INTO visas (Nom, Prenom, DateValidite, Valide, DelivrePar, Type)
                   VALUES (%s,%s,%s,%s,%s,%s)""",
                (nom, prenom, date_validite, 1 if valide else 0, delivre_par, type),
            )
            msg = f"✅ Visa **ajouté** pour **{prenom} {nom}** (jusqu'au {date_validite:%d/%m/%Y %H:%M})."

        await interaction.response.send_message(msg, ephemeral=True)
        await self._refresh_visa_table_in_configured_channel()

    # -------------------------
    # /visa_modifier
    # -------------------------
    @app_commands.command(name="visa_modifier", description="Modifie le visa le plus récent d'un utilisateur.")
    @app_commands.describe(
        nom="Nom",
        prenom="Prénom",
        valide="Mettre le visa en valide (true) ou invalide (false) (optionnel)",
        ajout_duree="Ajouter une nouvelle durée (ex: 12h, 3d, 1s, 1m). Repart de maintenant. (optionnel)",
        type="Changer le type (travaille, vacances,politique, autre) (optionnel)",
    )
    @app_commands.choices(
        type=[
            app_commands.Choice(name="travaille", value="travaille"),
            app_commands.Choice(name="vacances", value="vacances"),
            app_commands.Choice(name="politique", value="politique"),
            app_commands.Choice(name="autre", value="autre"),
        ]
    )
    async def visa_modifier(
        self,
        interaction: discord.Interaction,
        nom: str,
        prenom: str,
        valide: Optional[bool] = None,
        ajout_duree: Optional[str] = None,
        type: Optional[str] = None,
    ):
        vid = _latest_visa_id(nom, prenom)
        if not vid:
            await interaction.response.send_message("⛔ Aucun visa trouvé pour cette personne.", ephemeral=True)
            return

        sets = []
        args: List[Any] = []

        if ajout_duree:
            try:
                delta = _parse_duration(ajout_duree)
            except ValueError as e:
                await interaction.response.send_message(f"⛔ Durée invalide : {e}", ephemeral=True)
                return
            new_validite = datetime.now() + delta
            sets.append("DateValidite=%s")
            args.append(new_validite)

        if valide is not None:
            sets.append("Valide=%s")
            args.append(1 if valide else 0)

        if type is not None:
            if type not in VALID_TYPES:
                await interaction.response.send_message("⛔ `type` doit être `travaille`, `vacances`,`politique` ou `autre`.", ephemeral=True)
                return
            sets.append("Type=%s")
            args.append(type)

        # Toujours mettre à jour DelivrePar au modificateur
        sets.append("DelivrePar=%s")
        args.append(interaction.user.display_name)

        if not sets:
            await interaction.response.send_message("Aucun champ à modifier.", ephemeral=True)
            return

        args.append(vid)
        execute(f"UPDATE visas SET {', '.join(sets)} WHERE id=%s", tuple(args))
        await interaction.response.send_message("✅ Visa **modifié**.", ephemeral=True)
        await self._refresh_visa_table_in_configured_channel()

    # -------------------------
    # /visa_supprimer
    # -------------------------
    @app_commands.command(name="visa_supprimer", description="Supprime un visa (le plus récent) ou tous les visas d'une personne.")
    @app_commands.describe(
        nom="Nom",
        prenom="Prénom",
        tout="Si vrai, supprime TOUS les visas de cette personne (défaut: false).",
    )
    async def visa_supprimer(
        self,
        interaction: discord.Interaction,
        nom: str,
        prenom: str,
        tout: Optional[bool] = False,
    ):
        if tout:
            count = fetchone("SELECT COUNT(*) AS c FROM visas WHERE Nom=%s AND Prenom=%s", (nom, prenom))["c"]
            if count == 0:
                await interaction.response.send_message("Aucun visa à supprimer.", ephemeral=True)
                return
            execute("DELETE FROM visas WHERE Nom=%s AND Prenom=%s", (nom, prenom))
            await interaction.response.send_message(f"🗑️ **{count} visa(s)** supprimé(s) pour **{prenom} {nom}**.", ephemeral=True)
        else:
            vid = _latest_visa_id(nom, prenom)
            if not vid:
                await interaction.response.send_message("⛔ Aucun visa trouvé pour cette personne.", ephemeral=True)
                return
            execute("DELETE FROM visas WHERE id=%s", (vid,))
            await interaction.response.send_message(f"🗑️ Visa **le plus récent** supprimé pour **{prenom} {nom}**.", ephemeral=True)

        await self._refresh_visa_table_in_configured_channel()

    # -------------------------
    # /visa_recherche
    # -------------------------
    @app_commands.command(name="visa_recherche", description="Recherche des visas par nom/prénom (partiel accepté).")
    @app_commands.describe(
        nom="Nom (optionnel, partiel accepté)",
        prenom="Prénom (optionnel, partiel accepté)",
        seulement_valides="Ne montrer que les visas valides (défaut: false)",
        limite="Nombre max de résultats (défaut: 15, max 50)",
    )
    async def visa_recherche(
        self,
        interaction: discord.Interaction,
        nom: Optional[str] = None,
        prenom: Optional[str] = None,
        seulement_valides: Optional[bool] = False,  # <<< défaut à False
        limite: Optional[int] = 15,
    ):
        where = []
        args: List[Any] = []

        if nom:
            where.append("Nom LIKE %s")
            args.append(f"%{nom}%")
        if prenom:
            where.append("Prenom LIKE %s")
            args.append(f"%{prenom}%")

        if seulement_valides:
            where.append("(Valide=1 AND DateValidite >= NOW())")

        clause = " WHERE " + " AND ".join(where) if where else ""
        try:
            lim = max(1, min(int(limite or 15), 50))
        except Exception:
            lim = 15

        rows = fetchall(
            f"""SELECT Nom, Prenom, DateValidite, Valide, DelivrePar, Type
                FROM visas {clause}
                ORDER BY DateValidite DESC, Nom, Prenom
                LIMIT {lim}""",
            tuple(args),
        )

        if not rows:
            await interaction.response.send_message("Aucun résultat.", ephemeral=True)
            return

        now = datetime.now()
        lines: List[str] = []
        for r in rows:
            is_valid = (r["Valide"] == 1) and (r["DateValidite"] >= now)
            status = "✅" if is_valid else "❌"
            lines.append(
                f"- **{r['Prenom']} {r['Nom']}** — jusqu’au **{r['DateValidite']:%d/%m/%Y %H:%M}** • {status} • {r.get('Type') or '-'} • délivré par {r.get('DelivrePar') or '-'}"
            )

        await interaction.response.send_message("\n".join(lines[:lim]), ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Visas(bot))
