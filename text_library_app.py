"""
File: text_library.py
Description: A breakdown of Kanye West's biggest hits

Authors: Vichu Selvaraju & Jon Wong
"""

from text_library import TextLibrary
import pandas as pd


lyric_urls = {
    "All Falls Down": "https://genius.com/Kanye-west-all-falls-down-lyrics",
    "Gold Digger": "https://genius.com/Kanye-west-gold-digger-lyrics",
    "Can't Tell Me Nothing": "https://genius.com/Kanye-west-cant-tell-me-nothing-lyrics",
    "Heartless": "https://genius.com/Kanye-west-heartless-lyrics",
    "Father Strech My Hands Pt 1": "https://genius.com/Kanye-west-father-stretch-my-hands-pt-1-lyrics",
    "Bound 2": "https://genius.com/Kanye-west-bound-2-lyrics",
    "Ghost Town": "https://genius.com/Kanye-west-ghost-town-lyrics",
    "Off the Grid": "https://genius.com/Kanye-west-off-the-grid-lyrics",
}


def main():
    # Initlize object
    tl = TextLibrary()

    # Set stop words
    tl.load_stop_words(stopwords_file="stop_words.txt")

    for label, url in lyric_urls.items():
        tl.load_text(
            url=url,
            div_class="Lyrics__Container-sc-1ynbvzw-1 kUgSbL",
            parser=tl.website_parser,
            label=label,
        )

    tl.sankey(5)


if __name__ == "__main__":
    main()
