from __future__ import print_function

from quantworks.feed import csvfeed

feed = csvfeed.Feed("Date", "%Y-%m-%d")
feed.addValuesFromCSV("quandl_gold_2.csv")
for dateTime, value in feed:
    print(dateTime, value)
