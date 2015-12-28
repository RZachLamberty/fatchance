#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: auth.py
Author: zlamberty
Created: 2015-12-28

Description:
    authentication details

Usage:
    <usage>

"""

import sqlite3

import model


# ----------------------------- #
#   authentication              #
# ----------------------------- #

class AuthenticationError(Exception):
    pass


def add_user(username, password):
    try:
        resp = model.query_db(
            query='insert into weighin_users (username, password) values (?, ?)',
            args=(username, password),
            commit=True
        )
    except sqlite3.IntegrityError:
        raise AuthenticationError("That user name already exists")
    except:
        raise


def authenticate(username, password):
    pws = model.query_db(
        query='select count(*) ct from weighin_users where username == ? and password == ?',
        args=(username, password),
        one=True
    )

    if pws['ct'] == 0:
        # check if user exist
        userct = model.query_db(
            query='select count(*) ct from weighin_users where username == ?',
            args=(username,),
            one=True
        )['ct']
        if userct == 1:
            raise AuthenticationError("Invalid password")
        else:
            raise AuthenticationError("Invalid username")
    # s'all good
