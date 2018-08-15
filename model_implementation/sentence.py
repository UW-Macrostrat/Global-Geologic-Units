"""
File: sentence.py
Description: A set of classes to represent an NLP352-encoded sentence
    and enable natural manipulation of tokens.
"""

class Word(object):
    def __init__(self, **kw):
        self.text = kw.pop('text')
        self.sentence = kw.pop('sentence', None)

    def __str__(self):
        return self.text

class Sentence(object):
    def __init__(self, sentence):
        """
        Class should be initialized by passing a SQLAlchemy row object
        representing a single sentence.
        """
        self.__raw__ = sentence
        self.words = []
        for i, word in enumerate(sentence.words):
            w = Word(
                text=word,
                sentence=self)
            self.words.append(w)

    def __str__(self):
        """
        Render the sentence to plain text.
        """
        joined=" ".join(str(w) for w in self.words)
        subs = [(" ,", ","),
                (" .", "."),
                ("-LRB- ","("),
                (" -RRB-",")"),
                ("-LSB- ","["),
                (" -RSB-","]")]
        for s in subs:
            joined=joined.replace(*s)
        return joined

