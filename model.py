#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: model.py
Author: zlamberty
Created: 2015-12-28

Description:
    access to our external database and associated CRUD operations

Usage:
    <usage>

"""

import contextlib
import flask
import sqlite3

from fatchance import app


# ----------------------------- #
#   db stuff                    #
# ----------------------------- #

# making sure database exists
def init_db():
    with contextlib.closing(_connect_db()) as db:
        with app.open_resource('sqlite_schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# creating connections within a context
def _connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def get_db():
    db = getattr(flask.g, '_database', None)
    if db is None:
        db = flask.g._database = _connect_db()
        _set_row_factory()
    return db


# context manager
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(flask.g, '_database', None)
    if db is not None:
        db.close()


# utilities for easier querying of the database
def _set_row_factory():
    flask.g._database.row_factory = _make_dicts


def _make_dicts(cursor, row):
    return {
        cursor.description[idx][0]: value
        for (idx, value) in enumerate(row)
    }


def query_db(query, args=(), one=False, commit=False):
    con = get_db()
    with con:
        cur = con.execute(query, args)
        rv = cur.fetchall()
        if commit:
            con.commit()
        cur.close()
    return (rv[0] if rv else None) if one else rv
