from app.models import db, Location, LocationImage, Review, ReviewImage, User

# ========================== Helper Functions ==========================
def get_location_images(location_id):
    """
    Retrieves all images associated with a specific location ID.
    Returns a list of dictionaries containing image `id`, `url`, and `preview` status.
    """
    images = LocationImage.query.filter_by(locationId=location_id).all()
    return [{"id": img.id, "url": img.url, "preview": img.preview} for img in images]

def get_review_images(review_id):
    """
    Retrieves all images attached to a particular review ID.
    Returns a list of dictionaries with `id` and `imageUrl`.
    """
    images = ReviewImage.query.filter_by(reviewId=review_id).all()
    return [{"id": img.id, "url": img.imageUrl} for img in images]

def get_reviews_for_location(location_id):
    """
    Retrieves all reviews for a given location, including the reviewer's info
    (username, avatar) and any images attached to the review.
    """
    reviews_query = Review.query.filter_by(locationId=location_id).all()
    reviews = []
    
    for review in reviews_query:
        user = User.query.get(review.userId)
        review_images = get_review_images(review.id)
        
        reviews.append({
            "id": review.id,
            "stars": review.stars,
            "review": review.text,
            "createdAt": review.createdAt,
            "user": {
                "id": user.id,
                "username": user.username,
                "avatar": user.avatar
            },
            "images": review_images
        })
    
    return reviews

def calculate_average_rating(reviews):
    """
    Calculates the average star rating from a list of review objects
    which each contain 'stars'. If no reviews exist, returns 0.
    """
    if not reviews:
        return 0
    return sum(review["stars"] for review in reviews) / len(reviews)

def apply_category_filters(query, category, filters):
    """
    Applies category-specific filters to the SQLAlchemy query object.
    'filters' is a dictionary of possible filter values such as difficulty, riverClass, etc.
    Based on the category, we add the relevant filters to 'query'.
    """
    if category == 1:  # Hiking
        if filters.get("difficulty"):
            query = query.filter(Location.difficulty == filters["difficulty"])
        if filters.get("bestSeason"):
            query = query.filter(Location.bestSeason.ilike(f"%{filters['bestSeason']}%"))
    
    elif category == 2:  # Rafting
        if filters.get("river_class"):
            query = query.filter(Location.river_class == filters["river_class"])
    
    elif category == 3:  # Camping
        if filters.get("maxTents"):
            query = query.filter(Location.maxTents == filters["maxTents"])
        if filters.get("fireAllowed") is not None:
            query = query.filter(Location.fireAllowed == filters["fireAllowed"])
        if filters.get("lake") is not None:
            query = query.filter(Location.lake == filters["lake"])
    
    elif category == 4:  # Climbing
        if filters.get("difficulty"):
            query = query.filter(Location.difficulty == filters["difficulty"])
        if filters.get("routeType"):
            query = query.filter(Location.routeType == filters["routeType"])
    
    elif category == 5:  # Snow Sports
        if filters.get("bestSeason"):
            query = query.filter(Location.bestSeason.ilike(f"%{filters['bestSeason']}%"))
    
    elif category == 6:  # ATV/Bikes
        if filters.get("terrainType"):
            query = query.filter(Location.terrainType == filters["terrainType"])
    
    return query