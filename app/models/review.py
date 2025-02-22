from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime, timezone

class Review(db.Model):
    __tablename__ = 'reviews'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")), nullable=False)
    locationId = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("locations.id")), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updatedAt = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)


    # Relationships
    user = db.relationship("User", back_populates="reviews")
    location = db.relationship("Location", back_populates="reviews")
    images = db.relationship("ReviewImage", back_populates="review", cascade="all, delete-orphan")


    # Debugging representation
    def __repr__(self):
        return f"<Review id={self.id}, userId={self.userId}, locationId={self.locationId}, stars={self.stars}>"
