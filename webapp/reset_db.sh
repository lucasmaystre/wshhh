#!/bin/bash
DATABASE=data/database.db
rm $DATABASE
sqlite3 $DATABASE < schema.sql
sqlite3 $DATABASE < symbols.sql
sqlite3 $DATABASE < fakedata.sql
