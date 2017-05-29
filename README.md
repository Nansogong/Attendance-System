Attendance System
====
This is system that manage students attendance. Project for Software Engineering Class.


Build Status
----
| Service | Master | Develop |
| ---- |----- |----|
| Travis-Ci | [![Build Status](https://travis-ci.org/Nansogong/Attendance-System.svg?branch=master)](https://travis-ci.org/Nansogong/Attendance-System) | [![Build Status](https://travis-ci.org/Nansogong/Attendance-System.svg?branch=develop)](https://travis-ci.org/Nansogong/Attendance-System)|


Requirements
----
1. python 3.5+
1. flask
1. fabric3
1. mariadb

Installation
----
	$ python -m venv venv # virtualenv has to locate this project's root directory.
	$ source venv/bin/activate #if you use mac or linux
	$ pip install -r requirements.txt

Usage Fabric
-----
    $ fab develop run # develop server running
    $ fab develop stop # develop server stop
    $ fab localhost init_db # initialize database