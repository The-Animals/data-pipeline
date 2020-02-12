from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from textrank_algorithm import HtmlParser
from textrank_algorithm import PlaintextParser
from textrank_algorithm import Tokenizer
from textrank_algorithm import TextRankSummarizer as Summarizer
from textrank_algorithm import Stemmer
from textrank_algorithm import get_stop_words

LANGUAGE = "english"
SENTENCES_COUNT = 10


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Automatic_summarization"
    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))

    # or for plain text files
    # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
    # parser = PlaintextParser.from_string("Check this out.", Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        print(sentence)
