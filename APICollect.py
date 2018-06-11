#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Pulls json data off API and save as .txt file

config file stores API key, URL name of group to pull, and path to save .txt
files.

"""

import urllib.request
import math
import config
import json
import os
import config

def callAPI(group_name, offset, key, path):
    path = path + group_name + '_' + str(offset) + '.txt'

    url = 'https://api.meetup.com/2/members?offset={}&group_urlname={}&key={}&sign=true\
&page=200&order=name'.format(offset,group_name,key)
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    f = open(path, 'w')
    f.write(data)
    f.close()
    return data

def main():
    key = config.key
    group_name = config.group_name
    path = config.path
    os.mkdir(path)
    os.chdir(path)
    offset = 0
    data = callAPI(group_name, offset, key, path)
    js = json.loads(data)
    last = math.ceil(js['meta']['total_count'] / 200)
    print(last)
    for offset in range(1,last+1):
        callAPI(group_name, offset, key, path)

if __name__ == "__main__":
    main()