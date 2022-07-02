.. _botping:

*******
BotPing
*******
**Detailed bot latency information.**

.. important::
    To use this cog, you will need to install and load it first.
    See the :ref:`Getting Started<getting_started>` page.

========
Commands
========

--------
``ping``
--------

.. code-block:: yaml

    Syntax: [p]ping

**Description:** View bot's latency.

----

~~~~~~~~~~~~~~~~
``ping message``
~~~~~~~~~~~~~~~~

.. code-block:: yaml

    Syntax: [p]ping message

**Description:** Show bot's message latency.

----

-----------
``pingset``
-----------

.. code-block:: yaml

    Syntax: [p]pingset

**Description:** Manage BotPing settings.

.. note::
    This command is only available for the Bot Owner.

----

~~~~~~~~~~~~~~~~~~~
``pingset usegifs``
~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    Syntax : [p]pingset usegifs [true_or_false]
    Aliases: [p]pingset usegif [p]pingset gif

**Description:** Toggle displaying GIFs on the ping embed.