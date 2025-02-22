from app.models import db, Location, environment, SCHEMA
from sqlalchemy.sql import text

def seed_locations():
    locations = [
        # Hiking (Category 1)
        Location(categoryId=1, ownerId=1, name="Longs Peak", city="Estes Park", description="One of Colorado's famous 14ers.", height=4346.0, difficulty="Hard", distance=14.5, bestSeason="Summer"),
        Location(categoryId=1, ownerId=1, name="Maroon Bells", city="Aspen", description="Iconic twin peaks.", height=4270.0, difficulty="Medium", distance=12.0, bestSeason="Summer-Fall"),
        Location(categoryId=1, ownerId=1, name="Pikes Peak", city="Colorado Springs", description="America's Mountain, accessible by car or hike.", height=4302.0, difficulty="Hard", distance=13.5, bestSeason="Spring-Summer"),
        Location(categoryId=1, ownerId=1, name="Mount Elbert", city="Leadville", description="Colorado's highest peak.", height=4401.0, difficulty="Medium", distance=10.2, bestSeason="Summer"),
        Location(categoryId=1, ownerId=1, name="Hanging Lake", city="Glenwood Springs", description="Scenic hike to a pristine mountain lake.", height=2134.0, difficulty="Easy", distance=2.4, bestSeason="Spring-Summer"),
        Location(categoryId=1, ownerId=1, name="Humble Peak", city="Westcliffe", description="A challenging hike with stunning views.", height=3000.0, difficulty="Hard", distance=5.0, bestSeason="Summer"),
        Location(categoryId=1, ownerId=1, name="Rocky Mountain NP Trail", city="Estes Park", description="Famous national park with many hiking routes.", height=2500.0, difficulty="Medium", distance=8.0, bestSeason="Summer-Fall"),
        Location(categoryId=1, ownerId=1, name="Ice Lakes Trail", city="Silverton", description="A stunning turquoise alpine lake.", height=3200.0, difficulty="Hard", distance=7.5, bestSeason="Summer"),
        Location(categoryId=1, ownerId=1, name="Bear Peak Trail", city="Boulder", description="Challenging hike with rewarding views.", height=2600.0, difficulty="Hard", distance=9.0, bestSeason="Spring-Summer"),
        Location(categoryId=1, ownerId=1, name="Sky Pond Trail", city="Estes Park", description="Breathtaking scenery with waterfalls.", height=2900.0, difficulty="Medium", distance=10.5, bestSeason="Summer"),

        # Rafting (Category 2)
        Location(categoryId=2, ownerId=2, name="Eagle River", city="Eagle", description="Challenging river rafting experience.", height=2000.0, river_class="IV"),
        Location(categoryId=2, ownerId=2, name="San Miguel River", city="Telluride", description="Beautiful and scenic rafting trip.", height=1800.0, river_class="III"),
        Location(categoryId=2, ownerId=2, name="Yampa River", city="Steamboat Springs", description="Long multi-day rafting trips.", height=1900.0, river_class="III"),
        Location(categoryId=2, ownerId=2, name="Dolores River", city="Dolores", description="Exciting rapids in a remote canyon.", height=2100.0, river_class="IV"),
        Location(categoryId=2, ownerId=2, name="Blue River", city="Silverthorne", description="Popular beginner-friendly rafting spot.", height=1700.0, river_class="II"),
        Location(categoryId=2, ownerId=2, name="Arkansas River", city="Buena Vista", description="One of the most popular rafting rivers.", height=2200.0, river_class="IV"),
        Location(categoryId=2, ownerId=2, name="Gunnison River", city="Gunnison", description="Technical rapids with stunning scenery.", height=2000.0, river_class="IV"),
        Location(categoryId=2, ownerId=2, name="Colorado River", city="Grand Junction", description="Iconic river with diverse rafting options.", height=1800.0, river_class="III"),
        Location(categoryId=2, ownerId=2, name="Animas River", city="Durango", description="Thrilling rapids in Durango.", height=1900.0, river_class="IV"),
        Location(categoryId=2, ownerId=2, name="Cache la Poudre River", city="Fort Collins", description="Wild and scenic river with challenging rapids.", height=2100.0, river_class="IV"),

        # Camping (Category 3)
        Location(categoryId=3, ownerId=3, name="Bear Lake Campground", city="Estes Park", description="Great camping spot near Bear Lake.", height=2500.0, maxTents=10, fireAllowed=True, lake=True),
        Location(categoryId=3, ownerId=3, name="Twin Lakes Campground", city="Leadville", description="Amazing lake views for campers.", height=2600.0, maxTents=12, fireAllowed=True, lake=True),
        Location(categoryId=3, ownerId=3, name="Moraine Park Campground", city="Estes Park", description="Scenic campground in Rocky Mountain NP.", height=2400.0, maxTents=15, fireAllowed=True, lake=False),
        Location(categoryId=3, ownerId=3, name="Great Sand Dunes Campground", city="Mosca", description="Camp near the tallest sand dunes in North America.", height=2300.0, maxTents=20, fireAllowed=True, lake=False),
        Location(categoryId=3, ownerId=3, name="Maroon Bells Campground", city="Aspen", description="Camp with iconic mountain views.", height=2700.0, maxTents=10, fireAllowed=True, lake=True),
        Location(categoryId=3, ownerId=3, name="Blue Mesa Reservoir Campground", city="Gunnison", description="Lakeside camping with water activities.", height=2200.0, maxTents=12, fireAllowed=True, lake=True),
        Location(categoryId=3, ownerId=3, name="Golden Gate Canyon Campground", city="Golden", description="Peaceful camping near Denver.", height=2500.0, maxTents=10, fireAllowed=True, lake=False),
        Location(categoryId=3, ownerId=3, name="Chatfield State Park Campground", city="Littleton", description="Family-friendly camping near Denver.", height=1800.0, maxTents=15, fireAllowed=True, lake=True),
        Location(categoryId=3, ownerId=3, name="Rifle Falls State Park Campground", city="Rifle", description="Camp near stunning waterfalls.", height=2000.0, maxTents=10, fireAllowed=True, lake=False),
        Location(categoryId=3, ownerId=3, name="Steamboat Lake Campground", city="Steamboat Springs", description="Beautiful mountain lake camping.", height=2600.0, maxTents=12, fireAllowed=True, lake=True),

        # Climbing (Category 4)
        Location(categoryId=4, ownerId=4, name="Flatirons (Boulder)", city="Boulder", description="A classic Colorado climbing destination.", height=2500.0, routeType="Trad", difficulty="Hard"),
        Location(categoryId=4, ownerId=4, name="Lumpy Ridge", city="Estes Park", description="High-quality granite climbing.", height=2800.0, routeType="Trad", difficulty="Medium"),
        Location(categoryId=4, ownerId=4, name="Eldorado Canyon", city="Boulder", description="Iconic climbing spot near Boulder.", height=2200.0, routeType="Trad", difficulty="Hard"),
        Location(categoryId=4, ownerId=4, name="Black Canyon of the Gunnison", city="Montrose", description="Steep and challenging climbs.", height=2400.0, routeType="Trad", difficulty="Hard"),
        Location(categoryId=4, ownerId=4, name="Rifle Mountain Park", city="Rifle", description="World-class sport climbing.", height=2000.0, routeType="Sport", difficulty="Medium"),
        Location(categoryId=4, ownerId=4, name="Mount Evans", city="Idaho Springs", description="Alpine climbing with stunning views.", height=4300.0, routeType="Trad", difficulty="Hard"),
        Location(categoryId=4, ownerId=4, name="Garden of the Gods", city="Colorado Springs", description="Unique sandstone formations.", height=1900.0, routeType="Trad", difficulty="Easy"),
        Location(categoryId=4, ownerId=4, name="Tenmile Range", city="Breckenridge", description="Varied climbing routes in the Rockies.", height=3500.0, routeType="Trad", difficulty="Medium"),
        Location(categoryId=4, ownerId=4, name="Shelf Road", city="Cañon City", description="Popular sport climbing area.", height=2100.0, routeType="Sport", difficulty="Medium"),
        Location(categoryId=4, ownerId=4, name="Unaweep Canyon", city="Whitewater", description="Remote and challenging climbs.", height=2300.0, routeType="Trad", difficulty="Hard"),

        # Snow Sports (Category 5)
        Location(categoryId=5, ownerId=5, name="Vail Ski Resort", city="Vail", description="One of the most popular ski resorts.", height=3500.0, bestSeason="Winter"),
        Location(categoryId=5, ownerId=5, name="Steamboat Springs", city="Steamboat Springs", description="Home to legendary snowfalls.", height=3300.0, bestSeason="Winter"),
        Location(categoryId=5, ownerId=5, name="Telluride Ski Resort", city="Telluride", description="Known for its breathtaking scenery.", height=3400.0, bestSeason="Winter"),
        Location(categoryId=5, ownerId=5, name="Aspen Snowmass", city="Aspen", description="World-class skiing and snowboarding.", height=3200.0, bestSeason="Winter"),
        Location(categoryId=5, ownerId=5, name="Breckenridge Ski Resort", city="Breckenridge", description="Historic town with great slopes.", height=3100.0, bestSeason="Winter"),
        Location(categoryId=5, ownerId=5, name="Keystone Resort", city="Keystone", description="Family-friendly ski destination.", height=3000.0, bestSeason="Winter"),
        Location(categoryId=5, ownerId=5, name="Copper Mountain", city="Copper Mountain", description="Varied terrain for all skill levels.", height=2900.0, bestSeason="Winter"),
        Location(categoryId=5, ownerId=5, name="Winter Park Resort", city="Winter Park", description="Longest ski season in Colorado.", height=2800.0, bestSeason="Winter"),
        Location(categoryId=5, ownerId=5, name="Crested Butte", city="Crested Butte", description="Steep and challenging terrain.", height=3300.0, bestSeason="Winter"),
        Location(categoryId=5, ownerId=5, name="Wolf Creek Ski Area", city="Pagosa Springs", description="Known for its deep powder.", height=3200.0, bestSeason="Winter"),

        # ATV/Bikes (Category 6)
        Location(categoryId=6, ownerId=6, name="Rampart Range", city="Woodland Park", description="Amazing off-road terrain.", height=2500.0, distance=70.0),
        Location(categoryId=6, ownerId=6, name="Grand Mesa Trails", city="Grand Junction", description="Endless miles of off-road trails.", height=3000.0, distance=85.0),
        Location(categoryId=6, ownerId=6, name="Taylor Park", city="Almont", description="Popular ATV and dirt bike area.", height=2800.0, distance=60.0),
        Location(categoryId=6, ownerId=6, name="San Juan Mountains", city="Ouray", description="Scenic and challenging trails.", height=3200.0, distance=100.0),
        Location(categoryId=6, ownerId=6, name="Gunnison National Forest", city="Gunnison", description="Diverse terrain for off-roading.", height=2900.0, distance=90.0),
        Location(categoryId=6, ownerId=6, name="Uncompahgre National Forest", city="Montrose", description="Remote and rugged trails.", height=3100.0, distance=80.0),
        Location(categoryId=6, ownerId=6, name="White River National Forest", city="Glenwood Springs", description="Great for ATV and bike adventures.", height=2700.0, distance=75.0),
        Location(categoryId=6, ownerId=6, name="Pike National Forest", city="Colorado Springs", description="Close to Denver with varied trails.", height=2600.0, distance=65.0),
        Location(categoryId=6, ownerId=6, name="Rio Grande National Forest", city="Monte Vista", description="Remote and scenic trails.", height=3000.0, distance=95.0),
        Location(categoryId=6, ownerId=6, name="Curecanti National Recreation Area", city="Gunnison", description="Lakeside trails with great views.", height=2800.0, distance=70.0),
    ]

    db.session.add_all(locations)
    db.session.commit()

def undo_locations():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.locations RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM locations"))
    
    db.session.commit()