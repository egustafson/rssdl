"""Feed Processing
"""

from rssdl.rss import Feed


def update_feed(dom, fid):
    with dom as d:
        feed = d.get_feed(fid)
    if not feed:
        return "No such feed_id[{}]".format(fid)
    f = Feed(feed.href)
    result = f.parse()
    if result > 0:
        return "Success[{}]".format(result)
    else:
        return "Failed."



## Local Variables:
## mode: python
## End:
