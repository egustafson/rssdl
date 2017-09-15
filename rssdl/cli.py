""" CLI for RSSDL
"""

import click
import yaml

from rssdl.dom import DOM
from feed_processing import update_feed
from feed_processing import dl_feed
from feed_processing import dl_item


def load_config(filename):
    with open(filename, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg


def load_dom(ctx):
    config = ctx.obj['CONFIG']
    dbfile = config['sqlite_file']
    return DOM(dbfile)

def cfg_dl_dir(ctx):
    config = ctx.obj['CONFIG']
    return config.get('dl_dir', '/tmp')


## ############################################################

@click.group()
@click.option('--conf',
              default='rssdl.yaml',
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


@cli.command(name='list')
@click.argument('ids', nargs=-1)
@click.pass_context
def feed_list(ctx, ids):
    args = list(ids)
    feed_id = None
    item_id = None
    if len(args):
        feed_id = args.pop()
    if len(args):
        item_id = args.pop()
    if len(args):
        click.UsageError("too many options provided")
    with load_dom(ctx) as dom:
        if item_id:
            response = dom.list_item(feed_id, item_id)
        elif feed_id:
            response = dom.list_feed(feed_id)
        else:
            response = dom.list_feeds()
        for line in response:
            click.echo(line)
            #click.echo("{:3}: {}".format(feed.id, feed.href))


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
@click.argument('fid')
@click.pass_context
def dl(ctx, fid):
    dl_dir = cfg_dl_dir(ctx)
    dom = load_dom(ctx)
    msg = dl_feed(dom, fid, dl_dir)
    click.echo(msg)


@cli.command()
@click.argument('feed_id')
@click.argument('item_id')
@click.pass_context
def dl1(ctx, feed_id, item_id):
    dl_dir = cfg_dl_dir(ctx)
    dom = load_dom(ctx)
    msg = dl_item(dom, feed_id, item_id, dl_dir)
    click.echo(msg)


@cli.command()
@click.argument('fid')
@click.pass_context
def dump(ctx, fid):
    with load_dom(ctx) as dom:
        feed = dom.get_feed(fid)
        click.echo("{}".format(feed))
        for item in feed.items:
            click.echo(" {}".format(item))
            for att in item.attachments:
                click.echo("  {}".format(att))


## Local Variables:
## mode: python
## End:
