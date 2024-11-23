import re
from collections import Counter
import textstat
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup


def load_website(url, div_class):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        text_divs = soup.find_all("div", class_=div_class)
        text = "\n".join(div.get_text(separator="\n").strip() for div in text_divs)
    return text


def clean_text(text, stop_words=None):
    """
    Cleans the input text by:
    - Lowercasing the text
    - Removing punctuation
    - Removing extra whitespace
    - Optionally filtering out stop words
    :param text: The raw input text to be cleaned
    :param stop_words: A set of stop words to be removed
    :return: The cleaned text
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
    """
    Tokenizes the input text into list of words
    :param text: input text
    :return: List of words
    """
    return text.split()


def compute_word_count(text):
    """
    Computes frequency of each word in the text
    :param text: input text
    :return: Counter object with word frequencies
    """
    words = tokenize_text(text)
    return Counter(words)


def compute_readability(text):
    """
    Compute readability scores for the text
    :param text: input text
    :return: Dictionary containing readability scores
    """
    return {
        "flesch_reading_ease": textstat.flesch_reading_ease(text),
        "gunning_fog": textstat.gunning_fog(text),
    }


def compute_sentiment(text):
    """
    Computes sentiment analysis for the text
    :param text: input text
    :return: dictionary containing sentiment polarity and subjectivity
    """
    blob = TextBlob(text)
    return {
        "polarity": blob.sentiment.polarity,
        "subjectivity": blob.sentiment.subjectivity,
    }


def extract_unique_words(text):
    """
    Extracts a set of unique words from the text
    :param text: input text
    :return: Set of unique words
    """
    words = tokenize_text(text)
    return set(words)


def website_parser(url, div_class):
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
    text = clean_text(text)

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


results = website_parser(
    "https://genius.com/Kanye-west-all-falls-down-lyrics",
    "Lyrics__Container-sc-1ynbvzw-1 kUgSbL",
)

print(results)
