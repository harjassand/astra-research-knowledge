"""Root port/rational fixtures. Imports no candidate recognition or FKT code."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
BITS=list(product((0,1),repeat=3))

def transform(t,port,g):
    out=[]
    for bits in BITS:
        value=F(0)
        for j in (0,1):
            src=list(bits);src[port]=j
            value+=g[bits[port]][j]*t[4*src[0]+2*src[1]+src[2]]
        out.append(value)
    return out

def build(components=1,odd=False):
    coeffs=[(1,2,3,5),(2,3,7,11),(3,5,7,11),(2,3,5,13)]
    ts=[];edges=[]
    for v in range(2*components):
        it=iter(coeffs[v]);parity=int(odd and v==0)
        ts.append([F(next(it)) if sum(bits)%2==parity else F(0) for bits in BITS])
    for c in range(components):
        edges.extend([[2*c,0,2*c+1,0],[2*c,1,2*c+1,2],[2*c,2,2*c+1,1]])
    for eid,(v,i,w,j) in enumerate(edges):
        a,b=F(eid+1,eid+2),F(eid+2,eid+3)
        ts[v]=transform(ts[v],i,[[F(1),a],[b,1+a*b]])
        ts[w]=transform(ts[w],j,[[1+a*b,-b],[-a,F(1)]])
    ports=[[None]*3 for _ in ts]
    for k,(v,i,w,j) in enumerate(edges):ports[v][i]=k;ports[w][j]=k
    z=F(0);nums=[[F(0),F(0)] for _ in edges]
    for bits in product((0,1),repeat=len(edges)):
        term=F(1)
        for v,p in enumerate(ports):term*=ts[v][4*bits[p[0]]+2*bits[p[1]]+bits[p[2]]]
        z+=term
        for k,b in enumerate(bits):nums[k][b]+=term
    assert all(sum(row)==z for row in nums)
    return {'input':{'tensors':[[str(x) for x in t] for t in ts],'edges':edges},
      'oracle':{'exact_partition':str(z),'original_bit_numerators':[[str(x) for x in row] for row in nums],
       'normalized_original_bit_weights':None if not z else [[str(x/z) for x in row] for row in nums]},
      'scope':{'parallel_edges':True,'components':components,'one_odd_component':odd,
       'original_assignments_enumerated':1<<len(edges)}}

if __name__=='__main__':
    out=[build(c,odd) for c in (1,2) for odd in (False,True)]
    Path(__file__).with_name('PORT_FIXTURES.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps([{'scope':r['scope'],'Z':r['oracle']['exact_partition']} for r in out]))
