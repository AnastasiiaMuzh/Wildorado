from flask import Blueprint, jsonify, request
from app.models import db, Location, User, Event, EventComment, EventParticipant, LocationImage
from sqlalchemy import func
from flask_login import login_required, current_user
from datetime import datetime, timezone
from dateutil.parser import isoparse
from app.models import db, Event

events_routes = Blueprint('events', __name__)

# ************************ GET /api/events ************************
@events_routes.route("/", methods=["GET"])
def get_events():
    try:
        events = Event.query.all()
        if not events:
            return jsonify({"message": "Events not found"}), 404

        event_ids = [event.id for event in events]
        location_ids = [event.locationId for event in events]

        # participant_count = EventParticipant.query.filter_by(eventId=ev.id).count()<--BAD!!!

        # получаем количество участников для всех событий одним запросом
        participant_counts = dict(
            db.session.query(
                EventParticipant.eventId,               
                func.count(EventParticipant.userId)    
            )
            .filter(EventParticipant.eventId.in_(event_ids))
            .group_by(EventParticipant.eventId)            
            .all()                                          
        )

        # Если пользователь залогинен, заранее достанем все eventId,
        # где он является участником. Избегаем n-запросов в цикле
        current_user_event_ids = set()
        if current_user.is_authenticated:
            # Найдём все записи EventParticipant для current_user
            user_participations = EventParticipant.query.filter_by(userId=current_user.id).all()
            current_user_event_ids = {ep.eventId for ep in user_participations}


        # получаем location вместе с их превью-фото одним запросом
        locations = Location.query.filter(Location.id.in_(location_ids)).all()
        locations_data = {loc.id: loc for loc in locations}

        preview_images = dict(
            db.session.query(LocationImage.locationId, LocationImage.url)
            .filter(
                LocationImage.locationId.in_(location_ids),
                LocationImage.preview == True
            )
            .all()
        )

        events_data = []
        for ev in events:
            location = locations_data.get(ev.locationId)
            is_current_user_participant = ev.id in current_user_event_ids

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
                "updatedAt": ev.updatedAt,
                "isCurrentUserParticipant": is_current_user_participant,
                "location": {
                    "name": location.name if location else None,
                    "city": location.city if location else None,
                    "previewImage": preview_images.get(ev.locationId, None),
                }
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
        
        # Получаем данные о локации
        location = Location.query.get(event.locationId)
        
        # превью-изображение
        preview_image = db.session.query(LocationImage.url).filter_by(locationId=event.locationId, preview=True).scalar()

        # данные о создателе события
        creator = User.query.get(event.userId)
        
        # ID текущего пользователя, если он залогинен
        current_user_id = current_user.id if current_user.is_authenticated else None
        
        # участников события
        participants = EventParticipant.query.filter_by(eventId=event.id).all()
        participant_ids = [p.userId for p in participants]
        
        # является ли текущий пользователь создателем или участником
        is_participant = current_user_id in {event.userId, *participant_ids}

        # все userId, которые нам нужны
        user_ids = set(participant_ids + [event.userId])
        
        # комментарии, если пользователь — участник или создатель
        comments_data = []
        if is_participant:
            comments = EventComment.query.filter_by(eventId=event.id).all()
            comment_author_ids = [c.userId for c in comments]
            user_ids.update(comment_author_ids)

        # всех нужных пользователей
        users = {user.id: user for user in User.query.filter(User.id.in_(user_ids)).all()}

        # Формируем список участников (добавляем avatar)
        participants_data = [
            {
                "id": p.userId,
                "username": users.get(p.userId).username if users.get(p.userId) else "Unknown",
                "avatar": users.get(p.userId).avatar if users.get(p.userId) else None
            }
            for p in participants
        ]

        # список комментариев
        if is_participant:
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
        
        # ответ
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
            "creator": {
                "id": creator.id if creator else None,
                "username": creator.username if creator else "Unknown",
                "avatar": creator.avatar if creator else None
            },
            "participants": participants_data,
            "comments": comments_data,
            "location": {
                "id": location.id if location else None,
                "name": location.name if location else None,
                "city": location.city if location else None,
                "previewImage": preview_image
            } if location else None
        }
        
        return jsonify({"event": event_data}), 200
        
    except Exception as e:
        print(f"ERROR DETAILS LOCATION: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

    
# ************************ GET /api/events/current ************************
@events_routes.route('/current', methods=['GET'])
@login_required
def get_current_user_events():
    """
    Returns a list of all events, которые текущий пользователь СОЗДАЛ.
    """
    try:
        user_id = current_user.id

        # события, которые СОЗДАЛ текущий пользователь
        created_events = Event.query.filter_by(userId=user_id).all()

        # Убираем события, в которых пользователь только участник
        all_events = created_events  # Теперь список содержит ТОЛЬКО СОЗДАННЫЕ события

        if not all_events:
            return jsonify({"message": "You have no events"}), 200

        # event_ids = [event.id for event in all_events]
        location_ids = [event.locationId for event in all_events]

        # Получаем только локации этих событий
        locations = Location.query.filter(Location.id.in_(location_ids)).all()
        locations_data = {loc.id: loc for loc in locations}

        # Получаем превью-изображения для этих локаций
        preview_images = dict(
            db.session.query(LocationImage.locationId, LocationImage.url)
            .filter(
                LocationImage.locationId.in_(location_ids),
                LocationImage.preview == True
            )
            .all()
        )

        response = {
            "events": [{
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "date": event.date,
                "maxParticipants": event.maxParticipants,
                "locationId": event.locationId,
                "location": {
                    "id": location.id if location else None,
                    "name": location.name if location else None,
                    "city": location.city if location else None,
                    "previewImage": preview_images.get(event.locationId, None)
                } if (location := locations_data.get(event.locationId)) else None,
                "createdAt": event.createdAt,
                "updatedAt": event.updatedAt
            } for event in all_events]
        }

        return jsonify(response), 200

    except Exception as e:
        print(f"ERROR EVENT CURRENT: {str(e)}")  
        return jsonify({"message": "Internal server error"}), 500

# ************************ POST /api/events ************************
@events_routes.route("/new", methods=["POST"])
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
        if not description:
            errors["description"] = "Description is required"    
        if not date:
            errors["date"] = "Date is required"
        if not max_participants:
            errors["max_participants"] = "Max Participant is required"    
        if max_participants is None and (not isinstance(max_participants, int) or max_participants <= 0):
            errors["maxParticipants"] = "Max participants must be a positive number"    
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
        print("MAX CHECK", max_participants)

        # if max_participants is None and (not isinstance(max_participants, int) or max_participants <= 0):
        #     errors["maxParticipants"] = "Max participants must be a positive number"
        # print("CHeck HERE!!!", errors)

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

        #Add the creator to the participants
        creator_participant = EventParticipant(
            eventId=new_event.id,
            userId=current_user.id
        )
        db.session.add(creator_participant)
        db.session.commit()  # Сохраняем участника

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
    
# ************************ PUT /api/events/:eventId/comments/:commentId ************************
@events_routes.route('/<int:event_id>/comments/<int:comment_id>', methods=["PUT"])   
@login_required
def update_comment(event_id, comment_id):
    """Update a comment (only author can edit)."""
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"message": "Event not found"}), 404
        
        comment = EventComment.query.get(comment_id)
        if not comment or comment.eventId != event_id:
            return jsonify({"message": "Comment not found"}), 404
        
        if comment.userId != current_user.id:
            return jsonify({"message": "Forbidden"}), 403
        
        data = request.get_json() or {}
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"message": "Comment cannot be empty!"}), 400
        
        comment.message = message
        comment.updatedAt = datetime.now()
        db.session.commit()

        return jsonify({
            "id": comment.id,
            "eventId": comment.eventId,
            "userId": comment.userId,
            "message": comment.message,
            "createdAt": comment.createdAt,
            "updatedAt": comment.updatedAt
        }), 200
    

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

# # ************************ PUT /api/events/event_id ************************
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
        
        # данные из запроса
        data = request.get_json() or {}
        
        title = data.get("title", "").strip()
        description = data.get("description", "").strip()
        date_str = data.get("date")
        max_participants = data.get("maxParticipants")

        errors = {}

        # Обновляем заголовок и описание (если переданы)
        if title:
            event.title = title
        if description:
            event.description = description

        # Обработка даты
        if date_str:
            try:
                # Преобразуем дату в объект datetime
                event_date = isoparse(date_str)

                # Если в дате нет часового пояса, добавляем UTC
                if event_date.tzinfo is None:
                    event_date = event_date.replace(tzinfo=timezone.utc)

                # Проверяем, чтобы дата была в будущем
                if event_date < datetime.now(timezone.utc):
                    errors["date"] = "Date must be in the future"
                else:
                    event.date = event_date

            except ValueError as e:
                errors["date"] = "Invalid date format"

        # Проверка maxParticipants
        if max_participants is not None:
            try:
                max_participants = int(max_participants)  # Принудительно преобразуем в int
                if max_participants <= 0:
                    raise ValueError
                event.maxParticipants = max_participants
            except ValueError:
                errors["maxParticipants"] = "Max participants must be a positive number"

        if errors:
            return jsonify({"message": "Bad Request", "errors": errors}), 400

        # Обновляем время изменения
        event.updatedAt = datetime.now(timezone.utc)

        # Сохраняем изменения
        db.session.commit()

        return jsonify({
            "id": event.id,
            "locationId": event.locationId,
            "userId": event.userId,
            "title": event.title,
            "description": event.description,
            "date": event.date.isoformat(),  # Отправляем в ISO формате
            "maxParticipants": event.maxParticipants,
            "createdAt": event.createdAt.isoformat(),
            "updatedAt": event.updatedAt.isoformat()
        }), 200

    except Exception as e:
        print(f" ERROR from update event: {e}")
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