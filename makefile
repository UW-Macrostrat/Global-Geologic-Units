all: local_setup

.PHONY: install data local_setup

local_setup: data
	./setup/setup.sh

install:
	pip install -r example_app/requirements.txt

data:
	curl https://geodeepdive.org/dev_subsets/example_input.zip | tar -xf - -C .


