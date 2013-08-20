def update():
    response.title = "Update your profile"

    auth_user_id = auth.user.id
    q = db.users.uid_ref == auth_user_id
    user = db(q).select()
    if len(user) > 0:
        user = user[0]
        form = crud.update(db.users, user,
                           deletable=False,
                           onvalidation=process_create_user_profile_form,
                           next=URL('profile','check_user'),
                           fields = ['first_name',
                                     'last_name',
                                     'phone',
                                     'sms_on',
                                     'nicknames']
                          )
    else:
        form = crud.create(db.users,
                           onvalidation=process_create_user_profile_form,
                           next=URL('profile','check_user'),
                           fields = ['first_name',
                                     'last_name',
                                     'phone',
                                     'sms_on',
                                     'nicknames']
                          )
        db.auth_event.insert(time_stamp=request.now,
                             client_ip='0.0.0.0',
                             user_id=auth.user.id,
                             origin='auth',
                             description='Users table entry created')
        
    return dict(ret=form)

@auth.requires_login()
def check_user():
    eventLogin = db(db.auth_event.user_id == auth.user.id).select()
    
    admin_group_id = db(db.auth_group.role == 'admin').select()[0].id
    #ra_group_id = db(db.auth_group.role == 'ra').select()[0].id

    if len(eventLogin) < 3:
        session.flash = 'This is the first time you have logged into DutyCalls, please fill in your profile.'
        redirect(URL('profile','update'))
    if admin_group_id in auth.user_groups:
        redirect(URL('admin','locations'))
    else:
        redirect(URL('overview','index'))

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

    # put the new user in the RA group by default
    q = db.auth_group.role == 'ra'
    ra_group_id = db(q).select()[0].id

    auth.add_membership(ra_group_id, auth_uid)
