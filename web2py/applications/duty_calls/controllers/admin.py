import util

@auth.requires_membership("admin")
def locations():
    args = request.args

    ## if there is a location specified (e.g. ...location/brandt) ##
    if len(args) > 0: 
        location_name = args[0]
        location = util.getLocationFromName(location_name)
        locations = [location] # return a list so we can use the same view
    
    ## no location specified; show all locations ##
    else: 
        q = db.locations.id > 0
        locations = db(q).select()

    return dict(locations=locations)

