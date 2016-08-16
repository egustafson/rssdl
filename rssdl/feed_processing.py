"""Feed Processing
"""

import datetime

from rssdl.rss import Feed

from rssdl.sql import Item


def update_feed(dom, fid):
    with dom as d:
        feed = d.get_feed(fid)
    if not feed:
        return "No such feed_id[{}]".format(fid)
    f = Feed(feed.href)
    result = f.parse()
    if result == 0:
        return "Failed to load RSS."
    #
    #
    d = f.data()
    with dom as dom:
        feed = dom.get_feed(fid)
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
                #
#                 for encl in entry.enclosures:
#                     att = Attachment( link = encl.href,
#                                       media_type = encl['type'] )
#                     item.append( att )
    return "success."



## Local Variables:
## mode: python
## End:
