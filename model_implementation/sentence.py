"""
File: sentence.py
Description: A set of classes to represent an NLP352-encoded sentence
    and enable natural manipulation of tokens.
"""

class Word(object):
    """
    This class should not be initialized directly as it depends
    on the keyword arguments being set correctly
    """
    def __init__(self, **kw):
        for k,v in kw.items():
            setattr(self, k,v)
        # Correct for 1-indexing of parent data
        if self.dep_parent == 0:
            self.dep_parent = None
        else:
            self.dep_parent -= 1

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"{self.text}: {self.pose}, {self.ner}"

    @property
    def parent(self):
        if self.dep_parent is None:
            return None
        return self.sentence.words[self.dep_parent]

    @property
    def tree(self):
        p = self.parent
        txt = str(self)
        while p is not None:
            txt += " → "+str(p)
            p = p.parent
        return txt

class Sentence(object):
    def __init__(self, sentence):
        """
        Class should be initialized by passing a SQLAlchemy row object
        representing a single sentence.
        """
        self.__raw__ = sentence
        r = self.__raw__
        self.words = []
        for i, word in enumerate(sentence.words):
            w = Word(
                text=word,
                sentence=self,
                # We're doing zero-indexing here, despite 1-indexing of parent data
                index=i,
                pose=r.poses[i],
                ner=r.ners[i],
                lemma=r.lemmas[i],
                dep_path=r.dep_paths[i],
                dep_parent=r.dep_parents[i]
                )
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

    def print_breakdown(self):
        for word in self.words:
            print(repr(word))

    def __iter__(self):
        return (s for s in self.words)

    def __getitem__(self, ix):
        return self.words[ix]

