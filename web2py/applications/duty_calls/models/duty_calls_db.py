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


db.define_table('users',
    Field('uid_ref', 'reference auth_user'),
    Field('first_name', 'string'),
    Field('last_name','string'),
    Field('phone','string'),
    Field('locations','list:reference locations'),
    Field('location_names','list:string', compute=lambda r:getLocationNames(r)),
    Field('sms_on', 'boolean', default=False),
    Field('nicknames','list:string')
)

def getLocationNames(row):
    names = []
    if row.locations:
        for lid in row.locations:
            q = db.locations.id == lid
            loc_name = db(q).select()[0].location_name
            names.append(loc_name)

    return names

