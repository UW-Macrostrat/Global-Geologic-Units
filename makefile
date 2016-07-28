all:
	cp credentials.yml.example credentials.yml;
	pip install -r requirements.txt;



local_setup:
	./setup/setup.sh
