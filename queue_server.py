# requires python 2.7 or later
"""
queue_server
============

This module provides a server which holds a multiprocessing.Queue object.

Multiple clients can connect to one server and get the queue object to
send requests to the server process.

The module provides following functions:
    start_server():
        To start the queue server.

    get_one():
        To get one request from the queue. This function will block if the
        queue is currently empty.
        The function returns a tuple (successful, request).

    cancel_wait():
        If a thread is currently blocked by get_one() function, this will
        make the function return immediately.

To access the multiprocessing.Queue object directly, just use:
    queue_server.shared_queue

Configurations of the server is located in queue_global module including
the address, port and authentication key of the server.

The server runs in a separate daemon thread and will not block the hosting
process when the process tries to quit.

"""

import sys
import os
import logging
import threading

from multiprocessing import Queue
from multiprocessing.managers import BaseManager

# server configurations
from queue_global import SERVER_CONFIG

__all__ = ['start_server', 'get_one', 'cancel_wait', 'shared_queue']

# just set up a null logger
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# the queue object with max size of 100
shared_queue = Queue(100)

# server manager class
class ServerManager(BaseManager): pass

# register get_shared_queue() method
ServerManager.register('get_shared_queue', callable=lambda: shared_queue)

def server_thread():
    logger.debug('Start server thread...')

    try:
        m = ServerManager(
            address=(SERVER_CONFIG['address'], SERVER_CONFIG['port']),
            authkey=SERVER_CONFIG['auth_key']
        )
        s = m.get_server()
        s.serve_forever()

    except Exception as e:
        sys.stderr.write(str(e) + '\n')

    sys.stderr.write('__error__: server exited.\n')
    os._exit(11)  # Queue server thread exited. Need to abort whole process.

class ServerThread:
    inst = None  # a reference to the sever thread instance

    def __init__(self):
        self._thread = threading.Thread(target=server_thread)
        self._thread.daemon = True
        self._thread.start()

def start_server():
    """Start the queue server."""
    if ServerThread.inst is None:
        ServerThread.inst = ServerThread()

def get_one():
    """Get one request from the queue."""
    try:
        request = shared_queue.get()
    except:
        logger.error('Cannot get request from queue.')
        return False, None
    return True, request

def cancel_wait():
    """Make get_one() return immediately."""
    shared_queue.put(None)  # just insert a None object to the queue
