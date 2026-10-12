#!/bin/bash
# Fixed-budget restarted tabu search on LABS, seeded by 4 families. Budget = TS flip steps per run
# (each step evaluates all N single-flip neighbours, O(N^2)); restarts cycle through the seed list.
cd /home/claude/work/repos/scratch_seqdesign
mkdir -p seeds out
declare -A BUD=( [101]=400000 [257]=200000 [509]=100000 [1021]=30000 [2053]=8000 [4099]=4000 )
for N in $NLIST; do
  B=${BUD[$N]}
  R=$(( B / N + 2 )); K=$R; if [ $K -gt 500 ]; then K=500; fi
  for fam in random legendre pipeline pipe_sign; do
    KK=$K; if [ $fam = random ]; then KK=$R; fi
    for run in 1 2 3; do
      sf=seeds/${fam}_${N}_${run}.txt
      t0=$(date +%s.%N)
      python3 seeds.py $fam $N $KK $((run*1000+N)) $sf > out/${fam}_${N}_${run}.seedlog
      t1=$(date +%s.%N)
      ./tabu $N $B $((run*7919+N)) $sf > out/${fam}_${N}_${run}.res
      t2=$(date +%s.%N)
      echo "$N $fam $run seedgen=$(echo "$t1-$t0"|bc) ts=$(echo "$t2-$t1"|bc) $(head -1 out/${fam}_${N}_${run}.seedlog) | $(head -1 out/${fam}_${N}_${run}.res)"
    done
  done
done
