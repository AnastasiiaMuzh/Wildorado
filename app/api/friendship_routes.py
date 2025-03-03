from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from datetime import datetime
from app.models import db, User, Friendship

friendship_routes = Blueprint('friendships', __name__)
    
# ************************ GET /api/friends ************************
@friendship_routes.route('/', methods=["GET"])
@login_required
def get_all_friends():
    """Get all friends of current user (status="accepted")."""
    try:

        # Get all friendships where current user is involved and status is "accepted"
        friendships = Friendship.query.filter(
            Friendship.status == "accepted",
            ((Friendship.userId1 == current_user.id) | (Friendship.userId2 == current_user.id))
        ).all()

        if not friendships:
            return jsonify({"friends": []}), 200  # Пустой список!, а не 404

        
        # Get all friends
        friend_ids = {f.userId1 if f.userId2 == current_user.id else f.userId2 for f in friendships}
        friends = {u.id: u for u in User.query.filter(User.id.in_(friend_ids)).all()}

        friends_data = [
            {"id": user.id, "username": user.username, "avatar": user.avatar}
            for user in friends.values()
        ]

        return jsonify({"friends": friends_data}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500

# ************************ GET /api/friends ************************
@friendship_routes.route('/suggestions', methods=["GET"])
@login_required
def get_friends_suggestions():
    """Get a list of users that the current user can add as friends."""

    try:

        # Get the ID of all users with whom there is already friendship
        existing_friends = Friendship.query.filter(
            (Friendship.userId1 == current_user.id) | (Friendship.userId2 == current_user.id)
        ).all()
        
        # Collect the IDs of everyone with whom we already have connections, no matter what is on the list
        connected_users = {current_user.id}  # Add yourself to not show in the list
        for friendship in existing_friends:
            connected_users.add(friendship.userId1)
            connected_users.add(friendship.userId2)

        # Search for users that are not in connected_users
        available_users = User.query.filter(User.id.notin_(list(connected_users))).all()

        # Get current user's interests as a set
        current_user_interest_set = set(current_user.interests.lower().split(",")) if current_user.interests else set()

        # Separate users into two groups
        users_with_shared_interests = []
        other_users = []

        for user in available_users:
            user_interest_set = set(user.interests.lower().split(",")) if user.interests else set()
            if current_user_interest_set & user_interest_set:  # Check for common interests
                users_with_shared_interests.append(user)
            else:
                other_users.append(user)

        # Form the final list: first with common interests, then all others
        sorted_users = users_with_shared_interests + other_users

        users_data = [
            {"id": user.id, "username": user.username, "avatar": user.avatar, "interests": user.interests}
            for user in sorted_users
        ]

        return jsonify({"suggestions": users_data}), 200
    
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500
    
# ************************ GET /api/friends/requests ************************
@friendship_routes.route('/requests', methods=["GET"])
@login_required
def get_friend_requests():
    """Get all pending friend requests for the current user."""

    try:
        # Find all requests that are sent to the current user (userId2) and have the status "pending"
        friend_requests = Friendship.query.filter(
            Friendship.userId2 == current_user.id,
            Friendship.status == "pending"
        ).all()

        # Get a list of user IDs that submitted requests
        request_user_ids = [f.userId1 for f in friend_requests]

        # Get all users in one request
        users = {u.id: u for u in User.query.filter(User.id.in_(request_user_ids)).all()}

        # Create a list of applications
        requests_data = [
            {
                "id": users[user_id].id,
                "username": users[user_id].username,
                "avatar": users[user_id].avatar,
                "friendshipId": f.id  # ID самой заявки
            }
            for user_id, f in zip(request_user_ids, friend_requests) if user_id in users
        ]

        return jsonify({"friend_requests": requests_data}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500

    
# ************************ POST /api/friends/:userId ************************
@friendship_routes.route('/<int:user_id>', methods=["POST"])
@login_required
def send_friend_request(user_id):
    """Send a friend request to another user."""
    try:
        # Check if user is trying to add themselves
        if user_id == current_user.id:
            return jsonify({"message": "You cannot send a friend request to yourself."}), 400

        # Check if user exists
        recipient = User.query.get(user_id)
        if not recipient:
            return jsonify({"message": "User not found."}), 404

        # Check if a friendship already exists
        existing_friendship = Friendship.query.filter(
            ((Friendship.userId1 == current_user.id) & (Friendship.userId2 == user_id)) |
            ((Friendship.userId1 == user_id) & (Friendship.userId2 == current_user.id))
        ).first()

        if existing_friendship:
            if existing_friendship.status == "pending":
                return jsonify({"message": "Friend request already sent!"}), 400
            elif existing_friendship.status == "accepted":
                return jsonify({"message": "You are already friends!"}), 400
            elif existing_friendship.status == "blocked":
                return jsonify({"message": "This user has blocked you."}), 403

        # Create a new friendship request (status: pending)
        new_request = Friendship(
            userId1=current_user.id,
            userId2=user_id,
            status="pending"
        )

        db.session.add(new_request)
        db.session.commit()

        return jsonify({
            "message": "Friend request sent successfully!",
            "friendshipId": new_request.id,
            "status": new_request.status
        }), 201

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "Internal server error"}), 500

# ************************ PUT /api/friends/:friendshipId ************************
@friendship_routes.route('/<int:friendship_id>', methods=["PUT"])
@login_required
def update_friend_request(friendship_id):
    """Accept or decline a friend request."""
    try:
        data = request.get_json() or {}
        new_status = data.get("status")  # "accepted" or "blocked"

        if new_status not in ["accepted", "blocked"]:
            return jsonify({"message": "Invalid status. Use 'accepted' or 'blocked'"}), 400

        friendship = Friendship.query.get(friendship_id)

        if not friendship:
            return jsonify({"message": "Friendship request not found"}), 404

        # Check that the current user is the one to whom the request was sent (userId2)
        if friendship.userId2 != current_user.id:
            return jsonify({"message": "Forbidden"}), 403

        if new_status == "accepted":
            friendship.status = "accepted"
        elif new_status == "blocked":
            db.session.delete(friendship)  # Delete the entry if you decide to block it

        db.session.commit()

        return jsonify({"message": f"Friend request {new_status} successfully"}), 200

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "Internal server error"}), 500
    
# ************************ DELETE /api/friends/:friendshipId ************************
@friendship_routes.route('/<int:friendship_id>', methods=["DELETE"])
@login_required
def remove_friendship(friendship_id):
    """Remove a friend or cancel a pending request."""
    try:
        friendship = Friendship.query.get(friendship_id)

        if not friendship:
            return jsonify({"message": "Friendship not found"}), 404

        # Check if the current user is one of the friendship parties
        if current_user.id not in [friendship.userId1, friendship.userId2]:
            return jsonify({"message": "Forbidden"}), 403

        db.session.delete(friendship)
        db.session.commit()

        return jsonify({"message": "Friendship successfully removed"}), 200

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "Internal server error"}), 500



   
    
# GET /api/friends –  (список друзей)
# GET /api/friends/suggestions – (список пользователей, которых можно добавить)
# Список заявок	GET	/api/friends/requests	Показать pending заявки
# Отправить заявку	POST	/api/friends/:userId	Отправить запрос в друзья
# Принять/отклонить	PUT	/api/friends/:friendshipId	Обновить статус (accepted/blocked)
# Удалить друга	DELETE	/api/friends/:friendshipId	Разорвать дружбу
