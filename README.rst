=============
 ztcli-async
=============

|ci| |wheels| |release| |badge| |coverage|

|pre| |cov| |pylint|

|tag| |license| |python|

ztcli-async is a thin async Python client wrapper for the zerotier-cli
node API (mainly based on `zerotier-client`_ and the `ZeroTier API doc`_).
ztcli-async works with all node types, eg root (aka moon), network controller,
and user nodes.

.. _zerotier-client: https://github.com/fabaff/zerotier-client
.. _ZeroTier API doc: https://zerotier.com/manual/


Getting Started
===============

This is a Python thin client interface to the zerotier JSON API, only some
of which is exposed by the ``zerotier-cli`` command-line interface.
Packages are available for `Debian and Ubuntu`_, and the latest can be
installed on Gentoo using the ebuilds in `this portage overlay`_.


.. _Debian and Ubuntu: https://launchpad.net/~nerdboy/+archive/ubuntu/embedded
.. _this portage overlay: https://github.com/VCTLabs/embedded-overlay/dev-libs/ztcli-async/


Prerequisites
-------------

In Theory, this software should work on anything with a working ZeroTier
package and Python, including most BSDs, Unix/Linux, MacOS, and Windows.
That said, it has really only been tested on the Linux variants below.

Existing Packages
-----------------

Packages are available for some (tested) linux distributions, mainly
something that uses either ``.ebuilds`` (eg, Gentoo or funtoo) or ``.deb``
packages, starting with at least Ubuntu xenial or Debian stretch (see
the above PPA package repo on Launchpad).

For the latter, make sure you have the ``add-apt-repository`` command
installed and then add the PPA:

::

  $ sudo apt-get install software-properties-common
  $ sudo add-apt-repository -y -s ppa:nerdboy/embedded


.. note:: Since the package series currently published are for xenial,
          bionic, and focal, the second command above will need to be
          manually corrected afterwards if installing on Debian.


To install on Debian you *can* use the above method, but you will need
to edit the file under ``sources.d`` and set the distro to the "closest",
then run the update command:

::

  $ sudo apt-get update

If you get a key error you will also need to manually import the PPA
signing key like so:

::

  $ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys <PPA_KEY>

where <PPA_KEY> is the key shown in the launchpad PPA page under "Adding
this PPA to your system", eg, ``41113ed57774ed19`` for `Embedded device ppa`_.


.. _Embedded device ppa: https://launchpad.net/~nerdboy/+archive/ubuntu/embedded


Dev Install
-----------

As long as you have git and at least Python 3.6, then the "easy" dev
install is to clone this repository and install the latest zerotier package
(there are packages in the PPA and Gentoo overlay).  Check the version of
zerotier in the main portage tree; you will need at least version ``1.4.6:0``.

Do the usual install dance, either::

  # emerge zerotier

or::

  $ sudo apt-get install zerotier-one


After cloning this repository, you can try running the example scripts
from the source tree; if you have already installed this package, the
examples should run from any directory, otherwise you'll need to copy
the file you want to run to the top-level source tree first.

Without installing ztcli-async, first install the two package dependencies
listed below, then install zerotier and make sure the service has started.
You can check the zerotier client state with::

  $ sudo zerotier-cli info

which should respond with::

  200 info <your ID> 1.4.6 ONLINE

If the above is working, you can try one of the examples:

::

  $ git clone https://github.com/sarnold/ztcli-async
  $ cd ztcli-async
  $ sudo python3 examples/pprint_data.py


.. note:: By default you will not have correct permissions to access the
          local zerotier node directly, due to the permissions on zerotier
          identity files.  You can either prefix the commands with ``sudo``,
          or add a usr ACL (for your local user) to the ``authtoken.secret``
          file.


Standards and Coding Style
--------------------------

Currently pep8 and flake8 are the only tests besides some CI code analysis
checks for complexity and security issues (we try to keep the "cognitive
complexity" low when possible).


User Install / Deployment
=========================

Use the latest ztcli-async package for your Linux distro and hardware
architecture; all arch-specific packages should support at least the
following:

* armhf/arm
* aarch64/arm64
* x86_64/amd64
* i686/x86


Software Stack and Tool Dependencies
====================================

* `Python`_ - at least version 3.6
* `async_timeout`_ - timeout context manager for asyncio
* `aiohttp`_ - http client/server for asyncio
* `ZeroTier`_ - network virtualization engine

.. _Python: https://docs.python.org/3.5/index.html
.. _async_timeout: https://github.com/aio-libs/async-timeout
.. _aiohttp: https://pypi.org/project/aiohttp/
.. _ZeroTier: https://www.zerotier.com/



Versioning
==========

We use `SemVer`_ for versioning. For the versions available, see the
`releases in this repository`_.

.. _SemVer: http://semver.org/
.. _releases in this repository: https://github.com/sarnold/ztcli-async/releases


Contributing
============

Please read `CONTRIBUTING.rst`_ for details on the code of conduct and the
process for submitting pull requests.

.. _CONTRIBUTING.rst: https://github.com/sarnold/ztcli-async/CONTRIBUTING.rst


Authors
=======

* **Stephen Arnold** - *Current implementation and packaging* - `nerdboy`_
* **Fabian Affolter** - *Original implementation* - `fabaff`_

.. _nerdboy: https://github.com/sarnold/
.. _fabaff: https://github.com/fabaff/


License
=======

This project is licensed under the MIT license - see the `LICENSE file`_ for
details.

.. _LICENSE file: https://github.com/sarnold/ztcli-async/blob/master/LICENSE


Acknowledgments
===============

* Thanks to Fabian for the clean original client implementation and inspiration
* Thanks to the ZeroTier project for providing the network virtualization engine

.. |ci| image:: https://github.com/sarnold/ztcli-async/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/sarnold/ztcli-async/actions/workflows/ci.yml
    :alt: CI Status

.. |wheels| image:: https://github.com/sarnold/ztcli-async/actions/workflows/wheels.yml/badge.svg
    :target: https://github.com/sarnold/ztcli-async/actions/workflows/wheels.yml
    :alt: Wheel Status

.. |coverage| image:: https://github.com/sarnold/ztcli-async/actions/workflows/coverage.yml/badge.svg
    :target: https://github.com/sarnold/ztcli-async/actions/workflows/coverage.yml
    :alt: Coverage workflow

.. |badge| image:: https://github.com/sarnold/ztcli-async/actions/workflows/pylint.yml/badge.svg
    :target: https://github.com/sarnold/ztcli-async/actions/workflows/pylint.yml
    :alt: Pylint Status

.. |release| image:: https://github.com/sarnold/ztcli-async/actions/workflows/release.yml/badge.svg
    :target: https://github.com/sarnold/ztcli-async/actions/workflows/release.yml
    :alt: Release Status

.. |cov| image:: https://raw.githubusercontent.com/sarnold/ztcli-async/badges/master/test-coverage.svg
    :target: https://github.com/sarnold/ztcli-async/
    :alt: Test coverage

.. |pylint| image:: https://raw.githubusercontent.com/sarnold/ztcli-async/badges/master/pylint-score.svg
    :target: https://github.com/sarnold/ztcli-async/actions/workflows/pylint.yml
    :alt: Pylint score

.. |license| image:: https://img.shields.io/github/license/sarnold/ztcli-async
    :target: https://github.com/sarnold/ztcli-async/blob/master/LICENSE
    :alt: License

.. |tag| image:: https://img.shields.io/github/v/tag/sarnold/ztcli-async?color=green&include_prereleases&label=latest%20release
    :target: https://github.com/sarnold/ztcli-async/releases
    :alt: GitHub tag

.. |python| image:: https://img.shields.io/badge/python-3.6+-blue.svg
    :target: https://www.python.org/downloads/
    :alt: Python

.. |pre| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
