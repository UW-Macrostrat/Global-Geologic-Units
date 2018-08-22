# ===================================== 
#
# get_strat_names.py
# 
# JULIA WILCOTS
# 08/21/18
# 
# assemble a list of geologic unit flag words ('Formation', 'Limestone') from Macrostrat.
# Will use this list as flags in future global-geologic-units app.
# ======================================

import urllib2, csv, sys

# function from stromatolites app. probably a different (faster?) sol'n out there, but this
# works for now.
def download_csv( url ):

    #return variable
    dump_dict = {}

    #get strat_names from Macrostrat API
    dump = urllib2.urlopen( url )
    dump = csv.reader(dump)

    #unpack downloaded CSV as list of tuples
    #--> length of VARIABLE == number of fields
    #--> length of VARIABLE[i] == number of rows
    #--> VARIABLE[i][0] = header name
    cols = list(zip(*dump))

    #key names correspond to field names (headers in the CSV file)
    for field in cols:
        dump_dict[field[0]]=field[1:]

    dump_dict['headers'] = sorted(dump_dict.keys())

    return dump_dict



# import unit names from macrostrat
#strat_dict = download_csv( 'https://macrostrat.org/api/defs/strat_names?all&format=csv' )
# test w/ fewer lines: 
strat_dict = download_csv( 'https://macrostrat.org/api/defs/strat_names?ref_id=1&format=csv' )
strat_names = strat_dict['strat_name_long'] # we want things like 'Formation' and 'Granite'

# add in macrostrat lithologies
lith_dict = download_csv( 'https://dev.macrostrat.org/api/defs/lithologies?all&format=csv' )
lith_names = lith_dict['name']

#print len(lith_names)  # 184
#print len(strat_names) # 9297

all_names = strat_names + lith_names


flag_words = []	# list to fill with found flag words
for name in all_names:
	name = name.split(' ') # names look like 'Almirante Sur Sand Lentil' right now, want to get last word, so split
	last_name = name[-1] # get the last word in the name (should be the flag)
	last_name = last_name.capitalize() # capitalize the word. if it already is, this won't do anything (built-in function)

	if last_name not in flag_words: # only unique cases
		#if last_name == 'Lentil': # lol what is this?
			#print name # ['Almirante', 'Sur', 'Sand', 'Lentil']
		flag_words.append(last_name)

# HOW TO DEAL WITH CAPITAL LETTERS?

#print len(flag_words) # 191 total
# alphabetize:
alpha_flags = sorted(flag_words, key=str.lower)
for flag in alpha_flags:
	sys.stdout.write(flag + '\n')

#print alpha_flags
# check
#print all_names[50:75]
# print flag_words[16]
#print alpha_flags[1]

