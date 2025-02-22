from app.models import db, ReviewImage, environment, SCHEMA
from sqlalchemy.sql import text

def seed_review_images():
    review_images = [
        # Review images for Hiking
        ReviewImage(reviewId=1, imageUrl="https://images.pexels.com/photos/8316325/pexels-photo-8316325.jpeg"),
        ReviewImage(reviewId=2, imageUrl="https://www.planetware.com/wpimages/2021/08/colorado-steamboat-springs-best-campgrounds-summit-lake-campground.jpg"),
        ReviewImage(reviewId=5, imageUrl="https://blog.gritroutdoors.com/wp-content/uploads/2017/04/hiking-alternative-thumb.jpg"),

        # Review images for Rafting
        ReviewImage(reviewId=11, imageUrl="https://thumbs.dreamstime.com/b/white-water-rifting-kayaks-rafting-fun-dangerous-sport-paddle-nature-fun-swift-turbulence-overturn-96628062.jpg"),
        ReviewImage(reviewId=12, imageUrl="https://example.com/rafting2.jpg"),

        # Review images for Camping
        ReviewImage(reviewId=21, imageUrl="https://t3.ftcdn.net/jpg/00/70/99/30/360_F_70993026_lnxa519g1TKt1E8153PEKGillBlPJ2ev.jpg"),
        ReviewImage(reviewId=22, imageUrl="https://images.stockcake.com/public/b/2/f/b2f75a42-ca23-492d-8c51-8807d8a0f377_large/mountain-camping-adventure-stockcake.jpg"),

        # Review images for Climbing
        ReviewImage(reviewId=31, imageUrl="https://images.pexels.com/photos/303040/pexels-photo-303040.jpeg?cs=srgb&dl=pexels-riciardus-303040.jpg&fm=jpg"),

        # Review images for Snow Sports
        ReviewImage(reviewId=41, imageUrl="https://www.shutterstock.com/image-photo/people-skiing-winter-holidays-snowcovered-260nw-2578939683.jpg"),
        ReviewImage(reviewId=42, imageUrl="https://images.stockcake.com/public/a/5/1/a511640c-8545-42fc-903d-d6d9b68ee8da_large/winter-ski-paradise-stockcake.jpg"),

        # Review images for Demo User (id=1)
        ReviewImage(reviewId=10, imageUrl="https://photos.thedyrt.com/photo/39127/photo/trout-lake-creek_a2037ad615ae0f4f5965696e7b74eafd.JPG"),

    ]

    db.session.add_all(review_images)
    db.session.commit()

def undo_review_images():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.review_images RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM review_images"))
    
    db.session.commit()
