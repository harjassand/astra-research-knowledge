"""All-sector finite-N compilation; binary64 diagnostic, NOT an interval solver.

The report gives a separate exact rational/generalized-eigenvalue algorithm.
This module checks the distinct-site normalization and keeps every total-spin
sector with its full multiplicity. It never uses a symmetric-sector-only
partition function. Dense Hilbert matrices appear only in the N=6 audit.
"""
import json,time,math
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import numpy as np
from scipy.special import logsumexp
from threadpoolctl import threadpool_limits
from calibrated_source import pauli_terms,heisenberg_commutator,expectation_polynomial
from polynomial_tools import indices

ROOT=Path(__file__).resolve().parent


def spins(L):
    d=L+1; plus=np.zeros((d,d),dtype=complex)
    for k in range(1,d): plus[k-1,k]=math.sqrt(k*(L-k+1))
    minus=plus.conj().T
    return [(plus+minus)/2,(plus-minus)/(2j),np.diag([L/2-k for k in range(d)])]


def matpoly_mul(p,q):
    out={}
    for a,A in p.items():
        for b,B in q.items():
            c=tuple(x+y for x,y in zip(a,b))
            value=A@B
            out[c]=out.get(c,0)+value
    return out


def block(N,L,p,K):
    S=spins(L); I=np.eye(L+1,dtype=complex)
    powers=[None]
    for j in range(1,K+1):
        r=j//2
        terms={}
        for a in product(range(r+1),repeat=3):
            if sum(a)!=r: continue
            c=math.factorial(r)/math.prod(math.factorial(x) for x in a)
            alpha=tuple(2*x for x in a)
            if j%2==0: terms[alpha]=N*c*I
            else:
                for q in range(3):
                    b=list(alpha); b[q]+=1; b=tuple(b)
                    terms[b]=terms.get(b,0)+2*c*S[q]
        powers.append(terms)
    E=[{(0,0,0):I}]
    for k in range(1,K+1):
        result={}
        for j in range(1,k+1):
            sign=1 if j%2 else -1
            for a,A in matpoly_mul(E[k-j],powers[j]).items():
                result[a]=result.get(a,0)+sign*A/k
        E.append(result)
    H=np.zeros_like(I)
    for a,c in p.items():
        count=math.factorial(N)//(math.factorial(N-sum(a))*math.prod(math.factorial(x) for x in a))
        H+=float(N*c/count)*E[sum(a)][a]
    assert np.max(np.abs(H-H.conj().T))<1e-8
    return H


def schur_spectrum(N,p,K):
    vals=[]; multiplicities=[]; dimensions=[]
    for L in range(N%2,N+1,2):
        H=block(N,L,p,K)
        mult=math.comb(N,(N-L)//2)-(math.comb(N,(N-L)//2-1) if (N-L)//2>=1 else 0)
        dims=L+1; dimensions.append((dims,mult))
        vals.extend(np.linalg.eigvalsh(H)); multiplicities.extend([mult]*dims)
    assert sum(d*m for d,m in dimensions)==2**N
    return np.array(vals),multiplicities,dimensions


def full_matrix(N,p):
    H=np.zeros((1<<N,1<<N),dtype=complex)
    for (x,z),c in pauli_terms(N,p).items():
        phase=1j**((x&z).bit_count())
        for col in range(1<<N):
            H[col^x,col]+=float(c)*phase*((-1)**((z&col).bit_count()))
    return H


def main():
    start=time.perf_counter()
    # A generic rational model exercises all monomials and Y phases.
    generic={a:Q((i%7)-3,97) for i,a in enumerate(indices(4)) if i%7!=3}
    N=6
    vals,mults,dims=schur_spectrum(N,generic,4)
    expanded=np.sort(np.repeat(vals,mults))
    full=np.linalg.eigvalsh(full_matrix(N,generic))
    difference=float(np.max(np.abs(expanded-full)))
    assert difference<1e-10
    # Exact central blind spot and exact tagged derivative, at N=6 and g=1.
    central=pauli_terms(N,{(2,0,0):Q(-1),(0,2,0):Q(-1),(0,0,2):Q(-1)})
    collective=[]
    for a in [(1,0,0),(0,1,0),(0,0,1)]:
        comm,_=heisenberg_commutator(central,pauli_terms(N,{a:Q(1)}))
        assert comm=={}; collective.append(True)
    comm,_=heisenberg_commutator(central,{(1,1):Q(1)})
    tagged=expectation_polynomial(comm,(1,0),N)
    assert tagged=={(0,0,1):Q(-4)}
    rows=[]
    p={(0,0,4):Q(-1),(1,0,0):Q(-32,27)}
    for n in [6,16,64]:
        t=time.perf_counter(); vv,mm,dd=schur_spectrum(n,p,4)
        f=-logsumexp(-2*vv+np.log(np.array(mm,dtype=float)))/(2*n)
        rows.append({'N':n,'full_hilbert_dimension':str(2**n),'number_of_blocks':len(dd),
                     'largest_block':max(d for d,m in dd),'stored_matrix_entries':sum(d*d for d,m in dd),
                     'distinct_eigenvalues_with_block_multiplicity':sum(d for d,m in dd),
                     'free_energy_beta2_binary64':float(f),'seconds':time.perf_counter()-t})
    result={'generic_degree4_spectral_audit_N':6,'max_eigenvalue_difference_binary64':difference,
            'exact_collective_central_commutators_zero':collective,
            'exact_tagged_derivative':'-4 r_z',
            'scope':'Numerical Schur diagnostic only; the principal certificates use rational global state bounds.',
            'finite_size_rows':rows,'wall_seconds':time.perf_counter()-start}
    (ROOT/'SCHUR_DIAGNOSTIC.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':
    with threadpool_limits(limits=1): main()
