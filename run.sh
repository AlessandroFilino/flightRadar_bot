#!/bin/bash

departures=("CGN" "QCH" "DUS")
arrivals=("PSA" "FLR")

for dep in "${departures[@]}"; do
    for arr in "${arrivals[@]}"; do
        python3.11 flightNotify.py "$dep" "$arr"
    done
done
