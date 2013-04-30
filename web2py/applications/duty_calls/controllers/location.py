def display():
    args = request.args
    location_id = args[0]
    q = db.locations.id == location_id
    result_set = db(q)

    return dict(rows=result_set.select())
