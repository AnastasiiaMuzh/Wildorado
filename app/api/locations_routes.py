from flask import Blueprint, request, jsonify
from app.models import db, Location
from sqlalchemy import or_

location_routes = Blueprint('locations', __name__)

@location_routes.route("/", methods=["GET"])
def get_locations():
    """Get locations with search, pagination, and category-specific filters"""
    try:
        # Pagination
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("perPage", 12, type=int)

        # Search (name, city, category)
        search_query = request.args.get("search", "", type=str).strip().lower()
        category = request.args.get("category", None, type=int)

        # Filters that all categories have
        elevation = request.args.get("elevation", None, type=str)
        distance = request.args.get("distance", None, type=str)

        # Category-specific filters
        difficulty = request.args.get("difficulty", None, type=str)
        best_season = request.args.get("bestSeason", None, type=str)
        river_class = request.args.get("riverClass", None, type=str)
        max_tents = request.args.get("maxTents", None, type=int)
        fire_allowed = request.args.get("fireAllowed", None, type=bool)
        lake = request.args.get("lake", None, type=bool)
        route_type = request.args.get("routeType", None, type=str)
        terrain_type = request.args.get("terrainType", None, type=str)

        query = Location.query

        # Search
        if search_query:
            query = query.filter(
                (Location.name.ilike(f"%{search_query}%")) |
                (Location.city.ilike(f"%{search_query}%"))
            )

        if category:
            query = query.filter(Location.categoryId == category)

        # Filter by elevation (все числа, начинающиеся с введённого значения)
        if elevation:
            query = query.filter(Location.elevation.cast(db.String).ilike(f"{elevation}%"))

        # Filter by distance (все числа, начинающиеся с введённого значения)
        if distance:
            query = query.filter(Location.distance.cast(db.String).ilike(f"{distance}%"))

        # Filters by category
        if category == 1:  # Hiking
            if difficulty:
                query = query.filter(Location.difficulty == difficulty)
            if best_season:
                query = query.filter(Location.bestSeason.ilike(f"%{best_season}%"))

        if category == 2:  # Rafting
            if river_class:
                query = query.filter(Location.river_class == river_class)

        if category == 3:  # Camping
            if max_tents:
                query = query.filter(Location.maxTents >= max_tents)
            if fire_allowed is not None:
                query = query.filter(Location.fireAllowed == fire_allowed)
            if lake is not None:
                query = query.filter(Location.lake == lake)

        if category == 4:  # Climbing
            if difficulty:
                query = query.filter(Location.difficulty == difficulty)
            if route_type:
                query = query.filter(Location.routeType == route_type)

        if category == 5:  # Snow Sports
            if best_season:
                query = query.filter(Location.bestSeason.ilike(f"%{best_season}%"))

        if category == 6:  # ATV/Bikes
            if terrain_type:
                query = query.filter(Location.terrainType == terrain_type)

        # Pagination
        locations = query.paginate(page=page, per_page=per_page, error_out=False)

        if not locations.items:
            return jsonify({"message": "No locations found."}), 404

        return jsonify({
            "Locations": [{
                "id": location.id,
                "name": location.name,
                "city": location.city,
                "description": location.description,
                "elevation": location.elevation,
                "distance": location.distance,
                "difficulty": location.difficulty,
                "bestSeason": location.bestSeason,
                "riverClass": location.river_class,
                "maxTents": location.maxTents,
                "fireAllowed": location.fireAllowed,
                "lake": location.lake,
                "routeType": location.routeType,
                "terrainType": location.terrainType
            } for location in locations.items],
            "Pagination": {
                "page": locations.page,
                "perPage": locations.per_page,
                "totalLocations": locations.total,
                "totalPages": locations.pages
            }
        }), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500



# Hiking : elevation, difficulty, distance, bestSeason
# Rafting : river_class, distance
# Camping : maxTents, fireAllowed, lake
# Climbing : routeType, difficulty, elevation, distance
# Snow Sports : bestSeason, elevation, distance
# ATV/Bikes : terrainType, distance, elevation