# -*- coding: utf-8 -*-
import os

import requests


def test_ping_demo_server(demo_baseurl):
    """
    baseurl should resolve to success response
    """
    r = requests.get(demo_baseurl)

    r.status_code == 200


def test_marker(demo_baseurl):
    """
    Server should contain the correct JSON file marker to ensure this is
    really the expected demo server.
    """
    url = os.path.join(demo_baseurl, "marker.json")
    r = requests.get(url)

    r.json() == {"generator": "py-website-capture marker"}
