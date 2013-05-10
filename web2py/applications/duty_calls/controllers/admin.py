import util

@auth.requires_membership("admin")
def locations():
    args = request.args

    ## if there is a location specified (e.g. ...locations/brandt) ##
    if len(args) > 0: 
        location_name = args[0]
        location = util.getLocationFromName(location_name)
        locations = [location] # return a list so we can use the same view
    
    ## no location specified; show all locations ##
    ## TODO first ##
    else: 
        q = db.locations.id > 0
        locations = db(q).select()

    return dict(locations=locations)


@auth.requires_membership("ahd")
def users():
    args = request.args
        
    ## if there is a location specified to show users from (e.g. users/brandt) ##
    if len(args) > 0:
        location_name = args[0]
        location = util.getLocationFromName(location_name)
        q = (db.auth_user.locations.contains(location.id))
    
    ## no location specified; show all users ##
    else:
        location = None
        q = db.auth_user.id > 0
    
    users = db(q).select()
    return dict(users=users, location=location)


