#!/usr/bin/env bash -l

script='hello_world_1.py'
yw graph $script > yw_prospective.gv
now run -e Tracer $script
now export -m dependency > nw.P
