.. _osu:

***
Osu
***
**Show osu! user stats with osu! API.**

.. important::
    To use this cog, you will need to install and load it first.
    See the :ref:`Getting Started<getting_started>` page.

========
Commands
========

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

^^^^^^^
osu set
^^^^^^^

.. code-block:: yaml

    Syntax: [p]osu set

**Description:** Settings for osu!

.. note::
    This command is only available for the Bot Owner.

----

"""""""""""""""""""
osu set authtimeout
"""""""""""""""""""

.. code-block:: yaml

    Syntax: [p]osuset authtimeout <timeout>

**Description:** Set the timeout for authentication. (Default is 5 minutes or 300 seconds)

.. note::
    This command is only available for the Bot Owner.

----

"""""""""""""
osu set creds
"""""""""""""

.. code-block:: yaml

    Syntax: [p]osuset creds

**Description:** Shows instructions on how to set osu! API credentials.

.. note::
    This command is only available for the Bot Owner.

----

"""""""""""""""""""
osu set menutimeout
"""""""""""""""""""

.. code-block:: yaml

    Syntax: [p]osuset menutimeout <timeout>

**Description:** Set the timeout for menu. (Default is 3 minutes or 180 seconds)

.. note::
    This command is only available for the Bot Owner.

----

"""""""""""""""""
osu set modeemoji
"""""""""""""""""

.. code-block:: yaml

    Syntax: [p]osuset modeemoji <mode> [emoji]

**Description:** Change an emoji used by the bot for showing modes. Omit ``emoji`` to reset a mode's emoji.

.. note::
    This command is only available for the Bot Owner.

----

"""""""""""""""""
osu set rankemoji
"""""""""""""""""

.. code-block:: yaml

    Syntax: [p]osuset rankemoji <rank> [emoji]

**Description:** Change an emoji used by the bot for showing ranks. Omit ``emoji`` to reset a rank's emoji.

.. note::
    This command is only available for the Bot Owner.

----

""""""""""""""
osu set scopes
""""""""""""""

.. code-block:: yaml

    Syntax: [p]osuset scopes [scopes...]

| **Description:** Set customized scopes for what you want your bot to allow. Omit ``scopes`` to view current scopes.
| **Scopes:** ``public``, ``identify``, ``friends.read``, ``forum.write``, ``delegate``, ``chat.write``, ``lazer``.
| You can find information about scopes `here <https://osu.ppy.sh/docs/index.html#scopes>`_.

.. note::
    This command is only available for the Bot Owner.

----

^^^^^^^^^^
osu unlink
^^^^^^^^^^

.. code-block:: yaml

    Syntax: [p]osu unlink

**Description:** Unlink your osu! account.