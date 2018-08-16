"""
File: __main__.py
Description: Example app utilizing the GeoDeepDive infrastructure and products
    to find ignimbrite mentions in the literature.
Assumes: make setup-local has been run (so that the example database is populated)
"""
import click
from urllib.request import urlretrieve
from tempfile import NamedTemporaryFile
import re

from .database import session, nlp, reflect_table, run_query
from .sentence import Sentence
from .util import terms, overlaps
from sqlalchemy.sql.expression import insert
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

ignimbrite_terms = terms('ignimbrite','welded','tuff')
age_terms = terms('Ma','Myr','Ga','Gyr','Ka','Kyr','39Ar','40Ar')
unit_types = terms('Member','Formation','Group','Supergroup','Tuff','Volcanic')

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
def locations():
    res = session.query(nlp).filter(
        nlp.c.lemmas.overlap(age_terms))

    # We want to employ more complex logic here,
    # so we define the query directly in SQL
    res = run_query('get_location_sentences')

    # Regex to parse common DMS and DD location coordinates
    expr = re.compile(" ((\d+(?:\.\d+)?)°([\d '`\"]+)([NSEW]))")

    # Regex to parse possible minute-second pairs to numbers
    expr2 = re.compile("[\d\.]+")


    def dms2dd(degrees, minutes=0, seconds=0):
        return degrees + minutes/60 + seconds/3600

    for row in res:
        lats = []
        lons = []
        sentence = Sentence(row)
        text = str(sentence)
        pos = 0
        matches = expr.findall(text)
        if len(matches) < 2:
            # We need at least two to have a hope of
            # finding a lat-lon pair
            continue
        for match, deg, minute_second, cardinal_direction in matches:
            deg = float(deg)
            if not minute_second.isspace():
                ms = expr2.findall(minute_second)
                def __get_value(ix):
                    try:
                        return float(ms[ix])
                    except IndexError:
                        return 0

                deg = dms2dd(deg,
                    minutes=__get_value(0),
                    seconds=__get_value(1))
            if cardinal_direction in ['S','W']:
                deg *= -1
            if cardinal_direction in ('N','S'):
                lons.append(deg)
            else:
                lats.append(deg)
        if not len(lons)*len(lats):
            continue
        # Get rid of sentences where there is too
        # wide a spread of lon/lat values (probably
        # signifying some sort of map labels).
        if max(lons)-min(lons) > 5:
            continue
        if max(lats)-min(lats) > 5:
            continue

        # We average for now
        # ...more interesting would be to create
        # and record bounding boxes
        mean = lambda x: sum(x)/len(x)
        lon = mean(lons)
        lat = mean(lats)

        print(sentence)
        print(lon, lat)
        print("")

        point = from_shape(Point(lon,lat),srid=4326)

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
                if prev.lemma in periods:
                    # The unit is preceded with an identified geological period
                    period = str(prev)
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
