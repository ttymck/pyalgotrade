Migrating from PyAlgoTrade
================================

QuantWorks is a fork of PyAlgoTrade. It should function as a drop-in replacement 
of ``pyalgotrade`` (as of v0.20), with a few minor tweaks.

Please keep in mind QuantWorks is a **Python 3** ONLY package, Python 2 support is not intended or guaranteed.

Changes
-------

- convert all ``pyalgotrade`` imports to ``quantworks``
- `BitcoinCharts & Bitstamp <https://pypi.org/project/quantworks-bitcoin/>`_
    - ``pip install quantworks-bitcoin``
    - convert ``pyalgotrade.bitstamp`` imports to ``quantworks.ext.bitstamp``
    - and ``pyalgotrade.bitcoincharts`` to ``quantworks.ext.bitcoincharts``
- `Twitter <https://pypi.org/project/quantworks-twitter/>`_
    - ``pip install quantworks-twitter``
    - convert ``pyalgotrade.twitter`` imports to ``quantworks.ext.twitter``

**If you uncover any compatibility issues with pyalgotrade please open an issue on GitHub.**

Backwards Compatibility
-----------------------

QuantWorks was forked from PyAlgoTrade v0.20, the first release of QuantWorks being v0.21. 

Backwards compatibility is not guaranteed as the public API changes until the v1.0 release.

If you feel strongly about keeping backwards compatibility in one or more specific modules, please open an issue to discuss.