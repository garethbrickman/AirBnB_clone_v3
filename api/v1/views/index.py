#!/usr/bin/python3
"""
Returns JSON status on object app_views
"""
from flask import Flask
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """ Returns status message in JSON
    """
    return ({"status": "OK"})
