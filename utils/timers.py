# utils/timers.py
import asyncio
import discord
from datetime import datetime, timedelta
from typing import Optional

# ============================================================
# Embeds jolis pour minuteurs
# ============================================================
def _create_timer_embed(activity_name: str, end_time: datetime, remaining_min: int, author_name: str, color: discord.Color):
    """
    Construit un embed pour afficher l'état du minuteur.
    """
    remaining_txt = f"{remaining_min} minute(s)" if remaining_min >= 1 else "moins d’1 minute"

    embed = discord.Embed(
        title=f"⏳ Minuteur : {activity_name}",
        description=f"**Lancé par {author_name}**",
        color=color
    )
    embed.add_field(name="📅 Fin estimée", value=end_time.strftime("%d/%m/%Y à %H:%M"), inline=False)
    embed.add_field(name="⏳ Temps restant", value=remaining_txt, inline=False)
    embed.set_footer(text="Niwa Bot • Minuteries")
    return embed


async def _run_timer_message(ctx, activity_name: str, duration_min: int, author_name: str) -> None:
    """
    Affiche un embed de minuteur, le met à jour chaque minute,
    puis SUPPRIME le message à la fin (aucune notification).
    """
    total_minutes = max(1, int(round(duration_min)))
    end_time = datetime.now() + timedelta(minutes=total_minutes)

    # Envoi du message initial
    embed = _create_timer_embed(activity_name, end_time, total_minutes, author_name, discord.Color.green())
    message = await ctx.send(embed=embed)

    try:
        # Mise à jour chaque minute
        for remaining in range(total_minutes, 0, -1):
            await asyncio.sleep(60)
            new_embed = _create_timer_embed(activity_name, end_time, remaining - 1, author_name, discord.Color.orange())
            try:
                await message.edit(embed=new_embed)
            except discord.NotFound:
                # Le message a été supprimé manuellement
                return
    finally:
        # À la fin du minuteur → on supprime le message (aucun embed final)
        try:
            await message.delete()
        except discord.NotFound:
            pass


async def _run_police_timer(ctx, police_wait_min: int, author: discord.abc.User) -> None:
    """
    Démarre un minuteur 'Attente Police' (10 min typiquement).
    - Affiche un embed 10 min (sans message d'annonce).
    - À la fin, supprime l'embed.
    - Poste ensuite un message qui tag l'auteur pour dire qu'on peut partir si aucune police.
      -> Ajoute la réaction ✅
      -> Si l'AUTEUR ajoute ✅ sur ce message, on le supprime.
    """
    activity_name = "Attente Police (10 min)"
    total_minutes = max(1, int(round(police_wait_min)))
    end_time = datetime.now() + timedelta(minutes=total_minutes)

    # Embed minuteur Police
    embed = _create_timer_embed(activity_name, end_time, total_minutes, author.display_name, discord.Color.blurple())
    police_msg = await ctx.send(embed=embed)

    try:
        for remaining in range(total_minutes, 0, -1):
            await asyncio.sleep(60)
            new_embed = _create_timer_embed(activity_name, end_time, remaining - 1, author.display_name, discord.Color.blurple())
            try:
                await police_msg.edit(embed=new_embed)
            except discord.NotFound:
                return
    finally:
        # Supprime le minuteur police à la fin…
        try:
            await police_msg.delete()
        except discord.NotFound:
            pass

    # …puis avertit qu’on peut partir (tag l’auteur)
    notify = await ctx.send(
        f"🚔 **10 minutes écoulées** — si **aucune unité de police** n’est présente, "
        f"vous pouvez **partir**. {author.mention}"
    )
    try:
        await notify.add_reaction("✅")
    except discord.HTTPException:
        pass  # au cas où l'ajout de réaction échoue

    # Attendre la réaction ✅ de l'AUTEUR puis supprimer ce message
    def _check(reaction: discord.Reaction, user: discord.abc.User) -> bool:
        return (
            reaction.message.id == notify.id
            and str(reaction.emoji) == "✅"
            and user.id == author.id
        )

    try:
        # Timeout généreux (2h) au cas où le joueur réagit plus tard
        await ctx.bot.wait_for("reaction_add", timeout=2 * 60 * 60, check=_check)
        try:
            await notify.delete()
        except discord.NotFound:
            pass
    except asyncio.TimeoutError:
        # On laisse le message si l'auteur n'a pas réagi
        pass


# ============================================================
# API publique : start_timer
# ============================================================
async def start_timer(
    ctx,
    activity_name: str,
    duration_min: int,
    police_wait_min: int = 0,
    item_name: Optional[str] = None
):
    """
    Lance un minuteur principal + un minuteur Police (optionnel).
    - Minuteur principal : embed mis à jour → supprimé à la fin (silencieux).
    - Minuteur Police (si police_wait_min > 0) : embed 10 min → supprimé,
      puis message qui tag l'auteur + réaction ✅ ; si l'auteur réagit, message supprimé.

    NOTE: La gestion de stock (item_name) n'est volontairement pas incluse ici pour garder utils/timers.py générique.
          Si tu veux décrémenter un stock, fais-le AVANT d’appeler start_timer dans tes cogs.
    """
    author = ctx.author
    tasks = [ _run_timer_message(ctx, activity_name, duration_min, author.display_name) ]

    if police_wait_min and police_wait_min > 0:
        tasks.append(_run_police_timer(ctx, police_wait_min, author))

    await asyncio.gather(*tasks)
