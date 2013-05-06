# this reloads modules (util.py) without having to restart
# the web2py server.
# This should be turned off in production as it will be a 
# significant performance hit.
from gluon.custom_import import track_changes; track_changes(True)


db.define_table('locations',
    Field('location_name','string', unique=True),
    Field('calendar_url','string'),
    Field('twilio_number_id','string'),
    Field('is_res_life','boolean'),
)

# sample contact dict 
#{"Austen Smith": "319-123-4567", "Isaac DL": "612-978-3683"}
