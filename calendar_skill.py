from pathlib import Path
from ics import Calendar, Event
import os
import yaml
from datetime import datetime
from dateutil.relativedelta import *
import pytz
#from yaml import loader

calendar_filename = 'myfile.ics'
calendar_datafile = 'myfile.yml'

class Calendar_skill():
    c = Calendar()

    def __init__(self):
        print("")
        print("*"*50)
        print("Calendar Skill Loaded")
        print("*"*50)
    
    def add_event(self, begin:str, name:str, description:str=None)-> bool:
        " adds an event to the calendar"
        e = Event()
        e.name = name
        e.begin = begin
        e.description = description
        try:
            self.c.events.add(e)
            return True
        except:
            print("there was a problem adding the event, sorry.")
            return False
    
    def remove_event(self, event_name:str):
        " Removes the event from the calendar "
        for event in self.c.events:
            print(event)
            if event_name == event_name:
                self.c.events.remove(event)
                print("removing event:",event_name)
                return True
        print("Sorry could not find event:",event_name)
        return False
    
    def parse_to_dict(self):
        dict = []
        for event in self.c.events:
            my_events = {}
            my_events['begin'] = event.begin.datetime
            my_events['name'] = event.name
            my_events['description'] = event.description
            dict.append(my_events)
        return dict
    
    def save(self):
        # Save the calendar ICS file
        with open(calendar_filename, 'w') as my_file:
            my_file.writelines(self.c)
        # Saves the YAML Data file

        # first check that there are somne entries in the dictionary, otherise remove the file
        if self.c.events == set():
            print("No events - Removing YAML file")
            try:
                os.remove(calendar_datafile)
            except:
                print("oops couldn't delete the YAML file")
        else:
            with open(calendar_datafile, 'w') as outfile:

                yaml.dump(self.parse_to_dict(), outfile, default_flow_style=False)
    
    def load(self):
        " load the calendar data from the YAML file "
        filename = calendar_datafile
        my_file = Path(filename)

        # check if the file exists
        if my_file.is_file():
            stream = open(filename, 'r')
            events_list = yaml.load(stream)
            for item in events_list:
                e = Event()
                e.begin = item['begin']
                e.description = item['description']
                e.name = item['name']
                self.c.events.add(e)
        else:
            # file doesnt exist
            print("file does not exist")
    
    def list_events(self, period:str=None)->bool:
        """Lists the upcoming events
        if 'period is left empty it will default to today
        other options are:
        'all' - lists all events in the calendar
        'this week' - lists all the events this week
        'this month' - lists all the events this month
        """

        if period == None:
            period = "this week"
        
        # check that there are events
        if self.c.events == set():
            # no events found
            print("No events in calendar")
            return False
        else:
            event_list = []
            # have to fix the localisation - that the +00 time zone
            # otherwise it complains of non-naive date being compared with naive date
            now = pytz.utc.localize(datetime.now())
            if period == "this week":
                nextperiod = now+relativedelta(weeks=+1)
            if period == "this month":
                nextperiod = now+relativedelta(month=+1)
            if period == "all":
                nextperiod = now+relativedelta(years=+100)
            for event in self.c.events:
                events_date = event.begin.datetime
                if (events_date >= now) and (events_date <= nextperiod):
                    event_list.append(event)
            return event_list