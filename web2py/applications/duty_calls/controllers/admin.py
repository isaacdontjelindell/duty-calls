import util

@auth.requires_login()
def display():
    env = request.env
    
    q = db.locations.id > 0
    locations = db(q).select()

    for loc in locations:
        duty = util.getCurrentPersonsOnDuty(loc.calendar_url, loc.is_res_life)
        print "On duty: " +  str(duty)
        loc['twilio_number_str'] = util.getTwilioNumber(loc['twilio_number_id'])

    return dict(locations=locations)
        
