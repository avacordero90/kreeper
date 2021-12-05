#!/bin/bash

sudo docker rm --force $(sudo docker ps -a -q)

sudo docker image rm --force $(sudo docker images -q)