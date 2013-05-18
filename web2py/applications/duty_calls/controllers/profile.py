def update():
    form = SQLFORM(db.users,
                   fields = ['first_name',
                             'last_name',
                             'phone',
                             'sms_on',
                             'nicknames'],
                   submit_button = "Update your profile")

    if form.process(onvalidation=processUserProfileUpdateForm).accepted:
        response.flash = "Profile saved."
        # TODO add a redirect here
    else:
        response.flash = "Errors!"
        # TODO add a redirect here

    return dict(form=form)

def index():
    q = db.users.uid_ref == auth.user.id
    user = db(q).select()

    return dict(user=user)

def processUserProfileUpdateForm(form):
    
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
