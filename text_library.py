"""
File: text_library.py
Description: A reusable library for text analysis and comparison
In theory, the framework should support any collection of texts
of interest (though this might require the implementation of some
custom parsers.)

Authors: Vichu Selvaraju & Jon Wong
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from preprocessor import load_text
from preprocessor import load_website
from preprocessor import clean_text
from preprocessor import extract_unique_words
from preprocessor import compute_word_count
from preprocessor import compute_sentiment
from preprocessor import compute_readability
import sankey as sk


class TextLibrary:

    def __init__(self):
        """Constructor

        datakey --> (filelabel --> datavalue)
        """
        self.data = defaultdict(dict)
        self.stop_words = set()

    def default_parser(self, filename):
        """Parse a standard text file and
        extract data results in the form of a dictionary.

        Args:
            filename (string): Name of the file

        Returns:
            dictionary: Text information
        """

        results = {}

        # Load the text
        text = load_text(filename)

        # Clean the text
        text = clean_text(text, self.stop_words)

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

    def website_parser(self, url, div_class):
        """Parse a website and extract data
        results in the form of a dictionary.

        Args:
            url (string): Website url
            div_class (string): Div class to find specific text

        Returns:
            dictionary: Text information
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
        """Load stop words from a file

        Args:
            stopwords_file (string): filename for stop words
        """
        with open(stopwords_file, "r") as file:
            content = file.read()
        self.stop_words = set(content.split())

    def load_text(
        self, filename=None, url=None, div_class=None, label=None, parser=None
    ):
        """Register a document with the framework.
        Extract and store data to be used later by
        the visualizations

        Args:
            filename (string, optional): Text file to regsiter. Defualts to None.
            url (string, optional): Website url with text to regsiter. Defaults to None.
            div_class (string, optinal): Div class of website to get text. Defaults to None.
            label (string, optional): Label for file. Defaults to None.
            parser (object, optional): Name of parser to use for file. Defaults to None.
        """
        if parser is None:
            results = self.default_parser(filename)
        else:
            results = parser(url, div_class)

        if label is None:
            label = filename

        for k, v in results.items():
            self.data[k][label] = v

    def sankey(self, k):
        """Sankey diagram connecting text to words

        Args:
            k (integer): Number of words to include
        """
        rows = [
            {"Label": label, "Word": word, "Count": count}
            for label, word_counts in self.data["wordcount"].items()
            for word, count in word_counts.most_common(k)
        ]

        df = pd.DataFrame(rows, columns=["Label", "Word", "Count"])
        sk.make_sankey(df, "Label", "Word", vals="Count")

    def sentiment_graph(self):
        """Graph comapring sentiment analysis"""
        # Data for plots
        songs = list(self.data["polarity"].keys())
        polarity_scores = list(self.data["polarity"].values())
        subjectivity_scores = list(self.data["subjectivity"].values())
        x_axis = np.arange(0, len(songs) * 2, 2)

        # Plots
        plt.bar(x_axis - 0.3, polarity_scores, 0.6, label="Polarity")
        plt.bar(x_axis + 0.3, subjectivity_scores, 0.6, label="Subjectivity")

        # Labels
        plt.xticks(x_axis, songs)
        plt.xlabel("Song Titles", fontsize=10)
        plt.ylabel("Polarity/Subjectivity Scores", fontsize=10)
        plt.title("Subjectivity and Polarity of Kanye's songs")
        plt.axhline(0, color="black", linewidth=1, linestyle="--")

        # Show plot
        plt.legend()
        plt.show()

    def readability_graph(self):
        """ readability subplots for each file """

        # Data
        labels = list(self.data['flesch_reading_ease'].keys())
        num_files = len(labels)
        flesch_scores = list(self.data['flesch_reading_ease'].values())
        gunning_scores = list(self.data['gunning_fog'].values())

        # Subplot Dimensions
        rows = int(np.ceil(np.sqrt(num_files)))
        cols = int(np.ceil(num_files / rows))

        # Subplots
        fig, axes = plt.subplots(rows, cols, figsize=(15, rows * 5))
        if num_files == 1:
            axes = [axes]  # Wrap single subplot in a list
        else:
            axes = axes.flatten()  # Flatten array of subplots for easy indexing

        for i, label in enumerate(labels):
                ax = axes[i]
                ax.bar(["Flesch", "Gunning"], [flesch_scores[i], gunning_scores[i]],
                       color=["skyblue", "lightgreen"])
                ax.set_title(label)
                ax.set_ylabel("Score")
                ax.set_ylim(0, 100)
