"""
File: example_app.py
Description: Example app utilizing the GeoDeepDive infrastructure and products.
    This will look at the produced NLP table and print a list of proper nouns which
    are modified by adjectives, along with the sentence id in which they occur.
Assumes: make setup-local has been run (so that the example database is populated)
"""

import yaml
import psycopg2
from psycopg2.extensions import AsIs

with open('../credentials.yml', 'r') as credential_yaml:
    credentials = yaml.load(credential_yaml)

with open('../config.yml', 'r') as config_yaml:
    config = yaml.load(config_yaml)

# Connect to Postgres
connection = psycopg2.connect(
    dbname=credentials['postgres']['database'],
    user=credentials['postgres']['user'],
    host=credentials['postgres']['host'],
    port=credentials['postgres']['port'])
cursor = connection.cursor()

proper_nouns_with_adj = {} # key: proper_noun, value: (adjective, sentence_id)

# read all sentences from our NLP example database.
cursor.execute("SELECT * FROM stringed_instruments_sentences_nlp352;")
for sentence in cursor:
    sentid = sentence[1]
    words = sentence[3]
    poses = sentence[4]
    dep_parents = sentence[8]
    proper_nouns = [] # list of proper nouns
    adjectives = [] # list of adjectives
    for idx, pos in enumerate(poses): # look for proper nouns and adjectives
        if pos == "NNP":
            proper_nouns.append(idx)
        elif pos == "JJ":
            adjectives.append(idx)
    for idx, parent in enumerate(dep_parents): # loop over dependencies to look for adjectives which relate to a proper noun
        # within the table, the dep_parents is indexed from 1.  Our internal
        # indexing is from 0, so subtract one.
        if idx in adjectives and parent-1 in proper_nouns:
            if words[parent-1] in proper_nouns_with_adj:
                proper_nouns_with_adj[words[parent-1]].append((words[idx], sentid))
            else:
                proper_nouns_with_adj[words[parent-1]] = [(words[idx], sentid)]

# write results to the output directory
with open("../output/proper_nouns_with_adjectives", "w") as fout:
    for proper_noun in proper_nouns_with_adj.keys():
        fout.write("%s - %s\n" % (proper_noun, proper_nouns_with_adj[proper_noun]))
