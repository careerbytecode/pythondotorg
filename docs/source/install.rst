Installing
==========

Here are three ways to hack on python.org:

1. :ref:`docker-setup`
2. :ref:`vagrant-setup`
3. :ref:`manual-setup`

.. _docker-setup:

Docker Setup
------------

First, install Docker_ on your machine. The Docker installation will
include docker-compose which can be used to bring up the application:

::

    $ docker-compose up

docker-compose will bring up the application container and a PostgreSQL 
container. The website will be available at http://localhost:8000.

Each time changes are made to local files the application container
will need to be rebuilt:

::

    $ docker-compose up --build
    # You can also make changes inside the application container
    $ docker exec -it $(docker ps | grep "pythondotorg_web" | awk '{print $1}') /bin/ash

.. _Docker: https://docs.docker.com/install/

.. _vagrant-setup:

Vagrant Setup
-------------

First, install Vagrant_ (2.0+) and Ansible_ (2.0+) on your machine.
You should then be able to provision the Vagrant box.

::

    $ vagrant up

The box will be provisioned with a latest Python 3.6 version, a virtual
environment with all the requirements installed, and a database ready to use.

Once this is done it's time to create some data and start the development server
for the first time::

    # SSH into the Vagrant box.
    $ vagrant ssh
    # Go to the pythondotorg/ directory and activate the virtual environment.
    $ cd ~/pythondotorg
    $ . venv/bin/activate
    # Create initial data for the most used applications (optional).
    $ ./manage.py create_initial_data
    # Set a password for the superuser "cbiggles". This username and password
    # can be used to login to the admin environment.
    $ ./manage.py changepassword cbiggles
    # Run the server.
    $ ./manage.py runserver 0.0.0.0:8000

Now use your favorite browser to go to http://localhost:8001/. The admin pages
can be found at http://localhost:8001/admin/. You can use your superuser
credentials to log in to Django admin.

You will only need to run the following five commands the next time you want to
work on python.org::

    $ vagrant up
    $ vagrant ssh
    $ cd ~/pythondotorg
    $ . venv/bin/activate
    $ ./manage.py runserver 0.0.0.0:8000

.. _Vagrant: https://www.vagrantup.com/downloads.html
.. _Ansible: https://docs.ansible.com/ansible/intro_installation.html

.. _manual-setup:

Manual setup
------------

First, clone the repository::

    $ git clone git://github.com/python/pythondotorg.git

Then create a virtual environment::

    $ python3.6 -m venv venv

And then you'll need to install dependencies. You don't need to use ``pip3``
inside a Python 3 virtual environment::

    $ pip install -r dev-requirements.txt

*pythondotorg* will look for a PostgreSQL database named ``pythondotorg`` by
default. Run the following command to create a new database::

    $ createdb pythondotorg -E utf-8 -l en_US.UTF-8

.. note::

   If the above command fails to create a database and you see an error message
   similar to::

       createdb: database creation failed: ERROR:  permission denied to create database

   Use the following command to create a database with *postgres* user as the
   owner::

       $ sudo -u postgres createdb pythondotorg -E utf-8 -l en_US.UTF-8

   Note that this solution may not work if you've installed PostgreSQL via
   Homebrew.

   If you get an error like this::

       createdb: database creation failed: ERROR:  new collation (en_US.UTF-8) is incompatible with the collation of the template database (en_GB.UTF-8)

   Then you will have to change the value of the ``-l`` option to what your
   database was set up with initially.

To change database configuration, you can add the following setting to
``pydotorg/settings/local.py`` (or you can use the ``DATABASE_URL`` environment
variable)::

    DATABASES = {
        'default': dj_database_url.parse('postgres:///your_database_name'),
    }

If you prefer to use a simpler setup for your database you can use SQLite.
Set the ``DATABASE_URL`` environment variable for the current terminal session::

    $ export DATABASE_URL="sqlite:///pythondotorg.db"

.. note::

   If you prefer to set this variable in a more permanent way add the above
   line in your ``.bashrc`` file. Then it will be set for all terminal
   sessions in your system.

Whichever database type you chose, now it's time to run migrations::

    $ ./manage.py migrate

To compile and compress static media, you will need *compass* and
*yui-compressor*::

    $ gem install bundler
    $ bundle install

.. note::

   To install *yui-compressor*, use your OS's package manager or download it
   directly then add the executable to your ``PATH``.

To create initial data for the most used applications, run::

    $ ./manage.py create_initial_data

See :ref:`command-create-initial-data` for the command options to specify 
while creating initial data.

Finally, start the development server::

    $ ./manage.py runserver


Optional: Install Elasticsearch
-------------------------------

The search feature in Python.org uses Elasticsearch engine.  If you want to
test out this feature, you will need to install Elasticsearch_.

Once you have it installed, update the URL value of ``HAYSTACK_CONNECTIONS``
settings in ``pydotorg/settings/local.py`` to your local ElasticSearch server.

.. _Elasticsearch: https://www.elastic.co/downloads/elasticsearch


Generating CSS files automatically
----------------------------------

Due to performance issues of django-pipeline_, we are using a dummy compiler
``pydotorg.compilers.DummySASSCompiler`` in development mode. To generate CSS
files, use ``sass`` itself in a separate terminal window::

    $ cd static
    $ sass --compass --scss -I $(dirname $(dirname $(gem which susy))) --trace --watch sass/style.scss:sass/style.css

.. _django-pipeline: https://github.com/cyberdelia/django-pipeline/issues/313


Running tests
-------------

To run the test suite::

    $ ./manage.py test

To generate coverage report::

    $ coverage run manage.py test
    $ coverage report

Generate an HTML report with ``coverage html`` if you like.


Useful commands
---------------

* Create a super user (for a new DB)::

      $ ./manage.py createsuperuser

* Want to save some data from your DB before nuking it, and then load it back
  in?::

      $ ./manage.py dumpdata --format=json --indent=4 $APPNAME > fixtures/$APPNAME.json

