# from datetime import datetime

# from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Enum, Integer, func, Float, Table
# from sqlalchemy.orm import declarative_base, relationship, Mapped

# Base = declarative_base()



# class User(Base):
#     __tablename__ = "users"

#     user_id = Column('user_id', Integer, primary_key=True)
#     full_name = Column(String)
#     banned = Column(Boolean, default=False)
#     created_at = Column(DateTime, default=datetime.now)
    


# class Post(Base):
#     __tablename__ = 'posts'

#     post_id = Column('post_id', Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.user_id'))
#     text = Column(String, nullable=False)
#     photo = Column(list(Integer))
#     city = Column(String, nullable=False)
#     created_at = Column(DateTime, default=datetime.now)
#     updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


# class Rotation(Base):
#     __tablename__ = 'rotations'

#     rotation_id = Column('rotation_id', Integer, primary_key=True)
#     post_id = Column(Integer, ForeignKey('posts.post_id'))
#     start_date = Column(DateTime, default=datetime.now)
#     finish_date = Column(DateTime)
#     period = Column('period', Integer, default=60)
#     group = Column(String, nullable=False)  # Список груп


# class PinkPost(Base):
#     __tablename__ = 'pink_posts'

#     pink_posts_id = Column('pink_posts_id', Integer, primary_key=True)
#     post_id = Column(Integer, ForeignKey('posts.post_id'))
#     start_date = Column(DateTime, default=datetime.now)
#     finish_date = Column(DateTime)
#     group = Column(String, nullable=False)  # Список груп
