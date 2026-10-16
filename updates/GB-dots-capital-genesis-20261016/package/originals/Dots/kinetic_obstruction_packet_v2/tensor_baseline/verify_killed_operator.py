"""Independent specification test. Does not import/run acquired upstream code."""
import json
import numpy as np
from scipy.sparse import csr_matrix, diags, eye, kron

def verify(L, cap, threshold, edges):
    q=cap+1; ns=q**L; counts=np.arange(q)
    plus=diags(np.ones(cap),-1,shape=(q,q),format='csr'); minus=plus.T
    ident=eye(q,format='csr'); num=diags(counts,format='csr')
    birth=diags(2.676*counts*(counts-1)+108.102,format='csr')
    death=diags(.040*counts*(counts-1)*(counts-2)+37.881*counts,format='csr')
    def embed(ops):
        a=csr_matrix([[1.]])
        for i in range(L): a=kron(a,ops.get(i,ident),format='csr')
        return a
    h=csr_matrix((ns,ns))
    for i in range(L): h+=embed({i:(plus-ident)@birth+(minus-ident)@death})
    directed=[p for i,j in edges for p in ((i,j),(j,i))]
    for i,j in directed: h+=8.2207*(embed({i:minus@num,j:plus})-embed({i:num}))
    states=list(np.ndindex(*(q,)*L)); inB=np.array([max(x)<=threshold for x in states])
    g=h@diags((~inB).astype(float)); rr=[];cc=[];vv=[]
    def add(row,col,v): rr.append(row);cc.append(col);vv.append(v)
    for col,x in enumerate(states):
        if inB[col]: continue
        exits=0.
        events=[]
        for i,n in enumerate(x):
            y=list(x);y[i]+=1;events.append((y,2.676*n*(n-1)+108.102))
            if n: y=list(x);y[i]-=1;events.append((y,.040*n*(n-1)*(n-2)+37.881*n))
        for i,j in directed:
            if x[i]: y=list(x);y[i]-=1;y[j]+=1;events.append((y,8.2207*x[i]))
        for y,rate in events:
            exits+=rate
            if max(y)<=cap: add(np.ravel_multi_index(tuple(y),(q,)*L),col,rate)
        add(col,col,-exits)
    direct=csr_matrix((vv,(rr,cc)),shape=(ns,ns)); delta=g-direct
    err=float(np.max(np.abs(delta.data))) if delta.nnz else 0.
    sums=np.asarray(g.sum(axis=0)).ravel()
    assert err<1e-10 and sums.max()<1e-10
    assert g[:,inB].nnz==0
    return dict(sites=L,cap=cap,target_threshold=threshold,states=ns,max_entry_error=err,
                max_column_sum=float(sums.max()),min_column_sum=float(sums.min()),
                target_columns_zero=True,backward_target_rows_zero=True)

edges=[(0,1),(1,2),(2,3),(4,5),(5,6),(6,7),(0,4),(1,5),(2,6),(3,7)]
order=[0,4,1,5,2,6,3,7]
crossings=[]
for k in range(1,8):
    left=set(order[:k]); crossings.append(sum((i in left)!=(j in left) for i,j in edges))
print(json.dumps(dict(upstream_executed=False,tests=[verify(8,1,0,edges),verify(2,4,1,[(0,1)])],
                     site_order=order,crossing_edges=crossings,
                     conservative_H_bonds=[2+2*c for c in crossings],
                     conservative_frozen_G_bonds=[2*(2+2*c) for c in crossings]),indent=2))
