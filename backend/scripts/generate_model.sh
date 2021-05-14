#!/usr/bin/env bash


TABLES="flatten"



flask-sqlacodegen --flask --schema "dw" --tables $TABLES --outfile model/models.py postgresql+psycopg2://$POSTGRES_USER:$POSTGRES_PW@$POSTGRES_URL/$POSTGRES_DB
