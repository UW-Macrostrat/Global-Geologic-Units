import re
from sqlalchemy.sql.expression import insert
from GDDTools import Sentence

from .database import session, nlp, reflect_table, run_query
from .util import terms, overlaps

age_terms = terms('Ma','Myr', 'm.y.', 'm.y.r','Ga','Gyr','Ka','Kyr','39Ar','40Ar')

def fix_age(val, unit):
    if val == '':
        val = None
    if val is None:
        return val
    val = float(val)
    if unit == 'ka':
        val /= 1000
    return val

def ages():
    run_query('create_ages_table')
    table = reflect_table('global_geology_age')

    res = session.query(nlp).filter(
        nlp.c.lemmas.overlap(age_terms))

    age_range = re.compile("(\d+(?:\.\d+)?)(?: ± (\d+(?:\.\d+)?))?(?: ?(-*|to|and) ?(\d+(?:\.\d+)?))? ?([Mk]a)")
    for row in res:
        sentence = Sentence(row)
        __ = age_range.findall(str(sentence))
        for match in __:
            (age, error, sep, end_age, unit) = match

            stmt = insert(table).values(
                docid=sentence.document,
                sentid=sentence.id,
                age=fix_age(age, unit),
                error=fix_age(error, unit),
                end_age=fix_age(end_age, unit))
            session.execute(stmt)
        session.commit()


