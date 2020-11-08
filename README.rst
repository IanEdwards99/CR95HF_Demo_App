============================================================
Demonstrator Application for nfcreader API for CR95HF module
============================================================


.. image:: https://img.shields.io/pypi/v/nfcreader.svg
        :target: https://pypi.python.org/pypi/nfcreader

.. image:: https://readthedocs.org/projects/CR95HF_Demo_App/badge/?version=latest
        :target: https://nfcreader.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Python demonstration application for CR95HF NFC Reader API for an access control use-case.

* Free software: MIT license
* Documentation: https://nfcreader.readthedocs.io.

Abstract
--------
The aim was to provide better support for the CR95HF's use for the Raspberry Pi in Python3, via an API.
Thus an API was developed here: https://github.com/IanEdwards99/nfcreader

Features of Demonstrator Application
------------------------------------
- Automatic USB Connect
- Protocol Select (Select between ISO15693, ISO14443-A, ISO14443-B, and ISO18092)
- Inventory command on tag (request ID and tag information from tag.)
- Enter tag hunting mode (Looks for a tag for 5 seconds before timeout.)
- Read a block from a tag (Specify address to read from 0 to 128.) Tag must be present.
- Write a block to a tag (Specify address to write to, and data to write.) Tag must be present.
- Access control demo (contiuously scans for registered tags.)
- Scan till written to a tag (Enter data to write, and scans continuously till tag is in range and writes.)
- Print authorized tag access history (print out log of all tags successfully read.)
- Read entire tag contents (Place tag on reader and read entire contents in all address locations.)
- Add tag access (for access control demo purposes.)
- Clean tag (wipe all address locations clean.)
- Reset SPI connection to NFC reader from Pi.
- Exit demonstrator.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
