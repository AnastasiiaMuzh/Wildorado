from flask.cli import AppGroup
from .users import seed_users, undo_users
from .categories import seed_categories, undo_categories
from .locations import seed_locations, undo_locations
from .location_images import seed_location_images, undo_location_images
from .reviews import seed_reviews, undo_reviews
from .reviewImages import seed_review_images, undo_review_images
from .events import seed_events, undo_events
from .event_participants import seed_event_participants, undo_event_participants
from .event_comments import seed_event_comments, undo_event_comments
from .friendships import seed_friendships, undo_friendships


from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Before seeding in production, you want to run the seed undo 
        # command, which will  truncate all tables prefixed with 
        # the schema name (see comment in users.py undo_users function).
        # Make sure to add all your other model's undo functions below
        undo_friendships()
        undo_event_comments()
        undo_event_participants()
        undo_events()
        undo_review_images()
        undo_reviews()
        undo_location_images()
        undo_locations()
        undo_categories()
        undo_users()
    seed_users()
    seed_categories()
    seed_locations()
    seed_location_images()
    seed_reviews()
    seed_review_images()
    seed_events()
    seed_event_participants()
    seed_event_comments()
    seed_friendships()
    # Add other seed functions here


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_friendships()
    undo_event_comments()
    undo_event_participants()
    undo_events()
    undo_review_images()
    undo_reviews()
    undo_location_images()
    undo_locations()
    undo_categories()
    undo_users()
    # Add other undo functions here
