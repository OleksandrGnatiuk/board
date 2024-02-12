import os
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Enum, Integer, func, Float, Table
from sqlalchemy.orm import declarative_base, relationship, Mapped


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_id = Column('user_id', Integer, primary_key=True)
    full_name = Column(String)
    banned = Column(Boolean, default=False)
    num_paid_post = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    posts = relationship('Post', back_populates='user')

    def __str__(self):
        return self.full_name


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    post_id = Column('post_id', Integer)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    text = Column(String, nullable=True)
    caption = Column(String, nullable=True)
    city = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    user = relationship('User', back_populates='posts')

