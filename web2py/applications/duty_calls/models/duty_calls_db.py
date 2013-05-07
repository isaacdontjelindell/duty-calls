import os
import json

# this reloads modules (util.py) without having to restart
# the web2py server.
# This should be turned off in production as it will be a 
# significant performance hit.
from gluon.custom_import import track_changes; track_changes(True)

db.define_table('auth_tokens',
    Field('name','string'),
    Field('token_value','string')
)

db.define_table('locations',
    Field('location_name','string', unique=True),
    Field('calendar_url','string'),
    Field('twilio_number_id','string'),
    Field('is_res_life','boolean'),
    Field('fail_number','string')
)

if not request.env.web2py_runtime_gae:
    conf_path = os.path.join(request.folder,'private','conf.json')
    with open(conf_path,'r') as f:
        conf = json.load(f)
        os.environ['TWILIO_AUTH_TOKEN'] = conf['TWILIO_AUTH_TOKEN']
        os.environ['TWILIO_ACCOUNT_SID'] = conf['TWILIO_ACCOUNT_SID']
else:
    q = db.auth_tokens.name == 'TWILIO_AUTH_TOKEN'
    row = db(q).select()[0]
    at = row['token_value']

    q = db.auth_tokens.name == 'TWILIO_ACCOUNT_SID'
    row = db(q).select()[0]
    acs = row['token_value']

    os.environ['TWILIO_AUTH_TOKEN'] = at
    os.environ['TWILIO_ACCOUNT_SID'] = acs

# sample contact dict 
#{"Austen Smith": "319-123-4567", "Isaac DL": "612-978-3683"}
