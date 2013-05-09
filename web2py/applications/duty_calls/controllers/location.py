import util

def display():
    args = request.args
    location_name = args[0]  # TODO add error handling

    # TODO: I'm using like() instead of == to provide case-insensitive lookup.
    # PostgreSQL may behave differently than MySQL and SQLite
    location = util.getLocationFromName(location_name)

    twilio_number_str = util.getTwilioNumber(location)

    #TESTING PRINT STATEMENTS
    print(twilio_number_str)
    print ("CurrentForwarding: ", util.getCurrentForwardingDestinations(location))
    print("Current on Cal: ", util.getCurrentPersonsOnDuty(location))

    return dict(location=location)
