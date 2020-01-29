#!/usr/bin/python3
"""
Creates a new view for State objects for all default API actions
"""
from flask import Flask, request, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State


def getstate(state):
    """ """
    return (state.to_dict(), 200)


def putstate(state):
    """ """
    try:
        new = request.get_json()
    except:
        return ("Not a JSON", 400)
    for (k, v) in new.items():
        if k is not 'id' and k is not 'created_at' and k is not 'updated_at':
            setattr(state, k, v)
        return (state.to_dict(), 200)


def deletestate(state):
    """ """
    storage.delete(state)
    storage.reload()
    return ({}, 200)


@app_views.route('/states', methods=['GET', 'POST'])
def states():
    """  Retrieves list of all state objs or creates a state"""
    if request.method == 'GET':
        all_states = [x.to_dict() for x in storage.all('State').values()]
        return (jsonify(all_states), 200)
    elif request.method == 'POST':
        try:
            new = request.get_json()
        except:
            return ("Not a JSON", 400)
        if 'name' not in new.keys():
            return ("Missing name", 400)
        x = State()
        for (k, v) in new.items():
            setattr(x, k, v)
        x.save()
        return (x.to_dict(), 201)


@app_views.route('/states/<ident>', methods=['GET', 'PUT', 'DELETE'])
def states_id(ident):
    """ """
    states = storage.all('State')
    for s in states.values():
        if s.id == ident:
            if request.method == 'GET':
                return getstate(s)
            elif request.method == 'PUT':
                return putstate(s)
            elif request.method == 'DELETE':
                return deletestate(s)
    return ({}, 404)
