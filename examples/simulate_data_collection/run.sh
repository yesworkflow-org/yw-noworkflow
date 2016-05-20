#!/usr/bin/env bash

# run the simulation creating a mininum of outputs
now run -e Tracer simulate_data_collection.py q55 --cutoff 12 --redundancy 0 | cut -c 21-

# remove one image so that noWorkflow provenance and YW reconstruction differ
rm -f run/data/DRT240/DRT240_12000eV_002.img
