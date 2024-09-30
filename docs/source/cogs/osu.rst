.. _osu:

***
Osu
***
**Show osu! user stats with osu! API.**

.. important::
    To use this cog, you will need to install and load it first.
    See the :ref:`Installation<installation>` page.

========
Commands
========

.. warning::
    Do not include the ``<`` and ``>`` or ``[`` and ``]`` when runnning a command.
    ``<argument>`` only means that **the argument is required** and
    ``[argument]`` only means that **the argument is optional**.

.. note::
    All the ``user`` argument defaults to you if not passed
    which requires you to link your osu! account first with ``[p]osu link``

---
osu
---

.. code-block:: yaml

    Syntax: [p]osu

**Description:** osu! related commands.

.. tip::
    This command group is available as a slash command! Enable it with ``[p]slash enable osu``.

----

^^^^^^^^^^
osu avatar
^^^^^^^^^^

.. code-block:: yaml

    Syntax : [p]osu avatar [user]

**Description:** Get a user's current osu! Avatar.

----

^^^^^^^^
osu card
^^^^^^^^

.. code-block:: yaml

    Syntax : [p]osu card [user]

**Description:** Get a user's osu! Standard profile card.

----

^^^^^^^^
osu link
^^^^^^^^

.. code-block:: yaml

    Syntax: [p]osu link

**Description:** Link your osu! account.

----

^^^^^^^^^^^
osu profile
^^^^^^^^^^^

.. code-block:: yaml

    Syntax: [p]osu profile [user] [query_type]

**Description:** Link your osu! account. ``query_type`` should be either ``username`` or ``userid``.

----

^^^^^^^^^^
osu unlink
^^^^^^^^^^

.. code-block:: yaml

    Syntax: [p]osu unlink

**Description:** Unlink your osu! account.

----

------
osuset
------

.. code-block:: yaml

    Syntax: [p]osuset

**Description:** osu! settings.

.. note::
    This command is only available for the Bot Owner.

----

^^^^^^^^^^^^^^^^^^
osuset authtimeout
^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

    Syntax: [p]osuset authtimeout <timeout>

**Description:** Set the timeout for authentication. (Default is 5 minutes or 300 seconds)

.. note::
    This command is only available for the Bot Owner.

----

^^^^^^^^^^^^
osuset creds
^^^^^^^^^^^^

.. code-block:: yaml

    Syntax: [p]osuset creds

**Description:** Shows instructions on how to set osu! API credentials.

.. note::
    This command is only available for the Bot Owner.

----

^^^^^^^^^^^^^^^^^^
osuset menutimeout
^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

    Syntax: [p]osuset menutimeout <timeout>

**Description:** Set the timeout for menu. (Default is 3 minutes or 180 seconds)

.. note::
    This command is only available for the Bot Owner.

----

^^^^^^^^^^^^^
osuset scopes
^^^^^^^^^^^^^

.. code-block:: yaml

    Syntax: [p]osuset scopes [scopes...]

| **Description:** Set customized scopes for what you want your bot to allow. Omit ``scopes`` to view current scopes.
| **Scopes:** ``public``, ``identify``, ``friends.read``, ``forum.write``, ``delegate``, ``chat.write``, ``lazer``.
| You can find information about scopes `here <https://osu.ppy.sh/docs/index.html#scopes>`_.

.. note::
    This command is only available for the Bot Owner.