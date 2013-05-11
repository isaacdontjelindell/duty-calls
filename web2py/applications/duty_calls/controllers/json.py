def users():
    q = db.auth_user.id > 0
    user_rows = db(q).select()

    users = {}

    for row in user_rows:
        users[row.id] = {}

        users[row.id]['name'] = row['first_name'] + " " + row['last_name']
        users[row.id]['phone'] = row['phone']
        users[row.id]['email'] = row['email']

    return dict(users=users)
