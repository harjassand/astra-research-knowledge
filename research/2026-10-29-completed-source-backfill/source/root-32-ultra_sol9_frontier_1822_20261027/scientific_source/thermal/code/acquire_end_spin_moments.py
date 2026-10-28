"""All-state exact end-spin thermal moments on the physical open chains2..6.

Tr[(-Sz_left Sz_right) (2H)^k] is integer in the polynomial spin basis.
This provides the actual spin-one boundary-message moments of K_beta/5.
No eigenvalue accuracy, source-kernel cutoff, low-energy selection or finite
rank assumption enters the acquired integers.
"""
import pathlib,sys,json,time,argparse
import numpy as np
import sympy as sp
ROOT=pathlib.Path(__file__).resolve().parents[1]
PRIOR=ROOT.parents[1]/'sol8_opportunity_selection_20261027/obstruction_first/continuation'
sys.path.insert(0,str(PRIOR))
from acquire_open_moments import sector

def acquire(n,degree):
    dim=5**n;bound=4*dim*(12*(n-1))**degree
    primes=[];modulus=1;p=2**49
    while modulus<=2*bound:
        p=int(sp.nextprime(p+1000));primes.append(p);modulus*=p
    residues=[0]*(degree+1);current=1;timing=[]
    all_words=np.array(list(np.ndindex(*(5,)*n)),dtype=np.int8)
    mags=np.sum(all_words.astype(np.int16)-2,axis=1)
    for prime in primes:
        start=time.monotonic();trace_mod=[0]*(degree+1)
        for mag in range(2*n+1):
            h=sector(n,mag);d=h.shape[0]
            if not d:continue
            words=all_words[mags==mag]
            obs=-(words[:,0].astype(np.int64)-2)*(words[:,-1].astype(np.int64)-2)
            row_abs=np.asarray(abs(h).sum(axis=1)).ravel()
            assert int(row_abs.max(initial=0))*prime<2**62
            assert 4*d*prime<2**62
            a=np.eye(d,dtype=np.int64)
            for k in range(degree+1):
                value=int(np.dot(obs,np.diag(a)))
                trace_mod[k]=(trace_mod[k]+(1 if mag==0 else 2)*value)%prime
                if k<degree:a=(h@a)%prime
        inv=pow(current,-1,prime)
        for k,r in enumerate(trace_mod):
            residues[k]+=current*(((r-residues[k])*inv)%prime)
        current*=prime;elapsed=time.monotonic()-start;timing.append(elapsed)
        print('end-spin',n,'prime',prime,'seconds',round(elapsed,3),flush=True)
    exact=[r if r<=current//2 else r-current for r in residues]
    assert exact[0]==0
    assert all(v==0 for v in exact[:n-1])
    assert all(abs(v)<=4*dim*(12*(n-1))**k for k,v in enumerate(exact))
    return {'n':n,'degree':degree,'trace_minus_SzSz_2H_powers':[str(x)for x in exact],
            'CRT_primes':primes,'CRT_modulus':str(current),
            'unique_reconstruction_bound':str(bound),'seconds':sum(timing),
            'per_prime_seconds':timing,
            'status':'EXACT_INTEGER_END_SPIN_MOMENTS_ALL_MAGNETIZATION_SECTORS'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--degree',type=int,default=192);args=p.parse_args()
    result={'degree':args.degree,'chains':[],
            'observable':'-Sz_left Sz_right; standard physical spin2, all sectors.',
            'kernel_identity':'<f_alpha,(K_beta/5)^r f_alpha> = Tr[-Sz_left Sz_right exp(-beta H_open,r+2)]/5^r.'}
    target=ROOT/'results'/f'end_spin_moments_exact_degree{args.degree}.json'
    for n in range(2,7):
        result['chains'].append(acquire(n,args.degree))
        target.write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
