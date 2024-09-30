.. _reactlog:

********
ReactLog
********
**Log when reactions are added or removed.**

.. important::
    To use this cog, you will need to install and load it first.
    See the :ref:`Installation<installation>` page.

========
Commands
========

.. warning::
    Do not include the ``[`` and ``]`` when running a command.

    ``[argument]`` only means that **the argument is optional**.

--------
reactlog
--------

.. code-block:: yaml

    Syntax: [p]reactlog
    Alias : [p]reactionlog

**Description:** Reaction logging configuration commands.

.. tip::
    This command group is available as a slash command! Enable it with ``[p]slash enable reactlog``.

----

^^^^^^^^^^^^^^^^
reactlog channel
^^^^^^^^^^^^^^^^

.. code-block:: yaml

    Syntax: [p]reactlog channel [channel]
    Alias : [p]reactionlog channel

**Description:** Set the reaction logging channel. Pass nothing to unset.

----

^^^^^^^^^^^^^^^^^
reactlog reactadd
^^^^^^^^^^^^^^^^^

.. code-block:: yaml

    Syntax: [p]reactlog reactadd [toggle]
    Alias : [p]reactionlog reactadd

**Description:** Enable/disable logging when reactions added.

----

^^^^^^^^^^^^^^^^^
reactlog reactdel
^^^^^^^^^^^^^^^^^

.. code-block:: yaml

    Syntax: [p]reactlog reactdel [toggle]
    Alias : [p]reactionlog reactdel

**Description:** Enable/disable logging when reactions removed.

----

^^^^^^^^^^^^^^^
reactlog logall
^^^^^^^^^^^^^^^

.. code-block:: yaml

    Syntax: [p]reactlog logall [toggle]
    Alias : [p]reactionlog logall

| **Description:** Set whether to log all reactions or not.
| If enabled, all reactions will be logged. If disabled, only first added or last removed reactions will be logged.

----

^^^^^^^^^^^^^^^^^
reactlog settings
^^^^^^^^^^^^^^^^^

.. code-block:: yaml

    Syntax: [p]reactlog settings
    Alias : [p]reactionlog settings

**Description:** Show current reaction logging settings.