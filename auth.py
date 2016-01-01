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

import model


# ----------------------------- #
#   authentication              #
# ----------------------------- #

class AuthenticationError(Exception):
    pass


def add_user(username, password):
    try:
        model.add_user(username, password)
    except model.INTEGRITY_ERROR:
        raise AuthenticationError("That user name already exists")
    except:
        raise


def authenticate(username, password):
    # check if user exists
    if not model.user_exists(username):
        raise AuthenticationError("Invalid username")
    elif not model.user_has_password(username, password):
        raise AuthenticationError("Invalid password")
    # s'all good
