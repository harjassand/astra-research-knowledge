#!/usr/bin/env python3
"""Exact rank-two subtraction replay; executes only our independently written base checker prefix."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
# Reuse our own sparse Fraction polynomial code and completed base checks, but
# stop before the base receipt writer so previously delivered files are untouched.
src=(ROOT/'replay.py').read_text().split("receipt={'certificate_sha256'",1)[0]
exec(compile(src,str(ROOT/'replay.py'),'exec'),globals())
eps=F(1,2000)
v1=[F(int(i==0)-int(i==12)+int(i==16)) for i in range(18)]
v2=[F(-int(i==13)+int(i==17)) for i in range(18)]
K=[[12*D[0][0]*v1[i]*v1[j]+12*D[1][1]*v2[i]*v2[j] for j in range(18)] for i in range(18)]
Se=[[S[i][j]-eps*K[i][j] for j in range(18)] for i in range(18)]
Le=[[F(i==j) for j in range(18)] for i in range(18)];pe=[]
for k in range(18):
 p=Se[k][k]-sum(Le[k][r]**2*pe[r] for r in range(k));assert p>0;pe.append(p)
 for i in range(k+1,18):Le[i][k]=(Se[i][k]-sum(Le[i][r]*Le[k][r]*pe[r] for r in range(k)))/p
assert all(Se[i][j]==sum(Le[i][k]*pe[k]*Le[j][k] for k in range(18)) for i in range(18) for j in range(18))
def solveS(v):
 y=[]
 for i in range(18):y.append(v[i]-sum(L[i][j]*y[j] for j in range(i)))
 t=[y[i]/piv[i] for i in range(18)];x=[F(0)]*18
 for i in range(17,-1,-1):x[i]=t[i]-sum(L[j][i]*x[j] for j in range(i+1,18))
 assert all(sum(S[i][j]*x[j] for j in range(18))==v[i] for i in range(18))
 return x
iv1=solveS(v1);iv2=solveS(v2)
T0=12*(D[0][0]*sum(v1[i]*iv1[i] for i in range(18))+D[1][1]*sum(v2[i]*iv2[i] for i in range(18)))
assert 0<T0<2000
ell=[add(*(scale(Z[i],C[i][k]) for i in range(24))) for k in range(18)]
r=add(a,scale(d,-1));ss=add(b,c)
for ix,want in [(0,mul(a,z[0])),(12,mul(d,z[0])),(13,scale(mul(r,z[1]),-1)),(16,scale(mul(r,z[4]),-1)),(17,scale(mul(r,z[5]),-1))]:
 assert ell[ix]==want
assert add(*(scale(ell[i],v1[i]) for i in range(18)))==mul(r,add(z[0],scale(z[4],-1)))
assert add(*(scale(ell[i],v2[i]) for i in range(18)))==mul(r,add(z[1],scale(z[5],-1)))
def sq(p):return mul(p,p)
def fourth(p):return sq(sq(p))
r4=fourth(r)
hr=[[deriv(deriv(r4,i),j) for j in range(4)] for i in range(4)]
rheat=add(*(scale(mul(hr[i][j],mul(B[i],B[j])),w) for w,B in [(D[0][0],B1),(D[1][1],B2)] for i in range(4) for j in range(4)))
kpoly=add(*(scale(mul(ell[i],ell[j]),K[i][j]) for i in range(18) for j in range(18)))
assert rheat==kpoly
updated=add(*(scale(mul(ell[i],ell[j]),Se[i][j]) for i in range(18) for j in range(18)))
assert updated==add(heat,corr,scale(rheat,-eps))
# Exact four-angle average without irrational numbers: (r±s)/sqrt(2)
# raised to the fourth power is (r±s)^4/4.
avg=scale(add(fourth(r),fourth(ss),scale(fourth(add(r,ss)),F(1,4)),scale(fourth(add(r,scale(ss,-1))),F(1,4))),F(1,4))
assert avg==scale(sq(add(sq(r),sq(ss))),F(3,8))
kappa=eps*F(3,8);assert kappa==F(3,16000)
# Verify the quartic Bregman SOS in two-dimensional vectors x,h.
xx=[var(0),var(1)];hh=[var(2),var(3)]
x2=add(*(sq(v) for v in xx));h2=add(*(sq(v) for v in hh));xh=add(*(mul(x,y) for x,y in zip(xx,hh)))
qgap=add(sq(add(x2,scale(xh,2),h2)),scale(sq(x2),-1),scale(mul(x2,xh),-4),scale(sq(h2),F(-1,3)))
sos=add(scale(sq(add(xh,scale(h2,F(1,3)))),6),scale(add(mul(x2,h2),scale(sq(xh),-1)),2))
assert qgap==sos
normsq=2*(F(24)+1)/4;assert normsq==F(25,2)
norm4=normsq**2;assert norm4==F(625,4)
gamma=kappa/F(3)/norm4;assert gamma==F(1,2500000)
res={'all_algebra_checks_passed':True,'epsilon':str(eps),'T0':str(T0),'T0_decimal_diagnostic':float(T0),'T0_positive_and_less_than_2000':True,'positive_subtracted_LDL_pivots':[str(p) for p in pe],'subtracted_LDL_entries_checked':324,'ell_coordinate_identities_checked':5,'v_dot_ell_identities_checked':2,'rank_two_density_exact':True,'updated_heat_identity_exact':True,'four_rotation_average_exact':True,'quartic_Bregman_SOS_exact':True,'kappa':str(kappa),'L4_fourth_power_constant':str(norm4),'gamma':str(gamma),'analytic_input':'Banuelos-Janakiraman Theorem 1.1, complex-valued L4 bound sqrt(24), separately inspected in primary PDF'}
(ROOT/'coercivity_receipt.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
