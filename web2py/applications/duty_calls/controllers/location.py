import util

def display():
    args = request.args
    location_name = args[0]
    db = current.db

    # TODO: I'm using like() instead of == to provide case-insensitive lookup.
    # PostgreSQL may behave differently than MySQL and SQLite
    location = util.getLocationFromName(location_name)
    onDuty = util.getCurrentPersonsOnDuty(location)
    onDuty_string = ""
    for name in onDuty:
        onDuty_string = onDuty_string + name + ", "

    contacts = None

    twilio_number_str = util.getTwilioNumber(location)

    #TESTING PRINT STATEMENTS
    print(twilio_number_str)
    print ("CurrentForwarding: ", util.getCurrentForwardingDestinations(location))
    print("Current on Cal: ", util.getCurrentPersonsOnDuty(location))

    return dict(location=location, twilio_number_str=twilio_number_str, onDuty=onDuty)

    