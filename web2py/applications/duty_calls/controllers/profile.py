def update():
    response.title = "Update your profile"

    auth_user_id = auth.user.id
    q = db.users.id == auth_user_id
    user = db(q).select()
    if len(user) > 0:
        user = user[0]
        form = crud.update(db.users, user,
                           onvalidation=process_create_user_profile_form,
                           fields = ['first_name',
                                     'last_name',
                                     'phone',
                                     'sms_on',
                                     'nicknames']
                          )
    else:
        form = crud.create(db.users,
                           onvalidation=process_create_user_profile_form,
                           fields = ['first_name',
                                     'last_name',
                                     'phone',
                                     'sms_on',
                                     'nicknames']
                          )

    return dict(ret=form)

def index():
    q = db.users.uid_ref == auth.user.id
    user = db(q).select()

    return dict(user=user)

def check_user():
    eventLogin = db(db.auth_event.user_id == auth.user.id).select()
    
    print "Uid: " + str(auth.user.id)
    print "Number of auth events: " + str(len(eventLogin))
    print ""

    if len(eventLogin) == 1:
        session.flash= 'This is the first time you have logged into DutyCalls, please fill in your profile.'
        redirect(URL('profile','update'))
    else:
        session.flash = "Seen you before."
        redirect(URL('admin','locations'))

    return dict()

def process_create_user_profile_form(form):
    # make sure the nicknames list at least contains the nickname
    # Firstname Lastname
    default_nickname = form.vars.first_name + " " + form.vars.last_name
    nicknames = form.vars.nicknames

    if not default_nickname in nicknames:
        if isinstance(nicknames, list):
            nicknames.append(default_nickname)
        else:
            nicknames = [nicknames, default_nickname]
    form.vars.nicknames = nicknames

    # associate this user row with the auth_user row
    auth_uid = auth.user.id
    form.vars.uid_ref = auth_uid
