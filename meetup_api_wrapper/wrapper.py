#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wrapper for calling MeetUp's API

"""
import json
import urllib.request
import os

class meetupAPI:
    def __init__(self, key):
        self.key = key
        self.cache_path = self.set_cache_path()

    def set_cache_path(self, folder_name=None):
        if folder_name:
            path = os.path.join(os.getcwd(), '.cache/{}'.format(folder_name))
        else:
            path = os.path.join(os.getcwd(), '.cache/')
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def get_group_members(self, group_name):
        all_members = []
        offset = 0
        initial_call = self.call_members_api(offset, group_name)
        all_members = initial_call['members']
        count = initial_call['count']
        total_count = initial_call['total_count']
        counter = total_count - count

        while counter > 0:
            print('{} out of {} total members remaining to collect'.format(counter,
                total_count))
            offset += 1
            call = self.call_members_api(offset, group_name)
            all_members += call['members']
            counter -= call['count']
        print('all collected')

        return all_members
    
    def call_members_api(self, offset, group_name):
        cache_folder = self.set_cache_path(folder_name=group_name)
        url =\
        'https://api.meetup.com/2/members?offset={}&group_urlname={}&key={}&sign=true&page=200&order=name'.format(offset,
                group_name, self.key)
        uh = urllib.request.urlopen(url)
        data = uh.read().decode()
        data = json.loads(data)

        with open(os.path.join(cache_folder, '{}_{}.json'.format(group_name,
            offset)), 'w') as f:
            json.dump(data, f)

        return {'members': data['results'], 
                'count': data['meta']['count'],
                'total_count': data['meta']['total_count']}

