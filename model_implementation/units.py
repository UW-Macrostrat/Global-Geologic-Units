from sqlalchemy.sql.expression import insert
from GDDTools import Sentence

from .database import session, nlp, reflect_table, run_query
from .util import terms
from .ages import age_terms

unit_types = terms('Member','Formation','Group','Supergroup','Tuff','Volcanic')

def units():
    """Writes a table containing geologic unit mentions"""

    # Instead of creating table in raw SQL and then reflecting,
    # we could define it's schema directly in the SQLAlchemy ORM.
    run_query('create_unit_table')
    table = reflect_table('global_geology_unit')

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
