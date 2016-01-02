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

from fatchance import app

import auth
import model


# ----------------------------- #
#   views                       #
# ----------------------------- #

@app.route('/')
def show_weighins():
    return render_template('show_weighins.html', weighins=model.weighins())


@app.route('/weighin', methods=['POST'])
def add_weighin():
    if not session.get('logged_in'):
        abort(401)

    model.add_weighin(
        username=request.form['username'],
        weighdate=request.form['weighdate'],
        weight=request.form['weight']
    )

    flash('New weighin recorded!', SUC)
    return redirect(url_for('show_user_home', username=session.get('username')))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            username = request.form['username']
            auth.authenticate(
                username=username,
                password=request.form['password']
            )
            session['username'] = username
            session['logged_in'] = True
            flash('You have been logged in, {}'.format(username), INF)
            return redirect(url_for('show_weighin_summary'))
        except auth.AuthenticationError as error:
            error = error
    return render_template(
        'login.html',
        name='login',
        error=error
    )


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out', INF)
    return redirect(url_for('show_weighin_summary'))


@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    error = None
    if request.method == 'POST':
        try:
            # make sure they typed the same password both times
            if not request.form['password'] == request.form['password2']:
                raise auth.AuthenticationError("Passwords did not match")
            auth.add_user(
                username=request.form['username'],
                password=request.form['password']
            )
            session['logged_in'] = True
            flash('Your user name has been created', INF)
            return redirect(url_for('show_weighin_summary'))
        except auth.AuthenticationError as error:
            error = error
    return render_template(
        'new_user.html',
        name='new_user',
        error=error
    )
