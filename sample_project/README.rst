===============================
Running the example application
===============================

We assume you are using poetry. Follow these steps to download and run the
solid-backend example application in this directory:

::
	
	
	$ git clone https://github.com/zentrumnawi/solid-backend.git
	$ cd solid-backend/sample_project
	$ poetry install # this will find the pyproject.toml in the directory above


::

Now, since this project uses a PostgreSQL database, you need to manually create a database
(this is not done automatically by django). You can do so by Installing PostgreSQL and the following
steps:

::


	$ sudo su - postgres
	postgres@my-pc:~$ psql
	# We are now in the PostgreSQL-DB shell
	postgres=# CREATE DATABASE local_db;
	postgres=# CREATE USER localuser WITH PASSWORD 'localpass';
	postgres=# GRANT ALL PRIVILEGES ON DATABASE local_db TO localuser;
	postgres=# \q
	postgres@my-pc:~$ exit
	
	
::


At this point a note for troubleshooting: It might happen that PostgreSQL isn't running
on port 5432 (default port) which the example application assumes. If so, the following 
Error is encountered during the next steps.

::

	psycopg2.OperationalError: FATAL:  password authentication failed for user "localuser"
	FATAL:  password authentication failed for user "localuser"

::

So, now to the last steps: Migrate and Superuser creation.

::

	$ poetry run python manage.py migrate
	$ poetry run python manage.py createsuperuser

::

Finally start the developments server and you are good to go:

::

	$ poetry run python manage.py runserver_plus

::

After that step you should be able to open your browser on http://localhost:8000/admin and see
the admininterface.



