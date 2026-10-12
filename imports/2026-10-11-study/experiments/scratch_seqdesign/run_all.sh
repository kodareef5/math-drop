#!/bin/bash
cd /home/claude/work/repos/scratch_seqdesign
NLIST="4099 509 257" ./run_exp.sh > log_a.txt 2>&1 &
NLIST="2053 1021 101" ./run_exp.sh > log_b.txt 2>&1 &
wait
echo DONE >> log_a.txt
