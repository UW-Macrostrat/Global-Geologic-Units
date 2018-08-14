all: local_setup

.PHONY: install test_data training_data local_setup

local_setup:
	./bin/setup-app

install:
	pip install -r example_app/requirements.txt

test_data:
	curl https://geodeepdive.org/dev_subsets/example_input.zip | tar -xf - -C .

training_data:
	# Test data for volcanic ash provided by Ian Ross
	mkdir input
	cd input; curl https://geodeepdive.org/dev_subsets/volcanic_ash_intervals_overlap.zip | tar -xf - -C .

