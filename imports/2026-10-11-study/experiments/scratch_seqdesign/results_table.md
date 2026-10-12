| N | TS budget (flip steps) | random | Legendre (rotated+appended) | pipeline (chirp + greedy-L4 rounding) | pipeline (chirp + sign rounding) |
|---|---|---|---|---|---|
| 101 | 400000 | 5.63-5.84 (seed 2.24) | 5.84-6.03 (seed 5.46) | 6.17-6.24 (seed 4.97) | 5.97-6.17 (seed 4.13) |
| 257 | 200000 | 5.00-5.13 (seed 1.53) | 6.27-6.27 (seed 6.27) | 5.48-5.88 (seed 4.68) | 5.44-5.67 (seed 3.85) |
| 509 | 100000 | 4.73-4.82 (seed 1.36) | 6.38-6.38 (seed 6.38) | 5.05-5.36 (seed 4.27) | 5.16-5.41 (seed 3.54) |
| 1021 | 30000 | 4.61-4.73 (seed 1.18) | 6.33-6.33 (seed 6.33) | 4.97-5.10 (seed 4.03) | 4.95-5.17 (seed 3.08) |
| 2053 | 8000 | 4.49-4.53 (seed 1.06) | 6.35-6.35 (seed 6.34) | 4.55-4.81 (seed 3.50) | 4.71-4.76 (seed 2.51) |
| 4099 | 4000 | 4.39-4.50 (seed 1.05) | 6.34-6.34 (seed 6.34) | 4.52-4.74 (seed 3.56) | 4.67-4.93 (seed 2.58) |

(101, 'legendre') runs 3 mean TS s 12 mean seedgen s 1 restarts [3978, 3967, 3996]
(101, 'pipe_sign') runs 3 mean TS s 10 mean seedgen s 2 restarts [3986, 4013, 3967]
(101, 'pipeline') runs 3 mean TS s 9 mean seedgen s 32 restarts [3970, 4001, 3946]
(101, 'random') runs 3 mean TS s 13 mean seedgen s 2 restarts [3972, 3987, 3993]
(257, 'legendre') runs 3 mean TS s 18 mean seedgen s 1 restarts [783, 776, 795]
(257, 'pipe_sign') runs 3 mean TS s 14 mean seedgen s 1 restarts [776, 774, 772]
(257, 'pipeline') runs 3 mean TS s 13 mean seedgen s 105 restarts [783, 780, 773]
(257, 'random') runs 3 mean TS s 20 mean seedgen s 1 restarts [777, 786, 781]
(509, 'legendre') runs 3 mean TS s 40 mean seedgen s 2 restarts [196, 199, 185]
(509, 'pipe_sign') runs 3 mean TS s 21 mean seedgen s 1 restarts [200, 196, 201]
(509, 'pipeline') runs 3 mean TS s 19 mean seedgen s 74 restarts [198, 190, 196]
(509, 'random') runs 3 mean TS s 59 mean seedgen s 2 restarts [201, 201, 199]
(1021, 'legendre') runs 3 mean TS s 62 mean seedgen s 4 restarts [30, 31, 29]
(1021, 'pipe_sign') runs 3 mean TS s 88 mean seedgen s 2 restarts [30, 29, 29]
(1021, 'pipeline') runs 3 mean TS s 89 mean seedgen s 142 restarts [29, 32, 31]
(1021, 'random') runs 3 mean TS s 68 mean seedgen s 1 restarts [28, 27, 29]
(2053, 'legendre') runs 3 mean TS s 100 mean seedgen s 37 restarts [4, 5, 5]
(2053, 'pipe_sign') runs 3 mean TS s 62 mean seedgen s 1 restarts [5, 5, 5]
(2053, 'pipeline') runs 3 mean TS s 66 mean seedgen s 36 restarts [5, 5, 5]
(2053, 'random') runs 3 mean TS s 103 mean seedgen s 2 restarts [5, 5, 5]
(4099, 'legendre') runs 3 mean TS s 126 mean seedgen s 101 restarts [2, 2, 1]
(4099, 'pipe_sign') runs 3 mean TS s 188 mean seedgen s 2 restarts [2, 2, 1]
(4099, 'pipeline') runs 3 mean TS s 143 mean seedgen s 64 restarts [2, 2, 1]
(4099, 'random') runs 3 mean TS s 202 mean seedgen s 2 restarts [2, 2, 1]
