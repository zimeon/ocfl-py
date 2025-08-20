Installing ``ocfl-py``
======================

Installation of ``ocfl-py`` gives access to both the `command line tools
<command_line.html>`_ and the `ocfl Python module
<api.html>`__.

Install with ``pip``
--------------------

To install or update ``ocfl-py``, simply run this command in your terminal of choice::

    > python -m pip install --upgrade ocfl-py

Get the source code
-------------------

``ocfl-py`` development happens on `GitHub
<https://github.com/zimeon/ocfl-py>`__ and the latest updates are always available from there in the `main` branch. See also `ocfl-py releases
<https://github.com/zimeon/ocfl-py/releases>`_.

You can clone the public repository::

  > git clone https://github.com/zimeon/ocfl-py.git

Or, download the ``main`` branch as a ``tar.gz`` file::

  > curl -L -o ocfl-py.tar.gz https://github.com/zimeon/ocfl-py/archive/refs/heads/main.tar.gz

or a ``zip`` file::

  > curl -L -o ocfl-py.zip https://github.com/zimeon/ocfl-py/archive/refs/heads/main.zip

Once you have a copy of the source, you can embed it in your own Python package, or install it into your site-packages easily::

  > cd ocfl-py
  > python -m pip install .
