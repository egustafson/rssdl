""" CLI for RSSDL
"""

import click
import yaml

from rssdl.dom import DOM
from feed_processing import update_feed


def load_config(filename):
    with open(filename, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg


def load_dom(ctx):
    config = ctx.obj['CONFIG']
    dbfile = config['sqlite_file']
    return DOM(dbfile)


## ############################################################

@click.group()
@click.option('--conf',
              default='rssdl.yml',
              type=click.Path(exists=True, dir_okay=False))
@click.pass_context
def cli(ctx, conf):
    ctx.obj = {}
    ctx.obj['CONFIG'] = load_config(conf)


@cli.command()
@click.pass_context
def init(ctx):
    dom = load_dom(ctx)
    dom.create_db()


@cli.command()
@click.pass_context
def list(ctx):
    with load_dom(ctx) as dom:
        fl = dom.list_feeds()
    for feed in fl:
        click.echo("{:3}: {}".format(feed.id, feed.href))


@cli.command()
@click.argument('href')
@click.pass_context
def add(ctx, href):
    with load_dom(ctx) as dom:
        dom.add_feed(href)


@cli.command()
@click.argument('fid')
@click.pass_context
def rm(ctx, fid):
    with load_dom(ctx) as dom:
        dom.rm_feed(fid)


@cli.command()
@click.argument('fid')
@click.pass_context
def update(ctx, fid):
    dom = load_dom(ctx)
    msg = update_feed(dom, fid)
    click.echo(msg)


@cli.command()
@click.pass_context
def dl(ctx):
    click.echo('stub - done.')



@cli.command()
@click.argument('fid')
@click.pass_context
def dump(ctx, fid):
    with load_dom(ctx) as dom:
        feed = dom.get_feed(fid)
        click.echo("{}".format(feed))
        for item in feed.items:
            click.echo("{}".format(item))


## Local Variables:
## mode: python
## End:
