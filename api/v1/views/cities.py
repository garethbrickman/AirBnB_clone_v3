#!/usr/bin/python3
"""
Creates a new view for State objects for all default API actions
"""
from flask import Flask, request, jsonify
from api.v1.views import app_views
from api.v1.app import not_found
from models import storage
from models.city import City


def getcity(city):
    return (city.to_dict(), 200)


def putcity(city):
    try:
        new = request.get_json()
    except:
        return ({"error": "Not a JSON"}, 400)
    for (k, v) in new.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(city, k, v)
    city.save()
    return (city.to_dict(), 200)


def deletecity(city):
    storage.delete(city)
    storage.save()
    return ({}, 200)


@app_views.route('/cities', methods=['GET', 'POST'])
def cities():
    """  Retrieves list of all state objs"""
    if request.method == 'GET':
        all_cities = [x.to_dict() for x in storage.all('City').values()]
        return (jsonify(all_cities), 200)
    elif request.method == 'POST':
        try:
            new = request.get_json()
        except:
            return ({"error": "Not a JSON"}, 400)
        if 'name' not in new.keys():
            return ({"error": "Missing name"}, 400)
        x = City()
        for (k, v) in new.items():
            setattr(x, k, v)
        x.save()
        return (x.to_dict(), 201)


@app_views.route('/cities/<ident>', methods=['GET', 'PUT', 'DELETE'])
def cities_id(ident):
    """ """
    cities = storage.all("City")
    for c in cities:
        if c.id == ident:
            if request.method == 'GET':
                return getcity(c)
            elif request.method == 'PUT':
                return putcity(c)
            elif request.method == 'DELETE':
                return deletecity(c)
    return (not_found(None))
