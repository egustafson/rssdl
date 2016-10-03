"""Feed Processing
"""

import datetime

from rssdl.rss import Feed
from rssdl.sql import Item
from rssdl.sql import Attachment


def update_feed(dom, feed_id):
    with dom as d:
        feed = d.get_feed(feed_id)
    if not feed:
        return "No such feed_id[{}]".format(feed_id)
    f = Feed(feed.href)
    result = f.parse()
    if result == 0:
        return "Failed to load RSS."
    #
    #
    d = f.data()
    with dom as dom:
        feed = dom.get_feed(feed_id)
        feed.title = d.feed.title
        feed.active = True
        feed.updated_at = datetime.datetime.now()
        #
        db_items = {}
        for item in feed.items:
            db_items[item.guid] = item
        for entry in d.entries:
            if entry.id not in db_items:
                pub_time = datetime.datetime.fromtimestamp(0)  ## epoch
                if hasattr(entry, 'published'):
                    pub_time = datetime.datetime(*entry.published_parsed[:-3])
                item = Item( title = entry.title,
                             link = entry.link,
                             guid = entry.id,
                             pub_at = pub_time,
                             updated_at = datetime.datetime.now() )
                feed.items.append( item )
                for encl in entry.enclosures:
                    att = Attachment( link = encl.href,
                                      media_type = encl['type'] )
                    item.attachments.append( att )
    return "success."

## ######################################################################

import os.path

from urlparse import urlparse

import requests


def dl_file(url, fn):
    r = requests.get(url, stream=True)
    with open(fn, 'wb') as fd:
        for chunk in r.iter_content(4096):
            fd.write(chunk)


def dl_item(dom, feed_id, item_id, dl_dir):
    assert( os.path.isdir(dl_dir) )
    with dom as d:
        item = d.get_item(feed_id, item_id)
        assert(item!=None)
        for att in item.attachments:
            if att.path == None:
                link = att.link
                url = urlparse(link)
                base = os.path.basename(url.path)
                fn = os.path.join(dl_dir, base)
                print("dl: {} -> {}".format(link, fn))
                dl_file(link, fn)
                att.path = fn
    return "stub-result."


def dl_feed(dom, feed_id, dl_dir):
    assert( os.path.isdir(dl_dir) )
    with dom as d:
        feed = d.get_feed(feed_id)
        for item in feed.items:
            for att in item.attachments:
                if att.path == None:
                    link = att.link
                    url = urlparse(link)
                    base = os.path.basename(url.path)
                    fn = os.path.join(dl_dir, base)
                    print("dl: {} -> {}".format(link, fn))
                    dl_file(link, fn)
                    att.path = fn

    return "stub-result."


## Local Variables:
## mode: python
## End:
