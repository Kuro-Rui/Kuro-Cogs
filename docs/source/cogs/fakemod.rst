.. _fakemod:

*******
FakeMod
*******
**Fake moderation commands made for fun!**

.. important::
    To use this cog, you will need to install and load it first.
    See the :ref:`Installation<installation>` page.

========
Commands
========

.. warning::
    Do not include the ``<`` and ``>`` or ``[`` and ``]`` when running a command.

    ``<argument>`` only means that **the argument is required** and
    ``[argument]`` only means that **the argument is optional**.

---
ben
---

.. code-block:: yaml

    Syntax : [p]ben <user> [reason]
    Aliases: [p]bam, [p]bon, [p]beam, [p]bean

**Description:** Fake ban a user.

----

-------------
fakemodlogset
-------------

.. code-block:: yaml

    Syntax: [p]fakemodlogset

**Description:** Manage fake modlog settings.

----

^^^^^^^^^^^^^^^^^^^
fakemodlogset emoji
^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

    Syntax: [p]fakemodlogset emoji <action> <emoji>

| **Description:**
| Set an emoji for a fake mod action. Action must be either ``warn``, ``mute``, ``kick``, or ``ban``.

----

^^^^^^^^^^^^^^^^^^^^
fakemodlogset modlog
^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

    Syntax: [p]fakemodlogset modlog [channel]

**Description:** Set a channel as the fake modlog. Pass nothing to deactivate fake modlog.

----

^^^^^^^^^^^^^^^^^^^^^^^^
fakemodlogset resetcases
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

    Syntax: [p]fakemodlogset resetcases

**Description:** Reset all fake modlog cases in this server.

----

---
kik
---

.. code-block:: yaml

    Syntax : [p]kik <member> [reason]
    Aliases: [p]kek, [p]keck

**Description:** Fake kick a member.

----

----
myut
----

.. code-block:: yaml

    Syntax: [p]myut <member> [reason]
    Alias : [p]moot

**Description:** Fake mute a member.

----

-----
unben
-----

.. code-block:: yaml

    Syntax : [p]unben <user> [reason]
    Aliases: [p]unbam, [p]unbon, [p]unbeam, [p]unbean

**Description:** Fake unban a user.

----

------
unmyut
------

.. code-block:: yaml

    Syntax: [p]unmyut <member> [reason]
    Alias : [p]unmoot

**Description:** Fake unmute a member.

----

------
unworn
------

.. code-block:: yaml

    Syntax: [p]unworn <user> [reason]

**Description:** Fake unwarn a member.

----

----
worn
----

.. code-block:: yaml

    Syntax: [p]worn <user> [reason]

**Description:** Fake warn a member.