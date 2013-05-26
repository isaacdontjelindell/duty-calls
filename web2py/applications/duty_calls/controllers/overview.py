@auth.requires_membership("ra")
def index():
    response.title = "Locations"
    locs = db(db.locations.id > 0).select()
    return dict(ret=locs)
