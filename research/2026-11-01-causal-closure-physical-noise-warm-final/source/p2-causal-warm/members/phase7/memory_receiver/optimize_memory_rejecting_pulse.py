"""Same physical force cap, but optimize the signal actually used by the receiver.

Finite cosine basis, numerical feasible candidates only. The receiver discards
the union of both conditional initial-mode response spaces. No global hardware
optimality claim. This optimization gives conventional control the new receiver.
"""
from pathlib import Path
import json,sys,argparse
import numpy as np
from scipy.linalg import eigh,svd
from scipy.optimize import minimize,minimize_scalar
from scipy.special import ndtri,ndtr
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'new_research'/'conventional_routes'))
from optimize_finite_mediator import matrices
from project_initial_memory import responses,simpson_weights,project

def optimize(T,n,cap=3.,q=.001,initial=None):
    m=dict(T=T,g=1.,Gamma=4.,chi=2.,kb=1e-4,kc=1e-4,eta=.5,cap=cap,q=q)
    t=np.linspace(0,T,4001);w=simpson_weights(t);f=matrices(n,t,m)
    H=responses(m,t);Q,ss,_=svd(np.sqrt(w)[:,None]*H,full_matrices=False)
    rank=int(np.sum(ss>ss[0]*1e-12));Q=Q[:,:rank]
    aw=np.sqrt(w)[:,None]*f['A'];ap=aw-Q@(Q.conj().T@aw)
    QE=(ap.conj().T@ap).real;QB=f['B'].T@(w[:,None]*f['B'])
    d,v=eigh(QE)
    if d[0]<=0:raise ValueError('Receiver signal normalization lost positive definiteness')
    W=v@np.diag(1/np.sqrt(d));Hb=W.T@QB@W
    _,evec=eigh(Hb);N=ndtri(q)**2/(4*m['eta'])
    ts=np.linspace(0,T,801);fs=matrices(n,ts,m)
    J=np.vstack([fs['u'],fs['w']])@W*np.sqrt(N)
    effective_cap=cap-1e-4
    con=[dict(type='eq',fun=lambda y:float(y@y-1),jac=lambda y:2*y),
         dict(type='ineq',fun=lambda y:effective_cap-J@y,jac=lambda y:-J),
         dict(type='ineq',fun=lambda y:effective_cap+J@y,jac=lambda y:J)]
    starts=[evec[:,0]]
    c=np.r_[1.,np.zeros(n)];y=np.linalg.solve(W,c);starts.append(y/np.linalg.norm(y))
    if initial is not None:
        c=np.zeros(n+1);c[:min(n+1,len(initial))]=initial[:n+1]
        y=np.linalg.solve(W,c);starts.insert(0,y/np.linalg.norm(y))
    rng=np.random.default_rng(703)
    starts.append((evec[:,0]+.1*rng.normal(size=n+1)))
    starts[-1]/=np.linalg.norm(starts[-1])
    history=[];best=None
    for y0 in starts:
        opt=minimize(lambda y:float(y@Hb@y),y0,jac=lambda y:2*Hb@y,
                     method='SLSQP',constraints=con,
                     options={'ftol':2e-11,'maxiter':500,'disp':False})
        violation=float(max(0,np.max(abs(J@opt.x))-effective_cap))
        eq=float(abs(opt.x@opt.x-1));ok=violation<2e-6 and eq<2e-7
        history.append(dict(success=bool(opt.success),feasible=ok,ratio=float(opt.fun),
                            max_force_violation=violation,norm_error=eq,
                            message=str(opt.message),iterations=opt.nit))
        if ok and (best is None or opt.fun<best.fun):best=opt
    result=dict(model=m,order=n,response_rank=rank,normalization_condition=float(d[-1]/d[0]),attempts=history)
    if best is None:
        result['feasible']=False
        result['scope']='No feasible point found by this finite numerical search; not an impossibility certificate.'
        return result
    refinements=[]
    for refinement in range(4):
        c=np.sqrt(N)*W@best.x
        tr=np.linspace(0,T,24001);fr=matrices(n,tr,m)
        new_rows=[];extrema=[]
        for name in ('u','w'):
            values=fr[name]@c
            ids=np.flatnonzero((abs(values[1:-1])>=abs(values[:-2])) &
                              (abs(values[1:-1])>=abs(values[2:])))+1
            for j in ids:
                optpeak=minimize_scalar(lambda tt:-abs((matrices(n,np.array([tt]),m)[name]@c).item()),
                                        bounds=(tr[j-1],tr[j+1]),method='bounded',
                                        options={'xatol':1e-12})
                peak=-optpeak.fun;extrema.append(dict(control=name,time=float(optpeak.x),peak=float(peak)))
                if peak>effective_cap+1e-8:
                    new_rows.append(matrices(n,np.array([optpeak.x]),m)[name][0]@W*np.sqrt(N))
        refinements.append(dict(max_peak=max(x['peak'] for x in extrema),added=len(new_rows)))
        if not new_rows:break
        J=np.vstack([J,np.array(new_rows)])
        best=minimize(lambda y:float(y@Hb@y),best.x,jac=lambda y:2*Hb@y,
                      method='SLSQP',constraints=con,
                      options={'ftol':1e-12,'maxiter':800,'disp':False})
    c=np.sqrt(N)*W@best.x
    td=np.linspace(0,T,24001);wd=simpson_weights(td);fd=matrices(n,td,m)
    physical={k:v@c for k,v in fd.items()}
    projected,_,_=project(m,td,physical['A'],'joint_optimized')
    peak={k:float(max(abs(physical[k]))) for k in ('u','w')}
    result.update(dict(feasible=max(peak.values())<=cap+2e-6,coefficients=c.tolist(),
                       extrema_refinements=refinements,
                       projection=projected,IB=float(wd@physical['B']**2),
                       peak_u=peak['u'],peak_w=peak['w'],
                       action_u=float(wd@physical['u']**2),action_w=float(wd@physical['w']**2),
                       exposure_b=float(wd@(physical['U']**2+physical['B']**2)),
                       exposure_c=float(wd@(physical['V']**2+physical['B']**2)),
                       peak_b=float(max(physical['U']**2+physical['B']**2)),
                       peak_c=float(max(physical['V']**2+physical['B']**2)),
                       peak_m=float(max(physical['A']**2)/m['Gamma']),
                       base_cold_pZ=float(-np.expm1(-2*(m['kb']+m['kc'])*(wd@physical['B']**2))/2)))
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--times',default='8,10,12,16');p.add_argument('--orders',default='6,10,14')
    args=p.parse_args();rows=[]
    for T in map(float,args.times.split(',')):
        initial=None
        for n in map(int,args.orders.split(',')):
            row=optimize(T,n,initial=initial);rows.append(row)
            if row['feasible']:initial=row['coefficients']
            print(T,n,'feasible',row['feasible'],
                  ('IB '+str(row['IB'])+' N '+str(row['projection']['N'])) if row['feasible'] else '',flush=True)
            (HERE/'memory_rejecting_optimization_results.json').write_text(json.dumps(dict(rows=rows),indent=2)+'\n')

if __name__=='__main__':main()
