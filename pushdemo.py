import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extensions import parse_dsn
import os
from urllib.parse import urlparse

import eventlet
from eventlet import wsgi
from eventlet import websocket
from eventlet.hubs import trampoline

dsn = os.environ['DATABASE_URL']
result = urlparse(dsn)
dbname = result.path[1:]
user = result.username
password = result.password
host = result.hostname

def dblisten(q):
    """
    Open a db connection and add notifications to *q*.
    """
    cnn = psycopg2.connect(dbname = dbname, 
                           user = user, 
                           host = host, 
                           password = password)
    cnn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = cnn.cursor()
    cur.execute("LISTEN new_user;")
    while 1:
        trampoline(cnn, read=True)
        cnn.poll()
        while cnn.notifies:
            n = cnn.notifies.pop()
            q.put(n)

@websocket.WebSocketWSGI
def handle(ws):
    """
    Receive a connection and send it database notifications.
    """
    q = eventlet.Queue()
    eventlet.spawn(dblisten, q)
    while 1:
        n = q.get()
        print(n)
        ws.send(n.payload)

def dispatch(environ, start_response):
    if environ['PATH_INFO'] == '/new_user':
        return handle(environ, start_response)
    else:
        start_response('200 OK',
            [('content-type', 'text/html'),('Access-Control-Allow-Origin', '*')])
        return [page]

page = """
<html>
  <head><title>pushdemo</title>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.1/jquery.min.js" crossOrigin="anonymous"></script>
    <style type="text/css">
      .bar {width: 20px; height: 20px;}
    </style>
    <script>
      window.onload = function() {
        ws = new WebSocket("ws://localhost:7000/new_user");
        ws.onmessage = function(msg) {
          bar = $('#' + msg.data);
          bar.width(bar.width() + 100);
          document.getElementById('audiotag1').play();
        }
      }
    </script>
    

      
    
  </head>
  <body>
    <audio id="audiotag1" src="doorbell.mp3" preload="auto" crossOrigin="anonymous"></audio>
    <div style="width: 800px;">
      <div id="red" class="bar"
          style="height:100px; background-color: red;">&nbsp;</div>
      <div id="green" class="bar"
          style="background-color: green;">&nbsp;</div>
      <div id="blue" class="bar"
          style="background-color: blue;">&nbsp;</div>
    </div>
    
    
  </body>
</html>
"""

if __name__ == "__main__":
    listener = eventlet.listen(('127.0.0.1', 7000))
    wsgi.server(listener, dispatch)


