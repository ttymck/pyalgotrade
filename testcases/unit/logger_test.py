# QuantWorks
#
# Copyright 2011-2018 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>, Tyler M Kontra <tyler@tylerkontra.com@gmail.com>
"""

from contextlib import redirect_stderr
import datetime, io

from testcases import common

from quantworks import strategy
from quantworks import bar
from quantworks import logger
from quantworks.barfeed import membf


class MockBarFeed(membf.BarFeed):
    def barsHaveAdjClose(self):
        raise NotImplementedError()


class MockStrategy(strategy.BacktestingStrategy):
    def __init__(self, barFeed, cash):
        logger.rootLoggerInitialized = False
        strategy.BacktestingStrategy.__init__(self, barFeed, cash)

    def onBars(self, bars):
        self.info("bla")
        logger.getLogger("custom").info("ble")

    @classmethod
    def run_test(cls):
        bf = MockBarFeed(bar.Interval.DAY)
        bars = [
            bar.BasicBar(datetime.datetime(2000, 1, 1), 10, 10, 10, 10, 10, 10, bar.Interval.DAY),
        ]
        bf.addBarsFromSequence("orcl", bars)

        strat = MockStrategy(bf, 1000)
        strat.run()


class TestCase(common.TestCase):
    # Check that strategy and custom logs have the proper datetime, this is, the bars date time.
    def testBacktestingLog(self):
        stdout = io.StringIO()
        with redirect_stderr(stdout):
            MockStrategy.run_test()

        expectedLines = [
            "2000-01-01 00:00:00 strategy [INFO] bla",
            "2000-01-01 00:00:00 custom [INFO] ble",
        ]
        self.assertEqual([line.strip() for line in stdout.getvalue().split("\n") if line.strip() != ""], expectedLines)