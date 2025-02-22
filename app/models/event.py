from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime, timezone

class Event(db.Model):
    __tablename__ = 'events'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    locationId = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("locations.id")), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")), nullable=False)
    title = db.Column(db.String(255), nullable=False) 
    description = db.Column(db.Text, nullable=False) 
    date = db.Column(db.DateTime, nullable=False) 
    maxParticipants = db.Column(db.Integer, nullable=True)  
    createdAt = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updatedAt = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

    # Relationships
    location = db.relationship("Location", back_populates="events")
    user = db.relationship("User", back_populates="events")
    participants = db.relationship("EventParticipant", back_populates="event", cascade="all, delete-orphan")
    comments = db.relationship("EventComment", back_populates="event", cascade="all, delete-orphan")

    # Debugging representation
    def __repr__(self):
        return f"<Event id={self.id}, title='{self.title}', locationId={self.locationId}, userId={self.userId}>"
