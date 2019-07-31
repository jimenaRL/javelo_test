#!/bin/bash
BASEPATH="$(cd "$(dirname "$1")"; pwd)/$(basename "$1")"
export PYTHONPATH=$PYTHONPATH:$BASEPATH/code

export PYTHONIOENCODING=UTF-8


