#!/usr/bin/env bash -l
#
# ./run.sh &> run.txt

script='hello_world_1.py'
yw graph $script > yw_prospective.gv
now run -e Tracer $script
now export -m dependency | grep -v 'environment(' > nw_facts.P
