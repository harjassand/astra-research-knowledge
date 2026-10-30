"""Exact unrestricted polyconvexity certificate for the supplied B0 quartic.

Standard library only. Rebuilds the global supporting-plane matrix from F,
checks its actual acoustic lift, verifies every rational Bernstein coefficient
by integer Bareiss elimination, and checks the full canonical cover.
"""
from fractions import Fraction as R
from pathlib import Path
from math import comb,lcm
import json,time

HERE=Path(__file__).resolve().parent;start=time.perf_counter()
cert=json.loads((HERE/'b0_pc_certificate.json').read_text())

def add(*ps):
    out={}
    for pp in ps:
        for e,co in pp.items():out[e]=out.get(e,R(0))+co
    return {e:co for e,co in out.items() if co}
def scale(pp,co):return {e:co*x for e,x in pp.items() if co*x}
def mul(pp,qq):
    out={}
    for e,co in pp.items():
        for ee,cc in qq.items():
            key=tuple(a+b for a,b in zip(e,ee));out[key]=out.get(key,R(0))+co*cc
    return {e:co for e,co in out.items() if co}
def diff(pp,i):
    out={}
    for e,co in pp.items():
        if e[i]:
            ee=list(e);ee[i]-=1;out[tuple(ee)]=co*e[i]
    return out
def var(n,i):return {tuple(int(j==i) for j in range(n)):R(1)}
def literal(rows):return {tuple(row[:2]):R(row[2],row[3]) for row in rows if row[2]}
def contract(pp):
    out={}
    for e,co in pp.items():
        if not e[2]:
            ee=(e[1],e[3]);out[ee]=out.get(ee,R(0))+co
    return {e:co for e,co in out.items() if co}
def evaluate(pp,x):return sum((co*__import__('math').prod(xx**ee for xx,ee in zip(x,e)) for e,co in pp.items()),R(0))
def transform(pp,perm,sign):
    out={}
    for e,co in pp.items():
        ee=[0]*len(e)
        for i,j in enumerate(perm):ee[j]+=e[i];co*=sign[i]**e[i]
        key=tuple(ee);out[key]=out.get(key,R(0))+co
    return {e:co for e,co in out.items() if co}

AA=[var(4,i) for i in range(4)]
T=add(*(mul(x,x) for x in AA))
q=add(mul(AA[0],AA[3]),scale(mul(AA[1],AA[2]),-1))
X=add(mul(AA[0],AA[0]),mul(AA[2],AA[2]),scale(mul(AA[1],AA[1]),-1),scale(mul(AA[3],AA[3]),-1))
F=add(mul(T,T),scale(mul(q,q),R(60,13)),scale(mul(q,X),R(44,13)))
L=R(cert['L']);mu=R(cert['M_lambda'])
assert L==R(23,5) and mu==R(9488,715)
lam=add(scale(X,L),scale(q,mu))
grad=[diff(F,i) for i in range(4)]
HF=[[diff(grad[i],j) for j in range(4)] for i in range(4)]
E=[[0,0,0,1],[0,0,-1,0],[0,-1,0,0],[1,0,0,0]]
B=[[L*(1 if i in (0,2) else -1)*int(i==j)+mu*R(E[i][j],2) for j in range(4)] for i in range(4)]
Cf=[[add(scale(mul(F,HF[i][j]),2),scale(mul(grad[i],grad[j]),-1),scale(mul(F,q),-4*B[i][j])) for j in range(4)] for i in range(4)]
C=[[contract(pp) for pp in row] for row in Cf]
assert C==[[literal(pp) for pp in row] for row in cert['C']]
# Full-matrix symmetries needed for the canonical representative.
JA=[scale(AA[2],-1),scale(AA[3],-1),AA[0],AA[1]]
for pp in (F,lam):assert not add(*(mul(diff(pp,i),JA[i]) for i in range(4)))
sgn=(1,-1,-1,1);perm=(1,0,3,2)
assert transform(F,range(4),sgn)==F and transform(lam,range(4),sgn)==lam
assert transform(F,perm,(1,1,1,1))==F
assert transform(lam,perm,(1,1,1,1))==scale(lam,-1)

M=[[literal(pp) for pp in row] for row in cert['M']]
k=[literal(pp) for pp in cert['kernel']]
w=literal(cert['w']);g=literal(cert['g'])
assert k[0]=={(0,0):R(1)}
assert C==[list(row) for row in zip(*C)] and M==[list(row) for row in zip(*M)]
lhs=add(*(mul(mul(k[i],C[i][j]),k[j]) for i in range(4) for j in range(4)))
rhs=add(mul(mul(w,w),M[0][0]),scale(mul(mul(w,g),M[0][1]),2),mul(mul(g,g),M[1][1]))
assert lhs==rhs
for j in range(1,4):
    assert add(*(mul(k[i],C[i][j]) for i in range(4)))==add(mul(w,M[0][j+1]),mul(g,M[1][j+1]))
    for i in range(1,4):assert C[i][j]==M[i+1][j+1]

def pd(matrix):
    den=lcm(*(x.denominator for row in matrix for x in row))
    aa=[[int(x*den) for x in row] for row in matrix];last=1
    for k in range(len(aa)):
        pivot=aa[k][k];assert pivot>0
        for i in range(k+1,len(aa)):
            for j in range(i,len(aa)):
                val=aa[i][j]*pivot-aa[i][k]*aa[k][j];assert val%last==0
                aa[i][j]=aa[j][i]=val//last
        last=pivot
    determinant=R(last,den**len(matrix))
    trace=sum((matrix[i][i] for i in range(len(matrix))),R(0))
    return determinant/trace**(len(matrix)-1)

def bernstein(mat,box):
    n=len(mat);nb=max((e[0] for row in mat for pp in row for e in pp),default=0)
    nd=max((e[1] for row in mat for pp in row for e in pp),default=0)
    lb,ub,ld,ud=box;converted={}
    for i in range(n):
        for j in range(i,n):
            power={}
            for (ib,id_),co in mat[i][j].items():
                for aa in range(ib+1):
                    for bb in range(id_+1):
                        ee=(aa,bb)
                        power[ee]=power.get(ee,R(0))+co*comb(ib,aa)*lb**(ib-aa)*(ub-lb)**aa*comb(id_,bb)*ld**(id_-bb)*(ud-ld)**bb
            converted[i,j]=power
    count=0;ell=None
    for u in range(nb+1):
        for v in range(nd+1):
            coeff=[[R(0) for _ in range(n)] for _ in range(n)]
            for (i,j),power in converted.items():
                val=sum((co*R(comb(u,aa),comb(nb,aa))*R(comb(v,bb),comb(nd,bb)) for (aa,bb),co in power.items() if aa<=u and bb<=v),R(0))
                coeff[i][j]=coeff[j][i]=val
            lower=pd(coeff);count+=1
            ell=lower if ell is None else min(ell,lower)
    return count,ell

local=tuple(map(R,cert['cover']['local_box']))
count,ell=bernstein(M,local);boxes=[];area=R(0)
for leaf in cert['cover']['leaves']:
    box=tuple(map(R,leaf['box']));a,b,c,d=box
    assert 0<=a<b<=1 and -1<=c<d<=1
    for aa,bb,cc,dd in boxes:assert min(b,bb)<=max(a,aa) or min(d,dd)<=max(c,cc)
    boxes.append(box);area+=(b-a)*(d-c)
    if leaf['proof']=='M':assert local[0]<=a<b<=local[1] and local[2]<=c<d<=local[3]
    else:
        assert leaf['proof']=='C'
        extra,lower=bernstein(C,box);count+=extra;ell=min(ell,lower)
assert area==2

# Preserve the concrete failure of the tempting simpler support rule L=4.
# This is a failure of that rule; the verified L=23/5 rule proves PC of F.
base=list(map(R,(0,10,9,0)));direction=[R(1),R(0),R(0),R(-2,5)]
Atot=[x+y for x,y in zip(base,direction)]
failed_lam=add(scale(X,R(4)),scale(q,R(1960,143)))
failure=evaluate(F,Atot)-evaluate(F,base)-sum(evaluate(grad[i],base)*direction[i] for i in range(4))-evaluate(failed_lam,base)*evaluate(q,direction)
assert failure<0

out={'polynomial':'F_(11/13,28/13)','minor_support_rule':'lambda(A)=(23/5) X(A)+(9488/715) det(A)',
     'support_matrix_rebuilt':True,'global_symmetries_exact':True,'actual_lift_identity_exact':True,
     'cover_rectangles':len(boxes),'positive_Bernstein_coefficient_matrices':count,
     'minimum_eigenvalue_exact_lower_bound':str(ell),
     'all_signs_exact':True,'unrestricted_polyconvexity':True,
     'failed_L4_rule_witness':{'base':list(map(str,base)),'increment':list(map(str,direction)),'support_gap':str(failure)},
     'seconds':time.perf_counter()-start,
     'scope':'Global supporting-plane certificate for all real matrices and arbitrary convex minor lifts. This proves B0 polyconvex; it is not merely a polynomial-lift test.'}
(HERE/'b0_pc_verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
