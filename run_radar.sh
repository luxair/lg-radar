#!/bin/bash

set -e -x

export PATH=$(dirname $0)/venv/bin:$PATH

python3 radar/radar.py
