#!/usr/bin/env python

import requests
import csv
from bs4 import BeautifulSoup
url = 'http://lost-in-the-mountains.com/washington_climbing.php'  #?lid=9

locations = []

for lid in range(9, 13):
    req = requests.get(url + '?lid=' + str(lid))
    soup = BeautifulSoup(req.text)
    for link in soup.find_all('a'):
        linkurl = link.get('href')
        if 'forecast.weather.gov' not in linkurl:
            continue
        queries = linkurl.split('?')[1].split('&')  # I bet requests has a function to do this
        lat = queries[0].split('=')[1]
        lon = queries[1].split('=')[1]
        location_name = link.text.replace(' ', '')
        print location_name, lat, lon
        locations.append({'name':location_name, 'lat':lat, 'lon':lon})


with open('lost-locations.csv', 'w') as outfile:
    writer = csv.DictWriter(outfile, ('name', 'lat', 'lon'))
    for locinfo in locations:
        writer.writerow(locinfo)
