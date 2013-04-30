def display():
    env = request.env
    
    q = db.locations.id > 0
    result_set = db(q)

    return dict(rows=result_set.select())
        
