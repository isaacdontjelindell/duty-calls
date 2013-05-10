import util

def all():
    q = db.locations.id > 0
    locations = db(q).select()

    for loc in locations:
        print "Updating " + loc.location_name
        print ""
        util.update(loc)
        

def location():
    args = request.args
    location_name = args[0]
    
    location = util.getLocationFromName(location_name)

    print "Updating " + loc.location_name
    print ""
    util.update(location)

def test():
    nicknames = db(db.auth_user.id == 3).select()[0]['nicknames']
    #nicknames = ['Austen Smith']
    nicknames.append('HELLO')
    db(db.auth_user.id == 3).update(nicknames=nicknames)

