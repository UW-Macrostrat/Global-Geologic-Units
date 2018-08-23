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
