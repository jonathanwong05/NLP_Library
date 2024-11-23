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
import matplotlib.pyplot as plt
import textstat
from textblob import TextBlob
import re

class TextLibrary:

    def __init__(self):
        """ Constructor

        datakey --> (filelabel --> datavalue)
        """
        self.data = defaultdict(dict)
        self.stop_words = set()

    def clean_text(self, text):
        """
        Cleans the input text by:
        - Lowercasing the text
        - Removing punctuation
        - Removing extra whitespace
        - Optionally filtering out stop words
        :param text: The raw input text to be cleaned
        :return: The cleaned text
        """
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)

        # Lowercase
        text = text.lower()

        # Split into words
        words = text.split()

        # Remove stop words
        if self.stop_words:
            words = [word for word in words if word not in self.stop_words]

        # Join words back into single string
        return ' '.join(words)

    def tokenize_text(self, text):
        """
        Tokenizes the input text into a list of words.
        """
        return text.split()

    def compute_word_count(self, text):
        """
        Computes the frequency of each word in the text.
        """
        words = self.tokenize_text(text)
        return Counter(words)

    def compute_readability(self, text):
        """
        Computes readability scores for the text.
        """
        return {
            'flesch_reading_ease': textstat.flesch_reading_ease(text),
            'gunning_fog': textstat.gunning_fog(text)
        }

    def compute_sentiment(self, text):
        """
        Computes sentiment analysis for the text.
        """
        blob = TextBlob(text)
        return {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }

    def default_parser(self, filename):
        """ Parse a standard text file and produce
        extract data results in the form of a dictionary. """

        results = {
            'wordcount': Counter("To be or not to be".split(" ")),
            'numwords' : rnd.randrange(10, 50)
        }

        return results

    def load_stop_words(self, stopwords_file):
        pass




    def load_text(self, filename, label=None, parser=None):
        """ Register a document with the framework.
        Extract and store data to be used later by
        the visualizations """
        if parser is None:
            results = self.default_parser(filename)
        else:
            results = parser(filename)

        if label is None:
            label = filename

        for k, v in results.items():
            self.data[k][label] = v

    def compare_num_words(self):
        """ This is a very simplistic visualization that creates
        a bar chart comparing number of words.   (Not intended
        for your project.)  """

        num_words = self.data['numwords']
        for label, nw in num_words.items():
            plt.bar(label, nw)
        plt.show()