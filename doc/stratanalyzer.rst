stratanalyzer -- Strategy analyzers
===================================

Strategy analyzers provide an extensible way to attach different calculations to strategy executions.

.. automodule:: quantworks.stratanalyzer
    :members: StrategyAnalyzer
    :show-inheritance:

Returns
-------
.. automodule:: quantworks.stratanalyzer.returns
    :members: Returns
    :show-inheritance:

Sharpe Ratio
------------
.. automodule:: quantworks.stratanalyzer.sharpe
    :members: SharpeRatio
    :show-inheritance:

DrawDown
--------
.. automodule:: quantworks.stratanalyzer.drawdown
    :members: DrawDown
    :show-inheritance:

Trades
------
.. automodule:: quantworks.stratanalyzer.trades
    :members: Trades
    :member-order: bysource
    :show-inheritance:

Example
-------
Save this code as sma_crossover.py:

.. literalinclude:: ../samples/sma_crossover.py

and save this code in a different file:

.. literalinclude:: ../samples/sample-strategy-analyzer.py

The output should look like this:

.. literalinclude:: ../samples/sample-strategy-analyzer.output
