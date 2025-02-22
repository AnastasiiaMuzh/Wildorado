from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timezone
# from sqlalchemy.schema import UniqueConstraint
# from sqlalchemy import Enum



class User(db.Model, UserMixin):
    __tablename__ = 'users'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255))
    bio = db.Column(db.Text)
    interests = db.Column(db.String(255))
    createdAt = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updatedAt = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

    # Relationships
    locations = db.relationship("Location", back_populates="user", cascade="all, delete-orphan")
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete-orphan")
    events = db.relationship("Event", back_populates="user", cascade="all, delete-orphan")
    event_participants = db.relationship("EventParticipant", back_populates="user", cascade="all, delete-orphan")
    event_comments = db.relationship("EventComment", back_populates="user", cascade="all, delete-orphan")
    friendships1 = db.relationship("Friendship", foreign_keys="[Friendship.userId1]", back_populates="friend1")
    friendships2 = db.relationship("Friendship", foreign_keys="[Friendship.userId2]", back_populates="friend2")

    # For password hashing
    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'avatar': self.avatar,
            'bio': self.bio,
            'interests': self.interests
        }