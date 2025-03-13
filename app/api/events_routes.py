from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from datetime import datetime
from app.models import db, Location, User, Event, EventComment, EventParticipant
from sqlalchemy import func


events_routes = Blueprint('events', __name__)


# ************************ GET /api/events ************************
@events_routes.route("/", methods=["GET"])
def get_events():
    """Getting a list of all events."""
    try:
        events = Event.query.all()
        if not events:
            return jsonify({"message": "Location not found"}), 404
        
        event_ids = [event.id for event in events]

        participant_counts = dict(
            db.session.query(
                EventParticipant.eventId,
                func.count(EventParticipant.userId)
            )
            .filter(EventParticipant.eventId.in_(event_ids))
            .group_by(EventParticipant.eventId)
            .all()
        )
        
        events_data = []
        for ev in events:
            events_data.append({
                "id": ev.id,
                "locationId": ev.locationId,
                "userId": ev.userId,
                "title": ev.title,
                "description": ev.description,
                "date": ev.date,
                "maxParticipants": ev.maxParticipants,
                "participantCount": participant_counts.get(ev.id, 0), 
                "createdAt": ev.createdAt,
                "updatedAt": ev.updatedAt
            })

        return jsonify({"events": events_data}), 200
        
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500  

# ************************ GET /api/events/:eventId ************************   
@events_routes.route('/<int:event_id>', methods=["GET"]) 
def get_event_detail(event_id):
    """Get event details including participants and comments (only for participants + creator)."""
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"message": "Event not found"}), 404
        
        # Get current user's ID if authenticated
        current_user_id = current_user.id if current_user.is_authenticated else None
        
        # Retrieve all event participants in one query
        participants = EventParticipant.query.filter_by(eventId=event.id).all()
        participant_ids = [p.userId for p in participants]
        
        # Check if current user is participant or creator
        is_participant = (
            current_user_id is not None and
            (current_user_id == event.userId or current_user_id in participant_ids)
        )
        
        # Collect all user IDs we need to fetch
        user_ids = set(participant_ids)
        if event.userId:
            user_ids.add(event.userId)
            
        # Initialize comments data
        comments_data = []
        
        # Get comments only if user is participant or creator
        if is_participant:
            comments = EventComment.query.filter_by(eventId=event.id).all()
            
            # Add comment author IDs to the list of users we need to fetch
            comment_author_ids = [c.userId for c in comments]
            user_ids.update(comment_author_ids)
        
        # Fetch all needed users
        users = {user.id: user for user in User.query.filter(User.id.in_(list(user_ids))).all()} if user_ids else {}
        
        # Get creator data
        creator_data = {
            "id": event.userId,
            "username": users.get(event.userId).username if users.get(event.userId) else "Unknown"
        } if event.userId else None
        
        # Format participants data
        participants_data = [
            {"id": p.userId, "username": users.get(p.userId).username if users.get(p.userId) else "Unknown"} 
            for p in participants
        ]
        
        # Format comments data if user is participant/creator
        if is_participant and 'comments' in locals():
            comments_data = [
                {
                    "id": c.id,
                    "userId": c.userId,
                    "username": users.get(c.userId).username if users.get(c.userId) else "Unknown",
                    "message": c.message,
                    "createdAt": c.createdAt
                }
                for c in comments
            ]
        
        event_data = {
            "id": event.id,
            "locationId": event.locationId,
            "userId": event.userId,
            "title": event.title,
            "description": event.description,
            "date": event.date,
            "maxParticipants": event.maxParticipants,
            "createdAt": event.createdAt,
            "updatedAt": event.updatedAt,
            "creator": creator_data,
            "participants": participants_data,
            "comments": comments_data
        }
        
        return jsonify({"event": event_data}), 200
        
    except Exception as e:
        print(f"🔥 ERROR: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

    
# ************************ GET /api/events/current ************************
@events_routes.route('/current', methods=["GET"])
@login_required
def get_current_user_event():
    """Get all events created by the current user."""

    try:
        events = Event.query.filter_by(userId=current_user.id).all()
        if not events:
            return jsonify({"message": "You do not have any Events!"}), 200
        
        events_data = []
        for ev in events:
            events_data.append({
                "id": ev.id,
                "locationId": ev.locationId,
                "userId": ev.userId,
                "title": ev.title,
                "description": ev.description,
                "date": ev.date,
                "maxParticipants": ev.maxParticipants,
                "createdAt": ev.createdAt,
                "updatedAt": ev.updatedAt
            })

        return jsonify({"events": events_data}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500
    
# ************************ POST /api/events ************************
@events_routes.route("/", methods=["POST"])
@login_required
def create_event():
    """Create a new event."""
    try:
        data = request.get_json() or {}

        # Check if required fields are passed
        title = data.get("title", "").strip()
        description = data.get("description", "").strip()
        date = data.get("date")
        location_id = data.get("locationId")
        max_participants = data.get("maxParticipants")

        # Data validation
        errors = {}
        if not title:
            errors["title"] = "Title is required"
        if not date:
            errors["date"] = "Date is required"
        else:
            try:
                event_date = datetime.fromisoformat(date)
                if event_date < datetime.now():
                    errors["date"] = "Date must be in the future"
            except ValueError:
                errors["date"] = "Invalid date format"


        location = Location.query.get(location_id)
        if not location:
            return jsonify({"message": "Location not found"}), 404

        if max_participants is not None and (not isinstance(max_participants, int) or max_participants <= 0):
            errors["maxParticipants"] = "Max participants must be a positive number"

        if errors:
            return jsonify({"message": "Bad Request", "errors": errors}), 400
        

        # Check if there is already an event with the same name, in the same location, on the same date
        existing_event = Event.query.filter_by(
        title=data["title"],
        locationId=location_id,
        # date=data["date"]
        date=event_date  
        ).first()

        if existing_event:
            return jsonify({"message": "An event with this title at this location on the same date already exists."}), 400

        # Create event
        new_event = Event(
            locationId=location_id,
            userId=current_user.id,
            title=title,
            description=description,
            date=event_date,
            maxParticipants=max_participants
        )

        db.session.add(new_event)
        db.session.commit()

        return jsonify({
            "id": new_event.id,
            "locationId": new_event.locationId,
            "userId": new_event.userId,
            "title": new_event.title,
            "description": new_event.description,
            "date": new_event.date,
            "maxParticipants": new_event.maxParticipants,
            "createdAt": new_event.createdAt,
            "updatedAt": new_event.updatedAt
        }), 201

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "Internal server error"}), 500


# ************************ POST /api/events/:eventId/join ************************
@events_routes.route('/<int:event_id>/join', methods=["POST"])
@login_required
def join_event(event_id):
    """Join in event."""
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"message": "Event not found"}), 404

        # Check if current user already Participant
        already_participant = EventParticipant.query.filter_by(eventId=event_id, userId=current_user.id).first()
        if already_participant:
            return jsonify({"message": "You are already participating in this event"}), 400

        # Check if not maximum number of participants been exceeded
        participant_count = EventParticipant.query.filter_by(eventId=event_id).count()
        if event.maxParticipants and participant_count >= event.maxParticipants:
            return jsonify({"message": "This event is already full"}), 400
        
        # Add user to event!
        new_participant = EventParticipant(eventId=event_id, userId=current_user.id)
        db.session.add(new_participant)
        db.session.commit()

        return jsonify({"message": "Successfully joined the event"}), 201
    
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "Internal server error"}), 500


# ************************ DELETE /api/events/:eventId/leave ************************
@events_routes.route('/<int:event_id>/leave', methods=["DELETE"])
@login_required
def leave_event(event_id):
    """Leave in event."""
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"message": "Event not found"}), 404
        
        already_participant = EventParticipant.query.filter_by(eventId=event_id, userId=current_user.id).first()
        
        if not already_participant:
            return jsonify({"message": "You are not a participant of this event"}), 400
        
        db.session.delete(already_participant)
        db.session.commit()
        return jsonify({"message": "Sacssesfuly leave Event!"}), 200
    
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"message": "Internal server error"}), 500
        
        
# ************************ POST /api/events/:eventId/comments ************************
@events_routes.route('/<int:event_id>/comments', methods=["POST"])
@login_required
def create_comments(event_id):
    """Create a comments for the event."""
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"message": "Event not found"}), 404
        
        # Check if current user participant
        current_participant = EventParticipant.query.filter_by(eventId=event.id, userId=current_user.id).first()
        if not current_participant:
            return jsonify({"message": "You must join the event before commenting!"}), 400
        
        # Get comment data
        data = request.get_json() or {}
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"message": "Comment cannot be empty!"}), 400
        
        # Create new comment
        new_comment = EventComment(
            eventId=event.id,
            userId=current_user.id,
            message=message
        )

        db.session.add(new_comment)
        db.session.commit()

        return jsonify({
            "id": new_comment.id,
            "eventId": new_comment.eventId,
            "userId": new_comment.userId,
            "message": new_comment.message,
            "createdAt": new_comment.createdAt,
            "updatedAt": new_comment.updatedAt
        }), 201

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "Internal server error"}), 500

# ************************ Delete /api/events/:eventid/comments/:commentId ************************
@events_routes.route('/<int:event_id>/comments/<int:comment_id>', methods=["DELETE"])
@login_required
def delete_comment(event_id, comment_id):
    """Delete comment, (only author)"""
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"message": "Event not found"}), 404
        
        comment = EventComment.query.get(comment_id)
        if not comment or comment.eventId != event_id:
            return jsonify({"message": "Comment not found"}), 404
        
        if comment.userId != current_user.id:
            return jsonify({"message": "Forbidden"}), 403
        
        db.session.delete(comment)
        db.session.commit()

        return jsonify({"message": "Comment successfully deleted."}), 200
    
    except Exception as e:
        print (e)
        return jsonify({"message": "Internal server error"}), 500

# ************************ PUT /api/events/event_id ************************
@events_routes.route('/<int:event_id>', methods=["PUT"])
@login_required
def update_event(event_id):
    """Update an event (only the creator can edit)."""
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"message": "Event not found"}), 404

        if event.userId != current_user.id:
            return jsonify({"message": "Forbidden"}), 403
        
        # Get data from request
        data = request.get_json() or {}
        
        title = data.get("title", "").strip()
        description = data.get("description", "").strip()
        date = data.get("date")
        max_participants = data.get("maxParticipants")

        errors = {}

        if title:
            event.title = title
        if description:
            event.description = description
        if date:
            try:
                event_date = datetime.fromisoformat(date)
                if event_date < datetime.utcnow():
                    errors["date"] = "Date must be in the future"
                else:
                    event.date = event_date
            except ValueError:
                errors["date"] = "Invalid date format"
        if max_participants is not None:
            if not isinstance(max_participants, int) or max_participants <= 0:
                errors["maxParticipants"] = "Max participants must be a positive number"
            else:
                event.maxParticipants = max_participants

        if errors:
            return jsonify({"message": "Bad Request", "errors": errors}), 400

        # Update date
        event.updatedAt = datetime.now()

        # Save changes
        db.session.commit()

        return jsonify({
            "id": event.id,
            "locationId": event.locationId,
            "userId": event.userId,
            "title": event.title,
            "description": event.description,
            "date": event.date,
            "maxParticipants": event.maxParticipants,
            "createdAt": event.createdAt,
            "updatedAt": event.updatedAt
        }), 200

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "Internal server error"}), 500

# ************************ Delete /api/event/:eventId ************************
@events_routes.route('/<int:event_id>', methods=["DELETE"])
@login_required
def delete_event(event_id):
    """Delete event, (only the creator can delete)"""
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"message": "Event not found"}), 404

        if event.userId != current_user.id:
            return jsonify({"message": "Forbidden"}), 403
        
        db.session.delete(event)
        db.session.commit()
        
        return jsonify({"message": "Event successfully deleted."}), 200
    
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "Internal server error"}), 500


# *** Доступно для всех (без входа в систему):
# GET /api/events → Получить список всех событий
# GET /api/events/:eventId → Получить детали конкретного события
# *** Только для залогиненных пользователей:
# GET /api/events/current -> Poluchit svoi eventi
# POST /api/events → Создать новое событие
# POST /api/events/:eventId/join → Присоединиться к событию
# DELETE /api/events/:eventId/leave → Покинуть событие
# POST /api/events/:eventId/comments → Оставить комментарий
# DELETE /api/events/:eventId/comments/:commentId → Удалить свой комментарий
# PUT /api/events/:eventId → Редактировать свое событие
# DELETE /api/events/:eventId → Удалить свое событие