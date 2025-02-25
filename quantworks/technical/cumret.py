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

from quantworks import technical


class CumRetEventWindow(technical.EventWindow):
    def __init__(self):
        super(CumRetEventWindow, self).__init__(2)
        self.__prevCumRet = 0

    def getValue(self):
        ret = None
        if self.windowFull():
            values = self.getValues()
            prev = values[0]
            actual = values[1]
            netReturn = (actual - prev) / float(prev)
            ret = (1 + self.__prevCumRet) * (1 + netReturn) - 1
            self.__prevCumRet = ret
        return ret


class CumulativeReturn(technical.EventBasedFilter):
    """This filter calculates cumulative returns over another dataseries.

    :param dataSeries: The DataSeries instance being filtered.
    :type dataSeries: :class:`quantworks.dataseries.DataSeries`.
    :param maxLen: The maximum number of values to hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.
    """

    def __init__(self, dataSeries, maxLen=None):
        super(CumulativeReturn, self).__init__(dataSeries, CumRetEventWindow(), maxLen)
