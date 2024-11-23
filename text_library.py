"""

file: text_library.py

Description: A reusable library for text analysis and comparison
In theory, the framework should support any collection of texts
of interest (though this might require the implementation of some
custom parsers.)

Possible sources for your mini-project

- gutenburg texts
- political speech
- tweet compilations
- corporate filings
- philosophy treatises
- letters, journals, diaries
- blogs
- news articles


The core data structure:

Input: "A" --> raw text,  "B" --> another text

Extract wordcounts:
        "A" --> wordcounts_A,   "B" --> wordcounts_B, ......

What get stored:

        "wordcounts"  --->   {"A" --> wordcounts_A,
                              "B" --> wordcounts_B, etc.}

        e.g., dict[wordcounts][A] --> wordcounts_A

"""

from collections import defaultdict, Counter
import random as rnd
from preprocessor import load_website
from preprocessor import clean_text
from preprocessor import extract_unique_words
from preprocessor import compute_word_count
from preprocessor import compute_sentiment
from preprocessor import compute_readability

# import matplotlib.pyplot as plt
# import textstat
# from textblob import TextBlob
# import re
# import requests
# from bs4 import BeautifulSoup


class TextLibrary:

    def __init__(self):
        """Constructor

        datakey --> (filelabel --> datavalue)
        """
        self.data = defaultdict(dict)
        self.stop_words = set()

    def default_parser(self, filename):
        """Parse a standard text file and produce
        extract data results in the form of a dictionary."""

        results = {
            "wordcount": Counter("To be or not to be".split(" ")),
            "numwords": rnd.randrange(10, 50),
        }

        return results

    def website_parser(self, url, div_class):
        """Gets information on text from a website

        Args:
            url (string): Website url
            div_class (string): Div class to find specific text

        Returns:
            dictionary: dictionary with text information
        """
        results = {}

        # Load the text from a website
        text = load_website(url, div_class)

        # Clean the text
        text = clean_text(text, self.stop_words)

        # Get word counts
        word_counts = compute_word_count(text)
        results["wordcount"] = word_counts

        # Get unique words
        unique_words = extract_unique_words(text)
        results["unique words"] = unique_words

        # Get sentiment
        sentiment = compute_sentiment(text)
        results.update(sentiment)

        # Get readability
        readability = compute_readability(text)
        results.update(readability)

        return results

    def load_stop_words(self, stopwords_file):
        pass

    def load_text(self, filename, label=None, parser=None):
        """Register a document with the framework.
        Extract and store data to be used later by
        the visualizations"""
        if parser is None:
            results = self.default_parser(filename)
        else:
            results = parser(filename)

        if label is None:
            label = filename

        for k, v in results.items():
            self.data[k][label] = v
