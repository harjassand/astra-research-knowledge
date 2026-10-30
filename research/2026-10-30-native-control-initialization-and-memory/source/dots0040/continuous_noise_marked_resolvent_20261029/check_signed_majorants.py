import numpy as np,json
rng=np.random.default_rng(1237)
maxerr=0.; minmargin=1.
for d in [2,3,5]:
 I=np.eye(d)
 for trial in range(20):
  H=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));H=(H+H.conj().T)/2;g=np.linalg.norm(H,2);A=H/g
  cp=lambda J:np.kron(J.conj(),J)
  plus=(g/2)*cp(I-1j*A);minus=(g/2)*cp(I+1j*A)
  target=-1j*(np.kron(I,H)-np.kron(H.T,I))
  maxerr=max(maxerr,np.max(abs(plus-minus-target)))
  minmargin=min(minmargin,np.linalg.eigvalsh(2*g*I-g*(I+A@A)).min())
  L=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));ell=np.linalg.norm(L,2);B=L.conj().T@L/ell**2
  plus=cp(L)+(ell**2/4)*cp(I-B);minus=(ell**2/4)*cp(I+B)
  target=cp(L)-.5*(np.kron(I,L.conj().T@L)+np.kron((L.conj().T@L).T,I))
  maxerr=max(maxerr,np.max(abs(plus-minus-target)))
  minmargin=min(minmargin,np.linalg.eigvalsh(2*ell**2*I-ell**2*(B+.5*(I+B@B))).min())
print(json.dumps({'max_signed_identity_residual':float(maxerr),'min_positive_effect_margin':float(minmargin),'trials':60,'note':'Numerical algebra regression only; not a full memory theorem.'},indent=2))
assert maxerr<1e-11 and minmargin>-1e-11
