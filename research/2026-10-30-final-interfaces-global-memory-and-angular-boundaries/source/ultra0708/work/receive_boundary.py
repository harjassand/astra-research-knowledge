"""Independent literal receiver. Python stdlib, no producer imports or solvers.

Reconstructs F, d(P/T), the compatible-Hessian density, all symmetries,
the acoustic blow-up identity and every coefficient sign in a direct
matrix-Bernstein cover. Mathematical heat/Stokes steps are in PROOF.txt.
"""
from fractions import Fraction as R
from math import comb,lcm
from pathlib import Path
import json,time,os,sys

HERE=Path(os.environ.get('ASTRA_ANGULAR_CASE',Path(__file__).parent))

def add(*ps):
    q={}
    for p in ps:
        for e,c in p.items():q[e]=q.get(e,R(0))+c
    return {e:c for e,c in q.items() if c}
def scale(p,c):return {e:v*c for e,v in p.items() if v*c}
def mul(p,q):
    r={}
    for a,c in p.items():
        for b,d in q.items():
            e=tuple(x+y for x,y in zip(a,b));r[e]=r.get(e,R(0))+c*d
    return {e:c for e,c in r.items() if c}
def diff(p,i):
    out={}
    for e,c in p.items():
        if e[i]:
            f=list(e);f[i]-=1;out[tuple(f)]=c*e[i]
    return out
def var(n,i):return {tuple(int(j==i) for j in range(n)):R(1)}
def literal(rows,n):
    out={tuple(row[:n]):R(row[n],row[n+1]) for row in rows}
    assert len(out)==len(rows)
    return {e:c for e,c in out.items() if c}
def transform(p,perm,sign):
    out={}
    for e,c in p.items():
        ee=[0]*len(e)
        for i,j in enumerate(perm):ee[j]+=e[i];c*=sign[i]**e[i]
        out[tuple(ee)]=c
    return out
def contract(p):
    out={}
    for e,c in p.items():
        if e[2]:continue
        ee=(e[1],e[3]);out[ee]=out.get(ee,R(0))+c
    return {e:c for e,c in out.items() if c}
def pd(matrix):
    den=lcm(*(x.denominator for row in matrix for x in row))
    aa=[[int(x*den) for x in row] for row in matrix];last=1
    for k in range(len(aa)):
        pivot=aa[k][k]
        assert pivot>0
        for i in range(k+1,len(aa)):
            for j in range(i,len(aa)):
                val=aa[i][j]*pivot-aa[i][k]*aa[k][j]
                assert val%last==0
                aa[i][j]=aa[j][i]=val//last
        last=pivot

def bernstein_signs(mat,box):
    n=len(mat);nb=max((e[0] for row in mat for p in row for e in p),default=0)
    nd=max((e[1] for row in mat for p in row for e in p),default=0)
    lb,ub,ld,ud=box; converted={}
    for i in range(n):
        for j in range(i,n):
            power={}
            for (ib,id_),co in mat[i][j].items():
                for aa in range(ib+1):
                    for bb in range(id_+1):
                        ee=(aa,bb)
                        power[ee]=power.get(ee,R(0))+co*comb(ib,aa)*lb**(ib-aa)*(ub-lb)**aa*comb(id_,bb)*ld**(id_-bb)*(ud-ld)**bb
            converted[i,j]=power
    count=0
    for u in range(nb+1):
        for v in range(nd+1):
            coeff=[[R(0) for _ in range(n)] for _ in range(n)]
            for (i,j),power in converted.items():
                val=sum((co*R(comb(u,a),comb(nb,a))*R(comb(v,b),comb(nd,b)) for (a,b),co in power.items() if a<=u and b<=v),R(0))
                coeff[i][j]=coeff[j][i]=val
            pd(coeff);count+=1
    return count

def line_coefficients(poly,base,direction):
    ans=[R(0)]*5
    for exponent,co in poly.items():
        term=[co]
        for power,x,y in zip(exponent,base,direction):
            fac=[R(comb(power,j))*x**(power-j)*y**j for j in range(power+1)]
            new=[R(0)]*(len(term)+len(fac)-1)
            for i,u in enumerate(term):
                for j,v in enumerate(fac):new[i+j]+=u*v
            term=new
        for i,v in enumerate(term):ans[i]+=v
    return ans

def main():
    start=time.perf_counter();certificate_path=Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'literal_boundary_certificate.json'
    cert=json.loads(certificate_path.read_text())
    P=[literal(x,4) for x in cert['P']];A=[var(4,i) for i in range(4)]
    assert all(sum(e)==5 for p in P for e in p)
    T=add(*(mul(x,x) for x in A));T2=mul(T,T)
    q=add(mul(A[0],A[3]),scale(mul(A[1],A[2]),-1))
    X=add(mul(A[0],A[0]),mul(A[2],A[2]),scale(mul(A[1],A[1]),-1),scale(mul(A[3],A[3]),-1))
    beta,r=R(cert['beta']),R(cert['r'])
    F=add(T2,scale(mul(q,q),4*(r-1)),scale(mul(q,X),4*beta))
    # Exact Lie identity and the two anti-pullbacks.
    JA=[scale(A[2],-1),scale(A[3],-1),A[0],A[1]]
    JTP=[P[2],P[3],scale(P[0],-1),scale(P[1],-1)]
    for i in range(4):assert not add(*(mul(diff(P[i],j),JA[j]) for j in range(4)),JTP[i])
    signs=(1,-1,-1,1)
    for i in range(4):assert not add(scale(transform(P[i],range(4),signs),signs[i]),P[i])
    perm=(1,0,3,2)
    for i in range(4):assert not add(transform(P[perm[i]],perm,(1,1,1,1)),P[i])
    H=[[diff(diff(F,i),j) for j in range(4)] for i in range(4)]
    W=[[{} for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(i+1,4):
            W[i][j]=add(mul(T,add(diff(P[j],i),scale(diff(P[i],j),-1))),scale(add(mul(A[i],P[j]),scale(mul(A[j],P[i]),-1)),-2))
            W[j][i]=scale(W[i][j],-1)
    C=[[{} for _ in range(6)] for _ in range(6)];p1=(0,1,3,4);p2=(1,2,4,5)
    for pp in (p1,p2):
        for i in range(4):
            for j in range(4):C[pp[i]][pp[j]]=add(C[pp[i]][pp[j]],mul(T2,H[i][j]))
    for i in range(4):
        for j in range(4):
            a,b=p1[i],p2[j];term=scale(W[i][j],R(1,2))
            C[a][b]=add(C[a][b],term);C[b][a]=add(C[b][a],term)
    C=[[contract(p) for p in row] for row in C]
    saved=[[literal(x,2) for x in row] for row in cert['matrices']['C']['entries']]
    assert C==saved
    M=[[literal(x,2) for x in row] for row in cert['matrices']['M']['entries']]
    assert C==[list(row) for row in zip(*C)] and M==[list(row) for row in zip(*M)]
    kk=[literal(x,2) for x in cert['kernel']];assert kk[0]=={(0,0):R(1)}
    w=literal(cert['w'],2);g=literal(cert['g'],2)
    cp00=add(*(mul(mul(kk[i],C[i][j]),kk[j]) for i in range(6) for j in range(6)))
    rhs=add(mul(mul(w,w),M[0][0]),scale(mul(mul(w,g),M[0][1]),2),mul(mul(g,g),M[1][1]))
    assert cp00==rhs
    for j in range(1,6):
        assert add(*(mul(kk[i],C[i][j]) for i in range(6)))==add(mul(w,M[0][j+1]),mul(g,M[1][j+1]))
        for i in range(1,6):assert C[i][j]==M[i+1][j+1]
    cover=cert['cover'];local=tuple(map(R,cover['local_box']))
    coeff_count=bernstein_signs(M,local);boxes=[];area=R(0)
    for leaf in cover['leaves']:
        box=tuple(map(R,leaf['box']));a,b,c,d=box
        assert 0<=a<b<=1 and -1<=c<d<=1
        for aa,bb,cc,dd in boxes:assert min(b,bb)<=max(a,aa) or min(d,dd)<=max(c,cc)
        boxes.append(box);area+=(b-a)*(d-c)
        if leaf['proof']=='M':assert a>=local[0] and b<=local[1] and c>=local[2] and d<=local[3]
        else:
            assert leaf['proof']=='C';coeff_count+=bernstein_signs(C,box)
    assert area==2
    nonpc=None
    if 'nonpc' in cert:
        cuts=cert['nonpc'];base=list(map(R,cuts['A']));bounds=[]
        for key in ('Rplus','Rminus'):
            rr=list(map(R,cuts[key]));det=rr[0]*rr[3]-rr[1]*rr[2]
            assert det>0 if key=='Rplus' else det<0
            c0,c1,c2,_,_=line_coefficients(F,rr,base)
            assert c0>0
            bounds.append((c2-c1*c1/(4*c0))/det)
        assert bounds[1]>bounds[0]
        nonpc={'upper':str(bounds[0]),'lower':str(bounds[1]),'strict_gap':str(bounds[1]-bounds[0])}
    out={'literal_primitive_terms':sum(len(p) for p in P),'density_rebuilt':True,
         'symmetries_exact':True,'blowup_identity_exact':True,'cover_boxes':len(boxes),
         'positive_coefficient_matrices':coeff_count,'all_signs_exact':True,
         'nonpc_cuts':nonpc,
         'seconds':time.perf_counter()-start,
         'scope':'Internal exact replay of the literal mathematical certificate; no external review or general Morrey claim.'}
    if len(sys.argv)==1:(HERE/'literal_replay.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
