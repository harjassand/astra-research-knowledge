"""Source-effect commutation does not imply terminal output preservation.
Algebra-only counterexample to an omitted terminal intertwiner premise.
"""
import numpy as np,json
from pathlib import Path
I=np.eye(2);X=np.array([[0.,1.],[1.,0.]]);p0=np.diag([1.,0.]);k=np.kron
PC=k(k(I,p0),I);PB=k(k(I,I),p0)
FC=k(k(I,np.diag([1.,2.])),I);GB=k(k(I,I),np.diag([1.,3.]))
J=k(k(X,I),X) # flips unknown logical qubit and clean BUSY bit
E=J.T@J
rho=np.zeros((8,8));rho[0,0]=1
out=J@rho@J.T
comm=lambda a,b:np.linalg.norm(a@b-b@a)
assert all(comm(E,a)==0 for a in [PC,PB,FC,GB])
assert np.trace((np.eye(8)-PB)@out)==1
logicalout=np.trace(out.reshape(2,4,2,4),axis1=1,axis2=3)
assert np.linalg.norm(logicalout-p0,ord='nuc')==2
r={'effect_commutators':{n:comm(E,a) for n,a in [('PC',PC),('PB',PB),('FC',FC),('GB',GB)]},'post_terminal_busy_bad_mass':float(np.trace((np.eye(8)-PB)@out)),'logical_output_trace_error':float(np.linalg.norm(logicalout-p0,ord='nuc')),'correct_repair':'preserve/intertwine the desired output module and predicate, OR compare actual terminal maps fed by safe preterminal states without an automatic output decoder conclusion','scope':'algebraic counterexample; no physical terminal operation is authorized by source-effect commutation alone'}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
