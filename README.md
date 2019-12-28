QuantWorks
===========

![PyPI](https://img.shields.io/pypi/v/quantworks)
![PyPI - License](https://img.shields.io/pypi/l/quantworks)
![Travis (.com)](https://img.shields.io/travis/com/ttymck/quantworks)
<!-- [![Build Status](https://travis-ci.org/gbeced/pyalgotrade.png?branch=master)](https://travis-ci.org/gbeced/pyalgotrade)
[![Coverage Status](https://coveralls.io/repos/gbeced/pyalgotrade/badge.svg?branch=master)](https://coveralls.io/r/gbeced/pyalgotrade?branch=master) -->


QuantWorks is an **event driven algorithmic trading** framework. It is a fork of [PyAlgoTrade](https://gbeced.github.io/pyalgotrade/) (see [Motivation](#motivation)). 

QuantWorks provides a Python API for **strategy** authoring, **backtesting**, **paper trading**, and of course **live trading** via the `Broker` interface.

To get started using QuantWorks, please take a look at the original `PyAlgoTrade` [tutorial](http://gbeced.github.io/pyalgotrade/docs/v0.20/html/tutorial.html) and the [full documentation](http://gbeced.github.io/pyalgotrade/docs/v0.20/html/index.html).


Main Features
-------------

 * Event driven.
 * Supports Market, Limit, Stop and StopLimit orders.
 * Supports any type of time-series data in Pandas or CSV format (like Yahoo! Finance, Google Finance, Quandl and NinjaTrader), as well as database (i.e. sqlite).
 * Technical indicators and filters like SMA, WMA, EMA, RSI, Bollinger Bands, Hurst exponent and others.
 * Performance metrics like Sharpe ratio and drawdown analysis.
 * Event profiler.
 * TA-Lib integration.


Motivation
----------

QuantWorks is a fork of `PyAlgoTrade` by [@gbeced](https://github.com/gbeced). This project aims to be:

 * **Modern**: first-class **Python 3** development ([Python 2 is EOL as of 2020](https://pythonclock.org/))
 * **Extensible**: as a framework, robust extension support is a must, and we encourage users of QuantWorks to give back by publishing their extensions (see [Extensions](#extensions))
 * **Easy to Develop**: state-of-the-art tooling (pytest, poetry, travis) and approachable design principles should make it easy for newcomers to contribute.
 * **Open**: as a fork of an Apache 2.0 license project, QuantWorks maintains the spirit of FOSS development. **CONTRIBUTING.md forthcoming**


Development
------------

QuantWorks is developed and tested using 3.7 and depends on:

 * [NumPy and SciPy](http://numpy.scipy.org/).
 * [pytz](http://pytz.sourceforge.net/).
 * [dateutil](https://dateutil.readthedocs.org/en/latest/).
 * [requests](http://docs.python-requests.org/en/latest/).
 * [matplotlib](http://matplotlib.sourceforge.net/) for plotting support.
 * [ws4py](https://github.com/Lawouach/WebSocket-for-Python) for Bitstamp support.
 * [tornado](http://www.tornadoweb.org/en/stable/) for Bitstamp support.
 * [tweepy](https://github.com/tweepy/tweepy) for Twitter support.

Developer ergonomics are provided by 
 
 * poetry
 * pytest
 * tox
 * travis-ci


Extensions 
----------

- [Bitstamp](https://www.bitstamp.net/) (bitcoin) live trading is implemented by the `quantworks-bitstamp` package (pending)
- Twitter real-time feeds are supported via the `quantworks-twitter` package (pending)