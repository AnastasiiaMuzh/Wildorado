from .db import db, environment, SCHEMA, add_prefix_for_prod

class ReviewImage(db.Model):
    __tablename__ = 'review_images'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    reviewId = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("reviews.id")), nullable=False)
    imageUrl = db.Column(db.String(255), nullable=False)  

    # Relationships
    review = db.relationship("Review", back_populates="images")

    # Debugging representation
    def __repr__(self):
        return f"<ReviewImage id={self.id}, reviewId={self.reviewId}, imageUrl='{self.imageUrl}'>"
