"""Exact complete small-cycle moments for the A4 N-sector norm count.

I/P closing-bond rotations are rational integer operations in the source
polynomial basis. All physical magnetization sectors are retained.
"""
import pathlib,sys,json,time,argparse,math,functools
import numpy as np
import scipy.sparse as ss
ROOT=pathlib.Path(__file__).resolve().parents[1]
PRIOR=ROOT.parents[1]/'sol8_opportunity_selection_20261027/obstruction_first/continuation'
sys.path.insert(0,str(PRIOR))
from acquire_open_moments import sector
import sympy as sp

@functools.lru_cache(None)
def cycle(n,mag,kind):
    words=np.array(list(np.ndindex(*(5,)*n)),dtype=np.int8)
    words=words[np.sum(words.astype(np.int16)-2,axis=1)==mag]
    codes=[sum(int(x)*5**j for j,x in enumerate(w))for w in words]
    lookup={int(c):i for i,c in enumerate(codes)}
    rr=[];cc=[];vv=[]
    for col,(code,w)in enumerate(zip(codes,words)):
        m=w.astype(np.int64)-2;diag=2*int(m[-1])*int(m[0])
        if diag:rr.append(col);cc.append(col);vv.append(diag)
        for di in [1,-1]:
            if not(0<=int(w[-1])+di<5 and 0<=int(w[0])-di<5):continue
            row=lookup[code+di*5**(n-1)-di]
            val=(2-di*int(m[-1]))*(2+di*int(m[0]))
            if kind=='P':val=-val
            rr.append(row);cc.append(col);vv.append(val)
    extra=ss.csr_matrix((np.array(vv,dtype=np.int64),(rr,cc)),shape=(len(words),len(words)))
    return sector(n,mag)+extra,words

def acquire(n,kind,degree):
    dim=5**n;bound=dim*(12*n)**degree
    primes=[];modulus=1;p=2**49
    while modulus<=2*bound:
        p=int(sp.nextprime(p+1000));primes.append(p);modulus*=p
    residues=[0]*(degree+1);current=1;timing=[]
    for prime in primes:
        start=time.monotonic();trace_mod=[0]*(degree+1)
        for mag in range(2*n+1):
            h,_=cycle(n,mag,kind);d=h.shape[0]
            if not d:continue
            row_abs=np.asarray(abs(h).sum(axis=1)).ravel()
            assert int(row_abs.max(initial=0))*prime<2**62 and d*prime<2**62
            a=np.eye(d,dtype=np.int64)
            for k in range(degree+1):
                trace_mod[k]=(trace_mod[k]+(1 if mag==0 else 2)*int(np.trace(a)))%prime
                if k<degree:a=(h@a)%prime
        inv=pow(current,-1,prime)
        for k,r in enumerate(trace_mod):residues[k]+=current*(((r-residues[k])*inv)%prime)
        current*=prime;elapsed=time.monotonic()-start;timing.append(elapsed)
        print('cycle',n,kind,'prime',prime,'seconds',round(elapsed,3),flush=True)
    exact=[r if r<=current//2 else r-current for r in residues]
    assert exact[0]==dim and exact[1]==0
    assert all(abs(v)<=dim*(12*n)**k for k,v in enumerate(exact))
    return {'n':n,'twist':kind,'degree':degree,'trace_2H_powers':[str(x)for x in exact],
            'CRT_primes':primes,'CRT_modulus':str(current),
            'unique_reconstruction_bound':str(bound),'seconds':sum(timing),
            'per_prime_seconds':timing,'status':'EXACT_INTEGER_CYCLE_MOMENTS_ALL_MAGNETIZATION_SECTORS'}

def preview():
    import scipy.linalg as la
    output=[]
    for n in [2,3,4,6]:
        spectra={}
        for kind in ['I','P']:
            vals=[]
            for mag in range(2*n+1):
                h,words=cycle(n,mag,kind);d=h.shape[0]
                if not d:continue
                scales=np.array([math.prod(1/math.sqrt(math.comb(4,int(x)))for x in w)for w in words])
                physical=h.toarray()*scales[:,None]/scales[None,:]/2
                assert np.max(abs(physical-physical.T))<1e-13
                vals.extend(la.eigvalsh(physical,check_finite=False).tolist()*(1 if mag==0 else 2))
            spectra[kind]=np.array(vals)
        for beta in [.75,1.5]:
            z={kind:float(np.exp(-beta*es).sum()/5**n)for kind,es in spectra.items()}
            row={'n':n,'beta':beta,'N_moment':(z['I']-z['P'])/4,'normalized_traces':z}
            output.append(row);print(row,flush=True)
    (ROOT/'results/cycle_preview.json').write_text(json.dumps({'rows':output},indent=2)+'\n')

def main():
    p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=6);p.add_argument('--degree',type=int,default=192)
    p.add_argument('--preview',action='store_true');args=p.parse_args()
    if args.preview:preview();return
    result={'degree':args.degree,'n':args.n,'records':[]}
    target=ROOT/'results'/f'cycle{args.n}_moments_exact_degree{args.degree}.json'
    for kind in ['I','P']:
        result['records'].append(acquire(args.n,kind,args.degree))
        target.write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
