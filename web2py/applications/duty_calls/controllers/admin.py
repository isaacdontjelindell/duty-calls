import util

@auth.requires_membership("admin")
def locations():
    ## Show information about location_name ##
    def show_location(location_name):
        location = util.getLocationFromName(location_name)
        response.title = location_name
        response.subtitle = location.twilio_number
    
        form = crud.update(db.locations, location.id, readonly=True, deletable=False,
                         fields = ['current_on_duty',
                                   'current_forwarding_destinations',
                                   'fail_name',
                                   'fail_number',
                                   'is_res_life',
                                   'calendar_url',
                                   'twilio_number_id'],
                         headers = {"current_on_duty":"Currently On Duty",
                                    "calendar_url":"Duty Calendar URL"}
                        )

        return form
        
    ## Update information for location_name ##
    def update_location(location_name):
        response.title = location_name
        location = util.getLocationFromName(location_name)
        
        form = crud.update(db.locations, location.id,
                           fields = ['twilio_number_id',
                                     'calendar_url',
                                     'is_res_life',
                                     'fail_name',
                                     'fail_number'],
                           ondelete = redirect_to_locations,
                           next = URL('locations',args=(location.location_name))
                          )

        return form

    ## Show a list of all locations in the database ##
    def show_all_locations():
        response.title = "Locations"
        locs = db(db.locations.id > 0).select()
        return locs

    ## redirect to /duty_calls/admin/locations ##
    def redirect_to_locations(id):
        redirect(URL('locations'))


### DISPATCH ###
    args = request.args
    action = ''
    location_name = ''

    if len(args) == 0:
        # show all locations
        action = 'show_all_locations'
        ret = show_all_locations()

    elif len(args) == 1:
        # show location arg[0]
        action = 'show_location'
        location_name = args[0]
        ret = show_location(location_name)

    elif len(args) > 1:
        location_name = args[0]
        action = args[1]

        # /%location_name%/add
        if action == "add":
            addUser(location_name)

        # /%location_name%/remove
        elif action == "remove":
            removeUser(location_name)
        
        # /%location_name%/update
        elif action == "update":
            action = 'update_location'
            ret = update_location(location_name)  

        # redirect back to the location interface after changing stuff
        # This is equivalent to "raise HTTP(301, 'Redirect')"
        #redirect(URL('locations', args=(location_name)))
        

    return dict(ret=ret, action=action, location_name=location_name)


###############################################################################

@auth.requires_membership("ahd","admin")
def add_location():
    response.title = "Add Location"
    form = crud.create(db.locations,
                       next = URL('locations'),
                       fields = ['location_name',
                                 'calendar_url',
                                 'twilio_number_id',
                                 'is_res_life',
                                 'fail_name',
                                 'fail_number']
                      ) 
    return dict(ret=form)

###############################################################################

@auth.requires_membership("ahd","admin")
def users():
    response.title = "All Users"
    form = crud.select(db.users, "id>0",
                       fields = ['first_name',
                                 'last_name',
                                 'phone',
                                 'location_names',
                                 'nicknames',
                                 'sms_on']
                      )
    
    return dict(ret=form)


###############################################################################

def removeLocation():
    ## remove the location
    post_vars = request.post_vars
    location_ids = post_vars['remove_ids']
    if not location_ids:
        return

    for location_id in location_ids:
        del db.locations[location_id]
        redirect(URL('/duty_calls/admin/locations'))

###############################################################################

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

###############################################################################

def processAddLocationForm(form):
    twilio_number_id = form.vars.twilio_number_id
    cal_Url = form.vars.calendar_url

    if(not util.validTwilioNumber(twilio_number_id)):
        form.errors.twilio_number_id = "Invalid  Twilio Number ID"
    elif(not util.validCalUrl(cal_Url)):
        form.errors.calendar_url = "Invalid Calendar URL"
    
