"""Exact exterior-hole contraction, with NO hidden-U model or sampling."""

from fractions import Fraction as F
from itertools import product
from math import comb,factorial
from pathlib import Path
import json,time


def parity(p):
    return -1 if sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2 else 1


def contraction(r):
    d=2*r;raw=[[0]*4 for _ in range(4)];assignments=0
    for junk in product(range(r),repeat=d):
        amp=[0]*4
        for bits in product((0,1),repeat=r+1):
            logical=[];sg=1
            for bit in bits[:r-1]:
                logical.extend((bit,1-bit));sg*=(-1 if bit else 1)
            logical.extend(bits[r-1:])
            physical=tuple(r*a+b for a,b in zip(logical,junk))
            if len(set(physical))!=d:continue
            amp[2*bits[-2]+bits[-1]]+=sg*parity(physical);assignments+=1
        for i in range(4):
            for j in range(4):raw[i][j]+=amp[i]*amp[j]
    den=2**(r+1)*factorial(d)*r**d
    rho=[[F(x,den) for x in row] for row in raw]
    p=sum(rho[i][i] for i in range(4))
    cat=comb(2*r,r)//(r+1);claimed=F(1,4*r**(2*r)*cat)
    singlet=[[F(0)]*4 for _ in range(4)]
    singlet[1][1]=singlet[2][2]=F(1,2)
    singlet[1][2]=singlet[2][1]=F(-1,2)
    assert p==claimed
    assert rho==[[p*x for x in row] for row in singlet]
    return {'r':r,'physical_calls':2*r-1,'success_probability':str(p),
            'known_Pauli_corrected_output':'exact normalized Bell state, hence identity channel',
            'all_16_unnormalized_Choi_entries_checked':True,
            'nonzero_contraction_assignments':assignments}


def main():
    start=time.perf_counter();rows=[contraction(r) for r in (1,2,3)]
    out={'scope':'exact rational contraction of one exterior-hole circuit family; no source calls, draws, unknown frame or hardware',
         'cases':rows,'general_admission_formula':'1/(4*r^(2*r)*Catalan_r)',
         'full_throughput':'NOT_ACHIEVED','failed_payload_retry':'NOT_JUSTIFIED',
         'seconds_after_imports':time.perf_counter()-start}
    Path(__file__).with_name('EXTERIOR_HOLE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
