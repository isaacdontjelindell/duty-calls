import os
import json
import util

# this reloads modules (util.py) without having to restart
# the web2py server.
# TODO This should be turned off in production as it will be a 
# significant performance hit.
from gluon.custom_import import track_changes; track_changes(True)

db.define_table('locations',
    Field('location_name','string', unique=True),
    Field('calendar_url','string'),
    Field('twilio_number_id','string'),
    Field('twilio_number','string', compute=lambda r: util.getTwilioNumber(r)),
    Field('is_res_life','boolean'),
    Field('fail_name','string'),
    Field('fail_number','string'),
    Field('current_on_duty','list:string', default=""),
    Field('current_forwarding_destinations','list:string', default="")
)
