python_ipc_queue
================

An inter-process queue implemented using pure Python.

Based on the [example](https://docs.python.org/2/library/multiprocessing.html#using-a-remote-manager) included in the document of multiprocessing module.

Works with Python 2.7 or later.

Usage
=====

Server side:
```
>>> import queue_server
>>> queue_server.start_server()
>>> queue_server.get_one()
(True, 'hello')
```

Client side:
```
>>> import queue_client
>>> queue_client.reconnect()
True
>>> queue_client.send_request('hello')
True
```

License
=======

Copyright 2015 Matt Jones <mattjones1811@hotmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
