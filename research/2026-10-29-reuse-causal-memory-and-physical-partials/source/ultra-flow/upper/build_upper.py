#!/usr/bin/env python3
"""Bounded-memory equilibrated-pseudostress generator. No large factorization.
The exact consumer, not this numerical solve, certifies the continuum upper.
"""
from pathlib import Path
import hashlib,json,time
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as sla
BASE=Path(__file__).parent

class AggregateVcycle:
    """Symmetric Jacobi/Galerkin algebraic preconditioner, not a new PDE grid."""
    def __init__(self,A,coords):
        self.A=A.tocsr();self.invdiag=1/self.A.diagonal()
        self.P=None;self.child=None;self.chol=None
        if A.shape[0]<=32:
            self.chol=np.linalg.cholesky(A.toarray());return
        coarse,group=np.unique(coords//2,axis=0,return_inverse=True)
        if len(coarse)==len(coords):raise ValueError('Aggregation stalled')
        self.P=sp.csr_matrix((np.ones(len(group)),(np.arange(len(group)),group)),shape=(len(group),len(coarse)))
        self.child=AggregateVcycle((self.P.T@A@self.P).tocsr(),coarse)
    def apply(self,b):
        one=b.ndim==1
        if one:b=b[:,None]
        if self.chol is not None:
            x=np.linalg.solve(self.chol.T,np.linalg.solve(self.chol,b))
            return x[:,0] if one else x
        x=np.zeros_like(b)
        for _ in range(2):x+=(2/3)*self.invdiag[:,None]*(b-self.A@x)
        x+=self.P@self.child.apply(self.P.T@(b-self.A@x))
        for _ in range(2):x+=(2/3)*self.invdiag[:,None]*(b-self.A@x)
        return x[:,0] if one else x
    def sizes(self):
        return [dict(n=self.A.shape[0],nnz=self.A.nnz)]+(self.child.sizes() if self.child else [])

def geometry(mask):
    M=mask.shape[0];coords=np.argwhere(mask);nv=len(coords)
    node=np.full(mask.shape,-1,dtype=np.int64);node[tuple(coords.T)]=np.arange(nv)
    tail=[];head=[];axis=[];site=[];maps=[]
    for ax in range(3):
        pos=np.argwhere(mask|np.roll(mask,-1,axis=ax))
        dst=pos.copy();dst[:,ax]=(dst[:,ax]+1)%M
        ids=np.arange(len(tail),len(tail)+len(pos))
        fm=np.full(mask.shape,-1,dtype=np.int64);fm[tuple(pos.T)]=ids;maps.append(fm)
        tail.extend(node[tuple(pos.T)]);head.extend(node[tuple(dst.T)])
        axis.extend([ax]*len(pos));site.extend(pos)
    tail=np.array(tail);head=np.array(head);axis=np.array(axis);site=np.array(site)
    incoming=np.empty((nv,3),dtype=np.int64);outgoing=np.empty_like(incoming)
    for ax in range(3):
        outgoing[:,ax]=maps[ax][tuple(coords.T)]
        prev=coords.copy();prev[:,ax]=(prev[:,ax]-1)%M
        incoming[:,ax]=maps[ax][tuple(prev.T)]
    both=(tail>=0)&(head>=0)
    rr=np.r_[np.arange(nv),tail[both],head[both]]
    cc=np.r_[np.arange(nv),head[both],tail[both]]
    L=sp.coo_matrix((np.r_[np.full(nv,6.),-np.ones(2*both.sum())],(rr,cc)),shape=(nv,nv)).tocsr()
    return coords,tail,head,axis,site,incoming,outgoing,L

def forest(tail,head,nv):
    adj=[[] for _ in range(nv)];wall=[[] for _ in range(nv)]
    for e,(a,b) in enumerate(zip(tail,head)):
        if a>=0 and b>=0:
            adj[a].append((int(b),e,-1));adj[b].append((int(a),e,+1))
        elif a>=0:wall[a].append((e,1))
        else:wall[b].append((e,-1))
    parent=np.full(nv,-1,dtype=np.int64);pe=parent.copy();sign=np.zeros(nv,dtype=np.int64)
    order=[];roots=[];boundary=[];label=np.full(nv,-1,dtype=np.int64)
    for seed in range(nv):
        if parent[seed]>=0:continue
        todo=[seed];seen={seed};choice=None
        for v in todo:
            if wall[v]:choice=v;break
            for w,_,_ in adj[v]:
                if w not in seen:seen.add(w);todo.append(w)
        assert choice is not None
        root=choice;parent[root]=root;roots.append(root);boundary.append(wall[root][0])
        queue=[root]
        for v in queue:
            order.append(v);label[v]=len(roots)-1
            for w,e,sgn in adj[v]:
                if parent[w]>=0:continue
                parent[w]=v;pe[w]=e;sign[w]=sgn;queue.append(w)
    return parent,pe,sign,np.array(order),np.array(roots),boundary,label

def repair(q,incoming,outgoing,parent,pe,sign,order,roots,boundary,target,bits):
    scale=1<<bits
    assert np.max(np.abs(q))*scale<2**60
    z=np.rint(q*scale).astype(np.int64)
    r=z[outgoing].sum(axis=1)-z[incoming].sum(axis=1)-scale*target
    bound=len(parent)*int(np.max(np.abs(r)))+int(np.max(np.abs(z)))
    assert bound<2**61
    for v in order[::-1]:
        if pe[v]<0:continue
        z[pe[v]]-=sign[v]*r[v]
        r[parent[v]]+=r[v];r[v]=0
    for v,(e,sgn) in zip(roots,boundary):z[e]-=sgn*r[v];r[v]=0
    assert not np.any(z[outgoing].sum(axis=1)-z[incoming].sum(axis=1)-scale*target)
    return z

def main():
    start=time.perf_counter()
    mask=np.load(BASE.parent/'CURRENTS.npz')['pore_mask']
    M=mask.shape[0];assert mask.shape==(48,48,48)
    coords,tail,head,axis,site,inc,out,L=geometry(mask)
    nv=len(coords);nf=len(tail);nq=3*nf;nt=nq+3*nv
    parent,pe,sgn,order,roots,wall,label=forest(tail,head,nv)
    mg=AggregateVcycle(L,coords)
    tsetup=time.perf_counter()-start
    pos_t=tail>=0;pos_h=head>=0
    def DT(p):
        r=np.zeros((nf,p.shape[1]));r[pos_t]+=p[tail[pos_t]];r[pos_h]-=p[head[pos_h]]
        return r
    def D(q):return q[out].sum(axis=1)-q[inc].sum(axis=1)
    def stressA(q):
        a=q[inc];b=q[out];mean=(a+b)/2;delta=(b-a)/12
        trace=sum(mean[:,j,j] for j in range(3))/3
        for j in range(3):mean[:,j,j]-=trace;delta[:,j,j]*=2/3
        ri=mean/2-delta;ro=mean/2+delta
        r=np.zeros_like(q)
        r[pos_t]+=ro[tail[pos_t],axis[pos_t]]
        r[pos_h]+=ri[head[pos_h],axis[pos_h]]
        return r
    def energy(q):return float(np.sum(q*stressA(q))/M**3)
    def matvec(x):
        q=x[:nq].reshape(nf,3);p=x[nq:].reshape(nv,3)
        return np.r_[(stressA(q)+DT(p)).ravel(),D(q).ravel()]
    degree=pos_t.astype(float)+pos_h.astype(float)
    diagonal=np.repeat((degree/3)[:,None],3,axis=1)
    diagonal[np.arange(nf),axis]*=2/3
    def precondition(x):
        q=x[:nq].reshape(nf,3);p=x[nq:].reshape(nv,3)
        return np.r_[(q/diagonal).ravel(),(mg.apply(p)/3).ravel()]
    K=sla.LinearOperator((nt,nt),matvec=matvec,dtype=float)
    P=sla.LinearOperator((nt,nt),matvec=precondition,dtype=float)
    # Deterministic implementation controls, not continuum proof substitutes.
    x=np.sin(np.arange(nt)*.071);y=np.cos(np.arange(nt)*.053)
    symerr=abs(x@matvec(y)-y@matvec(x))/max(1,abs(x@matvec(y)),abs(y@matvec(x)))
    assert symerr<1e-11
    preerr=abs(x@precondition(y)-y@precondition(x))/max(1,abs(x@precondition(y)),abs(y@precondition(x)))
    assert preerr<1e-11 and x@precondition(x)>0
    tscalar=time.perf_counter();count=[0]
    def cb_scalar(x):count[0]+=1
    scalar_p,info=sla.cg(L,np.ones(nv),M=sla.LinearOperator(L.shape,matvec=mg.apply),
        rtol=1e-11,atol=0,maxiter=300,callback=cb_scalar)
    scalar_q=DT(scalar_p[:,None])
    scalar_z=repair(scalar_q,inc,out,parent,pe,sgn,order,roots,wall,np.ones((nv,1),dtype=np.int64),32)
    scalar_seconds=time.perf_counter()-tscalar
    stresses=np.empty((nf,3,3));stats=[]
    for force in range(3):
        rhs=np.zeros(nt);rhs[nq:].reshape(nv,3)[:,force]=1
        q0=np.zeros((nf,3));q0[:,force]=scalar_q[:,0]
        initial=np.zeros(nt);initial[:nq]=q0.ravel();initial[nq:].reshape(nv,3)[:,force]=-scalar_p/3
        hist=[];counter=[0];tf=time.perf_counter()
        def callback(x):
            counter[0]+=1
            if counter[0]%40==0:
                q=x[:nq].reshape(nf,3)
                div=D(q);div[:,force]-=1
                item=dict(iteration=counter[0],energy=energy(q),divergence_max=float(np.max(np.abs(div))),seconds=time.perf_counter()-tf)
                hist.append(item);print(json.dumps(dict(force=force,**item)),flush=True)
        sol,mi=sla.minres(K,rhs,x0=initial,M=P,rtol=1e-9,maxiter=800,callback=callback,check=True)
        q=sol[:nq].reshape(nf,3)
        # Constant hydrostatic gauges per fluid component have zero source/energy.
        a=q[inc];b=q[out];tr=sum((a[:,j,j]+b[:,j,j])/2 for j in range(3))/3
        pressure=np.bincount(label,weights=tr)/np.bincount(label)
        face_label=np.where(pos_t,label[np.maximum(tail,0)],label[np.maximum(head,0)])
        q[np.arange(nf),axis]-=pressure[face_label]
        stresses[:,:,force]=q
        target=np.zeros((nv,3));target[:,force]=1
        stats.append(dict(force=force,iterations=counter[0],MINRES_info=int(mi),
            seconds=time.perf_counter()-tf,energy=energy(q),
            relative_KKT_residual=float(np.linalg.norm(matvec(sol)-rhs)/np.linalg.norm(rhs)),
            force_balance_max=float(np.max(np.abs(D(q)-target))),history=hist))
        print(json.dumps(dict(force_finished=force,**{k:v for k,v in stats[-1].items() if k!='history'})),flush=True)
    tr=time.perf_counter();zs=[]
    for f in range(3):
        target=np.zeros((nv,3),dtype=np.int64);target[:,f]=1
        zs.append(repair(stresses[:,:,f],inc,out,parent,pe,sgn,order,roots,wall,target,32))
    z=np.stack(zs,axis=2);repair_seconds=time.perf_counter()-tr
    np.savez_compressed(BASE/'STRESSES.npz',pore_mask=mask,coords=coords,tail=tail,head=head,
        axis=axis,site=site,incoming=inc,outgoing=out,stress_numerators=z,
        scalar_numerators=scalar_z[:,0],dyadic_bits=np.array(32))
    result=dict(status='REPAIRED_ORIGINAL_GRID_STRESSES_EXACT_CONSUMER_PENDING',
        original_mask_sha256=hashlib.sha256(mask.tobytes()).hexdigest(),
        shape=list(mask.shape),fluid_cells=nv,faces=nf,mixed_unknowns=nt,
        algebraic_preconditioner=dict(levels=mg.sizes(),coarsest_dense_dimension=mg.sizes()[-1]['n'],
            setup_seconds=tsetup,new_physical_grid=False),
        implementation_checks=dict(operator_symmetry_relative=symerr,preconditioner_symmetry_relative=preerr),
        scalar_initial_upper=dict(CG_iterations=count[0],CG_info=int(info),seconds=scalar_seconds,
            source_balance_repaired_exactly=True),
        stress_optimization=stats,exact_repair_seconds=repair_seconds,
        total_seconds=time.perf_counter()-start,large_LU_allocations=0,
        new_images=0,new_crops=0,new_physical_shots=0,paid_compute=0,
        note='Algebraic aggregate levels precondition the original-grid equations; they are not new pore discretizations. Exact consumer decides validity and gap.')
    (BASE/'BUILD_UPPER.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='stress_optimization'},indent=2),flush=True)

if __name__=='__main__':main()
