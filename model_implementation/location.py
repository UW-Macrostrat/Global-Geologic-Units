# Recognizing locations from Stanford NER
# http://ricedh.github.io/03-ner.html
import re
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from sqlalchemy.sql.expression import insert

from GDDTools import Sentence

from .database import session, nlp, reflect_table, run_query

def locations():
    "Get locations in degrees"
    run_query('create_locations_table')
    table = reflect_table('global_geology_location')

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
                lats.append(deg)
            else:
                lons.append(deg)
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

        stmt = insert(table).values(
            geometry=point,
            docid=sentence.document,
            sentid=sentence.id)
        session.execute(stmt)
    session.commit()

def named_locations():
    run_query('create_named_locations_table')
    table = reflect_table('global_geology_named_location')

    res = session.query(nlp).filter(
        nlp.c.ners.overlap(['LOCATION']))

    for row in res:
        sentence = Sentence(row)
        loc_ixs = [i for i,v in enumerate(sentence) if v.ner == 'LOCATION']
        phrases = []
        for i in loc_ixs:
            if i-1 in loc_ixs:
                phrases[-1] += f" {sentence[i]}"
            elif i-2 in loc_ixs:
                phrases[-1] += f" {sentence[i-1]} {sentence[i]}"
            else:
                phrases.append(str(sentence[i]))

        for phrase in phrases:
            stmt = insert(table).values(
                phrase=phrase,
                docid=sentence.document,
                sentid=sentence.id)
            session.execute(stmt)

    session.commit()

