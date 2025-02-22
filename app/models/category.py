from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime, timezone


class Category(db.Model):
    __tablename__ = 'categories'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True) 

    # relationships below
    locations = db.relationship("Location", back_populates="category", cascade="all, delete-orphan")

    # Debugging representation
    def __repr__(self):
        return f"<Category id={self.id}, name='{self.name}'>"