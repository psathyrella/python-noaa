#!/usr/bin/env python
import sys
import datetime
from xml.etree import ElementTree as ET

tree = ET.parse('verbose.xml')
root = tree.getroot()

# point_forecast_url = list(root.iter('moreWeatherInformation'))[0].text

def get_time_layouts(root):
    layouts = {}
    for lout in root.find('data').findall('time-layout'):
        name = lout.find('layout-key').text
        layouts[name] = []
        for start in lout.iter('start-valid-time'):
            # datetime.date(year, month, day)
            layouts[name].append(start.text)
    return layouts

def parse_data(root, time_layouts):
    pars = root.find('data').find('parameters')
    data = {}
    for vardata in pars:
        # key = vardata.get('type') + '-' + vardata.tag
        all_names = list(vardata.iter('name'))
        if len(all_names) != 1:
            raise Exception('ERROR too many names for %s: %s' % (vardata.tag, ', '.join(all_names)))
        name = all_names[0].text
        if name in data:
            raise Exception('ERROR %s already in data' % key)

        if vardata.get('time-layout') is not None:
            layout = time_layouts[vardata.get('time-layout')]
            print len(layout)
        else:
            print '%s no layout' % name
    
time_layouts = get_time_layouts(root)
parse_data(root, time_layouts)
