import psycopg2 
import os


from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from eventlet.hubs import trampoline

DB_URL = os.environ['DATABASE_URL']


def dblisten(q):
    """
    Open a db connection and add notifications to *q*.
    """
    cnn = psycopg2.connect(DB_URL)
    cnn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = cnn.cursor()
    cur.execute("LISTEN data;")
    while 1:
        trampoline(cnn, read=True)
        cnn.poll()
        while cnn.notifies:
            n = cnn.notifies.pop()
            q.put(n)