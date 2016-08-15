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

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type == None:
            self.commit()
        else:
            self.rollback()



class DOM(object):

    def __init__(self, dbfile):
        dburl = "sqlite:///{}".format(dbfile)
        self._engine = create_engine(dburl)
        self._session_factory = sessionmaker( class_=SessionGuard,
                                              bind=self._engine )
        self._session = None

    def __enter__(self):
        self._session = self._session_factory()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self._session.rollback()
        else:
            self._session.commit()

    def commit():
        self._session.commit()

    def rollback():
        self._session.rollback()

    ## ##########

    def create_db(self):
        Base.metadata.create_all(self._engine)

    def get_feed(self, fid):
        return self._session.query(Feed).filter_by(id=fid).one_or_none()

    def add_feed(self, href):
        now = datetime.datetime.now()
        feed = Feed( title="", href=href, active=False,
                     added_at=now, updated_at=now )
        self._session.add(feed)

    def rm_feed(self, fid):
        s = self._session
        feed = s.query(Feed).filter_by(id=fid).one_or_none()
        if feed:
            s.delete(feed)

    def list_feeds(self):
        fl = self._session.query(Feed).all()
        return fl


## Local Variables:
## mode: python
## End:
