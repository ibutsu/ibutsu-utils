.. image:: https://img.shields.io/github/v/release/ibutsu/ibutsu-utils
   :target: https://github.com/ibutsu/ibutsu-utils/releases

.. image:: https://img.shields.io/pypi/v/ibutsu-utils.svg
   :target: https://pypi.org/project/ibutsu-utils

.. image:: https://img.shields.io/pypi/pyversions/ibutsu-utils.svg
   :target: https://pypi.org/project/ibutsu-utils

Ibutsu Utilities
================

Some command line utilities for `Ibutsu <https://ibutsu-project.org/>`_. There are currently two
tools:

- `Download artifacts - ibutsu-download <#download-tool>`_
- `Upload test runs - ibutsu-upload <#upload-tool>`_
- `Combine JUnit XML files - ibutsu-xmerge <#combine-tool>`_

Installation
------------

These utilities are available on `PyPI <https://pypi.org/ibutsu-utils>`_ and can be installed with
``pip``::

   $ pip install ibutsu-utils

Download Tool
-------------

The ``ibutsu-download`` command line tool downloads an artifact from Ibutsu.

Usage
~~~~~

.. code-block::

   $ ibutsu-download -h
   usage: ibutsu-download [-h] -H HOST [-t API_TOKEN] [-o OUTPUT] artifact_id

   A tool to download an artifact from an Ibutsu server

   positional arguments:
     artifact_id           The ID of the artifact to download

   options:
     -h, --help            show this help message and exit
     -H HOST, --host HOST  The Ibutsu instance for uploading, e.g. https://my.ibutsu.com/api
     -t API_TOKEN, --api-token API_TOKEN
                           An API token for authentication
     -o OUTPUT, --output OUTPUT
                           The destination to save the file. If omitted will use the current directory and the artifact file name

Example
~~~~~~~

.. code-block::

   $ ibutsu-download --host https://my.ibutsu.com/api --token AwEdE...4GyT --output errors.log ea8550e2-7eeb-4b4e-8a31-92d8a3e1169c

Upload Tool
-----------

The ``ibutsu-upload`` command line tool uploads JUnit XML or Ibutsu archives to Ibutsu.

Usage
~~~~~

.. code-block::

   $ ibutsu-upload --help
   usage: ibutsu-upload [-h] -H HOST -p PROJECT [-t API_TOKEN] [-s SOURCE] [-m METADATA] [-w] input [input ...]

   A tool to upload a jUnit XML or Ibutsu archive to Ibutsu

   positional arguments:
     input                 The file(s) to upload

   options:
     -h, --help            show this help message and exit
     -H HOST, --host HOST  The Ibutsu instance for uploading, e.g. https://my.ibutsu.com/api
     -p PROJECT, --project PROJECT
                           The project for the upload
     -t API_TOKEN, --api-token API_TOKEN
                           An API token for authentication
     -s SOURCE, --source SOURCE
                           The source used in the test results
     -m METADATA, --metadata METADATA
                           Additional metadata to set when uploading, in the format of dotted.key.path=value
     -w, --wait            Wait for the upload to complete (by default this command does not wait)

Example
~~~~~~~

.. code-block::

   $ ibutsu-upload --host https://my.ibutsu.com/api --token AwEdE...4GyT --project ibutsu-server --source jenkins-run-tests-53 --metadata component=frontend --metadata env=prod --metadata durations.call=34.405 --metadata durations.setup=0.0005 --metadata durations.teardown=0.689 --metadata markers=core,smoke,frontend --wait 550aed75-b214-4d17-983d-fe0829311b98.tar.gz

The above ``--metadata`` arguments will populate the ``metadata`` field in the run object:

.. code-block:: json

   {
     "metadata": {
       "component": "frontend",
       "env": "prod",
       "durations": {
         "call": 34.405,
         "setup": 0.0005,
         "teardown": 0.689
       },
       "markers": [
         "core",
         "smoke",
         "frontend"
       ]
     },
   }

Combine Tool
------------

Some test runners output multiple JUnit XML files for a single test run. The ``ibutsu-xmerge``
utility will combine multiple XML files into a single file.

Usage
~~~~~

.. code-block::

   $ ibutsu-xmerge --help
   usage: ibutsu-xmerge [-h] [-o OUTPUT] input [input ...]

   positional arguments:
     input                 Input files

   options:
     -h, --help            show this help message and exit
     -o OUTPUT, --output OUTPUT
                           Output to a file. Defaults to stdout without this.

Example
~~~~~~~

.. code-block::

   $ ibutsu-xmerge --output ../merged.xml *.xml
