# BookIt
# Introduction
BookIt aims to be a one-stop shop for resources you wish to provide or make a booking for.
It allows providers to register the resources they can make available to consumers on the
platform. Consumers can then look for available resources that they're interested in, view
their details, and place a booking for resources they are interested in as long as it falls within
their monthly booking allowance of 10 booking hours. These consumers can browse through
their bookings, and express their content with a resource they've completed one or more
bookings for by liking it on the platform, or cancel an upcoming booking if they no longer
need it. BookIt also provides consumers with recommendations for resources they haven't
booked yet - but may wish to. See the project objectives for further details on what this
platform must be able to do.
# Project Objectives
Resource providers can register their name, contact details, and a description of the types of
resources they provide (eg: tennis courts, meeting rooms, and/or other resources).
Registered providers must be able to specify the name, type, location, description, and
availability for each of their resources with hourly granularity (eg for a resource: (name:
tennis court 1), (type: Tennis Court), (location: 1 Example Rd, Sydney, NSW 2000, Australia),
(description: indoor tennis court), (available: Mondays to Fridays 8am to 8pm)). Resource
consumers must be able to register to find and book the resources they are interested in,
where they can search for resources available within a given time period by keywords that
match on any combination of the name, type, description, and/or location (note: a resource
is not available at a given time if it has already been booked at that time). Once a consumer
has identified a resource they are interested in, they must be able to view its full details,
including its name, type, location, description, full availability on a calendar (showing
booked & available times), as well as the provider details. When a consumer is happy with
the details for a resource, they must be able to book the resource for 1 or more timeperiods of hourly granularity, when the resource is currently available (once booked, the
resource would become unavailable for the booking time-periods), with each consumer
being given an allowance of 10 hours per calendar month for bookings (ie: no consumer
should have more than 10 hours in total worth of bookings within any given month).
Consumers must be able to view all of their past, current, and upcoming bookings, and be
able to like only bookings that have occurred in the past (where booking end time is in the
past). Consumers can change their mind, so they must be able to cancel any of their
resource bookings if the first day of their booking is more than 3 days away. BookIt must be
able to recommend to a consumer resources they haven't booked yet, based on resource
likes they have in common with other consumers, and other resources that these other
consumers have liked but which the consumer getting the recommendations hasn't booked
yet; as well as based on any 1 other factor that can determine resources that a consumer is
likely to want to book.


## Set up instructions

After pulling the project from Github, please follow the following steps:

For database:

step0: Install MySQL(https://dev.mysql.com/downloads/mysql/) in your local environment

step1: Initialize the database and set password **12345678** for the user **root**

step2: Open a terminal, go into the 'capstoneproject-comp3900-w18a-default' folder, run 

```
chmod +x create_db.sh
```

step3: then, run 

```
./create_db.sh
```

 and enter the password **12345678**

For Backend server:

step0: Download python 3.7 or python 3.8 in order to run the project.

step1: Open a terminal, go into the 'capstoneproject-comp3900-w18a-default' folder,  create a virtual environment by 

```
python3 -m venv env
```

step2: In the same terminal,  activate the virtual environment.

```
 source env/bin/activate
```

step3:  install all packages we need.

```
pip install -r requirement.txt
```

Step4: run the project

```
python3 app.py
```

You can deactivate the virtual environment by typing **deactivate** in the terminal.

 

The website in now running on **http://127.0.0.1:5000/ ,** please copy and paste it into your web browser to use our website.
