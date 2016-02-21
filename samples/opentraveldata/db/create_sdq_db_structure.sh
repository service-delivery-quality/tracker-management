#!/bin/bash
#
# All the parameters are optional for this script:
# - the host server of the database
# - the port of the database

##
# Default parameters
DB_HOST="localhost"
DB_PORT="3306"
DB_USER="sdq"
DB_PASSWD="${DB_USER}"
DB_NAME="sdq_sdq"


if [ "$1" = "-h" -o "$1" = "--help" ];
then
	echo "Usage: $0 [<Database Server Hostname> [<Database Server Port>]]"
	echo
	echo "The database is assumed to be MySQL/MariaDB."
	echo
	echo "  Default parameters:"
	echo "    - Database server hostname: $DB_HOST"
	echo "    - Database server port: $DB_PORT"
	echo
	exit -1
fi

##
# Database Server Hostname
if [ "$1" != "" ];
then
	DB_HOST="$1"
fi

# Database Server Port
if [ "$2" != "" ];
then
	DB_PORT="$2"
fi

#
function execSQL() {
	echo "Processing the ${SQL_FILE} SQL script file..."
	mysql -u ${DB_USER} --password=${DB_PASSWD} -P ${DB_PORT} -h ${DB_HOST} ${DB_NAME} < ${SQL_FILE}
	echo "... Done"
}

# Create and fill the tables
SQL_FILE="create_sdq_db_tables.sql"
execSQL

# Create the indexes
SQL_FILE="create_sdq_db_values.sql"
execSQL

