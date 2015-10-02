PEP Page Generation
===================

.. _pep_process:

Process Overview
----------------

We are generating the PEP pages by lightly parsing the HTML output from the
`PEP Repository`_ and then cleaning up some post-parsing formatting.

The PEP Page Generation process is as follows:

1. Set ``PEP_REPO_PATH`` in ``pydotorg/settings/local.py`` to the location
   of the `PEP Repository`_.
2. Run ``pep2html.py``
3. Run ``genpepindex.py``
4. After all PEP pages are generated into HTML, run::

   $ ./manage.py generate_pep_pages

This process runs periodically via cron to keep the PEP pages up to date.

Management Commands
-------------------

generate_pep_pages
^^^^^^^^^^^^^^^^^^

This Django management command generates ``pages.Page`` objects from the output
of the existing PEP repository generation process. You run it like::

    $ ./manage.py generate_pep_pages

To get verbose output run it like::

    $ ./manage.py generate_pep_pages --verbosity=2

It uses the conversion code in the ``peps.converters`` module in an attempt to
normalize the formatting for display purposes.

dump_pep_pages
^^^^^^^^^^^^^^

This simply dumps our PEP related pages as JSON. The ``dumpdata`` content is
written to ``stdout`` just like a normal ``dumpdata`` command.

.. _PEP Repository: https://hg.python.org/peps/
