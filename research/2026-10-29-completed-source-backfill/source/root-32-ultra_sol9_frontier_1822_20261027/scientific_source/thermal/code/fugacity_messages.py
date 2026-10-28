"""Scalar history messages from inhomogeneous open spin-two blocks.

Numerical discovery only. SU(2) path matrices include every multiplet.
The proof and exact acquisition consumer are separate from this proposer.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import functools, itertools, json, pathlib, time, argparse
import numpy as np
import scipy.linalg as la
from sympy.physics.wigner import wigner_6j

ROOT=pathlib.Path(__file__).resolve().parents[1]

@functools.lru_cache(None)
def paths(n):
    out=[(0,)]
    for k in range(n):
        out=[p+(j,) for p in out for j in range(abs(p[-1]-2),p[-1]+3)]
    return out

@functools.lru_cache(None)
def racah(a,d,es):
    fs=tuple(f for f in range(5) if abs(a-f)<=d<=a+f)
    u=np.array([[float(wigner_6j(a,2,e,2,d,f))*np.sqrt((2*e+1)*(2*f+1))
                  for f in fs] for e in es])
    assert np.max(np.abs(u@u.T-np.eye(len(es))))<2e-14
    return (u*np.array([(f*(f+1)-12)/2 for f in fs]))@u.T

@functools.lru_cache(None)
def blocks(n):
    result=[]
    ps=paths(n)
    assert sum(2*p[-1]+1 for p in ps)==5**n
    for total in range(2*n+1):
        sub=[p for p in ps if p[-1]==total]
        if not sub: continue
        bonds=[]
        for edge in range(n-1):
            mat=np.zeros((len(sub),len(sub)))
            groups={}
            for i,p in enumerate(sub):
                key=p[:edge+1]+p[edge+2:]
                groups.setdefault(key,[]).append((i,p))
            for group in groups.values():
                indices=[i for i,p in group]
                a=group[0][1][edge]; d=group[0][1][edge+2]
                es=tuple(p[edge+1] for i,p in group)
                mat[np.ix_(indices,indices)]=racah(a,d,es)
            bonds.append(mat)
        result.append((total,np.array(bonds)))
    return result

CACHE={}
@functools.lru_cache(None)
def trace(couplings):
    if not couplings:return 5.0
    z=0.0
    for spin,bs in blocks(len(couplings)+1):
        h=np.tensordot(couplings,bs,axes=1)
        vals=la.eigvalsh(h,check_finite=False,overwrite_a=True)
        z+=(2*spin+1)*np.sum(np.exp(-vals))
    CACHE[','.join(format(x,'.17g') for x in couplings)]=z
    return float(z)

def entries(beta, messages):
    """Each message is (r,a): D_sqrt(beta)*r K_1 D_a K_1 v.

    v occupies index0. All inner products are literal physical open traces.
    """
    k=len(messages)+1
    g=np.zeros((k,k));h=np.zeros((k,k));h2=np.zeros((k,k))
    g[0,0]=1;h[0,0]=5;h2[0,0]=trace((beta,))
    for i,(r,a) in enumerate(messages,1):
        g[0,i]=g[i,0]=trace((a,))
        h[0,i]=h[i,0]=trace((a,beta*r))
        h2[0,i]=h2[i,0]=trace((a,beta*r,beta))
        for j,(s,b) in enumerate(messages[:i],1):
            g[i,j]=g[j,i]=trace((a,beta*r*s,b))
            h[i,j]=h[j,i]=trace((a,beta*r,beta*s,b))
            h2[i,j]=h2[j,i]=trace((a,beta*r,beta,beta*s,b))
    return g,h,h2

def propose(beta,messages,cutoff=1e-11):
    g,h,h2=entries(beta,messages)
    scale=1/np.sqrt(np.diag(g)); g=scale[:,None]*g*scale[None,:]
    h=scale[:,None]*h*scale[None,:];h2=scale[:,None]*h2*scale[None,:]
    vals,vecs=la.eigh(g)
    keep=vals>cutoff*vals[-1]
    q=vecs[:,keep]/np.sqrt(vals[keep])
    es,us=la.eigh(q.T@h@q)
    c=q@us[:,-1]
    theta=float(c@h@c/(c@g@c))
    variance=float(c@h2@c/(c@g@c)-theta**2)
    answer={'beta':beta,'messages':messages,'Gram_eigenvalues_scaled':vals.tolist(),
        'retained_rank':int(sum(keep)), 'theta_K':theta,'variance_K':variance,
        'relative_variance':variance/theta**2,
        'candidate_coefficients':(c*scale).tolist(),
        'scope':'Uncertified float64 discovery; all SU2 sectors included.'}
    return answer

def control():
    # Pair eigenvalues and complete degeneracies; exact open traces from prior run.
    z=trace((.75,))
    exact=sum((2*j+1)*np.exp(-.75*(j*(j+1)-12)/2) for j in range(5))
    assert abs(z/exact-1)<3e-15
    prior=ROOT.parents[1]/'sol8_opportunity_selection_20261027/obstruction_first/continuation/data/open_moments_exact_degree192.json'
    import mpmath as mp
    mp.mp.dps=70
    records=json.loads(prior.read_text())['chains']
    controls=[]
    for rec in records:
        n=rec['n']; beta=mp.mpf('0.75')
        ref=sum(mp.mpf(v)*(-beta/2)**k/mp.factorial(k) for k,v in enumerate(rec['trace_2H_powers']))
        val=trace((.75,)*(n-1)) if n>1 else 5.0
        err=abs(val/float(ref)-1)
        assert err<3e-13,(n,err)
        controls.append({'n':n,'relative_error_vs_prior_exact_moments':err,
                         'largest_multiplicity':max(len(x) for j,x in [(J,[p for p in paths(n) if p[-1]==J]) for J in range(2*n+1)])})
    return controls

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--beta',type=float,default=.75)
    parser.add_argument('--grid',choices=['small','wide'],default='small')
    args=parser.parse_args(); start=time.monotonic()
    controls=control();b=args.beta
    if args.grid=='small':
        messages=[(1.,0.),(1.,b),(.75,b),(1.25,b),(1.,.5*b),(1.,1.5*b),(.75,.5*b),(1.25,1.5*b)]
    else:
        messages=[(r,a*b) for r in [.6,.8,1.,1.2,1.4] for a in [0.,.5,1.,1.5,2.]]
    rows=[]
    for cutoff in [1e-7,1e-9,1e-11,1e-13]:
        row=propose(b,messages,cutoff);rows.append(row)
        print({k:row[k]for k in ['beta','retained_rank','theta_K','variance_K','relative_variance']},flush=True)
    result={'controls':controls,'proposals':rows,'seconds':time.monotonic()-start,
            'cached_trace_count':trace.cache_info().currsize}
    target=ROOT/'results'/f'fugacity_discovery_beta{b:g}_{args.grid}.json'
    target.write_text(json.dumps(result,indent=2)+'\n')
    (ROOT/'results'/f'fugacity_trace_discovery_beta{b:g}_{args.grid}.json').write_text(json.dumps(CACHE,indent=2)+'\n')
    print('seconds',result['seconds'],flush=True)

if __name__=='__main__': main()
