"""
File: text_library.py
Description: A breakdown of Kanye West's biggest hits
Authors: Vichu Selvaraju & Jon Wong
"""

import requests
from bs4 import BeautifulSoup

lyric_links = [
    "https://genius.com/Kanye-west-all-falls-down-lyrics",
    "https://genius.com/Kanye-west-gold-digger-lyrics",
    "https://genius.com/Kanye-west-cant-tell-me-nothing-lyrics",
    "https://genius.com/Kanye-west-heartless-lyrics",
    "https://genius.com/Kanye-west-father-stretch-my-hands-pt-1-lyrics",
    "https://genius.com/Kanye-west-bound-2-lyrics",
    "https://genius.com/Kanye-west-ghost-town-lyrics",
    "https://genius.com/Kanye-west-off-the-grid-lyrics",
]


def main():
    response = requests.get(lyric_links[1])
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        lyrics_divs = soup.find_all(
            "div", class_="Lyrics__Container-sc-1ynbvzw-1 kUgSbL"
        )
        lyrics = "\n".join(div.get_text(separator="\n").strip() for div in lyrics_divs)
    print(lyrics)


if __name__ == "__main__":
    main()
