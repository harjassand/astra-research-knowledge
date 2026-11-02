#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import json

P=Path(__file__).resolve().parent
def ff2(n):return n*(n-1) if n>=2 else 0
def main():
    checked=0
    for R in range(4):
        S=max(64*(R+1),96)
        for r in range(-R,R+1):
            for s in range(-R,R+1):
                for B in range(S+1):
                    C=B-r;E=S-B;FF=E-s
                    if min(C,FF)<0:continue
                    forward=4*ff2(B)*ff2(C);back=2*ff2(E)*ff2(FF)
                    high=2*B*C;low=2+2*B+E
                    u=lambda b:F(1,b+1)
                    Lu=(forward*(u(B-2)-u(B)) if forward else 0)+back*(u(B+2)-u(B))
                    eps=F(1,16384);value=F(16384,S*S)*(1+eps*u(B))
                    actual=-F(16384,S*S)*eps*Lu+(high+low)*value
                    assert actual>=1,(R,S,B,C,E,FF,actual);checked+=1
    out={'exact_full_fiber_supersolution_states':checked,'scope':'Finite algebra consistency check; ACTUAL_GREEN_TAIL_AND_SERVICE.md proves the displayed all-input inequalities.'}
    (P/'results/service_supersolution_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

if __name__=='__main__':main()
