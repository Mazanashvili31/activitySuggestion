import requests
import json
import sqlite3

name = 'Activities.sqlite'
connection = sqlite3.connect(name)
cursor = connection.cursor()

cursor.execute("CREATE TABLE if not exists information("
               "id INTEGER PRIMARY KEY AUTOINCREMENT,"
               "h_name varchar(10),"
               "a_type varchar(10),"
               "activity varchar(30),"
               "participants INTEGER,"
               "price FLOAT,"
               "accessibility FLOAT)")

name = input("What's your name: ")
while(True):
    activity = input("What kind of activity do you love: recreational , education, busywork, cooking, social, charity: ")
    possible_answers = ('recreational', 'education', 'busywork', 'cooking', 'social', 'charity')
    if activity.lower() in possible_answers:
        break
    else:
        print("Please choose only from given options")
        continue

url = 'https://www.boredapi.com/api/activity'
res = requests.get(url)
if res.status_code == 200:
    dict = res.json()
    print("Hmm... Let me think...")
    while not (dict['type']) == activity.lower():
        res = requests.get(url)
        dict = res.json()

    print(f"{name}, You should try to {dict['activity']}")
    print(f"\nThe given suggestions are from {res.url}")
    print('JSON file will be also included')
    file = open('../API/activities.json', 'w')
    json.dump(dict, file, indent=4)
    file.close()
    dict['name'] = name
    cursor.execute("insert into information (h_name, a_type, activity, participants, price, accessibility) values (:name, :type, :activity, :participants, :price, :accessibility)", dict)

else:
    print("Something went wrong status code:",res.status_code)

connection.commit()
connection.close()



