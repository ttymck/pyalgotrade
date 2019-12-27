technical -- Technical indicators
=================================

.. automodule:: quantworks.technical
    :members: EventWindow, EventBasedFilter
    :show-inheritance:

Example
-------

The following example shows how to combine an :class:`EventWindow` and an :class:`EventBasedFilter` to build a custom filter:

.. literalinclude:: ../samples/technical-1.py

The output should be:

.. literalinclude:: ../samples/technical-1.output

Moving Averages
---------------

.. automodule:: quantworks.technical.ma
    :members: SMA, EMA, WMA
    :show-inheritance:

.. automodule:: quantworks.technical.vwap
    :members: VWAP
    :show-inheritance:

Momentum Indicators
-------------------

.. automodule:: quantworks.technical.macd
    :members: MACD
    :show-inheritance:

.. automodule:: quantworks.technical.rsi
    :members: RSI
    :show-inheritance:

.. automodule:: quantworks.technical.stoch
    :members: StochasticOscillator
    :show-inheritance:

.. automodule:: quantworks.technical.roc
    :members: RateOfChange
    :show-inheritance:

Other Indicators
----------------

.. automodule:: quantworks.technical.atr
    :members: ATR
    :show-inheritance:

.. automodule:: quantworks.technical.bollinger
    :members: BollingerBands
    :show-inheritance:

.. automodule:: quantworks.technical.cross
    :members: cross_above, cross_below
    :show-inheritance:

.. automodule:: quantworks.technical.cumret
    :members: CumulativeReturn
    :show-inheritance:

.. automodule:: quantworks.technical.highlow
    :members: High, Low
    :show-inheritance:

.. automodule:: quantworks.technical.hurst
    :members: HurstExponent
    :show-inheritance:

.. automodule:: quantworks.technical.linebreak
    :members: Line, LineBreak
    :show-inheritance:

.. automodule:: quantworks.technical.linreg
    :members: LeastSquaresRegression, Slope
    :show-inheritance:

.. automodule:: quantworks.technical.stats
    :members: StdDev, ZScore
    :show-inheritance:

