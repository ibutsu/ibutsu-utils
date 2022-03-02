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

- `Upload test runs - ibutsu-upload <#upload-tool>`_
- `Combine JUnit XML files - ibutsu-xmerge <#combine-tool>`_

Installation
------------

These utilities are available on `PyPI <https://pypi.org/ibutsu-utils>`_ and can be installed with
``pip``::

   $ pip install ibutsu-utils


Upload Tool
-----------

The ``ibutsu-upload`` command line tool uploads JUnit XML or Ibutsu archives to Ibutsu.

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


Combine Tool
------------

Some test runners output multiple JUnit XML files for a single test run. The ``ibutsu-xmerge``
utility will combine multiple XML files into a single file.

.. code-block::

   $ ibutsu-xmerge --help
   usage: ibutsu-xmerge [-h] [-o OUTPUT] input [input ...]

   positional arguments:
     input                 Input files

   options:
     -h, --help            show this help message and exit
     -o OUTPUT, --output OUTPUT
                           Output to a file. Defaults to stdout without this.
