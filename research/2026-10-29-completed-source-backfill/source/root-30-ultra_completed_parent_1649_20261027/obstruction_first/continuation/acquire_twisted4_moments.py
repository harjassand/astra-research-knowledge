"""Exact four-site A4-projection thermal data, not a fitted sector model.

Use source conjugacy angles pi and2pi/3. In the polynomial spin basis,
2H_pi has integer entries and2H_C is over Z[zeta], zeta²+zeta+1=0.
The latter traces are real Galois-invariant integers; the zeta coefficient
is checked zero modulo every CRT prime. All magnetizations are included.
"""
import pathlib,json,math,time
import numpy as np
import scipy.sparse as ss
import sympy as sp
from acquire_open_moments import sector
ROOT=pathlib.Path(__file__).resolve().parent

def matrices(mag,kind):
    n=4;words=np.array(list(np.ndindex(*(5,)*n)),dtype=np.int8)
    words=words[np.sum(words.astype(np.int16)-2,axis=1)==mag]
    codes=[sum(int(x)*5**j for j,x in enumerate(w))for w in words]
    lookup={int(c):i for i,c in enumerate(codes)};rr=[[],[]];cc=[[],[]];vv=[[],[]]
    for col,(code,w)in enumerate(zip(codes,words)):
        m=w.astype(np.int64)-2
        diag=2*int(m[3])*int(m[0])
        if diag:rr[0].append(col);cc[0].append(col);vv[0].append(diag)
        for di in [1,-1]:
            if not(0<=int(w[3])+di<5 and 0<=int(w[0])-di<5):continue
            row=lookup[code+di*5**3-di]
            value=(2-di*int(m[3]))*(2+di*int(m[0]))
            phase=(-1,0)if kind=='P'else((0,1)if di==1 else(-1,-1))
            for t in [0,1]:
                if phase[t]:rr[t].append(row);cc[t].append(col);vv[t].append(value*phase[t])
    extra=[ss.csr_matrix((np.array(vv[t],dtype=np.int64),(rr[t],cc[t])),shape=(len(words),len(words)))for t in [0,1]]
    return sector(4,mag)+extra[0],extra[1]

def acquire(kind,degree=192):
    bound=625*48**degree;modulus=1;p=2**49;primes=[]
    while modulus<=2*bound:p=int(sp.nextprime(p+1000));primes.append(p);modulus*=p
    residues=[0]*(degree+1);current=1;start=time.monotonic()
    for prime in primes:
        tr0=[0]*(degree+1);tr1=[0]*(degree+1)
        for mag in range(9):
            a,b=matrices(mag,kind);d=a.shape[0]
            row=np.asarray((abs(a)+2*abs(b)).sum(axis=1)).ravel()
            assert int(row.max(initial=0))*prime<2**62 and d*prime<2**62
            x=np.eye(d,dtype=np.int64);y=np.zeros((d,d),dtype=np.int64)
            for k in range(degree+1):
                mul=1 if mag==0 else 2
                tr0[k]=(tr0[k]+mul*int(np.trace(x)))%prime
                tr1[k]=(tr1[k]+mul*int(np.trace(y)))%prime
                if k<degree:
                    ax=a@x;by=b@y
                    yy=(a@y+b@x-by)%prime;xx=(ax-by)%prime;x,y=xx,yy
        assert not any(tr1)
        inv=pow(current,-1,prime)
        for k,r in enumerate(tr0):residues[k]+=current*(((r-residues[k])*inv)%prime)
        current*=prime
    exact=[r if r<=current//2 else r-current for r in residues]
    assert exact[:4]==[625,0,48*4*625,-48*4*625]
    assert all(abs(x)<=625*48**k for k,x in enumerate(exact))
    return {'twist':kind,'degree':degree,'trace_2H_powers':[str(x)for x in exact],
        'CRT_primes':primes,'CRT_modulus':str(current),'unique_reconstruction_bound':str(bound),
        'seconds':time.monotonic()-start,'all_zeta_trace_coefficients_zero':True}

def run():
    records=[acquire(k)for k in ['P','C']]
    result={'status':'EXACT_ALL_STATE_A4_TWISTED_FOUR_SITE_TRACE_MOMENTS','records':records}
    (ROOT/'data/twisted4_moments_exact_degree192.json').write_text(json.dumps(result,indent=2))
    print([(r['twist'],r['seconds'])for r in records]);return result

if __name__=='__main__':run()
