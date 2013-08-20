import util

def all():
    q = db.locations.id > 0
    locations = db(q).select()

    for loc in locations:
        util.update(loc)
    
    db.commit()

def location():
    args = request.args
    location_name = args[0]
    
    location = util.getLocationFromName(location_name)

    print "Updating " + loc.location_name
    print ""
    util.update(location)

