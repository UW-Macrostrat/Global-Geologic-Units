all: local_setup

.PHONY: training_data

training_data:
	# Test data for volcanic ash provided by Ian Ross
	mkdir input
	cd input; curl http://geodeepdive.org/dev_subsets/interval_location_signals_partial_sample.zip | tar -xf - -C .

