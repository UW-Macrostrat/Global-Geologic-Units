# Julia's development version of finding stratigraphic entities for global-geologic-units app
# 
# differences from strom app:
# + lots more terms (igneous, metamorphic, etc.)
# + a few new types of entities:
#		= Large Igneous Province (is 'Large' a stop word?)
#		= ** [rock type][NNP][NNP?] (of) [NNP][NNP] (might be rare) e.g. Quartz Monzonite of Ruby Lake
#		= ends in 'Complex'
# 		= anything else?
#
# input flag_words lists:
#	= last word in every Macrostrat strat_name
# 	= every Macrostrat lithology
# 	= extra ones from Brenhin
#	= ?
#
# Input will be a file with each entity separated by a newline:
#		Limestone
#		Formation
#		etc.
#
# two(+?) methods:
#	= similar to strom (will find 'Green River Formation' or 'Big Red Schist')
#		+ find flag_words, read backwards,
#		+ keep same strom rules
#			- (will not find Quartz Monzonite, I don't think -- double flag_word rule)
#	= different to account for Brenhin's example: 'Quartz Monzonite of Ruby Lake'
#		+ is this format always/almost always the same?
#		+ algorithm:
#			- find flag
#			- read backwards through proper nouns before flag
#			- relax rules but keep:
#				1. capitalized first letter
#				2. not a number
#				3. not a stop word
#				4. any others?
#			- read forwards from flag
#			- if it's 'of':
#				look after 'of' -- proper noun(s) = keep
#			- save "...[NNP][NNP] flag 'of' [NNP][NNP]..."
#
# =============================

# import
from sqlalchemy.sql.expression import insert
from GDDTools import Sentence
#from stop_words import get_stop_words

# these are from user-defined methods
from .database import session, nlp, reflect_table, run_query
from .util import terms
from .ages import age_terms


def ext_strat_phrases():
# TABLE to put entities in
# rows: docid, sentid, strat_flag, strat_name_full, strat_mention, flag_id, mention_idx
	run_query('create_strat_phrases_table')
	table = reflect_table('strat_phrases')

# ================== #
# FLAG WORDS
# ================== #

# Trim Macrostrat strat_name_long and save the last word
# save to local list? or psql table?

# GET strat_name_long FROM Macrostrat (table: macrostrat_strat)
	strat_names = [r[0] for r in run_query('get_strat_names')]

# GET Macrostrat lithologies FROM table: macrostrat_lith
	lith_names = [r[0] for r in run_query('get_liths')]

	all_names = strat_names + lith_names

	flag_words = []	# list to fill with found flag words
# chop off all but last word in strat_names (note: don't want to do this for lith_names as some are multi-word)
	for name in strat_names:
		name = name.split(' ') # names look like 'Almirante Sur Sand Lentil' right now, want to get last word, so split
		last_name = name[-1] # get the last word in the name (should be the flag)
		last_name = last_name.capitalize() # capitalize the word. if it already is, this won't do anything (built-in function)

		if last_name not in flag_words: # only unique cases
			flag_words.append(last_name)

# do the same for lithology names		
	for name in lith_names: # some of these are multi-word flags -- how will this be handled?
		cap_name = name.capitalize()
		if cap_name not in flag_words:
			flag_words.append(cap_name)

# add manually-entered flag words
	#with open('./word_lists/manual_flags.txt') as fid:
		#manual_flags = fid.readlines()
	#for i in manual_flags:
		#exec(i) # doesn't work, is risky
	abbrevs = ["Gp.", "Fm.", "Mbr.", "SGp.", "Gp", "Fm", "Mbr", "SGp"]
	metaig_words = ["Platform", "Massif", "Batholith", "Pluton", "Stock", "Laccolith", "Diatreme", "Province", "Swarm", "Dike", "Ophiolite", "Terrane", "Orogen"]
# Now there are two other lists of flag words: abbrevs and metaig_words 
# add them to the list of flags
	for name in abbrevs:
		# (should already be capitalized, but just in case:)
		cap_name = name.capitalize()
		if cap_name not in flag_words:
			flag_words.append(cap_name)
	for name in metaig_words:
		# (should already be capitalized, but just in case:)
		cap_name = name.capitalize()
		if cap_name not in flag_words:
			flag_words.append(cap_name)

# At this point, flag_words should have: Macrostrat strat names, lith names, and manually-entered names
	# alphabetize flag words:
	flag_words = sorted(flag_words, key=str.lower)
	print(flag_words)

# ================== #
# STOP / BAD WORDS
# ================== #
# STOP WORDS (which are the most common words in english -- words usually skipped by search engines)
	#stop_words = get_stop_words('english') # these all have a u in front of them?
	#stop_words = [i.encode('ascii','ignore') for i in stop_words] # this gets rid of the u...
	#alpha = list(string.ascii_lowercase); # every letter in the alphabet, lowercase
	#alpha_period = [i+'.' for i in alpha]   # every letter + a period, lowercase
	#stop_words = stop_words + ['lower','upper','research'] + alpha + alpha_period # add three words that were problematic at one point + the letters to the list of stop words


# ================== #
# FIND FLAGS
# ================== #

# read in lines from psql sentences table: global_geology_sentences_nlp352 ('nlp' from database.py)
# cols are: sentid, wordidx, words, poses, ners, lemmas, dep_paths, dep_parents

# this is from Daven's units.py:
#	- A session is a sqlalchemy database session, connects to psql 
# 	- Session = sessionmaker() # from sqlalchemy.orm.session
#	- session = Session(bind=engine.connect()) # sqlalchemy creates an engine
#	- 'nlp' is the nlp output (sentences table)
#	- 'filter' is a class in query() (see sqlalchemy documentation: http://docs.sqlalchemy.org/en/latest/orm/query.html)
#	- '.c' is the class? column?
#	- 'words' is the column to filter by
#	- 'overlap(list x)' will look for the overlap of x and words
# Only get rows that have a flag_word in them:
	res = session.query(nlp).filter(nlp.c.words.overlap(flag_words))
# will this take forever???

# loop through the rows with flag words in them
	for row in res:
		# GDDTools Sentence converts a line in the sentences table
		sentence = Sentence(row)
		# check results if you want:
		#print(sentence)




