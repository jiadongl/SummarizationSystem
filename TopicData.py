import nltk
import string


IgnoredWords = ['the', 'of', 'a', 'to', 'that', 'and', 'in', '``', "''"]
CueWords = ['therefore', 'hence', 'lastly', 'finally', 'meanwhile']


def word_tokenize(sentence):
    words = []
    for word in nltk.word_tokenize(sentence):
        if word not in string.punctuation and word not in IgnoredWords:
            word = nltk.stem.PorterStemmer().stem(word)
            words.append(word)
    return words


class TopicData:

    def __init__(self):
        return
