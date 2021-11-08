# [kreeper](https://github.com/avacordero90/kreeper) - by [Luna Cordero](https://lunacordero.com)
a kucoin service that buys and sells crypto based on technical analysis indicators

## installation
run the following command to install the kreeper service (requires root access).
```
curl --silent --show-error --retry 5 http://kreeper.trade/backend/kreeper/setup/install.sh | bash
```
downloads the kreeper source code, installs dependencies, creates and inits a virtual environment, and runs config.sh (see next section)

## configuration
run the following command to start a python virtual environment and configure the kreeper service (requires root access and pip):
```
<!-- curl -X GET https://raw.githubusercontent.com/avacordero90/kreeper/main/install/config.sh | sudo pipenv shell source -->
```
* this configurator is for internal use only.
* it will connect to an API key on a given kucoin account, therefore binding it.
* this means calling this kreeper instance may trigger crypto trades with your account. USE WITH CAUTION.
* only use this configurator within a python virtual environment.
* to install all dependencies and then automatically run this script within a virtual environment, run ./install.sh

## usage
```
$ kreeper.py [-h] [-c COINS [COINS ...]] [-q QUOTES [QUOTES ...]] [-l LINES] [-i INTERVAL] [-b BARS] [-L LIMIT] [-v]

executes crypto trades based on desired investment and risk level.

optional arguments:
  -h, --help            show this help message and exit
  -c COINS [COINS ...], --coins COINS [COINS ...]
                        which coins to trade
  -q QUOTES [QUOTES ...], --quotes QUOTES [QUOTES ...]
                        which quotes to trade against
  -l LINES, --lines LINES
                        how many lines (datapoints) to display
  -i INTERVAL, --interval INTERVAL
                        what interval of datapoints to request -- 1min, 3min, 5min, 15min, 30min, 1hour, 2hour, 4hour, 6hour, 8hour, 12hour, 1day, 1week
  -b BARS, --bars BARS  how many bars to collect data from
  -L LIMIT, --limit LIMIT
                        limit of datapoints to return
  -v, --verbose         displays all logging and market data
```


## examples
```
./kreeper.py                            # run with defaults
./kreeper.py -h                         # get help
./kreeper.py --verbose                  # run in verbose mode
./kreeper.py --coins ETH ETH3L          # gets all ETH and ETH3L quotes
./kreeper.py --coins ETH --quotes BTC   # gets ETH-BTC
./kreeper.py --coins ETH ETH3L -quotes USDT BTC --interval 1hour --lines 10 # advanced usage
```