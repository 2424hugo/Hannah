import pyjokes
from ai import AI
from todo import Todo, Item
from weather import Weather
from randfacts import randfacts
from datetime import datetime
from calendar_skill import Calendar_skill
import dateparser
 

hannah = AI()
todo = Todo()
calendar = Calendar_skill()
calendar.load()

def facts():
    fact = randfacts.get_fact()
    print(fact)
    hannah.say(fact)

def joke():
    funny = pyjokes.get_joke()
    print(funny) 
    hannah.say(funny)

def add_todo()->bool:
    item = Item()
    hannah.say("Tell me what to add to the list")
    try:
        item.title = hannah.listen()
        todo.new_item(item)
        message = "Added" + item.title
        hannah.say(message)
        return True
    except:
        print("oops there was an error")
        return False

def list_todos():
    if len(todo) > 0:
        hannah.say("Here are your to do's")
        for item in todo:
            hannah.say(item.title)
    else:
        hannah.say("The list is empty!")

def remove_todo()->bool:
    hannah.say("Tell me which item to remove")
    try:
        item_title = hannah.listen()
        todo.remove_item(title=item_title)
        message = "Removed" + item_title
        hannah.say(message)
        return True
    except:
        print("oops there was an error")
        return False

def add_event()->bool:
    hannah.say("What is the name of the event")
    try:
        event_name = hannah.listen()
        hannah.say("When is the evemt")
        event_begin = hannah.listen()
        event_isodate = dateparser.parse(event_begin).strftime("%Y-%m-%d %H:%M:%S")
        hannah.say("What is the event description?")
        event_description = hannah.listen()
        message = "Ok, adding event " + event_name
        hannah.say(message)
        calendar.add_event(begin=event_isodate, name=event_name, description=event_description)
        calendar.save()
        return True
    except:
        print("opps there was an error") 
        return False

def remove_event()->bool:
    hannah.say("What is the name of the event you want to remove?")
    try:
        event_name = hannah.listen()
        try:
            message = "Okay removing " + event_name
            print(message)
            hannah.say(message)
            calendar.remove_event(event_name=event_name)
            calendar.save()
            return True
        except:
            hannah.say("Sorry I could not find the event", event_name)
            return False
    except:
        print("1 opps there was an error")
        return False

def list_events(period):
    this_period = calendar.list_events(period=period)
    print(this_period)
    if this_period is not False:
        message = "There "
        if len(this_period)>1:
            message = message + "are " + len(this_period) + " events in the diary"
        else:
            message = message + "is 1 event in the diary"
        hannah.say(message)
        for event in this_period:
            event_date = event.begin.datetime
            weekday = datetime.strftime(event_date, "%A")
            day = str(event.begin.datetime.day)
            month = datetime.strftime(event_date, "%B")
            year = datetime.strftime(event_date, "%Y")
            time = datetime.strftime(event_date, "%I:%M %p")
            name = event.name
            description = event.description
            message = "On " + weekday + " the " + day + " of " + month + " " + year + " at " + time + ", there is an event called " + name + " with an event description of " + description
            hannah.say(message)
    else:
        hannah.say("There are no events booked")


def weather():
    todays_weather = Weather()
    forecast = todays_weather.forecast()
    print(forecast)
    hannah.say(forecast)

def next_weather():
    tomorrows_weather = Weather()
    forecast = tomorrows_weather.tomorows_forcast()
    print(forecast)
    hannah.say(forecast)



command = ""
hannah.say("Hello, I'm hannah! How can I help you today?")
while True and command != "goodbye":
    try:
        command = hannah.listen()
        command = command.lower()
    except:
        print("oops there was an error")
        command = ""
    print("comand was:", command)

    if command == "tell me a joke":
        joke()
        command = ""
    if command in ["add to-do","add to do", "add item"]:
        add_todo()
        command = ""
    if command in ["list todos", "list todo", "list to do" "list the to-do", "list to do's", "list items"]:
        list_todos()
        command = ""
    if command in ["remove todo", "remove item", "mark done", "remove todos", "remove to-do", "remove to do's"]:
        remove_todo()
    if command in ['weather today', "what's the weather like", "what's the weather today", "what's the weather like today"]:
        weather()
    if command in ['weather tomorrow', "what's the weather like tomorrow", "what's the weather tomorrow"]:
        next_weather()
    if command == "tell me a fact":
        facts()
    if command in ['good morning', 'good afternoon', 'good evening', 'good night']:
        now = datetime.now()
        hr = now.hour
        if hr >= 0 and hr <= 12:
            message = "Morning"
        if hr > 12 and hr <= 17:
            message = "Afternoon"
        if hr > 17 and hr <= 21:
            message = "Evening"
        if hr >= 21: message = "Night"

        message = "Good " + message + " Hugo"
        if hr >= 0 and hr <= 12:
            hannah.say(message)
            weather()
        if hr >= 21:
            next_weather()
            hannah.say(message)
        else:
            hannah.say(message)
    
    # Calendar
    if command in ["add event", "add to calendar", "new event", "add a new event"]:
        add_event()
    if command in ["remove event", "cancel event", "delete event"]:
        remove_event()
    if command in ["list events", "what's on this month", "what's coming up this month"]:
        list_events(period='this month')
    if command in ["what's on this week", "what's coming up this week","what's happening this week"]:
        list_events(period='this week')
    if command in ["list all events"]:
        list_events(period='all')



hannah.say("Goodbye")