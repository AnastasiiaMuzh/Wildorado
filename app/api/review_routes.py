from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from datetime import datetime
from app.models import db, Location, Review, ReviewImage, User

review_routes = Blueprint('reviews', __name__)

# *********************** GET /api/reviews/locations/:locationId ***********************
@review_routes.route("/locations/<int:location_id>", methods=["GET"])
def get_reviews_for_location(location_id):
    """Get all reviews for a specific location, including author and images."""
    try:
        location = Location.query.get(location_id)
        if not location:
            return jsonify({"message": "Location not found."}), 404
        
        reviews = Review.query.filter_by(locationId=location_id).all()

        reviews_data = []
        for review in reviews:
            # Get images for review
            review_images = ReviewImage.query.filter_by(reviewId=review.id).all()
            images = [{"id": img.id, "url": img.imageUrl} for img in review_images]

            # Find author and Check if user exists
            user = User.query.get(review.userId)
            if not user:
                continue  

            reviews_data.append({
                "id": review.id,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "avatar": user.avatar
                },
                "stars": review.stars,
                "text": review.text,
                "images": images,
                "createdAt": review.createdAt,
                "updatedAt": review.updatedAt
            })

        return jsonify(reviews_data), 200
        
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500

# *********************** POST /api/reviews/locations/:locationId ***********************
@review_routes.route("/locations/<int:location_id>", methods=["POST"])
@login_required
def create_review(location_id):
    """Create a new review for a location (optionally with an image)."""
    try:
        location = Location.query.get(location_id)
        if not location:
            return jsonify({"message": "Location not found."}), 404
        
        data = request.get_json() or {}

        # Checking required fields
        stars = data.get("stars")
        review_text = data.get("text", "").strip()  
        image_url = data.get("imageUrl")  # It's can be None if not image

        if stars is None or not isinstance(stars, int) or stars < 1 or stars > 5:
            return jsonify({"message": "Stars must be between 1 and 5"}), 400
        
        if not review_text:
            return jsonify({"message": "Review text cannot be empty"}), 400
        
        # Check if this user has already left a review
        exist_review = Review.query.filter_by(userId=current_user.id, locationId=location.id).first()
        if exist_review:
            return jsonify({"message": "You have already reviewed this location"}), 409
        
        # Create new review
        # First create and save a review without an image,
        # because i need to get the review ID before i can attach an image to it.
        new_review = Review(
            userId=current_user.id, # Review author - current user
            locationId=location_id, # What location does the review refer to?
            stars=stars,            # Rating (1-5 stars)
            text=review_text        # The text of the review itself
        )

        db.session.add(new_review)
        db.session.commit()

        # If have image, create them
        review_image = None  # Set review_image to None because some reviews may not have an image.
        if image_url:
            review_image = ReviewImage(
                reviewId=new_review.id, # Link to the newly(newly-> только что) created review
                imageUrl=image_url      # URL image
            )
            db.session.add(review_image)
            db.session.commit()


        response = {
            "id": new_review.id,
            "userId": new_review.userId,
            "locationId": new_review.locationId,
            "stars": new_review.stars,
            "text": new_review.text,
            "createdAt": new_review.createdAt,
            "updatedAt": new_review.updatedAt,
            "user": {
                "id": current_user.id,
                "username": current_user.username
            }
        }
        
        # Add an image to JSON (if it exists)
        if review_image:
            response["image"] = {
                "id": review_image.id,
                "url": review_image.imageUrl
            }

        return jsonify(response), 201
    
    except Exception as e:
        print(e)
        db.session.rollback()  
        return jsonify({"message": "Internal server error"}), 500

# *********************** PUT /api/reviews/:reviewId ***********************
@review_routes.route("/<int:review_id>", methods=["PUT"])
@login_required
def update_review(review_id):
    """Update an existing review (text, stars, image)"""
    try: 
        review = Review.query.get(review_id)  # search for a review in the db by review_id
        if not review:
            return jsonify({"message": "Review not found."}), 404
        
        if review.userId != current_user.id:  # check if this reviews by current user
            return jsonify({"message": "Forbidden"}), 403
        
        data = request.get_json() or {} #gets JSON data from the request. or {}→ If there is no data, an empty dictionary is added to avoid errors.
        print("Updating review:", data)

        # Update text and stars
        review_text = data.get("text") #new text
        stars = data.get("stars")      #new stars
        delete_image = data.get("deleteImage", False) #if user want to delete image-> deleteImage": true

        if stars is not None:
            if not isinstance(stars, int) or stars < 1 or stars > 5:
                return jsonify({"message": "Stars must be between 1 and 5"}), 400
            review.stars = stars
            
        if review_text is not None:
            review.text = review_text.strip()
            if not review_text:
                return jsonify({"message": "Review text cannot be empty"}), 400
            review.text = review_text
        

        review_image = ReviewImage.query.filter_by(reviewId=review.id).first() #Find image link to this review
        image_url = data.get("imageUrl") #Get new URL image from request

        # If image deletion is requested
        if delete_image and review_image: #if deleteImage: true and review have image
            db.session.delete(review_image) # add to db
            review_image = None             # reset review_image so that it doesn't get into the response.

        # Otherwise, if a new image URL is provided
        elif image_url:
            if review_image: # If an image already exists, update its URL
                review_image.imageUrl = image_url
            else: # If no image exists, create a new one
                new_image = ReviewImage(reviewId=review.id, imageUrl=image_url)
                db.session.add(new_image)

        review.updatedAt = datetime.now()
        db.session.commit()

        # JSON response with updated review data.
        updated_image = ReviewImage.query.filter_by(reviewId=review.id).first()
        
        response = {
            "id": review.id,
            "userId": review.userId,
            "locationId": review.locationId,
            "stars": review.stars,
            "text": review.text,
            "createdAt": review.createdAt,
            "updatedAt": review.updatedAt,
            "user": {
                "id": current_user.id,
                "username": current_user.username
            }
        }
        
        # if image exist, add in JSON
        if updated_image:
            response["image"] = {
                "id": updated_image.id, 
                "url": updated_image.imageUrl
            }

        return jsonify(response), 200

    except Exception as e:
        print(e)
        db.session.rollback() 
        return jsonify({"message": "Internal server error"}), 500

# *********************** DELETE /api/reviews/:reviewId ***********************
@review_routes.route('/<int:review_id>', methods=["DELETE"])
@login_required
def delete_review(review_id):
    """Delete a review along with its image (if exists)."""
    try:
        review = Review.query.get(review_id)
        if not review:
            return jsonify({"message": "Review not found."}), 404

        if review.userId != current_user.id:
            return jsonify({"message": "Forbidden"}), 403

        # Delete images current user
        review_images = ReviewImage.query.filter_by(reviewId=review.id).all()
        for image in review_images:
            db.session.delete(image)

        # Delete review
        db.session.delete(review)
        db.session.commit()

        return jsonify({"message": "Review and associated images successfully deleted."}), 200
    
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "Internal server error"}), 500