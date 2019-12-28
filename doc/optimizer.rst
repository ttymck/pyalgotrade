optimizer -- Parallel optimizers
================================

.. automodule:: quantworks.optimizer.server
    :members:
    :member-order: bysource
    :show-inheritance:

.. automodule:: quantworks.optimizer.worker
    :members:
    :member-order: bysource
    :show-inheritance:

.. automodule:: quantworks.optimizer.local
    :members:
    :member-order: bysource
    :show-inheritance:

.. note::
    * The server component will split strategy executions in chunks which are distributed among the different workers. You can optionally set the chunk size by passing in **batchSize** to the constructor of **quantworks.optimizer.xmlrpcserver.Server**.
    * The :meth:`quantworks.strategy.BaseStrategy.getResult` method is used to select the best strategy execution. You can override that method to rank executions using a different criteria.

