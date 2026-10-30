"""Exact rational matrix-Bernstein cover. Stdlib only for proof verification.

All accepted boxes pass integer Sylvester/Bareiss tests on EVERY matrix
Bernstein coefficient. Subdivision is exact de Casteljau at one half.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb,lcm,gcd
import json,time,os

HERE=Path(os.environ.get('ASTRA_ANGULAR_CASE',Path(__file__).parent))

def positive(mat):
    a=[list(row) for row in mat]; n=len(a); prev=1
    for k in range(n):
        pivot=a[k][k]
        if pivot<=0:return False
        if k==n-1:return True
        for i in range(k+1,n):
            for j in range(i,n):
                val=a[i][j]*pivot-a[i][k]*a[k][j]
                assert val%prev==0
                a[i][j]=a[j][i]=val//prev
        prev=pivot
    return True

def bernstein(data,box):
    n=data['size']; nb,nd=data['degrees']; lo,hi,ld,hd=map(F,box)
    powers={}
    for i in range(n):
        for j in range(i,n):
            power={}
            for ib,id_,num,den in data['entries'][i][j]:
                co=F(num,den)
                for aa in range(ib+1):
                    for bb in range(id_+1):
                        key=(aa,bb)
                        power[key]=power.get(key,F(0))+co*comb(ib,aa)*lo**(ib-aa)*(hi-lo)**aa*comb(id_,bb)*ld**(id_-bb)*(hd-ld)**bb
            powers[i,j]=power
    out=[]
    for u in range(nb+1):
        row=[]
        for v in range(nd+1):
            mat=[[F(0) for j in range(n)] for i in range(n)]
            for (i,j),power in powers.items():
                val=sum((cc*F(comb(u,aa),comb(nb,aa))*F(comb(v,bb),comb(nd,bb)) for (aa,bb),cc in power.items() if aa<=u and bb<=v),F(0))
                mat[i][j]=mat[j][i]=val
            row.append(mat)
        out.append(row)
    den=lcm(*(x.denominator for row in out for mat in row for rr in mat for x in rr))
    return [[[[int(x*den) for x in rr] for rr in mat] for mat in row] for row in out]

def good(net):
    return all(positive(mat) for row in net for mat in row)

def split(net,axis):
    if axis==1:
        trans=[list(x) for x in zip(*net)]
        a,b=split(trans,0)
        return [list(x) for x in zip(*a)],[list(x) for x in zip(*b)]
    degree=len(net)-1; m=len(net[0]); n=len(net[0][0]); left=[];right=[]
    for k in range(degree+1):
        lrow=[];rrow=[]
        for j in range(m):
            lmat=[[2**(degree-k)*sum(comb(k,i)*net[i][j][s][t] for i in range(k+1)) for t in range(n)] for s in range(n)]
            rmat=[[2**k*sum(comb(degree-k,i-k)*net[i][j][s][t] for i in range(k,degree+1)) for t in range(n)] for s in range(n)]
            lrow.append(lmat);rrow.append(rmat)
        left.append(lrow);right.append(rrow)
    for part in (left,right):
        gg=0
        for row in part:
            for mat in row:
                for rr in mat:
                    for x in rr:gg=gcd(gg,x)
        if gg>1:
            for row in part:
                for mat in row:
                    for rr in mat:
                        for j in range(len(rr)):rr[j]//=gg
    return left,right

def inside(box,small):
    return box[0]>=small[0] and box[1]<=small[1] and box[2]>=small[2] and box[3]<=small[3]

def main():
    start=time.perf_counter(); data=json.loads((HERE/'polynomial_matrices.json').read_text())
    # This is a rational center locator only; no floating point sign is used.
    cfg=json.loads((HERE/'case_config.json').read_text()) if (HERE/'case_config.json').exists() else {}
    bc=F(cfg.get('center_b','2280646102/10000000000'));dc=F(cfg.get('center_d','6756989713/10000000000'))
    local=None
    for k in range(3,18):
        den=2**k; lb=(bc*den).__floor__();ld=(dc*den).__floor__()
        box=(F(lb,den),F(lb+1,den),F(ld,den),F(ld+1,den))
        net=bernstein(data['M'],box)
        ok=good(net)
        print('local depth',k,'positive',ok,flush=True)
        if ok:local=box;break
    if local is None:raise ValueError('Local certificate not found')
    root=(F(0),F(1),F(-1),F(1)); net=bernstein(data['C'],root)
    todo=[(root,net,0)]; leaves=[]; maxdepth=0; examined=0
    while todo:
        box,net,depth=todo.pop();examined+=1;maxdepth=max(depth,maxdepth)
        if inside(box,local):
            leaves.append({'box':list(map(str,box)),'proof':'M'});continue
        if good(net):
            leaves.append({'box':list(map(str,box)),'proof':'C'});continue
        if depth>=34:raise ValueError('Unresolved box '+str(box))
        axis=0 if box[1]-box[0]>=box[3]-box[2] else 1
        lnet,rnet=split(net,axis);mid=(box[2*axis]+box[2*axis+1])/2
        lbox=list(box);rbox=list(box);lbox[2*axis+1]=mid;rbox[2*axis]=mid
        todo.append((tuple(rbox),rnet,depth+1));todo.append((tuple(lbox),lnet,depth+1))
        if examined%100==0:print('examined',examined,'leaves',len(leaves),'depth',maxdepth,'seconds',time.perf_counter()-start,flush=True)
    area=sum((F(x['box'][1])-F(x['box'][0]))*(F(x['box'][3])-F(x['box'][2])) for x in leaves)
    assert area==2
    out={'local_box':list(map(str,local)),'leaves':leaves,'leaf_count':len(leaves),'max_depth':maxdepth,
         'examined':examined,'seconds':time.perf_counter()-start,'area':str(area),
         'scope':'Exact coefficient-matrix positive definiteness; covers the complete square. Polynomial identities are verified separately.'}
    (HERE/'bernstein_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='leaves'},indent=2),flush=True)

if __name__=='__main__':main()
