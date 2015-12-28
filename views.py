#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: views.py
Author: zlamberty
Created: 2015-12-28

Description:
    our routing table and views

Usage:
    <usage>

"""

from flask import (abort, flash, url_for, redirect, render_template, request,
                   session)

import auth
import model

from fatchance import app


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
    weighins = model.query_db(q)
    return render_template('show_weighins.html', weighins=weighins)


@app.route('/weighin', methods=['POST'])
def add_weighin():
    if not session.get('logged_in'):
        abort(401)

    resp = model.query_db(
        'insert into weighins (username, weighdate, weight) values (?, ?, ?)',
        (
            request.form['username'], request.form['weighdate'],
            request.form['weight']
        ),
        commit=True
    )
    flash('New entry was successfully posted')
    return redirect(url_for('show_weighins'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            auth.authenticate(
                username=request.form['username'],
                password=request.form['password']
            )
            session['logged_in'] = True
            flash('You have been logged in')
            return redirect(url_for('show_weighins'))
        except auth.AuthenticationError as error:
            error = error
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out')
    return redirect(url_for('show_weighins'))
