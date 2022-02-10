# rich-rst

[![Documentation Status](https://readthedocs.org/projects/rich-rst/badge/?version=latest)](https://rich-rst.readthedocs.io/en/latest/?badge=latest)

Allows [rich](https://rich.readthedocs.io/en/latest/introduction.html) to print a [reStructuredText](https://docutils.sourceforge.io/rst.html) document in a rich format similar to [`rich.Markdown`](https://rich.readthedocs.io/en/latest/reference/markdown.html).

## Features

75 supported reStructuredText elements. For a list see [ELEMENTS.md](https://github.com/wasi-master/rich-rst/blob/main/ELEMENTS.md)

## Command line interface

Show the contents of readme.rst

```sh
python -m rich_rst readme.rst
```

Get from stdin

```sh
python -m rich_rst -
```

For more help see `python -m rich_rst --help`

## Usage

> Note: There are some aliases: RST, reST, ReStructuredText, reStructuredText, RestructuredText

```python
from rich_rst import RestructuredText
from rich import print

print(RestructuredText("This is a **test** document"))
```

![Demo of the usage](https://i.imgur.com/Nz6tc25.png "Demo of the usage")

## Advanced usage

```python
from rich_rst import RestructuredText
from rich import print

# Documentation for discord.py: https://pypi.org/project/discord.py
docs = "discord.py\n==========\n\n.. image:: https://discord.com/api/guilds/336642139381301249/embed.png\n   :target: https://discord.gg/r3sSKJJ\n   :alt: Discord server invite\n.. image:: https://img.shields.io/pypi/v/discord.py.svg\n   :target: https://pypi.python.org/pypi/discord.py\n   :alt: PyPI version info\n.. image:: https://img.shields.io/pypi/pyversions/discord.py.svg\n   :target: https://pypi.python.org/pypi/discord.py\n   :alt: PyPI supported Python versions\n\nA modern, easy to use, feature-rich, and async ready API wrapper for Discord written in Python.\n\nKey Features\n-------------\n\n- Modern Pythonic API using ``async`` and ``await``.\n- Proper rate limit handling.\n- 100% coverage of the supported Discord API.\n- Optimised in both speed and memory.\n\nInstalling\n----------\n\n**Python 3.5.3 or higher is required**\n\nTo install the library without full voice support, you can just run the following command:\n\n.. code:: sh\n\n    # Linux/macOS\n    python3 -m pip install -U discord.py\n\n    # Windows\n    py -3 -m pip install -U discord.py\n\nOtherwise to get voice support you should run the following command:\n\n.. code:: sh\n\n    # Linux/macOS\n    python3 -m pip install -U \"discord.py[voice]\"\n\n    # Windows\n    py -3 -m pip install -U discord.py[voice]\n\n\nTo install the development version, do the following:\n\n.. code:: sh\n\n    $ git clone https://github.com/Rapptz/discord.py\n    $ cd discord.py\n    $ python3 -m pip install -U .[voice]\n\n\nOptional Packages\n~~~~~~~~~~~~~~~~~~\n\n* PyNaCl (for voice support)\n\nPlease note that on Linux installing voice you must install the following packages via your favourite package manager (e.g. ``apt``, ``dnf``, etc) before running the above commands:\n\n* libffi-dev (or ``libffi-devel`` on some systems)\n* python-dev (e.g. ``python3.6-dev`` for Python 3.6)\n\nQuick Example\n--------------\n\n.. code:: py\n\n    import discord\n\n    class MyClient(discord.Client):\n        async def on_ready(self):\n            print('Logged on as', self.user)\n\n        async def on_message(self, message):\n            # don't respond to ourselves\n            if message.author == self.user:\n                return\n\n            if message.content == 'ping':\n                await message.channel.send('pong')\n\n    client = MyClient()\n    client.run('token')\n\nBot Example\n~~~~~~~~~~~~~\n\n.. code:: py\n\n    import discord\n    from discord.ext import commands\n\n    bot = commands.Bot(command_prefix='>')\n\n    @bot.command()\n    async def ping(ctx):\n        await ctx.send('pong')\n\n    bot.run('token')\n\nYou can find more examples in the examples directory.\n\nLinks\n------\n\n- `Documentation <https://discordpy.readthedocs.io/en/latest/index.html>`_\n- `Official Discord Server <https://discord.gg/r3sSKJJ>`_\n- `Discord API <https://discord.gg/discord-api>`_\n\n\n"

print(RestructuredText(docs, code_theme="dracula", show_errors=False))
```

[![Demo of the advanced usage](https://i.imgur.com/MbtqM33.png "Demo of the advanced usage, truncated")](https://i.imgur.com/MbtqM33.png)

## Changelog

A changelog can be found in [CHANGELOG.md](https://github.com/wasi-master/rich-rst/blob/main/CHANGELOG.md)
