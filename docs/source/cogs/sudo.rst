.. _sudo:

****
Sudo
****
**Allows dropping and elevating owner permissions!**

.. important::
    To use this cog, you will need to install and load it first.
    See the :ref:`Installation<installation>` page.

========
Commands
========

.. note::
    All commands of this cog is only available for the Bot Owner.

.. warning::
    Do not include the ``<`` and ``>`` or ``[`` and ``]`` when running a command.

    ``<argument>`` only means that **the argument is required** and
    ``[argument]`` only means that **the argument is optional**.

---
su
---

.. code-block:: yaml

    Syntax: [p]su

**Description:** Enable your bot owner privileges.

----

----
sudo
----

.. code-block:: yaml

    Syntax: [p]sudo <command>

**Description:** Runs the specified command with bot owner permissions.

----

-------
sudomsg
-------

.. code-block:: yaml

    Syntax: [p]sudomsg [content]

| **Description:**
| Dispatch a message event as if it were sent by bot owner.
| Current message is used as a base (including attachments, embeds, etc.)

.. note::
    If content isn't passed, the message needs to contain embeds, attachments, 
    or anything else that makes the message isn't empty.

----

---------
sutimeout
---------

.. code-block:: yaml

    Syntax: [p]sutimeout [interval=0:15:00]

| **Description:**
| Enable your bot owner privileges for the specified time between 1 minute and 1 day.
| Default is 15 minutes.

----

----
unsu
----

.. code-block:: yaml

    Syntax: [p]unsu

**Description:** Disable your bot owner privileges.