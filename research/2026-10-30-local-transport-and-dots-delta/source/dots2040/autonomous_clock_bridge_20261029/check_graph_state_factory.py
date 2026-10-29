"""Exact rational two-site graph-state/controller interface regression."""
import sympy as s,json,hashlib
from pathlib import Path
P=Path(__file__);I=s.eye;Z=s.diag(1,-1);X=s.Matrix([[0,1],[1,0]]);k=s.kronecker_product
D=4;A=9;n=36
stab=[k(X,Z),k(Z,X)]
def e(a,b):
 m=s.zeros(3);m[a,b]=1;return m
def ac(x,m):return k(m,I(3)) if x==0 else k(I(3),m)
def full(data,aux):return k(data,aux)
U=[];V=[];K=[];H=s.zeros(n);jumps=[]
for x,S in enumerate(stab):
 pp=(I(D)+S)/2;pm=(I(D)-S)/2;zx=k(Z,I(2)) if x==0 else k(I(2),Z)
 kk=[pp,zx*pm];K.append(kk)
 # own ready identity; excited block unitary [[P+,P-],[ZP-,-ZP+]]
 local=full(I(D),ac(x,e(0,0)))+full(pp,ac(x,e(1,1)))+full(pm,ac(x,e(1,2)))+full(zx*pm,ac(x,e(2,1)))-full(zx*pp,ac(x,e(2,2)))
 guard=full(I(D),ac(1-x,e(0,0)));ux=local*guard+(I(n)-guard);U.append(ux)
 vx=sum((full(kk[r],ac(x,e(r+1,0))) for r in range(2)),s.zeros(n));V.append(vx)
 H+=(vx+vx.T)*guard
 jumps +=[full(I(D),ac(x,e(0,r+1))) for r in range(2)]
W=U[0]*U[1];no=sum((l.T*l for l in jumps),s.zeros(n))
clock_bad=[]
for x in range(2):
 q=I(3)-e(0,0);guard=ac(1-x,e(0,0));clock_bad.append(ac(x,q)-ac(x,e(1,1))*guard)
good=(I(A)-clock_bad[0])*(I(A)-clock_bad[1]);flags=[]
for S in stab:
 d=(I(D)-S)/2
 af=I(n)-full(I(D)-d,good);flags.append(W*af*W.T)
checks={'local_extensions_unitary':all(u.T*u==I(n) for u in U),'extensions_commute':U[0]*U[1]==U[1]*U[0], 'flags_commute':flags[0]*flags[1]==flags[1]*flags[0]}
hc=sum(((ac(x,e(1,0)+e(0,1))*ac(1-x,e(0,0))) for x in range(2)),s.zeros(A))
checks['full_space_clock_only_H']=W.T*H*W==full(I(D),hc)
for j,B in enumerate(flags):
 checks[f'flag{j}_H_commutes']=H*B==B*H
 checks[f'flag{j}_jump_no_creation']=all(B*l*(I(n)-B)==s.zeros(n) for l in jumps)
 drift=sum((l.T*B*l for l in jumps),s.zeros(n))-(no*B+B*no)/2
 gram=sum((B*l.T*(I(n)-B)*l*B for l in jumps),s.zeros(n))
 checks[f'flag{j}_negative_Gram_identity']=drift == -gram
 checks[f'flag{j}_no_jump_commutes']=no*B==B*no
out={'scope':'Exact two-site graph-state combined data/controller no-creation regression. No uniform factory or logical threshold inferred solely from finite test.','checks':checks,'source_sha256':hashlib.sha256(P.read_bytes()).hexdigest()}
assert all(checks.values());P.with_suffix('.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
