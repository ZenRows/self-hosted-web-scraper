import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

TARGETS = [
    "https://dexscreener.com/solana",
    "https://www.sofascore.com/football",
    "https://www.g2.com/categories/crm",
]


def fetch_zenrows(url: str) -> str | None:
    response = requests.get(
        "https://api.zenrows.com/v1/",
        params={
            "apikey": os.getenv("ZENROWS_API_KEY"),
            "url": url,
            "mode": "auto",
        },
        timeout=180,
    )

    if response.status_code == 200:
        return response.text

    print(f"{url} returned {response.status_code}: {response.text[:200]}")
    return None


for url in TARGETS:
    html = fetch_zenrows(url)

    if html:
        soup = BeautifulSoup(html, "lxml")
        print(f"\n{url}")
        print("bytes:", len(html))
        print("title:", soup.title)

