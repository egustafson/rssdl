""" DB DOM for RSSDL
"""

import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from rssdl.sql import Base, Feed



class SessionGuard(Session):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.commit()



class DOM(object):

    def __init__(self, dbfile):
        dburl = "sqlite:///{}".format(dbfile)
        self._engine = create_engine(dburl)
        self._session_factory = sessionmaker( class_=SessionGuard,
                                              bind=self._engine )

    def session(self):
        return self._session_factory()

    def create_db(self):
        Base.metadata.create_all(self._engine)
    
    def add_feed(self, href):
        now = datetime.datetime.now()
        feed = Feed( title="", href=href, active=False,
                     added_at=now, updated_at=now )
        with self.session() as s:
            s.add(feed)

    def list_feeds(self):
        with self.session() as s:
            fl = s.query(Feed).all()
            return fl


## Local Variables:
## mode: python
## End:
