#!/bin/bash
yosys -l simple.log -p 'synth_ice40 -blif main.blif -json main.json' main.v
nextpnr-ice40 --hx8k --pcf main.pcf --json main.json --asc main.asc
icetime -d hx8k -c 100 main.asc
icepack main.asc main.bin
