from app.models import db, Event, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime

def seed_events():
    event1 = Event(
        locationId=7,  # Humble Peak (Hiking)
        userId=1,  # Demo user
        title="Spring Hiking Adventure",
        description="Join us for an amazing hike at Humble Peak. Expect stunning views and a great workout!",
        date=datetime(2025, 3, 22),
        maxParticipants=5
    )

    event2 = Event(
        locationId=16,  # Lumpy Ridge (Climbing)
        userId=3,  # Bobbie
        title="Climbing Challenge at Lumpy Ridge",
        description="A fun climbing event for all skill levels. Gear up and get ready for an adventure!",
        date=datetime(2025, 3, 29),
        maxParticipants=5
    )

    event3 = Event(
        locationId=26,  # Rampart Range (ATV/Bikes)
        userId=5,  # Charlie
        title="Off-Road Adventure at Rampart Range",
        description="Experience the thrill of off-roading in one of the best ATV trails in Colorado!",
        date=datetime(2025, 4, 12),
        maxParticipants=10
    )

    db.session.add_all([event1, event2, event3])
    db.session.commit()


def undo_events():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.events RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM events"))
    
    db.session.commit()
