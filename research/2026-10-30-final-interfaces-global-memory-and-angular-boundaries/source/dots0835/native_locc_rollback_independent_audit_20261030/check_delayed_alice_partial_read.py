import numpy as np, json
I=np.eye(2); X=np.array([[0.,1.],[1.,0.]]); Z=np.diag([1.,-1.]); H=(X+Z)/np.sqrt(2)
p0=np.diag([1.,0.]); p1=np.diag([0.,1.])
# ancilla, Alice resource1, Alice resource2
U_partial=(np.kron(p0,np.eye(4))+np.kron(p1,np.kron(X,I)))@np.kron(H,np.eye(4))
U_full=(np.kron(p0,np.eye(4))+np.kron(p1,np.kron(I,X)))@U_partial
phi=np.array([1,0,0,1.])/np.sqrt(2)
v=np.kron(np.array([1.,0.]),phi)
def trace_ancilla(psi):
    a=psi.reshape(2,4)
    return a.T@a.conj()
partial=trace_ancilla(U_partial@v)
full=trace_ancilla(U_full@v)
ZZ=np.kron(Z,Z)
wrong=(np.eye(4)-ZZ)/2
out={'initial_ZZ':float(phi@ZZ@phi),
     'partial_read_ZZ':float(np.trace(ZZ@partial)),
     'partial_read_invalidates_cached_ZZ_probability':float(np.trace(wrong@partial)),
     'full_read_ZZ':float(np.trace(ZZ@full)),
     'full_read_preservation_error':float(np.linalg.norm(full-np.outer(phi,phi)))}
assert abs(out['partial_read_invalidates_cached_ZZ_probability']-.5)<1e-14
assert abs(out['full_read_ZZ']-1)<1e-14
print(json.dumps(out,indent=2))
