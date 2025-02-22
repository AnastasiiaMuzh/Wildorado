from app.models import db, EventParticipant, environment, SCHEMA
from sqlalchemy.sql import text

def seed_event_participants():
    participants = [
        # Участники события 1 (Hiking)
        EventParticipant(eventId=1, userId=2),  # Marnie
        EventParticipant(eventId=1, userId=4),  # Alice
        EventParticipant(eventId=1, userId=5),  # Charlie
        EventParticipant(eventId=1, userId=6),  # Dave
        
        # Участники события 2 (Climbing)
        EventParticipant(eventId=2, userId=7),  # Ana
        EventParticipant(eventId=2, userId=8),  # Mila
        EventParticipant(eventId=2, userId=9),  # Jake
        
        # Участники события 3 (ATV/Bikes)
        EventParticipant(eventId=3, userId=3),  # Bobbie
        EventParticipant(eventId=3, userId=5),  # Charlie
        EventParticipant(eventId=3, userId=6),  # Dave
        EventParticipant(eventId=3, userId=7),  # Ana
        EventParticipant(eventId=3, userId=9)   # Jake
    ]

    db.session.add_all(participants)
    db.session.commit()


def undo_event_participants():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.event_participants RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM event_participants"))
    
    db.session.commit()
