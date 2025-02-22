from app.models import db, LocationImage, environment, SCHEMA
from sqlalchemy.sql import text


def seed_location_images():
    location_images_data = {
        1: [
            {"url": "https://static.cozycozy.com/images/catalog/bg2/horizontal-estes-park.jpg", "preview": True},
            {"url": "https://haydenslandscapes.com/images/07/LongsPeak.jpg", "preview": False},
            {"url": "https://thatcoloradocouple.com/wp-content/uploads/2022/10/Alberta-Falls-2-min-1024x819.jpg", "preview": False},
            {"url": "https://vanadieu.com/wp-content/uploads/2018/07/Depositphotos_48845721_original-400x500.jpg", "preview": False}
        ],
        2: [
            {"url": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhX3WN0InOdeFOJdu7QnIHOq_96ZVIK10cGj1JAM6xfOjlyqZYrkWd3JG5E7e-oXOQG_ByYdYZoZdn8sxlrOxhH2GALKcYFXl2RgV_ElZLCnpVVA8GKDeS68ptL-kJBN8LGMRt5X8MFkxLx/s800/MaroonBells_Aspen14_2.jpg", "preview": True},
            {"url": "https://bluemountainbelle.com/wp-content/uploads/2021/07/BasaltMaroonJuly21-44-min.jpg", "preview": False},
            {"url": "https://gowanderwild.com/wp-content/uploads/2024/07/Maroon-Bells-hike-Aspen-Colorado-20-533x800.jpg", "preview": False},
            {"url": "https://www.gosnowmass.com/wp-content/uploads/2018/06/bells-950x570.jpg", "preview": False}
        ],
        3: [
            {"url": "https://mlwd5nbv8uri.i.optimole.com/cb:1OS-.5fb6c/w:1500/h:996/q:mauto/f:best/ig:avif/https://www.pikes-peak.com/wp-content/uploads/Winter-in-Colorado-Springs-PP-GOGjpg.jpg", "preview": True},
            {"url": "https://www.visitcos.com/imager/files_idss_com/C88/22e6cce8-a032-4ea3-bf83-d7c666b5e468_e45adf5f6bc0c5c2a30a39868f44eab6.jpg", "preview": False},
            {"url": "https://www.visitcos.com/imager/cmsimages/4683480/barr-trail-2-WB_91852798b59be8b28fc00edfe4aec23a.jpg", "preview": False},
            {"url": "https://www.americansouthwest.net/colorado/photographs450/pikes-summit.jpg", "preview": False}
        ],
        4: [
            {"url": "https://media-cdn.tripadvisor.com/media/photo-c/2560x500/04/c9/32/9e/twin-lakes.jpg", "preview": True},
            {"url": "https://adventuresofaplusk.com/wp-content/uploads/2021/12/DSC05800-1024x682.jpg", "preview": False},
            {"url": "https://www.impulse4adventure.com/wp-content/uploads/2018/10/IMG_0400-e1556576204768-1024x767.jpg", "preview": False},
            {"url": "https://www.rickcrandall.net/wp-content/uploads/images/56_MtElbert-Hike-1_03.jpg", "preview": False}
        ],
        5: [
            {"url": "https://cdn.5280.com/2020/08/Hanging_Lake_Focqus_LLC_Getty_Images-960x720.jpg", "preview": True},
            {"url": "https://www.coloradofunguide.com/wp-content/uploads/Pic-4.png", "preview": False},
            {"url": "https://media-cdn.tripadvisor.com/media/photo-s/05/d4/2c/1c/hanging-lake-trail.jpg", "preview": False},
            {"url": "https://www.glenwoodcolorado.com/wp-content/uploads/elementor/thumbs/boy-scout-trail-entrance-osbodzrkuisr6dpj2wa5jjmkqv4cmqpzzsjbrl6xzw.jpg", "preview": False}
        ],
        6: [
            {"url": "https://kctrvlr.com/wp-content/uploads/2020/10/Humboldt-Peak-Colorado-14er-HP-KCTRVLR-WEB-12-1024x683.jpg", "preview": True},
            {"url": "https://images.squarespace-cdn.com/content/v1/5f39599f0dd69335c3379b81/1718651e-a367-4910-bf37-ccf9315a0f23/Phantom+Terrace+Venable-Commanche+Trail.jpg", "preview": False},
            {"url": "https://files.cdn-files-a.com/uploads/3315788/2000_5ea205c12ccc0.jpg", "preview": False},
            {"url": "https://kctrvlr.com/wp-content/uploads/2020/10/Humboldt-Peak-Colorado-14er-HP-KCTRVLR-WEB-17-1024x683.jpg", "preview": False}
        ],
        7: [
            {"url": "https://res.cloudinary.com/simpleview/image/upload/v1617669390/clients/granbyco/RMNP_Hiking_Trails_aca975bb-2e53-44ee-9675-8f90957a4102.jpg", "preview": True},
            {"url": "https://media.cntraveler.com/photos/647fa4126702ed16faad7365/3:2/w_5391,h_3594,c_limit/Iconic%20Rocky%20Mountain%20National%20Park%20Hikes_joe-dudeck-xqkGRlF7Uqg-unsplash.jpg", "preview": False},
            {"url": "https://i0.wp.com/www.parkchasers.com/wp-content/uploads/2015/12/IMG_4460.jpg", "preview": False},
            {"url": "https://www.rockymtnresorts.com/wp-content/uploads/2018/12/Rocky_Mountain_National_Park_trails_950_634.jpg", "preview": False}
        ],
        8: [
            {"url": "https://followtiffsjourney.com/wp-content/uploads/2019/09/IMG_8829.jpg", "preview": True},
            {"url": "https://images.squarespace-cdn.com/content/v1/6226f62738f4f73d2b353e79/dcc00763-a7a7-4d23-b914-06b53bfd28ac/IMG_8563.JPG", "preview": False},
            {"url": "https://assets.site-static.com/userFiles/1621/image/ice-lake-trail.jpg", "preview": False},
            {"url": "https://mtntownmagazine.com/wp-content/uploads/2012/09/ice-lake-silverton-co.jpg", "preview": False}
        ],
        9: [
            {"url": "https://cdn.actionhub.com/wp-content/uploads/2021/06/bg-south-boulder-peak-colorado.jpg", "preview": True},
            {"url": "https://hikinginboulder.com/wp-content/uploads/2018/01/green-mountain-from-fern-canyon-trail-1024x682.jpg", "preview": False},
            {"url": "https://hikingincolorado.com/wp-content/uploads/2018/01/bear-peak-summit-hike-via-fern-canyon-trail.jpg", "preview": False},
            {"url": "https://dayhikesneardenver.b-cdn.net/wp-content/uploads/2019/09/Bear-Peak-Hike-Near-Boulder-02-Homestead-Trail-Bridge.jpg", "preview": False}
        ],
        10: [
            {"url": "https://dayhikesneardenver.com/wp-content/uploads/2016/03/00-Sky-Pond-in-Rocky-Mountain-National-Park-bratman-creative-commons.jpg", "preview": True},
            {"url": "https://a.travel-assets.com/findyours-php/viewfinder/images/res70/226000/226979-Sky-Pond-Trail.jpg", "preview": False},
            {"url": "https://jennabraddock.com/wp-content/uploads/2024/07/sky-pond-trail-sign-edited-scaled.jpg", "preview": False},
            {"url": "https://raisinghikers.com/wp-content/uploads/2021/04/skypond.jpg", "preview": False}
        ],
        11: [
            {"url": "https://i.ytimg.com/vi/H1117RtJRe0/maxresdefault.jpg", "preview": True},
            {"url": "https://wetplanetwhitewater.com/wp-content/uploads/main_salmon_river_rafting_hero_2-1440x750.jpg", "preview": False},
            {"url": "https://assets.simpleviewinc.com/simpleview/image/upload/c_limit,q_75,w_1200/v1/crm/anchorage/2016-eagle-river-nature-deck1_303e00b9-5056-a36a-0a83d21dace42d27.jpg", "preview": False},
            {"url": "https://proraftingtours.com/wp-content/uploads/2019/02/main-salmon-river-rafting-idaho-activities-hiking.jpg", "preview": False}
        ],
        12: [
            {"url": "https://www.awanderlustadventure.com/wordpress/wp-content/uploads/2018/11/IMG_3333-2.jpg", "preview": True},
            {"url": "https://www.americanadventure.com/wp-content/uploads/2022/05/white-water-rafting-season-sunny-2-1024x683-1-1.jpg", "preview": False},
            {"url": "https://www.americanadventure.com/wp-content/uploads/2018/03/unique-honeymoon-ideas-rafting-768x512-1-1.jpg", "preview": False},
            {"url": "https://performancetours.com/wp-content/uploads/2024/04/s-7-6-2016-1024x680.jpg", "preview": False}
        ],
        13: [
            {"url": "https://www.uncovercolorado.com/wp-content/uploads/2014/04/Yampa-River-Rafting-Canyon-800x400.jpg", "preview": True},
            {"url": "https://media.oars.com/wp-content/uploads/2023/03/20231516/YAM-22-840x546.jpg", "preview": False},
            {"url": "https://mild2wildrafting.com/wp-content/uploads/2018/02/2.jpg", "preview": False},
            {"url": "https://th-thumbnailer.cdn-si-edu.com/ga3iL4VYhKR1-AOk4F2GpbmE0Hk=/fit-in/1200x0/https://tf-cmsv2-smithsonianmag-media.s3.amazonaws.com/filer/5e/57/5e579eba-23e8-45cb-b9aa-32670943e8c7/img_0221.jpg", "preview": False}
        ],
        14: [
            {"url": "https://cdn.outsideonline.com/wp-content/uploads/2019/07/10/dolores-river-sky_s.jpg", "preview": True},
            {"url": "https://www.coloradorafting.net/wp-content/uploads/2017/08/DSC_5325-1024x684.jpg", "preview": False},
            {"url": "https://www.uncovercolorado.com/wp-content/uploads/2020/07/dolores-river-rafting-snaggle-tooth-rapid-colorado2.jpg", "preview": False},
            {"url": "https://cdn.aorafting.com/images/kaweah/scenery.jpg", "preview": False}
        ],
        15: [
            {"url": "https://www.coloradorafting.net/wp-content/uploads/2017/07/AVA-Rafting-Buena-Vista-BROWNS-27-1024x683.jpg", "preview": True},
            {"url": "https://s40084.pcdn.co/wp-content/uploads/2023/07/BlueJune11-scaled.jpg", "preview": False},
            {"url": "https://www.planetware.com/wpimages/2020/08/montana-white-water-rafting-gallatin-river.jpg", "preview": False},
            {"url": "https://i.ytimg.com/vi/5FgdaBQNhig/maxresdefault.jpg", "preview": False}
        ],
        16: [
            {"url": "https://mtprinceton.com/wp-content/uploads/Buena-vista-salida-colorado-whitewater-rafting.jpg", "preview": True},
            {"url": "https://coloradoinfo.com/wp-content/uploads/2015/04/ColoradoRafting.jpg", "preview": False},
            {"url": "https://mtprinceton.com/wp-content/uploads/Buena-vista-salida-colorado-kayaking-arkansas-river.jpg", "preview": False},
            {"url": "https://images.squarespace-cdn.com/content/v1/5d7be41b5cb7d218f8c093c0/1568750955420-35VOQ5DSYFDPLJM7RHJ2/buena_vista_river_park-00004.jpg", "preview": False}
        ],
        17: [
            {"url": "https://gunnisonriverexpeditions.com/wp-content/uploads/2023/11/gunnison-river-expeditions-black-canyon.png", "preview": True},
            {"url": "https://www.inaraft.com/wp-content/uploads/2024/04/gunnison-river-rafting1.jpg", "preview": False},
            {"url": "https://gunnisonriverexpeditions.com/wp-content/uploads/2023/04/gunnison-gorge-rafting-683x1024.jpg", "preview": False},
            {"url": "https://www.americanrivers.org/wp-content/uploads/2022/12/Gunnison-River-Black-Canyon-credit-Alan-Cressler-header-1024x403.jpg", "preview": False}
        ],
        18: [
            {"url": "https://raftdefiance.com/wp-content/uploads/2024/08/Glenwood-Springs-Defiance-Raft-in-canyon.jpg", "preview": True},
            {"url": "https://www.riversandoceans.com/wp-content/uploads/2020/10/Full-Grand-Canyon-Motor-6429241-1024x795.jpg", "preview": False},
            {"url": "https://live.staticflickr.com/65535/49934338111_91c1915f21_c.jpg", "preview": False},
            {"url": "https://media.oars.com/wp-content/uploads/2022/11/21011455/canyonlands-hero.jpg", "preview": False}
        ],
        19: [
            {"url": "https://i.ytimg.com/vi/mWvxbImj7cE/sddefault.jpg", "preview": True},
            {"url": "https://blog.aorafting.com/wp-content/uploads/2023/10/sfa-scenery-ft.jpg", "preview": False},
            {"url": "https://blog.aorafting.com/wp-content/uploads/2024/03/tuolumne-river.jpg", "preview": False},
            {"url": "https://img2.fdfiles.info/upload/images/thumbs/2016/10/14/749w10000h1muser_99904_pic_1476462304_img_580106e0945b4.jpg", "preview": False}
        ],
        20: [
            {"url": "https://poudreheritage.org/wp-content/uploads/DJI_0415_LowRes_3899a1f4-cb75-4ebb-a12d-c9f66881e3b9.jpg", "preview": True},
            {"url": "https://www.coloradorafting.net/wp-content/uploads/2024/02/AVA-Rafting-Zipline-_-Blue-River-Rafting.mp4.00_00_13_00.Still004-768x432.png", "preview": False},
            {"url": "https://i.etsystatic.com/14261824/r/il/2d47e5/4273533611/il_1080xN.4273533611_88mo.jpg", "preview": False},
            {"url": "https://rms.memberclicks.net/assets/NRRD/FeaturedRiversPhotos/CacheLaPoudre.jpg", "preview": False}
        ],
        21: [
            {"url": "https://wereintherockies.com/wp-content/uploads/2023/12/bear-lake-road-bear-lake-in-late-fall-1024x768.jpg", "preview": True},
            {"url": "https://static.wixstatic.com/media/22d565_50497b1c72364b4a8722bee93eb93ee6~mv2_d_6598_4399_s_4_2.jpg/v1/fill/w_640,h_804,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/22d565_50497b1c72364b4a8722bee93eb93ee6~mv2_d_6598_4399_s_4_2.jpg", "preview": False},
            {"url": "https://hipcamp-res.cloudinary.com/f_auto,c_limit,w_1280,q_auto:eco/v1602264977/campground-photos/gcsqhtxixdopdd8u1itx.jpg", "preview": False},
            {"url": "https://photos.thedyrt.com/photo/543882/media/idaho-upper-payette-lake-dispersed_357311a4-aa7e-485c-89ec-df06722d7afb.jpg", "preview": False}
        ],
        22: [
            {"url": "https://photos.thedyrt.com/photo/647099/media/lakeview-twin-lakes_9f664fd6-6bf3-4883-bf10-93460d0b46dc.png", "preview": True},
            {"url": "https://lirp.cdn-website.com/59142d64/dms3rep/multi/opt/camoing-640w.jpg", "preview": False},
            {"url": "https://arkvalleyvoice.com/wp-content/uploads/2024/05/scott-goodwill-y8Ngwq34_Ak-unsplash-scaled.jpg", "preview": False},
            {"url": "https://hipcamp-res.cloudinary.com/f_auto,c_limit,w_1280,q_auto:eco/v1561827564/campground-photos/zoenv28haoykx7gphfth.jpg", "preview": False}
        ],
        23: [
            {"url": "https://coloradoinfo.com/wp-content/uploads/2022/12/13-mountain-towns-blog-estes-park.jpg", "preview": True},
            {"url": "https://www.campgroundviews.com/wp-content/uploads/2016/07/estes-park-campground-east-portal-01.jpg", "preview": False},
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Rocky_Mountain_National_Park_in_September_2011_-_Glacier_Gorge_from_Bear_Lake.JPG/1200px-Rocky_Mountain_National_Park_in_September_2011_-_Glacier_Gorge_from_Bear_Lake.JPG", "preview": False},
            {"url": "https://www.rv.com/wp-content/uploads/2020/12/Rocky-Mountains.jpg", "preview": False}
        ],
        24: [
            {"url": "https://darkskyoverland.com/wp-content/uploads/2023/11/great-sand-dunes-national-park-magnificent-dunes.jpg", "preview": True},
            {"url": "https://daytripnomad.com/wp-content/uploads/2024/02/GP-Great-Sand-Dunes-Ridge-1024x768.jpg", "preview": False},
            {"url": "https://www.rv.com/wp-content/uploads/2020/12/Sand-Dunes-5-NPS-1.jpg", "preview": False},
            {"url": "https://c1.staticflickr.com/5/4253/34940806782_a63cd17a73_z.jpg", "preview": False}
        ],
        25: [
            {"url": "https://blog.silverlight.store/wp-content/uploads/2023/08/ryan-milrad-RF-NWO82P-g-unsplash-1400x710-1.jpg", "preview": True},
            {"url": "https://images.squarespace-cdn.com/content/v1/5f39599f0dd69335c3379b81/1674849480386-ERNSTOAISBEBDC1YD05H/first+night+campsite+four+pass+loop.jpg", "preview": False},
            {"url": "https://images.silverlight.store//uploads/2023/08/david-rupert-qUQoCLLLAGc-unsplash-1200x800.jpg", "preview": False},
            {"url": "https://images.squarespace-cdn.com/content/v1/5f39599f0dd69335c3379b81/1674848883085-7UOW6K727MDS17ZHZAJC/views+from+mountain+four+pass+loop.jpg", "preview": False}
        ],
        26: [
            {"url": "https://i.ytimg.com/vi/Q7OW0hR-o0A/maxresdefault.jpg", "preview": True},
            {"url": "https://hipcamp-res.cloudinary.com/f_auto,c_limit,w_1280,q_auto:eco/v1722815729/campground-photos/xlig4taz64fwl80mtxxw.jpg", "preview": False},
            {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Dillonpin.JPG/640px-Dillonpin.JPG", "preview": False},
            {"url": "https://tmbtent.com/wp-content/uploads/2021/05/East-Elk-Creek-Group-Campground.jpg", "preview": False}
        ],
        27: [
            {"url": "https://ngazette.com/wp-content/uploads/2022/10/Outdoor-IMG_6156-1024x768.jpg", "preview": True},
            {"url": "https://cross-country-trips.com/sites/default/files/images/4k/110720_122541_4444.preview.jpg", "preview": False},
            {"url": "https://photos.thedyrt.com/photo/media/aspen-meadows-campground-golden-gate-state-park_a868652a-98a0-4669-bd6a-2958c3293204.jpg", "preview": False},
            {"url": "https://assets.simpleviewinc.com/simpleview/image/upload/c_fill,h_338,q_75,w_450/v1/clients/goldenco/IMG_1717_2_1469d1eb-f37f-4f5a-bff8-14703b9c756d.jpg", "preview": False}
        ],
        28: [
            {"url": "https://www.uncovercolorado.com/wp-content/uploads/2022/05/Chatfield-State-Park-Colorado-1600x800-1.jpg", "preview": True},
            {"url": "https://www.uncovercolorado.com/wp-content/uploads/2022/06/Chatfield-State-Park-Colorado.jpg", "preview": False},
            {"url": "https://hipcamp-res.cloudinary.com/f_auto,c_limit,w_1280,q_auto:eco/v1630296560/campground-photos/no7l9s6bi1qywjgmfmtp.jpg", "preview": False},
            {"url": "https://photos.thedyrt.com/photo/9998/photo/colorado-chatfield-state-park_e72324a2eb5b1b17c1e4221cddff0b23.jpg", "preview": False}
        ],
        29: [
            {"url": "https://photos.thedyrt.com/photo/638572/media/colorado-rifle-falls-state-park_eb8689ed-b897-449b-b1ef-42f92cabd4ea.jpg", "preview": True},
            {"url": "https://www.uncovercolorado.com/wp-content/uploads/2013/06/2012-08-03-Rocky-Mountain02b.jpg", "preview": False},
            {"url": "https://www.nps.gov/common/uploads/structured_data/ABA774AF-098D-A406-6C9EC4C886FE2B1B.jpg", "preview": False},
            {"url": "https://hipcamp-res.cloudinary.com/f_auto,c_limit,w_1280,q_auto:eco/v1496799829/campground-photos/q6j0gtuqmfeobgqle9za.jpg", "preview": False}
        ],
        30: [
            {"url": "https://darlatravels.com/wp-content/uploads/2021/10/DSCF5105.jpg", "preview": True},
            {"url": "https://res.cloudinary.com/simpleview/image/upload/v1534523992/clients/steamboat/camping_steamboat_springs_da4074e3-1e38-4037-b6fe-88c16be6ce01.jpg", "preview": False},
            {"url": "https://photos.thedyrt.com/photo/844410/media/colorado-steamboat-lake-state-park-sunrise-vista_0e2513b6-8576-4eee-9fca-4eb2938ca52e.jpg", "preview": False},
            {"url": "https://www.uncovercolorado.com/wp-content/uploads/2019/09/camping-near-steamboat-springs-sunrise-steamboat-lake-state-park-1600x800-1.jpg", "preview": False}
        ],
        31: [
            {"url": "https://cdn.climbing.com/wp-content/uploads/2018/09/dsc_0076-maiden-voyage_gn-web.jpg", "preview": True},
            {"url": "https://gripped.com/wp-content/uploads/2022/11/Flatirons-Climbing.jpg", "preview": False},
            {"url": "https://cdn.outsideonline.com/wp-content/uploads/2017/02/07/front-range-climbing_h-scaled.jpg", "preview": False},
            {"url": "https://hikebiketravel.com/wp-content/uploads/2012/06/Hike-between-the-Flatirons-in-Boulder-4.jpg", "preview": False}
        ],
        32: [
            {"url": "https://images.squarespace-cdn.com/content/v1/5e037b124b89f34b576a47fb/1577312965477-UV24QUOS5ZXZNRZFWL4N/Osiris-Route.jpg", "preview": True},
            {"url": "https://images.squarespace-cdn.com/content/v1/5e037b124b89f34b576a47fb/1577311508433-H1TSSY4TA3EFCX2OX3CJ/LumpyRidge.jpg", "preview": False},
            {"url": "https://i.pinimg.com/736x/b3/7a/47/b37a4783a45a2f5da9d2b44833f87138.jpg", "preview": False},
            {"url": "https://s3.us-west-1.amazonaws.com/mtnguide.net/2017/08/lumpy.3.jpg", "preview": False}
        ],
        33: [
            {"url": "https://themountainguides.com/wp-content/uploads/2015/03/863062FE-6505-4D6B-8FA4-C9748CCF8FC7-scaled.jpg", "preview": True},
            {"url": "https://themountainguides.com/wp-content/uploads/2015/03/eldorado-canyon-climb-2-990x660.jpg", "preview": False},
            {"url": "https://images.squarespace-cdn.com/content/v1/6047eb6caf3c4a6b10e9a529/c2ac3bcc-4b21-448e-bc61-4739bfd45825/IMG_2543.jpeg", "preview": False},
            {"url": "https://a-lodge.com/wp-content/uploads/2019/10/dblmajav01lmgefdb8ht.jpg", "preview": False}
        ],
        34: [
            {"url": "https://cdn.aarp.net/content/dam/aarpe/en/home/travel/vacation-ideas/outdoors/info-2023/black-canyon-of-the-gunnison/_jcr_content/root/container_main/container_body_main/container_travel_main_body/container_travel_body/container_body2/container_body_cf/body_two_cf_one/par6/articlecontentfragme/cfimage.coreimg.50.932.jpeg/content/dam/aarp/travel/national-parks/2023/09/1140-black-canyon-of-the-gunnison-national-park-overlook.jpg", "preview": True},
            {"url": "https://files.secure.website/wscfus/10637177/32304775/black-canyon-w604-o.jpg", "preview": False},
            {"url": "https://s3.us-west-1.amazonaws.com/mtnguide.net/2017/09/black.1.jpg", "preview": False},
            {"url": "https://www.nps.gov/blca/planyourvisit/images/05LisaLynch12608.jpg", "preview": False}
        ],
        35: [
            {"url": "https://assets.explore-share.com/trips/404662/cover/1647305186-rifleclimbingguidesinterview-sdn-061717-1.jpg", "preview": True},
            {"url": "https://images.squarespace-cdn.com/content/v1/61d48ff56ef0be4187705136/1d6c87df-d21f-4f73-8195-80ef9f796f21/rock-climbing-Rifle-background.jpg", "preview": False},
            {"url": "https://57hours.com/wp-content/uploads/2023/07/climbers-rifle-park-768x768.jpg", "preview": False},
            {"url": "https://www.uncovercolorado.com/wp-content/uploads/2020/04/Rifle-Mountain-Park-CO-1600x800-1-1536x768.jpeg", "preview": False}
        ],
        36: [
            {"url": "https://res.cloudinary.com/adrenalinecom/image/upload/f_auto,q_auto/v1557897123/adventures/eps_3864.jpg", "preview": True},
            {"url": "https://media.tacdn.com/media/attractions-splice-spp-674x446/07/0a/e0/ef.jpg", "preview": False},
            {"url": "https://cdn.recreation.gov/public/2022/08/29/21/39/10087438_a44202a9-9b9b-44c5-a7c1-fc59a9e23af5_1440.jpg", "preview": False},
            {"url": "https://www.coloradoviaferrata.com/wp-content/uploads/2024/06/6905-1024x683.jpg", "preview": False}
        ],
        37: [
            {"url": "https://www.broadmooroutfitters.com/wp-content/uploads/2022/09/sean-benesh-VnmbcgAfL3Q-unsplash-1-1000x565.jpg", "preview": True},
            {"url": "https://i.pinimg.com/736x/2a/bd/ce/2abdce1399e6b5496e5fc9fac36e8d93.jpg", "preview": False},
            {"url": "https://gardenofthegodscolorado.com/wp-content/uploads/garden-of-the-gods-rock-climbing-fb.jpg", "preview": False},
            {"url": "https://gardenofgods.com/wp-content/uploads/gallery-2.jpg", "preview": False}
        ],
        38: [
            {"url": "https://www.skyblueoverland.com/wp-content/uploads/Tenmile-2-1-1024x768.jpg", "preview": True},
            {"url": "https://www.swarpa.net/~danforth/photos/tenmile/dragon.jpg", "preview": False},
            {"url": "https://swiftmedia.s3.amazonaws.com/mountain.swiftcom.com/images/sites/2/2016/12/22181238/TenmileTraverse-sdn-090316-1-11.jpg", "preview": False},
            {"url": "https://www.skyblueoverland.com/wp-content/uploads/20200714-Tenmile-24-225x300.jpg", "preview": False}
        ],
        39: [
            {"url": "https://www.climbingolder.net/~statcy.bender/photos/Cactus_Spiney_Gym.jpg", "preview": True},
            {"url": "https://files.secure.website/wscfus/10637177/30091385/shelf-road-rock-climbing-w1920-o.jpg", "preview": False},
            {"url": "https://www.climbingolder.net/~statcy.bender/photos/Shelf_Menses_Prow.jpg", "preview": False},
            {"url": "https://www.foxintheforest.net/wp-content/uploads/2020/12/rock_climbing_Meg_Atteberry-8.jpg", "preview": False}
        ],
        40: [
            {"url": "https://images-sp.summitpost.org/tr:e-sharpen,e-contrast-1,fit-max,q-60,w-500/842759.jpg", "preview": True},
            {"url": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEidj_7EcIfqZl3z32ZVPFIkbvnSlr7X75gmFTZBs660zifpSaBGq1TXgjwIN4s3a1JF-wMm-IeUs1T7FykkRAaXuethkpx5BCvY3Q-Cvzsuj75JFBoffo-TcXq-AoHI4yYAhod5Du5WUhYJ/s1600/Access+Fund2+002.JPG", "preview": False},
            {"url": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjepjymTbYjayuLC17K6LB4HzcJReJijdjDKx0jgz4f2Df7s0W_m52MNcfzIGRgaWTupyM4DOC_41Ei5yXzx_1kzCwO8Uun4mF_VeVCfpDdtk_vkt-6d9M9LbiEVmonllWO4sSM1-cMT6SB/s1600/dovercourt_bri_3.jpg", "preview": False},
            {"url": "https://gjadventures.com/wp-content/uploads/2022/02/Climber-at-Unaweep-92021-e1644437584532-500x675.jpg", "preview": False}
        ],
        41: [
            {"url": "https://www.blacktieskis.com/vail-bc/wp-content/uploads/sites/16/2023/06/vl-vail2.jpg", "preview": True},
            {"url": "https://krystal93.com/wp-content/uploads/2024/12/vail2.png", "preview": False},
            {"url": "https://cdn.outsideonline.com/wp-content/uploads/2022/02/breckenridge-ski-resort-crowd_s.jpg", "preview": False},
            {"url": "https://www.vailresorts.com/wp-content/uploads/2023/09/20140313_BR_Affleck_004.jpeg", "preview": False}
        ],
        42: [
            {"url": "https://res.cloudinary.com/simpleview/image/upload/v1547486754/clients/steamboat/main_street_alpenglow_8aeff516-9d63-4665-936b-14f87bf0ad0c.jpg", "preview": True},
            {"url": "https://s3.amazonaws.com/fathom_media/photos/steamboat-springs-night-skiing.jpg.1200x800_q85_crop.jpg", "preview": False},
            {"url": "https://www.sswsc.org/images/pages/BashorComplex.png", "preview": False},
            {"url": "https://res.cloudinary.com/simpleview/image/upload/v1547486788/clients/steamboat/night_skiing_winter_glow_e3143419-c482-4086-a201-3edd3c42301f.jpg", "preview": False}
        ],
        43: [
            {"url": "https://www.travelandleisure.com/thmb/TsosqDFfNw8UhptjD4sXiEBctUo=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/main-st-teluride-TELURIDE1221-36894a82cd774058b1fd259707cccff5.jpg", "preview": True},
            {"url": "https://snowbrains.com/wp-content/uploads/2024/10/7.-Main-Street-__-THUMBNAIL.jpeg", "preview": False},
            {"url": "https://cdn.shortpixel.ai/spai/q_glossy+ret_img+to_auto/www.slopemagazine.com/wp-content/uploads/Snow/telluride-ski-resort-accommodation.jpg", "preview": False},
            {"url": "https://cdn.shortpixel.ai/spai/q_glossy+ret_img+to_auto/www.slopemagazine.com/wp-content/uploads/Snow/telluride-ski-review-resort.jpg", "preview": False}
        ],
        44: [
            {"url": "https://a.travel-assets.com/findyours-php/viewfinder/images/res70/138000/138113-Aspen-Mountain.jpg", "preview": True},
            {"url": "https://npr.brightspotcdn.com/c4/35/a9521b544665bd1ca7526b119022/btx08598.jpg", "preview": False},
            {"url": "https://swiftmedia.s3.amazonaws.com/mountain.swiftcom.com/images/sites/5/2024/12/23180043/Ajax_credit-Jordan-Curet-635x1024.jpg", "preview": False},
            {"url": "https://coloradoinfo.com/wp-content/uploads/2024/02/Aspen-Highlands-Map-scaled.jpg", "preview": False}
        ],
        45: [
            {"url": "https://www.blacktieskis.com/breckenridge/wp-content/uploads/sites/6/2023/06/bk-breckenridge5.jpg", "preview": True},
            {"url": "https://s40084.pcdn.co/wp-content/uploads/2023/03/gondola.jpg", "preview": False},
            {"url": "https://thetourguy.com/wp-content/uploads/2021/08/Where-to-Stay-In-Breckenridge-1440-x-675-900x420.jpg", "preview": False},
            {"url": "https://cdn0-pms.skisolutions.com/media/images/property/150/51_625_md.jpeg", "preview": False}
        ],
        46: [
            {"url": "https://www.coloradoluxeliving.com/wp-content/uploads/2020/07/keystone.jpg", "preview": True},
            {"url": "https://www.snowmagazine.com/images/ski-resorts/usa/keystone-piste.jpg", "preview": False},
            {"url": "https://digital.snow.com/api/imgproxy/fetch?url=unsafe/resize:fit:600:450/dpr:1/plain/https://images.vrinntopia.com/photos//50016713/50016713-8-d6cbf8c0.png", "preview": False},
            {"url": "https://a.travel-assets.com/findyours-php/viewfinder/images/res70/147000/147250-Keystone-Ski-Resort.jpg", "preview": False}
        ],
        47: [
            {"url": "https://snowbrains.com/wp-content/uploads/2022/01/IMG_3194.jpg", "preview": True},
            {"url": "https://www.trulia.com/pictures/thumbs_5/zillowstatic/fp/9dde955edf693e3fbf5f3db69379269a-full.jpg", "preview": False},
            {"url": "https://cdn.craft.cloud/101e4579-0e19-46b6-95c6-7eb27e4afc41/assets/uploads/Smugglers-Notch-VT.jpg", "preview": False},
            {"url": "https://snowbrains.com/wp-content/uploads/2020/07/woodward-snowboard.png", "preview": False}
        ],
        48: [
            {"url": "https://res.cloudinary.com/dm05gsblo/images/w_2560,h_1707/v1638365365/Austin_Travels/Winter-Park-Resort_Contrib-Winter-Park-Resort/Winter-Park-Resort_Contrib-Winter-Park-Resort.jpg", "preview": True},
            {"url": "https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/blogs/27908/images/3rkQJeEuQ4uX55CFOnuO_Winter_Park.jpeg", "preview": False},
            {"url": "https://cdn.outsideonline.com/wp-content/uploads/migrated-images_parent/migrated-images_48/WCMDEV_152971_skiing-7.jpg", "preview": False},
            {"url": "https://upload.wikimedia.org/wikipedia/commons/f/f6/Winter_Park_Base_Area.JPG", "preview": False}
        ],
        49: [
            {"url": "https://upload.wikimedia.org/wikipedia/commons/3/36/Mount_crested_butte_1988.jpg", "preview": True},
            {"url": "https://www.trulia.com/pictures/thumbs_5/zillowstatic/fp/d2da19087f59da99add7818264e2b1ec-full.jpg", "preview": False},
            {"url": "https://upload.terabitz.com/u/cbmp/agentsite/979541/agth_1680034960_81753.jpeg", "preview": False},
            {"url": "https://images.squarespace-cdn.com/content/v1/6529d6e106d20e4a3caaff93/4a6aec04-30e0-44d6-b3e5-d61f5e8b6d6a/FlippingOut_RLloyd-1.jpg", "preview": False}
        ],
        50: [
            {"url": "https://wolfcreekski.com/wp-content/uploads/2022/09/NAX0004a-scaled.jpg", "preview": True},
            {"url": "https://localfreshies.com/wp-content/uploads/2024/11/Erika-bowl-drop_2290435.jpg", "preview": False},
            {"url": "https://wolfcreekski.com/wp-content/uploads/2024/03/WolfCreekTrailMap_2023_Low.jpg", "preview": False},
            {"url": "https://wolfcreekski.com/wp-content/uploads/2022/08/10-Snow-Cat-Trails-11.jpg-scaled.jpg", "preview": False}
        ],
        51: [
            {"url": "https://cdn.thumpertalk.com/uploads/monthly_2020_08/vlcsnap-2020-08-16-17h10m14s983.png.32c57cb733e39e1156233bee66cfe1c3.png", "preview": True},
            {"url": "https://www.riderplanet-usa.com/atv/trails/photo/cec7271049b544d5975fcf90110fc022.jpg", "preview": False},
            {"url": "https://www.riderplanet-usa.com/atv/trails/photo/f3795952a2db425a8031fbe6ed933ac4.jpg", "preview": False},
            {"url": "https://pikespeakoutdoors.org/wp-content/uploads/2024/02/IMG_0473-1-768x1024.jpg", "preview": False}
        ],
        52: [
            {"url": "https://assets.simpleviewinc.com/simpleview/image/upload/c_fill,h_699,q_75,w_1080/v1/clients/grandjunctionco/685b1d09cf165a16770a7206d73483033e1783d9a8526dd46182d2068b881ba5_45a2a73b-dd04-4c26-b775-fdcfe5c8a2b7.jpg", "preview": True},
            {"url": "https://assets.simpleviewinc.com/simpleview/image/upload/c_limit,h_1200,q_75,w_1200/v1/clients/grandjunctionco/55515132_825149491157544_2346326765355401216_o_8fe8f70c-b9dc-4514-adf7-ce16d27d67fc.jpg", "preview": False},
            {"url": "https://res.cloudinary.com/simpleview/image/upload/v1690924250/clients/grandjunctionco/_DSC1126_copy_743bbf14-8d9c-4de9-936f-ba2c95d0595c.jpg", "preview": False},
            {"url": "https://www.coloradodirectory.com/grand-mesa-adventures/images/grand-mesa-atv-lg.jpg", "preview": False}
        ],
        53: [
            {"url": "https://travelcrestedbutte.com/wp-content/uploads/2019/04/DSC_6930-Pano.jpg", "preview": True},
            {"url": "https://www.exploretaylorpark.com/wp-content/uploads/2023/05/multitrack.jpg", "preview": False},
            {"url": "https://travelcrestedbutte.com/wp-content/uploads/2019/06/Taylor-Park-Trading.jpeg", "preview": False},
            {"url": "https://coloradoadventurerentals.com/wp-content/uploads/2014/12/gunnison-atv-rentals-3.jpg", "preview": False}
        ],
        54: [
            {"url": "https://ouraymountainadventures.com/wp-content/uploads/2023/09/Ouray-Mountain-Adventures-Jeep-Rentals-2023.jpg", "preview": True},
            {"url": "https://ouraymountainadventures.com/wp-content/uploads/2023/11/About-Ouray-Mountain-Adventures-jeep-utv-ebike-rentals-2023.jpg", "preview": False},
            {"url": "https://bucketlistjourney.net/wp-content/uploads/2018/11/Colorado-Silverton.png", "preview": False},
            {"url": "https://images.squarespace-cdn.com/content/v1/5fc8231f834b454a3d061624/b819debe-9429-47c2-b54d-6a631e148d53/AdobeStock_428905184.jpeg", "preview": False}
        ],
        55: [
            {"url": "https://gunnisoncrestedbutte.com/wp-content/uploads/DSC_7801-copy.jpg", "preview": True},
            {"url": "https://www.uncovercolorado.com/wp-content/uploads/2022/03/mounatin-bike-trail-401-gunnison-national-forest-colorado.jpg", "preview": False},
            {"url": "https://images.squarespace-cdn.com/content/v1/5fc8231f834b454a3d061624/c2019486-1684-4108-a6f8-c2b867f6f29e/Screenshot+2023-08-15+at+11.03.56+AM.png", "preview": False},
            {"url": "https://womanrider.com/wp-content/uploads/2023/11/C.-Jane-Taylor-Gunnison-Colorado-to-Hovenweep-National-Monument-13.jpg", "preview": False}
        ],
        56: [
            {"url": "https://images.singletracks.com/blog/wp-content/uploads/2018/07/wasatch-alskoj.jpg", "preview": True},
            {"url": "https://images.squarespace-cdn.com/content/v1/638e49a6cb1825380dec58e5/1695079678061-5CJXHPYNYGQHGHN3YLNN/Screenshot%2B2023-09-18%2B170749.jpg", "preview": False},
            {"url": "https://i.ytimg.com/vi/GYeDSWmehLA/maxresdefault.jpg", "preview": False},
            {"url": "https://dcasler.com/wp-content/uploads/2014/04/IMG_0098adj_lunch_stop_for_web.jpg", "preview": False}
        ],
        57: [
            {"url": "https://hipcamp-res.cloudinary.com/f_auto,c_limit,w_1280,q_auto:eco/v1433543209/t2swy3yue10ypujeurzc.jpg", "preview": True},
            {"url": "https://glenwoodadventure.com/app/uploads/2016/04/%C2%A9BrittneyKMorgan-20140722-CanonEOSRebelT3i-00050.jpg", "preview": False},
            {"url": "https://cdn-assets.alltrails.com/static-map/production/area/10117937/parks-us-colorado-white-river-national-forest-10117937-20201216110311000000000-1200x630-3-41608152280.jpg", "preview": False},
            {"url": "https://media.9news.com/assets/KUSA/images/380a97f2-4cd6-49bd-9d39-7dfb79b2bbfd/380a97f2-4cd6-49bd-9d39-7dfb79b2bbfd_1140x641.jpg", "preview": False}
        ],
        58: [
            {"url": "https://images.singletracks.com/blog/wp-content/uploads/2017/10/21273426_10155820587818447_8898616313208885487_o.jpg", "preview": True},
            {"url": "https://pikespeakoutdoors.org/wp-content/uploads/2024/02/13294_phantom_road_aka_phantom_creek-1440-1024x576.jpg", "preview": False},
            {"url": "https://blog-assets.thedyrt.com/uploads/2021/12/COVER-colorado-spruce-grove-Aidan-1024x485.jpg", "preview": False},
            {"url": "https://www.coloradodirectory.com/maps/images/Monument-Woodland-Park-Jeep-ATV-Trails-Map.jpg", "preview": False}
        ],
        59: [
            {"url": "https://i.ytimg.com/vi/4EJXCOHVwMw/maxresdefault.jpg", "preview": True},
            {"url": "https://visitriograndecounty.com/wp-content/uploads/2021/08/Aspens-30Mile3.jpg", "preview": False},
            {"url": "https://www.fs.usda.gov/Internet/FSE_MEDIA/stelprdb5187475.jpg", "preview": False},
            {"url": "https://visitriograndecounty.com/wp-content/uploads/2022/05/7029244_Marcela-S.jpg", "preview": False}
        ],
        60: [
            {"url": "https://gunnisoncrestedbutte.com/wp-content/uploads/DSC_7801-copy.jpg", "preview": True},
            {"url": "https://res.cloudinary.com/simpleview/image/upload/v1550521935/clients/montroseco/Document_51__8d7f6c1a-63ab-4587-81c7-d9344e4b9c11.jpg", "preview": False},
            {"url": "https://www.destinationwest.org/uploads/1/3/0/7/130743495/931jdl17_orig.jpg", "preview": False},
            {"url": "https://i.redd.it/52geyp7fpcv61.jpg", "preview": False}
        ],

        
    }

    images_to_add = []
    for location_id, images_info in location_images_data.items():
        for img_info in images_info:
            images_to_add.append(LocationImage(
                locationId=location_id,
                url=img_info["url"],
                preview=img_info["preview"]
            ))

    db.session.add_all(images_to_add)
    db.session.commit()

def undo_location_images():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.location_images RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM location_images"))
    
    db.session.commit()
