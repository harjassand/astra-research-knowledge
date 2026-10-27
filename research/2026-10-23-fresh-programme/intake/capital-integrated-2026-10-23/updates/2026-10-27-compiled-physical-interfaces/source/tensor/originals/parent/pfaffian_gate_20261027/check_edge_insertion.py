"""Exact edge-insertion transport check, including Fisher prefactor."""
from fractions import Fraction as F
from itertools import combinations,product
from functools import lru_cache
from pathlib import Path
import json

def check(signed):
    edges=list(combinations(range(4),2))
    ports=[(v,w) for v in range(4) for w in range(4) if v!=w]
    idx={p:i for i,p in enumerate(ports)}
    weights={e:(F(k+2),F(k+1,k+3)) if not signed else
             (F(k+1),F(2*(k+2))) for k,e in enumerate(edges)}
    N=[[F(3),F(-5)],[F(7),F(11)]]
    target=edges[2];z=F(0);pin=F(0)
    for s in product((0,1),repeat=4):
        base=F(1);query=F(1)
        for e,(a,b) in weights.items():
            v,w=e;factor=a if s[v]==s[w] else b
            base*=factor;query*=N[s[v]][s[w]] if e==target else factor
        z+=base;pin+=query
    W=[[F(0) for _ in ports] for _ in ports]
    for v in range(4):
        for w,u in combinations([j for j in range(4) if j!=v],2):
            i,j=idx[v,w],idx[v,u];W[i][j]=W[j][i]=1
    for (v,w),(a,b) in weights.items():
        i,j=idx[v,w],idx[w,v];W[i][j]=W[j][i]=(a+b)/(a-b)
    @lru_cache(None)
    def dimer(mask):
        if not mask:return F(1)
        i=(mask&-mask).bit_length()-1;rest=mask^(1<<i)
        return sum(W[i][j]*dimer(rest^(1<<j)) for j in range(i+1,len(ports))
                   if rest>>j&1 and W[i][j])
    full=(1<<len(ports))-1;v,w=target;i,j=idx[v,w],idx[w,v]
    h=W[i][j]*dimer(full^(1<<i)^(1<<j))/dimer(full)
    a,b=weights[target];A=(N[0][0]+N[1][1])/2;B=(N[0][1]+N[1][0])/2
    recovered=((A+B)/(a+b))*h+((A-B)/(a-b))*(1-h)
    assert recovered==pin/z
    return {'signed_weights':signed,'partition':str(z),'insertion':str(pin),
            'dimer_external_weight':str(h),'exact_original_ratio':str(pin/z),
            'transported_ratio':str(recovered),'status':'PASS'}

if __name__=='__main__':
    result=[check(False),check(True)]
    Path(__file__).with_name('EDGE_INSERTION_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
