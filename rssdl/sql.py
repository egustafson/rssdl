""" SQL Alchemy DOM
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

feed_str = "<Feed(id={}, title='{}', href='{}', active={}, added_at={}, updated_at={})>"
item_str = "<Item(id={}, title='{}', link='{}', guid='{}', pub_at={}, updated_at={})>"

Base = declarative_base()

class Feed(Base):
    __tablename__ = 'feeds'
    #
    id = Column(Integer, primary_key=True)
    title = Column(String)
    href = Column(String)
    active = Column(Boolean)
    added_at = Column(DateTime)
    updated_at = Column(DateTime)
    items = relationship("Item", back_populates="feed")

    def __repr__(self):
        return feed_str.format(self.id, self.title, self.href, self.active,
                               self.added_at, self.updated_at)


class Item(Base):
    __tablename__ = 'items'
    #
    id = Column(Integer, primary_key=True)
    title = Column(String)
    link = Column(String)
    guid = Column(String)
    pub_at = Column(DateTime)
    updated_at = Column(DateTime)
    feed_id = Column(Integer, ForeignKey('feeds.id'))
    feed = relationship("Feed", back_populates="items")

    def __repr__(self):
        return item_str.format(self.id, self.title, self.link, self.guid,
                               self.pub_at, self.updated_at)


class Attachment(Base):
    __tablename__ = 'attachments'
    #
    id = Column(Integer, primary_key=True)
    media_type = Column(String)
    link = Column(String)


## Local Variables:
## mode: python
## End:
