#!/bin/bash

# must have postgres installed
# sudo apt-get install postgresql

# must be run as postgres user
# sudo su - postgres
psql -f /home/zlamberty/git/fatchance/psql_schema.sql
