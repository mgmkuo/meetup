#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 09:48:45 2018

@author: maggie
Pulls data off API and puts into a table

Notes: To execute: (in command line) ./scrape.py > file.csv


"""
#import urllib.request
#import urllib.parse
#import urllib.error
import json
import time
import os

# api_key = '77e775b354a147e36391f51484532f'

path = '/home/maggie/Documents/insight/meetup/data'
os.chdir(path)

header = 'names,mem_id,city,state,lat,lon,time_visited,time_joined,blank'
for i in range(1,51):
    header += ',' + str(i)
print(header)

for f in os.listdir():
    with open(f) as json_file:
        js = json.load(json_file)

    for mem in range(len(js['results'])):
        try:
            name = js['results'][mem]['name']
        except KeyError:
            name = ''
        try:
            mem_id = str(js['results'][mem]['id'])
        except KeyError:
            mem_id = ''
        try:
            city = js['results'][mem]['city']
        except KeyError:
            city = ''
        try:
            state = js['results'][mem]['state']
        except KeyError:
            state = ''
        try:
            lat = str(js['results'][mem]['lat'])
        except KeyError:
            lat = ''
        try:
            lon = str(js['results'][mem]['lon'])
        except KeyError:
            lon = ''
        try:
            time_visited = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(js['results'][mem]['visited']/1000))
        except KeyError:
            time_visited = ''
        try:
            time_joined = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(js['results'][mem]['joined']/1000))
        except KeyError:
            time_joined = ''
    
        topics = ''
        for topic in range(len(js['results'][mem]['topics'])):
            topics += ',' + js['results'][mem]['topics'][topic]['urlkey']
    
        row = '\n' + name\
            + ',' + mem_id\
            + ',' + city\
            + ',' + state\
            + ',' + lat\
            + ',' + lon\
            + ',' + time_visited\
            + ',' + time_joined\
            + ',' + topics  
        print(row)
