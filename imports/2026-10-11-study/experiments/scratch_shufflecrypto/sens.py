import sys; sys.path.insert(0,'.')
import bounds
from bounds import *
bounds.U_GRID=[1.0]
for d in (20,32,64):
    for le in (-32,-64):
        sn=min_rounds_lift(d,le,'sn'); th=min_rounds_lift(d,le,'thorp')
        print(f"u=1 only (paper's C1): N=2^{d} eps=2^{le}: SN-lift {sn}  Thorp-lift {th}")
