**************
Network
**************

Introduction
============

We use a thin client, that has little to no knowledge about the game mechanics. Communication with the server is via TCP and messages. Messages are simple data structures that are being sent between client and server. They can also be seen as updates or events. The underlying library Qt signals new messages which are then serialized/deserialized (zipped/unzipped). Internally messages are handled by setting listeners to channels.

The server listens on a port, each client is connected to the server by a connection. However clients could be disconnect(ed) during the process, so we must allow re-connection.

Server
======

* Upon start the server binds to a port, then listens for incoming connections.
* Every new connection is assigned a temporary status.A validation message is sent (regularly) which invalidates the state. If correct return comes, status is kept valid.
* Client should send ID (for re-connecting) or request to get new ID.

Client
======
