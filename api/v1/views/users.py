#!/usr/bin/python3
"""
Creates a new view for User objects for all default API actions
"""
from flask import Flask, request, jsonify
from api.v1.views import app_views
from api.v1.app import not_found
from models import storage
from models.user import User


def getuser(user):
    """Get object"""
    return (user.to_dict(), 200)


def putuser(user):
    """Update object """
    try:
        new = request.get_json()
    except:
        return ({"error": "Not a JSON"}, 400)
    for (k, v) in new.items():
        if k is not 'id' and k is not 'email'\
           and k is not 'created_at' and k is not 'updated_at':
            setattr(user, k, v)
    user.save()
    return (user.to_dict(), 200)


def deleteuser(user):
    """Delete object """
    storage.delete(user)
    storage.save()
    return ({}, 200)


@app_views.route('/users', methods=['GET', 'POST'])
def users():
    """  Retrieves list of all objects or creates an object"""
    if request.method == 'GET':
        all_users = [x.to_dict() for x in storage.all('User').values()]
        return (jsonify(all_users), 200)
    elif request.method == 'POST':
        try:
            new = request.get_json()
        except:
            return ({"error": "Not a JSON"}, 400)
        if 'email' not in new.keys():
            return ({"error": "Missing email"}, 400)
        if 'password' not in new.keys():
            return ({"error": "Missing password"}, 400)
        x = User()
        for (k, v) in new.items():
            setattr(x, k, v)
        x.save()
        return (x.to_dict(), 201)


@app_views.route('/users/<ident>', methods=['GET', 'PUT', 'DELETE'])
def users_id(ident):
    """Retrieves a specific object"""
    users = storage.all('User')
    for s in users.values():
        if s.id == ident:
            if request.method == 'GET':
                return getuser(s)
            elif request.method == 'PUT':
                return putuser(s)
            elif request.method == 'DELETE':
                return deleteuser(s)
    return (not_found(None))
