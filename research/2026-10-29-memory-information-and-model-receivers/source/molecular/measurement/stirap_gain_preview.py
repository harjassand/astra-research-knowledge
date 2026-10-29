"""Coherent span-transfer preview, retaining the entire resonant D RF chain.

Carrier RWA only here. Off-resonant S/optical edges and all sidebands are NOT
qualified. RF is an additional specified control, not acquired apparatus.
"""
from pathlib import Path
import json,time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import svdvals
from parking_preview import model

HERE=Path(__file__).resolve().parent


def controls(t,T,Tr,Or,Os,schedule=None):
    if t<Tr:return 0.,Os*np.sin(np.pi*t/(2*Tr))**2
    if t<Tr+T:
        f=np.sin(np.pi*(t-Tr)/(2*T))**2
        theta=np.pi/2*f if schedule is None else np.interp(f,*schedule)
        return Or*np.sin(theta),Os*np.cos(theta)
    return Or*np.cos(np.pi*(t-Tr-T)/(2*Tr))**2,0.


def run(chain,T=200e-6,N=120,local=False):
    w,eta,g,D,packets,code=model(N)
    L=8 if chain else 4
    # a,b,d,c for Lambda; a,b,D(-5/2),D(-3/2),... for chain.
    initial=np.zeros((N,L,2),complex);initial[:,0,0]=1;initial[:,2,1]=1
    Or=2*np.pi*40e3
    Os=2*np.pi*85e3/np.sqrt(5)  # original stretched optical edge85kHz
    Tr=T/10
    weights=np.sqrt(np.array([5,8,9,8,5])/5)
    schedule=None;metric_integral=None
    if local:
        th=np.linspace(0,np.pi/2,4001)
        den=((g[:,None]*Os*np.cos(th))**2+(Or*np.sin(th))**2)**1.5
        mt=2*np.sqrt(149/45)*g[:,None]*Os*Or/den
        weight=np.sqrt(np.sum(abs(packets[0])[:,None]**2*mt**2,axis=0))
        cdf=np.r_[0,np.cumsum((weight[:-1]+weight[1:])/2*np.diff(th))]
        metric_integral=float(cdf[-1]);cdf/=cdf[-1]
        schedule=(cdf,th)
    def rhs(t,flat):
        y=flat.reshape(N,L,2);dy=np.zeros_like(y)
        r,s=controls(t,T,Tr,Or,Os,schedule)
        dy[:,1]+=s*g[:,None]/2*y[:,3]
        dy[:,3]+=s*g[:,None]/2*y[:,1]
        if chain:
            for j,q in enumerate(weights):
                dy[:,2+j]+=r*q/2*y[:,3+j]
                dy[:,3+j]+=r*q/2*y[:,2+j]
        else:
            dy[:,2]+=r/2*y[:,3];dy[:,3]+=r/2*y[:,2]
        return (-1j*dy).reshape(-1)
    sol=solve_ivp(rhs,(0,2*Tr+T),initial.reshape(-1),method='DOP853',
      rtol=1e-10,atol=1e-12,max_step=T/150)
    assert sol.success
    actual=sol.y[:,-1].reshape(N,L,2)
    target=np.zeros_like(actual);target[:,0,0]=1;target[:,1,1]=-1
    err=np.array([svdvals(actual[n]-target[n])[0] for n in range(N)])
    # Apply the SAME isometry to both coherently entangled source cat labels.
    coeff=np.zeros((N,2,2),complex)
    coeff[:,0,0]=packets[0]/np.sqrt(2);coeff[:,1,0]=packets[0]/np.sqrt(2)
    coeff[:,0,1]=packets[1]/np.sqrt(2);coeff[:,1,1]=-packets[1]/np.sqrt(2)
    joint=np.einsum('nli,nij->lnj',actual,coeff).reshape(L*N,2)
    ideal=np.einsum('nli,nij->lnj',target,coeff).reshape(L*N,2)
    overlap=np.trace(ideal.conj().T@joint)
    return {'chain':chain,'local_adiabatic':local,'metric_integral_s':metric_integral,
      'T_s':T,'total_s':2*Tr+T,'N':N,
      'peak_RF_edge_Hz':Or/(2*np.pi),'peak_optical_b_c_Hz':Os/(2*np.pi),
      'RF_edge_weights':weights.tolist() if chain else [1.],
      'uniform_n_error':float(err.max()),'n_worst':int(err.argmax()),
      'source_joint_code_error':float(svdvals(joint-ideal)[0]),
      'source_joint_code_entanglement_fidelity':float(abs(overlap/2)**2),
      'per_n_error':err.tolist(),'phase_of_d_to_b':np.angle(-actual[:,1,1]).tolist(),
      'norm_defect':float(max(np.linalg.norm(actual[n].conj().T@actual[n]-np.eye(2),2) for n in range(N))),
      'rhs_evaluations':sol.nfev,'unpaid':['off-resonant spectator edges','sidebands','detuning and noise','RF apparatus','return and science transfer']}


def main():
    start=time.perf_counter()
    a,b,c=run(False),run(True),run(True,local=True)
    out={'status':'CARRIER_MODEL_ONLY_NO_GATE_ACQUISITION','lambda':a,'full_resonant_D_chain':b,
      'full_chain_local_schedule':c,
      'wall_seconds':time.perf_counter()-start}
    (HERE/'STIRAP_GAIN_PREVIEW.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:{j:v[j] for j in ['uniform_n_error','n_worst','source_joint_code_error','total_s','rhs_evaluations']} for k,v in [('lambda',a),('chain',b),('local',c)]}|{'wall_seconds':out['wall_seconds']},indent=2))


if __name__=='__main__':main()
