"""Acquire a finite Bernstein cover for the B0 global minor-support matrix.

Floating arithmetic only proposes a cover. Exact coefficient signs are
checked separately by verify_b0_pc.py before accepting polyconvexity.
"""
from pathlib import Path
from fractions import Fraction as R
from math import comb
import json,time
import numpy as np

HERE=Path(__file__).resolve().parent;start=time.time()
data=json.loads((HERE/'b0_pc_candidate.json').read_text())

def unpack(mat):return [[{(ib,id_):R(n,dd) for ib,id_,n,dd in pp} for pp in row] for row in mat]
C=unpack(data['C']);M=unpack(data['M'])

def bernstein(mat,box):
    n=len(mat);nb=max((e[0] for row in mat for pp in row for e in pp),default=0)
    nd=max((e[1] for row in mat for pp in row for e in pp),default=0)
    lb,ub,ld,ud=map(float,box)
    out=np.zeros((nb+1,nd+1,n,n))
    for i in range(n):
        for j in range(i,n):
            power={}
            for (ib,id_),co in mat[i][j].items():
                co=float(co)
                for aa in range(ib+1):
                    for bb in range(id_+1):
                        ee=(aa,bb)
                        power[ee]=power.get(ee,0)+co*comb(ib,aa)*lb**(ib-aa)*(ub-lb)**aa*comb(id_,bb)*ld**(id_-bb)*(ud-ld)**bb
            for u in range(nb+1):
                for v in range(nd+1):
                    val=sum(co*comb(u,aa)/comb(nb,aa)*comb(v,bb)/comb(nd,bb) for (aa,bb),co in power.items() if aa<=u and bb<=v)
                    out[u,v,i,j]=out[u,v,j,i]=val
    return out

def split(coeff,axis):
    cc=np.moveaxis(coeff,axis,0);n=cc.shape[0]-1
    work=cc.copy();left=[work[0].copy()];right=[work[-1].copy()]
    for _ in range(n):
        work=(work[:-1]+work[1:])/2
        left.append(work[0].copy());right.append(work[-1].copy())
    return np.moveaxis(np.stack(left),0,axis),np.moveaxis(np.stack(right[::-1]),0,axis)

local=tuple(map(R,('25/64','51/128','-1/128','1/128')))
mm=bernstein(M,local);margin=float(np.linalg.eigvalsh(mm)[:,: ,0].min())
assert margin>1e-8,margin
a,b,c,d=local
initial=[(R(0),a,R(-1),R(1)),(b,R(1),R(-1),R(1)),(a,b,R(-1),c),(a,b,d,R(1))]
stack=[(box,bernstein(C,box),0) for box in initial]
leaves=[{'box':list(map(str,local)),'proof':'M'}]
worst=1e100;maxdepth=0
while stack:
    box,coeff,depth=stack.pop()
    eig=float(np.linalg.eigvalsh(coeff)[:,:,0].min())
    if eig>1e-8:
        leaves.append({'box':list(map(str,box)),'proof':'C'});worst=min(worst,eig);continue
    assert depth<30,(box,eig)
    lb,ub,ld,ud=box
    axis=0 if (ub-lb)>=(ud-ld) else 1
    first,second=split(coeff,axis)
    if axis==0:
        mid=(lb+ub)/2;bb1=(lb,mid,ld,ud);bb2=(mid,ub,ld,ud)
    else:
        mid=(ld+ud)/2;bb1=(lb,ub,ld,mid);bb2=(lb,ub,mid,ud)
    stack.append((bb2,second,depth+1));stack.append((bb1,first,depth+1))
    maxdepth=max(maxdepth,depth+1)
    assert len(stack)+len(leaves)<10000
data['cover']={'local_box':list(map(str,local)),'leaves':leaves}
data['acquisition']={'floating_local_margin':margin,'floating_other_margin':worst,'max_depth':maxdepth,'seconds':time.time()-start}
(HERE/'b0_pc_certificate.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'cover_leaves':len(leaves),'local_lift_margin':margin,'other_margin':worst,'max_depth':maxdepth,'seconds':time.time()-start},indent=2))
