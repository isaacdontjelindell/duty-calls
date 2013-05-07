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

        start_date = vevent.get('DTSTART').dt #.strftime("%Y-%m-%d")  # .dt is a datetime or date
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
                        return ["ResLife Office"]

        if start_date <= curr_date <= end_date: # if this event is right now
                title = str(vevent.get('SUMMARY')) # this will be the title of the event (hopefully  name)
                on_duty_names.append(title)

    if len(on_duty_names) == 0:
        on_duty_names.append("ResLife Office")
    return on_duty_names

def getCurrentForwardingDestinations(location): 
    #Returns a tuple with the first element a list of simulring numbers
    #curently on call and the second item the fail number string
    current_numbers = []

    split_url = twilio_client.phone_numbers.get(location['twilio_number_id']).voice_url.split("=")
    for part in split_url:
        if str(part).__contains__("-"):
            current_numbers.append(str(part.split("&")[0]))
    fail_number = current_numbers.pop(current_numbers.__len__() - 1)
    return (current_numbers, fail_number)

def update(location):
    ''' checks for changes to the person on duty and makes necessary changes to forwarding info '''
    curr_forwarding_destinations,failNum = getCurrentForwardingDestinations(location)
        
    new_forwarding_destinations = []

    for name in getCurrentPersonsOnDuty(location):
        new_forwarding_dest = getPhoneNumberForName(name.strip())
        new_forwarding_destinations.append(new_forwarding_dest)

    if not curr_forwarding_destinations == new_forwarding_destinations:
        self.updateForwardingDestinations(new_forwarding_destinations, location['fail_number'])

def updateForwardingDestinations(location):
    voice_URL = "http://twimlets.com/simulring?"
    increment_num = 0;

    old_destination_numbers = getCurrentForwardingDestinations(location)

    for number in new_destination_numbers:
        voice_URL = voice_URL + "PhoneNumbers%5B" + str(increment_num) + "%5D=" + number + "&"
        increment_num += 1

        if not number in old_destination_numbers and self.info['send_sms'] and not number == self.info['contact_list']['ResLife Office']:
            to_number = "+1" + number.replace("-", "")  # must be in format +12316851234
            message = self.twilio_client.sms.messages.create(to=to_number, 
                                                             from_=self.forwarding_number_obj.friendly_name,
                                                             body="You are now on duty.")

    voice_URL = voice_URL + "Message=Forwarded%20Call&" + "FailUrl=http://twimlets.com/forward?PhoneNumber=" + failNumber
    self.forwarding_number_obj.update(voice_url=voice_URL)

def getPhoneNumberForName(name):
    db = current.db

    q = db.auth_user.nicknames.contains(name)
    names = db(q).select()
 
    if len(names) == 0:
        logError("Didn't find any user named " + name,
                 level="fatal")
    elif len(names) > 1:
        logError("Found multiple users with the name " + name,
                 level="warn")
    else: # should just be 1 name
        return names[0].phone

def getLocationFromName(location_name):
    db = current.db

    q = db.locations.location_name.like(location_name)
    locs = db(q).select()

    if len(locs) == 0:
        logError("Could not find location : " + location_name, 
                 level="fatal")
    elif len(locs) > 1:
        logError("Multiple locations matching location name " + location_name + ". Using first one found.",
                 level="warn")
    else: # should be just 1 location
        return locs[0]

def logError(error, level="warning"):
    # TODO this should notify someone about errors passed to it
    raise HTTP(500, error)
