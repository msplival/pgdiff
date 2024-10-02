#!/bin/bash

# Load database configurations
# shellcheck source=./source.conf
source ./source.conf
# shellcheck source=./target.conf
source ./target.conf

# Execute source.sql on the source database
echo "Populate source database"
psql -h $SOURCE_DB_HOST -U $SOURCE_DB_USER -d $SOURCE_DB_NAME -f ./source.sql

# Execute target.sql on the target database
echo "Populate target database"
psql -h $TARGET_DB_HOST -U $TARGET_DB_USER -d $TARGET_DB_NAME -f ./target.sql
