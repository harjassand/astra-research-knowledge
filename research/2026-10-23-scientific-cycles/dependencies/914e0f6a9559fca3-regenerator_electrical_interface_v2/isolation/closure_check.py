"""Algebraic multiport check; no device or useful-operation certification."""
from pathlib import Path
import json
import numpy as np
from gate_stack import *
R=Path(__file__).resolve().parent

def U(mu,T,Vf):
 d=g.dirac(mu,T);z=face(mu,T,Vf)
 return d['Omega']+T*d['entropy']+mu*g.E_CHARGE*d['n']+z['Eiso']+z['Egeo']+.5*CGAP*(mu-PHIR)**2
rows=[]
for mu,T,Vf,Td,Vd,md in [(.3,343.,12.,1000.,-2e4,2e4),(.6,344.,.1,-500.,1e4,0.),(.1695,341.,23.,100.,0.,-1e4)]:
 z=face_flow(mu,T,Vf,Td,Vd,md);eps=1e-10
 du=(U(mu+eps*md,T+eps*Td,Vf+eps*Vd)-U(mu-eps*md,T-eps*Td,Vf-eps*Vd))/(2*eps)
 heat=z['CVmu']*Td+T*z['enT']*md
 ports=z['gate_power']+z['FE_cross_power']+z['reservoir_power']
 rows.append(dict(state=[mu,T,Vf],rates=[md,Td,Vd],dU_W_m2=du,heat_W_m2=heat,ports_W_m2=ports,
  energy_residual_W_m2=du-heat-ports,
  reduced_CV_identity=z['CVgate']+T*z['alpha_g']*z['Vg_T']-z['CVmu'],
  reduced_alpha_identity=z['alpha_g']*z['Vg_mu']-z['enT']))
(R/'closure_check.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
