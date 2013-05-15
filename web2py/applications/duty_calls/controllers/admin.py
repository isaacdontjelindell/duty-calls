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
        
        elif action == "update":
            update_info(location_name)  # TODO need to implement this!

        # redirect back to the location interface after changing stuff
        # This is equivalent to "raise HTTP(301, 'Redirect')"
        redirect(URL('locations', args=(location_name)))
        

    return dict(locations=locations, users=users)


@auth.requires_membership("ahd")
def users():
    args = request.args
    
    q = db.auth_user.id > 0
    grid = SQLFORM.smartgrid(db.auth_user, 
                             csv=False, 
                             deletable=False, 
                             linked_tables= ['locations'],
                             fields = [db.auth_user.first_name,
                                       db.auth_user.last_name,
                                       db.auth_user.phone,
                                       db.auth_user.email,
                                       db.auth_user.location_names,
                                       db.auth_user.sms_on
                                      ],
                             headers = { 'auth_user.location_names':'Locations'}
                            )
    
    users = db(q).select()

    q = db.locations.id > 0
    locations = db(q).select()
    return dict(grid=grid)



def addLocationProcess(form):
    twilio_number_id = form.vars.twilio_number_id
    cal_URL = form.vars.calendar_url
    #try:
    #    util.getTwilioNumber(twilio_number)
    #except TwilioRestException:
    if(cal_URL != "test"):
        form.errors.twilio_number_id = "Invalid number_ID"

    #TODO define test cases to check valid calender URL and Twilio ID
    
@auth.requires_membership("admin")
def addLocation():
    form = SQLFORM(db.locations, 
        fields = ['location_name', 'calendar_url','twilio_number_id','is_res_life','fail_name','fail_number'],
        labels = {'location_name':'Location Name','calendar_url':'Google Calender URL (iCal)','fail_name':"Default Forward Location",'fail_number':'Default Forward Number'},
        col3 = {'is_res_life':'Interprets all day events as 7pm to 8am Duty Events','twilio_number_id':'Obtained from Twilio number URL'})
    if form.process(onvalidation=addLocationProcess).accepted:
        response.flash = "Location Added"
        redirect(URL('locations'))
    elif form.errors:
        response.flash = "Errors!"
    return dict(form=form)
