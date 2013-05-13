import util

def users():
    q = db.auth_user.id > 0
    user_rows = db(q).select()

    users = {'aaData':[]}

    for row in user_rows:
        user = [row.first_name + " " + row.last_name, row.phone, row.email, row.id]
        users['aaData'].append(user)
    return dict(users)


def loc_users():
    args = request.args
    loc_name = args[0]
    
    location = util.getLocationFromName(loc_name)

    q = db.auth_user.locations.contains(location.id)
    user_rows = db(q).select()

    users = {'aaData':[]}

    for row in user_rows:
        user = [row.first_name + " " + row.last_name, row.phone, row.email, row.id]
        users['aaData'].append(user)

    return dict(users)



