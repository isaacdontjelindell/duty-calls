import util

def test():
    args = request.args
    location_name = args[0]

    location = util.getLocationFromName(location_name)

    print "On duty: " + str(util.getCurrentPersonsOnDuty(location))
    print "current destinations: " + str(util.getCurrentForwardingDestinations(location))
    util.update(location)

    print "updated destinations: " + str(util.getCurrentForwardingDestinations(location))
    print ""
    print ""
    print util.logError("Test message")
