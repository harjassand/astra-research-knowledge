#!/usr/bin/env python3
"""Coordinate search in the physical SU(2)-covariant multi-qubit-memory class.

The first q carriers are stored exactly in q initialized memory qubits.
All subsequent maps M E -> M and the final decoder are covariant with respect
 to the ordinary tensor powers of the spin-half representation.
"""
from control_search import *
from functools import lru_cache

PAULI_Y=np.array([[0,-1j],[1j,0]])


def tensor_power(a,n):
    r=np.ones((1,1),dtype=complex)
    for _ in range(n):r=np.kron(r,a)
    return r


@lru_cache(None)
def schur_blocks(n):
    d=1<<n
    raising=np.zeros((d,d),dtype=complex)
    plus=np.array([[0,1],[0,0]],complex)
    for k in range(n):
        raising+=np.kron(np.kron(np.eye(1<<k),plus),np.eye(1<<(n-k-1)))
    lowering=raising.conj().T
    ans=[]
    for k in range(n//2+1):
        j=n/2-k;spin=int(2*j+1)
        ids=np.array([x for x in range(d) if x.bit_count()==k],dtype=int)
        upids=np.array([x for x in range(d) if x.bit_count()==k-1],dtype=int)
        kernel=la.null_space(raising[np.ix_(upids,ids)],rcond=1e-12)
        mult=kernel.shape[1]
        highs=np.zeros((d,mult),dtype=complex);highs[ids,:]=kernel
        cols=[]
        for a in range(mult):
            v=highs[:,a].copy();cols.append(v)
            mag=j
            for _ in range(spin-1):
                v=lowering@v/np.sqrt((j+mag)*(j-mag+1))
                mag-=1;cols.append(v)
        u=np.stack(cols,axis=1)
        assert la.norm(u.conj().T@u-np.eye(spin*mult))<1e-10
        ans.append((j,mult,spin,u))
    full=np.concatenate([x[3] for x in ans],axis=1)
    assert la.norm(full@full.conj().T-np.eye(d))<1e-10
    return tuple(ans)


class CovariantSDPSolver:
    def __init__(self,nin,nout,solver='SCS',tol=1e-8):
        self.d=1<<nin;self.o=1<<nout;self.solver=solver;self.tol=tol
        flip=np.kron(np.eye(self.o),tensor_power(PAULI_Y,nin))
        self.blocks=[(j,m,s,flip@u) for j,m,s,u in schur_blocks(nin+nout)]
        self.x=[cp.Variable((m,m),hermitian=True) for j,m,s,u in self.blocks]
        self.h=[cp.Parameter((m,m),hermitian=True) for j,m,s,u in self.blocks]
        expr=0
        for x,(_,m,s,u) in zip(self.x,self.blocks):expr+=u@cp.kron(x,np.eye(s))@u.conj().T
        marginal=sum(expr[i*self.d:(i+1)*self.d,i*self.d:(i+1)*self.d] for i in range(self.o))
        # The marginal is already in the input-conjugate commutant.  Impose only
        # its independent real block entries; redundant full-matrix equalities
        # cause poor conditioning in otherwise tiny SDPs.
        constraints=[x>>0 for x in self.x]
        input_flip=tensor_power(PAULI_Y,nin)
        for _,mult,spin,basis in schur_blocks(nin):
            v=input_flip@basis
            z=v.conj().T@marginal@v
            for a in range(mult):
                for b in range(a,mult):
                    entry=sum(z[a*spin+k,b*spin+k] for k in range(spin))/spin
                    constraints.append(cp.real(entry)==(1. if a==b else 0.))
                    if a!=b:constraints.append(cp.imag(entry)==0.)
        self.problem=cp.Problem(cp.Maximize(sum(cp.real(cp.trace(h@x)) for h,x in zip(self.h,self.x))),constraints)
        self.calls=0;self.seconds=0.;self.statuses={}
    def project(self,j):
        total=np.zeros_like(j,dtype=complex)
        for _,m,s,u in self.blocks:
            x=np.einsum('aibi->ab',(u.conj().T@j@u).reshape(m,s,m,s))/s
            total+=u@np.kron(x,np.eye(s))@u.conj().T
        return herm(total)
    def solve(self,h,old=None):
        marginal=choi_marginal(h,self.o,self.d)/self.o
        centered=herm(h-np.kron(np.eye(self.o),marginal))
        projected=self.project(centered)
        scale=la.norm(projected,'fro')
        if scale<2e-14 and old is not None:return old,dict(status='flat',gain=0.,scale=scale)
        for par,x,(_,m,s,u) in zip(self.h,self.x,self.blocks):
            par.value=herm(np.einsum('aibi->ab',(u.conj().T@centered@u).reshape(m,s,m,s)))/max(scale,1e-14)
            if old is not None:
                x.value=herm(np.einsum('aibi->ab',(u.conj().T@old@u).reshape(m,s,m,s))/s)
        t=time.perf_counter()
        if self.solver=='CLARABEL':self.problem.solve(solver='CLARABEL',warm_start=True,tol_gap_abs=self.tol,tol_gap_rel=self.tol,tol_feas=self.tol,max_iter=200)
        else:self.problem.solve(solver='SCS',warm_start=True,eps=self.tol,max_iters=5000)
        elapsed=time.perf_counter()-t;self.calls+=1;self.seconds+=elapsed
        self.statuses[self.problem.status]=self.statuses.get(self.problem.status,0)+1
        if any(x.value is None for x in self.x):raise RuntimeError(self.problem.status)
        raw=sum(u@np.kron(x.value,np.eye(s))@u.conj().T for x,(_,m,s,u) in zip(self.x,self.blocks))
        raw=herm(raw)
        raw_min=float(la.eigvalsh(raw)[0]);raw_tp=float(la.norm(choi_marginal(raw,self.o,self.d)-np.eye(self.d)))
        candidate=cptp_repair(raw,self.o,self.d)
        gain=None if old is None else trace_pair(h,candidate-old)
        rejected=gain is not None and gain < -2e-11
        if rejected:candidate=old
        return candidate,dict(status=self.problem.status,gain=gain,scale=float(scale),raw_min_eigenvalue=raw_min,raw_tp_residual=raw_tp,seconds=elapsed,rejected=rejected)


def symmetric_initial_policy(q,n,kind,rng,theta):
    m=1<<q
    prefix=[swap_register_map(m,j) for j in range(min(q,n))]
    if n<=q:return prefix
    if kind=='prefix':return prefix+[identity_memory(m) for _ in range(n-q)]
    if kind.startswith('partial'):
        return prefix+initial_policy(m,n-q,kind,rng,theta)
    if kind.startswith('random'):
        strength=float(kind.split(':')[1]) if ':' in kind else theta**2
        pairs=[]
        for a in range(q+1):
            for b in range(a+1,q+1):
                order=list(range(q+1));order[a],order[b]=order[b],order[a]
                pairs.append(permutation_unitary([2]*(q+1),order))
        if len(pairs)>1:
            pairs.append(1j*(pairs[0]@pairs[-1]-pairs[-1]@pairs[0]))
        suffix=[]
        for _ in range(n-q):
            h=sum(rng.normal()*p for p in pairs)
            h=herm(h);h*=strength/max(la.norm(h,2),1e-12)
            suffix.append(unitary_memory_map(la.expm(1j*h),m))
        return prefix+suffix
    raise ValueError(kind)


def optimize_covariant(q,theta,n,sweeps=16,init='prefix',seed=0,solver='CLARABEL',tol=1e-8,stop=1e-8,verbose=True,resume=None):
    m=1<<q;rng=np.random.default_rng(seed)
    model=CollisionModel(m,theta)
    policy=symmetric_initial_policy(q,n,init,rng,theta)
    if resume:
        old=np.load(resume)
        oldpolicy=list(old['policy'])
        if oldpolicy[0].shape !=policy[0].shape:raise ValueError('resume memory mismatch')
        policy=oldpolicy[:n]+[identity_memory(m) for _ in range(max(0,n-len(oldpolicy)))]
    chan_solver=CovariantSDPSolver(q+1,q,solver,tol)
    dec_solver=CovariantSDPSolver(q,1,solver,tol)
    final=model.forward(policy)[-1]
    decoder,fe,_=model.terminal_optimize(final,dec_solver)
    history=[dict(sweep=-1,direction='initial',fidelity=fe,error=1-fe)]
    allstats=[];t0=time.perf_counter()
    if verbose:print(json.dumps(dict(q=q,theta=theta,n=n,init=init,seed=seed,**history[-1])),flush=True)
    for sweep in range(sweeps):
        old_fe=fe;localstats=[]
        if sweep%2==0:
            direction='forward'
            bs=[None]*(n+1);bs[n]=model.terminal_cost(decoder)
            for k in reversed(range(q,n)):bs[k]=model.adjoint_step(bs[k+1],policy[k])
            rho=model.rho0
            for k in range(min(q,n)):rho=model.step(rho,policy[k])
            for k in range(q,n):
                x=model.source(rho);h=choi_cost(x,bs[k+1],m,2*m)
                policy[k],stats=chan_solver.solve(h,policy[k]);localstats.append(stats)
                rho=herm(apply_local(x,policy[k],m,2*m))
            final=rho
        else:
            direction='backward';rs=model.forward(policy);b=model.terminal_cost(decoder)
            for k in reversed(range(q,n)):
                h=choi_cost(model.source(rs[k]),b,m,2*m)
                policy[k],stats=chan_solver.solve(h,policy[k]);localstats.append(stats)
                b=model.adjoint_step(b,policy[k])
            final=model.forward(policy)[-1]
        decoder,fe,_=model.terminal_optimize(final,dec_solver,decoder)
        entry=dict(sweep=sweep,direction=direction,fidelity=fe,error=1-fe,gain=fe-old_fe,seconds=time.perf_counter()-t0,
                   min_local_gain=min((x.get('gain',0.) or 0.) for x in localstats) if localstats else 0.,rejected_updates=sum(x.get('rejected',False) for x in localstats))
        history.append(entry);allstats.extend(localstats)
        if verbose:print(json.dumps(dict(q=q,theta=theta,n=n,init=init,seed=seed,**entry)),flush=True)
        if fe<old_fe-5e-8:raise RuntimeError('Nonmonotone sweep')
        if sweep>=7 and fe-old_fe<stop and history[-2]['gain']<stop:break
    rs=model.forward(policy)
    result=dict(q=q,m=m,theta=theta,n=n,init=init,seed=seed,solver=solver,tol=tol,history=history,fidelity=fe,error=1-fe,
                passive_error=.75*(1-np.sin(theta)**4)**n,global_lower_error=.75*(1-np.sqrt(1-(1-np.sin(theta)**4)**n)),
                policy_stats=policy_stats(policy,m),solver_calls=chan_solver.calls+dec_solver.calls,
                solver_seconds=chan_solver.seconds+dec_solver.seconds,solver_statuses=chan_solver.statuses,
                covariant_residual=max((float(la.norm(j-chan_solver.project(j))) for j in policy[q:]),default=0),
                final_state_min_eigenvalue=float(la.eigvalsh(rs[-1])[0]),final_state_trace=float(np.trace(rs[-1]).real),
                reference_marginal_residual=float(la.norm(np.einsum('asmbsm->ab',rs[-1].reshape(2,2,m,2,2,m))-np.eye(2)/2)))
    return result,policy,decoder,rs


def self_test():
    rng=np.random.default_rng(17)
    records=[]
    for q,n in [(1,3),(2,3)]:
        m=1<<q;model=CollisionModel(m,.7)
        policy=symmetric_initial_policy(q,n,'random:0.3',rng,.7)
        rho=model.forward(policy)[q]
        decoder,fe,_=model.terminal_optimize(rho,SDPSolver(m,2))
        cost=model.terminal_cost(decoder)
        x=model.source(rho);h=choi_cost(x,cost,m,2*m)
        dense,ds=SDPSolver(2*m,m).solve(h)
        cov_solver=CovariantSDPSolver(q+1,q)
        cov,cs=cov_solver.solve(h)
        dense_f=trace_pair(h,dense);cov_f=trace_pair(h,cov)
        assert abs(dense_f-cov_f)<2e-7,(q,dense_f,cov_f)
        assert la.norm(cov-cov_solver.project(cov))<1e-9
        records.append(dict(q=q,dense_optimum=dense_f,covariant_optimum=cov_f,blocks=[{'spin':j,'multiplicity':r} for j,r,s,u in cov_solver.blocks]))
    print(json.dumps(dict(status='passed',tests=records),indent=2),flush=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');p.add_argument('--q',type=int,default=2);p.add_argument('--theta',type=float,default=.7);p.add_argument('--n',type=int,default=12);p.add_argument('--sweeps',type=int,default=16);p.add_argument('--init',default='prefix');p.add_argument('--seed',type=int,default=0);p.add_argument('--solver',default='CLARABEL');p.add_argument('--tol',type=float,default=1e-8);p.add_argument('--stop',type=float,default=1e-8);p.add_argument('--out');p.add_argument('--resume')
    a=p.parse_args()
    if a.self_test:self_test();return
    result,policy,decoder,states=optimize_covariant(a.q,a.theta,a.n,a.sweeps,a.init,a.seed,a.solver,a.tol,a.stop,resume=a.resume)
    if a.out:
        stem=Path(a.out);stem.parent.mkdir(parents=True,exist_ok=True)
        Path(str(stem)+'.json').write_text(json.dumps(result,indent=2))
        np.savez_compressed(str(stem)+'.npz',policy=np.array(policy),decoder=decoder,states=np.array(states))
    print(json.dumps({'result':result},indent=2),flush=True)

if __name__=='__main__':main()
