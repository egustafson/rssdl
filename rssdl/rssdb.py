""" DB DOM for RSSDL
"""

import click
import os.path
import sqlite3
import sys


class RssDOM(object):

    def __init__(self):
        self.conn = None

    def connect(self, db_file):
        self.close()
        self.conn = sqlite3.connect(db_file)

    def close(self):
        if self.conn:
            self.conn.close()

    def initialize_schema(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS feeds
                     (id integer, url text, active integer, time_update text, time_added text)''')
        self.conn.commit()
        


## ----- CLI 'main' -----
##
@click.command()
@click.option('-f', '--force', default=False, is_flag=True)
@click.argument('db', type=click.Path())
def cli(force, db):
    exists = os.path.exists(db)
    if exists and not force:
        click.echo("db file [{}] exists.  Please use '--force' to overwrite.".format(db))
        sys.exit(1)
        
    dom = RssDOM()
    dom.connect(db)
    dom.initialize_schema()
    dom.close()
    click.echo("DB [{}] initialized.".format(db))

