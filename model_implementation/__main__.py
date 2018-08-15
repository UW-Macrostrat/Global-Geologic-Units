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
from .sentence import Sentence
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

ignimbrite_terms = ['ignimbrite','welded','tuff']

# Filter by lemmas using the PostgreSQL engine directly
# This is much quicker than filtering in Python.
res = session.query(sentences).filter(
    sentences.c.lemmas.overlap(ignimbrite_terms))

count=0
for row in res:
    sentence = Sentence(row)

    count+=1

    print(count, str(sentence))
    print(" ")

