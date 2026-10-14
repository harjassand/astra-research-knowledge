import sys,json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
import scipy
sys.path.insert(0,str(Path(__file__).resolve().parent/'replay_py314'))
from rotor_probe import rotor_blocks,NU,sigma_t
from scipy import constants as c
rows=[]
for jmax,M in [(70,12),(80,18),(70,9),(70,35)]:
 e,plus,*_=list(rotor_blocks(jmax,NU))[M]
 dp=plus.toarray();delta=e[:,None]-e[None,:];mask=abs(dp)>0
 dp[mask]/=np.exp(-(2*np.pi*c.c*100*delta[mask]*sigma_t)**2)
 D=dp+dp.conj().T
 for driver in ['evr','evd','evx','ev']:
  lam,V=eigh(D,driver=driver)
  orth=float(np.linalg.norm(V.conj().T@V-np.eye(len(D)),ord=2))
  eig=float(np.linalg.norm(D@V-V*lam,ord=2))
  rows.append(dict(jmax=jmax,M=M,dim=len(D),driver=driver,orthogonality_error=orth,eigen_residual=eig))
print(json.dumps({'numpy':np.__version__,'scipy':scipy.__version__,'rows':rows},indent=2))
