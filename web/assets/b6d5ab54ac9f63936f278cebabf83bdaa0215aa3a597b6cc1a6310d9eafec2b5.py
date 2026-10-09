"""Independent direct character enumeration, with integer counts, for small graphs."""
from pathlib import Path
import json
import numpy as np
from mixed_graph_search import evaluate
from graph_code_search import evaluate as same_graph_evaluate

rng=np.random.default_rng(2026100907)
records=[]
for n in (1,2,3,4):
    G=np.triu(rng.integers(0,3,(n,n)),1);G=G+G.T
    H=np.triu(rng.integers(0,3,(n,n)),1);H=H+H.T
    delta=rng.integers(0,3,(4,n));v=rng.integers(0,3,(4,n));w=rng.integers(0,3,(4,n))
    v[:,0]=w[:,0]=1
    a,b,p,q,L=evaluate(G,H,delta,v,w)
    grid=np.array(list(np.ndindex(*(3,)*(2*n))),dtype=np.int64);x=grid[:,:n];y=grid[:,n:]
    def Q(K,z):return np.sum((z@np.triu(K,1))*z,axis=1)%3
    sums=np.zeros((3,4,2),dtype=np.int64)
    for mask in range(1<<n):
        S=[i for i in range(n) if mask>>i&1]
        xx=x.copy();yy=y.copy();xx[:,S]=y[:,S];yy[:,S]=x[:,S]
        base=(Q(G,xx)+Q(H,yy)-Q(G,x)-Q(H,y))%3
        for j in range(4):
            # Explicit ket minus bra linear phases; no Gaussian elimination used.
            phases=(base+(-yy@delta[j])-(-y@delta[j]),
                    base+xx@v[j]+yy@(w[j]-delta[j])-x@v[j]-y@(w[j]-delta[j]),
                    base+xx@v[j]-yy@delta[j]-y@(w[j]-delta[j]))
            for k,phase in enumerate(phases):
                counts=np.bincount(phase%3,minlength=3)
                sums[k,j]+=((-1)**len(S)*2**(n-len(S)))*np.array([counts[0]-counts[2],counts[1]-counts[2]])
    expected=np.zeros_like(sums);expected[0,:,0]=a;expected[1,:,0]=b;expected[2,:,0]=p;expected[2,:,1]=q
    assert np.array_equal(sums,3**n*expected),(n,sums,expected)
    records.append({'sites':n,'label_triples':4,'complex_entries_checked':12,'status':'exact equality'})

agreement=[]
for n in (2,4,6):
    G=np.triu(rng.integers(0,3,(n,n)),1);G=G+G.T
    d=rng.integers(0,3,(8,n));v=rng.integers(0,3,(8,n));v[:,0]=1
    a,b,p,q,L=evaluate(G,G,d,v,v)
    a0,p0,q0,L0=same_graph_evaluate(G,d,v)
    ratio=L//L0
    assert L==L0*ratio
    assert np.array_equal(a,ratio*a0) and np.array_equal(b,ratio*a0)
    assert np.array_equal(p,ratio*p0) and np.array_equal(q,ratio*q0)
    agreement.append({'sites':n,'label_pairs':8,'status':'exact agreement of independent formulas'})
# Singular and indefinite finite-field forms are included in these tests.
out={'status':'exact finite consistency checks, not proof-assistant certification',
     'direct_character_enumeration':records,'same_graph_formula_agreement':agreement,
     'negative_control_status':'negative rank-three Werner control lives in IDENTITY_RECEIPT.json'}
Path(__file__).with_name('GRAPH_EXACT_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
