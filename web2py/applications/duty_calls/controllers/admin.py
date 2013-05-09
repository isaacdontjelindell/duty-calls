import util

@auth.requires_membership("admin")
def display():
    ''' displays all locations in the database '''
    q = db.locations.id > 0
    locations = db(q).select()
     
    for loc in locations:
        loc['twilio_number'] = util.getTwilioNumber(loc)

    return dict(locations=locations)
        

def location():
    args = request.args
    location_name = args[0]  # TODO add error handling

    location = util.getLocationFromName(location_name)

    location['twilio_number'] = util.getTwilioNumber(location)
    location['on_duty'] = util.getCurrentPersonsOnDuty(location)
