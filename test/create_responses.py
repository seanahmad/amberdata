import logging

import pandas as pd
from flask import Flask

from pyamber.enum import TimeInterval
from pyamber.flask_amberdata import amberdata
from io import StringIO

#def resources(name):
#    return os.path.join(os.path.dirname(__file__), "resources", name)

if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_pyfile('/amberdata/config/settings.cfg')
    amberdata.init_app(app)

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    log = logging.getLogger('requests.packages.urllib3')  # works
    log.setLevel(logging.DEBUG)  # needed
    log.propagate = True

    # logging from urllib3 to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    log.addHandler(ch)


    with app.app_context():
        request = amberdata.request
        output = StringIO()
        #x = request.prices.history(pair="eth_usd", start_date=pd.Timestamp("2020-02-12"), end_date=pd.Timestamp("2020-02-13"), logger=log)
        for exchange, series in request.prices.latest(pair="eth_usd", logger=log):
            series.to_csv(output)
            print(output.getvalue())

        output = StringIO()
        y = request.prices.history(pair="eth_usd", start_date=pd.Timestamp("2020-02-12"), end_date=pd.Timestamp("2020-02-13"), logger=log, time_interval=TimeInterval.DAYS)
        y.to_csv(output, header=True)
        print(output.getvalue())

        output = StringIO()
        for exchange, series in request.ohlcv.latest(pair="eth_usd", exchange="bitfinex", logger=log):
            series.to_csv(output, header=False)
            print(output.getvalue())