Attendance System
====
This is system that manage students attendance. Project for Software Engineering Class.


Requirements
----
1. python 3.6+
1. flask
1. fabric3

Installation
----
	$ python -m venv venv # virtualenv has to locate this project's root directory.
	$ activate venv/bin/activate #if you use mac or linux
	$ pip install -r requirements.txt

Usage Fabric
-----
    $ fab develop run # develop server running
    $ fab develop stop # develop server stop
    $ fab localhost init_db # initialize database