#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: config/fatchance.py
Author: zlamberty
Created: 2015-12-27

Description:
    configuration for the fatchance flask app

Usage:
    <usage>

"""

# configuration
SQLALCHEMY_DATABASE_URI = 'postgresql://fatchance:fatchance@localhost/fatchance'
SQLALCHEMY_TRACK_MODIFICATIONS = True
DEBUG = True
SECRET_KEY = 'development_key'
USERNAME = 'admin'
PASSWORD = 'password'
HOST = '0.0.0.0'
