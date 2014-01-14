tx_tecreports
=============
Python code for interacting with `Texas Ethics Commission`_ reports

.. note:: This does not account for all of the variations in all reports (yet).
          This message will stay here until it does.

Installation & Configuration
----------------------------
You can install this using `pip`_ like this:

::

    pip install tx_tecreports

Now you're ready to start using ``tx_tecreports``.


Usage
-----
``tx_tecreports`` parses campaign finance reports from the
`Texas Ethics Commission`_.  You use the ``tx_tecreports.fetcher.get_report``
like this.

.. code:: python

    >>> from tx_tecreports.fetcher import get_report

You can fetch any report so long as you have the correct ID.  For
example, you could grab Wendy Davis' first special session report
(the first one filed after her filibuster) with the ID ``581606``.
You can find that ID by visiting her `filer page`_ on the
`Texas Ethics Commission`_ website.

.. code:: python

    >>> report = get_report(581606)

Now you can interact with the various data in the cover element via
``report.cover``.

.. code:: python

    >>> report.cover.type_of_filing
    'COH-SS'
    >>> report.cover.is_original
    True
    >>> report.cover.through_date - report.cover.from_date
    datetime.timedelta(29)

You can verify that this is her personal filing by seeing that
the filer_type is a `IND`:

.. code:: python

    >>> report.cover.filer.filer_type
    'IND'

The really interesting data is in the ``receipts`` property, a list
of all of the contributions received in this report.  For example,
you can see how many contributions where made by looking at its
length:

.. code:: python

    >>> len(report.receipts)
    1240

You can create a list of all of the contributions on any given day
with by looking at the ``contribution.date`` like this:

.. code:: python

    >>> len([a for a in report.receipts if a.contribution.date == report.cover.from_date])
    0

Oops, looks like she didn't have any contributions on the first day
of that report.  Let's change it to the last day:

.. code:: python

    >>> len([a for a in report.receipts if a.contribution.date == report.cover.through_date])
    1187

That's more like it!

.. _Texas Ethics Commission: http://www.ethics.state.tx.us/
.. _filer page: http://www.ethics.state.tx.us/php/filer.php?acct=00062095COH
.. _pip: http://www.pip-installer.org/en/latest/
