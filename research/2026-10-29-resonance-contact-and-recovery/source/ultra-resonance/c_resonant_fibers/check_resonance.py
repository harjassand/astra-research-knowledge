"""Exact source-to-resonant-pseudospin check in a cyclotomic field.

No diagonalization/tolerance classifies energy equality. N=8 is one finite
consumer of the all-even-N derivation. The literal real-space two-particle
density interaction is independently Fourier transformed and compared with
the antisymmetrized vertex before constructing its many-body secular block.
"""
from pathlib import Path
from fractions import Fraction as F
import itertools
import json
import time

HERE=Path(__file__).resolve().parent
N=8
D=2*N
A={1:F(1),2:F(1,3)}
ZERO=(F(0),)*D


def scalar(q):return (F(q),)+(F(0),)*(D-1)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def scale(a,q):return tuple(x*q for x in a)
def power(k):
    k%=2*D
    return tuple(F(1 if k<D else -1) if j==k%D else F(0) for j in range(D))
def mul(a,b):
    c=[F(0)]*D
    for i,x in enumerate(a):
        if not x:continue
        for j,y in enumerate(b):
            if not y:continue
            k=i+j;c[k%D]+=(1 if k<D else -1)*x*y
    return tuple(c)
def conj(a):
    ans=ZERO
    for i,x in enumerate(a):
        if x:ans=add(ans,scale(power(-i),x))
    return ans
def cosine(k):return scale(add(power(4*k),power(-4*k)),F(1,2))
def sine(k):return scale(mul(power(N),sub(power(4*k),power(-4*k))),F(-1,2))
def vhat(q):
    ans=ZERO
    for r,a in A.items():ans=add(ans,scale(cosine(r*q),2*a))
    return ans
def vertex(a,b,c,d):
    if (a+b-c-d)%N:return ZERO
    return scale(sub(vhat(a-c),vhat(a-d)),F(1,N))


def ladder(mask,j,create):
    occupied=(mask>>j)&1
    if occupied==create:return None
    sign=(-1)**((mask&((1<<j)-1)).bit_count())
    return mask^(1<<j),sign


def apply_word(mask,word):
    s=1
    for j,create in word:
        z=ladder(mask,j,create)
        if z is None:return None
        mask,sg=z;s*=sg
    return mask,s


def main():
    started=time.perf_counter()
    pairs=list(itertools.combinations(range(N),2))
    # zeta=exp(2pi i/(4N)), Phi_(4N)=x^(2N)+1 at this N.
    energies={tw:[neg(add(power(4*k-tw),power(-4*k+tw)))
                  for k in range(N)] for tw in [0,1]}
    counts={}
    for tw in [0,1]:
        nontrivial=0;total=0
        for a,b in pairs:
            for c,d in pairs:
                if (a+b-c-d)%N:continue
                resonant=add(energies[tw][a],energies[tw][b])==add(energies[tw][c],energies[tw][d])
                declared=(a,b)==(c,d) or (tw==0 and (a+b)%N==N//2)
                assert resonant==declared
                total+=resonant;nontrivial+=resonant and (a,b)!=(c,d)
        counts[str(tw)]={'all_resonant_pair_matrix_entries':total,'nontrivial':nontrivial}
    # Independent exterior Fourier transform of literal V=sum_j n_j n_(j+r).
    checked=0
    for a,b in pairs:
        for c,d in pairs:
            exact=ZERO
            for x,y in pairs:
                real_energy=sum(ar for r,ar in A.items() if (y-x)%N in [r,N-r])
                if not real_energy:continue
                left=sub(power(4*(a*x+b*y)),power(4*(b*x+a*y)))
                right=sub(power(4*(c*x+d*y)),power(4*(d*x+c*y)))
                exact=add(exact,scale(mul(conj(left),right),real_energy/F(N*N)))
            assert exact==vertex(a,b,c,d)
            checked+=1
    reps=list(range(-N//4+1,N//4))
    ps=[(k%N,(N//2-k)%N) for k in reps]
    m=len(ps)
    basis={};back={}
    for bits in range(1<<m):
        mask=0;sgn=1
        for i,(k,p) in enumerate(ps):
            if (bits>>i)&1:
                mask,s=apply_word(mask,[(p,True),(k,True)]);sgn*=s
        basis[bits]=(mask,sgn);back[mask]=(bits,sgn)
    literal=[[ZERO for _ in basis] for _ in basis]
    outside=0
    for bits,(mask,phase) in basis.items():
        for a,b in pairs:
            for c,d in pairs:
                if add(energies[0][a],energies[0][b])!=add(energies[0][c],energies[0][d]):continue
                v=vertex(a,b,c,d)
                if v==ZERO:continue
                out=apply_word(mask,[(c,False),(d,False),(b,True),(a,True)])
                if out is None:continue
                dest,sgn=out
                if dest not in back:outside+=1;continue
                outbits,outphase=back[dest]
                literal[outbits][bits]=add(literal[outbits][bits],scale(v,phase*outphase*sgn))
    assert outside==0
    compact=[[ZERO for _ in basis] for _ in basis]
    for bits in basis:
        occupied=[i for i in range(m) if (bits>>i)&1]
        for r,ar in A.items():
            fs=[cosine(r*k) if r%2 else sine(r*k) for k in reps]
            gs=[sine(r*k) if r%2 else cosine(r*k) for k in reps]
            # Diagonal (4/N)[Q0^2-Qg^2]; diagonal BdagB corrections cancel.
            q0=F(len(occupied));qg=ZERO
            for i in occupied:qg=add(qg,gs[i])
            diag=sub(scalar(q0*q0),mul(qg,qg))
            compact[bits][bits]=add(compact[bits][bits],scale(diag,4*ar/N))
            for i in range(m):
                for j in occupied:
                    if i==j or (bits>>i)&1:continue
                    dest=bits^(1<<i)^(1<<j)
                    compact[dest][bits]=add(compact[dest][bits],scale(mul(fs[i],fs[j]),4*ar/N))
    assert compact==literal
    out={'N':N,'interaction':{'a1':'1','a2':'1/3'},'cyclotomic_basis':'Q[zeta_32], zeta_32^16=-1',
         'energy_equality':'EXACT integer/rational cyclotomic coefficients; no floating tolerance',
         'twist_convention':'one-body phase A=tw*pi/(2N); tw0 periodic and tw1 quarter-flux',
         'resonance_counts':counts,'literal_real_space_two_particle_vertices_checked':checked,
         'paired_modes':ps,'paired_Fock_dimension':1<<m,'paired_block_entries_checked':(1<<m)**2,
         'secular_transitions_leaving_paired_block':outside,
         'source_vertex_and_compact_block':'PASS',
         'scope':'One exact finite source consumer of the analytic all-N construction; not a full many-body simulation or an all-N proof by testing.',
         'seconds_after_imports':time.perf_counter()-started}
    (HERE/'EXACT_SOURCE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
