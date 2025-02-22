from .db import db, environment, SCHEMA, add_prefix_for_prod

class EventParticipant(db.Model):
    __tablename__ = 'event_participants'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    eventId = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("events.id")), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")), nullable=False)

    # Relationships
    event = db.relationship("Event", back_populates="participants")
    user = db.relationship("User", back_populates="event_participants")

    # Debugging representation
    def __repr__(self):
        return f"<EventParticipant id={self.id}, eventId={self.eventId}, userId={self.userId}>"
