"""
File: sentence.py
Description: A set of classes to represent an NLP352-encoded sentence
    and enable natural manipulation of tokens.
"""

class Word(object):
    """
    Class to represent word within a sentence.
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

    def lower(self):
        return self.text.lower()

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"{self.text}: {self.pose}, {self.ner}"

    @property
    def is_bad(self):
        """
        Boolean logic identifying non-word
        text miscategorized as words.
        """
        # Throws out empty strings
        if len(self.text) == 0:
            return True
        # Throws out `________` words
        if all(i == '_' for i in self.text):
            return True
        return False

    @property
    def is_noun(self):
        return 'NN' in self.pose

    @property
    def is_adjective(self):
        return 'JJ' in self.pose

    @property
    def is_verb(self):
        return 'VB' in self.pose

    @property
    def is_adverb(self):
        return 'RB' in self.pose

    @property
    def is_proper_noun(self):
        if self.is_bad:
            return False
        if not self.is_noun:
            return False
        if self.pose in ['NNP','NNPS']:
            return True
        if self.pose == 'NN' and self.text[0].isupper():
            return True
        return False

    @property
    def parent(self):
        if self.dep_parent is None:
            return None
        # Make sure we don't get an infinite loop
        if self.dep_parent == self.index:
            return None
        return self.sentence[self.dep_parent]

    @property
    def tree(self):
        """
        Get word's chain of references
        """
        p = self
        while p is not None:
            yield p
            p = p.parent

    def print_tree(self):
        p = self.parent
        txt = str(self)
        txt += f" ({self.pose} {self.ner})"
        while p is not None:
            txt += " → "+str(p)
            p = p.parent
        print(txt)

    def previous(self):
        ix = self.index-1
        if ix == -1:
            return None
        return self.sentence[ix]

class Sentence(object):
    def __init__(self, sentence):
        """
        Class should be initialized by passing a SQLAlchemy row object
        representing a single sentence.
        """
        self.__raw__ = sentence
        r = self.__raw__
        self.lemmas = r.lemmas
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
                (" -RSB-","]"),
                ("◦","°"),
                (" °", "°")]
        for s in subs:
            joined=joined.replace(*s)
        return joined

    def words_referencing(self, word):
        """
        Get words referencing another word in the sentence
        """
        for w in self:
            tree = list(w.tree)
            if word in tree and w != word:
                yield w

    @property
    def document(self):
        return self.__raw__.docid

    @property
    def id(self):
        return self.__raw__.sentid

    def print_breakdown(self):
        for word in self.words:
            word.print_tree()

    def __iter__(self):
        return (s for s in self.words)

    def __getitem__(self, ix):
        return self.words[ix]

