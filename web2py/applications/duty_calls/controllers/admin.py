import util

@auth.requires_membership("admin")
def display():
    env = request.env
    
    q = db.locations.id > 0
    locations = db(q).select()

    for loc in locations:
        duty = util.getCurrentPersonsOnDuty(loc)
        print "On duty: " +  str(duty)

        print "Forwarding number: " + util.getTwilioNumber(loc)

        forwarding_dests = util.getCurrentForwardingDestinations(loc)
        print "Current destinations: " + str(forwarding_dests)
            
    return dict(locations=locations)

