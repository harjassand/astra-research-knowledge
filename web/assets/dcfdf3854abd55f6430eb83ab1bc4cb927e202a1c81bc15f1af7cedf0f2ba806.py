"""Exact finite-field evaluation of rank-two graph-basis Werner witnesses.
A search is not a proof for arbitrary coefficient matrices.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np


def rref3(M: np.ndarray):
    a=M.astype(np.int64).copy()%3
    m,n=a.shape;E=np.eye(m,dtype=np.int64);piv=[];r=0
    for c in range(n):
        nz=np.flatnonzero(a[r:,c])
        if len(nz)==0: continue
        i=r+int(nz[0])
        a[[r,i]]=a[[i,r]];E[[r,i]]=E[[i,r]]
        if a[r,c]==2: a[r]=(2*a[r])%3;E[r]=(2*E[r])%3
        for j in range(m):
            if j!=r and a[j,c]:
                z=int(a[j,c]);a[j]=(a[j]-z*a[r])%3;E[j]=(E[j]-z*E[r])%3
        piv.append(c);r+=1
        if r==m: break
    return a[:r],E,np.array(piv,dtype=int)


def evaluate(G: np.ndarray,delta: np.ndarray,v: np.ndarray):
    """Return scaled A and B=p+q*omega, with exact int64 sums (n<=16)."""
    n=G.shape[0]
    if n>16: raise ValueError('The exact-int64 safety bound is restricted to n<=16.')
    if delta.shape!=v.shape or delta.shape[1]!=n: raise ValueError('Incorrect label shapes')
    k=len(delta);A=np.zeros(k,dtype=np.int64);B=np.zeros((k,3),dtype=np.int64)
    allidx=np.arange(n)
    for mask in range(1<<n):
        S=np.array([i for i in range(n) if mask>>i&1],dtype=int)
        R=np.array([i for i in range(n) if not (mask>>i&1)],dtype=int)
        rr,E,piv=rref3(G[np.ix_(S,R)]);rank=len(piv)
        b=(-delta[:,S]@E.T)%3
        good_d=np.all(b[:,rank:]==0,axis=1)
        h=v[:,R]
        remainder=(h-h[:,piv]@rr)%3
        good_v=np.all(remainder==0,axis=1)
        phase=np.sum(h[:,piv]*b[:,:rank],axis=1)%3
        coeff=(-1)**len(S)*2**(n-len(S))*3**(n//2-rank)
        A += coeff*good_d
        good=good_d&good_v
        for t in range(3): B[:,t] += coeff*(good&(phase==t))
    p=B[:,0]-B[:,2];q=B[:,1]-B[:,2]
    return A,p,q,2**n*3**(n//2)


def materialized_check():
    from npt_core import endpoint
    rng=np.random.default_rng(421)
    maximum=0.
    for n in (2,3,4):
        G=rng.integers(0,3,(n,n));G=np.triu(G,1);G=(G+G.T)%3
        d=rng.integers(0,3,(6,n));v=rng.integers(0,3,(6,n));v[:,0]=1
        A,p,q,scale=evaluate(G,d,v)
        basis=np.array(list(np.ndindex(*(3,)*n)),dtype=int)
        # Q(x)=sum_{i<j} G_ij x_i x_j.
        Q=sum(G[i,j]*basis[:,i]*basis[:,j] for i in range(n) for j in range(i+1,n))%3
        omega=np.exp(2j*np.pi/3)
        def state(label): return omega**((Q+basis@label)%3)/np.sqrt(3**n)
        for j in range(6):
            X=np.outer(state(np.zeros(n,dtype=int)),state(-d[j]).conj())
            Y=np.outer(state(v[j]),state(v[j]-d[j]).conj())
            BB=(int(p[j])+int(q[j])*omega)/scale
            AA=int(A[j])/scale
            for eta in (1.,-1.,1j,np.exp(.713j)):
                actual=endpoint(X+eta*Y,(3,)*n)
                predicted=2*AA+2*np.real(eta*BB)
                maximum=max(maximum,abs(actual-predicted))
                assert abs(actual-predicted)<1e-12,(n,j,actual,predicted)
    return {'materialized_complex_comparisons':72,'max_absolute_error':maximum}


def run(n:int,graphs:int,batch:int,seed:int):
    rng=np.random.default_rng(seed);records=[];negative=[]
    for trial in range(graphs):
        if trial==0:
            G=np.zeros((n,n),dtype=int)
            for i in range(n-1):G[i,i+1]=G[i+1,i]=1
            kind='path'
        elif trial==1:
            G=np.ones((n,n),dtype=int)-np.eye(n,dtype=int);kind='complete'
        else:
            G=rng.integers(0,3,(n,n));G=np.triu(G,1);G=(G+G.T)%3;kind='random'
        delta=rng.integers(0,3,(batch,n));v=rng.integers(0,3,(batch,n))
        # Include a normal sector and a nilpotent graph-orbit chain.
        delta[:batch//5]=0
        v[batch//5:2*batch//5]=delta[batch//5:2*batch//5]
        for j in range(batch):
            if not np.any(v[j]):v[j,0]=1
        A,p,q,scale=evaluate(G,delta,v)
        assert np.all(A>=0),'Rank-one positivity control failed.'
        gaps=[]
        for j in range(batch):
            a,b,c=map(int,(A[j],p[j],q[j]));gap=a*a-(b*b-b*c+c*c)
            gaps.append(gap)
            if gap<0:
                negative.append({'graph':G.tolist(),'delta':delta[j].tolist(),'v':v[j].tolist(),
                                 'A_numerator':a,'B_p':b,'B_q':c,'denominator':scale,'gap':str(gap)})
        rec={'sites':n,'trial':trial,'kind':kind,'candidates':batch,
             'negative_certificates':sum(x<0 for x in gaps),'zero_determinants':sum(x==0 for x in gaps),
             'minimum_scaled_determinant':str(min(gaps)),'scale':scale,'graph':G.tolist()}
        records.append(rec);print(json.dumps(rec),flush=True)
    out={'status':'exact evaluation only on the stated finite graph-basis witness family',
         'seed':seed,'records':records,'negative_certificates':negative}
    Path(__file__).with_name(f'GRAPH_SEARCH_n{n}.json').write_text(json.dumps(out,indent=2)+'\n')
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=6)
    p.add_argument('--graphs',type=int,default=4);p.add_argument('--batch',type=int,default=512)
    p.add_argument('--seed',type=int,default=20261009);p.add_argument('--check',action='store_true')
    args=p.parse_args()
    if args.check:
        x=materialized_check();print(json.dumps(x))
        Path(__file__).with_name('GRAPH_FORMULA_RECEIPT.json').write_text(json.dumps(x,indent=2)+'\n')
    run(args.n,args.graphs,args.batch,args.seed+args.n)
