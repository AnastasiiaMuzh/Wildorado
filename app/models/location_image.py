from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime, timezone

class LocationImage(db.Model):
    __tablename__ = 'location_images'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    locationId = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("locations.id")), nullable=False)
    url = db.Column(db.Text, nullable=False)
    preview = db.Column(db.Boolean, default=False, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updatedAt = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)

    # Relationship
    location = db.relationship("Location", back_populates="images")

    def __repr__(self):
        return f"<LocationImage id={self.id}, locationId={self.locationId}, url='{self.url}', preview={self.preview}, createdAt={self.createdAt}, updatedAt={self.updatedAt}>"
