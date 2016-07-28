# GeoDeepDive Application Template
A template and common set conventions for building applications to extract information from published and pre-processed documents in the [GeoDeepDive](https://geodeepdive.org) infrastructure. For general information about this infrastucture, see the [GeoDeepDive website](https://geodeepdive.org/about.html).

## TL;DR
1. Fork this repository to your account (click the "Fork" button in the upper right corner)
2. Edit `config.yml` with your application's details
3. Download the example data
4. When you are ready for a testing subset send us an email
5. Download the testing subset
6. Write your application
7. When you are confident that your application is ready to be run our infrastructure against the corpus, notify us
8. We will pull your application on to our infrastructure and run it


1. Make a local copy of this repository
2. Edit the `config` file with your application details
3. Contact us to set up a private repository under the `UW-Deepdive-Infrastructure` group for you
4. Add the repository created in step 3 as a remote and push your changes
5. A testing subset will be created for you. We will let you know when it is ready and where to download it.
6. Replace the data in the `./input` folder with the data created in step 5
7. Write your application
8. When you are confident that your application is ready to be run on the high throughput infrastructure against the corpus, commit and push your changes.
9. We will then run your application at the defined interval and results will be committed to the `./output` folder
10. Return to step 7 as needed


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
First, download and extract the example input data:

````
curl -o example_input.zip https://geodeepdive.org/dev_subsets/example_input.zip
unzip -j example_input.zip -d ./input
rm example_input.zip
````

The `./input` directory now contains an example of the possible inputs. These include:

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

#### config.yml
A YAML file that contains project settings.


#### credentials.yml
A YAML file that contains local postgres credentials for testing and generating examples.

#### run
A bash file that contains instructions for which script(s) or processes to run. The entry point to your application.

## License
CC-BY 4.0 International
