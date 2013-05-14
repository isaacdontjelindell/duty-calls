from gluon import *
from twilio.rest import TwilioRestClient
from icalendar import Calendar
import datetime
from dateutil import tz
import urllib
import os
import json

request = current.request
twilio_client = TwilioRestClient()

def getTwilioNumber(location):
    return twilio_client.phone_numbers.get(location['twilio_number_id']).friendly_name

def getCurrentPersonsOnDuty(location):
    on_duty_names = []
    
    try:
        ics = urllib.urlopen(location['calendar_url']).read()
    except:
        logError("Unable to read calendar URL", level="fatal")

    ical = Calendar.from_ical(ics)

    for vevent in ical.subcomponents:
        if vevent.name != "VEVENT":  # if it's not an event, ignore it
            continue

        start_date = vevent.get('DTSTART').dt # .dt is a datetime or date
        end_date = vevent.get('DTEND').dt

        if isinstance(start_date, datetime.datetime):
                # it's a datetime.datetime object (includes time)
                start_date = start_date.astimezone(tz.tzlocal()) # convert to local time
                end_date = end_date.astimezone(tz.tzlocal())
                curr_date = datetime.datetime.now(tz.tzlocal())

        elif isinstance(start_date, datetime.date):
                # it's a datetime.date object (does not include time)
                curr_date = datetime.date.today()
                end_date = end_date - datetime.timedelta(days=1)

                if location['is_res_life'] == True:
                    now_time = datetime.datetime.now().time()
                    #now_time = datetime.time(1,0,0)
                    #now_time = datetime.time(19,20,0)

                    seven_pm_time = datetime.time(19,0,0)
                    eight_am_time = datetime.time(8,0,0)
                    #print now_time
                    if seven_pm_time <= now_time <= datetime.time(23,59,59):
                        #print "Between 7 and midnight"
                        pass
                    elif datetime.time(0,0,0) <= now_time <= eight_am_time:
                        #print "Between midnight and 8am"
                        curr_date = curr_date - datetime.timedelta(days=1)
                    else:
                        #print "Not between 7pm and 8am"
                        return location["fail_name"]

        if start_date <= curr_date <= end_date: # if this event is right now
                # this will be the title of the event (hopefully a person's name)
                title = str(vevent.get('SUMMARY')) 
                on_duty_names.append(title)

    if len(on_duty_names) == 0:
        on_duty_names.append(location['fail_name'])
    return on_duty_names

def getCurrentForwardingDestinations(location):
    ''' return all forwarding destination numbers, not including the fail number '''
    current_numbers = []

    split_url = twilio_client.phone_numbers.get(location['twilio_number_id']).voice_url.split("&")
    for part in split_url:
        if "PhoneNumbers" in part:
            temp = part.split("=")
            for s in temp:
                if "-" in s:
                    current_numbers.append(s.encode('utf8'))
    return current_numbers


def update(location):
    ''' checks for changes to the person on duty and makes necessary changes to forwarding info '''
    db = current.db

    ## get numbers for each name on calendar ##
    old_forwarding_destinations = getCurrentForwardingDestinations(location)
    new_forwarding_users = []
    new_forwarding_user_names = []

    new_persons_on_duty = getCurrentPersonsOnDuty(location)
    for name in new_persons_on_duty:
        if name == location['fail_name']:
            new_forwarding_users.append({'phone':location['fail_number'],'sms_on':False})
            
            # this will be stored in db: current_on_duty
            new_forwarding_user_names.append(name)
        else:
            try:
                user_row = getUserDataFromName(name.strip())
            except KeyError, e:
                logError(e.message, location)
            new_forwarding_users.append(user_row)

            # save the users names in a list to update the database with; stored in current_on_duty
            new_forwarding_user_names.append(user_row['nicknames'][0])
    
    ## update twilio forwarding stuff if necessary ##
    voice_URL = "http://twimlets.com/simulring?"
    increment_num = 0

    for user in new_forwarding_users:

        # build the TwiML URL from each phone number
        voice_URL += "PhoneNumbers%5B" + str(increment_num) + "%5D=" + user['phone'] + "&"
        increment_num += 1
        
        # only send SMS notification if they are newly on duty, and only if they want SMS notifications
        if not user['phone'] in old_forwarding_destinations:  
            if user['sms_on']:
                to_number = "+1" + user['phone'].replace("-", "") # must be in format +12316851234
                message = twilio_client.sms.messages.create(to=to_number, 
                                                            from_=getTwilioNumber(location),
                                                            body="You are now on duty.")

    voice_URL += "Message=Forwarded%20Call&" + "FailUrl=http://twimlets.com/forward?PhoneNumber=" + location['fail_number']
    twilio_client.phone_numbers.get(location['twilio_number_id']).update(voice_url=voice_URL)

    # update the database with the changed info
    new_forwarding_destinations = getCurrentForwardingDestinations(location)
    db(db.locations.id == location['id']).update(current_on_duty=new_forwarding_user_names)
    db(db.locations.id == location['id']).update(current_forwarding_destinations=new_forwarding_destinations)


def getUserDataFromName(name):
    db = current.db
    q = db.auth_user.nicknames.contains(name)
    rows = db(q).select()
    
    if len(rows) == 0:
        #logError("Didn't find any user named " + name,
        #         level="fatal")
        raise KeyError("Didn't find any user named " + name)
    elif len(rows) > 1:
        #logError("Found multiple users with the name " + name,
        #         level="warn")
        raise KeyError("Found multiple users with the name " + name)
    else: # should just be 1 name
        return rows[0]

def getLocationFromName(location_name):
    db = current.db

    #q = db.locations.location_name.like(location_name)
    q = like_query(location_name, db.locations.location_name)
    locs = db(q).select()

    if len(locs) == 0:
        logError("Could not find location : " + location_name, 
                 level="fatal")
    elif len(locs) > 1:
        logError("Multiple locations matching location name " + 
                        location_name + ". Using first one found.")
    else: # should be just 1 location
        return locs[0]

def like_query(term, field):
    """Receives term and field to query, then returns the query to be performed
       This is a nasty hack needed because GAE BigTable doesn't support .like()
    """
    queryStart = term.decode('utf-8')
    queryEnd = queryStart+"\xEF\xBF\xBD".decode('utf-8')
    query =((field>=queryStart) & (field<=queryEnd))
    return query
 


def getUsersForLocation(location_row):
    db = current.db

    q = db.auth_user.locations.contains(location_row.id)
    users = db(q).select()
    return users

def logError(error, location=None, level="warn"):
    if not location is None:
        db = current.db
        
        # find the AHD group ID. Could hardcode this, but makes it more
        # portable to search for it.
        q = db.auth_group.role == "ahd"
        ahd_group_id = db(q).select()[0].id

        # find all users who have ahd_group_id and are associated with location
        q = ((db.auth_membership.group_id == ahd_group_id) & 
            (db.auth_membership.user_id == db.auth_user.id) & 
            (db.auth_user.locations.contains(location['id'])))
        ahd_list = db(q).select()
            
        #print ahd_list[0]['auth_user']['first_name']
        # TODO SMS/email AHD's and maybe admin's too
        raise HTTP(500, error)
    else:
        raise HTTP(500, error)


