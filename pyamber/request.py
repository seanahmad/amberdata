import os
from enum import Enum

import requests
import pandas as pd

from pyamber.util import payload2frame

pd.Timestamp.value_in_milliseconds = property(lambda self: int(self.value*1e-6))


class TimeFormat(Enum):
    MILLISECONDS = "milliseconds"
    MS = "ms"
    ISO = "iso"
    ISO8611 = "iso8611"


class TimeInterval(Enum):
    DAYS = "days"
    HOURS = "hours"
    MINUTES = "minutes"


class AmberRequest(object):
    def __init__(self, key=None):
        self.__key = key or os.environ["AMBER_KEY"]

    @property
    def headers(self):
        return {"accept": "application/json", "x-api-key": self.__key}

    def get(self, url, params=None):
        return requests.get(url=url, params=params, headers=self.headers)

    @property
    def health(self):
        return self.get(url="https://web3api.io/health")

    def price_history(self, pair, timeInterval=None, startDate=None, endDate=None, timeFormat=None):
        #pd.Timestamp.value_in_milliseconds = property(lambda self: int(self.value*1e-6))

        startDate = (startDate or pd.Timestamp("today")).value_in_milliseconds
        endDate = (endDate or pd.Timestamp("today")).value_in_milliseconds

        #gap = endDate - startDate
        timeInterval = timeInterval or TimeInterval.HOURS
        timeFormat = timeFormat or TimeFormat.MILLISECONDS

        url="https://web3api.io/api/v2/market/prices/{pair}/historical".format(pair=pair)
        params = {"timeInterval": timeInterval.value, "startDate": startDate, "endDate": endDate, "timeFormat": timeFormat.value}

        #request = AmberRequest()
        response = self.get(url=url, params=params)

        request = response.json()["payload"]
        return payload2frame(request)
