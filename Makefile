all: training_data

.PHONY: training_data

training_data:
	# Test data for volcanic ash provided by Ian Ross
	cd input; curl http://geodeepdive.org/dev_subsets/interval_location_signals_partial_sample.zip | tar -xf - -C .

