# Exact rational checks for conservative published confidence margins.
from fractions import Fraction as F
import numpy as np,json
from pathlib import Path
p=Path('producer-workspace/sharpened_frame_confidence_20261029');r=Path(__file__).parent
f=lambda x:F(float(x))
def mat(A):return [[f(x) for x in row] for row in A]
def trans(A):return list(map(list,zip(*A)))
def mul(A,B):return [[sum((x*y for x,y in zip(a,b)),F(0)) for b in trans(B)] for a in A]
def rownorm(A):return max(sum(map(abs,row)) for row in A)
e=F(115,1000);ell=F(7314,1000);m=10**6
assert m*e*e/(2*(900+31*e))>=ell
# exp(ell)>1500 follows already from this finite positive Taylor sum.
term=F(1);total=term
for j in range(1,61):term*=ell/j;total+=term
assert total>1500
sqlo=F('1.7320508075688772');sqhi=F('1.7320508075688774');assert sqlo**2<3<sqhi**2
bank=np.load(p/'actual_bank_counters.npz');rows=[]
assert set(np.unique(bank['Jembed'])).issubset({0.,1.})
for edge,S in enumerate(bank['sums']):
 assert np.array_equal(S,np.rint(S))
 M=S/m-bank['Jembed'];_,sv,Vt=np.linalg.svd(M);Q=mat(Vt.T)
 # M entries are exact acquired integer sums / m minus exact embed entries.
 A=[[F(int(S[i,j]),m)-f(bank['Jembed'][i,j]) for j in range(9)] for i in range(16)]
 B=mul(trans(A),A);G=mul(trans(Q),Q);C=mul(mul(trans(Q),B),Q)
 lam=[f(s*s) for s in sv]
 for i in range(9):G[i][i]-=1;C[i][i]-=lam[i]
 gd=rownorm(G);err=rownorm(C);assert gd<F(1,10**12) and err<F(1,10**12)
 assert lam[-1]>err and (lam[-1]+err)/(1-gd)<e*e
 lower_s2=[F('0.3372'),F('0.3508'),F('0.3441')][edge]
 assert (lam[-2]-err)/(1+gd)>=lower_s2**2
 # The final approximate eigenvector is within 1e-8 of some exact minimum
 # singular vector: exact rational residual plus eigenvalue separation.
 q=[Q[i][-1] for i in range(9)];norm2=sum(x*x for x in q)
 residual=[sum(B[i][j]*q[j] for j in range(9))-lam[-1]*q[i] for i in range(9)]
 assert abs(norm2-1)<F(1,10**12)
 assert sum(x*x for x in residual)<F(1,10**24)
 assert lower_s2**2-lam[-1]>F(1,10)
 # approximate polar rotation returned by NumPy, checked rationally below
 AA=np.sqrt(3)*Vt[-1].reshape(3,3);cand=[]
 for sign in [1,-1]:
  U,s,V=np.linalg.svd(sign*AA);R=U@np.diag([1,1,np.linalg.det(U@V)])@V
  cand.append((np.linalg.norm(R-sign*AA),sign,R))
 _,sign,R=min(cand,key=lambda z:z[0]);RR=mat(R);GG=mul(trans(RR),RR)
 for i in range(3):GG[i][i]-=1
 assert rownorm(GG)<F(1,10**12)
 det=RR[0][0]*(RR[1][1]*RR[2][2]-RR[1][2]*RR[2][1])-RR[0][1]*(RR[1][0]*RR[2][2]-RR[1][2]*RR[2][0])+RR[0][2]*(RR[1][0]*RR[2][1]-RR[1][1]*RR[2][0]);assert det>0
 # Hence the exact proper polar rotation of rational RR is <1e-10 away.
 inner=sum(RR[i][j]*sign*q[3*i+j] for i in range(3) for j in range(3));rn=sum(x*x for row in RR for x in row)
 crossroot=sqlo if inner>=0 else sqhi
 dist2_upper=rn+3*norm2-2*crossroot*inner
 rc=F('0.0600');assert dist2_upper<(rc-F(1,10**10))**2
 # Cone using s1>=0: sin(angle)<=e/s2. Verify h<0.35 via exact squaring.
 h=F('0.35');alpha=e/lower_s2
 assert 1-alpha*alpha>(1-h*h/2)**2
 # Frame bound < .0600+sqrt(3)*.35 +1e-7 < .667.
 frame=rc+sqhi*h+F(1,10**7);assert frame<F('0.667')
 # Opposite-sign distance >=2-rc > cone radius plus eigenvector error.
 assert 2-rc>sqhi*h+F(1,10**7)
 rows.append({'edge':edge+1,'exact_s2_lower':str(lower_s2),'exact_gap_lower':str(lower_s2-e),'exact_frame_bound_upper':'667/1000','unique_rotation_sign':sign,'gram_defect_upper':float(gd),'diagonalization_residual_upper':float(err)})
out={'all_exact_rational_checks_passed':True,'endpoint':m,'delta_upper':'1/20','operator_radius_upper':'23/200','frame_bound_upper':'667/1000','scope':'Conservative margin certificate; no true frame/occupation/bath input. Exact rational arithmetic checks scalar tail, matrix diagonalization, singular-vector residual and proper-rotation proximity.','edges':rows}
(r/'rational_margin.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
