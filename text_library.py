"""
File: text_library.py
Description: A reusable library for text analysis and comparison
In theory, the framework should support any collection of texts
of interest (though this might require the implementation of some
custom parsers.)

Authors: Vichu Selvaraju, Jon Wong & Ian Menachery
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
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
        """Graph comparing normalized sentiment analysis"""

        # Data for plots
        songs = list(self.data["polarity"].keys())
        polarity_scores = np.array(list(self.data["polarity"].values())).reshape(-1, 1)
        subjectivity_scores = np.array(
            list(self.data["subjectivity"].values())
        ).reshape(-1, 1)

        # Normalize data using MinMaxScaler
        scaler = MinMaxScaler()
        normalized_polarity = scaler.fit_transform(polarity_scores).flatten()
        normalized_subjectivity = scaler.fit_transform(subjectivity_scores).flatten()

        # X-axis values
        x_axis = np.arange(0, len(songs) * 2, 2)

        # Plots
        plt.bar(
            x_axis - 0.4,
            normalized_polarity,
            0.4,
            label="Polarity (Normalized)",
            color="blue",
        )
        plt.bar(
            x_axis + 0.4,
            normalized_subjectivity,
            0.4,
            label="Subjectivity (Normalized)",
            color="orange",
        )

        # Labels
        plt.xticks(x_axis, songs, rotation=30, ha="right", fontsize=10)
        plt.xlabel("Song Titles", fontsize=10)
        plt.ylabel("Normalized Scores", fontsize=10)
        plt.title("Normalized Subjectivity and Polarity of Songs")
        plt.axhline(0, color="black", linewidth=1, linestyle="--")

        # Legend
        plt.legend()

        # Adjust layout and show plot
        plt.tight_layout()
        plt.show()

    def lyrics_analysis_graph(self):
        """
        Creates subplots with normalized rhyme density, unique words,
        and word repetition data for each song using sklearn MinMaxScaler.
        Subplot dimensions are hardcoded to 3 columns with dynamic rows.
        The ticks are adjusted to represent normalized data values.
        """

        # Data
        labels = list(self.data["rhyme_density"].keys())
        rhyme_densities = self.data["rhyme_density"]
        unique_words = self.data["unique words"]
        word_repetitions = self.data["word_repetition"]

        # Prepare data for normalization
        scaler = MinMaxScaler()
        data = {
            "rhyme_density": list(rhyme_densities.values()),
            "unique_words": list(unique_words.values()),
            "word_repetitions": list(word_repetitions.values()),
        }

        # Normalize data
        normalized_data = scaler.fit_transform(np.array(list(data.values())).T)
        normalized_rhyme_densities = dict(zip(labels, normalized_data[:, 0]))
        normalized_unique_words = dict(zip(labels, normalized_data[:, 1]))
        normalized_word_repetitions = dict(zip(labels, normalized_data[:, 2]))

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

            # Bar plot for normalized word repetition and unique words
            bar_labels = ["Unique Words (Norm.)", "Repetition (%) (Norm.)"]
            ax.bar(
                bar_labels,
                [
                    normalized_unique_words.get(label, 0),  # Access normalized data
                    normalized_word_repetitions.get(label, 0),
                ],
                color=["purple", "orange"],
                label=bar_labels,
            )

            # Line plot for normalized rhyme density on secondary y-axis
            ax2.plot(
                ["Rhyme Density (Norm.)"],
                [normalized_rhyme_densities.get(label, 0)],
                color="cyan",
                linestyle="--",
                marker="o",
                label="Rhyme Density (Norm.)",
            )

            # Titles and labels
            ax.set_title(f"Lyrical Analysis: {label}")
            ax.set_ylim(0, 1)  # Normalized range
            ax2.set_ylim(0, 1)  # Normalized range

            ax.set_ylabel("Normalized Unique Words / Repetition (%)")
            ax2.set_ylabel("Normalized Rhyme Density")

            # Add legends for both axes
            ax.legend(loc="upper left")
            ax2.legend(loc="upper right")

            # Adjust x-axis ticks and labels
            ax.set_xticks(range(len(bar_labels) + 1))
            ax.set_xticklabels(bar_labels + ["Rhyme Density (Norm.)"])

        # Hide unused subplots if the number of songs is less than rows * cols
        for j in range(num_files, rows * cols):
            fig.delaxes(axes[j])

        # Adjust layout and add extra spacing
        plt.tight_layout()
        plt.subplots_adjust(
            hspace=0.6, wspace=0.5
        )  # Adjust vertical and horizontal spacing

        # Display the plot
        plt.show()
