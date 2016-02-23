# Delivery Quality - Tracking Management

## Overview
That repository features tools to ease the creation, implementation and management
of delivery quality trackers.

## Samples - OpenTravelData
The sample project is OpenTravelData (OPTD): http://github.com/opentraveldata/opentraveldata

### Database Creation
If the ```sdq``` database user does not exist, the following script creates it:
```bash
cd samples/opentraveldata/db
./create_sdq_user.sh
```
Normally, that script just needs to run once and for all.

If the ```sdq_sdq``` database does not exist, the following script creates it:
```bash
cd samples/opentraveldata/db
./create_sdq_db.sh
```
That script comes handy as well to reset the full database (as it drops it and re-creates it). However, once the database exists, it is usually not needed to re-run those scrips.

The following scripts create all the tables, as well as their related content, for the sample application:
```bash
cd samples/opentraveldata/db
./create_sdq_db_structure.sh
```

### Python Environment

Before starting, please ensure you have installed the mysql client, server and dev tools (libmysqlclient-dev)

Inspired by:
* http://www.roblayton.com/2015/04/creating-python-flask-crud-api-with.html
* http://cherrypy.readthedocs.org/en/3.3.0/tutorial/REST.html
Create a Python virtual environment, and install a few needed Python libraries within it:
```bash
cd samples/opentraveldata/python-db
virtualenv venv
source venv/bin/activate
pip install mysql flask simplejson flask-cors cherrypy
```

### Flask Server
Start the Flask server in the background:
```bash
cd samples/opentraveldata/python-db/flask/
python nameserver.py &
```

### Cherrypy Server
Start the Flask server in the background:
```bash
cd samples/opentraveldata/python-db/cherrypy/
python tracker_manager.py &
```

### WS API - Read
The following script allows to list all the notification events stored in the database:
```bash
curl -i -X GET http://localhost:5000/notification_events
[{"check_frequency": 1440, "thshd_lower": 0.70, "notification_list": "john@doe.me", "thshd_upper": 1.20, "content": "{\"notified_address_list\": \"john@doe.me\"}", "timestamp": "2016-02-01T08:00:00", "tag_list": "\"file\", \"opentraveldata\", \"optd_airline_por.csv\""}, {"check_frequency": 1440, "thshd_lower": 0.70, "notification_list": "john@doe.me", "thshd_upper": 1.20, "content": "{\"notified_address_list\": \"john@doe.me\"}", "timestamp": "2016-02-01T09:00:00", "tag_list": "\"file\", \"opentraveldata\", \"optd_airlines.csv\""}]
```

### WS API - Add
The following script allows to add a notification event in the database:
```bash
curl -i -H "Content-Type: application/json" -X POST -d '{"timestamp": "2016-02-05 20:00:00", "tag_list": "\"file\", \"opentraveldata\", \"optd_airlines.csv\"", "content": "{\"notified_address_list\": \"john@doe.me\"}"}' http://localhost:5000/notification_events/
```
Check that the item has been inserted:
```bash
curl -i -X GET http://localhost:5000/notification_events
[{"check_frequency": 1440, "thshd_lower": 0.70, "notification_list": "john@doe.me", "thshd_upper": 1.20, "content": "{\"notified_address_list\": \"john@doe.me\"}", "timestamp": "2016-02-01T08:00:00", "tag_list": "\"file\", \"opentraveldata\", \"optd_airline_por.csv\""}, {"check_frequency": 1440, "thshd_lower": 0.70, "notification_list": "john@doe.me", "thshd_upper": 1.20, "content": "{\"notified_address_list\": \"john@doe.me\"}", "timestamp": "2016-02-01T09:00:00", "tag_list": "\"file\", \"opentraveldata\", \"optd_airlines.csv\""}, {"check_frequency": 1440, "thshd_lower": 0.70, "notification_list": "john@doe.me", "thshd_upper": 1.20, "content": "{\"notified_address_list\": \"john@doe.me\"}", "timestamp": "2016-02-05T20:00:00", "tag_list": "\"file\", \"opentraveldata\", \"optd_airlines.csv\""}]
```

### WS API - Update
The following script allows to update a notification event in the database:
```bash
curl -i -H "Content-Type: application/json" -X PUT -d '{"timestamp": "2016-02-05 20:00:00", "tag_list": "\"file\", \"opentraveldata\", \"optd_airline_por.csv\"", "content": "{\"notified_address_list\": \"john@doe.me\"}"}' 'http://localhost:5000/notification_events/2016-02-05 20:00:00'
```

### WS API - Delete
The following script allows to delete a notification event in the database:
```bash
curl -i -X DELETE 'http://localhost:5000/notification_events/2016-02-05 20:00:00'
```
