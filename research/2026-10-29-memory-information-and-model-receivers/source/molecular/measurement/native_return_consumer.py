"""Source-informed complete one-mode parking/recoil/return consumer.

Added selective ground-RF control; no apparatus qualification. Full optical
motional sidebands, source beyond-LD cat generation and native return retained.
No postselection or scalar-C division. Uniform D-Stark phase is maximized
analytically; this is NOT a complete molecular science-transfer certificate.
"""
from pathlib import Path
import json,time
import numpy as np
from scipy.linalg import eigh,expm
from scipy.integrate import solve_ivp
from parking_preview import model,sequence

HERE=Path(__file__).resolve().parent


def optical(y,start,theta,bb1,smooth,rate,w,gref,D,inverse=False,axis_phase=0.):
    N=y.shape[1];K=y.shape[2]
    seq=sequence(theta,bb1)
    if inverse:seq=[(a,p+np.pi) for a,p in seq[::-1]]
    evaluations=0
    for angle,phase in seq:
        phase+=axis_phase
        om=2*np.pi*rate
        duration=(2 if smooth else 1)*angle/(om*gref)
        def rhs(t,flat):
            psi=flat.reshape(3,N,K)
            amp=om*(np.sin(np.pi*t/duration)**2 if smooth else 1.)
            ep=np.exp(1j*w*np.arange(N)*(start+t))
            dy=np.zeros_like(psi)
            dy[0]=-1j*amp/2*np.exp(1j*phase)*ep[:,None]*(D@(ep.conj()[:,None]*psi[2]))
            dy[2]=-1j*amp/2*np.exp(-1j*phase)*ep[:,None]*(D.conj().T@(ep.conj()[:,None]*psi[0]))
            return dy.reshape(-1)
        sol=solve_ivp(rhs,(0,duration),y.reshape(-1),method='DOP853',
          rtol=3e-10,atol=2e-12,max_step=2*np.pi/w/8)
        assert sol.success
        y=sol.y[:,-1].reshape(3,N,K);start+=duration;evaluations+=sol.nfev
    return y,start,evaluations


def rf(y,inverse=False):
    # pi swap5.6us inferred from the2.8us pi/2 preparation in Kurz2014.
    tmp=y.copy();sgn=1j if inverse else -1j
    tmp[0]=sgn*y[1];tmp[1]=sgn*y[0]
    return tmp,5.6e-6


def main():
    start_wall=time.perf_counter();N=100
    w,eta,g,D,packets,code=model(N)
    psi2=(code[:,0]+code[:,1])/np.sqrt(2)
    initial=np.zeros((3,N,1),complex);initial[0,:,0]=psi2[:N];initial[2,:,0]=psi2[N:]
    # Published sideband-only cat Hamiltonian, reversed with its native phase.
    from scipy.special import eval_genlaguerre
    n=np.arange(N-1)
    coupling=np.exp(-eta*eta/2)/np.sqrt(n+1)*eval_genlaguerre(n,1,eta*eta)
    ad=np.diag(coupling,-1);p=1j*(ad-ad.T)
    ep,P=eigh(p);strength=(2*np.pi*.145e6)*eta*175e-6/2
    cat_inverse={s:(P*np.exp(1j*s*strength*ep))@P.conj().T for s in (1,-1)}
    def uncat(y):
        ans=y.copy()
        plus=(y[0]+y[2])/np.sqrt(2);minus=(y[0]-y[2])/np.sqrt(2)
        plus=cat_inverse[1]@plus;minus=cat_inverse[-1]@minus
        ans[0]=(plus+minus)/np.sqrt(2);ans[2]=(plus-minus)/np.sqrt(2)
        return ans
    X=np.diag(np.sqrt(np.arange(1,N)),1);X=X+X.T
    ex,V=eigh(X)
    obs={'z':np.diag([1,0,-1]),'y':np.array([[0,0,-1j],[0,0,0],[1j,0,0]]),
         'x':np.array([[0,0,1],[0,0,0],[1,0,0]]),'ground_leak':np.diag([0,1,0])}
    def mean(y,O):return np.einsum('ink,ij,jnk->',y.conj(),O,y).real
    reports=[]
    for bb1,smooth in [(False,False),(True,False),(True,True)]:
        y,t=rf(initial);y,t,ne=optical(y,t,np.pi,bb1,smooth,85e3,w,g[42],D)
        Dpopulation=float(np.sum(abs(y[2])**2))
        sync=(-t)%(2*np.pi/w);t+=sync
        cases=[]
        for kick in [0.,-.03,.03]:
            K=(V*np.exp(1j*kick*ex))@V.T
            baseline=uncat(np.einsum('ab,ibk->iak',K,initial))
            kicked=np.einsum('ab,ibk->iak',K,y)
            # Resolve ground and D components. They carry phase1 and z=e^-iChi.
            split=np.zeros((3,N,2),complex)
            split[:2,:,0]=kicked[:2,:,0];split[2,:,1]=kicked[2,:,0]
            returned,tf,nr=optical(split,t,np.pi,bb1,smooth,85e3,w,g[42],D,inverse=True)
            returned,rf_time=rf(returned,inverse=True);tf+=rf_time
            output=uncat(returned)
            scores={}
            for name,O in obs.items():
                z0,z1=output[:,:,0],output[:,:,1]
                aa=np.einsum('in,ij,jn->',z0.conj(),O,z0).real
                dd=np.einsum('in,ij,jn->',z1.conj(),O,z1).real
                cross=np.einsum('in,ij,jn->',z0.conj(),O,z1)
                target=mean(baseline,O)
                nominal=aa+dd+2*cross.real
                scores[name]={'baseline':float(target),'parked_noStark':float(nominal),
                  'worst_error_all_uniform_D_Stark_phases':float(abs(aa+dd-target)+2*abs(cross))}
            cases.append({'kick':kick,'scores':scores,'control_time_s':tf,'return_rhs':nr})
        reports.append({'pulse':'smooth_BB1' if smooth else ('BB1' if bb1 else 'bare'),
          'D_population_during_science':Dpopulation,'forward_time_s':t,'sync_wait_s':sync,
          'forward_rhs':ne,'cases':cases})
    out={'status':'COMPLETE_SOURCE_MODEL_RECOIL_CONSUMER_NOT_MOLECULAR_QUERY_ACQUISITION',
      'N':N,'eta':eta,'source_repo':'b083acdaa181549ca591d76d86c283da013ed651','reports':reports,
      'wall_seconds':time.perf_counter()-start_wall,
      'unpaid':['RF/Zeeman selectivity on actual CaOH apparatus','other optical Zeeman edges',
       'spectator modes and measured control noise','state-dependent science/marked cross histories',
       'IR scalar-force gradients and real polarizabilities','full attempt rate/reset/loss/science signal']}
    (HERE/'NATIVE_RETURN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'reports':[{'pulse':r['pulse'],'D_population':r['D_population_during_science'],
      'time_s':r['cases'][0]['control_time_s'],
      'one_photon_scores':r['cases'][-1]['scores']} for r in reports],
      'wall_seconds':out['wall_seconds']},indent=2))


if __name__=='__main__':main()
