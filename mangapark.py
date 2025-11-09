
import requests, re, sys
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        self.BASE_URL = "https://mangapark.io"
        self.HEADERS = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:144.0) Gecko/20100101 Firefox/144.0",
            "Referer": self.BASE_URL,
            "Cookie": "nsfw=2;"
        }

    def get_latest_manga(self):
        return self.get_result(latest=True)

    def search_manga(self, manga):
        return self.get_result(search=True, manga=manga)

    def get_result(self, latest=None, search=None, manga=None):
        r = "/latest/manga" if latest else f"/search?word={manga}" if search else None
        pb = "3" if latest else "5" if search else None
        url = f"{self.BASE_URL}{r}"
        res = requests.get(url, headers=self.HEADERS)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        result = []
        for item in soup.select(f"div.flex.border-b.border-b-base-200.pb-{pb}"):
            title_tag = item.select_one("h3 a")
            chapter_tag = item.select_one("div.flex.flex-nowrap.justify-between a")
            img_tag = item.select_one("img")

            if not title_tag:
                continue

            img_url = None
            if img_tag:
                img_url = img_tag.get("src") or img_tag.get("data-src")
                if img_url and img_url.startswith("/"):
                    img_url = self.BASE_URL + img_url

            match = re.search(r"/title/(\d+)-", title_tag["href"])
            manga_id = match.group(1) if match else None

            manga_data = {
                "title": title_tag.text.strip(),
                "url": self.BASE_URL + title_tag["href"],
                "chapter_url": self.BASE_URL + chapter_tag["href"] if chapter_tag else None,
                "latest_chapter": chapter_tag.text.strip() if chapter_tag else None,
                "cover": img_url if img_url else "https://placehold.co/200x300?text=Loading...",
                "id": manga_id
            }
            result.append(manga_data)
        return result

def save_to_csv(result, latest=None, search=None):
    df = pd.DataFrame(result)
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"{'scraped_manga' if latest else 'searched_manga' if search else ''}-{current_date}.csv"
    print(f"saving {filename}")
    df.to_csv(f"{filename}")
    print("done")

if __name__ == "__main__":
    scraper = Scraper()
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} [ latest | search "manga_name" ]')
        sys.exit(1)

    if sys.argv[1] == "latest":
        save_to_csv(scraper.get_latest_manga(), latest=True)
    elif sys.argv[1] == "search" and len(sys.argv) > 2:
        manga_name = sys.argv[2]
        save_to_csv(scraper.search_manga(manga_name), search=True)
    else:
        print("Invalid arguments")