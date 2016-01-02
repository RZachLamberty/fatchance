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

import bcrypt

import model


# ----------------------------- #
#   authentication              #
# ----------------------------- #

class AuthenticationError(Exception):
    pass


def add_user(username, password):
    try:
        model.add_user(
            username=username,
            hashpass=bcrypt.hashpw(password, bcrypt.gensalt())
        )
    except model.INTEGRITY_ERROR:
        raise AuthenticationError("Unable to add user! Try again.")
    except:
        raise


def authenticate(username, password):
    # get user's hashed password and check it with bcrypt
    hashpass = model.get_users_hashpass(username)

    if not (bcrypt.hashpw(password.encode('utf-8'), hashpass) == hashpass):
        raise AuthenticationError("Invalid username or password")
    # s'all good
