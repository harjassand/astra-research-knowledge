import sympy as s,json
from pathlib import Path
Q=s.Rational;I=s.eye(2)
T=s.Matrix([[Q(1,2),Q(1,6),Q(1,3)],[Q(1,3),Q(1,2),Q(1,6)],[Q(1,6),Q(1,3),Q(1,2)]])
p=[Q(1,3)]*3;u=s.ones(3,1)*Q(3,11);c=Q(2,11)
assert all(sum(T[:,i])==1 for i in range(3))
assert all(s.factor(sum((T[y,i]-u[y])**2/T[y,i] for y in range(3)))==c for i in range(3))
assert 1-sum(1/sum(p[i]/T[y,i] for i in range(3)) for y in range(3))==c
v=[s.Matrix([1,0]),s.Matrix([-Q(1,2),s.sqrt(3)/2]),s.Matrix([-Q(1,2),-s.sqrt(3)/2])]
R=[Q(2,3)*x*x.T for x in v];h=[1,-1,0];H=[hi*ri for hi,ri in zip(h,R)];K=sum(H,s.zeros(2))
E=s.factor(sum(hi**2*s.trace(ri) for hi,ri in zip(h,R))-s.trace(K*K))
A=[sum((T[y,i]*R[i] for i in range(3)),s.zeros(2)) for y in range(3)]
J=[sum((T[y,i]*H[i] for i in range(3)),s.zeros(2)) for y in range(3)]
N=s.factor(sum(s.trace(j*a.inv()*j) for j,a in zip(J,A))-s.trace(K*K))
assert N/E==c
# Nonuniform rational square-root prior, using rational orthonormal coordinates.
root=s.Matrix([Q(1,3),Q(2,3),Q(2,3)]);pp=[x*x for x in root];w=s.Matrix([0,0,1])-root
House=s.eye(3)-2*w*w.T/(w.T*w)[0];V=House[:,:2].T
assert V*V.T==I and V*root==s.zeros(2,1)
vv=[V[:,i] for i in range(3)];RR=[x*x.T for x in vv];zz=[root[i]*vv[i] for i in range(3)]
assert sum(RR,s.zeros(2))==I and sum(zz,s.zeros(2,1))==s.zeros(2,1)
num=0
for y in range(3):
 aa=sum((T[y,i]*RR[i] for i in range(3)),s.zeros(2));bb=sum((T[y,i]*zz[i] for i in range(3)),s.zeros(2,1))
 value=(bb.T*aa.inv()*bb)[0]
 assert value==sum(pp[i]*T[y,i] for i in range(3))-1/sum(pp[i]/T[y,i] for i in range(3))
 num+=value
hh=[Q(1),Q(-1),Q(0)];HH=[hh[i]*RR[i] for i in range(3)];KK=sum(HH,s.zeros(2));gamma=s.trace(KK)/2;HH=[a-gamma*r for a,r in zip(HH,RR)];KK=sum(HH,s.zeros(2))
assert s.trace(KK)==0
ZZ=[HH[i]-RR[i]*KK for i in range(3)]
row=(vv[0].T*ZZ[0])/(root[0]*(vv[0].T*vv[0])[0])
assert all(ZZ[i]==zz[i]*row for i in range(3)) and row!=s.zeros(1,2)
physicalE=sum((Z.T*R.pinv()*Z for Z,R in zip(ZZ,RR)),s.zeros(2))
physicalN=s.zeros(2)
for y in range(3):
 aa=sum((T[y,i]*RR[i] for i in range(3)),s.zeros(2));bb=sum((T[y,i]*ZZ[i] for i in range(3)),s.zeros(2));physicalN+=bb.T*aa.inv()*bb
assert physicalN==num*physicalE
out={'pass':True,'cyclic_channel_exact_primal_dual':'2/11','cyclic_physical_reference_dimension':2,'cyclic_Hermitian_trace_ratio':str(N/E),'nonuniform_prior':list(map(str,pp)),'nonuniform_lower_value':str(num),'same_dimension_common_row_identity':True,'Hermitian_gauge_trace_zero':True}
assert json.loads(Path(__file__).with_name('small_classical_sdp_check.json').read_text()) == out, 'Exact fixture mismatch';print(out)
