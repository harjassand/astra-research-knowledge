import numpy as np
import cvxpy as cp
import json
from pathlib import Path

def frame(d):
    aa=[]
    for i in range(d):
        for j in range(i+1,d):
            a=np.zeros((d,d),complex); a[i,j]=a[j,i]=np.sqrt(d/2);aa.append(a)
            a=np.zeros((d,d),complex);a[i,j]=-1j*np.sqrt(d/2);a[j,i]=1j*np.sqrt(d/2);aa.append(a)
    for k in range(1,d):
        v=np.zeros(d);v[:k]=1;v[k]=-k
        aa.append(np.diag(v*np.sqrt(d/(k*(k+1)))))
    assert np.max(np.abs(np.array([[np.trace(a@b)/d for b in aa] for a in aa])-np.eye(d*d-1)))<1e-10
    return aa

def swap_outputs(d):
    s=np.zeros((d**3,d**3))
    for r in range(d):
        for a in range(d):
            for b in range(d):s[(r*d+b)*d+a,(r*d+a)*d+b]=1
    return s

def partials(omega,d):
    ra=cp.partial_trace(omega,[d,d,d],axis=2)
    rb=cp.partial_trace(omega,[d,d,d],axis=1)
    return [cp.partial_trace(ra,[d,d],axis=1),cp.partial_trace(ra,[d,d],axis=0),cp.partial_trace(rb,[d,d],axis=0)]

def setup(d):
    aa=frame(d);n=len(aa);eye=np.eye(d)
    omega=cp.Variable((d**3,d**3),hermitian=True)
    t=cp.bmat([[cp.reshape(cp.real(cp.trace(omega@np.kron(a.T,np.kron(b,eye)))),(1,1),order='C') for b in aa] for a in aa])
    wpar=cp.Parameter((d**3,d**3),hermitian=True)
    constraints=[omega>>0]+[m==eye/d for m in partials(omega,d)]
    sw=swap_outputs(d)
    constraints += [omega==sw@omega@sw.T,t==t.T,t>>0]
    broad=cp.Problem(cp.Maximize(cp.real(cp.trace(omega@wpar))-1),constraints)
    sym=[]
    for i in range(d):
        for j in range(i,d):
            v=np.zeros(d*d)
            if i==j:v[i*d+j]=1
            else:v[i*d+j]=v[j*d+i]=1/np.sqrt(2)
            sym.append(v)
    u=np.array(sym).T
    x=cp.Variable((len(sym),len(sym)),hermitian=True)
    sigma=u@x@u.T
    kpar=cp.Parameter((d*d,d*d),hermitian=True)
    moment=cp.Problem(cp.Maximize(cp.real(cp.trace(sigma@kpar))),[x>>0,cp.partial_trace(sigma,[d,d],axis=0)==eye/d,cp.partial_transpose(sigma,[d,d],axis=1)>>0])
    return aa,omega,t,wpar,broad,sigma,kpar,moment

def main():
    d=3;aa,omega,t,wpar,broad,sigma,kpar,moment=setup(d);n=len(aa)
    pair=[(np.kron(a.T,np.kron(b,np.eye(d))+np.kron(np.eye(d),b)),np.kron(a,b)) for a in aa for b in aa]
    rng=np.random.default_rng(842017)
    cases=[]
    for rank in [8,2,3,4,5,6,7,8]:
        for attempt in range(2):
            if len(cases)==0:q=np.eye(n)/n
            else:
                v=rng.normal(size=(n,rank));q=v@v.T;q/=np.trace(q)
            w=sum(q.flat[i]*p[0] for i,p in enumerate(pair))
            k=sum(q.flat[i]*p[1] for i,p in enumerate(pair))
            wpar.value=w;kpar.value=k
            broad.solve(solver='SCS',eps=1e-6,max_iters=20000,warm_start=True)
            moment.solve(solver='SCS',eps=1e-6,max_iters=20000,warm_start=True)
            cr={'rank':rank,'attempt':attempt,'broadcaster_status':broad.status,'h1_upper_status':moment.status,'compatible_objective':float(broad.value),'bosonic_ppt_upper':float(moment.value),'candidate_gap':float(broad.value-moment.value),'q':q.tolist(),'phi_eigenvalues':np.linalg.eigvalsh((t.value+t.value.T)/2).tolist(),'omega_min_eigenvalue':float(np.linalg.eigvalsh(omega.value)[0])}
            cases.append(cr)
            print(json.dumps({a:cr[a] for a in ['rank','attempt','compatible_objective','bosonic_ppt_upper','candidate_gap','broadcaster_status']}),flush=True)
            if cr['candidate_gap']>1e-4:
                np.savez(Path(__file__).with_name('candidate.npz'),q=q,omega=omega.value,sigma=sigma.value,t=t.value)
                break
        else:continue
        break
    out=Path(__file__).with_name('qutrit_sdp_search.json');out.write_text(json.dumps({'dimension':d,'status':'FINITE_NUMERICAL_SCREEN_ONLY','cases':cases},indent=2)+'\n')

if __name__=='__main__':main()
