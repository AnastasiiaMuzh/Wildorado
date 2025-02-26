from flask import Blueprint, jsonify
from app.models import db, Category, Location

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

        return jsonify({"locations": [
            {
                "id": location.id,
                "name": location.name,
                "city": location.city,
                "description": location.description,
                "elevation": location.elevation
            }
            for location in locations
        ]})
    
    except Exception:
        return jsonify({"message": "Internal server error"}), 500

