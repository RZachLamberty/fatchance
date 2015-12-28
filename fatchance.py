#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: fatchance.py
Author: zlamberty
Created: 2015-12-27

Description:
    primary file for the fatchance application

Usage:
    <usage>

"""

import contextlib
import flask
import os
import sqlite3

import config.fatchance


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

app = flask.Flask(__name__)
app.config.from_object(config.fatchance)


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


# ----------------------------- #
#   authentication              #
# ----------------------------- #

class AuthenticationError(Exception):
    pass


def add_user(username, password):
    try:
        resp = query_db(
            query='insert into weighin_users (username, password) values (?, ?)',
            args=(username, password),
            commit=True
        )
    except sqlite3.IntegrityError:
        raise AuthenticationError("That user name already exists")
    except:
        raise


def authenticate(username, password):
    pws = query_db(
        query='select count(*) ct from weighin_users where username == ? and password == ?',
        args=(username, password),
        one=True
    )

    if pws['ct'] == 0:
        # check if user exist
        userct = query_db(
            query='select count(*) ct from weighin_users where username == ?',
            args=(username,),
            one=True
        )['ct']
        if userct == 1:
            raise AuthenticationError("Invalid password")
        else:
            raise AuthenticationError("Invalid username")
    # s'all good


# ----------------------------- #
#   views                       #
# ----------------------------- #

@app.route('/')
def show_weighins():
    q = (
        'select username, weighdate, weight '
        'from weighins '
        'order by username, weighdate desc'
    )
    weighins = query_db(q)
    return flask.render_template('show_weighins.html', weighins=weighins)


@app.route('/weighin', methods=['POST'])
def add_weighin():
    if not flask.session.get('logged_in'):
        flask.abort(401)

    print flask.request.form
    resp = query_db(
        'insert into weighins (username, weighdate, weight) values (?, ?, ?)',
        (
            flask.request.form['username'], flask.request.form['weighdate'],
            flask.request.form['weight']
        ),
        commit=True
    )
    flask.flash('New entry was successfully posted')
    return flask.redirect(flask.url_for('show_weighins'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if flask.request.method == 'POST':
        try:
            authenticate(
                username=flask.request.form['username'],
                password=flask.request.form['password']
            )
            flask.session['logged_in'] = True
            flask.flash('You have been logged in')
            return flask.redirect(flask.url_for('show_weighins'))
        except AuthenticationError as error:
            error = error
    return flask.render_template('login.html', error=error)


@app.route('/logout')
def logout():
    flask.session.pop('logged_in', None)
    flask.flash('You have been logged out')
    return flask.redirect(flask.url_for('show_weighins'))


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    app.run(
        host='0.0.0.0'
    )
