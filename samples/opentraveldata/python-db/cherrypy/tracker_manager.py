import cherrypy
import decimal
import simplejson as json
import MySQLdb
from datetime import datetime

#
tracker_list = dict()
notification_list = dict()

# Build the standard select query
query_get_nl = "select ne.timestamp as ts, ne.tag_list as tl, "
query_get_nl += "tck.check_frequency as cf, tck.thshd_lower as tl, tck.thshd_upper as tu, "
query_get_nl += "tck.notification_list as nl, ne.content as ct "
query_get_nl += "from sdq_sdq.trackers as tck, "
query_get_nl += "sdq_sdq.notification_events as ne "
query_get_nl += "where ne.tag_list = tck.tag_list"

#
def json_serial (obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

#
def addNotificationEvent (row):
    timestamp = row[0]
    tag_list = row[1]
    content = row[6]

    print row

    #
    if not tag_list in notification_list:
        notification_list[tag_list] = dict()

    #
    notification_list[tag_list][json_serial(timestamp)] = content
    return (tag_list, timestamp, content)

#
class NotificationEvents:

    exposed = True

    # Read
    def GET (self, tag_list=None):
        # Connection to the database
        db = MySQLdb.connect (host='localhost', user='sdq', passwd='sdq',
                              db='sdq_sdq')
        cursor = db.cursor()

        if tag_list is None:
            #
            cursor.execute (query_get_nl)

            for row in cursor.fetchall():
                (tag_list, timestamp, content) = addNotificationEvent (row)
                # print ("tl: %s; ts: %s; ct: %s" % (tag_list, timestamp, content))


            data = json.dumps (notification_list, default=json_serial)
            db.close()
            print data
            #return ("The whole list: " + str(notification_list))
            return data

        else:
            #
            query_get_evt = query_get_nl + " and ne.tag_list = '" + tag_list + "'"
            cursor.execute (query_get_evt)

            for row in cursor.fetchall():
                (tag_list, timestamp, content) = addNotificationEvent (row)
                print ("tl: %s; ts: %s; ct: %s" % (tag_list, timestamp, content))

            db.close()
            return ("With ID")

    # Add
    def POST (self, timestamp, tag_list, content):
        # Build the insert query
        query_add_evt = ("INSERT INTO sdq_sdq.notification_events (timestamp, tag_list, content) VALUES (%s, %s, %s)" % (timestamp, tag_list, content))

        return ('Created a notification event with: %s; %s' % (tag_list, timestamp))

    # Update
    def PUT (self, tag_list, timestamp, content=None):
        #
        query_get_evt = query_get_nl + " and ne.tag_list = '" + tag_list + "'"
        cursor.execute (query_get_evt)
        for row in cursor.fetchall():
            (tag_list, timestamp, content) = addNotificationEvent (row)
            print ("tl: %s; ts: %s; ct: %s" % (tag_list, timestamp, content))

        return ('Update tl: %s; ts: %s with ct: %s' % (tag_list, timestamp, content))

    # Delete
    def DELETE (self, tag_list, timestamp):
        return ('Delete tl: %s; ts: %s' % (tag_list, timestamp))

# Main
if __name__ == '__main__':

    cherrypy.tree.mount (
        NotificationEvents(), '/api/notification_events',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
         }
    )

    cherrypy.engine.start()
    cherrypy.engine.block()
