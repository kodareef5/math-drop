#!/bin/bash
# core A: n=300 then n=400
cd /home/claude/work/repos/scratch_solvers_logic
python3 hit3.py 300 160 3001 march data/H_300.jsonl
python3 hit3.py 400 40 4001 march data/H_400.jsonl
