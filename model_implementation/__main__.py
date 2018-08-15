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
nlp = Table(__tablename, meta, autoload=True)

ignimbrite_terms = ['ignimbrite','welded','tuff']
age_terms = ['ma','myr','ga','gyr','ka','kyr','39Ar','40Ar']
unit_types = ['Member','Formation','Group','Supergroup','member','formation','group','supergroup']

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
