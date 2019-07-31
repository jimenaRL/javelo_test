#!/bin/bash

BASEPATH="$(cd "$(dirname "$1")"; pwd)/$(basename "$1")"
python -m unittest discover $BASEPATH/code/test