"""
File: example_app.py
Description: Example app utilizing the GeoDeepDive infrastructure and products.
    This will look at the produced NLP table and print a list of proper nouns which
    are modified by adjectives, along with the sentence id in which they occur.
Assumes: make setup-local has been run (so that the example database is populated)
"""

import yaml
from psycopg2.extensions import AsIs
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.engine.url import URL
from os.path import join, dirname
__here__ = dirname(__file__)

def open_relative(fn, mode='r'):
    fn = join(__here__, fn)
    return open(fn, mode)

with open_relative('../credentials.yml') as credential_yaml:
    credentials = yaml.load(credential_yaml)

with open_relative('../config.yml') as config_yaml:
    config = yaml.load(config_yaml)

conn_string = URL(
    drivername='postgres',
    **credentials['postgres'])

Session = sessionmaker()
engine = create_engine(conn_string)
conn = engine.connect()
meta=MetaData(bind=conn)
session = Session(bind=conn)
# read all sentences from our NLP example database.
__tablename = config['app_name']+'_sentences_nlp352'
sentences = Table(__tablename, meta, autoload=True)

res = session.query(sentences)

def intersects(arr1, arr2):
    for word in arr2:
        if word in arr1:
            return True
    return False

ignimbrite_terms = ['ignimbrite','welded','tuff']

count=0
for sentence in res:

    if not intersects(sentence.words, ignimbrite_terms):
        continue
    count+=1
    joined=" ".join(sentence.words)
    subs = [(" ,", ","),
            ("-LRB- ","("),
            (" -RRB-",")"),
            ("-LSB- ","["),
            (" -RSB-","]")]
    for s in subs:
        joined=joined.replace(*s)

    print(count, joined)
    print(" ")

