from app.models import db, Friendship, environment, SCHEMA
from sqlalchemy.sql import text

def seed_friendships():
    friendships = [
        # Accepted friendships
        Friendship(userId1=1, userId2=2, status="accepted"),
        Friendship(userId1=1, userId2=3, status="accepted"),
        Friendship(userId1=2, userId2=4, status="accepted"),
        Friendship(userId1=3, userId2=5, status="accepted"),
        Friendship(userId1=4, userId2=6, status="accepted"),
        Friendship(userId1=5, userId2=7, status="accepted"),
        Friendship(userId1=6, userId2=8, status="accepted"),
        Friendship(userId1=7, userId2=9, status="accepted"),
        Friendship(userId1=8, userId2=10, status="accepted"),
        
        # Pending friendships
        # Friendship(userId1=2, userId2=3, status="pending"),
        # Friendship(userId1=4, userId2=5, status="pending"),
        # Friendship(userId1=6, userId2=7, status="pending"),
        # Friendship(userId1=8, userId2=9, status="pending"),
        # Friendship(userId1=9, userId2=10, status="pending")
    ]

    db.session.add_all(friendships)
    db.session.commit()

def undo_friendships():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.friendships RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM friendships"))
    
    db.session.commit()
