"""Count-only positive predictive gauge certificate. No latent plant access."""
import itertools
import json
import math
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent

class Counts:
    def __init__(self, path):
        self.data = json.loads(Path(path).read_text())
        self.tables = {tuple(t['actions']):t for t in self.data['tables']}
        self.w = self.data['hoeffding_width_rational'][0]/self.data['hoeffding_width_rational'][1]
    def probability(self, actions, requirements):
        t = self.tables[tuple(actions)]
        total = sum(c for bits,c in t['counts'].items()
                    if all(int(bits[i])==o for i,o in requirements.items()))
        return total/t['shots']
    def matrices(self):
        h=np.ones((2,2)); dh=np.zeros((2,2)); hz={}; dz={}
        for j,prep in enumerate([(),(0,)]):
            h[1,j] = self.probability(prep+(1,), {len(prep):1})
            dh[1,j]=self.w
        for a,o in itertools.product(range(2),repeat=2):
            z=(a,o); hz[z]=np.zeros((2,2)); dz[z]=np.full((2,2),self.w)
            for j,prep in enumerate([(),(0,)]):
                hz[z][0,j]=self.probability(prep+(a,),{len(prep):o})
                hz[z][1,j]=self.probability(prep+(a,1),{len(prep):o,len(prep)+1:1})
        return h,dh,hz,dz

def simplex_projection(v):
    u=np.sort(v)[::-1]
    rho=np.nonzero(u*np.arange(1,len(u)+1) > np.cumsum(u)-1)[0][-1]
    theta=(u[:rho+1].sum()-1)/(rho+1)
    return np.maximum(v-theta,0)

def box_simplex_tv(p, lower, upper):
    """Exact support-function formula, evaluated in float here and rationally later."""
    best=0.
    for mask in itertools.product([False,True],repeat=len(p)):
        mask=np.array(mask)
        max_mass=min(upper[mask].sum(),1-lower[~mask].sum())
        best=max(best,float(max_mass-p[mask].sum()))
    return best

def certify_gauge(h,dh,hz,dz,s):
    S=np.array([[1+s,-s],[-s,1+s]])
    V=h@S; dV=dh@abs(S); U=np.linalg.inv(V)
    A=abs(U)@dV
    if max(abs(np.linalg.eigvals(A)))>=1:
        return {'s':s,'status':'UNKNOWN_INVERSE'}
    M=np.linalg.solve(np.eye(2)-A,abs(U))
    raw={z:U@v@S for z,v in hz.items()}
    errors={z:M@(dz[z]@abs(S)+dV@abs(raw[z])) for z in raw}
    margin=min(float(np.min(raw[z]-errors[z])) for z in raw)
    c0=np.linalg.solve(S,np.array([1.,0.]))
    result={'s':s,'status':'PASS' if margin>=0 and c0.min()>=0 else 'UNKNOWN_POSITIVITY',
            'positive_margin':margin,'inverse_radius':float(max(abs(np.linalg.eigvals(A)))),
            'initial':c0.tolist()}
    if result['status']!='PASS': return result
    fit={z:raw[z].copy() for z in raw}
    t=0.; loose=0.
    for a,j in itertools.product(range(2),repeat=2):
        p=np.concatenate([raw[a,o][:,j] for o in range(2)])
        pfit=simplex_projection(p)
        lower=np.concatenate([raw[a,o][:,j]-errors[a,o][:,j] for o in range(2)])
        upper=np.concatenate([raw[a,o][:,j]+errors[a,o][:,j] for o in range(2)])
        lower=np.maximum(lower,0); upper=np.minimum(upper,1)
        assert lower.sum()<=1+1e-10 and upper.sum()>=1-1e-10
        t=max(t,box_simplex_tv(pfit,lower,upper))
        loose=max(loose,0.5*np.maximum(abs(pfit-lower),abs(pfit-upper)).sum())
        for o in range(2): fit[a,o][:,j]=pfit[2*o:2*o+2]
    result.update(local_tv=t,loose_local_tv=loose,
                  W={str(z):v.tolist() for z,v in fit.items()},
                  raw={str(z):v.tolist() for z,v in raw.items()},
                  entry_errors={str(z):v.tolist() for z,v in errors.items()},
                  virtual_test_vertices=V.tolist(),S=S.tolist())
    return result

def frozen_spectral_bound(h,dh,hz,dz):
    U=np.linalg.inv(h); Jhat=np.linalg.norm(U,np.inf); dH=np.linalg.norm(dh,np.inf)
    nu=Jhat*dH; Jbar=Jhat/(1-nu)
    khat=max(np.linalg.norm(U@np.array(s),1) for s in itertools.product([-1,1],repeat=2))
    kbar=khat+2*Jbar*dH*Jhat
    errors={z:(np.linalg.norm(dz[z],np.inf)+np.linalg.norm(v@U,np.inf)*dH)*Jbar
            for z,v in hz.items()}
    e=kbar*max(sum(errors[a,o] for o in range(2)) for a in range(2))
    return dict(Jhat=Jhat,nu=nu,Jbar=Jbar,kappa_bound=kbar,joint_error=e,
                per_branch={str(z):v for z,v in errors.items()})

def main():
    oracle=Counts(ROOT/'counts.json'); h,dh,hz,dz=oracle.matrices()
    candidates=[certify_gauge(h,dh,hz,dz,s) for s in [0.,0.125,0.25,0.375,0.5,0.75,1.]]
    passing=[c for c in candidates if c['status']=='PASS']
    best=min(passing,key=lambda x:x['local_tv']) if passing else None
    n=min(t['shots'] for t in oracle.data['tables'])
    alpha=2*oracle.data['confidence_pool_K']*math.exp(-2*n*oracle.w**2)
    out={'confidence_failure_upper':alpha,'resets':oracle.data['resets'],
         'native_interventions':oracle.data['native_interventions'],
         'H':h.tolist(),'H_width':dh.tolist(),
         'spectral':frozen_spectral_bound(h,dh,hz,dz),'candidates':candidates,'selected':best}
    if best:
        t=best['local_tv']; delta=.4; gamma=1-delta
        out['reuse']={'abort_probability':delta,'one_macro_tv':gamma*t/(delta+gamma*t),
                      'two_macro_tv':1-(delta/(delta+gamma*t))**2,
                      'ten_native_steps_tv':1-(1-t)**10}
    (ROOT/'certificate.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['confidence_failure_upper','spectral','reuse'] if k in out},indent=2))
    print('gauge candidates:',[(c['s'],c['status'],c.get('positive_margin'),c.get('local_tv')) for c in candidates])

if __name__=='__main__': main()
