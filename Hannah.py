import pyjokes
from ai import AI
from todo import Todo, Item
from weather import Weather
from randfacts import randfacts
 

hannah = AI()
todo = Todo()

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

def weather():
    todays_weather = Weather()
    forecast = todays_weather.forecast()
    print(forecast)
    hannah.say(forecast)


command = ""
hannah.say("Hello")
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
    if command == "tell me a fact":
        facts()
    #if command in ['good morning', 'good evening', 'good night']:
    #    return True


hannah.say("Goodbye")