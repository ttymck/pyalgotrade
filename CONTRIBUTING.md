Contributing to QuantWorks
====================

Welcome!  QuantWorks is a community project that aims to be approachable, modern, and functional.  If you're interested in contributing to QuantWorks, please read on! 


Getting started: building, and testing
--------------------------------------

If you haven't already, take a look at the project's
[README.md file](README.md).

To get started:
- [fork](git@github.com:ttymck/quantworks.git) this repo
- [install TA-Lib](http://mrjbq7.github.io/ta-lib/)
- run `poetry install` ([install poetry](https://pypi.org/project/poetry/) if it is not already.)
- run `poetry run pytest testcases/` to ensure tests can run

If you believe a feature you need is not available, please see the [Issue Tracker](https://github.com/ttymck/quantworks/issues) and open a new issue if one does not exist for your specific request.

Adding Features
----------------

To add a feature to the `quantworks` framework, fork the repo and develop a feature branch. Then, open a PR against the `master` branch of `ttymck/quantworks`.

Adding Extensions or Plugins
----------------------------

Extensions or plugin functionality should be developed in the `quantworks.ext` namespace and published as a separate distribution package.

Extensions and plugins are any asset, market or broker specific implementations (i.e. Bitcoin feeds, Coinbase broker, Poloniex, Alpaca broker, IEX, IBKR, FTSE, etc).

This extension architecutre is intended to keep the quantworks framework lightweight and functional for a wide array of use cases, while allowing a plugin-style ecosystem.

