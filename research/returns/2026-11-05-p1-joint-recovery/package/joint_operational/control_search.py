#!/usr/bin/env python3
"""Exact-density coordinate ascent over causal nonselective CPTP receivers.

Choi convention: J[o,a,p,b] = T(|a><b|)[o,p], output first.
The retained memory dimension is m.  Input at a node is M tensor E.
Only the requested initial state is used; no bath-purifier/source access.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
import argparse
import json
import time
from pathlib import Path
import numpy as np
import scipy.linalg as la
import cvxpy as cp
from threadpoolctl import threadpool_limits
threadpool_limits(limits=1)


def herm(x):
    return (x+x.conj().T)/2


def choi_from_kraus(ks):
    return sum(np.outer(k.reshape(-1), k.reshape(-1).conj()) for k in ks)


def choi_marginal(j, out_dim, in_dim):
    return np.einsum('aiaj->ij', j.reshape(out_dim,in_dim,out_dim,in_dim))


def cptp_repair(j, out_dim, in_dim):
    w,v=la.eigh(herm(j))
    j=(v*np.maximum(w,0))@v.conj().T
    a=herm(choi_marginal(j,out_dim,in_dim))
    w,v=la.eigh(a)
    if np.min(w)<1e-12:
        # This should never be needed for a sufficiently accurate TP solve.
        j += 1e-10*np.eye(out_dim*in_dim)/out_dim
        a=herm(choi_marginal(j,out_dim,in_dim))
        w,v=la.eigh(a)
    r=(v*(1/np.sqrt(w)))@v.conj().T
    # J -> (I_out tensor r) J (I_out tensor r); trace-out becomes r a r.
    big=np.kron(np.eye(out_dim),r)
    return herm(big@j@big)


def apply_local(x, j, out_dim, in_dim):
    h=x.shape[0]//in_dim
    a=x.reshape(h,in_dim,h,in_dim)
    b=j.reshape(out_dim,in_dim,out_dim,in_dim)
    return np.einsum('aAbB,iAjB->aibj',a,b,optimize=True).reshape(h*out_dim,h*out_dim)


def adjoint_local(b, j, out_dim, in_dim):
    h=b.shape[0]//out_dim
    a=b.reshape(h,out_dim,h,out_dim)
    k=j.reshape(out_dim,in_dim,out_dim,in_dim)
    return np.einsum('aibj,iAjB->aAbB',a,k.conj(),optimize=True).reshape(h*in_dim,h*in_dim)


def choi_cost(x,b,out_dim,in_dim):
    h=x.shape[0]//in_dim
    xx=x.reshape(h,in_dim,h,in_dim)
    bb=b.reshape(h,out_dim,h,out_dim)
    return herm(np.einsum('aibj,bBaA->iAjB',bb,xx,optimize=True).reshape(out_dim*in_dim,out_dim*in_dim))


def trace_pair(a,b):
    return float(np.vdot(a,b).real)


class SDPSolver:
    def __init__(self,in_dim,out_dim,solver='CLARABEL',tol=1e-8):
        self.d=in_dim;self.o=out_dim;self.solver=solver;self.tol=tol
        n=in_dim*out_dim
        self.j=cp.Variable((n,n),hermitian=True)
        self.h=cp.Parameter((n,n),hermitian=True)
        marginal=sum(self.j[i*in_dim:(i+1)*in_dim,i*in_dim:(i+1)*in_dim] for i in range(out_dim))
        self.problem=cp.Problem(cp.Maximize(cp.real(cp.trace(self.h@self.j))),[self.j >> 0,marginal==np.eye(in_dim)])
        self.calls=0;self.seconds=0.;self.statuses={}
    def solve(self,h,old=None):
        # Remove the full TP-constraint component before scaling.  The objective
        # on the feasible set changes only by a constant.
        marginal=choi_marginal(h,self.o,self.d)/self.o
        centered=herm(h-np.kron(np.eye(self.o),marginal))
        scale=la.norm(centered,'fro')
        if scale<2e-14 and old is not None:
            return old,{'status':'flat','gain':0.,'scale':scale}
        self.h.value=centered/max(scale,1e-14)
        if old is not None:
            self.j.value=old
        t=time.perf_counter()
        if self.solver=='CLARABEL':
            self.problem.solve(solver='CLARABEL',warm_start=True,tol_gap_abs=self.tol,tol_gap_rel=self.tol,tol_feas=self.tol,max_iter=200)
        elif self.solver=='SCS':
            self.problem.solve(solver='SCS',warm_start=True,eps=self.tol,max_iters=5000,acceleration_lookback=10)
        else:
            self.problem.solve(solver=self.solver,warm_start=True)
        elapsed=time.perf_counter()-t
        self.seconds+=elapsed;self.calls+=1
        self.statuses[self.problem.status]=self.statuses.get(self.problem.status,0)+1
        if self.j.value is None:
            raise RuntimeError('SDP returned no solution: '+str(self.problem.status))
        raw=herm(self.j.value)
        raw_min=float(la.eigvalsh(raw)[0])
        raw_tp=float(la.norm(choi_marginal(raw,self.o,self.d)-np.eye(self.d)))
        candidate=cptp_repair(raw,self.o,self.d)
        gain=None if old is None else trace_pair(h,candidate-old)
        if gain is not None and gain < -2e-11:
            candidate=old
            rejected=True
        else:
            rejected=False
        return candidate,dict(status=self.problem.status,gain=gain,scale=float(scale),raw_min_eigenvalue=raw_min,raw_tp_residual=raw_tp,seconds=elapsed,rejected=rejected)


def permutation_unitary(dims,order):
    size=int(np.prod(dims))
    # Matrix maps old tensor slots to the indicated output tensor ordering.
    return np.eye(size).reshape(tuple(dims)+(size,)).transpose(tuple(order)+(len(dims),)).reshape(size,size)


def identity_memory(m):
    return choi_from_kraus([np.kron(np.eye(m),np.eye(2)[e:e+1]) for e in range(2)])


def unitary_memory_map(u,m):
    # U output ordering M,E; trace E.
    a=u.reshape(m,2,m*2)
    return choi_from_kraus([a[:,e,:] for e in range(2)])


def swap_register_map(m,register):
    q=int(round(np.log2(m)))
    if 1<<q !=m: raise ValueError('register initialization needs power-of-two m')
    dims=[2]*(q+1)
    order=list(range(q+1))
    order[register],order[-1]=order[-1],order[register]
    return unitary_memory_map(permutation_unitary(dims,order),m)


def initial_policy(m,n,kind,rng,theta):
    q=int(round(np.log2(m)))
    ident=identity_memory(m)
    if kind=='prefix':
        return [swap_register_map(m,j) if j<q else ident.copy() for j in range(n)]
    if kind=='rolling':
        # (M_0,...,M_(q-1),E) -> (M_1,...,E,M_0).
        u=permutation_unitary([2]*(q+1),list(range(1,q+1))+[0])
        j=unitary_memory_map(u,m)
        return [j.copy() for _ in range(n)]
    if kind.startswith('partial'):
        # Coherent collision with one register, pure initialized memory.
        angle=float(kind.split(':')[1]) if ':' in kind else theta
        out=[]
        for step in range(n):
            reg=step%q
            order=list(range(q+1));order[reg],order[-1]=order[-1],order[reg]
            p=permutation_unitary([2]*(q+1),order)
            u=np.cos(angle)*np.eye(2*m)+1j*np.sin(angle)*p
            out.append(unitary_memory_map(u,m))
        return out
    if kind.startswith('random'):
        strength=float(kind.split(':')[1]) if ':' in kind else 1.
        out=[]
        for _ in range(n):
            a=rng.normal(size=(2*m,2*m))+1j*rng.normal(size=(2*m,2*m))
            a=herm(a)
            a *= strength/la.norm(a,2)
            out.append(unitary_memory_map(la.expm(1j*a),m))
        return out
    raise ValueError(kind)


class CollisionModel:
    def __init__(self,m,theta):
        self.m=m;self.theta=theta;self.D=4*m
        # Ordering R,S,M,E; swap S and E while preserving R,M.
        dims=[2,2,m,2]
        p=permutation_unitary(dims,[0,3,2,1])
        self.u=np.cos(theta)*np.eye(8*m)+1j*np.sin(theta)*p
        self.swap_indices=np.argmax(p,axis=1)
        self.c=np.cos(theta);self.s=np.sin(theta)
        phi=np.array([1.,0.,0.,1.])/np.sqrt(2)
        bell=np.outer(phi,phi)
        mem=np.zeros((m,m));mem[0,0]=1
        self.rho0=np.kron(bell,mem).astype(complex)
        # Cost on R,S,Q, Bell_RQ tensor I_S, reordered.
        self.bell_rsq=np.einsum('aibj,st->asibtj',bell.reshape(2,2,2,2),np.eye(2)).reshape(8,8)
    def source(self,rho):
        x=np.kron(rho,np.eye(2)/2)
        ix=self.swap_indices;c=self.c;s=self.s
        return c*c*x+s*s*x[np.ix_(ix,ix)]+1j*c*s*(x[ix,:]-x[:,ix])
    def source_adjoint(self,cost):
        ix=self.swap_indices;c=self.c;s=self.s
        x=c*c*cost+s*s*cost[np.ix_(ix,ix)]+1j*c*s*(cost[:,ix]-cost[ix,:])
        return np.einsum('aebe->ab',x.reshape(self.D,2,self.D,2))/2
    def step(self,rho,j):
        return herm(apply_local(self.source(rho),j,self.m,2*self.m))
    def adjoint_step(self,b,j):
        return herm(self.source_adjoint(adjoint_local(b,j,self.m,2*self.m)))
    def forward(self,policy):
        r=[self.rho0]
        for j in policy:r.append(self.step(r[-1],j))
        return r
    def terminal_cost(self,decoder):
        return herm(adjoint_local(self.bell_rsq,decoder,2,self.m))
    def terminal_optimize(self,rho,solver,old=None):
        h=choi_cost(rho,self.bell_rsq,2,self.m)
        dec,stats=solver.solve(h,old)
        return dec,trace_pair(h,dec),stats


def policy_stats(policy,m):
    mins=[];tps=[];ranks=[];unital=[];choi_pur=[]
    for j in policy:
        w=la.eigvalsh(herm(j))
        mins.append(float(w[0]));ranks.append(int(np.sum(w>1e-6)))
        tps.append(float(la.norm(choi_marginal(j,m,2*m)-np.eye(2*m))))
        image=apply_local(np.eye(2*m)/(2*m),j,m,2*m)
        unital.append(float(la.norm(image-np.eye(m)/m)))
        choi_pur.append(float(np.vdot(j,j).real/(2*m)**2))
    return dict(min_eigenvalue=min(mins),max_tp_residual=max(tps),kraus_ranks=ranks,unital_deviations=unital,normalized_choi_purities=choi_pur)


def optimize(m,theta,n,sweeps=6,init='prefix',seed=0,solver='CLARABEL',tol=1e-8,stop=1e-7,verbose=True):
    rng=np.random.default_rng(seed)
    model=CollisionModel(m,theta)
    policy=initial_policy(m,n,init,rng,theta)
    rs=model.forward(policy)
    chan_solver=SDPSolver(2*m,m,solver,tol)
    dec_solver=SDPSolver(m,2,solver,tol)
    decoder,fe,_=model.terminal_optimize(rs[-1],dec_solver)
    history=[dict(sweep=-1,direction='initial',fidelity=fe,error=1-fe)]
    allstats=[]
    t0=time.perf_counter()
    if verbose: print(json.dumps(dict(m=m,theta=theta,n=n,init=init,seed=seed,**history[-1])),flush=True)
    for sweep in range(sweeps):
        old_fe=fe
        localstats=[]
        if sweep%2==0:
            direction='forward'
            bs=[None]*(n+1);bs[n]=model.terminal_cost(decoder)
            for k in reversed(range(n)):bs[k]=model.adjoint_step(bs[k+1],policy[k])
            rho=model.rho0
            for k in range(n):
                x=model.source(rho)
                h=choi_cost(x,bs[k+1],m,2*m)
                policy[k],stats=chan_solver.solve(h,policy[k]);localstats.append(stats)
                rho=herm(apply_local(x,policy[k],m,2*m))
            final_rho=rho
        else:
            direction='backward'
            rs=model.forward(policy)
            b=model.terminal_cost(decoder)
            for k in reversed(range(n)):
                h=choi_cost(model.source(rs[k]),b,m,2*m)
                policy[k],stats=chan_solver.solve(h,policy[k]);localstats.append(stats)
                b=model.adjoint_step(b,policy[k])
            final_rho=model.forward(policy)[-1]
        decoder,fe,ds=model.terminal_optimize(final_rho,dec_solver,decoder)
        entry=dict(sweep=sweep,direction=direction,fidelity=fe,error=1-fe,gain=fe-old_fe,seconds=time.perf_counter()-t0,
                   min_local_gain=min((x.get('gain',0.) or 0.) for x in localstats),rejected_updates=sum(x.get('rejected',False) for x in localstats))
        history.append(entry);allstats.extend(localstats)
        if verbose:print(json.dumps(dict(m=m,theta=theta,n=n,init=init,seed=seed,**entry)),flush=True)
        if fe<old_fe-5e-8:raise RuntimeError('Nonmonotone sweep exceeds tolerance')
        if sweep>=3 and fe-old_fe<stop and history[-2]['gain']<stop:break
    rs=model.forward(policy)
    spectrum=la.eigvalsh(rs[-1])
    # Partial R trace is invariant, independent of the maps.
    rmargin=np.einsum('asmbsm->ab',rs[-1].reshape(2,2,m,2,2,m))
    result=dict(m=m,theta=theta,n=n,init=init,seed=seed,solver=solver,tol=tol,history=history,
                fidelity=fe,error=1-fe,passive_error=.75*(1-np.sin(theta)**4)**n,
                global_lower_error=.75*(1-np.sqrt(1-(1-np.sin(theta)**4)**n)),
                final_state_min_eigenvalue=float(spectrum[0]),final_state_trace=float(np.trace(rs[-1]).real),
                reference_marginal_residual=float(la.norm(rmargin-np.eye(2)/2)),
                policy_stats=policy_stats(policy,m),solver_calls=chan_solver.calls+dec_solver.calls,
                solver_seconds=chan_solver.seconds+dec_solver.seconds,solver_statuses=chan_solver.statuses,
                maximum_raw_cp_violation=max((max(0,-x.get('raw_min_eigenvalue',0.)) for x in allstats),default=0),
                maximum_raw_tp_residual=max((x.get('raw_tp_residual',0.) for x in allstats),default=0))
    return result,policy,decoder,rs


def global_decoder_optimum(theta,n,solver='CLARABEL'):
    phi=np.array([1.,0.,0.,1.])/np.sqrt(2)
    bell=np.outer(phi,phi)
    rho=bell.astype(complex)
    for k in range(n):
        rho=np.kron(rho,np.eye(2)/2)
        dims=[2]*(k+3)
        order=list(range(k+3));order[1],order[-1]=order[-1],order[1]
        p=permutation_unitary(dims,order)
        u=np.cos(theta)*np.eye(1<<(k+3))+1j*np.sin(theta)*p
        rho=u@rho@u.conj().T
    d=1<<n
    rb=np.trace(rho.reshape(2,2,d,2,2,d),axis1=1,axis2=4).reshape(2*d,2*d)
    h=choi_cost(rb,bell,2,d)
    dec,stats=SDPSolver(d,2,solver,1e-9).solve(h)
    return trace_pair(h,dec),stats


def self_test():
    rng=np.random.default_rng(8)
    for m in [2,4]:
        d=2*m;h=4
        x=rng.normal(size=(h*d,h*d))+1j*rng.normal(size=(h*d,h*d));x=x@x.conj().T;x/=np.trace(x)
        b=rng.normal(size=(h*m,h*m))+1j*rng.normal(size=(h*m,h*m));b=herm(b)
        j=initial_policy(m,1,'random:2',rng,.5)[0]
        y=apply_local(x,j,m,d)
        aa=trace_pair(b,y);bb=trace_pair(adjoint_local(b,j,m,d),x);cc=trace_pair(choi_cost(x,b,m,d),j)
        assert abs(aa-bb)<1e-12 and abs(aa-cc)<1e-12,(aa,bb,cc)
        model=CollisionModel(m,.4)
        rho=model.rho0;cost=herm(rng.normal(size=(4*m,4*m))+1j*rng.normal(size=(4*m,4*m)))
        assert abs(trace_pair(cost,model.step(rho,j))-trace_pair(model.adjoint_step(cost,j),rho))<1e-12
    tests=[]
    for theta in [.3,.7]:
        exact=.25+.75*np.sin(theta)**2
        for m in [2,4]:
            result,_,_,_=optimize(m,theta,1,sweeps=2,verbose=False)
            assert abs(result['fidelity']-exact)<1e-7,(theta,m,result['fidelity'],exact)
            tests.append(dict(theta=theta,m=m,n=1,fidelity=result['fidelity'],known_optimum=exact))
        glob,_=global_decoder_optimum(theta,2)
        result,_,_,_=optimize(4,theta,2,sweeps=2,verbose=False)
        assert abs(result['fidelity']-glob)<2e-7,(theta,result['fidelity'],glob)
        tests.append(dict(theta=theta,m=4,n=2,fidelity=result['fidelity'],global_optimum=glob))
    print(json.dumps(dict(status='passed',tests=tests),indent=2),flush=True)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--self-test',action='store_true');p.add_argument('--m',type=int,default=2);p.add_argument('--theta',type=float,default=.7);p.add_argument('--n',type=int,default=8)
    p.add_argument('--sweeps',type=int,default=8);p.add_argument('--init',default='prefix');p.add_argument('--seed',type=int,default=0);p.add_argument('--solver',default='CLARABEL');p.add_argument('--tol',type=float,default=1e-8);p.add_argument('--stop',type=float,default=1e-7);p.add_argument('--out')
    a=p.parse_args()
    if a.self_test:self_test();return
    result,policy,decoder,states=optimize(a.m,a.theta,a.n,a.sweeps,a.init,a.seed,a.solver,a.tol,a.stop)
    if a.out:
        stem=Path(a.out);stem.parent.mkdir(parents=True,exist_ok=True)
        stem.with_suffix('.json').write_text(json.dumps(result,indent=2))
        np.savez_compressed(stem.with_suffix('.npz'),policy=np.array(policy),decoder=decoder,states=np.array(states))
    print(json.dumps({'result':result},indent=2),flush=True)

if __name__=='__main__':main()
