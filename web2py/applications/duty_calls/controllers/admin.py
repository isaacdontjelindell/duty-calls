import util

@auth.requires_membership("admin")
def display():
    env = request.env
    
    q = db.locations.id > 0
    locations = db(q).select()

    for loc in locations:
        duty = util.getCurrentPersonsOnDuty(loc.calendar_url, loc.is_res_life)
        print "On duty: " +  str(duty)

        print "Forwarding number: " + util.getTwilioNumber(loc['twilio_number_id'])

        forwarding_dests = util.getCurrentForwardingDestinations(loc['twilio_number_id'])
        print "Current destinations: " + str(forwarding_dests)
            
    return dict(locations=locations)

