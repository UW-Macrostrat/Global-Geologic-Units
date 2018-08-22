"""
File: __main__.py
Description: Example app utilizing the GeoDeepDive infrastructure and products
    to find geologic unit mentions in the literature.
"""
import click
from urllib.request import urlretrieve
from tempfile import NamedTemporaryFile
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.sql.expression import insert
from os import makedirs
from os.path import join, dirname, abspath, exists
from json import load
from subprocess import run

from .database import session, nlp, reflect_table, run_query, credentials
from .location import locations
from .units import units
from .ages import ages
from .util import terms, overlaps

__here__ = dirname(__file__)

@click.group()
def cli():
    pass

cli.command(name='locations')(locations)
cli.command(name='units')(units)
cli.command(name='ages')(ages)

@cli.command(name='setup')
def setup():
    """Set up required database extensions and tables"""
    try:
        run_query('setup_database')
    except ProgrammingError:
        click.echo("Extension already exists")

@cli.command(name='load-test-data')
@click.argument('filename', required=False, type=click.File())
def load_test_data(filename=None):
    """Set up required database extensions and tables"""
    if filename is None:
        filename = abspath(join(__here__, '..', 'input', 'sentences_nlp352'))
    run_query('load_test_data', filename=filename)

@cli.command(name='dump-database')
def dump_database():
    """Set up required database extensions and tables"""
    pg = credentials['postgres']
    cmd = ('pg_dump','-Fc','--exclude-table=global_geology_sentences_nlp352',
           '-h', pg['host'], '-p', str(pg['port']), '-U', pg['username'], '-d', pg['database'])
    run(cmd)

@cli.command(name='join-datasets')
def join_datasets():
    """
    Join unit names and coordinates tables
    """
    run_query('create_join_view')

@cli.command(name='import-papers')
def import_papers():
    """
    Import papers from bibjson file
    """
    with open(join(__here__,'..','input','bibjson')) as f:
        data = load(f)

    run_query('create_papers_table')
    table = reflect_table('global_geology_paper')

    for i in data:
        i['docid'] = i.pop('_gddid')

        __ = insert(table).values(**i)
        session.execute(__)
    session.commit()

@cli.command(name='load-macrostrat')
def load_macrostrat():
    "Load macrostrat data into database"
    with NamedTemporaryFile(delete=True) as f:
        urlretrieve("https://macrostrat.org/api/defs/intervals?all&format=csv", f.name)
        run_query("create_periods_table", filename=f.name)

if __name__ == '__main__':
    cli()
