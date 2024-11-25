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
from preprocessor import compute_rhyme_density
from preprocessor import compute_word_repetition
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
        raw_text = load_text(filename)

        # Clean the text for readability
        minimally_cleaned_text = clean_text(raw_text, preserve_punctuation=True)

        # Clean the text removing punctuation and stop words
        fully_cleaned_text = clean_text(raw_text, stop_words=self.stop_words)

        # Store minimally and fully cleaned text
        results["minimally_cleaned_text"] = minimally_cleaned_text
        results["fully_cleaned_text"] = fully_cleaned_text

        # Get word counts
        word_counts = compute_word_count(fully_cleaned_text)
        results["wordcount"] = word_counts

        # Get unique words
        unique_words = len(extract_unique_words(fully_cleaned_text))
        results["unique words"] = unique_words

        # Get word repetition
        percent_repeated_words = compute_word_repetition(fully_cleaned_text)
        results["word_repetition"] = percent_repeated_words

        # Get sentiment
        sentiment = compute_sentiment(minimally_cleaned_text)
        results.update(sentiment)

        # Get rhyme density
        rhyme_density = compute_rhyme_density(fully_cleaned_text)
        results["rhyme_density"] = rhyme_density

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
        raw_text = load_website(url, div_class)

        # Clean the text for readability
        minimally_cleaned_text = clean_text(raw_text, preserve_punctuation=True)

        # Clean the text removing punctuation and stop words
        fully_cleaned_text = clean_text(raw_text, stop_words=self.stop_words)

        # Store minimally and fully cleaned text
        results["minimally_cleaned_text"] = minimally_cleaned_text
        results["fully_cleaned_text"] = fully_cleaned_text

        # Get word counts
        word_counts = compute_word_count(fully_cleaned_text)
        results["wordcount"] = word_counts

        # Get unique words
        unique_words = len(extract_unique_words(fully_cleaned_text))
        print(f"Unique words: {unique_words}")
        results["unique words"] = unique_words

        # Get word repetition
        percent_repeated_words = compute_word_repetition(fully_cleaned_text)
        print(f"Word repetition: {percent_repeated_words}")
        results["word_repetition"] = percent_repeated_words

        # Get sentiment
        sentiment = compute_sentiment(minimally_cleaned_text)
        results.update(sentiment)

        # Get rhyme density
        rhyme_density = compute_rhyme_density(fully_cleaned_text)
        results["rhyme_density"] = rhyme_density

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
        """Graph comparing sentiment analysis"""
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

    def lyrics_analysis_graph(self):
        """
        Creates subplots with rhyme density information for each song.
        Subplot dimensions are hardcoded to 3 columns with dynamic rows.
        """

        # Data
        labels = list(self.data["rhyme_density"].keys())
        rhyme_densities = self.data["rhyme_density"]
        unique_words = self.data["unique words"]  # Fix: Ensure correct access
        word_repetitions = self.data["word_repetition"]

        # Subplot dimensions
        cols = 3
        num_files = len(labels)
        rows = int(np.ceil(num_files / cols))

        # Create subplots
        fig, axes = plt.subplots(rows, cols, figsize=(20, rows * 6))
        axes = axes.flatten()  # Flatten axes array for easy indexing

        for i, label in enumerate(labels):
            ax = axes[i]

            # Create secondary y-axis for rhyme density
            ax2 = ax.twinx()

            # Bar plot for word repetition and unique words
            ax.bar(
                ["Unique Words", "Repetition (%)"],
                [
                    unique_words.get(label, 0),  # Access unique words correctly
                    word_repetitions.get(label, 0),
                ],
                color=["purple", "orange"],
                label=["Unique Words", "Repetition (%)"]
            )

            # Line plot for rhyme density on secondary y-axis
            ax2.plot(
                ["Rhyme Density"],
                [rhyme_densities.get(label, 0)],
                color="cyan",
                linestyle="--",
                marker="o",
                label="Rhyme Density"
            )

            # Titles and labels
            ax.set_title(f"Lyrical Analysis: {label}")
            ax.set_ylim(0, max(
                max(unique_words.values(), default=0),
                max(word_repetitions.values(), default=0)) + 10
                        )
            ax2.set_ylim(0, max(rhyme_densities.values(), default=0) + 0.1)

            ax.set_ylabel("Unique Words / Repetition (%)")
            ax2.set_ylabel("Rhyme Density")

            # Add legends for both axes
            ax.legend(loc="upper left")
            ax2.legend(loc="upper right")

        # Adjust layout and display
        plt.tight_layout()
        plt.show()
