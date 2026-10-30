import numpy as np,json
I=np.eye(2,dtype=complex);Z=np.diag([1,-1]).astype(complex)
Hc=np.zeros((3,3),complex);Hc[0,1]=Hc[1,0]=1
H=np.kron(Hc,Z)
Jc=np.zeros((3,3),complex);Jc[2,1]=np.sqrt(.7);J=np.kron(Jc,I)
P=np.kron(np.diag([0,1,0]),I)
c=np.array([1,1j,0],complex)/np.sqrt(2)
values=[]
for b in range(2):
 d=np.eye(2,dtype=complex)[:,b];v=np.kron(c,d);rho=np.outer(v,v.conj())
 L=-1j*(H@rho-rho@H)+J@rho@J.conj().T-(J.conj().T@J@rho+rho@J.conj().T@J)/2
 values.append(float(np.trace(P@L).real))
assert abs(values[0]-values[1])>1.9
print(json.dumps({'scope':'Dirty coherent-prefix counterexample only; clean forest-factorized schedule law unaffected','terminal_population_derivatives_for_Z_data_eigenstates':values,'difference':abs(values[0]-values[1])},indent=2))
