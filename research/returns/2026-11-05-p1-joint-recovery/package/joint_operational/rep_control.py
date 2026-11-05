"""SU(2) covariant channels in irreducible Choi multiplicity coordinates."""
from control_search import *


def spin_rep(j):
    d=int(round(2*j+1));z=np.diag(np.arange(j,-j-1,-1));plus=np.zeros((d,d),complex)
    for col in range(1,d):
        mag=j-col;plus[col-1,col]=np.sqrt((j-mag)*(j+mag+1))
    return plus,z


def tensor_rep(a,b):
    pa,za=a;pb,zb=b;da=len(pa);db=len(pb)
    return np.kron(pa,np.eye(db))+np.kron(np.eye(da),pb),np.kron(za,np.eye(db))+np.kron(np.eye(da),zb)


def rep_blocks(plus,z,allowed=None):
    d=len(plus);weights=np.rint(2*np.diag(z).real).astype(int)
    assert la.norm(z-np.diag(weights/2))<1e-10
    answer=[]
    for twice_j in range(int(max(weights)),-1,-2):
        j=twice_j/2
        if allowed is not None and not any(abs(j-x)<1e-8 for x in allowed):continue
        ids=np.flatnonzero(weights==twice_j);upids=np.flatnonzero(weights==twice_j+2)
        highest=la.null_space(plus[np.ix_(upids,ids)],rcond=1e-11);mult=highest.shape[1]
        if not mult:continue
        spin=twice_j+1;highs=np.zeros((d,mult),complex);highs[ids,:]=highest;cols=[]
        for a in range(mult):
            v=highs[:,a];cols.append(v);mag=j
            for _ in range(spin-1):
                v=plus.conj().T@v/np.sqrt((j+mag)*(j-mag+1));mag-=1;cols.append(v)
        u=np.stack(cols,axis=1)
        assert la.norm(u.conj().T@u-np.eye(mult*spin))<1e-9
        answer.append((j,mult,spin,u))
    if allowed is None:
        u=np.concatenate([v for _,_,_,v in answer],axis=1)
        assert la.norm(u@u.conj().T-np.eye(d))<1e-9
    return answer


class RepChannel:
    def __init__(self,rep_in,rep_out,allowed=None,solver='CLARABEL',tol=1e-8):
        pi,zi=rep_in;po,zo=rep_out;self.d=len(pi);self.o=len(po);self.solver=solver;self.tol=tol
        plus=np.kron(po,np.eye(self.d))-np.kron(np.eye(self.o),pi.T)
        z=np.kron(zo,np.eye(self.d))-np.kron(np.eye(self.o),zi.T)
        self.blocks=rep_blocks(plus,z,allowed)
        self.bases=[u.reshape(self.o,self.d,m,s).transpose(2,3,0,1) for _,m,s,u in self.blocks]
        self.bigbases={};self.x=[cp.Variable((m,m),hermitian=True) for _,m,s,u in self.blocks]
        self.h=[cp.Parameter((m,m),hermitian=True) for _,m,s,u in self.blocks]
        self.constraint_coeffs=[];self.constraint_targets=[]
        for _,r,s,v in rep_blocks(-pi.T,-zi.T):
            for a in range(r):
                va=v[:,a*s:(a+1)*s];self._add_constraint(va@va.conj().T/s,1.)
                for b in range(a+1,r):
                    vb=v[:,b*s:(b+1)*s];ab=va@vb.conj().T/s
                    self._add_constraint((ab+ab.conj().T)/2,0.)
                    self._add_constraint((ab-ab.conj().T)/(2j),0.)
        constraints=[x>>0 for x in self.x]
        for coeff,target in zip(self.constraint_coeffs,self.constraint_targets):
            constraints.append(sum(cp.real(cp.trace(c@x)) for c,x in zip(coeff,self.x))==target)
        objective=sum(cp.real(cp.trace(h@x)) for h,x in zip(self.h,self.x))
        self.problem=cp.Problem(cp.Maximize(objective),constraints)
        gram=np.array([[sum(trace_pair(a,b) for a,b in zip(ca,cb)) for cb in self.constraint_coeffs] for ca in self.constraint_coeffs])
        self.gram_pinv=la.pinvh(gram);self.calls=0;self.seconds=0.;self.statuses={}
    def _operator_coeffs(self,t):
        return [herm(np.einsum('auoi,ij,buoj->ab',k.conj(),t,k,optimize=True)) for k in self.bases]
    def _add_constraint(self,t,target):
        self.constraint_coeffs.append(self._operator_coeffs(t));self.constraint_targets.append(target)
    def coeff_from_kraus(self,kraus):
        a=np.stack([k.reshape(-1) for k in kraus],axis=1);result=[]
        for _,m,s,u in self.blocks:
            b=(u.conj().T@a).reshape(m,s,len(kraus))
            result.append(herm(np.einsum('aik,bik->ab',b,b.conj())/s))
        return result
    def coeff_from_choi(self,j):
        return [herm(np.einsum('aibi->ab',(u.conj().T@j@u).reshape(m,s,m,s))/s) for _,m,s,u in self.blocks]
    def dense_choi(self,coeff):
        return herm(sum(u@np.kron(x,np.eye(s))@u.conj().T for x,(_,m,s,u) in zip(coeff,self.blocks)))
    def big_bases(self,h):
        if h not in self.bigbases:
            self.bigbases[h]=[np.array([[np.kron(np.eye(h),k[a,mu]) for mu in range(k.shape[1])] for a in range(k.shape[0])]) for k in self.bases]
        return self.bigbases[h]
    def kraus(self,coeff,h=1):
        result=[]
        for x,k in zip(coeff,self.big_bases(h)):
            w,v=la.eigh(herm(x));keep=w>1e-13;a=v[:,keep]*np.sqrt(np.maximum(w[keep],0))
            result.extend(np.einsum('ar,auij->ruij',a,k,optimize=True).reshape(-1,h*self.o,h*self.d))
        return np.array(result)
    def apply(self,rho,coeff):
        h=rho.shape[0]//self.d;k=self.kraus(coeff,h)
        return herm(np.sum((k@rho)@k.conj().transpose(0,2,1),axis=0))
    def adjoint(self,b,coeff):
        h=b.shape[0]//self.o;k=self.kraus(coeff,h)
        return herm(np.sum((k.conj().transpose(0,2,1)@b)@k,axis=0))
    def cost(self,rho,b):
        h=rho.shape[0]//self.d;result=[]
        for k in self.big_bases(h):
            bkx=(b@k)@rho;result.append(herm(np.einsum('auij,buij->ab',k.conj(),bkx,optimize=True)))
        return result
    def score(self,coeff,cost):return sum(trace_pair(x,g) for x,g in zip(coeff,cost))
    def marginal(self,coeff):
        k=self.kraus(coeff)
        return herm(np.sum(k.conj().transpose(0,2,1)@k,axis=0).T)
    def repair(self,coeff):
        positive=[]
        for x in coeff:
            w,v=la.eigh(herm(x));positive.append(herm((v*np.maximum(w,0))@v.conj().T))
        a=self.marginal(positive);w,v=la.eigh(a)
        if min(w)<1e-12:raise RuntimeError('Singular trace-preservation marginal')
        r=(v/np.sqrt(w))@v.conj().T;lifts=self._operator_coeffs(r)
        return [herm((lift/s)@x@(lift/s)) for lift,x,(_,_,s,_) in zip(lifts,positive,self.blocks)]
    def solve(self,cost,old=None):
        projections=np.array([sum(trace_pair(c,g) for c,g in zip(coeff,cost)) for coeff in self.constraint_coeffs])
        weights=self.gram_pinv@projections
        centered=[g-sum(weights[k]*self.constraint_coeffs[k][j] for k in range(len(weights))) for j,g in enumerate(cost)]
        scale=np.sqrt(sum(la.norm(x,'fro')**2 for x in centered))
        if scale<2e-14 and old is not None:return old,dict(status='flat',gain=0.,scale=float(scale))
        for par,g in zip(self.h,centered):par.value=herm(g/max(scale,1e-14))
        if old is not None:
            for x,v in zip(self.x,old):x.value=v
        start=time.perf_counter()
        try:
            if self.solver=='CLARABEL':self.problem.solve(solver='CLARABEL',warm_start=True,tol_gap_abs=self.tol,tol_gap_rel=self.tol,tol_feas=self.tol,max_iter=150)
            else:self.problem.solve(solver='SCS',warm_start=True,eps=self.tol,max_iters=5000)
        except cp.error.SolverError:self.problem.solve(solver='SCS',warm_start=False,eps=self.tol,max_iters=10000)
        elapsed=time.perf_counter()-start;self.calls+=1;self.seconds+=elapsed
        self.statuses[self.problem.status]=self.statuses.get(self.problem.status,0)+1
        if any(x.value is None for x in self.x):raise RuntimeError(self.problem.status)
        raw=[herm(x.value) for x in self.x];rawmin=min(float(la.eigvalsh(x)[0]) for x in raw)
        candidate=self.repair(raw);gain=None if old is None else self.score(candidate,cost)-self.score(old,cost)
        rejected=gain is not None and gain < -2e-11
        if rejected:candidate=old
        return candidate,dict(status=self.problem.status,gain=gain,scale=float(scale),seconds=elapsed,rejected=rejected,raw_min_eigenvalue=rawmin)
