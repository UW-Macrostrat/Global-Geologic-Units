all: local_setup

.PHONY: install test_data training_data local_setup

local_setup:
	./bin/setup-app

install:
	pip install -r example_app/requirements.txt

training_data:
	# Test data for volcanic ash provided by Ian Ross
	mkdir input
	cd input; curl http://geodeepdive.org/dev_subsets/interval_location_signals_partial_sample.zip | tar -xf - -C .

