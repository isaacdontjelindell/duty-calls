import util

@auth.requires_membership("admin")
def locations():
    
    def specific_location(location_name):
        ## if there is a location specified (e.g. ...locations/brandt) ##
        location_name = args[0]
        location = util.getLocationFromName(location_name)
        locations = [location] # return a list so we can use the same view
        users = util.getUsersForLocation(location)
        return (locations, users)
    
    def all_locations():
        ## no location specified; show all locations ##
        q = db.locations.id > 0
        locations = db(q).select()
        return locations
    
    def removeUser(location_name):
        ## remove the user ids from the POST from location_name ##
        post_vars = request.post_vars
        remove_user_ids = post_vars['remove_ids']
        if not remove_user_ids:
            return

        location_id = util.getLocationFromName(location_name).id
        for remove_user_id in remove_user_ids:
            user = db(db.auth_user.id == remove_user_id).select()[0]

            # get the list of locations the user is currently associated with
            user_locs = user.locations
            
            # remove this location from the user's locations list
            user_locs = user_locs.remove(long(location_id)) 
            user.update_record(locations=user_locs)
    
    def addUser(location_name):
        post_vars = request.post_vars
        add_user_ids = post_vars['add_ids'] # user ID's to remove from location
        if not add_user_ids:
            return

        location_id = util.getLocationFromName(location_name).id
        for add_user_id in add_user_ids:
            user = db(db.auth_user.id == add_user_id).select()[0]
            # get the list of locatitons the user is currently associated with
            user_locs = user.locations
            
            # don't put duplicate location references in the DB
            if not long(location_id) in user_locs:
                # add this location to the user's locations list
                user_locs.append(long(location_id))
                user.update_record(locations=user_locs)


    locations = []
    users = []

    args = request.args
    if len(args) == 0:
        locations = all_locations()

    elif len(args) == 1:
        locations, users = specific_location(args[0])

    elif len(args) > 1:
        location_name = args[0]
        action = args[1]

        # /%location_name%/add
        if action == "add":
            addUser(location_name)

        # /%location_name%/remove
        elif action == "remove":
            removeUser(location_name)
            
        # redirect back to the location interface after remove user
        # This is equivalent to "raise HTTP(301, 'Redirect')"
        redirect(URL('locations', args=(location_name)))
        

    return dict(locations=locations, users=users)


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

def addLocation():
    
    return dict()
