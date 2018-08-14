all: local_setup

.PHONY: install data local_setup

local_setup: data
	./setup/setup.sh

install:
	pip install -r example_app/requirements.txt

test_data:
	curl https://geodeepdive.org/dev_subsets/example_input.zip | tar -xf - -C .

test_data2:
	# Test data for volcanic ash provided by Ian Ross
	curl https://geodeepdive.org/dev_subsets/volcanic_ash_intervals_overlap.zip | tar -xf - -C input

