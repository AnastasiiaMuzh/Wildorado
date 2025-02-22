from app.models import db, Category, environment, SCHEMA
from sqlalchemy.sql import text

def seed_categories():
    hiking = Category(name="Hiking")
    rafting = Category(name="Rafting")
    camping = Category(name="Camping")
    climbing = Category(name="Climbing")
    snow_sports = Category(name="Snow Sports")
    atv_bikes = Category(name="ATV/Bikes")

    db.session.add_all([hiking, rafting, camping, climbing, snow_sports, atv_bikes])
    db.session.commit()

def undo_categories():  
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.categories RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM categories"))
        
    db.session.commit()
