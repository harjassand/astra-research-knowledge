#!/usr/bin/env python3
"""Global Bell-cost control of a payload qubit times a tracial spin-J gauge.

Environment spin 1/2, with arbitrary multiplicity, is the default channel class.
The --all-env option allows every covariant CPTP channel on the fixed memory.
"""
from rep_control import *


class UnrestrictedDecoder:
    def __init__(self,m,solver,tol):self.m=m;self.solver=SDPSolver(m,2,solver,tol)
    @property
    def calls(self):return self.solver.calls
    @property
    def seconds(self):return self.solver.seconds
    def cost(self,rho,b):return [choi_cost(rho,b,2,self.m)]
    def solve(self,cost,old=None):
        x,stats=self.solver.solve(cost[0],None if old is None else old[0]);return [x],stats
    def score(self,coeff,cost):return trace_pair(coeff[0],cost[0])
    def adjoint(self,b,coeff):return adjoint_local(b,coeff[0],2,self.m)


def setup(j,theta,solver='CLARABEL',tol=1e-8,all_env=False,gauge_state='tracial',gauge_seed=123):
    half=spin_rep(.5);gauge=spin_rep(j);mem=tensor_rep(half,gauge);inp=tensor_rep(mem,half)
    m=2*int(2*j+1)
    chan=RepChannel(inp,mem,None if all_env else [.5],solver,tol)
    dec=RepChannel(mem,half,None,solver,tol) if gauge_state=='tracial' else UnrestrictedDecoder(m,solver,tol)
    model=CollisionModel(m,theta)
    phi=np.array([1.,0.,0.,1.])/np.sqrt(2)
    dg=m//2
    if gauge_state=='tracial':gauge_rho=np.eye(dg)/dg
    else:
        vector=np.zeros(dg,complex)
        if gauge_state=='north':vector[0]=1
        elif gauge_state=='cat':vector[0]=vector[-1]=1/np.sqrt(2)
        elif gauge_state=='random':
            rng=np.random.default_rng(gauge_seed);vector=rng.normal(size=dg)+1j*rng.normal(size=dg);vector/=la.norm(vector)
        else:raise ValueError(gauge_state)
        gauge_rho=np.outer(vector,vector.conj())
    model.rho0=np.kron(np.outer(phi,phi),np.kron(np.eye(2)/2,gauge_rho)).astype(complex)
    return model,chan,dec,inp


def initial_coeff_policy(j,n,kind,rng,chan,inp):
    m=chan.o;dg=int(2*j+1);swap=permutation_unitary([2,dg,2],[2,1,0])
    capture=chan.coeff_from_kraus([swap.reshape(m,2,2*m)[:,e,:] for e in range(2)])
    ident=chan.coeff_from_kraus([np.kron(np.eye(m),np.eye(2)[e:e+1]) for e in range(2)])
    if kind=='prefix':return [capture]+[[x.copy() for x in ident] for _ in range(n-1)]
    if kind.startswith('random'):
        strength=float(kind.split(':')[1]) if ':' in kind else .2
        blocks=rep_blocks(*inp);answer=[capture]
        for _ in range(n-1):
            u=np.zeros((2*m,2*m),complex)
            for _,r,s,v in blocks:
                a=herm(rng.normal(size=(r,r))+1j*rng.normal(size=(r,r)));a*=strength/max(la.norm(a,2),1e-12)
                u+=v@np.kron(la.expm(1j*a),np.eye(s))@v.conj().T
            answer.append(chan.coeff_from_kraus([u.reshape(m,2,2*m)[:,e,:] for e in range(2)]))
        return answer
    raise ValueError(kind)


def optimize_gauge(j,theta,n,sweeps=12,init='prefix',seed=0,solver='CLARABEL',tol=1e-8,stop=1e-8,all_env=False,verbose=True,gauge_state='tracial',gauge_seed=123):
    model,chan,dec,inp=setup(j,theta,solver,tol,all_env,gauge_state,gauge_seed);m=chan.o
    policy=initial_coeff_policy(j,n,init,np.random.default_rng(seed),chan,inp)
    def forward():
        states=[model.rho0]
        for coeff in policy:states.append(chan.apply(model.source(states[-1]),coeff))
        return states
    def terminal(rho,old=None):
        cost=dec.cost(rho,model.bell_rsq);d,stats=dec.solve(cost,old)
        return d,dec.score(d,cost),stats
    def adjoint_step(b,coeff):return model.source_adjoint(chan.adjoint(b,coeff))
    states=forward();decoder,fe,_=terminal(states[-1]);start=time.perf_counter()
    history=[dict(sweep=-1,direction='initial',fidelity=fe,error=1-fe)];allstats=[]
    if verbose:print(json.dumps(dict(j=j,m=m,theta=theta,n=n,init=init,**history[-1])),flush=True)
    for sweep in range(sweeps):
        old_fe=fe;local=[]
        if sweep%2==0:
            direction='forward';bs=[None]*(n+1);bs[n]=dec.adjoint(model.bell_rsq,decoder)
            for k in reversed(range(1,n)):bs[k]=adjoint_step(bs[k+1],policy[k])
            rho=chan.apply(model.source(model.rho0),policy[0])
            for k in range(1,n):
                x=model.source(rho);cost=chan.cost(x,bs[k+1]);policy[k],st=chan.solve(cost,policy[k]);local.append(st)
                rho=chan.apply(x,policy[k])
            final=rho
        else:
            direction='backward';states=forward();b=dec.adjoint(model.bell_rsq,decoder)
            for k in reversed(range(1,n)):
                cost=chan.cost(model.source(states[k]),b);policy[k],st=chan.solve(cost,policy[k]);local.append(st)
                b=adjoint_step(b,policy[k])
            final=forward()[-1]
        decoder,fe,_=terminal(final,decoder)
        entry=dict(sweep=sweep,direction=direction,fidelity=fe,error=1-fe,gain=fe-old_fe,seconds=time.perf_counter()-start,
                   min_local_gain=min((x.get('gain',0.) or 0.) for x in local) if local else 0.,rejected_updates=sum(x.get('rejected',False) for x in local))
        history.append(entry);allstats.extend(local)
        if verbose:print(json.dumps(dict(j=j,m=m,theta=theta,n=n,init=init,**entry)),flush=True)
        if fe<old_fe-1e-7:raise RuntimeError('Nonmonotone sweep')
        if sweep>=7 and fe-old_fe<stop and history[-2]['gain']<stop:break
    states=forward()
    ranks=[sum(int(np.sum(la.eigvalsh(x)>1e-7))*s for x,(_,_,s,_) in zip(coeff,chan.blocks)) for coeff in policy]
    result=dict(j=j,m=m,theta=theta,n=n,sweeps=sweeps,init=init,seed=seed,all_env=all_env,gauge_state=gauge_state,gauge_seed=gauge_seed,fidelity=fe,error=1-fe,history=history,
                passive_error=.75*(1-np.sin(theta)**4)**n,blocks=[dict(spin=k,multiplicity=r) for k,r,s,u in chan.blocks],
                maximum_tp_residual=max(float(la.norm(chan.marginal(x)-np.eye(chan.d))) for x in policy),
                minimum_coefficient_eigenvalue=min(float(la.eigvalsh(x)[0]) for coeff in policy for x in coeff),kraus_ranks=ranks,
                final_state_min_eigenvalue=float(la.eigvalsh(states[-1])[0]),final_state_trace=float(np.trace(states[-1]).real),
                reference_marginal_residual=float(la.norm(np.einsum('asmbsm->ab',states[-1].reshape(2,2,m,2,2,m))-np.eye(2)/2)),
                solver_calls=chan.calls+dec.calls,solver_seconds=chan.seconds+dec.seconds,solver_statuses=chan.statuses)
    return result,policy,decoder,states


def self_test():
    records=[];rng=np.random.default_rng(19)
    for j in [.5,1.,2.]:
        model,chan,dec,inp=setup(j,.5);m=chan.o
        coeff=initial_coeff_policy(j,2,'random:0.4',rng,chan,inp)[-1];dense=chan.dense_choi(coeff)
        assert la.norm(choi_marginal(dense,m,2*m)-np.eye(2*m))<1e-10
        rho=model.source(model.rho0);b=herm(rng.normal(size=(4*m,4*m))+1j*rng.normal(size=(4*m,4*m)))
        a=chan.apply(rho,coeff);a2=apply_local(rho,dense,m,2*m);assert la.norm(a-a2)<1e-10
        cost=chan.cost(rho,b);v1=chan.score(coeff,cost);v2=trace_pair(b,a);v3=trace_pair(chan.adjoint(b,coeff),rho)
        assert max(abs(v1-v2),abs(v1-v3))<1e-10,(j,v1,v2,v3)
        opt,stats=chan.solve(cost,coeff);assert chan.score(opt,cost)>=v1-1e-9
        assert la.norm(chan.marginal(opt)-np.eye(2*m))<1e-8
        records.append(dict(j=j,m=m,trace_residual=float(la.norm(chan.marginal(opt)-np.eye(2*m))),blocks=[dict(spin=k,multiplicity=r) for k,r,s,u in chan.blocks]))
    print(json.dumps(dict(status='passed',tests=records),indent=2),flush=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');p.add_argument('--j',type=float,default=1.);p.add_argument('--theta',type=float,default=.5);p.add_argument('--n',type=int,default=37);p.add_argument('--sweeps',type=int,default=12);p.add_argument('--init',default='prefix');p.add_argument('--seed',type=int,default=0);p.add_argument('--solver',default='CLARABEL');p.add_argument('--tol',type=float,default=1e-8);p.add_argument('--stop',type=float,default=1e-8);p.add_argument('--all-env',action='store_true');p.add_argument('--out');p.add_argument('--gauge-state',default='tracial');p.add_argument('--gauge-seed',type=int,default=123)
    a=p.parse_args()
    if a.self_test:self_test();return
    result,policy,decoder,states=optimize_gauge(a.j,a.theta,a.n,a.sweeps,a.init,a.seed,a.solver,a.tol,a.stop,a.all_env,gauge_state=a.gauge_state,gauge_seed=a.gauge_seed)
    if a.out:
        stem=Path(a.out);stem.parent.mkdir(parents=True,exist_ok=True);Path(str(stem)+'.json').write_text(json.dumps(result,indent=2));data={'states':np.array(states)}
        for k,x in enumerate(zip(*policy)):data['policy_block_'+str(k)]=np.array(x)
        for k,x in enumerate(decoder):data['decoder_block_'+str(k)]=x
        np.savez_compressed(str(stem)+'.npz',**data)
    print(json.dumps({'result':result},indent=2),flush=True)

if __name__=='__main__':main()
