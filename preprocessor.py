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


def clean_text(text, stop_words=None):
    """Cleans the text

    Args:
        text (string): The text to be cleaned
        stop_words (set, optional): Set of stop words to remove from text. Defaults to None.

    Returns:
        string: Cleaned text
    """
    # Remove punctuation
    text = re.sub(r"[^\w\s]", "", text)

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


def compute_readability(text):
    """Compute readability scores for the text

    Args:
        text (string): Input text

    Returns:
        dictionary: Readability scores
    """
    return {
        "flesch_reading_ease": textstat.flesch_reading_ease(text),
        "gunning_fog": textstat.gunning_fog(text),
    }


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
