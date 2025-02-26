from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user, logout_user
from app.models import User, db, Friendship

profile_routes = Blueprint('profile', __name__)

#*********************** GET /api/profile ***********************#
@profile_routes.route('/', methods=['GET'])
@login_required
def get_profile():
    """ Get the current user's profile """
    return jsonify(current_user.to_dict()), 200


#*********************** PUT /api/profile ***********************#
@profile_routes.route('/', methods=['PUT'])
@login_required
def update_profile():
    """ Update the current user's profile """

    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No data provided"}), 400  

    if "avatar" in data:
        if not isinstance(data["avatar"], str):  
            return jsonify({"message": "Avatar must be a string"}), 400
        current_user.avatar = data["avatar"]

    if "bio" in data:
        if not isinstance(data["bio"], str):  
            return jsonify({"message": "Bio must be a string"}), 400
        current_user.bio = data["bio"]

    if "interests" in data:
        if not isinstance(data["interests"], str): 
            return jsonify({"message": "Interests must be a string"}), 400
        current_user.interests = data["interests"]

    try:
        db.session.commit()
        return jsonify(current_user.to_dict()), 200
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Internal server error"}), 500


#*********************** DELETE /api/profile (удаление профиля) ***********************#

@profile_routes.route('/', methods=['DELETE'])
@login_required
def delete_profile():
    user_id = current_user.id
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404  

    # Удаляем дружбу, если надо
    Friendship.query.filter(
        (Friendship.userId1 == user_id) | (Friendship.userId2 == user_id)
    ).delete()

    logout_user()
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Profile deleted"}), 200
