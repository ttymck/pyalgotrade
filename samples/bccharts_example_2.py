from quantworks import bar
from quantworks import strategy
from quantworks import plotter
from quantworks.technical import vwap
from quantworks.barfeed import csvfeed
from quantworks.bitstamp import broker
from quantworks import broker as basebroker


class VWAPMomentum(strategy.BacktestingStrategy):
    MIN_TRADE = 5

    def __init__(self, feed, brk, instrument, vwapWindowSize, buyThreshold, sellThreshold):
        super(VWAPMomentum, self).__init__(feed, brk)
        self.__instrument = instrument
        self.__vwap = vwap.VWAP(feed[instrument], vwapWindowSize)
        self.__buyThreshold = buyThreshold
        self.__sellThreshold = sellThreshold

    def _getActiveOrders(self):
        orders = self.getBroker().getActiveOrders()
        buy = [o for o in orders if o.isBuy()]
        sell = [o for o in orders if o.isSell()]
        return buy, sell

    def _cancelOrders(self, orders):
        brk = self.getBroker()
        for o in orders:
            self.info("Canceling order %s" % (o.getId()))
            brk.cancelOrder(o)

    def _buySignal(self, price):
        buyOrders, sellOrders = self._getActiveOrders()
        self._cancelOrders(sellOrders)

        brk = self.getBroker()
        cashAvail = brk.getCash() * 0.98
        size = round(cashAvail / price, 3)
        if len(buyOrders) == 0 and price*size > VWAPMomentum.MIN_TRADE:
            self.info("Buy %s at %s" % (size, price))
            try:
                self.limitOrder(self.__instrument, price, size)
            except Exception as e:
                self.error("Failed to buy: %s" % (e))

    def _sellSignal(self, price):
        buyOrders, sellOrders = self._getActiveOrders()
        self._cancelOrders(buyOrders)

        brk = self.getBroker()
        shares = brk.getShares(self.__instrument)
        if len(sellOrders) == 0 and shares > 0:
            self.info("Sell %s at %s" % (shares, price))
            self.limitOrder(self.__instrument, price, shares*-1)

    def getVWAP(self):
        return self.__vwap

    def onBars(self, bars):
        vwap = self.__vwap[-1]
        if vwap is None:
            return

        price = bars[self.__instrument].getClose()
        if price > vwap * (1 + self.__buyThreshold):
            self._buySignal(price)
        elif price < vwap * (1 - self.__sellThreshold):
            self._sellSignal(price)

    def onOrderUpdated(self, order):
        if order.isBuy():
            orderType = "Buy"
        else:
            orderType = "Sell"

        exec_info_str = ""
        if order.getExecutionInfo():
            exec_info_str = " - Price: %s - Amount: %s - Fee: %s" % (
                order.getExecutionInfo().getPrice(), order.getExecutionInfo().getQuantity(),
                round(order.getExecutionInfo().getCommission(), 2)
            )

        self.info("%s order %d updated - Status: %s%s" % (
            orderType,
            order.getId(),
            basebroker.Order.State.toString(order.getState()),
            exec_info_str
        ))


def main(plot):
    instrument = "BTC"
    initialCash = 1000
    vwapWindowSize = 100
    buyThreshold = 0.02
    sellThreshold = 0.01

    barFeed = csvfeed.GenericBarFeed(bar.Frequency.MINUTE*30)
    barFeed.addBarsFromCSV(instrument, "30min-bitstampUSD.csv")
    brk = broker.BacktestingBroker(initialCash, barFeed)
    strat = VWAPMomentum(barFeed, brk, instrument, vwapWindowSize, buyThreshold, sellThreshold)

    if plot:
        plt = plotter.StrategyPlotter(strat)
        plt.getInstrumentSubplot(instrument).addDataSeries("VWAP", strat.getVWAP())

    strat.run()

    if plot:
        plt.plot()


if __name__ == "__main__":
    main(True)
