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

    #TODO make sure all location names are stored as all lower case

    q = db.auth_user.locations.contains(location.id)
    contacts = db(q).select()

    #TODO get ahd id dynamically

    q = db.auth_group.role == "ahd"
    ahd_group_id = db(q).select()[0].id

    q = ((db.auth_membership.group_id == ahd_group_id) & 
        (db.auth_membership.user_id == db.auth_user.id) & 
        (db.auth_user.locations.contains(location['id'])))
    ahd_list = db(q).select()

    ahd_string = ""
    for row in ahd_list:
        ahd_string = ahd_string + row.auth_user.first_name + " " + row.auth_user.last_name + ", "

    print("CONTACTS: ")

    for row in contacts:
        print(row.first_name)

    twilio_number_str = util.getTwilioNumber(location)

    #TESTING PRINT STATEMENTS
    print(twilio_number_str)
    print ("CurrentForwarding: ", util.getCurrentForwardingDestinations(location))
    print("Current on Cal: ", util.getCurrentPersonsOnDuty(location))

    return dict(location=location, twilio_number_str=twilio_number_str, onDuty=onDuty, ahd_string = ahd_string)

    