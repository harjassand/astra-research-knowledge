"""Independent finite regressions; not a protected-code gate simulation."""
from functools import reduce
from pathlib import Path
import json, numpy as np
from scipy.linalg import eigvalsh,norm
from scipy.sparse import csc_matrix,eye,kron
from scipy.sparse.linalg import expm_multiply

def ten(*xs): return reduce(np.kron,xs)
def kb(i,j,d):
 a=np.zeros((d,d),complex);a[i,j]=1;return a
I2=np.eye(2);I3=np.eye(3);X=kb(0,1,2)+kb(1,0,2);Y=-1j*kb(0,1,2)+1j*kb(1,0,2);Z=np.diag([1.,-1.])
Om=.8;kap=1.3
H0=Om*(kb(0,1,3)+kb(1,0,3));J0=np.sqrt(kap)*kb(2,1,3)
B=kb(0,0,3)+kb(1,1,3)
R=np.zeros((3,3),complex);R[:2,:2]=[[2/kap+kap/(4*Om**2),-1j/(2*Om)],[1j/(2*Om),2/kap]]
Rm=eigvalsh(R[:2,:2])[-1];a=eigvalsh(R[:2,:2])[0]/Rm;r=1/Rm;A=R/Rm

def adj(H,js,O):return 1j*(H@O-O@H)+sum((j.conj().T@O@j-.5*(j.conj().T@j@O+O@j.conj().T@j) for j in js),np.zeros_like(O))
res=float(norm(adj(H0,[J0],R)+B))
# memory x clock x clock x common bath; projection kills memory label 1.
D=36;Id=np.eye(D);P=ten(kb(0,0,2),I3,I3,I2)
H=ten(I2,H0,I3,I2)+ten(I2,I3,H0,I2)
js=[ten(I2,J0,I3,I2),ten(I2,I3,J0,I2)]
X02=kb(0,2,3)+kb(2,0,3)
nh=.0005*ten(X,X02,X02,X)
nj=np.sqrt(.0003)*ten(I2,kb(0,2,3),kb(0,2,3),X)
# Physical program-conditioned memory exit: killed map retains its loss.
exitj=np.sqrt(.0007)*ten(kb(1,0,2),kb(0,0,3),I3,I2)
H+=nh;js += [nj,exitj]
eta=2*norm(nh,2)+2*norm(nj,2)**2+2*norm(exitj,2)**2;q=2
# Restriction to the memory=0 corner.
inds=np.arange(18); Hk=(P@H@P)[np.ix_(inds,inds)]
Jks=[(P@j@P)[np.ix_(inds,inds)] for j in js]
loss=[(P@j.conj().T@j@P)[np.ix_(inds,inds)] for j in js]
Ik=eye(18,format='csc',dtype=complex);hk=csc_matrix(Hk)
L=-1j*(kron(Ik,hk)-kron(hk.T,Ik))
for j,l in zip(Jks,loss):
 j=csc_matrix(j);l=csc_matrix(l)
 L+=kron(j.conjugate(),j)-.5*(kron(Ik,l)+kron(l.T,Ik))
# Initially correlated programs and bath, not a product program input.
psi=np.zeros(18,complex);psi[0]=np.sqrt(.6);psi[9]=1j*np.sqrt(.4)
rho=np.outer(psi,psi.conj())
obs=[];least_outgoing=1.
for S in [(0,),(1,),(0,1)]:
 factors=[A if i in S else I3 for i in range(2)]
 M=ten(I2,*factors,I2);Mk=M[np.ix_(inds,inds)]
 full=(P@adj(H,js,M)@P)[np.ix_(inds,inds)]
 killed=1j*(Hk@Mk-Mk@Hk)+sum((j.conj().T@Mk@j-.5*(l@Mk+Mk@l) for j,l in zip(Jks,loss)),np.zeros_like(Mk))
 least_outgoing=min(least_outgoing,float(eigvalsh(full-killed)[0]))
 BB=ten(*(B if i in S else I3 for i in range(2)),I2)
 obs.append((S,Mk,BB))
rows=[];worst=0.
for t in [0.,1.,5.,15.,40.]:
 rt=expm_multiply(t*L,rho.ravel(order='F')).reshape(18,18,order='F')
 p=(np.exp(-q*r*t)+(eta/r)*(1-np.exp(-q*r*t)))**(1/q)
 row={'time':t,'trace':float(np.trace(rt).real),'moments':[]}
 for S,M,BB in obs:
  ma=float(np.trace(rt@M).real);mb=float(np.trace(rt@BB).real)
  worst=max(worst,ma-p**len(S),mb-(p/a)**len(S))
  row['moments'].append({'set':S,'A_moment':ma,'A_bound':p**len(S),'unfinished':mb,'unfinished_bound':(p/a)**len(S)})
 rows.append(row)
# The audited structural-footprint defect: SWAP preserves total excitation,
# but XX and YY Pauli coefficients separately connect different energy sectors.
SWAP=.5*(ten(I2,I2)+ten(X,X)+ten(Y,Y)+ten(Z,Z))
energy=ten(kb(1,1,2),I2)+ten(I2,kb(1,1,2))
swap_comm=float(norm(SWAP@energy-energy@SWAP))
xx_comm=float(norm(ten(X,X)@energy-energy@ten(X,X)))
assert swap_comm<1e-12 and xx_comm>1
# Exact frame equation with a noncommuting controller-controlled forest.
CNOT=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],complex)
F=ten(np.eye(4),kb(0,0,2))+ten(ten(X,I2),kb(1,1,2))
U=ten(CNOT,I2);Fstar=U@F@U.conj().T
frame_res=[]
for label in [0,1,2]:
 G=np.eye(8) if label==0 else U
 E=F.conj().T@U.conj().T@G@F
 frame_res.append(float(norm(Fstar.conj().T@G@F-U@E)))
assert res<1e-12 and least_outgoing>-1e-12 and worst<1e-10 and max(frame_res)<1e-12
out={'scope':'Finite-dimensional algebra checks only. This does not simulate a native protected code, establish strong raw moments, or certify a gate threshold.','gramian_residual':res,'a':a,'r':r,'eta':float(eta),'killed_outgoing_min_eigenvalue':least_outgoing,'maximum_moment_violation':worst,'samples':rows,'structural_footprint_counterexample':{'swap_energy_commutator':swap_comm,'xx_energy_commutator':xx_comm},'frame_identity_residuals':frame_res}
Path(__file__).with_name('killed_clock_and_suffix_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
