from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from sqlalchemy import or_
from datetime import datetime, timezone
from app.models import db, Location, LocationImage, Review, ReviewImage, User, Category
from app.api.utils import apply_category_filters, get_location_images, calculate_average_rating, get_reviews_for_location
from sqlalchemy import func

location_routes = Blueprint('locations', __name__)

# ************************ GET /api/locations ************************
@location_routes.route("/", methods=["GET"])
def get_locations():
    """
    Retrieves a paginated list of locations. Allows:
      - Searching by 'name' or 'city' (via 'search' query param).
      - Filtering by 'category' plus category-specific fields 
        (e.g. difficulty for Hiking, riverClass for Rafting, etc.).
      - 'elevation' and 'distance' can also be filtered by partial matching.
    """
    try:
        # Pagination params
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("perPage", 12, type=int)

        # Search and filter params
        search_query = request.args.get("search", "", type=str).strip().lower()
        category_name = request.args.get("category", None, type=str)
        elevation = request.args.get("elevation", None, type=str)
        distance = request.args.get("distance", None, type=str)

        # Category-specific filters
        filters = {
            "difficulty": request.args.get("difficulty", None, type=str),
            "bestSeason": request.args.get("bestSeason", None, type=str),
            "riverClass": request.args.get("riverClass", None, type=str),
            "maxTents": request.args.get("maxTents", None, type=int),
            "fireAllowed": request.args.get("fireAllowed", None, type=bool),
            "lake": request.args.get("lake", None, type=bool),
            "routeType": request.args.get("routeType", None, type=str),
            "terrainType": request.args.get("terrainType", None, type=str)
        }

        #query = Location.query

         # Основной запрос с JOIN на таблицу категорий
        query = Location.query.join(Category)

        # Search in name or city
        if search_query:
            query = query.filter(
                or_(
                    Location.name.ilike(f"%{search_query}%"),
                    Location.city.ilike(f"%{search_query}%"),
                    Category.name.ilike(f"%{search_query}%")
                )
            )

        # search by category name
        if category_name:
            query = query.filter(Category.name.ilike(f"%{category_name}%"))

        # Filter by elevation (partial match) and distance (partial match)
        if elevation:
            query = query.filter(Location.elevation.cast(db.String).ilike(f"{elevation}%"))
        if distance:
            query = query.filter(Location.distance.cast(db.String).ilike(f"{distance}%"))

        # Paginate results
        locations = query.paginate(page=page, per_page=per_page, error_out=False)

        if not locations.items:
            return jsonify({"message": "No locations found."}), 404


        response = {
            "Locations": [{
                "id": loc.id,
                "name": loc.name,
                "ownerId": loc.ownerId,  # <== обязательно!
                "city": loc.city,
                # For 'imageUrl', we fetch the first image if it exists
                "imageUrl": (
                    get_location_images(loc.id)[0]["url"]
                    if get_location_images(loc.id) else None
                ),
                # Calculate average rating by fetching all reviews
                "avgRating": round(calculate_average_rating(get_reviews_for_location(loc.id)), 1),
                "reviewCount": len(get_reviews_for_location(loc.id)),
                "elevation": loc.elevation
            } for loc in locations.items],
            "Pagination": {
                "page": locations.page,
                "perPage": locations.per_page,
                "totalLocations": locations.total,
                "totalPages": locations.pages
            }
        }

        return jsonify(response), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500


#************************ GET /api/locations/<int:id> ************************
@location_routes.route("/<int:id>", methods=["GET"])
def get_location_detail(id):
    """
    Retrieves detailed information about a single location by ID, including:
      - All associated images
      - Reviews with images and user data
      - Owner info
      - Category-specific fields
      - Timestamps (createdAt/updatedAt)
    """
    try:
        location = Location.query.get(id)
        if not location:
            return jsonify({"message": "Location not found"}), 404

        # Grab location images and reviews
        location_images = get_location_images(location.id)
        reviews = get_reviews_for_location(location.id)
        avg_rating = calculate_average_rating(reviews)

        # Category-specific fields: depends on the categoryId
        category_fields = {
            1: ["elevation", "difficulty", "distance", "bestSeason"],  
            2: ["river_class", "distance"],   
            3: ["maxTents", "fireAllowed", "lake", "distance"], 
            4: ["routeType", "difficulty", "elevation", "distance"],
            5: ["bestSeason", "elevation", "distance"],
            6: ["terrainType", "distance", "elevation"]
        }

        # Generate a dictionary of only the relevant fields for this category
        category_specific = {

            # field: (
                
            #     {getattr(location, field)} if field == "distance" 
            #     else {int(getattr(location, field))} if field == "elevation" and getattr(location, field) % 1 == 0
            #     else {getattr(location, field)} if field == "elevation"
            #     else getattr(location, field)
            # )
            # for field in category_fields.get(location.categoryId, [])

            field: (
                
                f"{getattr(location, field)} mi" if field == "distance" 
                else f"{int(getattr(location, field))} ft" if field == "elevation" and getattr(location, field) % 1 == 0
                else f"{getattr(location, field)} ft" if field == "elevation"
                else getattr(location, field)
            )
            for field in category_fields.get(location.categoryId, [])
        }

            
        
        # Owner info (username, avatar, etc.)
        owner = User.query.get(location.ownerId)

        response = {
            "id": location.id,
            # "ownerId": location.ownerId,
            "name": location.name,
            "city": location.city,
            "description": location.description,
            "categoryId": location.categoryId,
            "categorySpecific": category_specific,
            "avgRating": round(avg_rating, 1),
            "reviewCount": len(reviews),
            "reviews": reviews,  # includes user data and images
            "images": location_images,
            "owner": {
                "id": owner.id,
                "username": owner.username,
                "avatar": owner.avatar
            },
            "createdAt": str(location.createdAt),
            "updatedAt": str(location.updatedAt)
        }

        return jsonify(response), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500


# ************************ GET /api/locations/current ************************
@location_routes.route('/current', methods=['GET'])
@login_required
def get_current_user_locations():
    """
    Returns a list of all locations whose 'ownerId' matches the current user's ID.
    Only accessible to logged-in users.
    """
    try:
        user_id = current_user.id
        locations = Location.query.filter_by(ownerId=user_id).all()

        if not locations:
            return jsonify({"message": "You have no locations"}), 200

        response = {
            "Locations": [{
                "id": loc.id,
                "name": loc.name,
                "city": loc.city,
                "categoryId": loc.categoryId,
                "imageUrl": (
                    get_location_images(loc.id)[0]["url"]
                    if get_location_images(loc.id) else None
                ),
                "avgRating": round(calculate_average_rating(get_reviews_for_location(loc.id)), 1),
                "reviewCount": len(get_reviews_for_location(loc.id))
            } for loc in locations]
        }

        return jsonify(response), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500


# ************************ POST /api/locations ************************
@location_routes.route('/new', methods=['POST'])
@login_required
def create_location():
    """
    Creates a new location, ensuring that all category-specific required fields are present
    and that numeric fields (distance/elevation) are positive.
    Also checks for duplicates (name + city).
    """
    try:
        data = request.get_json() or {}

        # Required fields for all categories
        base_required_fields = ["categoryId", "name", "city", "description", "distance"]

        # Category-specific fields
        category_fields = {
            1: ["difficulty", "bestSeason", "elevation"],  
            2: ["riverClass"],  
            3: ["maxTents", "fireAllowed", "lake", "elevation"],
            4: ["routeType", "difficulty", "elevation"],
            5: ["bestSeason", "elevation"],
            6: ["terrainType", "elevation"]
        }

        # Check categoryId
        category_id = data.get("categoryId")
        if category_id not in category_fields:
            return jsonify({"message": "Invalid categoryId"}), 400

        # Combine base + category fields
        required_fields = base_required_fields + category_fields[category_id]
        missing_fields = [f for f in required_fields if f not in data]
        if missing_fields:
            return jsonify({"message": "Missing required fields", "missing": missing_fields}), 400

        # Validate that 'name', 'city', 'description' are non-empty
        for field in ["name", "city", "description"]:
            if not data[field].strip():
                return jsonify({"message": f"Field '{field}' cannot be empty"}), 400

        # Validate 'distance' as a positive number
        if not isinstance(data["distance"], (int, float)) or data["distance"] <= 0:
            return jsonify({"message": "Distance must be a positive number"}), 400

        # If 'elevation' is required for this category, validate it as well
        if "elevation" in category_fields[category_id]:
            if not isinstance(data["elevation"], (int, float)) or data["elevation"] <= 0:
                return jsonify({"message": "Elevation must be a positive number"}), 400

        # Validate enum fields (difficulty, riverClass, routeType, terrainType)
        valid_difficulties = ["Easy", "Medium", "Hard"]
        valid_river_classes = ["I", "II", "III", "IV", "V"]
        valid_route_types = ["Trad", "Sport"]
        valid_terrain_types = ["Dirt", "Rocky", "Forest", "Mixed"]

        if "difficulty" in data and data["difficulty"] not in valid_difficulties:
            return jsonify({"message": "Invalid difficulty value"}), 400
        if "riverClass" in data and data["riverClass"] not in valid_river_classes:
            return jsonify({"message": "Invalid river class value"}), 400
        if "routeType" in data and data["routeType"] not in valid_route_types:
            return jsonify({"message": "Invalid route type value"}), 400
        if "terrainType" in data and data["terrainType"] not in valid_terrain_types:
            return jsonify({"message": "Invalid terrain type value"}), 400

        #Check for duplicate (location name + city)
        existing_location = Location.query.filter_by(name=data["name"], city=data["city"]).first()
        if existing_location:
            return jsonify({"message": "A location with this name already exists in this city"}), 400
        
        # Validate that at least four image is provided
        if "images" not in data or len(data["images"]) != 4:
            return jsonify({"message": "At least four image is required"}), 400

        # Create the new location
        new_loc = Location(
            categoryId=category_id,
            ownerId=current_user.id,
            name=data["name"],
            city=data["city"],
            description=data["description"],
            distance=data["distance"],
            elevation=data.get("elevation"),  
            difficulty=data.get("difficulty"),
            river_class=data.get("riverClass"),
            lake=data.get("lake"),
            fireAllowed=data.get("fireAllowed"),
            maxTents=data.get("maxTents"),
            routeType=data.get("routeType"),
            terrainType=data.get("terrainType"),
            bestSeason=data.get("bestSeason")
        )
        db.session.add(new_loc)
        db.session.commit()

        # Add images
        for img_data in data["images"]:
            new_image = LocationImage(
                locationId=new_loc.id,
                url=img_data["url"],
                preview=img_data.get("preview", False)
            )
            db.session.add(new_image)
        db.session.commit()


        response = {
            "id": new_loc.id,
            "ownerId": new_loc.ownerId,
            "categoryId": new_loc.categoryId,
            "name": new_loc.name,
            "city": new_loc.city,
            "description": new_loc.description,
            "distance": new_loc.distance,
            "images": [
                {
                    "id": img.id,
                    "url": img.url,
                    "preview": img.preview
                }
                for img in new_loc.images
            ]
        }
        # Add category-specific fields
        for field in category_fields[category_id]:
            response[field] = getattr(new_loc, field)

        return jsonify(response), 201

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"message": f"Internal server error: {str(e)}"}), 500

# ************************ PUT /api/locations/<int:id> ************************
@location_routes.route('/<int:location_id>', methods=['PUT'])
@login_required
def update_location(location_id):
    """
    Updates an existing location. Must match the owner and 
    pass all validation checks for the relevant category fields.
    """
    try:
        loc = Location.query.get(location_id)
        if not loc:
            return jsonify({"message": "Location not found"}), 404
        if loc.ownerId != current_user.id:
            return jsonify({"message": "Forbidden"}), 403

        data = request.get_json() or {}
        print("DAT FOR UPDATING:", data)  # Логируем данные

        if "images" not in data or len(data["images"]) != 4:
            return jsonify({"message": "Exactly 4 images are required"}), 400

        # Same approach as in create_location:
        base_required_fields = ["categoryId", "name", "city", "description", "distance"]
        category_fields = {
            1: ["difficulty", "bestSeason", "elevation"],
            2: ["riverClass"],
            3: ["maxTents", "fireAllowed", "lake", "elevation"],
            4: ["routeType", "difficulty", "elevation"],
            5: ["bestSeason", "elevation"],
            6: ["terrainType", "elevation"]
        }

        category_id = data.get("categoryId")
        if category_id not in category_fields:
            return jsonify({"message": "Invalid categoryId"}), 400

        required_fields = base_required_fields + category_fields[category_id]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"message": "Missing required fields", "missing": missing_fields}), 400

        # Check non-empty strings
        for field in ["name", "city", "description"]:
            if not data[field].strip():
                return jsonify({"message": f"Field '{field}' cannot be empty"}), 400

        # Check distance
        if not isinstance(data["distance"], (int, float)) or data["distance"] <= 0:
            return jsonify({"message": "Distance must be a positive number"}), 400

        # If this category requires elevation, check it
        if "elevation" in category_fields[category_id]:
            if not isinstance(data["elevation"], (int, float)) or data["elevation"] <= 0:
                return jsonify({"message": "Elevation must be a positive number"}), 400

        # Validate enum fields
        valid_difficulties = ["Easy", "Medium", "Hard"]
        valid_river_classes = ["I", "II", "III", "IV", "V"]
        valid_route_types = ["Trad", "Sport"]
        valid_terrain_types = ["Dirt", "Rocky", "Forest", "Mixed"]

        if "difficulty" in data and data["difficulty"] not in valid_difficulties:
            return jsonify({"message": "Invalid difficulty value"}), 400
        if "riverClass" in data and data["riverClass"] not in valid_river_classes:
            return jsonify({"message": "Invalid river class value"}), 400
        if "routeType" in data and data["routeType"] not in valid_route_types:
            return jsonify({"message": "Invalid route type value"}), 400
        if "terrainType" in data and data["terrainType"] not in valid_terrain_types:
            return jsonify({"message": "Invalid terrain type value"}), 400

        # Приводим текущие значения из БД к "чистому" виду:
        current_name = loc.name.strip().lower()
        current_city = loc.city.strip().lower()
        new_name = data["name"].strip().lower()
        new_city = data["city"].strip().lower()

        # Если изменилось хотя бы одно из значений,  проверку дубликатов
        if new_name != current_name or new_city != current_city:
            existing_location = Location.query.filter(
                func.lower(Location.name) == new_name,
                func.lower(Location.city) == new_city,
                Location.id != int(location_id)
            ).first()
            if existing_location:
                return jsonify({"message": "A location with this name already exists in this city"}), 409
        

        # Обновляем все поля, которые пришли в data
        for field in data:
            if field == "images":
                continue
            if hasattr(loc, field):
                setattr(loc, field, data[field])


        # Delete old images
        LocationImage.query.filter_by(locationId=location_id).delete()
        db.session.commit()  # Сохраняем удаление старых изображений

        # Add new images
        if "images" in data:
            for img_data in data["images"]:
                new_image = LocationImage(
                    locationId=location_id,
                    url=img_data["url"],
                    preview=img_data.get("preview", False)
                )
                db.session.add(new_image)
            db.session.commit()  # Сохраняем добавление новых изображений

        # Получаем обновленные изображения для ответа
        updated_images = LocationImage.query.filter_by(locationId=location_id).all()

        response = {
            "id": loc.id,
            "ownerId": loc.ownerId,
            "categoryId": loc.categoryId,
            "name": loc.name,
            "city": loc.city,
            "description": loc.description,
            "distance": loc.distance,
            "images": [
                {
                    "id": img.id,
                    "url": img.url,
                    "preview": img.preview
                }
                for img in updated_images
            ]
        }

        # Add category-specific fields
        for field in category_fields[category_id]:
            response[field] = getattr(loc, field)

        response["updatedAt"] = str(loc.updatedAt)

        return jsonify(response), 200

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"message": f"Internal server error: {str(e)}"}), 500
    

# ************************ DELETE /api/locations/<int:id> ************************
@location_routes.route('/<int:location_id>', methods=['DELETE'])
@login_required
def delete_location(location_id):
    """
    Deletes an existing location. Only allowed if the current user is the owner.
    """
    try:
        loc = Location.query.get(location_id)
        if not loc:
            return jsonify({"message": "Location not found"}), 404
        if loc.ownerId != current_user.id:
            return jsonify({"message": "Forbidden"}), 403

        db.session.delete(loc)
        db.session.commit()
        return jsonify({"message": "Location deleted"}), 200

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"message": "Internal server error"}), 500
    

# # ************************ LOCATION IMAGES ************************
#     # ************ POST /api/locations/:id/images ***************
@location_routes.route('/<int:location_id>/images', methods=['POST'])
@login_required
def add_location_image(location_id):
    """Adds a new image to a location."""
    try:
        location = Location.query.get(location_id)
        if not location:
            return jsonify({"message": "Location not found."}), 404
        if location.ownerId != current_user.id:
            return jsonify({"message": "Forbidden"}), 403

        # Getting data from the request
        data = request.get_json()
        image_url = data.get("url")
        preview = data.get("preview", False)  # False по умолчанию

        # Check for URL presence
        if not image_url:
            return jsonify({"message": "Image URL is required"}), 400

        # Checking the limit (5 images)
        if len(location.images) >= 10:
            return jsonify({"message": "Maximum number of images reached for this location (10)"}), 403

        # Create an image
        new_image = LocationImage(locationId=location_id, url=image_url, preview=preview)
        db.session.add(new_image)
        db.session.commit()

        # We return only the necessary data
        return jsonify({
            "id": new_image.id,
            "url": new_image.url,
            "preview": new_image.preview
        }), 201

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500

# ************ PUT /api/locations/:location_id/images/image_id ***************
@location_routes.route('/<int:location_id>/images/<int:image_id>', methods=['PUT'])
@login_required
def update_location_image(location_id, image_id):
    """Updates an existing image for a location."""
    try:
        location = Location.query.get(location_id)
        if not location:
            return jsonify({"message": "Location not found."}), 404
        if location.ownerId != current_user.id:
            return jsonify({"message": "Forbidden"}), 403

        image = LocationImage.query.get(image_id)
        if not image or image.locationId != location_id:
            return jsonify({"message": "Image not found."}), 404

        data = request.get_json()
        if not data or "url" not in data or "preview" not in data:
            return jsonify({"message": "URL and preview status are required"}), 400

        # Обновляем данные изображения
        image.url = data["url"]
        image.preview = data["preview"]
        # image.updatedAt = datetime.now(timezone.utc)

        db.session.commit()

        return jsonify({
            "id": image.id,
            "locationId": image.locationId,
            "url": image.url,
            "preview": image.preview,
            "updatedAt": str(image.updatedAt)
        }), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500
    
    # ************ DELETE /api/locations/:id/images ***************
@location_routes.route('/<int:location_id>/images/<int:image_id>', methods=['DELETE'])
@login_required
def delete_location_image(location_id, image_id):
    """Deletes an existing image from a location."""
    try:
        location = Location.query.get(location_id)
        if not location:
            return jsonify({"message": "Location not found."}), 404
        if location.ownerId != current_user.id:
            return jsonify({"message": "Forbidden"}), 403

        image = LocationImage.query.get(image_id)
        if not image or image.locationId != location_id:
            return jsonify({"message": "Image not found."}), 404

        # Удаляем изображение
        db.session.delete(image)
        db.session.commit()

        return jsonify({"message": "Image successfully deleted."}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500







