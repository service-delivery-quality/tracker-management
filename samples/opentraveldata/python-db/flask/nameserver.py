from flask import Flask
from flask import g
from flask import Response
from flask import request
import flask.json
import decimal
import simplejson as json
import MySQLdb
from datetime import datetime
#enabling of cors
from flask.ext.cors import CORS

app = flask.Flask (__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

#

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

# Override the JSON encoder of Flask
class MyFlaskJSONEncoder (flask.json.JSONEncoder):
    def default (self, obj):
        if isinstance (obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super (MyFlaskJSONEncoder, self).default(obj)

app.json_encoder = MyFlaskJSONEncoder

@app.before_request
def db_connect():
  flask.g.conn = MySQLdb.connect (host='localhost',
                                  user='sdq',
                                  passwd='sdq',
                                  db='sdq_sdq')
  flask.g.cursor = flask.g.conn.cursor()

@app.after_request
def db_disconnect(response):
  flask.g.cursor.close()
  flask.g.conn.close()
  return response

def query_db(query, args=(), one=False):
  flask.g.cursor.execute(query, args)
  rv = [dict((flask.g.cursor.description[idx][0], value)
             for idx, value in enumerate(row))
        for row in flask.g.cursor.fetchall()]
  return (rv[0] if rv else None) if one else rv

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/notification_events", methods=['GET'])
def get():
  result = query_db("SELECT ne.timestamp, ne.tag_list, tck.check_frequency, tck.thshd_lower, tck.thshd_upper, tck.notification_list, ne.content FROM sdq_sdq.trackers as tck, sdq_sdq.notification_events as ne where ne.tag_list = tck.tag_list")
  data = json.dumps (result, default=json_serial)
  resp = flask.Response(data, status=200, mimetype='application/json')
  return resp

@app.route("/notification_events/", methods=['POST'])
def post():
  req_json = flask.request.get_json()
  flask.g.cursor.execute ("INSERT INTO sdq_sdq.notification_events (timestamp, tag_list, content) VALUES (%s, %s, %s)",
                          (req_json['timestamp'], req_json['tag_list'], req_json['content']))
  flask.g.conn.commit()
  resp = flask.Response ("Record added", status=201, mimetype='application/json')
  return resp

# Does not work yet
@app.route("/notification_events/", methods=['DELETE'])
def delete():
  req_json = flask.request.get_json()
  flask.g.cursor.execute ("DELETE FROM sdq_sdq.notification_events WHERE timestamp = %s",
                          (req_json['timestamp']))
  flask.g.conn.commit()
  resp = flask.Response ("Record deleted", status=201, mimetype='application/json')
  return resp

# Main
if __name__ == "__main__":
  app.run(debug=True)
