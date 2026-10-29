"""Competent finite-pulse output-error fitting with analytic sensitivities.

The same linear calibration and actual reconstructed endpoint records are
given to both routes. Two starts are declared in advance, both retained.
Only the first12 experimental records train; all140 are forecast controls.
No truth tensor is used by fitting.
"""
from pathlib import Path
import json,time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm
from energy_experiment import gauge_error,SyntheticPort


def generators(n):
    out=[]
    for i in range(1,n):
        for j in range(i+1,n):
            a=np.zeros((n,n));a[i,j]=1;a[j,i]=-1;out.append(a)
    return np.array(out)


class Forward:
    def __init__(self,lam,g=.35):self.lam=lam;self.g=g;self.nfev=0;self.solves=0
    def solve(self,Q,X,tau,sens=False):
        n,m=X.shape;E=generators(n);p=len(E)
        state=np.zeros((1+p if sens else 1,n,m),complex);state[0]=X
        def rhs(_,flat):
            S=flat.reshape(state.shape);xx=S[0];z=Q@xx;aa=np.abs(z)**2;zz=z*z;N=aa*z
            dy=np.empty_like(S);dy[0]=-1j*(self.lam[:,None]*xx+self.g*(Q.T@N))*tau
            if sens:
                qs=np.einsum('ab,pbm->pam',Q,S[1:])
                ez=np.einsum('pab,bm->pam',E,z);en=np.einsum('pab,bm->pam',E,N)
                inside=2*aa[None]*(qs+ez)+zz[None]*(qs+ez).conj()-en
                ds=self.lam[None,:,None]*S[1:]+self.g*np.einsum('ab,pbm->pam',Q.T,inside)
                dy[1:]=-1j*ds*tau[None,None,:]
            return dy.ravel()
        sol=solve_ivp(rhs,(0,1),state.ravel(),method='DOP853',rtol=5e-11,atol=5e-13)
        assert sol.success
        self.solves+=1;self.nfev+=sol.nfev
        out=sol.y[:,-1].reshape(state.shape)
        if not sens:return out[0]
        # Complex Jacobian columns in the same C-order as the state residual.
        J=out[1:].reshape(p,n*m).T
        return out[0],np.concatenate([J.real,J.imag],axis=0)


def realvec(z):return np.concatenate([z.ravel().real,z.ravel().imag])


def fit(startQ,X,Y,tau,lam):
    f=Forward(lam);Q=startQ.copy();E=generators(len(lam));history=[]
    begin=time.perf_counter();status='ITERATION_CAP'
    for iteration in range(40):
        pred,J=f.solve(Q,X,tau,True);res=realvec(pred-Y);loss=float(res@res)
        step=np.linalg.lstsq(J,-res,rcond=None)[0]
        if np.linalg.norm(step)>1.5:step*=1.5/np.linalg.norm(step)
        tangent=np.einsum('p,pab->ab',step,E);accepted=False
        for k in range(9):
            scale=2.**(-k);trial=expm(scale*tangent)@Q
            r=realvec(f.solve(trial,X,tau)-Y);newloss=float(r@r)
            if newloss<loss:
                Q=trial;accepted=True;break
        history.append({'iteration':iteration,'loss':loss,'step_norm':float(np.linalg.norm(step)),
                        'accepted':accepted,'line_search_halvings':k})
        if np.linalg.norm(step)<1e-9:
            status='SMALL_STEP';break
        if not accepted:
            status='LINE_SEARCH_STOP';break
    return Q,{'status':status,'history':history,'seconds':time.perf_counter()-begin,
              'ODE_solves':f.solves,'ODE_evaluations':f.nfev,
              'training_complex_residual_norm':float(np.linalg.norm(f.solve(Q,X,tau)-Y))}


def main():
    root=Path(__file__).parent;d=np.load(root/'DATA.npz');lam=d['lam'];c=d['c'];n=len(c)
    u=np.eye(n)[0]-c;B=np.eye(n)-2*np.outer(u,u)/(u@u)
    E=generators(n);rng=np.random.default_rng(202610299702)
    starts=[B,expm(np.einsum('p,pab->ab',rng.normal(size=len(E)),E))@B]
    X,Y,tau=d['X'],d['Y'],d['taus'];training=12;rows=[];oracle=SyntheticPort()
    begin=time.perf_counter()
    for j,Q0 in enumerate(starts):
        Q,row=fit(Q0,X[:,:training],Y[:,:training],tau[:training],lam)
        forward=Forward(lam);tick=time.perf_counter();prediction=forward.solve(Q,X,tau)
        row.update({'start':j,'training_experiments':training,'all_available_experiments':X.shape[1],
                    'all_record_forecast_residual_norm':float(np.linalg.norm(prediction-Y)),
                    'forecast_seconds':time.perf_counter()-tick,
                    'reconstruction':gauge_error(Q,np.diag(lam),oracle)})
        rows.append(row)
        print(json.dumps({k:v for k,v in row.items() if k!='history'}),flush=True)
    result={'status':'TWO_PREDECLARED_ORDINARY_FITS_BOTH_RETAINED',
            'mechanism':'Riemannian Gauss--Newton with analytic forward sensitivities',
            'source_data':'same finite-pulse port records/calibration as energy route',
            'rows':rows,'seconds_total':time.perf_counter()-begin,
            'global_convergence_guarantee':False,'physical_or_all_method_advantage':False}
    (root/'ORDINARY_FIT.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
