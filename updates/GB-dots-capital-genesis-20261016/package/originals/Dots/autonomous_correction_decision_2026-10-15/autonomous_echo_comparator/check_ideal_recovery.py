"""Independent four-level check; does not import or execute deposited author code."""
import numpy as np
import math,json
m=np.array([-1.5,-.5,.5,1.5])
s=math.sqrt(3)/2
L=np.array([[.5,0],[0,s],[s,0],[0,.5]],dtype=complex)
E=np.array([[-s,0],[0,-.5],[.5,0],[0,s]],dtype=complex)
R=[L@L.conj().T,L@E.conj().T]
assert np.allclose(L.conj().T@L,np.eye(2))
assert np.allclose(E.conj().T@E,np.eye(2))
assert np.allclose(L.conj().T@E,0)
assert np.allclose(sum(r.conj().T@r for r in R),np.eye(4))
rho01=np.outer(L[:,0],L[:,1].conj())
maxerr=0.
for theta in np.linspace(-4*math.pi,4*math.pi,401):
 U=np.diag(np.exp(-1j*theta*m))
 out=sum(r@U@rho01@U.conj().T@r.conj().T for r in R)
 f=-np.exp(3j*theta)/8+3*np.exp(1j*theta)/4+3*np.exp(-1j*theta)/8
 maxerr=max(maxerr,abs((L.conj().T@out@L)[0,1]-f))
 assert np.allclose(out,f*rho01)
 assert abs(f-(math.cos(theta)*(1+.5*math.sin(theta)**2)+.5j*math.sin(theta)**3))<1e-14
 assert abs(abs(f)**2-(1-.75*math.sin(theta)**4))<1e-14
 # Verify same fixed-angle recovery repeated, without replacing by averaged channel.
 out2=sum(r@U@out@U.conj().T@r.conj().T for r in R)
 assert np.allclose(out2,f*f*rho01)
# Exact Fourier-polynomial Gaussian integration, illustrative variance only.
c={3:-1/8,1:3/4,-1:3/8}
def multiply(a,b):
 out={}
 for k,v in a.items():
  for l,w in b.items():out[k+l]=out.get(k+l,0)+v*w
 return out
def gaussian_average(a,variance):return sum(v*math.exp(-k*k*variance/2) for k,v in a.items())
v=.4**2
print(json.dumps({'status':'PASS','max_four_level_factor_error':maxerr,'illustrative_phase_sd_rad':math.sqrt(v),'same_angle_two_cycles_E_f_squared':gaussian_average(multiply(c,c),v),'independent_two_cycles_E_f_then_squared':gaussian_average(c,v)**2,'warning':'These are conditional ideal-code checks, not a fitted experimental channel or a novelty claim.'},indent=2))
