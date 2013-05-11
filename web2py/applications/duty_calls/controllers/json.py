def users():
    q = db.auth_user.id > 0
    user_rows = db(q).select()

    users = {'aaData':[]}

    for row in user_rows:
        user = [row.first_name + " " + row.last_name, row.phone, row.email, row.id]
        users['aaData'].append(user)
    return dict(users)
