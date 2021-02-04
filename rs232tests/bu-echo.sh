#!/bin/bash
yosys -l simple.log -p 'synth_ice40 -blif mainecho.blif -json mainecho.json' mainecho.v
nextpnr-ice40 --hx8k --pcf mainecho.pcf --json mainecho.json --asc mainecho.asc
icetime -d hx8k -c 100 mainecho.asc
icepack mainecho.asc mainecho.bin
