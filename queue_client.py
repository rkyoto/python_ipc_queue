# requires python 2.7 or later
"""
queue_client
============

This module provides client-side functions for the queue server module:
    reconnect():
        To reconnect to the queue server.
        The function returns True if successful.

    send_request(req):
        To send a request to the queue server.
        The function returns True if successful.

Configurations of the server is located in queue_global module including
the address, port and authentication key of the server.

"""

import logging
from multiprocessing.managers import BaseManager

# server configurations
from queue_global import SERVER_CONFIG

__all__ = ['reconnect', 'send_request']

# just set up a null logger
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# server manager class
class ServerManager(BaseManager): pass

# register get_shared_queue() method
ServerManager.register('get_shared_queue')

class QueueServer:
    inst = None  # a reference to the queue server instance

    def __init__(self, server, queue):
        self.server = server
        self.shared_queue = queue

def reconnect():
    """Reconnect to the queue server."""

    # discard previous connection
    QueueServer.inst = None

    try:
        # create server
        server = ServerManager(
            address=(SERVER_CONFIG['address'], SERVER_CONFIG['port']),
            authkey=SERVER_CONFIG['auth_key']
        )
        server.connect()

        # get shared queue
        shared_queue = server.get_shared_queue()
        QueueServer.inst = QueueServer(server, shared_queue)

    except Exception as e:
        logger.error(e)
        logger.error('Cannot connect to queue server.')

    return QueueServer.inst is not None

def send_request(req):
    """Send a request to the queue server."""

    if QueueServer.inst is None:
        logger.error('Server not connected.')
        return False

    try:
        QueueServer.inst.shared_queue.put(req)
    except:
        logger.error('Cannot send request to server.')
        return False

    return True
