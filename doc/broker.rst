broker -- Order management classes
==================================

Base module and classes
------------------------

.. automodule:: quantworks.broker
    :members: Order, MarketOrder, LimitOrder, StopOrder, StopLimitOrder, OrderExecutionInfo, Broker
    :member-order: bysource
    :show-inheritance:

Backtesting module and classes
------------------------------

.. automodule:: quantworks.broker.backtesting
    :members: Commission, NoCommission, FixedPerTrade, TradePercentage, Broker
    :show-inheritance:

.. automodule:: quantworks.broker.slippage
    :members: SlippageModel, NoSlippage, VolumeShareSlippage
    :show-inheritance:

.. automodule:: quantworks.broker.fillstrategy
    :members: FillStrategy, DefaultStrategy
    :show-inheritance:
