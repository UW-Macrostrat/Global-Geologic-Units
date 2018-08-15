"""
File: example_app.py
Description: Example app utilizing the GeoDeepDive infrastructure and products.
    This will look at the produced NLP table and print a list of proper nouns which
    are modified by adjectives, along with the sentence id in which they occur.
Assumes: make setup-local has been run (so that the example database is populated)
"""

import yaml

from .database import session, nlp
from .sentence import Sentence

def terms(*items):
    "Provides both a capitalized and uncapitalized version of strings"
    for item in items:
        yield item.lower()
        yield item.capitalize()

ignimbrite_terms = terms('ignimbrite','welded','tuff')
age_terms = terms('Ma','Myr','Ga','Gyr','Ka','Kyr','39Ar','40Ar')
unit_types = terms('Member','Formation','Group','Supergroup')

# Filter by lemmas using the PostgreSQL engine directly
# This is much quicker than filtering in Python.
res = session.query(nlp).filter(
    nlp.c.lemmas.overlap(ignimbrite_terms))

def overlaps(l1,l2):
    for v in l2:
        if v in l1:
            return True
    return False

count=0
sentences = []
units = []
for row in res:
    sentence = Sentence(row)

    print(count)
    print(sentence.document, sentence.id)
    print(str(sentence))
    if overlaps(sentence.lemmas, age_terms):
        print("Has age")
    print(" ")
    # For introspection
    sentences.append(sentence)
    count+=1

    # Formations
    for w1,w2 in zip(sentence[:-1], sentence[1:]):
        if not w1.is_proper_noun:
            continue
        if not w2.lemma in unit_types:
            continue
        __ = [w1,w2]
        # Expand to catch multiword units
        prev = w1.previous()
        while prev.is_proper_noun:
            # Should institute a check for geologic unit map ids e.g.
            # `Tsvl`, `Qal` as these throw things off a lot.
            __ = [prev] + __
            prev = prev.previous()
            if prev is None:
                break

        name = " ".join(str(i) for i in __)

        units.append(name)

import IPython; IPython.embed(); raise
