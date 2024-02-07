from datetime import datetime

from sqlalchemy import Boolean, DateTime, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///doroge_deshevo.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

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


Base.metadata.create_all(engine)
Base.metadata.bind = engine
