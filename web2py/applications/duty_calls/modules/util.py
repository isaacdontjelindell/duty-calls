from gluon import *
from twilio.rest import TwilioRestClient
from icalendar import Calendar
import datetime
from dateutil import tz
import urllib
import os
import json

request = current.request
conf_path = os.path.join(request.folder,'private','conf.json')
with open(conf_path,'r') as f:
    conf = json.load(f)
    os.environ['TWILIO_AUTH_TOKEN'] = conf['TWILIO_AUTH_TOKEN']
    os.environ['TWILIO_ACCOUNT_SID'] = conf['TWILIO_ACCOUNT_SID']

twilio_client = TwilioRestClient()

def getTwilioNumber(twilio_number_id):
    return twilio_client.phone_numbers.get(twilio_number_id).friendly_name

def getCurrentPersonsOnDuty(calendar_url, is_res_life):
    on_duty_names = []

    ics = urllib.urlopen(calendar_url).read()
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

                if is_res_life == True:
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

def getCurrentForwardingDestinations(twilio_number_id): #Returns a tuple with the first element a list of simulring numbers
    #curently on call and the second item the fail number string
    current_numbers = []

    split_url = twilio_client.phone_numbers.get(twilio_number_id).voice_url.split("=")
    for part in split_url:
        if str(part).__contains__("-"):
            current_numbers.append(str(part.split("&")[0]))
    fail_number = current_numbers.pop(current_numbers.__len__() - 1)
    return (current_numbers, fail_number)

