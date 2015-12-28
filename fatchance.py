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

app = flask.Flask(__name__)
app.config.from_object(config.fatchance)

import auth
import model

from views import *

# ----------------------------- #
#   Module Constants            #
# ----------------------------- #


# ----------------------------- #
#   Command line                #
# ----------------------------- #

if __name__ == '__main__':
    app.run(
        host='0.0.0.0'
    )
