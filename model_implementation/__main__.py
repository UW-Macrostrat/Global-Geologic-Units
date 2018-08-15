"""
File: __main__.py
Description: Example app utilizing the GeoDeepDive infrastructure and products
    to find ignimbrite mentions in the literature.
Assumes: make setup-local has been run (so that the example database is populated)
"""
import click
import IPython

from .database import session, nlp, run_query
from .sentence import Sentence
from .util import terms, overlaps
from sqlalchemy.sql.expression import insert

ignimbrite_terms = terms('ignimbrite','welded','tuff')
age_terms = terms('Ma','Myr','Ga','Gyr','Ka','Kyr','39Ar','40Ar')
unit_types = terms('Member','Formation','Group','Supergroup')

@click.group()
def cli():
    pass

@cli.command()
def ignimbrites(count, name):
    """Writes a table indexing sentences mentioning ignimbrites"""
    # Filter by lemmas using the PostgreSQL engine directly
    # This is much quicker than filtering in Python.
    res = session.query(nlp).filter(
        nlp.c.lemmas.overlap(ignimbrite_terms))

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


@cli.command()
def units():
    """Writes a table containing geologic unit data"""

    run_query('create_unit_table')

    res = session.query(nlp).filter(
        nlp.c.lemmas.overlap(unit_types))

    for row in res:
        sentence = Sentence(row)
        # iterate pairwise through units, as each `unit_type`
        # must be preceded by at least one proper name
        for w1,w2 in zip(sentence[:-1], sentence[1:]):
            if not w1.is_proper_noun:
                continue
            if not w2.lemma in unit_types:
                continue
            # Build an array back to front
            __ = [w2,w1]
            # Expand to catch multiword units
            prev = w1.previous()
            while prev is not None:
                if not prev.is_proper_noun:
                    break
                    # Should institute a check for geologic unit map ids e.g.
                    # `Tsvl`, `Qal` as these seem to be categorized as proper nouns.
                __.append(prev)
                prev = prev.previous()
            __.reverse()

            name = " ".join(str(i) for i in __)
            print(name)

if __name__ == '__main__':
    cli()
