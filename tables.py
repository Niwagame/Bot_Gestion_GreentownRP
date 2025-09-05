# tables.py
from datetime import datetime
from typing import Optional, Sequence, Tuple, Callable, List, Any

import discord
from db import fetchone, fetchall, execute

# ============================================================
# Palette par tableau (couleurs ANSI)
# ============================================================
PALETTES = {
    "Armes":     {"frame": "31;1", "header": "91", "row_a": "37", "row_b": "90", "emoji": "🔫"},
    "Munitions": {"frame": "33;1", "header": "93", "row_a": "37", "row_b": "90", "emoji": "💥"},
    "Drogues":   {"frame": "32;1", "header": "92", "row_a": "37", "row_b": "90", "emoji": "🌿"},
    "Outils":    {"frame": "36;1", "header": "96", "row_a": "37", "row_b": "90", "emoji": "🧰"},
    "Visa":      {"frame": "34;1", "header": "94", "row_a": "37", "row_b": "90", "emoji": "🛂"},
}
RESET = "\033[0m"

# Pour éviter les retours à la ligne sur Discord (desktop & mobile)
GLOBAL_MAX_LINE = 86  # ~86-90 garde bien la mise en page sur mobile sombre

# ============================================================
# Helpers ANSI + format
# ============================================================
def _color(txt: str, code: str) -> str:
    return f"\033[{code}m{txt}{RESET}"

def _clean_cell(x: Any) -> str:
    s = "-" if x is None or x == "" else str(x)
    # empêche les retours à la ligne dans une cellule
    return " ".join(s.replace("\t", " ").split())

def _ellipsis(s: str, w: int) -> str:
    if w <= 1:
        return s[:w]
    return (s if len(s) <= w else (s[: max(0, w - 1)] + "…"))

def _pad_l(s: str, w: int) -> str:
    return s + " " * max(0, w - len(s))

def _pad_r(s: str, w: int) -> str:
    return " " * max(0, w - len(s)) + s

def _pad_c(s: str, w: int) -> str:
    if w <= len(s):
        return s
    total = w - len(s)
    left = total // 2
    right = total - left
    return (" " * left) + s + (" " * right)

def _calc_widths(
    headers: Sequence[str],
    rows: List[List[Any]],
    minw: List[int],
    maxw: List[int],
) -> List[int]:
    cols = len(headers)
    widths = [max(minw[i], len(headers[i])) for i in range(cols)]
    for r in rows:
        for i in range(cols):
            cell = _clean_cell(r[i]) if i < len(r) else ""
            widths[i] = max(widths[i], len(cell), minw[i])
    # borne supérieure par colonne
    widths = [min(widths[i], maxw[i]) for i in range(cols)]
    # borne globale: si la ligne dépasse, on réduit les colonnes les plus “flex”
    def line_len(ws: List[int]) -> int:
        # "│ " + " │ ".join(cols) + " │" ; séparateurs = 3*(n-1), bords = 4
        return 4 + sum(ws) + 3 * (cols - 1)

    if line_len(widths) > GLOBAL_MAX_LINE:
        # on réduit en priorité les colonnes texte (0,1, etc.), jamais sous minw
        order = list(range(cols))  # simple: de gauche à droite
        while line_len(widths) > GLOBAL_MAX_LINE:
            changed = False
            for i in order:
                if widths[i] > minw[i]:
                    widths[i] -= 1
                    changed = True
                    if line_len(widths) <= GLOBAL_MAX_LINE:
                        break
            if not changed:
                break
    return widths

def _border(widths: List[int], frame_code: str, left: str, mid: str, right: str) -> str:
    parts = [left]
    for idx, w in enumerate(widths):
        parts.append("─" * (w + 2))
        parts.append(mid if idx < len(widths) - 1 else right)
    return _color("".join(parts), frame_code)

def _render_row(
    cells: List[str], widths: List[int], ink: str, aligns: List[str]
) -> str:
    out = []
    for i, w in enumerate(widths):
        val = cells[i] if i < len(cells) else ""
        # tronque au besoin
        val = _ellipsis(_clean_cell(val), w)
        a = aligns[i]
        if a == "r":
            pad = _pad_r(val, w)
        elif a == "c":
            pad = _pad_c(val, w)
        else:
            pad = _pad_l(val, w)
        out.append(pad)
    return _color("│ " + " │ ".join(out) + " │", ink)

def _build_table(
    title: str,
    headers: Sequence[str],
    rows: List[List[Any]],
    palette: dict,
    aligns_header: List[str],
    aligns_row: List[str],
    minw: List[int],
    maxw: List[int],
    row_color_func: Optional[Callable[[List[Any], int], str]] = None,
    footer: Optional[str] = None,
) -> str:
    widths = _calc_widths(headers, rows, minw, maxw)
    top = _border(widths, palette["frame"], "╭", "┬", "╮")
    mid = _border(widths, palette["frame"], "├", "┼", "┤")
    bot = _border(widths, palette["frame"], "╰", "┴", "╯")

    out = []
    out.append("```ansi")
    out.append(_color(title, palette["frame"]))
    out.append(top)
    out.append(_render_row(list(headers), widths, palette["header"], aligns_header))
    out.append(mid)

    if rows:
        for i, r in enumerate(rows):
            ink = row_color_func(r, i) if row_color_func else (palette["row_a"] if i % 2 == 0 else palette["row_b"])
            cells = [ _clean_cell(r[k]) if k < len(r) else "" for k in range(len(widths)) ]
            out.append(_render_row(cells, widths, ink, aligns_row))
    else:
        out.append(_render_row(["Aucune donnée"] + [""]*(len(widths)-1), widths, "90", aligns_row))

    out.append(bot)
    if footer:
        out.append(_color(footer, "90"))
    out.append("```")
    return "\n".join(out)

# ============================================================
# Utilitaires Message/Salon
# ============================================================
def get_channel_and_message_id(item_type: str) -> Tuple[Optional[int], Optional[int]]:
    row = fetchone("SELECT ID_Salon, ID_Message FROM message WHERE Nom = %s", (item_type,))
    if not row:
        return (None, None)
    return (row.get("ID_Salon"), row.get("ID_Message"))

def update_message_id(item_type: str, new_message_id: int) -> None:
    execute("UPDATE message SET ID_Message = %s WHERE Nom = %s", (new_message_id, item_type))

async def delete_existing_messages(channel: discord.TextChannel, item_type: str) -> None:
    channel_id, message_id = get_channel_and_message_id(item_type)
    if channel_id and message_id and channel.id == channel_id:
        try:
            msg = await channel.fetch_message(message_id)
            await msg.delete()
        except discord.NotFound:
            pass

# ============================================================
# Rendu générique
# ============================================================
async def send_table_for_item_type(
    channel: discord.TextChannel,
    item_type: str,
    sql: str,
    headers: Sequence[str],
    row_mapper: Callable[[dict], List[Any]],
    aligns_header: List[str],
    aligns_row: List[str],
    minw: List[int],
    maxw: List[int],
    row_color_func: Optional[Callable[[List[Any], int], str]] = None,
    order_note: Optional[str] = None,
) -> None:
    rows_db = fetchall(sql)
    rows = [row_mapper(r) for r in rows_db]

    palette = PALETTES.get(item_type, {"frame": "35;1", "header": "96", "row_a": "37", "row_b": "90", "emoji": "📋"})
    date_now = datetime.now().strftime("%d/%m/%Y %H:%M")
    title = f"{palette['emoji']}  {item_type.upper()}  •  Mise à jour : {date_now}"
    if order_note:
        title += f"  •  {order_note}"

    # supprimer ancien
    ch_id, old_id = get_channel_and_message_id(item_type)
    if old_id and ch_id == channel.id:
        try:
            old = await channel.fetch_message(old_id)
            await old.delete()
        except discord.NotFound:
            pass

    content = _build_table(
        title, list(headers), rows, palette,
        aligns_header, aligns_row,
        minw, maxw, row_color_func=row_color_func,
    )
    msg = await channel.send(content)
    update_message_id(item_type, msg.id)

# ============================================================
# Tables spécifiques
#  - En-têtes centrés
#  - Noms/groupe à gauche
#  - Prix à droite
#  - Min/Max par colonne pour forcer l’adaptation (et couper proprement)
# ============================================================
async def display_armes_table(channel: discord.TextChannel):
    await send_table_for_item_type(
        channel,
        "Armes",
        "SELECT Nom, Groupe, Propre, Sale FROM armes ORDER BY ID",
        headers=["Nom", "Groupe", "Propre", "Sale"],
        row_mapper=lambda a: [a["Nom"], a.get("Groupe"), a.get("Propre"), a.get("Sale")],
        aligns_header=["c","c","c","c"],
        aligns_row   =["l","l","r","r"],
        minw=[10, 8, 4, 4],
        maxw=[24, 14, 10, 10],
    )

async def display_munitions_table(channel: discord.TextChannel):
    await send_table_for_item_type(
        channel,
        "Munitions",
        "SELECT Nom, Groupe, Propre, Sale FROM munitions ORDER BY Nom",
        headers=["Nom", "Groupe", "Propre", "Sale"],
        row_mapper=lambda m: [m["Nom"], m.get("Groupe"), m.get("Propre"), m.get("Sale")],
        aligns_header=["c","c","c","c"],
        aligns_row   =["l","l","r","r"],
        minw=[10, 6, 4, 4],
        maxw=[22, 12, 10, 10],
    )

async def display_drogues_table(channel: discord.TextChannel):
    await send_table_for_item_type(
        channel,
        "Drogues",
        "SELECT Nom, Groupe, Propre, Sale FROM drogues ORDER BY Nom",
        headers=["Nom", "Groupe", "Propre", "Sale"],
        row_mapper=lambda d: [d["Nom"], d.get("Groupe"), d.get("Propre"), d.get("Sale")],
        aligns_header=["c","c","c","c"],
        aligns_row   =["l","l","r","r"],
        minw=[10, 6, 4, 4],
        maxw=[20, 14, 10, 10],
    )

async def display_outils_table(channel: discord.TextChannel):
    await send_table_for_item_type(
        channel,
        "Outils",
        "SELECT Nom, Groupe, Propre, Sale FROM outils ORDER BY Nom",
        headers=["Nom", "Groupe", "Propre", "Sale"],
        row_mapper=lambda o: [o["Nom"], o.get("Groupe"), o.get("Propre"), o.get("Sale")],
        aligns_header=["c","c","c","c"],
        aligns_row   =["l","l","r","r"],
        minw=[12, 6, 4, 4],
        maxw=[22, 14, 10, 10],
    )

# ============================================================
# VISA — pagination avec couleurs + coupe propre
# ============================================================
def _visa_rows() -> List[List[Any]]:
    rows_db = fetchall(
        "SELECT Nom, Prenom, DateValidite, Valide, DelivrePar, Type FROM visas ORDER BY DateValidite DESC, Nom, Prenom"
    )
    now = datetime.now()
    out: List[List[Any]] = []
    for r in rows_db:
        is_valid = (r.get("Valide") == 1) and (r.get("DateValidite") and r["DateValidite"] >= now)
        out.append([
            r["Nom"],
            r["Prenom"],
            r["DateValidite"].strftime("%Y-%m-%d %H:%M") if r.get("DateValidite") else "-",
            "✅" if is_valid else "❌",
            r.get("DelivrePar") or "-",
            r.get("Type") or "-",
        ])
    return out

def _visa_row_color(row: List[Any], idx: int) -> str:
    return "92" if (len(row) >= 4 and row[3] == "✅") else "91"

def build_visa_pages(per_page: int = 15) -> List[str]:
    headers = ["Nom", "Prénom", "Date de validité", "Valide ?", "Délivré par", "Type"]
    palette = PALETTES["Visa"]
    emoji = palette["emoji"]
    date_now = datetime.now().strftime("%d/%m/%Y %H:%M")

    rows = _visa_rows()
    if not rows:
        return []

    pages: List[str] = []
    total = len(rows)
    if per_page <= 0:
        per_page = total

    aligns_header = ["c","c","c","c","c","c"]
    aligns_row    = ["l","l","c","c","l","l"]
    minw = [10, 10, 16, 7, 12, 8]
    maxw = [18, 16, 18, 7, 18, 12]

    for i in range(0, total, per_page):
        chunk = rows[i:i+per_page]
        page_index = (i // per_page) + 1
        page_count = (total + per_page - 1) // per_page
        title = f"{emoji}  VISA  •  Mise à jour : {date_now}"
        footer = f"Page {page_index}/{page_count}  •  Total: {total}"

        content = _build_table(
            title, headers, chunk, palette,
            aligns_header, aligns_row, minw, maxw,
            row_color_func=_visa_row_color, footer=footer
        )
        pages.append(content)

    return pages
