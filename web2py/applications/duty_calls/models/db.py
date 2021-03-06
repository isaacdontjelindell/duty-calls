# -*- coding: utf-8 -*-
from gluon import current
import os
import json

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])

else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))


## This table will hold the Twilio API access stuff.
## Needs to be manually populated with the auth token and account SID.
db.define_table('auth_tokens',
    Field('name','string'),
    Field('token_value','string')
)

## populate the auth_tokens table with dummy values so that GAE creates it ##
q = db.auth_tokens.name == 'TWILIO_ACCOUNT_SID'
sid = db(q).select()
if len(sid) == 0:
    db.auth_tokens.insert(name='TWILIO_ACCOUNT_SID', token_value='XXXXXXXXXXXXXXXXXXXXX')
    db.auth_tokens.insert(name='TWILIO_AUTH_TOKEN', token_value='XXXXXXXXXXXXXXXXXXXXX')


## if on GAE, get the auth tokens from the DB. Otherwise get them from private/conf.json
if not request.env.web2py_runtime_gae:
    conf_path = os.path.join(request.folder,'private','conf.json')
    with open(conf_path,'r') as f:
        conf = json.load(f)
        os.environ['TWILIO_AUTH_TOKEN'] = conf['TWILIO_AUTH_TOKEN']
        os.environ['TWILIO_ACCOUNT_SID'] = conf['TWILIO_ACCOUNT_SID']
else:
    row = db(db.auth_tokens.name == 'TWILIO_AUTH_TOKEN').select()[0]
    at = row['token_value']

    row = db(db.auth_tokens.name == 'TWILIO_ACCOUNT_SID').select()[0]
    acs = row['token_value']

    os.environ['TWILIO_AUTH_TOKEN'] = at
    os.environ['TWILIO_ACCOUNT_SID'] = acs


## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] 
#if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()


## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

auth.settings.actions_disabled.append('change_password')
auth.settings.actions_disabled.append('request_reset_password')
auth.settings.actions_disabled.append('profile')

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
#from gluon.contrib.login_methods.rpx_account import use_janrain
#use_janrain(auth, filename='private/janrain.key')
if request.env.web2py_runtime_gae:
    from gluon.contrib.login_methods.gae_google_account import GaeGoogleAccount
    auth.settings.login_form = GaeGoogleAccount()
else:
    from gluon.contrib.login_methods.rpx_account import use_janrain
    use_janrain(auth, filename='private/janrain.key')


## so that the db object can be accessed from modules 
current.db = db

## redirect to a controller that checks if this is the first time login
def redirect_login(form):
    redirect(URL('profile','check_user'))
        
auth.settings.login_onaccept = redirect_login
auth.settings.register_onaccept = redirect_login


## create the admin and ra groups if they don't already exist
ra = db(db.auth_group.role == 'ra').select()
if len(ra) < 1:
    db.auth_group.insert(role='ra', description='resident assistant')

admin = db(db.auth_group.role == 'admin').select()
if len(admin) < 1:
    db.auth_group.insert(role='admin', description='administrator')


## create an initial admin user if there isn't already one
if not db().select(db.auth_user.ALL).first():
    user_id = db.auth_user.insert(first_name = 'System',
                                  last_name = 'Administrator',
                                  email = 'root@null.com',
                                  password = db.auth_user.password.validate('password')[0]
                                 )
    admin_id = db(db.auth_group.role == 'admin').select()[0].id
    ra_id = db(db.auth_group.role == 'ra').select()[0].id
    db.auth_membership.insert(user_id=user_id, group_id=admin_id)
    db.auth_membership.insert(user_id=user_id, group_id=ra_id)


#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
