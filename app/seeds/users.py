from app.models import db, User, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a demo user, you can add other users here if you want
def seed_users():
    demo = User(
        username='Demo', email='demo@aa.io', password='password')
    marnie = User(
        username='marnie', email='marnie@aa.io', password='password')
    bobbie = User(
        username='bobbie', email='bobbie@aa.io', password='password')
    alice = User(
        username='alice', email='alice@aa.io', password='password')
    charlie = User(
        username='charlie', email='charlie@aa.io', password='password')
    dave = User(
        username='dave', email='dave@aa.io', password='password')
    ana = User(
        username='ana', email='ana@aa.io', password='password')
    mila = User(
        username='mila', email='mila@aa.io', password='password')
    jake = User(
        username='jake', email='jake@aa.io', password='password')
    masha = User(
        username='masha', email='masha@aa.io', password='password')


    db.session.add(demo)
    db.session.add(marnie)
    db.session.add(bobbie)
    db.session.add(alice)
    db.session.add(charlie)
    db.session.add(dave)
    db.session.add(ana)
    db.session.add(mila)
    db.session.add(jake)
    db.session.add(masha)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_users():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM users"))
        
    db.session.commit()
