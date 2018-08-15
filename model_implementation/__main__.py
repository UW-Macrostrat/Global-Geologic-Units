"""
File: __main__.py
Description: Example app utilizing the GeoDeepDive infrastructure and products
    to find ignimbrite mentions in the literature.
Assumes: make setup-local has been run (so that the example database is populated)
"""
import click
import IPython

from .database import session, nlp, reflect_table, run_query
from .sentence import Sentence
from .util import terms, overlaps
from sqlalchemy.sql.expression import insert

ignimbrite_terms = terms('ignimbrite','welded','tuff')
age_terms = terms('Ma','Myr','Ga','Gyr','Ka','Kyr','39Ar','40Ar')
unit_types = terms('Member','Formation','Group','Supergroup','Tuff')

@click.group()
def cli():
    pass

@cli.command()
def ignimbrites():
    """Writes a table indexing sentences mentioning ignimbrites"""
    # Filter by lemmas using the PostgreSQL engine directly
    # This is much quicker than filtering in Python.
    # In general, all logic that can be pushed to SQL should be...

    run_query('create_mention_table')
    table = reflect_table('ignimbrite_mention')

    res = session.query(nlp).filter(
        nlp.c.lemmas.overlap(ignimbrite_terms))

    for row in res:
        sentence = Sentence(row)
        # More advanced logic would go here
        print(sentence)
        print("")
        stmt = insert(table).values(
            docid=sentence.document,
            sentid=sentence.id)
        session.execute(stmt)
    session.commit()

@cli.command()
def units():
    """Writes a table containing geologic unit mentions"""

    # Instead of creating table in raw SQL and then reflecting,
    # we could define it's schema directly in the SQLAlchemy ORM.
    run_query('create_unit_table')
    table = reflect_table('ignimbrite_unit')

    res = session.query(nlp).filter(
        nlp.c.lemmas.overlap(unit_types))

    for row in res:
        sentence = Sentence(row)
        # iterate pairwise through units, as each `unit_type`
        # must be preceded by at least one proper name
        for word in sentence:
            if not word.lemma in unit_types:
                continue
            __ = [word]
            prev = word.previous()

            # Upper, middle, lower, etc.
            position = None

            # Hack to allow continue from within while loop
            # ...there is probably a cleaner way to do this
            _should_exit = False
            while prev is not None:
                if not prev.is_proper_noun:
                    break
                # Should institute a check for geologic unit map ids e.g.
                # `Tsvl`, `Qal` as these seem to be categorized as proper nouns.
                if prev.lemma in terms('Working','Research', 'Data'):
                    # Often `Groups` are actually functional groups of people!
                    __ = None
                    break
                if prev.lemma in terms('Upper', 'Middle', 'Lower'):
                    # Filter out upper, middle lower
                    position = str(prev)
                    break

                # Build an array back to front catching multiword units
                __.append(prev)
                prev = prev.previous()
            if __ is None or len(__) < 2:
                continue
            __.reverse()

            name = " ".join(str(i) for i in __)
            print(name)
            stmt = insert(table).values(
                name=name,
                short_name=" ".join(str(i) for i in __[:-1]),
                position=position,
                docid=sentence.document,
                sentid=sentence.id)
            session.execute(stmt)
    session.commit()

if __name__ == '__main__':
    cli()
