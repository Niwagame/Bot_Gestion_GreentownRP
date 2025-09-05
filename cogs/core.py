# cogs/core.py
import discord
from discord.ext import commands

from tables import (
    display_armes_table,
    display_munitions_table,
    display_drogues_table,
    display_outils_table,
    get_channel_and_message_id,
)


class Core(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} est connecté à Discord!")

        try:
            synced = await self.bot.tree.sync()
            print(f"Commandes Slash synchronisées : {len(synced)}")
        except Exception as e:
            print(f"Erreur de synchronisation des commandes Slash : {e}")

        # Rafraîchir les tableaux dynamiques au démarrage (hors Visa)
        for item_type in ["Armes", "Munitions", "Drogues", "Outils"]:
            channel_id, _ = get_channel_and_message_id(item_type)
            if not channel_id:
                continue

            channel = self.bot.get_channel(channel_id)
            if not isinstance(channel, discord.TextChannel):
                continue

            try:
                if item_type == "Armes":
                    await display_armes_table(channel)
                elif item_type == "Munitions":
                    await display_munitions_table(channel)
                elif item_type == "Drogues":
                    await display_drogues_table(channel)
                elif item_type == "Outils":
                    await display_outils_table(channel)
            except Exception as e:
                print(f"⚠️ Erreur lors de l'affichage du tableau {item_type} : {e}")

        # Rafraîchir le tableau VISA au démarrage via le cog Visas
        try:
            visas_cog = self.bot.get_cog("Visas")
            if visas_cog and hasattr(visas_cog, "_refresh_visa_table_in_configured_channel"):
                await visas_cog._refresh_visa_table_in_configured_channel()
            else:
                print("ℹ️ Cog 'Visas' introuvable ou méthode de refresh indisponible.")
        except Exception as e:
            print(f"⚠️ Erreur lors de l'affichage du tableau Visa : {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Core(bot))
