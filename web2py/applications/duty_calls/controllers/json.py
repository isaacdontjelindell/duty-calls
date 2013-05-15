import util

def users():
    args = request.args
    if len(args) > 0:
        location = util.getLocationFromName(args[0])
        q = db.auth_user.locations.contains(location.id)
        
    else: 
        q = db.auth_user.id > 0
    user_rows = db(q).select()

    users = {'aaData':[]}

    for row in user_rows:
        user = [row.first_name + " " + row.last_name, row.phone, row.email, row.sms_on, row.locations, row.id]
        users['aaData'].append(user)
    return dict(users)

