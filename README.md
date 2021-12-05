# [kreeper](https://github.com/avacordero90/kreeper) - by [Luna Cordero](https://lunacordero.com) - v1.0.8

a kucoin service that buys and sells crypto based on technical analysis indicators

## installation
run the following command to install the kreeper service TO A CONTAINER(requires root access). You may have to run `apt install -y curl` first.
```
bash <(curl -k https://file.kreeper.trade/kreeper-server-install.sh)
```
downloads the kreeper source code, installs dependencies, creates and inits a virtual environment, and runs configuration.

## running from docker
run the following command to start a dev container and run the service in that container. you may have to run `apt install -y git && curl -fsSL https://get.docker.com | sh` first.
```
git clone https://github.com/avacordero90/kreeper.git && ./kreeper/start.sh
```

## usage
```
$ kreeper.py
```


## examples
```
kreeper.py                            # run with defaults
```