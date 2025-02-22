from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime, timezone
from sqlalchemy.schema import UniqueConstraint

class Friendship(db.Model):
    __tablename__ = 'friendships'

    if environment == "production":
        __table_args__ = (
            {'schema': SCHEMA},
            UniqueConstraint('userId1', 'userId2', name='unique_friendship')
        )

    id = db.Column(db.Integer, primary_key=True)
    userId1 = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")), nullable=False)
    userId2 = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")), nullable=False)
    status = db.Column(db.Enum('pending', 'accepted', 'blocked', name="friendship_status_enum"), nullable=False, default='pending')

    # Relationships
    friend1 = db.relationship("User", foreign_keys=[userId1], back_populates="friendships1")
    friend2 = db.relationship("User", foreign_keys=[userId2], back_populates="friendships2")

    def __repr__(self):
        return f"<Friendship id={self.id}, userId1={self.userId1}, userId2={self.userId2}, status={self.status}>"
