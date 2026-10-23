"""Passive Gaussian converter calibration bridge and exact observational failures.
Synthetic governing-model checks, not a physical converter experiment.
"""
from pathlib import Path
import json,numpy as np
ROOT=Path(__file__).resolve().parent

def adj(A):return A.conj().T

def expm(A):
 w,V=np.linalg.eig(A);return (V*np.exp(w))@np.linalg.inv(V)

def lyap(G,D):
 n=len(G);L=np.kron(np.eye(n),G)+np.kron(G.conj(),np.eye(n));C=np.linalg.solve(L,-D.reshape(-1,order='F')).reshape((n,n),order='F');return (C+adj(C))/2

def herm_inv_sqrt(M):
 d,V=np.linalg.eigh((M+adj(M))/2);assert d.min()>0;return (V*(1/np.sqrt(d)))@adj(V)

def log_branch(T,tau):
 w,V=np.linalg.eig(T);return (V*(np.log(w)/tau))@np.linalg.inv(V)

def main():
 rng=np.random.default_rng(23102623);n=3;I=np.eye(n);k=np.array([1.,1.4,.7]);Qi=[np.diag([k[i] if j==i else 0 for j in range(n)]).astype(complex) for i in range(n)];K=sum(Qi)
 H=np.array([[.1,.28+.07j,0],[.28-.07j,-.15,.17j],[0,-.17j,.23]],complex);G=-K/2-1j*H
 assert np.linalg.eigvals(G).real.max()<0
 p=np.array([.6,.2j,.3]);Dp=.04*np.outer(p,p.conj());S=np.array([[1.2,.1j,.05],[.03,.8,.04j],[.01j,.06,1.1]],complex)
 # A valid unknown colored sensor: its own OU drift and positive covariance input.
 Gsens=np.diag([-.8+.1j,-.5-.2j,-1.+.4j]);Rs=lyap(Gsens,.03*I)
 def R(t):return expm(Gsens*t)@Rs
 def observe(gg,C,t):return S@expm(gg*t)@C@adj(S)+R(t)
 n0=.08;dn=.03;C0=lyap(G,n0*K+Dp);C1=lyap(G,(n0+dn)*K+Dp)
 M=(observe(G,C1,0)-observe(G,C0,0))/dn;W=herm_inv_sqrt(M);U=W@S
 tau=.001
 T=W@(observe(G,C1,tau)-observe(G,C0,tau))@W/dn
 Gu=log_branch(T,tau);target=U@G@adj(U)
 # Known branch contract for this synthetic decoder; not inferred from one lag.
 assert np.linalg.norm(G,2)*tau<np.pi/2
 bath_est=[]
 for i in range(n):
  Cb=lyap(G,n0*K+Dp+dn*Qi[i]);Ci_u=W@(observe(G,Cb,0)-observe(G,C0,0))@W/dn
  bath_est.append(-(Gu@Ci_u+Ci_u@adj(Gu)))
 errors={'metric_F':float(np.linalg.norm(M-S@adj(S))),'unitarity_F':float(np.linalg.norm(U@adj(U)-I)),'drift_F':float(np.linalg.norm(Gu-target)),'bath_Q_F':[float(np.linalg.norm(q-U@Qi[i]@adj(U))) for i,q in enumerate(bath_est)]}
 assert max([errors['metric_F'],errors['unitarity_F'],errors['drift_F']]+errors['bath_Q_F'])<1e-9
 # Equal-time data cannot supply an absolute dynamical clock.
 scale=7.;clock_same=max(float(np.linalg.norm(lyap(scale*G,scale*(sum(x*q for x,q in zip(ns,Qi))+Dp))-lyap(G,sum(x*q for x,q in zip(ns,Qi))+Dp))) for ns in [[.1,.2,.3],[.4,.2,.1],[.1,.1,.1]])
 # Trusted pump-off reference has known covariance nref I; it calibrates the
 # colored detector kernel, assuming it does not change when the pump is applied.
 Gref=-K/2-1j*np.diag([.1,-.15,.23]);nref=.06;Cref=nref*I
 R_u_tau=W@observe(Gref,Cref,tau)@W-nref*(U@expm(Gref*tau)@adj(U))
 # Gref in a real experiment also needs a calibrated differential-lag identification.
 Cu=expm(-Gu*tau)@(W@observe(G,C0,tau)@W-R_u_tau)
 Dpu=-(Gu@Cu+Cu@adj(Gu))-n0*sum(bath_est)
 currents=np.array([np.trace(q@(n0*I-Cu)).real for q in bath_est]);true_currents=np.array([np.trace(q@(n0*I-C0)).real for q in Qi])
 rescue={'C_F':float(np.linalg.norm(Cu-U@C0@adj(U))),'pump_D_F':float(np.linalg.norm(Dpu-U@Dp@adj(U))),'bath_number_current_errors':np.abs(currents-true_currents).tolist(),'number_currents':currents.tolist(),'requirements':['Trusted pump-off covariance with all bath occupations equal and no pump excess diffusion','Same instantaneous invertible S and independent sensor covariance kernel across pump/reference','Reference and target drift known with a calibrated clock and log branch/continuous lag','No hidden loss bath omitted from the occupation reference']};assert max(rescue['C_F'],rescue['pump_D_F'],max(rescue['bath_number_current_errors']))<1e-9
 # Exactly indistinguishable proper Gaussian one-mode observed processes.
 g=-1.-2j;n1,n2=1.,0.;CA=(n1+n2)/2;CB=CA+.5
 def ga(t,C,readout):return np.exp(g*t)*(C+readout)
 aliasdiff=max(abs(ga(t,CA,.5)-ga(t,CB,0)) for t in [0,.1,.7,2.])
 assert aliasdiff==0
 alias={'G':[g.real,g.imag],'Q':[1,1],'occupations':[n1,n2],'model_A':{'Dp':0,'C':CA,'sensor_OU_variance':.5,'currents':[n1-CA,n2-CA]},'model_B':{'Dp':1,'C':CB,'sensor_OU_variance':0,'currents':[n1-CB,n2-CB]},'observed_covariance_difference':aliasdiff,'scope':'All Gaussian process laws and all controlled occupation settings match; no passive data volume resolves internal pump versus invariant sensor OU noise.'}
 # Partial-bath control: identical observations, wrong inferred metric even with Dp=0.
 nc=.4;partial=[]
 for qc,qu,s in [(1.,1.,1.),(.5,1.5,np.sqrt(2))]:
  C=nc*qc/2;partial.append({'Qc':qc,'Qu':qu,'S':float(s),'C':C,'observed_C':float(s*s*C),'Mcontrolled':float(s*s*qc/2),'true_metric':float(s*s),'controlled_number_current':qc*(nc-C)})
 assert abs(partial[0]['observed_C']-partial[1]['observed_C'])<1e-14
 out={'status':'Model-conditional acquisition bridge plus exact indistinguishability constructions; no physical validation','seed':23102623,'synthetic_three_mode_errors':errors,'equal_time_common_rate_scale':scale,'max_equal_time_covariance_change':clock_same,'reference_rescue':rescue,'pump_sensor_alias':alias,'partial_control_alias':partial,'energy_scope':'These are bath number currents. Heat requires a supplied physical energy observable; for local single-mode bath i, multiply by hbar omega_i. Pump power, source inefficiency and material absorption are not inferred by these covariance checks.','physical_contract':['Full instantaneous complex-quadrature readout; fixed invertible transduction S','Known common occupation shift of ALL dissipative bath contributions: deltaD=delta_n K','Hurwitz G and unique stationary covariance','Fixed H,K,Qi,Dp during thermal settings; no pump-induced drift of detector noise','Time-lag data with calibrated time/phase and branch control','Trusted sensor reference or temporally white sensor if absolute heating/current is sought']}
 (ROOT/'thermal_bridge_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
