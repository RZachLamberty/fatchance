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

import datetime
import flask
import pandas as pd
import sqlalchemy

from fatchance import app
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


# ----------------------------- #
#   constants                   #
# ----------------------------- #

INTEGRITY_ERROR = sqlalchemy.exc.IntegrityError
TDY = datetime.datetime.now()


# ----------------------------- #
#   sql alchemy classes         #
# ----------------------------- #

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column('username', db.TEXT, primary_key=True)
    hashpass = db.Column('hashpass', db.TEXT)


class Weighin(db.Model):
    __tablename__ = 'weighins'
    weighdate = db.Column('weighdate', db.DATE, primary_key=True, default=TDY)
    username = db.Column(
        'username', db.TEXT, db.ForeignKey('users.username'), primary_key=True
    )
    weight = db.Column('weight', db.REAL)

    usernamerel = db.relationship('User', foreign_keys=username)


# ----------------------------- #
#   utility functions           #
# ----------------------------- #

def with_session(f, autocommit=True):
    """ wrapper for session transactions """
    def go(*args, **kw):
        try:
            ret = f(*args, **kw)
            if autocommit:
                db.session.commit()
            return ret
        except:
            print "unable to commit session; rolling back"
            db.session.rollback()
            raise
    return go


@with_session
def add_user(username, hashpass):
    u = User(username=username, hashpass=hashpass)
    db.session.add(u)


@with_session
def get_users_hashpass(username):
    return User.query.filter_by(username=username).first().hashpass.encode('utf-8')


@with_session
def weighins():
    return Weighin.query.order_by(
        Weighin.username.desc(), Weighin.weighdate.desc()
    ).all()


@with_session
def add_weighin(username, weighdate, weight):
    w = Weighin(username=username, weighdate=weighdate, weight=weight)
    db.session.add(w)


# ----------------------------- #
#   db stuff                    #
# ----------------------------- #

# play nice with pandas
def q_as_dicts(res):
    """ turn sqlalchemy results into a listdict """
    return [
        {k: v for (k, v) in row.items() if k != '_sa_instance_state'}
        for row in res
    ]


def q_as_df(res):
    """ turn sqlalchemy results into a df """
    return pd.DataFrame([row.__dict__ for row in res]).drop(
        '_sa_instance_state', axis=1
    )
