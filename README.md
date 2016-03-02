# GeoDeepDive Application Template


## Getting started
Dependencies:
  + [GNU Make](https://www.gnu.org/software/make/)
  + [git](https://git-scm.com/)
  + [pip](https://pypi.python.org/pypi/pip)
  + [PostgreSQL](http://www.postgresql.org/)

````
git clone https://github.com/UW-DeepDiveInfrastructure/app-template
cd app-template
make
````

Edit `credentials` with the connection credentials for your local Postgres database.

To create a database with the data included in `/setup/usgs_example`:

````
make local_setup
````

## Files

#### config
A YAML file that contains project settings.


#### credentials
A YAML file that contains local postgres credentials for testing and generating examples.


#### requirements.txt
List of Python dependencies to be installed by `pip`


#### run.py
Python script that runs the entire application, including any setup tasks and exporting of results to the folder `/output`.
