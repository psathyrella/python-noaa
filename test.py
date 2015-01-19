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
            date_str, time_str = start.text.split('T')  # will raise ValueError if it doesn't split into to pieces
            year, month, day = [ int(val) for val in date_str.split('-') ]
            moment = datetime.datetime(year, month, day, hour, minute, second, microsecond, tzinfo)
            layouts[name].append(start.text)
        sys.exit()
    return layouts

def unify_values(timedelta, values):
    """ 
    The variables all come with different time intervals and horizons, 
    so if we want all of them, e.g., every 12 hours, we have to go through 
    and either find the closest value (e.g. temperature), or integrate out
    or divide values (e.g. precip)
    """
    

def parse_data(root, time_layouts):
    pars = root.find('data').find('parameters')
    data = {}
    for vardata in pars:
        # first figure out the name
        all_names = list(vardata.iter('name'))
        if len(all_names) != 1:
            raise Exception('ERROR too many names for %s: %s' % (vardata.tag, ', '.join(all_names)))
        name = all_names[0].text
        if name in data:
            raise Exception('ERROR %s already in data' % key)

        # then get the data
        data[name] = {}
        if vardata.get('time-layout') is None:  # single-point data
            print '  no layout %s' % name
            continue
        else:  # time series data
            data[name]['time-layout'] = time_layouts[vardata.get('time-layout')]
            data[name]['values'] = [ val.text for val in vardata.findall('value') ]
            if len(data[name]['time-layout']) != len(data[name]['values']):
                print '  time layout different length for %s' % name

    return data
    
time_layouts = get_time_layouts(root)
data = parse_data(root, time_layouts)
