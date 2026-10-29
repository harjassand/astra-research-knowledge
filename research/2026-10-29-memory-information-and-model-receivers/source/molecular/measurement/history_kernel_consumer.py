"""Complete finite-history source-model kernels; no physical qualification.
Both S levels fluoresce. Sidebands and physical same-command return retained.
"""
from pathlib import Path
import json,time
import numpy as np
from scipy.linalg import eigh
from scipy.special import eval_genlaguerre
from parking_preview import model
from native_return_consumer import optical,rf
HERE=Path(__file__).resolve().parent

def enc(a):return {'real':a.real.tolist(),'imag':a.imag.tolist()}

def project_toeplitz(a,hs,blocks):
    t=np.zeros_like(a)
    for lag in range(min(hs)-max(hs),max(hs)-min(hs)+1):
        vals=[a[j,k] for bl in blocks for j in bl for k in bl if hs[k]-hs[j]==lag]
        if vals:
            val=sum(vals)/len(vals)
            for j in range(len(hs)):
                for k in range(len(hs)):
                    if hs[k]-hs[j]==lag:t[j,k]=val
    return a-t,t

def bound(A,B,hs,blocks):
    ra,ta=project_toeplitz(A,hs,blocks);rb,tb=project_toeplitz(B,hs,blocks)
    norms=lambda q:[np.linalg.norm(q[np.ix_(bl,bl)],2) for bl in blocks]
    return {'raw_uniform_Stark_error_upper':float(max(a+2*b for a,b in zip(norms(A),norms(B)))),
      'nonzero_phase_harmonic_error_upper':float(max(a+2*b for a,b in zip(norms(ra),norms(rb)))),
      'toeplitz_A':enc(ta),'toeplitz_B':enc(tb),'blocks':blocks}

def run(bb1,smooth,N=100):
    w,eta,g,D,packets,code=model(N)
    hs=list(range(-4,5));H=len(hs)
    psi=(code[:,0]+code[:,1])/np.sqrt(2)
    initial=np.zeros((3,N,1),complex);initial[0,:,0]=psi[:N];initial[2,:,0]=psi[N:]
    n=np.arange(N-1)
    coupling=np.exp(-eta*eta/2)/np.sqrt(n+1)*eval_genlaguerre(n,1,eta*eta)
    ad=np.diag(coupling,-1);p=1j*(ad-ad.T)
    ep,P=eigh(p);strength=(2*np.pi*.145e6)*eta*175e-6/2
    up=(P*np.exp(1j*strength*ep))@P.conj().T
    um=(P*np.exp(-1j*strength*ep))@P.conj().T
    def uncat(y):
        ans=y.copy();pl=up@((y[0]+y[2])/np.sqrt(2));mi=um@((y[0]-y[2])/np.sqrt(2))
        ans[0]=(pl+mi)/np.sqrt(2);ans[2]=(pl-mi)/np.sqrt(2)
        return ans
    parked,t=rf(initial)
    parked,t,nf=optical(parked,t,np.pi,bb1,smooth,85e3,w,g[42],D)
    sync=(-t)%(2*np.pi/w);t+=sync
    aa=np.diag(np.sqrt(np.arange(1,N)),1);x=aa+aa.T
    ex,V=eigh(x);etaIR=.03
    inputs=np.zeros((3,N,2*H),complex);targets=np.zeros((3,N,H),complex)
    for j,h in enumerate(hs):
        kick=(V*np.exp(1j*h*etaIR*ex))@V.T
        k=np.einsum('ab,ibk->iak',kick,parked)
        inputs[:2,:,j]=k[:2,:,0];inputs[2,:,H+j]=k[2,:,0]
        targets[:,:,j]=np.einsum('ab,ibk->iak',kick,initial)[:,:,0]
    returned,tf,nr=optical(inputs,t,np.pi,bb1,smooth,85e3,w,g[42],D,inverse=True)
    returned,rt=rf(returned,inverse=True);tf+=rt
    outputs=uncat(returned);targets=uncat(targets)
    combined=np.concatenate([outputs,targets],axis=2)
    bright=np.repeat(np.array([1.,1.,-1.]),N)
    def kernels(y):
        f=y.reshape(3*N,3*H);G=f[:,:H];Dp=f[:,H:2*H];T=f[:,2*H:]
        gg=G.conj().T@(bright[:,None]*G);dd=Dp.conj().T@(bright[:,None]*Dp)
        gd=G.conj().T@(bright[:,None]*Dp);target=T.conj().T@(bright[:,None]*T)
        A=gg+dd-target;B=gd
        sets={'all_degree4':[list(range(H))],
          'charge_preserving_all_q_plus':[[hs.index(0)],[hs.index(1)]],
          'charge_preserving_second_q_minus':[[hs.index(h) for h in [-2,0,2]],
                                               [hs.index(h) for h in [-1,1,3]]]}
        return {'Kgg':enc(gg),'Kdd':enc(dd),'Kgd':enc(gd),'Ktarget':enc(target),
          'A':enc(A),'B':enc(B),'mean_bounds':{name:bound(A,B,hs,bl) for name,bl in sets.items()}}
    result={'Z_physical_bright':kernels(combined)}
    for name,phase in [('Y_analysis',0.),('X_analysis',np.pi/2)]:
        y,ta,na=optical(combined,tf+175e-6,np.pi/2,False,True,85e3,w,g[0],D,axis_phase=phase)
        result[name]=kernels(y);result[name]['analysis_duration_s']=ta-(tf+175e-6)
        result[name]['analysis_rhs']=na
    return {'pulse':'smooth_BB1' if smooth else 'bare','N':N,'hs':hs,'etaIR':etaIR,
      'forward_control_time_s':t,'total_control_time_s':tf,'sync_wait_s':sync,
      'D_population_during_science':float(np.sum(abs(parked[2])**2)),
      'forward_rhs':nf,'return_rhs':nr,'observables':result,
      'readout':'mean=2*pBright-1; both S states bright; full optical analysis pulse',
      'phase_nuisance':'uniform arbitrary D phase z; fixed across optical phase cycle',
      'unpaid':['other Zeeman edges and measuredB','RF on actual apparatus','spectator modes/control noise',
       'phase-independent loaded instrument','finite science band/product prep/frozen motion','molecular signal/loss/full cycle']}

def main():
    start=time.perf_counter()
    reports=[run(False,False),run(True,True)]
    out={'status':'COMPLETE_FINITE_HISTORY_KERNEL_MODEL_NOT_PHYSICAL_QUERY','reports':reports,
      'wall_seconds':time.perf_counter()-start}
    (HERE/'HISTORY_KERNELS.json').write_text(json.dumps(out,indent=2)+'\n')
    summary={r['pulse']:{o:{s:{k:v for k,v in b.items() if k.endswith('upper')} for s,b in a['mean_bounds'].items()}
      for o,a in r['observables'].items()} for r in reports}
    print(json.dumps(summary|{'wall_seconds':out['wall_seconds']},indent=2))

if __name__=='__main__':main()
