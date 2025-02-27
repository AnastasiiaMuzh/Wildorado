from app.models import db, Location, environment, SCHEMA
from sqlalchemy.sql import text

def seed_locations():
    locations = [
        # Hiking (Category 1)
        Location(categoryId=1, ownerId=1, name="Longs Peak", city="Estes Park", description="One of Colorado's famous 14ers.", elevation=14259, difficulty="Hard", distance=14.5, bestSeason="Summer"),
        Location(categoryId=1, ownerId=1, name="Maroon Bells", city="Aspen", description="Iconic twin peaks.", elevation=14163, difficulty="Medium", distance=12.0, bestSeason="Summer-Fall"),
        Location(categoryId=1, ownerId=1, name="Pikes Peak", city="Colorado Springs", description="America's Mountain, accessible by car or hike.", elevation=14115, difficulty="Hard", distance=13.5, bestSeason="Spring-Summer"),
        Location(categoryId=1, ownerId=1, name="Mount Elbert", city="Leadville", description="Colorado's highest peak.", elevation=14440, difficulty="Medium", distance=10.2, bestSeason="Summer"),
        Location(categoryId=1, ownerId=1, name="Hanging Lake", city="Glenwood Springs", description="Scenic hike to a pristine mountain lake.", elevation=7000, difficulty="Easy", distance=2.4, bestSeason="Spring-Summer"),
        Location(categoryId=1, ownerId=1, name="Humble Peak", city="Westcliffe", description="A challenging hike with stunning views.", elevation=9843, difficulty="Hard", distance=5.0, bestSeason="Summer"),
        Location(categoryId=1, ownerId=1, name="Rocky Mountain NP Trail", city="Estes Park", description="Famous national park with many hiking routes.", elevation=8200, difficulty="Medium", distance=8.0, bestSeason="Summer-Fall"),
        Location(categoryId=1, ownerId=1, name="Ice Lakes Trail", city="Silverton", description="A stunning turquoise alpine lake.", elevation=10498, difficulty="Hard", distance=7.5, bestSeason="Summer"),
        Location(categoryId=1, ownerId=1, name="Bear Peak Trail", city="Boulder", description="Challenging hike with rewarding views.", elevation=8461, difficulty="Hard", distance=9.0, bestSeason="Spring-Summer"),
        Location(categoryId=1, ownerId=1, name="Sky Pond Trail", city="Estes Park", description="Breathtaking scenery with waterfalls.", elevation=10747, difficulty="Medium", distance=10.5, bestSeason="Summer"),


        # Rafting (Category 2)
        Location(categoryId=2, ownerId=2, name="Eagle River", city="Eagle", description="Challenging river rafting experience.", river_class="IV", distance=12.5),
        Location(categoryId=2, ownerId=2, name="San Miguel River", city="Telluride", description="Beautiful and scenic rafting trip.", river_class="III", distance=18.0),
        Location(categoryId=2, ownerId=2, name="Yampa River", city="Steamboat Springs", description="Long multi-day rafting trips.", river_class="III", distance=44.0),
        Location(categoryId=2, ownerId=2, name="Dolores River", city="Dolores", description="Exciting rapids in a remote canyon.", river_class="IV", distance=32.5),
        Location(categoryId=2, ownerId=2, name="Blue River", city="Silverthorne", description="Popular beginner-friendly rafting spot.", river_class="II", distance=10.0),
        Location(categoryId=2, ownerId=2, name="Arkansas River", city="Buena Vista", description="One of the most popular rafting rivers.", river_class="IV", distance=45.0),
        Location(categoryId=2, ownerId=2, name="Gunnison River", city="Gunnison", description="Technical rapids with stunning scenery.", river_class="IV", distance=22.0),
        Location(categoryId=2, ownerId=2, name="Colorado River", city="Grand Junction", description="Iconic river with diverse rafting options.", river_class="III", distance=50.0),
        Location(categoryId=2, ownerId=2, name="Animas River", city="Durango", description="Thrilling rapids in Durango.", river_class="IV", distance=15.0),
        Location(categoryId=2, ownerId=2, name="Cache la Poudre River", city="Fort Collins", description="Wild and scenic river with challenging rapids.", river_class="IV", distance=30.0),


        # Camping (Category 3)
        Location(categoryId=3, ownerId=3, name="Bear Lake Campground", city="Estes Park", description="Great camping spot near Bear Lake.", elevation=8200.0, maxTents=10, fireAllowed=True, lake=True, distance=0.5),
        Location(categoryId=3, ownerId=3, name="Twin Lakes Campground", city="Leadville", description="Amazing lake views for campers.", elevation=8600.0, maxTents=12, fireAllowed=True, lake=True, distance=1.0),
        Location(categoryId=3, ownerId=3, name="Moraine Park Campground", city="Estes Park", description="Scenic campground in Rocky Mountain NP.", elevation=7900.0, maxTents=15, fireAllowed=True, lake=False, distance=2.5),
        Location(categoryId=3, ownerId=3, name="Great Sand Dunes Campground", city="Mosca", description="Camp near the tallest sand dunes in North America.", elevation=7500.0, maxTents=20, fireAllowed=True, lake=False, distance=0.0),
        Location(categoryId=3, ownerId=3, name="Maroon Bells Campground", city="Aspen", description="Camp with iconic mountain views.", elevation=8900.0, maxTents=10, fireAllowed=True, lake=True, distance=1.2),
        Location(categoryId=3, ownerId=3, name="Blue Mesa Reservoir Campground", city="Gunnison", description="Lakeside camping with water activities.", elevation=7200.0, maxTents=12, fireAllowed=True, lake=True, distance=0.0),
        Location(categoryId=3, ownerId=3, name="Golden Gate Canyon Campground", city="Golden", description="Peaceful camping near Denver.", elevation=8200.0, maxTents=10, fireAllowed=True, lake=False, distance=1.8),
        Location(categoryId=3, ownerId=3, name="Chatfield State Park Campground", city="Littleton", description="Family-friendly camping near Denver.", elevation=5900.0, maxTents=15, fireAllowed=True, lake=True, distance=0.0),
        Location(categoryId=3, ownerId=3, name="Rifle Falls State Park Campground", city="Rifle", description="Camp near stunning waterfalls.", elevation=6600.0, maxTents=10, fireAllowed=True, lake=False, distance=0.7),
        Location(categoryId=3, ownerId=3, name="Steamboat Lake Campground", city="Steamboat Springs", description="Beautiful mountain lake camping.", elevation=8600.0, maxTents=12, fireAllowed=True, lake=True, distance=0.5),


        # Climbing (Category 4)
        Location(categoryId=4, ownerId=4, name="Flatirons (Boulder)", city="Boulder", description="A classic Colorado climbing destination.", elevation=8200.0, routeType="Trad", difficulty="Hard", distance=5.5),
        Location(categoryId=4, ownerId=4, name="Lumpy Ridge", city="Estes Park", description="High-quality granite climbing.", elevation=9200.0, routeType="Trad", difficulty="Medium", distance=6.0),
        Location(categoryId=4, ownerId=4, name="Eldorado Canyon", city="Boulder", description="Iconic climbing spot near Boulder.", elevation=7300.0, routeType="Trad", difficulty="Hard", distance=4.8),
        Location(categoryId=4, ownerId=4, name="Black Canyon of the Gunnison", city="Montrose", description="Steep and challenging climbs.", elevation=8100.0, routeType="Trad", difficulty="Hard", distance=7.2),
        Location(categoryId=4, ownerId=4, name="Rifle Mountain Park", city="Rifle", description="World-class sport climbing.", elevation=6600.0, routeType="Sport", difficulty="Medium", distance=3.5),
        Location(categoryId=4, ownerId=4, name="Mount Evans", city="Idaho Springs", description="Alpine climbing with stunning views.", elevation=14265.0, routeType="Trad", difficulty="Hard", distance=8.1),
        Location(categoryId=4, ownerId=4, name="Garden of the Gods", city="Colorado Springs", description="Unique sandstone formations.", elevation=6400.0, routeType="Trad", difficulty="Easy", distance=2.7),
        Location(categoryId=4, ownerId=4, name="Tenmile Range", city="Breckenridge", description="Varied climbing routes in the Rockies.", elevation=11400.0, routeType="Trad", difficulty="Medium", distance=6.3),
        Location(categoryId=4, ownerId=4, name="Shelf Road", city="Cañon City", description="Popular sport climbing area.", elevation=7200.0, routeType="Sport", difficulty="Medium", distance=4.0),
        Location(categoryId=4, ownerId=4, name="Unaweep Canyon", city="Whitewater", description="Remote and challenging climbs.", elevation=7800.0, routeType="Trad", difficulty="Hard", distance=5.9),


        # Snow Sports (Category 5)
        Location(categoryId=5, ownerId=5, name="Vail Ski Resort", city="Vail", description="One of the most popular ski resorts.", elevation=11570.0, bestSeason="Winter", distance=195.0),
        Location(categoryId=5, ownerId=5, name="Steamboat Springs", city="Steamboat Springs", description="Home to legendary snowfalls.", elevation=10568.0, bestSeason="Winter", distance=165.0),
        Location(categoryId=5, ownerId=5, name="Telluride Ski Resort", city="Telluride", description="Known for its breathtaking scenery.", elevation=13150.0, bestSeason="Winter", distance=148.0),
        Location(categoryId=5, ownerId=5, name="Aspen Snowmass", city="Aspen", description="World-class skiing and snowboarding.", elevation=12510.0, bestSeason="Winter", distance=237.0),
        Location(categoryId=5, ownerId=5, name="Breckenridge Ski Resort", city="Breckenridge", description="Historic town with great slopes.", elevation=12998.0, bestSeason="Winter", distance=187.0),
        Location(categoryId=5, ownerId=5, name="Keystone Resort", city="Keystone", description="Family-friendly ski destination.", elevation=12408.0, bestSeason="Winter", distance=128.0),
        Location(categoryId=5, ownerId=5, name="Copper Mountain", city="Copper Mountain", description="Varied terrain for all skill levels.", elevation=12313.0, bestSeason="Winter", distance=150.0),
        Location(categoryId=5, ownerId=5, name="Winter Park Resort", city="Winter Park", description="Longest ski season in Colorado.", elevation=12060.0, bestSeason="Winter", distance=143.0),
        Location(categoryId=5, ownerId=5, name="Crested Butte", city="Crested Butte", description="Steep and challenging terrain.", elevation=12162.0, bestSeason="Winter", distance=120.0),
        Location(categoryId=5, ownerId=5, name="Wolf Creek Ski Area", city="Pagosa Springs", description="Known for its deep powder.", elevation=11900.0, bestSeason="Winter", distance=77.0),


        # ATV/Bikes (Category 6)
        Location(categoryId=6, ownerId=6, name="Rampart Range", city="Woodland Park", description="Amazing off-road terrain.", elevation=2500.0, distance=70.0, terrainType="Dirt"),
        Location(categoryId=6, ownerId=6, name="Grand Mesa Trails", city="Grand Junction", description="Endless miles of off-road trails.", elevation=3000.0, distance=85.0, terrainType="Rocky"),
        Location(categoryId=6, ownerId=6, name="Taylor Park", city="Almont", description="Popular ATV and dirt bike area.", elevation=2800.0, distance=60.0, terrainType="Mixed"),
        Location(categoryId=6, ownerId=6, name="San Juan Mountains", city="Ouray", description="Scenic and challenging trails.", elevation=3200.0, distance=100.0, terrainType="Dirt"),
        Location(categoryId=6, ownerId=6, name="Gunnison National Forest", city="Gunnison", description="Diverse terrain for off-roading.", elevation=2900.0, distance=90.0, terrainType="Forest"),
        Location(categoryId=6, ownerId=6, name="Uncompahgre National Forest", city="Montrose", description="Remote and rugged trails.", elevation=3100.0, distance=80.0, terrainType="Rocky"),
        Location(categoryId=6, ownerId=6, name="White River National Forest", city="Glenwood Springs", description="Great for ATV and bike adventures.", elevation=2700.0, distance=75.0, terrainType="Mixed"),
        Location(categoryId=6, ownerId=6, name="Pike National Forest", city="Colorado Springs", description="Close to Denver with varied trails.", elevation=2600.0, distance=65.0, terrainType="Dirt"),
        Location(categoryId=6, ownerId=6, name="Rio Grande National Forest", city="Monte Vista", description="Remote and scenic trails.", elevation=3000.0, distance=95.0, terrainType="Forest"),
        Location(categoryId=6, ownerId=6, name="Curecanti National Recreation Area", city="Gunnison", description="Lakeside trails with great views.", elevation=2800.0, distance=70.0, terrainType="Rocky"),

    ]

    db.session.add_all(locations)
    db.session.commit()

def undo_locations():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.locations RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM locations"))
    
    db.session.commit()