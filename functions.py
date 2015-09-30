import requests
import time
import pickle
import sys

import vk
import webbrowser
import PyQt4

sys.path.append('..')
from user import login, password, token

#webbrowser.open('https://oauth.vk.com/authorize?client_id=5073025&display=page&redirect_uri=https://oauth.vk.com/blank.html&response_type=token&v=5.37')

class Person():
    elo = 0                     # Elo rating
    group = 0                   # Matchmaking group
    k = 40                      # Initial coefficient
    battles = 0                 # Batlles was played
vkapi = vk.API('5073025', login, password, access_token=token)

def unpickle(): 
    data = open('data.pkl', 'rb')
    self = pickle.load(data)
    data.close()
    return self

def save(self):
    data = open('data.pkl', 'wb')
    pickle.dump(self, data)
    data.close()

def download(): # Download library
    profiles = vkapi.users.search(
        sort=0, 
        #sex=1, 
        has_photo=1, 
        #university=1,
        #university_year=2016,
        #university_faculty=1,
        count=10,
        fields='photo_max_orig'
        )

    print(len(profiles['items']))

    array = []
    # Parsing library to array of Person() class
    for i in range(len(profiles['items'])):
        array.append(Person())
        array[i].name    = profiles['items'][i]['first_name']
        array[i].sname = profiles['items'][i]['last_name']
        array[i].id  = profiles['items'][i]['id']
        array[i].jpg = r'pics/'+str(profiles['items'][i]['id'])+'.jpg'

    # Download images 
    for i in range(len(profiles['items'])):
        p = requests.get(profiles['items'][i]['photo_max_orig'])
        adress=r'pics/'+str(profiles['items'][i]['id'])+'.jpg'
        out = open(adress, "wb")
        out.write(p.content)
        out.close()

    save(array)

def buttle(w, l):
    we=w.elo
    le=l.elo
    w.elo=we+w.k*(1-1/(1+pow(10, (le-we)/400)))
    l.elo=we+w.k*(1-1/(0+pow(10, (le-we)/400)))
    w.battles=w.battles+1
    l.battles=l.battles+1
    if w.battles>30: w.k=20
    if l.battles>30: l.k=20