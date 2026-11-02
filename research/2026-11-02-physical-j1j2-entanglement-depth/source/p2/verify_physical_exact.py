#!/usr/bin/env python3
"""Physical-H spin/eigenvector, classical square, and α-range exact-rational checks.
  These finite checks complement rather than replace written general proofs.
"""
from fractions import Fraction as F
import json
from pathlib import Path

def action(n,bonds,vec):
    out={i:F(0) for i in range(1<<n)}
    for st,amp in vec.items():
        for i,j,J in bonds:
            if ((st>>i)^(st>>j))&1:
                out[st]-=amp*J/4
                out[st^(1<<i)^(1<<j)]+=amp*J/2
            else:out[st]+=amp*J/4
    return {k:v for k,v in out.items() if v}

def double_square(L):
    aa={}
    for y in range(L):
      for x in range(L):
        i=x+L*y
        aa[i]=(F((x+2*y)%7-3,13),F((3*x-y)%11-5,17),F((x+5*y)%9-4,19))
    inner=lambda i,j:sum(a*b for a,b in zip(aa[i],aa[j]))
    norm=lambda i:sum(a*a for a in aa[i])
    nn=set(); nnn=set()
    def eid(a,b):return tuple(sorted((a,b)))
    for y in range(L):
      for x in range(L):
        i=x+L*y
        for dx,dy in [(1,0),(0,1)]:nn.add(eid(i,((x+dx)%L)+L*((y+dy)%L)))
        for dx,dy in [(1,1),(1,-1)]:nnn.add(eid(i,((x+dx)%L)+L*((y+dy)%L)))
    lhs=sum((inner(i,j) for i,j in nn),F(0)) +F(1,2)*sum((inner(i,j) for i,j in nnn),F(0))+sum((norm(i) for i in aa),F(0))
    rhs=F(0)
    for y in range(L):
      for x in range(L):
        pts=[x+L*y,((x+1)%L)+L*y,x+L*((y+1)%L),((x+1)%L)+L*((y+1)%L)]
        rhs+=F(1,4)*sum(sum(aa[i][a] for i in pts)**2 for a in range(3))
    assert lhs==rhs
    return {'L':L,'bond_counts':[len(nn),len(nnn)],'exact_square_identity':True}

def main():
    # cyclic physical square 0--1--2--3--0, two opposite diagonals
    v={st:F(2 if st in (0b0101,0b1010) else -1) for st in range(16) if st.bit_count()==2}
    assert sum((amp*amp for amp in v.values()),F(0))==12
    nn=[(0,1,F(1)),(1,2,F(1)),(2,3,F(1)),(3,0,F(1))]
    dg=[(0,2,F(1)),(1,3,F(1))]
    r=action(4,nn,v); assert all(r.get(i,0)==-2*v.get(i,0) for i in range(16))
    r=action(4,dg,v); assert all(r.get(i,0)==F(1,2)*v.get(i,0) for i in range(16))
    # S_tot^+|v> = 0: normalized 4-spin state is a global singlet.
    raised={s:F(0) for s in range(16)}
    for st,c in v.items():
        for i in range(4):
            if (st>>i)&1: raised[st^(1<<i)]+=c
    assert all(t==0 for t in raised.values())
    cases=[]
    for alpha in [F(1,3),F(2,5),F(1,2),F(11,20),F(3,5)]:
        e2=-F(3,8)-abs(alpha-F(1,2))/2
        et=-F(1,2)+alpha/8
        margin=e2-et
        assert (margin>0)==(F(1,3)<alpha<F(3,5))
        cases.append({'alpha':str(alpha),'two_product_floor':str(e2),
                      'plaquette_upper':str(et),'entanglement_gap':str(margin)})
    obs={'four_spin_norm_squared':12,'ring_eigenvalue':'-2',
         'diagonals_eigenvalue':'1/2','singlet_annihilation':True,
         'square_identities':[double_square(L) for L in [4,6,8]],
         'alpha_intervals':cases,
         'strict_5prod_ground_gap_rational':'46909/100000 - 91/200 = 1409/100000',
         'thermal_T_0p02_guaranteed':'1409/100000 - (1/50)*ln2 > 1409/100000 - 7/500 = 9/100000',
         'note':'A numerical experiment is not the proof of all-state 2-producibility or infinite-volume claims; see RESEARCH_REPORT.md'}
    Path(__file__).with_name('PHYSICAL_CHECKS.json').write_text(json.dumps(obs,indent=2)+'\n')
    print('PASS exact four-spin ring, diagonal, singlet and square completions; alpha interval')
if __name__=='__main__':main()
