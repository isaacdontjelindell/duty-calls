import util

def test():
    args = request.args
    location_name = args[0]

    location = util.getLocationFromName(location_name)
    #print "On duty: " + str(util.getCurrentPersonsOnDuty(location))
    #print "current destinations: " + str(util.getCurrentForwardingDestinations(location))
    #util.update(location)
    #print "updated destinations: " + str(util.getCurrentForwardingDestinations(location))
    #print ""
    #util.logError("Test message", location)


def all():
    q = db.locations.id > 0
    locations = db(q).select()

    for loc in locations:
        print "Updating " + loc.location_name
        print ""
        util.update(loc)
