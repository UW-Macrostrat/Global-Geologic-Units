import yaml
from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.engine.url import URL
from click import secho
from os.path import join, dirname

__here__ = dirname(__file__)

def open_relative(fn, mode='r'):
    fn = join(__here__, fn)
    return open(fn, mode)

with open_relative('../credentials.yml') as credential_yaml:
    credentials = yaml.load(credential_yaml)

with open_relative('../config.yml') as config_yaml:
    config = yaml.load(config_yaml)

conn_string = URL(
    drivername='postgres',
    **credentials['postgres'])

Session = sessionmaker()
engine = create_engine(conn_string)
conn = engine.connect()
meta=MetaData(bind=conn)
session = Session(bind=conn)

def reflect_table(name):
    "Use SQLAlchemy to reflect the database table schema"
    return Table(name, meta, autoload=True)

# read all sentences from our NLP example database.
__tablename = config['app_name']+'_sentences_nlp352'
nlp = reflect_table(__tablename)

def run_query(sqlfile, **kw):
    if not sqlfile.endswith('.sql'):
        # We have a query identifier rather than a path
        # Queries are stored in the `sql` subdirectory
        sqlfile = join(__here__,'sql',sqlfile+'.sql')
    with open(sqlfile) as f:
        sql = f.read()
    secho(sql,fg='cyan')
    return conn.execute(text(sql), **kw)
