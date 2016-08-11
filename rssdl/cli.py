""" CLI for RSSDL
"""

import click
import yaml

from rssdl.dom import DOM
from rssdl.rss import Feed


def load_config(conffile):
    filename = 'rssdl.yml'
    with open(filename, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg


@click.group()
@click.option('--conf',
              type=click.Path(exists=True, dir_okay=False))
@click.pass_context
def cli(ctx, conf):
    ctx.obj = {}
    ctx.obj['CONFIG'] = load_config(conf)


@cli.command()
@click.pass_context
def daemon(ctx):
    click.echo('stub daemon - exiting.')


@cli.command()
@click.pass_context
def dl(ctx):
    click.echo('stub - done.')


@cli.command()
@click.pass_context
def dbcreate(ctx):
    config = ctx.obj['CONFIG']
    dbfile = config['sqlite_file']
    dom = DOM(dbfile)
    dom.create_db()


@cli.command()
@click.argument('href')
@click.pass_context
def add(ctx, href):
    config = ctx.obj['CONFIG']
    dbfile = config['sqlite_file']
    dom = DOM(dbfile)
    dom.add_feed(href)


@cli.command()
@click.argument('href')
@click.pass_context
def testfeed(ctx, href):
    f = Feed(href)
    result = f.parse()
    if result > 0:
        print("Success[{}]".format(result))
    else:
        print("Failed.")


@cli.command()
@click.argument('fid')
@click.pass_context
def rmfeed(ctx, fid):
    config = ctx.obj['CONFIG']
    dbfile = config['sqlite_file']
    dom = DOM(dbfile)
    dom.rm_feed(fid)


@cli.command()
@click.pass_context
def listfeeds(ctx):
    config = ctx.obj['CONFIG']
    dbfile = config['sqlite_file']
    dom = DOM(dbfile)
    fl = dom.list_feeds()
    for feed in fl:
        print("{:3}: {}".format(feed.id, feed.href))



## Local Variables:
## mode: python
## End:
