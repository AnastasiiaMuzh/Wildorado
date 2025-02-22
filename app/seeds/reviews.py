from app.models import db, Review, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime, timezone
import random

def seed_reviews():
    reviews = [
        # Hiking (Category 1)
        Review(userId=2, locationId=1, stars=5, text="Absolutely stunning hike! The views from the summit were breathtaking."),
        Review(userId=3, locationId=1, stars=4, text="Very challenging, but worth every step."),
        Review(userId=4, locationId=2, stars=5, text="Maroon Bells is one of the most beautiful places I've ever seen."),
        Review(userId=5, locationId=2, stars=4, text="Amazing, but crowded during peak season."),
        Review(userId=6, locationId=3, stars=5, text="Pikes Peak is incredible. The drive up was scenic too!"),
        Review(userId=7, locationId=3, stars=3, text="Too many tourists at the top, but great views."),
        Review(userId=8, locationId=4, stars=5, text="Mount Elbert was a tough climb but so rewarding."),
        Review(userId=9, locationId=4, stars=4, text="Be prepared for unpredictable weather!"),
        Review(userId=10, locationId=5, stars=5, text="Hanging Lake was absolutely stunning. The water is so clear!"),
        Review(userId=1, locationId=5, stars=5, text="One of the most unique hikes in Colorado."),

        # Rafting (Category 2)
        Review(userId=2, locationId=11, stars=4, text="Exciting rapids! Highly recommend for thrill-seekers."),
        Review(userId=3, locationId=11, stars=5, text="One of the best rafting experiences ever!"),
        Review(userId=4, locationId=12, stars=3, text="Not as intense as I expected, but still fun."),
        Review(userId=5, locationId=12, stars=4, text="Beautiful scenery along the river."),
        Review(userId=6, locationId=13, stars=5, text="The guides were fantastic, and the rapids were exhilarating!"),
        Review(userId=7, locationId=13, stars=4, text="A bit too crowded, but overall a great experience."),
        Review(userId=8, locationId=14, stars=5, text="Perfect mix of adventure and relaxation."),
        Review(userId=9, locationId=14, stars=4, text="Would definitely come back again!"),
        Review(userId=10, locationId=15, stars=5, text="Great for beginners, highly recommended!"),
        Review(userId=1, locationId=15, stars=4, text="Super fun but a bit short."),

        # Camping (Category 3)
        Review(userId=2, locationId=21, stars=5, text="Amazing campground with stunning lake views."),
        Review(userId=3, locationId=21, stars=4, text="Nice and quiet, but bring bug spray!"),
        Review(userId=4, locationId=22, stars=5, text="Perfect for a weekend getaway."),
        Review(userId=5, locationId=22, stars=3, text="Facilities could use some improvement."),
        Review(userId=6, locationId=23, stars=5, text="Incredible location surrounded by nature."),
        Review(userId=7, locationId=23, stars=4, text="Fire pits were useful, and the lake was beautiful!"),
        Review(userId=8, locationId=24, stars=5, text="One of the best camping spots in Colorado!"),
        Review(userId=9, locationId=24, stars=4, text="Great for stargazing."),
        Review(userId=10, locationId=25, stars=5, text="Clean, quiet, and relaxing."),
        Review(userId=1, locationId=25, stars=4, text="Highly recommended for nature lovers!"),

        # Climbing (Category 4)
        Review(userId=2, locationId=31, stars=5, text="One of the best climbing spots in the country!"),
        Review(userId=3, locationId=31, stars=4, text="Challenging but super rewarding."),
        Review(userId=4, locationId=32, stars=5, text="Lumpy Ridge has amazing climbing routes!"),
        Review(userId=5, locationId=32, stars=3, text="It was a bit crowded, but still great."),
        Review(userId=6, locationId=33, stars=5, text="Eldorado Canyon is perfect for trad climbing."),
        Review(userId=7, locationId=33, stars=4, text="Very scenic and great rock quality."),
        Review(userId=8, locationId=34, stars=5, text="A must-visit for serious climbers."),
        Review(userId=9, locationId=34, stars=4, text="Great routes and fun challenges."),
        Review(userId=10, locationId=35, stars=5, text="Excellent variety of routes!"),
        Review(userId=1, locationId=35, stars=4, text="Awesome climbing, but bring lots of water!"),

        # Snow Sports (Category 5)
        Review(userId=2, locationId=41, stars=5, text="Vail is my favorite ski resort!"),
        Review(userId=3, locationId=41, stars=4, text="Snow was amazing, but expensive."),
        Review(userId=4, locationId=42, stars=5, text="Steamboat has the best powder!"),
        Review(userId=5, locationId=42, stars=3, text="The lift lines were too long."),
        Review(userId=6, locationId=43, stars=5, text="Telluride is magical."),
        Review(userId=7, locationId=43, stars=4, text="Great resort, but pricey."),
        Review(userId=8, locationId=44, stars=5, text="Aspen Snowmass is world-class."),
        Review(userId=9, locationId=44, stars=4, text="The terrain variety is excellent."),
        Review(userId=10, locationId=45, stars=5, text="Breckenridge is fantastic for families."),
        Review(userId=1, locationId=45, stars=4, text="Great ski town with a lot to offer!"),

        # ATV/Bikes (Category 6)
        Review(userId=2, locationId=51, stars=5, text="Rampart Range is an off-road paradise!"),
        Review(userId=3, locationId=51, stars=4, text="Fun and challenging trails."),
        Review(userId=4, locationId=52, stars=5, text="Grand Mesa Trails are amazing!"),
        Review(userId=5, locationId=52, stars=3, text="Good variety, but some areas are rough."),
        Review(userId=6, locationId=53, stars=5, text="Taylor Park is a must for ATV lovers."),
        Review(userId=7, locationId=53, stars=4, text="Great trails, but can be busy."),
        Review(userId=8, locationId=54, stars=5, text="Incredible mountain views."),
        Review(userId=9, locationId=54, stars=4, text="Well-maintained trails."),
        Review(userId=10, locationId=55, stars=5, text="A true off-road adventure."),
        Review(userId=1, locationId=55, stars=4, text="Challenging and rewarding."),
    ]

    db.session.add_all(reviews)
    db.session.commit()

def undo_reviews():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.reviews RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM reviews"))

    db.session.commit()
