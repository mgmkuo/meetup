from bs4 import BeautifulSoup
import json
import math
import re
import scipy.sparse as sparse
from site_files import extractData
import urllib.request


def process_user_input(interest1, interest2, interest3):
    """
    Combines user input hobbies into one list. Reformats entries
    to match keys in database.
    
    Returns list of interests.
    """
    interests = [interest1, interest2, interest3]
    
    for i in range(len(interests)):
        interests[i] = interests[i].strip().lower().replace(' ','-')

    return interests

def zones(zone, recs):
    """
    Calculates how far down the list user selected zone corresponds to
    Returns lower limit of range to pull from.
    
    """
    llim = math.floor(float(zone)*(len(recs) - 7))

    return llim

def find_meetups(hobbies):
    """
    Scrapes Meetup page and pulls active Meetup groups and upcoming events.
    Returns list in format (hobby, event_url) with hobbies with events 
    in front and hobbies with no events at end.
    """
    events_upcoming = list()
    events_none = list()
    
    for hobby in hobbies:
        # Finding group related to hobby
        url = 'https://www.meetup.com/find/?allMeetups=false&keywords={}\
         &radius=5&userFreeform=New+York%2C+NY&mcId=z10001&mcName=New+York\
         %2C+NY&sort=default&eventFilter=mysugg'.format(hobby)
        url = url.replace(' ', '')
        uh = urllib.request.urlopen(url)
        data = uh.read().decode()    
        soup = BeautifulSoup(data, 'html.parser')

        try:
            group_url = soup.find(
                        attrs={'class':'groupCard--photo loading nametag-photo '}
                        ).attrs['href']

            # Finding upcoming event exists for group. Returns event if it does
            event_url = group_url + 'events/'
            uh = urllib.request.urlopen(event_url)
            data = uh.read().decode()    
            soup = BeautifulSoup(data, 'html.parser')
            soup_event_id = soup.find(attrs={'type':'application/ld+json'}).string

            if soup_event_id == '[]':
                event_url = group_url
                events_none.append((hobby, event_url))
            else:
                event_id = re.findall('events/([0-9a-zA-Z]*)', soup_event_id)[0]
                event_url = event_url + event_id
                events_upcoming.append((hobby, event_url))

        except AttributeError:
            events_none.append((hobby, 'https://www.meetup.com/placesnyc/'))
            continue
            
    events = events_upcoming + events_none

    return events


def Model(interest1, interest2, interest3, zone):
    """
    Main function. Takes in user entered interests and exploration extent.
    Returns suggestsed hobbies and urls to upcoming events or groups
    active in that topc.
    """
    
    # Gets data from files
    df_sparse = sparse.load_npz('meetup_db_sparse.npz')
    
    with open('dict_urlkey2name.json') as f:
        dict_urlkey2name = json.load(f)
    
    with open('dict_num2urlkey.json') as f:
        dict_num2urlkey = json.load(f)

        
    # Process user-entered interests
    interests = process_user_input(interest1, interest2, interest3)
    
    # Retrieve ranked list of hobbies and scores
    recs, hobby_scores = extractData.create_recs(interests, dict_num2urlkey, df_sparse)
    
    # Customizes recs based on selected zone
    llim = zones(zone, recs)
    hobbies = recs[llim:llim+5]


    # Find upcoming events
    events = find_meetups(hobbies)
    
    
    # Unpacking events variable for embedding in HTML
    hob0 = dict_urlkey2name[events[0][0]]
    hob1 = dict_urlkey2name[events[1][0]]
    hob2 = dict_urlkey2name[events[2][0]]
    hob3 = dict_urlkey2name[events[3][0]]
    hob4 = dict_urlkey2name[events[4][0]]

    events0 = events[0][1]
    events1 = events[1][1]
    events2 = events[2][1]
    events3 = events[3][1]
    events4 = events[4][1]

    return hob0, hob1, hob2, hob3, hob4, events0, events1, events2, events3, events4
