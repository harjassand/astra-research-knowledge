"""Independent full-spin1 anisotropic certificate; candidate not exposed."""
from sympy import symbols, Matrix, Rational as R, sqrt, Poly, expand, simplify, factor, eye
from itertools import product
import json
from pathlib import Path
h1,h2,h3=symbols('h1 h2 h3',real=True)
z1,z2,z3=symbols('z1 z2 z3',real=True)
u,v,w=symbols('u v w',nonnegative=True)
h=[h1,h2,h3];z=[z1,z2,z3]
weights=[x*x for x in h]
q=[sum(weights)-weights[i]+z[i]**2 for i in range(3)]
# Complete color-parity and BC-swap decomposition, derived directly below.
blocks=[]
for i in range(3):
    j,k=[x for x in range(3) if x!=i]
    qi,qj,qk=q[i],q[j],q[k];wi,wj,wk=weights[i],weights[j],weights[k]
    sym=Matrix([[qi,0,-sqrt(2)*wk,0,-sqrt(2)*wj],
                [0,(3*qi+2*qj)/5,sqrt(2)*wk,0,0],
                [-sqrt(2)*wk,sqrt(2)*wk,(qi+4*qj)/5,0,-wi],
                [0,0,0,(3*qi+2*qk)/5,sqrt(2)*wj],
                [-sqrt(2)*wj,0,-wi,sqrt(2)*wj,(qi+4*qk)/5]])
    anti=Matrix([[(qi+4*qj)/5,-wi],[-wi,(qi+4*qk)/5]])
    blocks.extend([(f'odd_color{i+1}_sym',sym),(f'odd_color{i+1}_anti',anti)])
di=[(3*q[i]+q[(i+1)%3]+q[(i+2)%3])/5 for i in range(3)]
for sign in [1,-1]:
    B=Matrix.diag(*di)
    for i in range(3):
        for j in range(i+1,3):
            k=3-i-j; B[i,j]=B[j,i]=sign*weights[k]
    blocks.append((f'color123_{"sym" if sign>0 else "anti"}',B))
assert sum(B.rows for _,B in blocks)==27

# Validate every block against an independently constructed 27x27 vector-
# representation operator and explicit orthonormal column embeddings.
I3=eye(3); ii=sqrt(-1)
J=[Matrix([[0,0,0],[0,0,-ii],[0,ii,0]]),Matrix([[0,0,ii],[0,0,0],[-ii,0,0]]),Matrix([[0,-ii,0],[ii,0,0],[0,0,0]])]
from sympy import kronecker_product as kron
Q=Matrix.diag(*q)
D=(3*kron(Q,I3,I3)+kron(I3,Q,I3)+kron(I3,I3,Q))/5
D+=sum((weights[i]*(kron(J[i],J[i],I3)+kron(J[i],I3,J[i])) for i in range(3)),Matrix.zeros(27))
bs=list(product(range(3),repeat=3));idx={st:i for i,st in enumerate(bs)}
def vector(st):
    V=Matrix.zeros(27,1);V[idx[st]]=1;return V
Slist=[]
for i in range(3):
    j,k=[x for x in range(3) if x!=i]
    vecs=[vector((i,i,i))]
    for a in [j,k]:
        vecs.extend([vector((i,a,a)),(vector((a,i,a))+vector((a,a,i)))/sqrt(2)])
    Slist.append(Matrix.hstack(*vecs))
    Slist.append(Matrix.hstack(*[(vector((a,i,a))-vector((a,a,i)))/sqrt(2) for a in [j,k]]))
Slist.append(Matrix.hstack(*[(vector((i,(i+1)%3,(i+2)%3))+vector((i,(i+2)%3,(i+1)%3)))/sqrt(2) for i in range(3)]))
Slist.append(Matrix.hstack(*[(vector((i,(i+1)%3,(i+2)%3))-vector((i,(i+2)%3,(i+1)%3)))/sqrt(2) for i in range(3)]))
S=Matrix.hstack(*Slist)
assert simplify(S.T*S)==eye(27)
for (name,B),SB in zip(blocks,Slist):
    assert simplify(SB.T*D*SB-B)==Matrix.zeros(B.rows),name
for a in range(len(Slist)):
    for b in range(a+1,len(Slist)):
        assert simplify(Slist[a].T*D*Slist[b])==Matrix.zeros(Slist[a].cols,Slist[b].cols)
print('PASS: complete 27dim orthonormal eight-block color-parity/swap decomposition.',flush=True)

# Four CLOSED simplicial cones cover sorted h1>=h2>=h3>=0.
cones={
 'A':([u+2*v+2*w,v+w,w],lambda H:[0,H[0],H[0]]),
 'B1':([u+2*v+2*w,u+v+w,w],lambda H:[R(2,3)*(2*H[1]-H[0]),R(2,3)*(2*H[0]-H[1]),R(2,3)*(H[0]+H[1])]),
 'B2':([u+3*v+2*w,u+3*v+w,2*v+w],lambda H:[R(2,3)*(2*H[1]-H[0]),R(2,3)*(2*H[0]-H[1]),R(2,3)*(H[0]+H[1])]),
 'C':([u+3*v+2*w,u+3*v+w,u+2*v+w],lambda H:[sum(H)-2*x for x in H]),
}
result=[]
for cone,(H,zfunc) in cones.items():
    Z=zfunc(H);sub=dict(zip(h,H));sub.update(zip(z,Z))
    for name,B in blocks:
        C=B.subs(sub,simultaneous=True).applyfunc(expand)
        for k in range(1,B.rows+1):
            determinant=expand(C[:k,:k].det(method='domain-ge'))
            p=Poly(determinant,u,v,w)
            coeffs=p.coeffs()
            if not coeffs or not all(c.is_nonnegative is True for c in coeffs):
                print('FAIL',cone,name,k,'negative coeffs',[(m,str(c)) for m,c in p.terms() if c.is_nonnegative is not True],flush=True)
                raise AssertionError('negative coefficient or identically-zero interior leading minor')
            assert any(c.is_positive is True for c in coeffs)
            result.append({'cone':cone,'block':name,'leading_size':k,'degree':p.total_degree(),'terms':[[list(m),str(c)] for m,c in p.terms()]})
    print('PASS cone',cone,'27 leading-minor polynomials with nonnegative coefficients; each nonzero, hence strictly positive for u,v,w>0.',flush=True)
Path(__file__).with_name('FULL_WEIGHTS_EXACT_COEFFICIENTS.json').write_text(json.dumps({'schema_version':1,'proof_basis':'exact determinant polynomial identities; Sylvester interior, closure continuity','cones':{key:[str(x) for x in val[0]] for key,val in cones.items()},'certificate':result},indent=2)+'\n')
print('FULL ALL-WEIGHTS SPIN1 DCORR THEOREM PASS: all 108 leading-minor polynomial identities exact.',flush=True)
