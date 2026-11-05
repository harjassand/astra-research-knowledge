#!/usr/bin/env python3
"""Finite-horizon control of a truncated regular SO(3) frame, with right multiplicities."""
from spin_gauge_control import *


def rotor_setup(cutoff,theta,initial='identity',solver='CLARABEL',tol=1e-8):
    reps=[];sectors=[];offset=0
    for j in range(cutoff+1):
        p,z=spin_rep(j);d=2*j+1;reps.append((np.kron(p,np.eye(d)),np.kron(z,np.eye(d))));sectors.append((j,d,offset));offset+=d*d
    mem=(la.block_diag(*[x[0] for x in reps]),la.block_diag(*[x[1] for x in reps]));inp=tensor_rep(mem,spin_rep(.5));m=offset
    chan=RepChannel(inp,mem,[.5],solver,tol);dec=UnrestrictedDecoder(m,solver,tol)
    model=CollisionModel(m,theta);vector=np.zeros(m,complex)
    if initial=='vacuum':vector[0]=1
    else:
        for j,d,off in sectors:
            weight=d if initial=='identity' else np.sin(np.pi*(j+1)/(cutoff+2))
            for k in range(d):vector[off+k*d+k]=weight/np.sqrt(d)
        vector/=la.norm(vector)
    phi=np.array([1.,0.,0.,1.])/np.sqrt(2)
    model.rho0=np.kron(np.outer(phi,phi),np.outer(vector,vector.conj()))
    return model,chan,dec,inp


def initial_policy_rotor(chan,inp,n,strength,seed):
    rng=np.random.default_rng(seed);blocks=rep_blocks(*inp);m=chan.o;answer=[]
    for k in range(n):
        u=np.zeros((2*m,2*m),complex)
        for _,r,s,v in blocks:
            h=herm(rng.normal(size=(r,r))+1j*rng.normal(size=(r,r)));h*=(1. if k==0 else strength)/max(la.norm(h,2),1e-12)
            u+=v@np.kron(la.expm(1j*h),np.eye(s))@v.conj().T
        answer.append(chan.coeff_from_kraus([u.reshape(m,2,2*m)[:,e,:] for e in range(2)]))
    return answer


def matched_rotor_policy(chan,inp,n,theta,seed):
    m=chan.o;plus,z=inp
    jp=np.einsum('aibi->ab',plus.reshape(m,2,m,2))/2
    jz=np.einsum('aibi->ab',z.reshape(m,2,m,2))/2
    jx=(jp+jp.conj().T)/2;jy=(jp-jp.conj().T)/(2j)
    px=np.array([[0,1],[1,0]],complex);py=np.array([[0,-1j],[1j,0]],complex);pz=np.diag([1.,-1.])
    h=np.kron(jx,px)+np.kron(jy,py)+np.kron(jz,pz)+np.eye(2*m)/2
    u=la.expm(1j*theta*h)
    coeff=chan.coeff_from_kraus([u.reshape(m,2,2*m)[:,e,:] for e in range(2)])
    return [[x.copy() for x in coeff] for _ in range(n)]


def optimize_rotor(cutoff,theta,n,sweeps=8,initial='identity',strength=.15,seed=0,solver='CLARABEL',tol=1e-8,_setup=rotor_setup,_policy=initial_policy_rotor):
    model,chan,dec,inp=_setup(cutoff,theta,initial,solver,tol);m=chan.o;policy=_policy(chan,inp,n,strength,seed)
    def forward():
        states=[model.rho0]
        for coeff in policy:states.append(chan.apply(model.source(states[-1]),coeff))
        return states
    def terminal(rho,old=None):
        cost=dec.cost(rho,model.bell_rsq);d,st=dec.solve(cost,old);return d,dec.score(d,cost)
    def back(b,x):return model.source_adjoint(chan.adjoint(b,x))
    states=forward();decoder,fe=terminal(states[-1]);start=time.perf_counter();history=[dict(sweep=-1,fidelity=fe,error=1-fe)]
    print(json.dumps(dict(cutoff=cutoff,m=m,theta=theta,n=n,initial=initial,**history[-1])),flush=True)
    for sweep in range(sweeps):
        old_fe=fe;stats=[]
        if sweep%2==0:
            bs=[None]*(n+1);bs[n]=dec.adjoint(model.bell_rsq,decoder)
            for k in reversed(range(n)):bs[k]=back(bs[k+1],policy[k])
            rho=model.rho0
            for k in range(n):
                x=model.source(rho);g=chan.cost(x,bs[k+1]);policy[k],st=chan.solve(g,policy[k]);stats.append(st);rho=chan.apply(x,policy[k])
            final=rho
        else:
            states=forward();b=dec.adjoint(model.bell_rsq,decoder)
            for k in reversed(range(n)):
                g=chan.cost(model.source(states[k]),b);policy[k],st=chan.solve(g,policy[k]);stats.append(st);b=back(b,policy[k])
            final=forward()[-1]
        decoder,fe=terminal(final,decoder)
        entry=dict(sweep=sweep,fidelity=fe,error=1-fe,gain=fe-old_fe,seconds=time.perf_counter()-start,rejected_updates=sum(s.get('rejected',False) for s in stats))
        history.append(entry);print(json.dumps(dict(cutoff=cutoff,m=m,theta=theta,n=n,initial=initial,**entry)),flush=True)
        if fe<old_fe-1e-7:raise RuntimeError('Nonmonotone sweep')
    states=forward();result=dict(cutoff=cutoff,m=m,theta=theta,n=n,initial=initial,strength=strength,seed=seed,fidelity=fe,error=1-fe,history=history,
                blocks=[dict(spin=j,multiplicity=r) for j,r,s,u in chan.blocks],
                maximum_tp_residual=max(float(la.norm(chan.marginal(x)-np.eye(chan.d))) for x in policy),
                minimum_coefficient_eigenvalue=min(float(la.eigvalsh(x)[0]) for coeff in policy for x in coeff),
                final_state_trace=float(np.trace(states[-1]).real),final_state_min_eigenvalue=float(la.eigvalsh(states[-1])[0]),
                solver_calls=chan.calls+dec.calls,solver_seconds=chan.seconds+dec.seconds,solver_statuses=chan.statuses)
    return result,policy,decoder,states


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cutoff',type=int,default=1);p.add_argument('--theta',type=float,default=.5);p.add_argument('--n',type=int,default=37);p.add_argument('--sweeps',type=int,default=8);p.add_argument('--initial',default='identity');p.add_argument('--strength',type=float,default=.15);p.add_argument('--seed',type=int,default=0);p.add_argument('--solver',default='CLARABEL');p.add_argument('--tol',type=float,default=1e-8);p.add_argument('--out');p.add_argument('--seed-policy',default='random');a=p.parse_args()
    result,policy,decoder,states=optimize_rotor(a.cutoff,a.theta,a.n,a.sweeps,a.initial,a.theta if a.seed_policy=='matched' else a.strength,a.seed,a.solver,a.tol,_policy=matched_rotor_policy if a.seed_policy=='matched' else initial_policy_rotor)
    if a.out:
        Path(a.out+'.json').write_text(json.dumps(result,indent=2));data={'states':np.array(states),'decoder':decoder[0]}
        for k,x in enumerate(zip(*policy)):data['policy_block_'+str(k)]=np.array(x)
        np.savez_compressed(a.out+'.npz',**data)
    print(json.dumps({'result':result},indent=2),flush=True)
