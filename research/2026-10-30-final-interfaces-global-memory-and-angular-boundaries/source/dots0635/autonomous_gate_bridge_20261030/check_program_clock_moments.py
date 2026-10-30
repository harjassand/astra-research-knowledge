"""Actual coherent 3-state clocks with one shared bath: algebra regression."""
import itertools,json
from pathlib import Path
import numpy as np
from scipy.linalg import eigvalsh
from scipy.sparse import csc_matrix,eye,kron
from scipy.sparse.linalg import expm_multiply

I3=np.eye(3,dtype=complex); I2=np.eye(2,dtype=complex)
def ketbra(i,j,d=3):
 x=np.zeros((d,d),complex);x[i,j]=1;return x
def prod(xs):
 r=np.array([[1]],complex)
 for x in xs:r=np.kron(r,x)
 return r
Om=1.;kap=1.
H0=Om*(ketbra(0,1)+ketbra(1,0))
J0=np.sqrt(kap)*ketbra(2,1)
B0=ketbra(0,0)+ketbra(1,1)
R0=np.zeros((3,3),complex)
R0[:2,:2]=[[2/kap+kap/(4*Om**2),-1j/(2*Om)],[1j/(2*Om),2/kap]]
Rmax=eigvalsh(R0[:2,:2])[-1]
a=eigvalsh(R0[:2,:2])[0]/Rmax;r=1/Rmax;A0=R0/Rmax
Lstar=lambda H,js,O:1j*(H@O-O@H)+sum((j.conj().T@O@j-.5*((j.conj().T@j)@O+O@(j.conj().T@j)) for j in js),np.zeros_like(O))
res=np.linalg.norm(Lstar(H0,[J0],R0)+B0)
# Two program registers and one retained common bath qubit.
D=18;I=np.eye(D,dtype=complex)
H=prod([H0,I3,I2])+prod([I3,H0,I2])
js=[prod([J0,I3,I2]),prod([I3,J0,I2])]
Xb=np.array([[0,1],[1,0]],complex)
# A correlated coherent reinfection and correlated jump touch BOTH programs.
X02=ketbra(0,2)+ketbra(2,0)
noise_h=.001*prod([X02,X02,Xb])
noise_j=np.sqrt(.0005)*prod([ketbra(0,2),ketbra(0,2),Xb])
eta=2*np.linalg.norm(noise_h,2)+2*np.linalg.norm(noise_j,2)**2
q=2
H=H+noise_h;js=js+[noise_j]
Hsp=csc_matrix(H);Id=eye(D,format='csc',dtype=complex)
L=-1j*(kron(Id,Hsp)-kron(Hsp.T,Id))
for j in js:
 j=csc_matrix(j); jj=j.conj().T@j
 L+=kron(j.conjugate(),j)-.5*(kron(Id,jj)+kron(jj.T,Id))
psi=prod([np.array([[1],[0],[0]],complex),np.array([[1],[0],[0]],complex),np.array([[1],[1j]],complex)/np.sqrt(2)]).ravel()
rho=np.outer(psi,psi.conj())
As=[prod([A0,I3,I2]),prod([I3,A0,I2])]
Bs=[prod([B0,I3,I2]),prod([I3,B0,I2])]
obs=[]
for S in [(0,),(1,),(0,1)]:
 MA=I.copy();MB=I.copy()
 for i in S:MA=MA@As[i];MB=MB@Bs[i]
 obs.append((S,MA,MB))
rows=[];max_violation=0.
for T in [0.,1.,4.,10.,20.]:
 rt=expm_multiply(L*T,rho.ravel(order='F')).reshape(D,D,order='F')
 p=(np.exp(-q*r*T)+(eta/r)*(1-np.exp(-q*r*T)))**(1/q)
 row={'time':T,'p':p,'unfinished_tail_base':p/a,'trace_error':float(abs(np.trace(rt)-1))}
 vals=[]
 for S,MA,MB in obs:
  m=float(np.trace(MA@rt).real);u=float(np.trace(MB@rt).real)
  gap=max(m-p**len(S),u-(p/a)**len(S))
  max_violation=max(max_violation,gap)
  vals.append({'set':list(S),'A_moment':m,'A_bound':p**len(S),'unfinished_moment':u,'unfinished_bound':(p/a)**len(S)})
 row['moments']=vals;rows.append(row)
assert res<1e-12
assert max_violation<1e-10
out={'dimension':D,'Omega':Om,'kappa':kap,'R_eigenvalues':eigvalsh(R0[:2,:2]).tolist(),'a':a,'r':r,'joint_noise_incidence_eta':eta,'q':q,'gramian_residual':res,'maximum_bound_violation':max_violation,'samples':rows,'scope':'Finite algebra regression only; not a protected-gate or code simulation.'}
p=Path(__file__).with_name('program_clock_moment_checks.json');p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
