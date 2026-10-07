#!/usr/bin/env python3
"""Finite diagnostics for the proposed positive-kernel/XXZ reduction.
These tests do not implement or certify the imported Chen--Liu FPRAS.
Run: python checks/check_mechanisms.py
"""
from __future__ import annotations
import itertools, json, math, time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parents[1]

def embedding_count(word: tuple[int, ...], alphabet: int, sweeps: int) -> int:
    dp = [1] + [0] * len(word)
    for symbol in list(range(alphabet)) * sweeps:
        for j in range(len(word)-1, -1, -1):
            if word[j] == symbol:
                dp[j+1] += dp[j]
    return dp[-1]

def test_words() -> dict:
    fixtures = 0
    for alphabet in (1, 2, 3):
        for sweeps in range(1, 7):
            for k in range(0, 7):
                for word in itertools.product(range(alphabet), repeat=k):
                    got = embedding_count(word, alphabet, sweeps)
                    lo = math.comb(sweeps, k) if k <= sweeps else 0
                    hi = math.comb(sweeps+k-1, k) if k else 1
                    assert lo <= got <= hi, (word, sweeps, lo, got, hi)
                    fixtures += 1
    return {'fixtures': fixtures, 'arithmetic': 'exact integer', 'passed': True}

def convolve(a, b):
    out = [F(0)] * (len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out

def test_scalar_tail_majorant() -> dict:
    fixtures = 0
    for weights in ((F(1,3), F(2,5)), (F(1,10), F(3,4), F(7,6))):
        for m in range(1, 8):
            coeff = [F(1)]
            for _ in range(m):
                for a in weights:
                    coeff = convolve(coeff, [F(1), a/m])
            T = sum(weights)
            for k, c in enumerate(coeff):
                assert c <= T**k / math.factorial(k)
                fixtures += 1
    return {'coefficient_inequalities': fixtures, 'arithmetic': 'exact rational', 'passed': True}

def local_A(f: float, d: float) -> np.ndarray:
    if f < abs(d) or f < 0:
        raise ValueError('Expected f >= |d|.')
    dp, dm = max(d, 0), max(-d, 0)
    return np.array([[dm,0,0,0],[0,dp,f,0],[0,f,dp,0],[0,0,0,dm]], dtype=float)

def embed_two(n: int, u: int, v: int, a: np.ndarray) -> np.ndarray:
    N = 1 << n
    out = np.zeros((N,N))
    for col in range(N):
        bits = [(col >> (n-1-j)) & 1 for j in range(n)]
        ci = 2*bits[u]+bits[v]
        for z in range(4):
            bb = bits.copy(); bb[u], bb[v] = z//2, z%2
            row = sum(bit << (n-1-j) for j,bit in enumerate(bb))
            out[row,col] += a[z,ci]
    return out

def min_kernel_bits(n: int, tau: F, fmin: F) -> int:
    D = n*n
    b = min(F(1), tau*fmin)
    lam = b**D / math.factorial(D)
    # Return B with 2**(-B) <= lambda, using exact integer bit lengths.
    return max(0, lam.denominator.bit_length()-lam.numerator.bit_length()+1)

def test_entrywise_spin_kernels() -> dict:
    rows = []
    alpha = F(1, 8)
    for n in (2, 3, 4):
        for case in range(4):
            edges = [(j,j+1,F(j+2,4),F((-1)**(j+case)*(j+2),8)) for j in range(n-1)]
            if n > 2 and case == 3:
                edges.append((0,n-1,F(2,3),F(2,3)))
            tau = (F(1,20),F(1,3),F(1),F(3,2))[case]
            terms = [embed_two(n,u,v,local_A(float(f),float(d))) for u,v,f,d in edges]
            V = sum(f+max(d,F(0)) for _,_,f,d in edges)
            T = tau*V
            B = min_kernel_bits(n,tau,min(e[2] for e in edges))
            log_budget = math.ceil(math.log2(64/float(alpha)))
            K = max(1, math.ceil(6*float(T)), B+log_budget)
            m = max(2*K, math.ceil(8*K*K/float(alpha)))
            sweep = np.eye(1<<n)
            for term in terms:
                sweep = (np.eye(1<<n)+float(tau)/m*term) @ sweep
            approx = np.linalg.matrix_power(sweep,m)
            exact = expm(float(tau)*sum(terms))
            support = exact > 1e-100
            relative = np.max(np.abs(approx[support]/exact[support]-1))
            zero_error = np.max(np.abs(approx[~support])) if (~support).any() else 0
            assert relative <= float(alpha)+1e-5, (n,case,relative)
            assert zero_error <= 1e-12
            rows.append({'n':n,'case':case,'tau':str(tau),'K':K,'m':m,
                         'max_relative_error':float(relative),'zero_error':float(zero_error)})
    return {'fixtures':rows,'arithmetic':'double precision diagnostic, not a certificate','passed':True}

def rational_gate(f: F, d: F, t: F):
    dp,dm=max(d,F(0)),max(-d,F(0))
    a,b,c=1+t*dm,1+t*dp,t*f
    assert a <= b+c and b <= a+c and c <= a+b
    return [[a,F(0),F(0),F(0)], [F(0),b,c,F(0)],
            [F(0),c,b,F(0)], [F(0),F(0),F(0),a]]

def matmul(a,b):
    return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*b)] for row in a]

def transpose(a): return [list(x) for x in zip(*a)]

def partial_trace_first_qubit(rho):
    return [[sum((rho[2*a+b][2*c+b] for b in (0,1)),F(0)) for c in (0,1)] for a in (0,1)]

def tensor_replica_count(gate, q: int, swapped_qubits: tuple[int,...], pins=None):
    """Exact enumeration of a two-qubit C C^T replica network, C=one gate.
    q copies, two gate nodes per copy; each wire is an independent bit.
    A copy has boundary bits x and midpoint bits y. Replica wiring replaces
    the outgoing x on selected qubits by the next copy's x.
    """
    total=F(0)
    pins = pins or {}
    for z in itertools.product((0,1), repeat=4*q):
        # For each replica store x0,x1,y0,y1.
        if any(z[k] != value for k,value in pins.items()):
            continue
        weight=F(1)
        for r in range(q):
            x=z[4*r:4*r+2]; y=z[4*r+2:4*r+4]
            out=list(x)
            for j in swapped_qubits:
                out[j]=z[4*((r+1)%q)+j]
            weight *= gate[2*x[0]+x[1]][2*y[0]+y[1]]
            weight *= gate[2*out[0]+out[1]][2*y[0]+y[1]]
        total += weight
    return total

def test_replica_and_pins() -> dict:
    fixtures=0
    examples=[]
    for f,d,t in ((F(1),F(1),F(1,3)), (F(3,2),F(-1),F(1,5)),
                  (F(1),F(0),F(1,4))):
        C=rational_gate(f,d,t)
        # Positive one-site diagonal factors break the spin-flip symmetry.
        # They are two-leg, degree-one log-concave tensors.
        row_factors=[F(7,5),F(7,5),F(1),F(1)]
        col_factors=[F(1),F(6,5),F(1),F(6,5)]
        C=[[row_factors[i]*C[i][j]*col_factors[j] for j in range(4)] for i in range(4)]
        density=matmul(C,transpose(C))
        Z=sum((density[i][i] for i in range(4)),F(0))
        for length in range(5):
            for prefix in itertools.product((0,1),repeat=length):
                pins=dict(enumerate(prefix))
                got=tensor_replica_count(C,1,(),pins)
                want=F(0)
                for x0,x1,y0,y1 in itertools.product((0,1),repeat=4):
                    bits=(x0,x1,y0,y1)
                    if bits[:length]==prefix:
                        want += C[2*x0+x1][2*y0+y1]**2
                assert got==want
                fixtures+=1
        reduced=partial_trace_first_qubit(density)
        for q in (2,3):
            power=reduced
            for _ in range(q-1): power=matmul(power,reduced)
            want=power[0][0]+power[1][1]
            got=tensor_replica_count(C,q,(0,))
            assert got==want
            fixtures+=1
            examples.append({'f':str(f),'d':str(d),'t':str(t),'q':q,'moment':str(got/Z**q)})
    return {'equalities':fixtures,'examples':examples,'arithmetic':'exact rational exhaustive contraction','passed':True}

def test_triangle_region() -> dict:
    fixtures=0
    for f in (F(1,7),F(1),F(7,2)):
        for r in (F(-1),F(-1,2),F(0),F(1,3),F(1)):
            d=r*f
            for t in (F(1,100),F(1,20),F(1,4)):
                a,b,c=1+t*max(-d,0),1+t*max(d,0),t*f
                eig=(a+b+c,a-b-c,-a+b-c,-a-b+c)
                assert sum(e>0 for e in eig)==1
                fixtures+=1
    for d in (F(-2),F(2)):
        f=F(1);t=F(1,100)
        a,b,c=1+t*max(-d,0),1+t*max(d,0),t*f
        eig=(a+b+c,a-b-c,-a+b-c,-a-b+c)
        assert sum(e>0 for e in eig)==2
    return {'inside_cone_fixtures':fixtures,'outside_cone_counterexamples':2,'arithmetic':'exact rational','passed':True}

def test_small_trace_error_bad_relative_purity() -> dict:
    rows=[]
    for k in (4,8,12,16):
        # d=2^(4k), delta=2^-k: trace distance tends to zero but purity ratio grows.
        d=2**(4*k);delta=F(1,2**k)
        trace=delta*(1-F(1,d))
        ratio=1+delta**2*(d-1)
        assert ratio>2**(2*k)
        rows.append({'dimension':str(d),'trace_distance':str(trace),'purity_ratio':str(ratio)})
    return {'examples':rows,'arithmetic':'exact rational','passed':True}

def test_ground_pf_and_entropy_obstruction() -> dict:
    fixtures=[]
    for n in (3,4,5):
        edges=[(i,i+1,0.5+0.2*i,(-1)**i*0.2) for i in range(n-1)]
        terms=[embed_two(n,u,v,local_A(f,d)) for u,v,f,d in edges]
        field_norm=0.0
        for site in range(n):
            h=(-1)**site*(site+1)/11
            diag=[]
            for x in range(1<<n):
                z=1-2*((x>>(n-1-site))&1)
                diag.append(abs(h)-h*z)
            terms.append(np.diag(diag));field_norm+=2*abs(h)
        A=sum(terms)
        sector=[x for x in range(1<<n) if x.bit_count()==n//2]
        As=A[np.ix_(sector,sector)]
        vals,vecs=np.linalg.eigh(As)
        v=vecs[:,-1]
        if v[0]<0:v=-v
        assert np.min(v)>0
        gap=vals[-1]-vals[-2]
        V=sum(f+max(d,0) for _,_,f,d in edges)+field_norm
        fmin=min(f for _,_,f,d in edges)
        logmu=-0.5*n*math.log(2)+n*n*math.log(fmin/V)
        assert np.log(np.min(v))>=logmu-1e-10
        alpha=0.01
        tau=(-2*logmu+math.log(1/alpha))/gap
        col=expm(tau*(As-vals[-1]*np.eye(len(sector))))[:,0]
        relative=np.max(np.abs(col/(v*v[0])-1))
        assert relative<=alpha+1e-8
        fixtures.append({'n':n,'sector_size':len(sector),'gap':float(gap),
                         'time':float(tau),'log_minimum_bound':float(logmu),
                         'relative_column_error':float(relative)})
    moments=[]
    for n in (8,16,32):
        R=2**n
        for q in (2,3,5,10):
            m1=F(1,2**q)*(1+F(1,R**(q-1)))
            m2=F(1,2**q)*(1+F(1,(R*R)**(q-1)))
            rel=abs(m1/m2-1)
            assert rel<=F(1,R)
            moments.append({'n':n,'q':q,'relative_moment_difference':str(rel),
                            'entropy_gap_nats':0.5*n*math.log(2)})
    return {'ground_diagnostics':fixtures,'moment_obstruction_exact_checks':moments,
            'passed':True,'scope':'PF tests numerical; moment comparisons exact rational.'}



def test_global_ground_replica_transfer() -> dict:
    rng=np.random.default_rng(202610071)
    rows=[]
    for n in (2,3,4):
        N=1<<n
        # The transfer lemma is general: random real eigenbases, not just XXZ.
        U,_=np.linalg.qr(rng.normal(size=(N,N)))
        for g in (1,2,3):
            gap=0.37+0.11*g
            energies=np.r_[np.zeros(g),np.linspace(gap,2.4*gap,N-g)]
            rho0=(U[:,:g]@U[:,:g].T)/g
            for size in sorted(set((1,n//2,n))):
                ds=1<<size;de=N//ds
                red0=np.trace(rho0.reshape(ds,de,ds,de),axis1=1,axis2=3)
                for q in (2,3,5):
                    eps=0.05
                    beta=(n*math.log(2)+(q-1)*size*math.log(2)+math.log(8*q/eps))/gap
                    weights=np.exp(-beta*energies);weights/=weights.sum()
                    rhob=(U*weights)@U.T
                    redb=np.trace(rhob.reshape(ds,de,ds,de),axis1=1,axis2=3)
                    m0=float(np.trace(np.linalg.matrix_power(red0,q)))
                    mb=float(np.trace(np.linalg.matrix_power(redb,q)))
                    ratioerror=abs(mb/m0-1)
                    bound=2*q*N*(ds**(q-1))*math.exp(-beta*gap)
                    assert m0>=ds**(1-q)*(1-1e-10)
                    assert ratioerror<=bound+1e-9
                    assert bound<=eps/4*(1+1e-10)
                    rows.append({'n':n,'ground_rank':g,'subsystem_size':size,'q':q,
                                 'beta':beta,'relative_error':ratioerror,'bound':bound})
    return {'fixtures':len(rows),'examples':rows,'passed':True,
            'scope':'Floating-point tests of the general transfer bound, not the FPRAS.'}


def main():
    start=time.time()
    tests=(test_words,test_scalar_tail_majorant,test_triangle_region,
           test_entrywise_spin_kernels,test_replica_and_pins,
           test_small_trace_error_bad_relative_purity,test_ground_pf_and_entropy_obstruction,
           test_global_ground_replica_transfer)
    result={test.__name__:test() for test in tests}
    result['elapsed_seconds']=time.time()-start
    result['scope']='Finite checks only; no execution or certification of the general counting algorithm.'
    out=ROOT/'checks'/'results.json'
    out.write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
