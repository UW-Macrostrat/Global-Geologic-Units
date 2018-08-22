# Recognizing locations from Stanford NER
# http://ricedh.github.io/03-ner.html
import re
from click import secho
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from sqlalchemy.sql.expression import insert

from GDDTools import Sentence

from .database import session, nlp, reflect_table, run_query

def dms2dd(degrees, minutes=0, seconds=0):
    return degrees + minutes/60 + seconds/3600

def locations():
    "Get locations in degrees"
    run_query('create_locations_table')
    table = reflect_table('global_geology_location')

    # We want to employ more complex logic here,
    # so we define the query directly in SQL
    res = run_query('get_location_sentences')

    # Regex to parse common DMS and DD location coordinates
    expr = re.compile("[\s]((\d+(?:\.\d+)?)°([\d\s′'`\"]*)([NSEW]))\W")

    # Regex to parse possible minute-second pairs to numbers
    expr2 = re.compile("[\d\.]+")

    for row in res:
        lats = []
        lons = []
        sentence = Sentence(row)
        # Pad sentence with spaces so our regex will match coordinates
        # at the beginning and end of a line.
        text = f" {sentence} "
        pos = 0
        matches = expr.findall(text)
        if len(matches) < 2:
            # We need at least two matches to have any hope of
            # finding an X-Y coordinate pair
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
        secho(f"{len(lons)} longitudes and {len(lats)} latitudes found", fg='green')
        secho(f"{lon} {lat}", fg='green')
        print("")

        point = from_shape(Point(lon,lat),srid=4326)

        stmt = insert(table).values(
            geometry=point,
            docid=sentence.document,
            sentid=sentence.id,
            sentence=str(sentence))
        session.execute(stmt)
    session.commit()

