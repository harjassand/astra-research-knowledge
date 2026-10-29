"""Recover and exactly verify a rational Lyapunov certificate, n=30,g=kappa=1."""
import numpy as np,json
from scipy.linalg import solve_continuous_lyapunov
import sympy as sp
n=30
A=-1j*(np.diag(np.ones(n-1),1)+np.diag(np.ones(n-1),-1));A[-1,-1]-=.5
P=solve_continuous_lyapunov(A.conj().T,-np.eye(n))
Qr=np.rint(4*P.real).astype(int);Qi=np.rint(4*P.imag).astype(int)
Q=sp.Matrix([[int(Qr[i,j])+sp.I*int(Qi[i,j]) for j in range(n)] for i in range(n)])
B=sp.zeros(n)
for i in range(n-1):B[i,i+1]=B[i+1,i]=-2*sp.I
B[-1,-1]=-1
assert B.conjugate().T*Q+Q*B == -8*sp.eye(n)
assert Q==Q.conjugate().T
traceP=sp.trace(Q)/4
assert traceP==sp.Rational(24335,4)
result={'dimension':n,'trace_P_exact':str(traceP),'ready_mean_exact':str(Q[0,0]/4),
        'T_for_half_reset_probability':str(2*traceP),
        'delta_bound_for_quarter_noisy_reset_probability':str(1/(8*traceP)),
        'Q_real':Qr.tolist(),'Q_imag':Qi.tolist()}
open('autonomous_noise_bridge_20261029/path_clock_certificate.json','w').write(json.dumps(result,indent=2)+'\n')
print({k:v for k,v in result.items() if not k.startswith('Q_')})
