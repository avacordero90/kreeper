#!/bin/bash

sudo docker rm --force $(sudo docker ps -a -q) 2> /dev/null

sudo docker image rm --force $(sudo docker images -q) 2> /dev/null