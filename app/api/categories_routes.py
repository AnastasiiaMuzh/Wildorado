from flask import Blueprint, jsonify
from app.models import db, Category, Location, LocationImage, Review

category_routes = Blueprint('categories', __name__)


#*********************** GET /api/categories ***********************#
@category_routes.route("/", methods=["GET"])
def get_categories():
    """Get list all categories"""
    try:
        categories_list = Category.query.all()

        if not categories_list:
            return jsonify({"message": "No categories found"}), 404
        
        return jsonify({"categories": [{"id": category.id, "name": category.name} for category in categories_list]})
    
    except Exception:
        return jsonify({"message": "Internal server error"}), 500



# *********************** GET /api/categories/<int:id> ***********************
@category_routes.route("/<int:id>", methods=["GET"])
def get_category(id):
    """Get all locations related to the selected category"""
    try:
        category = Category.query.get(id)
    
        if not category:
            return jsonify({"message": "Category not found"}), 404

        locations = Location.query.filter_by(categoryId=id).all()

        if not locations:
            return jsonify({"message": "No locations found in this category"}), 404

        # For each location, get the preview image and average rating
        locations_data = []
        for location in locations:
            # Get preview image
            preview_image = LocationImage.query.filter_by(locationId=location.id, preview=True).first()
            image_url = preview_image.url if preview_image else None
            
            # Get average rating
            reviews = Review.query.filter_by(locationId=location.id).all()
            avg_rating = sum(review.stars for review in reviews) / len(reviews) if reviews else 0
            review_count = len(reviews)
            if review_count > 0:
                avg_rating = sum(review.stars for review in reviews) / review_count
            else:
                avg_rating = 0
            
            locations_data.append({
                "id": location.id,
                "name": location.name,
                "city": location.city,
                "reviews": [review.text for review in reviews],
                "imageUrl": image_url,
                "avgRating": round(avg_rating, 1),
                "reviewCount": review_count
            })

        return jsonify({
            "category": {"id": category.id, "name": category.name},
            "locations": locations_data
        })
    
    except Exception:
        return jsonify({"message": "Internal server error"}), 500

