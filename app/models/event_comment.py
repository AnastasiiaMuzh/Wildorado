from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime, timezone

class EventComment(db.Model):
    __tablename__ = 'event_comments'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    eventId = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("events.id")), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")), nullable=False)
    message = db.Column(db.Text, nullable=False) 
    createdAt = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updatedAt = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

    # Relationships
    event = db.relationship("Event", back_populates="comments")
    user = db.relationship("User", back_populates="event_comments")

    # Debugging representation
    def __repr__(self):
        return f"<EventComment id={self.id}, eventId={self.eventId}, userId={self.userId}>"
