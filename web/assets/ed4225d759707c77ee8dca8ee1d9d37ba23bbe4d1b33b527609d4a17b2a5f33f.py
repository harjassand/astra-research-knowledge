"""Finite exact-coefficient diagnostics, NOT proof of the general theorem."""
from fractions import Fraction as F
from itertools import combinations, product
from math import factorial
import json
import numpy as np

def coeff(T, blocks, tables, complement=True):
    z=F(1)
    for block,b in zip(blocks,tables):
        k=len(set(T)&set(block))
        z*=b[len(block)-k if complement else k]
    return z

def all_quadratic_derivatives(blocks,tables,complement=True):
    m=sum(map(len,blocks)); largest_second=-1e99; count=0
    for degree in range(2,m+1):
        for forced in combinations(range(m),degree-2):
            rem=[i for i in range(m) if i not in forced]
            h=np.zeros((len(rem),len(rem)))
            for i,j in combinations(range(len(rem)),2):
                z=coeff((*forced,rem[i],rem[j]),blocks,tables,complement)
                h[i,j]=h[j,i]=float(z)
            eig=np.linalg.eigvalsh(h)
            largest_second=max(largest_second,float(eig[-2]))
            count+=1
    return count,largest_second

records=[]
for sizes in [(2,2),(3,3),(2,3),(2,2,2)]:
    blocks=[]; j=0
    for q in sizes: blocks.append(tuple(range(j,j+q)));j+=q
    for mode in ['factorial','repulsive','linear','zeros']:
        tables=[]
        for q in sizes:
            if mode=='factorial': b=[F(factorial(k)) for k in range(q+1)]
            elif mode=='repulsive': b=[F(1,2**(k*(k-1)//2)) for k in range(q+1)]
            elif mode=='linear': b=[F(factorial(k)*3**k,2**k) for k in range(q+1)]
            else: b=[F(factorial(k)) if 1<=k<=q-1 else F(0) for k in range(q+1)]
            tables.append(b)
        count,second=all_quadratic_derivatives(blocks,tables)
        assert second<1e-8,(sizes,mode,second)
        records.append(dict(sizes=sizes,mode=mode,quadratic_derivatives=count,max_second_eigenvalue=second))

# Sharp weak-attraction and complementary-orientation fixtures.
blocks=[(0,1),(2,3)]
for a in [F(1),F(2),F(21,10)]:
    h=np.zeros((4,4))
    for i,j in combinations(range(4),2):
        h[i,j]=h[j,i]=float(coeff((i,j),blocks,[[F(1),F(1),a]]*2))
    eig=np.linalg.eigvalsh(h)
    assert (eig[-2]>1e-8)==(a>2)
    records.append(dict(two_site_a=str(a),hessian_eigenvalues=eig.tolist()))
blocks=[(0,1,2),(3,4,5)]
tables=[[F(factorial(k)) for k in range(4)]]*2
count,second=all_quadratic_derivatives(blocks,tables,False)
assert second>0.9
records.append(dict(direct_factorial_counterexample_second_eigenvalue=second))
out={'status':'finite diagnostics passed','records':records,'diagnostics_not_general_proof':True}
with open('work/cycle3/root_filter_check.json','w') as f: json.dump(out,f,indent=2)
print(json.dumps({'status':out['status'],'cases':len(records),'quadratic_derivatives':sum(r.get('quadratic_derivatives',0) for r in records)}))
