"""Exact all-state thermal moments for the actual spin-two OPEN chains1..6.

2H has integer entries in the unnormalized polynomial spin basis and is
diagonally similar to the physical Hermitian Hamiltonian. CRT reconstructs
Tr(2H)^k uniquely using the physical bound dim*(12*(n-1))^k. No low-energy
selection, fitted spectrum, spectral gap or unverified eigensolver is used.
The result supplies vacuum Krylov moments of the continuous history kernel.
"""
import pathlib,json,time,math,argparse
import numpy as np
import scipy.sparse as ss
import sympy as sp
ROOT=pathlib.Path(__file__).resolve().parent

def sector(n,mag):
    all_words=np.array(list(np.ndindex(*(5,)*n)),dtype=np.int8)
    words=all_words[np.sum(all_words.astype(np.int16)-2,axis=1)==mag]
    codes=np.array([sum(int(x)*5**j for j,x in enumerate(w))for w in words],dtype=np.int64)
    lookup={int(c):i for i,c in enumerate(codes)};rows=[];cols=[];values=[]
    for col,(code,w)in enumerate(zip(codes,words)):
        m=w.astype(np.int64)-2
        diag=2*sum(int(m[i])*int(m[i+1])for i in range(n-1))
        if diag:rows.append(col);cols.append(col);values.append(diag)
        for i in range(n-1):
            j=i+1
            for di in [1,-1]:
                if not(0<=int(w[i])+di<5 and 0<=int(w[j])-di<5):continue
                row=lookup[int(code)+di*5**i-di*5**j]
                value=(2-di*int(m[i]))*(2+di*int(m[j]))
                rows.append(row);cols.append(col);values.append(value)
    return ss.csr_matrix((np.array(values,dtype=np.int64),(rows,cols)),shape=(len(words),len(words)))

def acquire(n,degree):
    dim=5**n;bound=max(dim*(12*(n-1))**k for k in range(degree+1))
    primes=[];modulus=1;p=2**49
    while modulus<=2*bound:
        p=int(sp.nextprime(p+1000));primes.append(p);modulus*=p
    residues=[0]*(degree+1);current=1;timing=[]
    for prime in primes:
        start=time.monotonic();trace_mod=[0]*(degree+1)
        for mag in range(2*n+1):
            h=sector(n,mag);d=h.shape[0]
            if not d:continue
            # Every multiplication is signed-small sparse H times [0,p)
            # integers. This explicit row bound prevents int64 overflow.
            row_abs=np.asarray(abs(h).sum(axis=1)).ravel()
            assert int(row_abs.max(initial=0))*prime<2**62
            assert d*prime<2**62
            a=np.eye(d,dtype=np.int64)
            for k in range(degree+1):
                trace_mod[k]=(trace_mod[k]+(1 if mag==0 else 2)*int(np.trace(a)))%prime
                if k<degree:a=(h@a)%prime
        inv=pow(current,-1,prime)
        for k,r in enumerate(trace_mod):residues[k]+=current*(((r-residues[k])*inv)%prime)
        current*=prime
        elapsed=time.monotonic()-start;timing.append(elapsed)
        print('open',n,'prime',prime,'seconds',round(elapsed,3),flush=True)
    exact=[r if r<=current//2 else r-current for r in residues]
    assert exact[0]==dim and exact[1]==0
    assert exact[2]==48*(n-1)*dim
    assert exact[3]==-48*(n-1)*dim
    assert all(abs(v)<=dim*(12*(n-1))**k for k,v in enumerate(exact))
    return {'n':n,'degree':degree,'trace_2H_powers':[str(x)for x in exact],
        'CRT_primes':primes,'CRT_modulus':str(current),'unique_reconstruction_bound':str(bound),
        'seconds':sum(timing),'per_prime_seconds':timing,
        'status':'EXACT_INTEGER_TRACE_MOMENTS_ALL_MAGNETIZATION_SECTORS'}

def run(degree=24):
    path=ROOT/f'data/open_moments_exact_degree{degree}.json';answer={'degree':degree,'chains':[],
        'scope':'Actual uniform spin-two open chains1..6, used as moments of the actual continuous-time spatial kernel. Not a long-ring spectrum.'}
    answer['chains'].append({'n':1,'degree':degree,'trace_2H_powers':['5']+['0']*degree,'status':'EXACT_ONE_SITE'})
    for n in range(2,7):
        answer['chains'].append(acquire(n,degree));path.write_text(json.dumps(answer,indent=2))
    print('EXACT_OPEN_MOMENTS_ACQUIRED',flush=True);return answer

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--degree',type=int,default=24);args=p.parse_args();run(args.degree)
