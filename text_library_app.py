"""
File: text_library.py
Description: A breakdown of Kanye West's biggest hits

Authors: Vichu Selvaraju & Jon Wong
"""

from text_library import TextLibrary

lyric_urls = {
    "All Falls Down (2004)": "https://genius.com/Kanye-west-all-falls-down-lyrics",
    "Gold Digger (2005)": "https://genius.com/Kanye-west-gold-digger-lyrics",
    "Can't Tell Me Nothing (2007)": "https://genius.com/Kanye-west-cant-tell-me-nothing-lyrics",
    "Heartless (2008)": "https://genius.com/Kanye-west-heartless-lyrics",
    "Runaway (2010)": "https://genius.com/Kanye-west-runaway-lyrics",
    "Bound 2 (2013)": "https://genius.com/Kanye-west-bound-2-lyrics",
    "Saint Pablo (2016)": "https://genius.com/Kanye-west-saint-pablo-lyrics",
    "Ghost Town (2018)": "https://genius.com/Kanye-west-ghost-town-lyrics",
    "Off the Grid (2021)": "https://genius.com/Kanye-west-off-the-grid-lyrics",
    "Pure Souls (2021)": "https://genius.com/Kanye-west-pure-souls-lyrics"
}


def main():
    # Initlize object
    tl = TextLibrary()

    # Set stop words
    tl.load_stop_words(stopwords_file="stop_words.txt")

    # Load in data
    for label, url in lyric_urls.items():
        tl.load_text(
            url=url,
            div_class="Lyrics__Container-sc-1ynbvzw-1 kUgSbL",
            parser=tl.website_parser,
            label=label,
        )

    # Sankey diagram
    tl.sankey(5)

    tl.sentiment_graph()

    tl.lyrics_analysis_graph()

if __name__ == "__main__":
    main()
