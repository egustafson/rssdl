""" RSS DOM for RSSDL
"""

import feedparser

class Feed(object):

    def __init__(self, href):
        self._href = href
        self._d = None

    def result(self):
        return self._d

    def parse(self):
        self._d = feedparser.parse(self._href)
        return self._d.status if 'status' in self._d else 0



## Local Variables:
## mode: python
## End:
