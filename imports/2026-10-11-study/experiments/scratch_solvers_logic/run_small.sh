#!/bin/bash
cd /home/claude/work/repos/scratch_solvers_logic
python3 hit3.py 50 4000 50 minisat22 data/H_50.jsonl
python3 hit3.py 100 3000 100 minisat22 data/H_100.jsonl
python3 hit3.py 150 2000 150 march data/H_150.jsonl
python3 hit3.py 200 2000 200 march data/H_200.jsonl
