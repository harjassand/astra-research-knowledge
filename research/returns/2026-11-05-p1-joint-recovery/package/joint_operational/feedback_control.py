#!/usr/bin/env python3
"""Exact finite classical-state feedback control with m-dimensional memory.

Policy[k,x,y] is the Choi matrix of a CP map M E -> M for transition x->y.
For each time k and current classical label x the sum over y is trace-preserving.
The average joint RSM state is propagated separately for each free classical label.
"""
from control_search import *


class InstrumentSolver:
    def __init__(self,d,o,C,solver='CLARABEL',tol=1e-8):
        self.d=d;self.o=o;self.C=C;self.solver=solver;self.tol=tol;n=d*o
        self.j=[cp.Variable((n,n),hermitian=True) for _ in range(C)]
        self.h=[cp.Parameter((n,n),hermitian=True) for _ in range(C)]
        marginal=sum(j[a*d:(a+1)*d,a*d:(a+1)*d] for j in self.j for a in range(o))
        self.problem=cp.Problem(cp.Maximize(sum(cp.real(cp.trace(h@j)) for h,j in zip(self.h,self.j))),[j>>0 for j in self.j]+[marginal==np.eye(d)])
        self.calls=0;self.seconds=0.;self.statuses={}
    def solve(self,cost,old):
        common=sum(choi_marginal(h,self.o,self.d) for h in cost)/(self.o*self.C)
        centered=[herm(h-np.kron(np.eye(self.o),common)) for h in cost]
        scale=np.sqrt(sum(la.norm(h,'fro')**2 for h in centered))
        if scale<2e-14:return old,dict(status='flat',gain=0.,scale=float(scale))
        for p,h,j,o in zip(self.h,centered,self.j,old):p.value=h/scale;j.value=o
        start=time.perf_counter()
        if self.solver=='CLARABEL':self.problem.solve(solver='CLARABEL',warm_start=True,tol_gap_abs=self.tol,tol_gap_rel=self.tol,tol_feas=self.tol,max_iter=200)
        else:self.problem.solve(solver='SCS',warm_start=True,eps=self.tol,max_iters=5000)
        elapsed=time.perf_counter()-start;self.seconds+=elapsed;self.calls+=1
        self.statuses[self.problem.status]=self.statuses.get(self.problem.status,0)+1
        if any(j.value is None for j in self.j):raise RuntimeError(self.problem.status)
        positive=[];rawmin=[]
        for j in self.j:
            w,v=la.eigh(herm(j.value));rawmin.append(float(w[0]));positive.append(herm((v*np.maximum(w,0))@v.conj().T))
        a=herm(sum(choi_marginal(j,self.o,self.d) for j in positive));w,v=la.eigh(a)
        if min(w)<1e-12:raise RuntimeError('Singular instrument TP marginal')
        r=(v/np.sqrt(w))@v.conj().T;big=np.kron(np.eye(self.o),r)
        candidate=[herm(big@j@big) for j in positive]
        gain=sum(trace_pair(h,j-o) for h,j,o in zip(cost,candidate,old));rejected=gain < -2e-11
        if rejected:candidate=old
        return candidate,dict(status=self.problem.status,gain=gain,scale=float(scale),seconds=elapsed,rejected=rejected,raw_min_eigenvalue=min(rawmin))


def initial_feedback_policy(m,C,n,kind,seed):
    rng=np.random.default_rng(seed);q=int(round(np.log2(m)));answer=[]
    strength=float(kind.split(':')[1]) if ':' in kind else .2
    for k in range(n):
        maps=[]
        for x in range(C):
            if k<q:
                order=list(range(q+1));order[k],order[-1]=order[-1],order[k]
                u=permutation_unitary([2]*(q+1),order)
            elif kind=='prefix':u=np.eye(2*m)
            else:
                a=herm(rng.normal(size=(2*m,2*m))+1j*rng.normal(size=(2*m,2*m)));a*=strength/max(la.norm(a,2),1e-12)
                u=la.expm(1j*a)
            ks=u.reshape(m,2,2*m)
            row=[np.zeros((2*m*m,2*m*m),complex) for _ in range(C)]
            for e in range(2):
                y=(2*x+e)%C;v=ks[:,e,:].reshape(-1);row[y]+=np.outer(v,v.conj())
            maps.append(row)
        answer.append(maps)
    return np.array(answer)


def default_decoder(m):
    rest=m//2
    return choi_from_kraus([np.kron(np.eye(2),np.eye(rest)[e:e+1]) for e in range(rest)])


def optimize_feedback(m,C,theta,n,sweeps=10,init='random:0.2',seed=0,solver='CLARABEL',tol=1e-8,stop=1e-8,verbose=True):
    model=CollisionModel(m,theta);D=4*m;policy=initial_feedback_policy(m,C,n,init,seed)
    ins=InstrumentSolver(2*m,m,C,solver,tol);dec_solver=SDPSolver(m,2,solver,tol)
    def advance(rhos,maps):
        xs=[model.source(r) for r in rhos]
        return np.array([herm(sum(apply_local(xs[x],maps[x,y],m,2*m) for x in range(C))) for y in range(C)])
    def forward():
        rho=np.zeros((C,D,D),complex);rho[0]=model.rho0;states=[rho]
        for maps in policy:states.append(advance(states[-1],maps))
        return states
    def backwards(bs,maps):
        return np.array([herm(model.source_adjoint(sum(adjoint_local(bs[y],maps[x,y],m,2*m) for y in range(C)))) for x in range(C)])
    def terminal(rhos,old=None):
        if old is None:old=[default_decoder(m) for _ in range(C)]
        out=[];fe=0.
        for x in range(C):
            d,f,stats=model.terminal_optimize(rhos[x],dec_solver,old[x]);out.append(d);fe+=f
        return out,fe
    states=forward();decoders,fe=terminal(states[-1]);start=time.perf_counter();allstats=[]
    history=[dict(sweep=-1,direction='initial',fidelity=fe,error=1-fe)]
    if verbose:print(json.dumps(dict(m=m,C=C,theta=theta,n=n,init=init,**history[-1])),flush=True)
    for sweep in range(sweeps):
        old_fe=fe;local=[]
        if sweep%2==0:
            direction='forward';bs=[None]*(n+1);bs[n]=np.array([model.terminal_cost(d) for d in decoders])
            for k in reversed(range(n)):bs[k]=backwards(bs[k+1],policy[k])
            rhos=np.zeros((C,D,D),complex);rhos[0]=model.rho0
            for k in range(n):
                inputs=[model.source(rho) for rho in rhos]
                for x in range(C):
                    cost=[choi_cost(inputs[x],bs[k+1][y],m,2*m) for y in range(C)]
                    policy[k,x],st=ins.solve(cost,policy[k,x]);local.append(st)
                rhos=np.array([herm(sum(apply_local(inputs[x],policy[k,x,y],m,2*m) for x in range(C))) for y in range(C)])
            final=rhos
        else:
            direction='backward';states=forward();bs=np.array([model.terminal_cost(d) for d in decoders])
            for k in reversed(range(n)):
                for x in range(C):
                    inp=model.source(states[k][x]);cost=[choi_cost(inp,bs[y],m,2*m) for y in range(C)]
                    policy[k,x],st=ins.solve(cost,policy[k,x]);local.append(st)
                bs=backwards(bs,policy[k])
            final=forward()[-1]
        decoders,fe=terminal(final,decoders)
        entry=dict(sweep=sweep,direction=direction,fidelity=fe,error=1-fe,gain=fe-old_fe,seconds=time.perf_counter()-start,
                   min_local_gain=min((x.get('gain',0.) or 0.) for x in local),rejected_updates=sum(x.get('rejected',False) for x in local))
        history.append(entry);allstats.extend(local)
        if verbose:print(json.dumps(dict(m=m,C=C,theta=theta,n=n,init=init,**entry)),flush=True)
        if fe<old_fe-1e-7:raise RuntimeError('Nonmonotone sweep')
        if sweep>=7 and fe-old_fe<stop and history[-2]['gain']<stop:break
    states=forward();margins=[];mins=[]
    for maps in policy:
        for row in maps:
            margins.append(la.norm(sum(choi_marginal(j,m,2*m) for j in row)-np.eye(2*m)))
            mins.extend(la.eigvalsh(herm(j))[0] for j in row)
    avg=sum(states[-1]);rmargin=np.einsum('asmbsm->ab',avg.reshape(2,2,m,2,2,m))
    result=dict(m=m,C=C,theta=theta,n=n,init=init,seed=seed,history=history,fidelity=fe,error=1-fe,
                passive_error=.75*(1-np.sin(theta)**4)**n,maximum_tp_residual=float(max(margins)),minimum_choi_eigenvalue=float(min(mins)),
                final_label_probabilities=[float(np.trace(r).real) for r in states[-1]],reference_marginal_residual=float(la.norm(rmargin-np.eye(2)/2)),
                solver_calls=ins.calls+dec_solver.calls,solver_seconds=ins.seconds+dec_solver.seconds,solver_statuses=ins.statuses)
    return result,policy,decoders,states


def main():
    p=argparse.ArgumentParser();p.add_argument('--m',type=int,default=2);p.add_argument('--C',type=int,default=2);p.add_argument('--theta',type=float,default=.7);p.add_argument('--n',type=int,default=12);p.add_argument('--sweeps',type=int,default=12);p.add_argument('--init',default='random:0.2');p.add_argument('--seed',type=int,default=0);p.add_argument('--solver',default='CLARABEL');p.add_argument('--tol',type=float,default=1e-8);p.add_argument('--out')
    a=p.parse_args();result,policy,decoders,states=optimize_feedback(a.m,a.C,a.theta,a.n,a.sweeps,a.init,a.seed,a.solver,a.tol)
    if a.out:
        stem=Path(a.out);stem.parent.mkdir(parents=True,exist_ok=True);Path(str(stem)+'.json').write_text(json.dumps(result,indent=2))
        np.savez_compressed(str(stem)+'.npz',policy=policy,decoders=np.array(decoders),states=np.array(states))
    print(json.dumps({'result':result},indent=2),flush=True)

if __name__=='__main__':main()
