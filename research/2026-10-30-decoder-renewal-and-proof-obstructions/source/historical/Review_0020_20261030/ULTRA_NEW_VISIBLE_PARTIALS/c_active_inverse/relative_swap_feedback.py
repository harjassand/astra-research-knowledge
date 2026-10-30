"""A literal two-query feedback circuit, reduced by EXACT permutation moments.

First query is Bell-input. Before the second query, use
 W=I-(I+s*SWAP_(payload,out1))*Phi_(ref1,input2), s=+1 or-1.
Second input is an otherwise fresh Bell half. W is a KNOWN Hermitian
unitary: it is a Bell reflection controlled by the relative SWAP sector.
It uses the retained unknown quantum memory, with no unknown controlled N.

The exact rational output Choi after physical frame twirl has48x48 size
independent of r,D. A floating SDP ONLY proposes a final known decoder.
No source or circuit has run, and its output is not a numerical certificate.
"""

from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import argparse,json,time
import numpy as np
import cvxpy as cp


PERMS=tuple(permutations(range(3)))


def compose(a,b):return tuple(a[b[i]] for i in range(3))


def inverse(a):return tuple(a.index(i) for i in range(3))


def cycle(a):
    seen=set();n=0
    for i in range(3):
        if i in seen:continue
        n+=1;j=i
        while j not in seen:seen.add(j);j=a[j]
    return n


def pmove(x,p):
    bits=[(x>>(2-i))&1 for i in range(3)];out=[0]*3
    for i in range(3):out[p[i]]=bits[i]
    return 4*out[0]+2*out[1]+out[2]


def vectors(sector):
    # References are(T,R1,R2); logical carriers(payload,input1,input2).
    v=np.empty((8,8),dtype=object);v[:]=F(0)
    for i in range(8):v[i,i]=F(1) # common normalization1/sqrt8
    phi=np.empty_like(v);phi[:]=F(0)
    for ref in range(8):
        for log in range(8):
            if not v[ref,log]:continue
            if ((ref>>1)&1)!=(log&1):continue
            for bit in (0,1):
                rr=(ref&~2)|(bit<<1);ll=(log&~1)|bit
                phi[rr,ll]+=v[ref,log]/2
    a=v-phi;b=np.empty_like(v);b[:]=F(0)
    for i in range(8):
        for log in range(8):b[i,pmove(log,(1,0,2))]-=sector*phi[i,log]
    return a,b


def exact_state(r,sector=1):
    assert sector in(-1,1)
    a,b=vectors(sector);v=(a,b);mom={};flip=(1,0,2)
    for pi in PERMS:
        m=[[F(0) for _ in range(8)] for _ in range(8)]
        for s in range(2):
            for t in range(2):
                coef=F(r**cycle(compose(flip,pi) if s!=t else pi),r**3*8)
                for i in range(8):
                    for j in range(8):
                        m[i][j]+=coef*sum(v[s][i,l]*v[t][j,pmove(l,pi)] for l in range(8))
        mom[pi]=m
    z=[[F(0) for _ in range(48)] for _ in range(48)]
    for pi in PERMS:
        inv=inverse(pi);m=mom[pi]
        for h,g in enumerate(PERMS):
            gh=PERMS.index(compose(inv,g))
            for i in range(8):
                for j in range(8):z[6*i+gh][6*j+h]+=m[i][j]/6
    assert all(z[i][j]==z[j][i] for i in range(48) for j in range(48))
    assert sum(z[i][i] for i in range(48))==1
    # Output known registers C=(R1,R2,regularS3) dimension24, targetT first.
    target=np.array([[float(z[24*a+i][24*b+j])/2 for j in range(24) for b in range(2)]
                     for i in range(24) for a in range(2)])
    assert np.linalg.norm(target-target.T)<1e-14
    return z,target


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--r',type=int,default=2)
    ap.add_argument('--sector',choices=['symmetric','antisymmetric'],default='antisymmetric')
    a=ap.parse_args();assert a.r>=1;start=time.perf_counter()
    z,target=exact_state(a.r,1 if a.sector=='symmetric' else-1);minimum=float(np.linalg.eigvalsh(np.array(z,dtype=float))[0])
    assert minimum>=-1e-12
    C=cp.Variable((48,48),symmetric=True)
    tr=C[0::2,0::2]+C[1::2,1::2]
    problem=cp.Problem(cp.Maximize(cp.trace(C@target)),[C>>0,tr==np.eye(24)])
    result=problem.solve(solver='CLARABEL',tol_gap_abs=1e-9,tol_feas=1e-9,tol_gap_rel=1e-9,max_iter=150)
    base=Path(__file__).parent
    np.save(base/f'FEEDBACK_{a.sector.upper()}_DECODER_PROPOSAL.npy',C.value)
    out={'scope':'literal two-query conditional-relative-SWAP circuit; exact Haar/permutation state; floating final-decoder proposal ONLY',
         'r':a.r,'source_queries_in_circuit':2,'actual_source_or_quantum_circuit_calls':0,
         'feedback':f'I-(I{"+" if a.sector=="symmetric" else "-"}SWAP_physical)*Phi_ref1_input2',
         'no_unknown_adjoint_controlled_dilation_or_switch':True,
         'exact_state_trace':str(sum(z[i][i] for i in range(48))),
         'state_min_eigenvalue_float_diagnostic':minimum,
         'decoder_dimension':24,'decoder_Choi_order':48,
         'Bell_fidelity_float_proposal':float(result),'solver_status':problem.status,
         'known_physical_coherence':'payload+out1 retained through feedback andsecond query; referencesR1/R2 thenfinalknownCPTPdecode',
         'seconds_after_imports':time.perf_counter()-start}
    (base/f'RELATIVE_SWAP_{a.sector.upper()}_PROPOSAL.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
