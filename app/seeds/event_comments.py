from app.models import db, EventComment, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime, timezone

def seed_event_comments():
    comments = [
        # Discussion for Event 1 (Hiking)
        EventComment(eventId=1, userId=2, message="What time are we starting? Maybe 6 AM?", createdAt=datetime(2025, 3, 15, 8, 30, tzinfo=timezone.utc)),
        EventComment(eventId=1, userId=4, message="I think 7 AM would be better, so it's not too dark.", createdAt=datetime(2025, 3, 15, 9, 00, tzinfo=timezone.utc)),
        EventComment(eventId=1, userId=5, message="Good idea! Who's bringing snacks?", createdAt=datetime(2025, 3, 15, 9, 30, tzinfo=timezone.utc)),

        # Discussion for Event 2 (Climbing)
        EventComment(eventId=2, userId=7, message="Does anyone know the best way to get there? Do we need a 4WD?", createdAt=datetime(2025, 3, 28, 10, 00, tzinfo=timezone.utc)),
        EventComment(eventId=2, userId=8, message="I've been there! The road is fine, but we should leave early.", createdAt=datetime(2025, 3, 28, 10, 45, tzinfo=timezone.utc)),
        EventComment(eventId=2, userId=9, message="Should we bring our own gear, or is there rental available?", createdAt=datetime(2025, 3, 28, 11, 15, tzinfo=timezone.utc)),

        # Discussion for Event 3 (ATV/Bikes)
        EventComment(eventId=3, userId=3, message="Where are we meeting before we start?", createdAt=datetime(2025, 4, 11, 13, 00, tzinfo=timezone.utc)),
        EventComment(eventId=3, userId=5, message="We can meet at the park entrance, there's a good parking spot.", createdAt=datetime(2025, 4, 11, 13, 30, tzinfo=timezone.utc)),
        EventComment(eventId=3, userId=6, message="How long do you think the ride will take?", createdAt=datetime(2025, 4, 11, 14, 00, tzinfo=timezone.utc))
    ]

    db.session.add_all(comments)
    db.session.commit()

def undo_event_comments():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.event_comments RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM event_comments"))
    
    db.session.commit()
