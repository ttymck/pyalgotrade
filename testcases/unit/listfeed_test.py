# QuantWorks
#
# Copyright 2019 Tyler M Kontra
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

import datetime
import pandas as pd
import pytz

from . import common
from . import feed_test

from quantworks import barfeed
from quantworks.barfeed import Interval
from quantworks.barfeed import common as bfcommon
from quantworks.barfeed import listfeed
from quantworks import bar
from quantworks.utils import dt


class ListFeedTestCase(common.TestCase):
    __columnNames = [
            "Date Time",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "Adj Close",
        ]

    def __loadIntradayBarFeed(self, timezone=None, maxLen=None):
        dt0 = datetime.datetime.utcnow()
        idx = range(1, 7)
        data = {
            "Date Time": [dt0 + datetime.timedelta(hours = i) for i in idx],
            "Open": [i for i in idx],
            "High": [i*3 for i in idx],
            "Low": [i/2 for i in idx],
            "Close": [i*2 for i in idx],
            "Volume": [i**2 for i in idx],
            "Adj Close": [i*2 for i in idx],
          }
        ret = listfeed.Feed(Interval.MINUTE, timezone, maxLen)
        rows = pd.DataFrame(data).to_dict(orient='record')
        ret.addBarsFromListofDicts("tst", rows, timezone)
        ret.loadAll()
        return ret

    def testBaseFeedInterface(self):
        barFeed = self.__loadIntradayBarFeed()
        feed_test.tstBaseFeedInterface(self, barFeed)

    def testWithTimezone(self):
        timeZone = pytz.timezone("US/Central")
        barFeed = self.__loadIntradayBarFeed(timeZone)
        ds = barFeed.getDataSeries()

        for i, currentBar in enumerate(ds):
            self.assertFalse(dt.datetime_is_naive(currentBar.getDateTime()))
            self.assertEqual(ds[i].getDateTime(), ds.getDateTimes()[i])

    def testBounded(self):
        barFeed = self.__loadIntradayBarFeed(maxLen=2)

        barDS = barFeed["tst"]
        self.assertEqual(len(barDS), 2)
        self.assertEqual(len(barDS.getDateTimes()), 2)
        self.assertEqual(len(barDS.getCloseDataSeries()), 2)
        self.assertEqual(len(barDS.getCloseDataSeries().getDateTimes()), 2)
        self.assertEqual(len(barDS.getOpenDataSeries()), 2)
        self.assertEqual(len(barDS.getHighDataSeries()), 2)
        self.assertEqual(len(barDS.getLowDataSeries()), 2)
        self.assertEqual(len(barDS.getAdjCloseDataSeries()), 2)
