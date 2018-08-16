# Recognizing locations from Stanford NER
# http://ricedh.github.io/03-ner.html

from .sentence import Sentence
from .database import session, nlp, reflect_table, run_query

def named_locations():
    res = session.query(nlp).filter(
        nlp.c.ners.overlap(['LOCATION']))

    for row in res:
        v = Sentence(row)
        loc_ixs = [i for i,v in enumerate(v) if v.ner == 'LOCATION']
        phrases = []
        for i in loc_ixs:
            if i-1 in loc_ixs:
                phrases[-1] += f" {v[i]}"
            elif i-2 in loc_ixs:
                phrases[-1] += f" {v[i-1]} {v[i]}"
            else:
                phrases.append(str(v[i]))


    import IPython; IPython.embed(); raise
