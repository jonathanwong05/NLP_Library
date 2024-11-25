"""
File: preprocessor.py
Description: Preprocessor functions to be used in text_library.py

Authors: Vichu Selvaraju & Jon Wong
"""

import re
from collections import Counter
import textstat
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
import pronouncing


def load_website(url, div_class):
    """Loads a website's text

    Args:
        url (string): Url of the website
        div_class (string): Div class of text

    Returns:
        string: Text from the website
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        text_divs = soup.find_all("div", class_=div_class)
        text = "\n".join(div.get_text(separator="\n").strip() for div in text_divs)
    return text


def load_text(filename):
    """Load text from a file

    Args:
        filename (string): Name of the file

    Returns:
        string: Text of the file
    """
    with open(filename, "r") as file:
        text = file.read()
    return text


def clean_text(text, stop_words=None, preserve_punctuation=False):
    """Cleans the text

    Args:
        text (string): The text to be cleaned
        stop_words (set, optional): Set of stop words to remove from text. Defaults to None.

    Returns:
        string: Cleaned text
    """
    if not preserve_punctuation:
        # Remove punctuation
        text = re.sub(r"[^\w\s]", "", text)
    else:
        # Remove all punctuation except sentence-ending punctuation
        text = re.sub(r"[^\w\s.!?]", "", text)

    # Lowercase
    text = text.lower()

    # Split into words
    words = text.split()

    # Remove stop words
    if stop_words:
        words = [word for word in words if word not in stop_words]

    # Join words back into single string
    return " ".join(words)


def tokenize_text(text):
    """Tokenizes the input text into list of words

    Args:
        text (text): Input text

    Returns:
        list: List of words in text
    """
    return text.split()


def compute_word_count(text):
    """Computes frequency of each word in the text

    Args:
        text (string): Input text

    Returns:
        dictionary: Frequency of each word in text
    """
    words = tokenize_text(text)
    return Counter(words)


def compute_rhyme_density(text):
    """Computes the density of rhymes in a text

    Returns:
        float: Rhyme density (number of rhyming words / total words).
    """
    words = text.split()

    # Find rhymes for each word
    rhymes = set()
    for word in words:
        rhymes.update(pronouncing.rhymes(word.lower()))  # Ensure lowercase for matching

    # Count rhyming words
    rhyme_count = sum(1 for word in words if word in rhymes)

    # Calculate rhyming density
    return rhyme_count / len(words)


def compute_sentiment(text):
    """Computes sentiment analysis for the text

    Args:
        text (string): Input text

    Returns:
        dictionary: Sentiment scores
    """
    blob = TextBlob(text)
    return {
        "polarity": blob.sentiment.polarity,
        "subjectivity": blob.sentiment.subjectivity,
    }


def extract_unique_words(text):
    """Extracts a set of unique words from the text

    Args:
        text (string): Input text

    Returns:
        set: Set of unique words
    """
    words = tokenize_text(text)
    return set(words)


def compute_word_repetition(text):
    """
    Computes the percentage of repeated words in a text.

    Args:
        text (string): Input text.

    Returns:
        float: Percentage of repeated words.
    """
    words = text.split()
    word_counts = Counter(words)
    repeated_words = sum(count - 1 for count in word_counts.values() if count > 1)
    return repeated_words / len(words) * 100
