#!/usr/bin/python3
"""
Creates a new view for objects for all default API actions
"""
from flask import Flask, request, jsonify
from api.v1.views import app_views
from models import storage
from models.city import City


def getcity(city):
    """Get object"""
    return (city.to_dict(), 200)


def putcity(city):
    """Update object"""
    if not request.is_json:
        abort(400, "Not a JSON")
    new = request.get_json()
    for (k, v) in new.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(city, k, v)
    city.save()
    return (city.to_dict(), 200)


def deletecity(city):
    """Delete object"""
    storage.delete(city)
    storage.save()
    return ({}, 200)


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities(state_id):
    """Retrieves list of all objects"""
    state = None
    for s in storage.all('State').values():
        if s.id == state_id:
            state = s
    if state is None:
        return not_found(None)
    if request.method == 'GET':
        all_cities = []
        for x in storage.all('City').values():
            if x.state_id == state_id:
                all_cities.append(x.to_dict())
        return (jsonify(all_cities), 200)
    elif request.method == 'POST':
        if not request.is_json:
            abort(400, "Not a JSON")
        new = request.get_json()
        if 'name' not in new.keys():
            return ({"error": "Missing name"}, 400)
        x = City()
        for (k, v) in new.items():
            setattr(x, k, v)
        setattr(x, 'state_id', state_id)
        x.save()
        return (x.to_dict(), 201)


@app_views.route('/cities/<ident>', methods=['GET', 'PUT', 'DELETE'])
def cities_id(ident):
    """Retrieves a specific object"""
    cities = storage.all("City").values()
    for c in cities:
        if c.id == ident:
            if request.method == 'GET':
                return getcity(c)
            elif request.method == 'PUT':
                return putcity(c)
            elif request.method == 'DELETE':
                return deletecity(c)
    abort(404, 'Not found')
