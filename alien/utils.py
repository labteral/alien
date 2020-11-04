#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
from datetime import timedelta, datetime
import re
from lxml import etree
import lxml.html
from urllib3 import ProxyManager, PoolManager
from os import environ

if 'HTTPS_PROXY' in environ:
    session = ProxyManager(environ['HTTPS_PROXY'], maxsize=100, block=True)
elif 'HTTP_PROXY' in environ:
    session = ProxyManager(environ['HTTP_PROXY'], maxsize=100, block=True)
else:
    session = PoolManager(maxsize=100, block=True)


def return_on_error(method):
    def return_on_error_(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except Exception:
            return

    return return_on_error_


def get_random_user_agent():
    system_info_lines = [
        'Windows NT 10.0; Win64; x64',  # Windows 10
        'Windows NT 6.3; Win64; x64',  # Windows 8.1
        'Windows NT 6.2; Win64; x64',  # Windows 8
        'Windows NT 6.1; Win64; x64',  # Windows 7
        'X11; Linux x86_64',
    ]

    chrome_version_lines = [
        '78.0.3904.87',
        '77.0.3865.90',
        '75.0.3770.100',
        '60.0.3112.113',
        '60.0.3112.90',
        '57.0.2987.133',
        '55.0.2883.87',
        '44.0.2403.157',
    ]

    system_info = system_info_lines[randint(0, len(system_info_lines) - 1)]
    chrome_version = chrome_version_lines[randint(0, len(chrome_version_lines) - 1)]

    user_agent = f'Mozilla/5.0 ({system_info}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36'
    return user_agent


def get_response(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.5',
        'dnt': '1',
        'pragma': 'no-cache',
        'cache-control': 'no-control',
        'upgrade-insecure-requests': '1',
        'origin': 'https://www.reddit.com/'
    }
    headers['user-agent'] = get_random_user_agent()
    request = session.request('GET', url=url, headers=headers)
    return request.data.decode('utf-8')


def get_lxml_from_response(response):
    return lxml.html.document_fromstring(response)


def get_fixed_subreddit(subreddit):
    if subreddit[:2] != 'r/':
        subreddit = f'r/{subreddit}'
    return subreddit


def get_timestamp_from_text(time_ago):
    # datetime.today() with tzinfo None (UTC)
    estimated_datetime = datetime.today()
    if not re.match("just\\snow.*", time_ago):
        m = re.match("([0-9]+)\\s(h|mi|d|mo|y).+", time_ago)
        if m:
            time_groups = m.groups()
            if time_groups[1] == 'h':
                estimated_datetime = estimated_datetime \
                    - timedelta(hours=int(time_groups[0]))
            elif time_groups[1] == 'mi':
                estimated_datetime = estimated_datetime \
                    - timedelta(minutes=int(time_groups[0]))
            elif time_groups[1] == 'd':
                estimated_datetime = estimated_datetime \
                    - timedelta(days=int(time_groups[0]))
            elif time_groups[1] == 'mo':
                estimated_datetime = estimated_datetime \
                    - timedelta(days=int(time_groups[0]) * 30)
            elif time_groups[1] == 'y':
                estimated_datetime = estimated_datetime \
                    - timedelta(days=int(time_groups[0]) * 365)
        else:
            return None
    return int(estimated_datetime.timestamp())


def get_element_id(element):
    return list(element.classes)[2].split('_')[1]


def get_content_url(element):
    """ Returns the URL of the posted content both internal or external links
    """
    return element.xpath("."
        + "/a[@class='title']"
        + "/@href")[0] \
        .split('.compact')[0]


class IterableResults:
    def __iter__(self):
        return self.results.__iter__()

    def __next__(self):
        return self.results.__next__()
