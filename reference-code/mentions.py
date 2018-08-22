ignimbrite_terms = terms('ignimbrite','tuff')

@cli.command()
def mentions():
    """Writes a table indexing sentences mentioning ignimbrites"""
    # Filter by lemmas using the PostgreSQL engine directly
    # This is much quicker than filtering in Python.
    # In general, all logic that can be pushed to SQL should be...

    run_query('create_mention_table')
    table = reflect_table('global_geology_mention')

    res = session.query(nlp).filter(
        nlp.c.lemmas.overlap(ignimbrite_terms))

    for row in res:
        sentence = Sentence(row)
        print(sentence.document, sentence.id)
        ignimbrite_words = (w for w in sentence if w.lemma in ignimbrite_terms)
        for word in ignimbrite_words:
            refs = [w for w
                    in sentence.words_referencing(word)
                    if w.is_adjective or w.is_adverb or w.is_verb]

            print(word, " ".join(str(s) for s in refs))
            print()
            stmt = insert(table).values(
                docid=sentence.document,
                sentid=sentence.id,
                wordidx=word.index,
                word=str(word),
                refs=[str(w) for w in refs],
                ref_poses=[w.pose for w in refs]
            )
            session.execute(stmt)
        session.commit()
