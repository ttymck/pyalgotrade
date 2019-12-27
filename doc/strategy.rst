strategy -- Basic strategy classes
==================================

Strategies are the classes that you define that implement the trading logic, when to buy, when to sell, etc.

Buying and selling can be done in two ways:

    * Placing individual orders using any of the following methods:

     * :meth:`quantworks.strategy.BaseStrategy.marketOrder`
     * :meth:`quantworks.strategy.BaseStrategy.limitOrder`
     * :meth:`quantworks.strategy.BaseStrategy.stopOrder`
     * :meth:`quantworks.strategy.BaseStrategy.stopLimitOrder`

    * Using a higher level interface that wrap a pair of entry/exit orders:

     * :meth:`quantworks.strategy.BaseStrategy.enterLong`
     * :meth:`quantworks.strategy.BaseStrategy.enterShort`
     * :meth:`quantworks.strategy.BaseStrategy.enterLongLimit`
     * :meth:`quantworks.strategy.BaseStrategy.enterShortLimit`

Positions are higher level abstractions for placing orders. They are escentially a pair of entry-exit orders and provide
easier tracking for returns and PnL than using individual orders.


Strategy
--------

.. automodule:: quantworks.strategy
    :members: BaseStrategy, BacktestingStrategy
    :show-inheritance:
    :member-order: bysource

Position
--------

.. automodule:: quantworks.strategy.position
    :members: Position
    :show-inheritance:
    :member-order: bysource
