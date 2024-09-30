.. _installation:

************
Installation
************

.. important::
    - Make sure Downloader is already loaded, if not load it with:
    .. code-block:: yaml

        [p]load downloader

=====================
Adding The Repository
=====================

.. code-block:: yaml

    [p]repo add kuro-cogs https://github.com/Kuro-Rui/Kuro-Cogs

.. note::
    ``[p]`` is your prefix.

===============
Installing Cogs
===============

.. warning::
    Do not include the ``<`` and ``>`` when installing cogs.
    ``<argument>`` only means that **the argument is required**.

1. Install the cogs with:
    .. code-block:: yaml

        [p]cog install kuro-cogs <cogs...>

2. Load the installed cogs with:
    .. code-block:: yaml

        [p]load <cogs...>

.. note::
    ``[p]`` is your prefix.