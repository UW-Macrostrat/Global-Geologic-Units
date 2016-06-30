# GeoDeepDive Application Template
A template and common set conventions for building applications to extract information from published and pre-processed documents in the [GeoDeepDive](https://geodeepdive.org) infrastructure. For general information about this infrastucture, see the [GeoDeepDive website](https://geodeepdive.org/about.html).

## TL;DR
1. Make a local copy of this repository
2. Edit the `config` file with your application details
3. Contact us to set up a private repository under the `UW-Deepdive-Infrastructure` group for you
4. Add the repository created in step 3 as a remote and push your changes
5. A testing subset will be created for you. We will let you know when it is ready and where to download it.
6. Replace the data in the `./input` folder with the data created in step 5
7. Write an application in a supported language (e.g., Python 2.7+)
8. When your application is ready to be run on the high throughput infrastructure against the entire corpus, commit and push your changes.
9. We will run your application at the defined interval and results will be committed to the `./output` folder
10. Return to step 7 as needed

## The Big Picture
GeoDeepDive and this app-template provide the infrastructure required to do the following:

1. Identify documents of potential interest to a project based on simple string matching
2. Generate a testing and developent dataset consisting of NLP/OCR output for a subset of these documents
3. Run an app-template-based application, written by you, against all of the potentially relevant documents 
4. Periodically re-run the application, and/or new versions of the application, to generate new results
5. Provide full citations and links to all original document sources supplying information

Currently, using this infrastructure requires communication/active collaboration with the [GeoDeepDive team](https://geodeepdive.org/people.html). 

## Getting started
Dependencies:
  + [GNU Make](https://www.gnu.org/software/make/)
  + [git](https://git-scm.com/)
  + [pip](https://pypi.python.org/pypi/pip)
  + [PostgreSQL](http://www.postgresql.org/)

Instructions for OS X are provided below, but it is not a requirement. However, development on a \*nix distribution is assumed, and the applications developed with this template will be run on Ubuntu.

### OS X
OS X ships with GNU Make, `git`, and Python, but you will need to install `pip` and PostgreSQL.

To install `pip`:
````
sudo easy_install pip
````

To install PostgreSQL, it is recommended that you use [Postgres.app](http://postgresapp.com/). Download
the most recent version, and be sure to follow [the instructions](http://postgresapp.com/documentation/cli-tools.html)
for setting up the command line tools, primarily adding the following line to your `~/.bash_profile`:

````
export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/latest/bin
````


### Setting up the project
First, download this repository and run the setup script:

````
curl -LOk https://github.com/UW-Deepdive-Infrastructure/app-template/archive/master.zip
unzip master.zip
cd app-template-master
make
````

### Data sources

#### Postgres
While Postgres is not required to run applications, it is the preferred method. These instructions assume you have Postgres 9.x installed and running on your machine.

1. Edit `credentials` with the connection credentials for your local Postgres database.

2. To create a database with the data included in `./input`, run `make local_setup`

3. To run an example application and check its output, run the following:

```
python run.py
cat output/proper_nouns_with_adjectives
```

#### Text files
You can also use TSV dumps of the data, which are in the `./input` directory. However, be advised that data should be read into your application in a memory-friendly way to ensure that your application scales.

## Inputs
The `./input` directory contains an example of the possible inputs. These include:

  * Cuneiform OCR output (cuneiform-page-000\*.html)
  * Tesseract OCR output (page-\*.hocr.html)
  * TSV dumps of sentence-level NLP processings with varying Stanford CoreNLP version and output formatting. These can be imported into Postgres and be used by a DeepDive application.
  * bibjson file containing the article's bibliographic information.

 See `./input/README` for more details on each product.

Applications should be written with the expectation that full data products
matching the desired terms will be available within the `./input`.


## Running on GeoDeepDive Infrastructure
All applications are required to have the same structure as this repository, namely an empty folder named `output`, a valid
`config` file, an updated `requirements.txt` describing any Python dependencies, and `run.py` which runs the application
and outputs results. The `credentials` file will be ignored and substituted with a unique version at run time. The `input`
directory will similarly be substituted with the complete set of desired products matching the terms (or dictionary) specified.

The GeoDeepDive infrastructure will have the following software available:
  + Python 2.7+ (Python 3.x not supported at this time)
  + PostgreSQL 9.4+, including command line tools and PostGIS

#### Submitting a config file
The `config` file outlines a list of terms OR dictionaries that you are interested in culling from the corpus. Once you have
updated this file, a private repository will be set up for you under the UW-DeepDive-Infrastructure Github group for you to
push the code from this repository to. Your `config` file will be used to generate a custom testing subset of documents that
you can use to develop your application.

#### Running the application
Once you have developed your application and tested it against the corpus subset, simply push your application to the
private repository created in the previous step. The application will then be run according to the parameters set in the
`config` file.

#### Getting results
After the application is run, the contents of the `output` folder will be gzipped and be made available to download. If
an error was encountered or your application did not run successfully any errors thrown will be logged into the file
`errors.txt` which is included in the gzipped results package.

## File Summary

#### config
A YAML file that contains project settings.


#### credentials
A YAML file that contains local postgres credentials for testing and generating examples.


#### requirements.txt
List of Python dependencies to be installed by `pip`


#### run.py
Python script that runs the entire application, including any setup tasks and exporting of results to the folder `./output`.

## Common Pitfalls
### postgres_cursor.fetchall()
Reading data into/out of postgres tables is supported (and to an extent expected),
but trying to read ALL results of a query into memory in one pass can be a very bad idea.
It may work for the test dataset you have, but these are typically on the order of a few
hundred documents. The full data set may be many orders of magnitude larger, and your application
may run into memory issues if not handled properly. Instead, loop over the cursor row-by-row (i.e. 
sentence-by-sentence).

## License
CC-BY 4.0 International
