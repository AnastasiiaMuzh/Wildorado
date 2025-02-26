from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime, timezone

class Location(db.Model):
    __tablename__ = 'locations'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    categoryId = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("categories.id")), nullable=False)
    ownerId = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")), nullable=False)  
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    elevation = db.Column(db.Float)
    difficulty = db.Column(db.Enum('Easy', 'Medium', 'Hard', name="difficulty_enum"), nullable=True)
    distance = db.Column(db.Float)
    river_class = db.Column(db.Enum('I', 'II', 'III', 'IV', 'V', name="river_class_enum"), nullable=True)
    lake = db.Column(db.Boolean, default=False)
    fireAllowed = db.Column(db.Boolean, default=False)
    maxTents = db.Column(db.Integer)
    routeType = db.Column(db.Enum('Trad', 'Sport', name="routeType_enum"), nullable=True)
    bestSeason = db.Column(db.String(100))
    terrainType = db.Column(db.Enum('Dirt', 'Rocky', 'Forest', 'Mixed', name="terrain_type_enum"), nullable=True)
    createdAt = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updatedAt = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False) 

    # Relationships
    category = db.relationship("Category", back_populates="locations")
    user = db.relationship("User", back_populates="locations")
    reviews = db.relationship("Review", back_populates="location", cascade="all, delete-orphan")
    events = db.relationship("Event", back_populates="location", cascade="all, delete-orphan")
    images = db.relationship("LocationImage", back_populates="location", cascade="all, delete-orphan")


    # Debugging representation
    def __repr__(self):
        return f"<Location id={self.id}, name='{self.name}', categoryId={self.categoryId}>"
