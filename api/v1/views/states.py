#!/usr/bin/python3
"""
Creates a new view for State objects for all default API actions
"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from api.v1.app import not_found, error_400
from models import storage
from models.state import State


def getstate(state):
    """Get object"""
    return (state.to_dict(), 200)


def putstate(state):
    """Update object"""
    try:
        new = request.get_json()
    except:
        abort(400, 'Not a JSON')
        # return (error_400({"error": "Not a JSON"}))
    for (k, v) in new.items():
        if k is not 'id' and k is not 'created_at' and k is not 'updated_at':
            setattr(state, k, v)
    storage.save()
    return (state.to_dict(), 200)


def deletestate(state):
    """Delete object"""
    storage.delete(state)
    storage.save()
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
            abort(400, 'Not a JSON')
            # return (error_400({"error": "Not a JSON"}))
        if 'name' not in new.keys():
            abort(400, 'Missing name')
            # return (error_400({"error": "Missing name"}))
        x = State()
        for (k, v) in new.items():
            setattr(x, k, v)
        x.save()
        return (x.to_dict(), 201)


@app_views.route('/states/<ident>', methods=['GET', 'PUT', 'DELETE'])
def states_id(ident):
    """Retrieves a specific object """
    states = storage.all('State')
    for s in states.values():
        if s.id == ident:
            if request.method == 'GET':
                return getstate(s)
            elif request.method == 'PUT':
                return putstate(s)
            elif request.method == 'DELETE':
                return deletestate(s)
    abort(404, 'Not found')
