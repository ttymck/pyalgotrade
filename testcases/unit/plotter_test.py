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

import sys
import os

from . import common

from quantworks.barfeed import yahoofeed
from quantworks import plotter

sys.path.append("samples")
import sma_crossover


class PlotterTestCase(common.TestCase):
    def testDownloadAndParseDaily(self):
        instrument = "orcl"
        barFeed = yahoofeed.Feed()
        barFeed.addBarsFromCSV(instrument, common.get_data_file_path("orcl-2000-yahoofinance.csv"))
        strat = sma_crossover.SMACrossOver(barFeed, instrument, 20)
        plt = plotter.StrategyPlotter(strat, True, True, True)
        plt.getInstrumentSubplot(instrument).addDataSeries("sma", strat.getSMA())
        strat.run()

        with common.TmpDir() as tmpPath:
            png = os.path.join(tmpPath, "plotter_test.png")
            plt.savePlot(png)
            # Check that file size looks ok.
            self.assertGreater(os.stat(png).st_size, 45000)
