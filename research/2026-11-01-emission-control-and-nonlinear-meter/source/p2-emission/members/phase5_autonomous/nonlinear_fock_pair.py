"""Full cubic six-mode Lindblad audit of one within-parity logical pair.

The shared moving displacement follows the EXACT common classical dynamics.
No cubic Hamiltonian term is dropped.  The remaining approximation is the
stated finite Fock cutoff.  All three cold and independent hot ports are traced.
"""
from pathlib import Path
import argparse,itertools,json,time
import numpy as np
from scipy import sparse as sp
from joint_gaussian_instrument import Model
from nonlinear_mean_model import controls,classical_trajectory,trajectory_at


class SparseLinearCombination:
    def __init__(self,ops):
        row=[];col=[];data=[];which=[]
        for i,O in enumerate(ops):
            O=O.tocoo();row.extend(O.row);col.extend(O.col);data.extend(O.data);which.extend([i]*O.nnz)
        self.n=ops[0].shape[0]
        unique,self.inverse=np.unique(np.array(row)*self.n+np.array(col),return_inverse=True)
        self.indices=unique%self.n;self.data=np.array(data);self.which=np.array(which)
        self.indptr=np.r_[0,np.cumsum(np.bincount(unique//self.n,minlength=self.n))]
        self.nnz=len(unique)
    def __call__(self,coeff):
        values=self.data*np.asarray(coeff)[self.which]
        values=np.bincount(self.inverse,weights=values.real,minlength=self.nnz)+1j*np.bincount(self.inverse,weights=values.imag,minlength=self.nnz)
        return sp.csr_matrix((values,self.indices,self.indptr),shape=(self.n,self.n))


class FullFock:
    def __init__(self,model,nc=3,nb=2,pair=(0,5),diagonals=True):
        self.model=model;self.nc=nc;self.nb=nb;self.pair=pair;self.diagonals=diagonals
        self.z=model.z[list(pair)];assert np.prod(self.z[0])==np.prod(self.z[1])
        self.S=np.prod(self.z[0]);self.dims=[nc]*3+[nb]*3;self.N=int(np.prod(self.dims))
        self.eye=sp.eye(self.N,format='csr',dtype=complex)
        self.ops=[]
        for j,dim in enumerate(self.dims):
            O=sp.csr_matrix([[1.]])
            for k,d in enumerate(self.dims):
                a=sp.diags(np.sqrt(np.arange(1,d)),1,shape=(d,d),format='csr') if j==k else sp.eye(d,format='csr')
                O=sp.kron(O,a,format='csr')
            self.ops.append(O)
        self.c=self.ops[:3];self.b=self.ops[3:]
        self.num=[O.conj().T@O for O in self.ops]
        self.top=[]
        for j,dim in enumerate(self.dims):
            self.top.append(np.array([np.unravel_index(k,self.dims)[j]==dim-1 for k in range(self.N)]))
        # Represent Hamiltonians as coefficient-weighted fixed sparse terms.
        self.hops=[];self.spec=[]
        def term(O,spec,hermitian_pair=True):
            self.hops.append(O);self.spec.append((spec,False))
            if hermitian_pair:self.hops.append(O.conj().T);self.spec.append((spec,True))
        for j in range(3):
            term(self.c[j]@self.b[j].conj().T,('beam',j))
            term(self.c[j]@self.c[j],('local_sq',j))
            term(self.c[j]@self.c[j]@self.b[j].conj().T,('cubic2',j))
            term(self.num[j],('det',j),False)
            term(self.c[j],('odd_linear',j))
        for j,k in itertools.combinations(range(3),2):term(self.c[j]@self.c[k],('desired_pair',j,k))
        term(self.c[0]@self.c[1]@self.c[2],('cubic3',))
        # All lower-weight drives, retaining constants, linears and quadratics.
        for q,R in enumerate(model.Rs):
            for nr in range(len(R)+1):
                for subset in itertools.combinations(R,nr):
                    O=self.eye
                    for j in subset:O=O@self.c[j]
                    term(O,('paras',q,subset))
        term(self.eye,('odd_constant',),False)
        self.combine=SparseLinearCombination(self.hops)
        self.decay=np.zeros(self.N)
        for b in self.b:
            self.decay+=(model.gamma*(b.conj().T@b)+model.heat*(b@b.conj().T)).diagonal().real
        self.loss=.5*(self.decay[:,None]+self.decay[None,:])
        self.ref_t,self.ref_a=classical_trajectory(model,z=self.z[:1],include_parasitics=False,include_odd=False)

    def H(self,t):
        m=self.model;A,B=np.split(trajectory_at(self.ref_t,self.ref_a,t)[0],2)
        th,dth=m.phases_at(t);on=t<m.drive_time
        odd=dth[None,:]*m.odd*self.z if on else np.zeros_like(self.z)
        common=dth*m.eps_common if on else np.zeros(3)
        _,para,_=controls(m,t,self.z)
        allH=[]
        for k in range(2):
            co=[]
            for spec,conj in self.spec:
                kind=spec[0]
                if kind=='beam':v=2*m.g2*A[spec[1]]
                elif kind=='local_sq':v=m.g2*B[spec[1]].conjugate()
                elif kind=='cubic2':v=m.g2
                elif kind=='det':v=common[spec[1]]+odd[k,spec[1]]
                elif kind=='odd_linear':v=odd[k,spec[1]]*A[spec[1]].conjugate()
                elif kind=='desired_pair':v=m.g3*self.S*A[3-spec[1]-spec[2]] if on else 0.
                elif kind=='cubic3':v=m.g3*self.S if on else 0.
                elif kind=='odd_constant':v=np.dot(odd[k],abs(A)**2)
                elif kind=='paras':
                    _,q,subset=spec;other=[j for j in m.Rs[q] if j not in subset]
                    v=para[q][k]*(np.prod(A[other]) if other else 1.)
                else:raise ValueError(kind)
                co.append(np.conj(v) if conj else v)
            allH.append(self.combine(co))
        return allH

    def rhs(self,t,rho):
        H=self.H(t);order=[(0,0),(1,1),(0,1)] if self.diagonals else [(0,1)]
        out=np.empty_like(rho)
        for i,(l,r) in enumerate(order):
            out[i]=-1j*(H[l]@rho[i]-(H[r].T@rho[i].T).T)-self.loss*rho[i]
        for b in self.b:
            for i in range(len(rho)):
                out[i]+=self.model.gamma*(b.conj()@(b@rho[i]).T).T
                out[i]+=self.model.heat*(b.T@(b.conj().T@rho[i]).T).T
        return out

    def run(self,label):
        m=self.model;thermal=np.ones(1)
        for d in self.dims:
            prob=(.001/1.001)**np.arange(d);prob/=prob.sum();thermal=np.kron(thermal,prob)
        rho=np.tile(np.diag(thermal).astype(complex),(3 if self.diagonals else 1,1,1))
        t=0.;stop=m.drive_time+m.ringdown;steps=0;start=time.monotonic()
        max_top=np.zeros((2,6));max_pop=np.zeros((2,6));traceerr=0.;snaps=[]
        while t<stop-1e-11:
            boundary=min(m.drive_time,(np.floor((t+1e-9)/m.segment)+1)*m.segment) if t<m.drive_time-1e-10 else stop
            dt=min(m.dt,boundary-t,stop-t)
            if dt<1e-10:t=boundary;continue
            k1=self.rhs(t+1e-10,rho);k2=self.rhs(t+dt/2,rho+dt*k1/2)
            k3=self.rhs(t+dt/2,rho+dt*k2/2);k4=self.rhs(t+dt-1e-10,rho+dt*k3)
            rho+=dt*(k1+2*k2+2*k3+k4)/6
            t+=dt;steps+=1
            if self.diagonals:
                diag=np.diagonal(rho[:2],axis1=-2,axis2=-1).real
                top=np.array([[np.sum(diag[k][q]) for q in self.top] for k in range(2)])
                pop=np.array([[np.dot(diag[k],q.diagonal().real) for q in self.num] for k in range(2)])
                max_top=np.maximum(max_top,top);max_pop=np.maximum(max_pop,pop)
                traceerr=max(traceerr,abs(diag.sum(axis=1)-1).max())
            if steps%(m.steps_per_segment*16)==0 or t>=stop-1e-10:
                w=np.trace(rho[-1]);snaps.append({'time':t,'trace':[w.real,w.imag],'visibility':float(abs(w))})
                print(json.dumps({'case':label,'time':t,'visibility_loss':float(1-abs(w)),'seconds':time.monotonic()-start}),flush=True)
        w=np.trace(rho[-1]);out={'label':label,'scope':'Full cubic Hamiltonian, six modes, finite displaced-Fock truncation; no analytic truncation error certificate.',
            'pair':list(self.pair),'branches':self.z.tolist(),'N':self.N,'storage_cutoff':self.nc,'buffer_cutoff':self.nb,
            'model_parameters':{k:getattr(m,k) for k in ('n','g2','g3','gamma','heat','nu','delta','eps_common','odd','u','drive_time','ringdown','dt')},
            'full_trace':[float(w.real),float(w.imag)],'visibility':float(abs(w)),'visibility_loss':float(1-abs(w)),
            'runtime_seconds':time.monotonic()-start,'steps':steps,'diagonal_audit_performed':self.diagonals,
            'trace_preservation_max_error':float(traceerr) if self.diagonals else None,
            'max_top_level_probability':max_top.tolist() if self.diagonals else None,
            'max_fluctuation_population':max_pop.tolist() if self.diagonals else None,'snapshots':snaps}
        folder=Path(__file__).parent;(folder/f'nonlinear_fock_{label}_results.json').write_text(json.dumps(out,indent=2)+'\n')
        print(json.dumps(out,indent=2),flush=True)
        return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',choices=['mod','unmod'],default='mod')
    p.add_argument('--nc',type=int,default=3);p.add_argument('--nb',type=int,default=2)
    p.add_argument('--cycles',type=int,default=16);p.add_argument('--ringdown',type=float,default=60.)
    p.add_argument('--steps',type=int,default=16);p.add_argument('--label',default=None)
    p.add_argument('--cross-only',action='store_true');p.add_argument('--odd',type=float,default=.0001)
    a=p.parse_args();m=Model(modulated=a.case=='mod',odd=a.odd,cycles=a.cycles,steps_per_segment=a.steps);m.ringdown=a.ringdown
    sim=FullFock(m,a.nc,a.nb,diagonals=not a.cross_only)
    sim.run(a.label or f'{a.case}_c{a.nc}_b{a.nb}')
