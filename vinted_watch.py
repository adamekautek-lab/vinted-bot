"""
Watcher ofert Vinted -> powiadomienia na Telegramie.
Odpalany cyklicznie przez GitHub Actions (.github/workflows/vinted-watch.yml).
"""

import asyncio
import json
import os
import time
from pathlib import Path

import requests
from vinted import VintedClient

# --- KONFIGURACJA ---------------------------------------------------------
# Wklej tu linki wyszukiwania skopiowane z paska adresu na vinted.pl.
# Wejdz na vinted.pl, ustaw filtry (marka, rozmiar, cena, stan) tak jak
# normalnie szukajac, skopiuj caly link. Mozesz dodac ich dowolnie wiele.
SEARCH_URLS = [
    "https://www.vinted.pl/catalog?brand_ids[]=219304&brand_ids[]=1908821&brand_ids[]=7026375&brand_ids[]=7026376&brand_ids[]=7489663&page=1&time=1788461886&order=newest_first",
]

ITEMS_PER_SEARCH = 20  # ile najnowszych ofert sprawdzac przy kazdym uruchomieniu
# ---------------------------------------------------------------------------

SEEN_FILE = Path("data/seen_items.json")
MAX_SEEN_STORED = 3000

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def load_seen() -> set:
    if SEEN_FILE.exists():
        return set(json.loads(SEEN_FILE.read_text()))
    return set()


def save_seen(seen: set) -> None:
    SEEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    SEEN_FILE.write_text(json.dumps(list(seen)[-MAX_SEEN_STORED:]))


def escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def format_message(item) -> str:
    lines = [f"\U0001F195 <b>{escape_html(item.title)}</b>"]
    extra = " \u00b7 ".join(x for x in [item.brand_title, item.size_title] if x)
    if extra:
        lines.append(f"\U0001F3F7\uFE0F {escape_html(extra)}")
    lines.append(f"\U0001F4B6 {item.price:.2f} {item.currency}")
    lines.append(f"\U0001F517 {item.url}")
    return "\n".join(lines)


def send_telegram(text: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    resp = requests.post(
        url,
        data={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"},
        timeout=15,
    )
    resp.raise_for_status()


async def check_all_searches(client: VintedClient, seen: set, new_seen: set, first_run: bool) -> int:
    sent = 0
    for search_url in SEARCH_URLS:
        try:
            items = await client.search_items(
                search_url, per_page=ITEMS_PER_SEARCH, order="newest_first"
            )
        except Exception as exc:
            print(f"[BLAD] {search_url[:70]}: {exc}")
            continue

        for item in items:
            item_id = str(item.id)
            if item_id in seen or item_id in new_seen:
                continue
            new_seen.add(item_id)
            if first_run:
                continue
            send_telegram(format_message(item))
            sent += 1
            time.sleep(1)
    return sent


async def main() -> None:
    seen = load_seen()
    first_run = len(seen) == 0
    new_seen = set(seen)

    async with VintedClient() as client:
        sent = await check_all_searches(client, seen, new_seen, first_run)

    save_seen(new_seen)
    print(f"OK - wyslano {sent} powiadomien. Pierwsze uruchomienie: {first_run}")


if __name__ == "__main__":
    asyncio.run(main())
