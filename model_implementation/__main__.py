"""
File: __main__.py
Description: Example app utilizing the GeoDeepDive infrastructure and products
    to find ignimbrite mentions in the literature.
Assumes: make setup-local has been run (so that the example database is populated)
"""
import click
from urllib.request import urlretrieve
from tempfile import NamedTemporaryFile
from sqlalchemy.exc import ProgrammingError
from os import makedirs
from os.path import join, dirname, abspath, exists
from json import load
from subprocess import run
import re

from GDDTools import Sentence

from .database import session, nlp, reflect_table, run_query, credentials
from .location import locations, named_locations
from .util import terms, overlaps
from sqlalchemy.sql.expression import insert

__here__ = dirname(__file__)

ignimbrite_terms = terms('ignimbrite','tuff')
age_terms = terms('Ma','Myr', 'm.y.', 'm.y.r','Ga','Gyr','Ka','Kyr','39Ar','40Ar')
unit_types = terms('Member','Formation','Group','Supergroup','Tuff','Volcanic')

@click.group()
def cli():
    pass

@cli.command()
def setup():
    """Set up required database extensions and tables"""
    try:
        run_query('setup_database')
    except ProgrammingError:
        click.echo("Extension already exists")

@cli.command(name='load-test-data')
@click.argument('filename', required=False, type=click.File())
def load_test_data(filename=None):
    """Set up required database extensions and tables"""
    if filename is None:
        filename = abspath(join(__here__, '..', 'input', 'sentences_nlp352'))
    run_query('load_test_data', filename=filename)

@cli.command(name='dump-database')
def dump_databased():
    """Set up required database extensions and tables"""
    pg = credentials['postgres']
    cmd = ('pg_dump','-Fc','--exclude-table=ignimbrites_sentences_nlp352',
           '-h', pg['host'], '-p', str(pg['port']), '-U', pg['username'], '-d', pg['database'])
    run(cmd)

@cli.command()
def mentions():
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
        print(sentence.document, sentence.id)
        ignimbrite_words = (w for w in sentence if w.lemma in ignimbrite_terms)
        for word in ignimbrite_words:
            refs = [w for w
                    in sentence.words_referencing(word)
                    if w.is_adjective or w.is_adverb or w.is_verb]

            print(word, " ".join(str(s) for s in refs))
            print()
            stmt = insert(table).values(
                docid=sentence.document,
                sentid=sentence.id,
                wordidx=word.index,
                word=str(word),
                refs=[str(w) for w in refs],
                ref_poses=[w.pose for w in refs]
            )
            session.execute(stmt)
        session.commit()

cli.command(name='locations')(locations)
cli.command(name='named-locations')(named_locations)

@cli.command(name='ages')
def ages():
    run_query('create_ages_table')
    table = reflect_table('ignimbrite_age')

    res = (session.query(nlp)
        .filter(nlp.c.lemmas.overlap(age_terms))
        .filter(nlp.c.lemmas.overlap(ignimbrite_terms))
    )

    age_range = re.compile("(\d+(?:\.\d+)?)(?: ± (\d+(?:\.\d+)?))?(?: ?(-*|to|and) ?(\d+(?:\.\d+)?))? ?([Mk]a)")
    for row in res:
        sentence = Sentence(row)
        __ = age_range.findall(str(sentence))
        for match in __:
            (age, error, sep, end_age, unit) = match
            def fix_age(val):
                if val == '':
                    val = None
                if val is None:
                    return val
                val = float(val)
                if unit == 'ka':
                    val /= 1000
                return val

            stmt = insert(table).values(
                docid=sentence.document,
                sentid=sentence.id,
                age=fix_age(age),
                error=fix_age(error),
                end_age=fix_age(end_age))
            session.execute(stmt)
        session.commit()


@cli.command(name='import-papers')
def import_papers():
    """
    Import papers from bibjson file
    """
    with open(join(__here__,'..','input','bibjson')) as f:
        data = load(f)

    run_query('create_papers_table')
    table = reflect_table('ignimbrite_paper')

    for i in data:
        i['docid'] = i.pop('_gddid')

        __ = insert(table).values(**i)
        session.execute(__)
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

    # Get unit periods from macrostrat
    periods = [r[0] for r in run_query('get_periods')]

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
            # Period
            period = None

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
                if any(p in prev.lemma for p in periods):
                    # The unit is preceded with word containing an identified geological period
                    period = str(prev)
                    break
                if prev.lemma in unit_types:
                    # We are stepping on previously identified units that are adjacent
                    break
                if prev.lemma in age_terms:
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
                period=period,
                docid=sentence.document,
                sentid=sentence.id)
            session.execute(stmt)
        session.commit()

@cli.command(name='load-macrostrat')
def load_macrostrat():
    "Load macrostrat data into database"
    with NamedTemporaryFile(delete=True) as f:
        urlretrieve("https://macrostrat.org/api/defs/intervals?all&format=csv", f.name)
        run_query("create_periods_table", filename=f.name)


if __name__ == '__main__':
    cli()
