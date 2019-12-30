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

from quantworks.barfeed import csvfeed
from quantworks import bar


class Feed(csvfeed.GenericBarFeed):
    """A :class:`quantworks.barfeed.csvfeed.BarFeed` that loads bars from CSV files downloaded from Quandl.

    :param interval: The interval of the bars. Only **quantworks.bar.Interval.DAY** or **quantworks.bar.Interval.WEEK**
        are supported.
    :param timezone: The default timezone to use to localize bars. Check :mod:`quantworks.marketsession`.
    :type timezone: A pytz timezone.
    :param maxLen: The maximum number of values that the :class:`quantworks.dataseries.bards.BarDataSeries` will hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.

    .. note::
        When working with multiple instruments:

            * If all the instruments loaded are in the same timezone, then the timezone parameter may not be specified.
            * If any of the instruments loaded are in different timezones, then the timezone parameter must be set.
    """

    def __init__(self, interval=bar.Interval.DAY, timezone=None, maxLen=None):
        if interval not in [bar.Interval.DAY, bar.Interval.WEEK]:
            raise Exception("Invalid interval")

        super(Feed, self).__init__(interval, timezone, maxLen)

        self.setDateTimeFormat("%Y-%m-%d")
        self.setColumnName("datetime", "Date")
        self.setColumnName("adj_close", "Adj. Close")
