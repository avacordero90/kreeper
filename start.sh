#!/bin/bash

~/kreeper/setup/docker-cleanup.sh & \
    (~/kreeper/setup/docker-config-dev.sh && \
    ~/kreeper/setup/docker-start.sh)