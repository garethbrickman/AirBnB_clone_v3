#!/usr/bin/python3
"""
Creates a new view for Amenity objects for all default API actions
"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


def getamen(amen):
    """Get object"""
    return (amen.to_dict(), 200)


def putamen(amen):
    """Update object """
    if not request.is_json:
        abort(400, "Not a JSON")
    new = request.get_json()
    for (k, v) in new.items():
        if k is not 'id' and k is not 'created_at' and k is not 'updated_at':
            setattr(amen, k, v)
    storage.save()
    return (amen.to_dict(), 200)


def deleteamen(amen):
    """Delete object """
    storage.delete(amen)
    storage.save()
    return ({}, 200)


@app_views.route('/amenities', methods=['GET', 'POST'])
def amens():
    """  Retrieves list of all amenities objs or creates a state"""
    if request.method == 'GET':
        all_amens = [x.to_dict() for x in storage.all('Amenity').values()]
        return (jsonify(all_amens), 200)
    elif request.method == 'POST':
        if not request.is_json:
            abort(400, "Not a JSON")
        new = request.get_json()
        if 'name' not in new.keys():
            return ({"error": "Missing name"}, 400)
        x = Amenity()
        for (k, v) in new.items():
            setattr(x, k, v)
        x.save()
        return (x.to_dict(), 201)


@app_views.route('/amenities/<ident>', methods=['GET', 'PUT', 'DELETE'])
def amens_id(ident):
    """Retrieves a specific object"""
    amens = storage.all('Amenity')
    for s in amens.values():
        if s.id == ident:
            if request.method == 'GET':
                return getamen(s)
            elif request.method == 'PUT':
                return putamen(s)
            elif request.method == 'DELETE':
                return deleteamen(s)
    abort(404, 'Not found')
