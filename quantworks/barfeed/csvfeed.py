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

import abc
import datetime

import pytz
import six

from quantworks.utils import dt
from quantworks.utils import csvutils
from quantworks.barfeed import membf
from quantworks import bar



class RowParser(metaclass=abc.ABCMeta):

    """Interface for serializing row of data into :class:`quantworks.bar.Bar`
    """

    @abc.abstractmethod
    def parseBar(self, csvRow: dict) -> bar.Bar:
        """Parses a single row of data into the desired :class:`quantworks.bar.Bar` object.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def getFieldNames(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def getDelimiter(self):
        raise NotImplementedError()


class BarFilter(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def includeBar(self, bar_: bar.Bar) -> bool:
        """Determine whether to include the bar or filter it out.
        :return: True if bar should be included, False if bar should be excluded.
        :rtype: bool
        """
        raise NotImplementedError()


class DateRangeFilter(BarFilter):

    """A simple date bounded, between `fromDate` and `toDate`, exclusive.
    Both `fromDate` and `toDate` are optional.

    :param fromDate: the earliest possible timestamp for bars, exclusive, defaults to None
    :type fromDate: datetime.datetime
    :param toDate: the latest possible timestamp for bars, exclusive, defaults to None
    :type toDate: datetime.datetime
    """
    def __init__(self, fromDate=None, toDate=None):

        self.__fromDate = fromDate
        self.__toDate = toDate

    def includeBar(self, bar_: bar.Bar) -> bool:
        if self.__toDate and bar_.getDateTime() > self.__toDate:
            return False
        if self.__fromDate and bar_.getDateTime() < self.__fromDate:
            return False
        return True


class USEquitiesRTH(DateRangeFilter):
    
    """US Equities Regular Trading Hours filter
    Monday ~ Friday - 9:30 ~ 16:00 (GMT-5, US/Eastern)
    """

    timezone = pytz.timezone("US/Eastern")

    def __init__(self, fromDate=None, toDate=None):
        super(USEquitiesRTH, self).__init__(fromDate, toDate)

        self.__fromTime = datetime.time(9, 30, 0)
        self.__toTime = datetime.time(16, 0, 0)

    def includeBar(self, bar_):
        # filter by instant in time
        ret = super(USEquitiesRTH, self).includeBar(bar_)
        if ret:
            # Check day of week
            barDay = bar_.getDateTime().weekday()
            if barDay > 4:
                return False

            # Check time of day
            barTime = dt.localize(bar_.getDateTime(), USEquitiesRTH.timezone).time()
            if barTime < self.__fromTime:
                return False
            if barTime > self.__toTime:
                return False
        return ret


class BarFeed(membf.BaseMemoryBarFeed):

    """Base class for CSV file based :class:`quantworks.barfeed.BarFeed`.

    .. note::
        This is a base class and should not be used directly.
    """

    def __init__(self, frequency, maxLen=None):
        super(BarFeed, self).__init__(frequency, maxLen)

        self.__barFilter = None
        self.__dailyTime = datetime.time(0, 0, 0)

    def getDailyBarTime(self):
        return self.__dailyTime

    def setDailyBarTime(self, time):
        self.__dailyTime = time

    def getBarFilter(self):
        return self.__barFilter

    def setBarFilter(self, barFilter):
        self.__barFilter = barFilter

    def addBarsFromCSV(self, instrument, path, rowParser, skipMalformedBars=False):
        def parse_bar_skip_malformed(row):
            ret = None
            try:
                ret = rowParser.parseBar(row)
            except Exception:
                pass
            return ret

        if skipMalformedBars:
            parse_bar = parse_bar_skip_malformed
        else:
            parse_bar = rowParser.parseBar

        # Load the csv file
        loadedBars = []
        reader = csvutils.FastDictReader(open(path, "r"), fieldnames=rowParser.getFieldNames(), delimiter=rowParser.getDelimiter())
        for row in reader:
            bar_ = parse_bar(row)
            if bar_ is not None and (self.__barFilter is None or self.__barFilter.includeBar(bar_)):
                loadedBars.append(bar_)

        self.addBarsFromSequence(instrument, loadedBars)


class GenericRowParser(RowParser):

    """Parses arbitrary row of serialized data into :class:`quantworks.bar.BasicBar` class specified by `barClass` param.

    :param columNames: mapping of :class:`quantworks.bar.BasicBar` slots names to data row keys
    :type columnNames: dict
    :param dateTimeFormat: the format string to parse datetime values
    :type dateTimeFormat: str
    :param dailyBarTime: the time of day to apply to daily bars
    :type dailyBarTime: datetime.time
    :param frequency: the bar frequency
    :type frequency: :class:`quantworks.bar.Frequency`
    :param timezone: the bar timezone
    :type timezone: :class:`pytz.timezone`
    :param barClass: the :class:`quantworks.bar.BasicBar` to construct from data rows, defaults to :class:`quantworks.bar.BasicBar`
    :type barClass: :class:`quantworks.bar.BasicBar` or subclass
    """

    def __init__(
        self, columnNames: dict, 
        dateTimeFormat: str, dailyBarTime: datetime.time,
        frequency: bar.Frequency, timezone: pytz.timezone, 
        barClass=bar.BasicBar
    ):
        self.__dateTimeFormat = dateTimeFormat
        self.__dailyBarTime = dailyBarTime
        self.__frequency = frequency
        self.__timezone = timezone
        self.__haveAdjClose = False
        self.__barClass = barClass
        # Column names.
        self.__dateTimeColName = columnNames["datetime"]
        self.__openColName = columnNames["open"]
        self.__highColName = columnNames["high"]
        self.__lowColName = columnNames["low"]
        self.__closeColName = columnNames["close"]
        self.__volumeColName = columnNames["volume"]
        self.__adjCloseColName = columnNames["adj_close"]
        self.__columnNames = columnNames

    def _parseDate(self, dateTime):
        ret = datetime.datetime.strptime(dateTime, self.__dateTimeFormat)

        if self.__dailyBarTime is not None:
            ret = datetime.datetime.combine(ret, self.__dailyBarTime)
        # Localize the datetime if a timezone was given.
        if self.__timezone:
            ret = dt.localize(ret, self.__timezone)
        return ret

    def barsHaveAdjClose(self):
        return self.__haveAdjClose

    def getFieldNames(self):
        # It is expected for the first row to have the field names.
        return None

    def getDelimiter(self):
        return ","

    def parseBar(self, csvRowDict):
        dateTime = self._parseDate(csvRowDict[self.__dateTimeColName])
        open_ = float(csvRowDict[self.__openColName])
        high = float(csvRowDict[self.__highColName])
        low = float(csvRowDict[self.__lowColName])
        close = float(csvRowDict[self.__closeColName])
        volume = float(csvRowDict[self.__volumeColName])
        adjClose = None
        if self.__adjCloseColName is not None:
            adjCloseValue = csvRowDict.get(self.__adjCloseColName, "")
            if len(adjCloseValue) > 0:
                adjClose = float(adjCloseValue)
                self.__haveAdjClose = True

        # Process extra columns.
        extra = {}
        for k, v in six.iteritems(csvRowDict):
            if k not in self.__columnNames.values():
                extra[k] = csvutils.float_or_string(v)

        return self.__barClass(
            dateTime, open_, high, low, close, volume, adjClose, self.__frequency, extra=extra
        )


class GenericBarFeed(BarFeed):
    """A BarFeed that loads bars from CSV files that have the following format:
    ::

        Date Time,Open,High,Low,Close,Volume,Adj Close
        2013-01-01 13:59:00,13.51001,13.56,13.51,13.56,273.88014126,13.51001

    :param frequency: The frequency of the bars. Check :class:`quantworks.bar.Frequency`.
    :type frequency: :class:`quantworks.bar.Frequency`
    :param timezone: The default timezone to use to localize bars. Check :mod:`quantworks.marketsession`.
    :type timezone: :class:`pytz.timezone`
    :param maxLen: The maximum number of values that the :class:`quantworks.dataseries.bards.BarDataSeries` will hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None or invalid (negative), then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int

    .. note::
        * The CSV file **must** have the column names in the first row.
        * It is ok if the **Adj Close** column is empty.
        * When working with multiple instruments:

         * If all the instruments loaded are in the same timezone, then the timezone parameter may not be specified.
         * If any of the instruments loaded are in different timezones, then the timezone parameter should be set.
    """

    def __init__(self, frequency, timezone=None, maxLen=None):
        super(GenericBarFeed, self).__init__(frequency, maxLen)

        self.__timezone = timezone
        # Assume bars don't have adjusted close. This will be set to True after
        # loading the first file if the adj_close column is there.
        self.__haveAdjClose = False

        self.__barClass = bar.BasicBar

        self.__dateTimeFormat = "%Y-%m-%d %H:%M:%S"
        self.__columnNames = {
            "datetime": "Date Time",
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
            "adj_close": "Adj Close",
        }
        # self.__dateTimeFormat expects time to be set so there is no need to
        # fix time.
        self.setDailyBarTime(None)

    def barsHaveAdjClose(self):
        return self.__haveAdjClose

    def setNoAdjClose(self):
        self.__columnNames["adj_close"] = None
        self.__haveAdjClose = False

    def setColumnName(self, col, name):
        self.__columnNames[col] = name

    def setDateTimeFormat(self, dateTimeFormat):
        """
        Set the format string to use with strptime to parse datetime column.
        """
        self.__dateTimeFormat = dateTimeFormat

    def setBarClass(self, barClass):
        self.__barClass = barClass

    def addBarsFromCSV(self, instrument, path, timezone=None, skipMalformedBars=False):
        """Loads bars for a given instrument from a CSV formatted file.
        The instrument gets registered in the bar feed.

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param path: The path to the CSV file.
        :type path: string.
        :param timezone: The timezone to use to localize bars. Check :mod:`quantworks.marketsession`.
        :type timezone: A pytz timezone.
        :param skipMalformedBars: True to skip errors while parsing bars.
        :type skipMalformedBars: boolean.
        """

        if timezone is None:
            timezone = self.__timezone

        rowParser = GenericRowParser(
            self.__columnNames, self.__dateTimeFormat, self.getDailyBarTime(), self.getFrequency(),
            timezone, self.__barClass
        )

        super(GenericBarFeed, self).addBarsFromCSV(instrument, path, rowParser, skipMalformedBars=skipMalformedBars)

        if rowParser.barsHaveAdjClose():
            self.__haveAdjClose = True
        elif self.__haveAdjClose:
            raise Exception("Previous bars had adjusted close and these ones don't have.")
