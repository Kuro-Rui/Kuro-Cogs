.. _permissionslocker:

*****************
PermissionsLocker
*****************
**Locks bot to a certain permissions set.**

.. important::
    To use this cog, you will need to install and load it first.
    See the :ref:`Installation<installation>` page.

========
Commands
========

.. warning::
    Do not include the ``<`` and ``>`` when running a command.

    ``<argument>`` only means that **the argument is required**.

--------
permlock
--------

.. code-block:: yaml

    Syntax: [p]permlock

**Description:** Permissions locker group command.

---

^^^^^^^^^^^^^^
permlock perms
^^^^^^^^^^^^^^

.. code-block:: yaml

    Syntax: [p]permlock perms <value>

**Description:** Set the permissions value that is required for the bot to work.

---

^^^^^^^^^^^^^^^^^
permlock settings
^^^^^^^^^^^^^^^^^

.. code-block:: yaml

    Syntax: [p]permlock settings

**Description:** View PermissionsLocker settings.

---

^^^^^^^^^^^^^^^^^^^^
permlock unwhitelist
^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

    Syntax: [p]permlock unwhitelist <guild_id>

**Description:** Remove a guild from the PermissionsLocker whitelist.

---

^^^^^^^^^^^^^^^^^^
permlock whitelist
^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

    Syntax: [p]permlock whitelist <guild_id>

**Description:** Whitelist a guild from PermissionsLocker checks.