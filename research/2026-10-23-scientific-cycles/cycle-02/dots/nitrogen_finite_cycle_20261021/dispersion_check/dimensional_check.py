"""Dimensional scales, not a trajectory or measured dispersion fit.
Run from any directory; uses existing pinned thermo helper solely for properties.
"""
from pathlib import Path
import sys,json,time,resource,hashlib
import numpy as np
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'thermo_helper'))
from helper import ThermoKernel
start=time.monotonic();K=ThermoKernel()
L=.1;dp=.009525;eps=.4;G=1.;N=12;dx=L/N
Y=np.zeros(6);Y[:2]=np.array([.79,.21])*K.W[:2];Y/=Y.sum()
r=K.evaluate(np.array([300.,1000.,1700.,2700.]),Y)
rows=[]
for i,T in enumerate(r['T']):
 rho=float(r['rho'][i]);mu=float(r['viscosity'][i]);cp=float(r['cp'][i]);kg=float(r['conductivity'][i]);us=G/rho;u=us/eps
 anum=u*dx/2;amech=u*dp/2
 rows.append(dict(T_K=float(T),rho_kg_m3=rho,mu_Pas=mu,cp_J_kgK=cp,kg_W_mK=kg,superficial_u_m_s=us,interstitial_U_m_s=u,Re_superficial=G*dp/mu,Pr=cp*mu/kg,alpha_molecular_m2_s=kg/(rho*cp),upwind_semidiscrete_D_m2_s=anum,conditional_highflow_alpha_m2_s=amech,conditional_mechanical_k_W_mK=eps*rho*cp*amech,gas_residence_s=L/u))
result=dict(scope='Fixed frozen feed composition at1atm, not hot reacting bed data; highflow coefficient is historical limiting scale only.',L_m=L,dp_m=dp,epsilon=eps,G_kg_m2s=G,N=N,dx_m=dx,L_over_dp=L/dp,numerical_Pe_particle=2*dp/dx,numerical_Pe_bed=2*L/dx,conditional_highflow_Pe_bed=2*L/dp,Dnum_over_conditional_highflow=dx/dp,rows=rows,notes=['Dnum=abs(U)*dx/2 is local constant-coefficient smooth-field semidiscrete modified equation; no CFL factor for method-of-lines. Time integration, pressure coupling, boundary half cells and reaction add errors.','Physical D has not been measured for this bed. Pe2 here is an historical high-flow thermal limiting scale, not a validated closure or species value.','Effective conductivity normalization is k_ax=epsilon*rho*cp*alpha_ax for gas-volume diffusivity. Existing solid radiative flux must not be counted again as effective gas conductivity.'])
result['runtime_s']=time.monotonic()-start;result['peak_rss_KiB_linux']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(R/'dimensional_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
