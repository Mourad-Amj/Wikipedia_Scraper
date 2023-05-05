import requests
import json
from bs4 import BeautifulSoup
import re

def get_leaders():
    root_url = 'https://country-leaders.onrender.com'
    cookie_url = root_url+'/cookie'
    leaders_url = root_url +'/leaders'
    countries_url = root_url + '/countries'
    s = requests.session()
    r = s.get(cookie_url)
    countries = s.get(countries_url,cookies = r.cookies).json()
    leaders_per_country = {}

    for country in countries:
        params = {'country': country} 
        req = s.get(leaders_url, cookies = r.cookies, params=params).status_code

        if req != 200:
            r = s.get(cookie_url)
            leaders = s.get(leaders_url, cookies = r.cookies, params=params).json()
            #leaders is are dict without the bio
            #print("cookie refresh")

        else:
            leaders = s.get(leaders_url, cookies = r.cookies, params=params).json()
            #print("cookie ok"

        leaders_per_country[country] = leaders
        #the list of dict of leader of a specific country given ('us', 'be', 'fr', 'ma', 'ru')
        for leader in leaders_per_country[country]:
            #for each leader( a dict with info about them ) in the list their country 
            first_paragraph = get_first_paragraph(leader['wikipedia_url'], s)
            leader['bio'] = first_paragraph
    return leaders_per_country

def get_first_paragraph(wikipedia_url,s):
    #print(wikipedia_url)
    wiki_text = s.get(wikipedia_url).text
    soup = BeautifulSoup(wiki_text, 'html.parser')
    first_paragraph = ''

    for paragraph in soup.find_all('p'):
        if paragraph.find('b'):
            first_paragraph = re.sub(r" \(.*\)","",paragraph.get_text())
            break
    return(first_paragraph)

leaders_per_country = get_leaders()
def save(leaders_per_country):
    with open( 'leaders.json','w' ) as outfile:
        json.dump(leaders_per_country,outfile, indent=4)

save(leaders_per_country)
