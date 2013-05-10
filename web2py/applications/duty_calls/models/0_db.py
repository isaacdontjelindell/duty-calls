import os
import json

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

