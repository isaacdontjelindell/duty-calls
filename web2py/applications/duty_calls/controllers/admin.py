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
    
    def update_info(location_name):
        post_vars = request.post_vars
        fail_name = post_vars['fail_name']
        fail_num = post_vars['fail_num']
        forwarding_id = post_vars['forwarding_id']
        calendar_url = post_vars['calendar_url']

        if 'is_res_life' in post_vars:
            is_res_life = True
        else:
            is_res_life = False

        location = util.getLocationFromName(location_name)
        
        location.fail_name = fail_name
        location.fail_number = fail_num
        location.is_res_life = is_res_life
        location.twilio_number_id = forwarding_id
        location.calendar_url = calendar_url
        location.update_record() # persist the changes in the DB

    def removeUser(location_name):
        ## remove the user ids from the POST from location_name ##
        post_vars = request.post_vars
        remove_user_ids = post_vars['remove_ids']
        if not remove_user_ids:
            return

        location_id = util.getLocationFromName(location_name).id
        for remove_user_id in remove_user_ids:
            user = db(db.users.id == remove_user_id).select()[0]

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
            user = db(db.users.id == add_user_id).select()[0]
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
        
        elif action == "update":
            update_info(location_name)  # TODO need to implement this!

        # redirect back to the location interface after changing stuff
        # This is equivalent to "raise HTTP(301, 'Redirect')"
        redirect(URL('locations', args=(location_name)))
        

    return dict(locations=locations, users=users)


@auth.requires_membership("ahd","admin")
def users():
    args = request.args

    grid = SQLFORM.smartgrid(db.users, 
                             csv=False, 
                             fields = [db.users.first_name,
                                       db.users.last_name,
                                       db.users.nicknames,
                                       db.users.phone,
                                       db.users.location_names,
                                       db.users.sms_on,
                                      ],
                             headers = { 'users.location_names':'Locations'},
                             onvalidation=lambda form:processUserUpdateForm(form)
                            )
    
    return dict(grid=grid)


def processUserUpdateForm(form):
    ## force the nicknames list to always have at least "first_name + ' ' + last_name"
    nicknames = form.vars.nicknames
    default_nickname = form.vars.first_name + " " + form.vars.last_name
    if not default_nickname in nicknames:
        if isinstance(nicknames, list):
            nicknames.append(default_nickname)
        else:
            nicknames = [nicknames, default_nickname]
    form.vars.nicknames = nicknames


def addLocationProcess(form):
    twilio_number_id = form.vars.twilio_number_id
    cal_Url = form.vars.calendar_url

    if(not util.validTwilioNumber(twilio_number_id)):
        form.errors.twilio_number_id = "Invalid  Twilio Number ID"
    elif(not util.validCalUrl(cal_Url)):
        form.errors.calendar_url = "Invalid Calendar URL"
    
@auth.requires_membership("admin")
def addLocation():
    form = SQLFORM(db.locations, 
        fields = ['location_name', 'calendar_url','twilio_number_id','is_res_life','fail_name','fail_number'],
        labels = {'location_name':'Location Name','calendar_url':'Google Calender URL (iCal)','fail_name':"Default Forward Location",'fail_number':'Default Forward Number'},
        col3 = {'is_res_life':'Interprets all day events as 7pm to 8am Duty Events','twilio_number_id':'Obtained from Twilio number URL'},
        submit_button = 'Add Location')
    if form.process(onvalidation=addLocationProcess).accepted:
        response.flash = "Location Added"
        redirect(URL('locations'))
    elif form.errors:
        response.flash = "Errors!"
    return dict(form=form)

def removeLocation():
    ## remove the location
    post_vars = request.post_vars
    location_ids = post_vars['remove_ids']
    if not location_ids:
        return

    for location_id in location_ids:
        del db.locations[location_id]
        redirect(URL('/duty_calls/admin/locations'))
