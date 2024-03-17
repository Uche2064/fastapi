from .db import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key = True,autoincrement = True, index = True)
    title = Column(String(50), nullable = False)
    content = Column(String(150), nullable = False)
    published = Column(Boolean, server_default=text("true"))
    created_at = Column(TIMESTAMP (timezone = True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    user = relationship("User")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    created_at = Column(TIMESTAMP(timezone = True), server_default=text("now()"))
    phone_number = Column(String(30))
    
class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)