import util

def display():
    args = request.args
    location_name =  args[0]

    # TODO: I'm using like() instead of == to provide case-insensitive lookup.
    # PostgreSQL may behave differently than MySQL and SQLite
    q = db.locations.location_name.like(location_name)
    db_rows = db(q).select()
    loc = db_rows[0]
    
    twilio_number_str = util.getTwilioNumber(loc['twilio_number_id'])

    #TESTING PRINT STATEMENTS
    print(twilio_number_str)
    print ("CurrentForwarding: " ,util.getCurrentForwardingDestinations(loc['twilio_number_id']))
    print("Current on Cal: ", util.getCurrentPersonsOnDuty(loc['calendar_url'],loc['is_res_life']))

    return dict(rows=db_rows)