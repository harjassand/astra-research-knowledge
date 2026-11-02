"""Sharp finite-history operational recovery for passive rooted TREE networks.

Each edge has inverse constitutive law phi_e(flow) and a warranted finite-range
slope band lo_e <= secant phi <= hi_e, with phi_e(0)=0. All terminal injections
and terminal voltages use the same unknown physical laws.

This implementation is a research fixture, uses floating HiGHS (not certified
rational arithmetic), and returns independent LP lower/upper values and dual
finite-data transport witness. The *mathematical* equivalences are proven in
companion research notes.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from scipy.optimize import linprog
from scipy import sparse


@dataclass
class RootedTree:
    """C[e,port]=1 iff port is downstream of edge, edge directed from root."""
    C: np.ndarray
    lo: np.ndarray
    hi: np.ndarray

    def __post_init__(self):
        self.C = np.asarray(self.C, float)
        self.lo = np.asarray(self.lo, float)
        self.hi = np.asarray(self.hi, float)
        assert self.C.ndim == 2 and set(np.unique(self.C)).issubset({0., 1.})
        assert self.C.shape[0] == len(self.lo) == len(self.hi)
        assert np.all(self.lo > 0.) and np.all(self.hi >= self.lo)

    @property
    def edges(self): return len(self.lo)
    @property
    def ports(self): return self.C.shape[1]
    @property
    def m(self): return (self.lo + self.hi)/2
    @property
    def d(self): return (self.hi-self.lo)/2

    def edge_flows(self, p):
        p=np.asarray(p,float)
        return p @ self.C.T

    def centered_voltage(self,p):
        flows=self.edge_flows(p)
        return (flows*self.m) @ self.C

    def actual_voltage(self,p,edge_inverse):
        p=np.asarray(p,float)
        flows=self.edge_flows(p)
        return np.array([sum(self.C[e,b]*edge_inverse[e](flows[e]) for e in range(self.edges))
                         for b in range(self.ports)])


@dataclass
class Observations:
    ports: np.ndarray      # integer index
    experiments: np.ndarray  # integer index into p_hist
    value: np.ndarray
    error: np.ndarray

    def __post_init__(self):
        self.ports=np.asarray(self.ports,int)
        self.experiments=np.asarray(self.experiments,int)
        self.value=np.asarray(self.value,float)
        self.error=np.asarray(self.error,float)
        assert len(self.ports)==len(self.experiments)==len(self.value)==len(self.error)
        assert np.all(self.error>=0)


class TreeTaskLP:
    def __init__(self,tree,p_hist,p_future,obs,task_weights):
        self.tree=tree
        self.p_hist=np.asarray(p_hist,float)
        self.p_future=np.asarray(p_future,float)
        self.task_weights=np.asarray(task_weights,float)
        self.obs=obs
        assert self.p_hist.ndim==2 and self.p_hist.shape[1]==tree.ports
        assert self.p_future.shape==(tree.ports,) and self.task_weights.shape==(tree.ports,)
        assert np.all((obs.ports>=0)&(obs.ports<tree.ports))
        assert np.all((obs.experiments>=0)&(obs.experiments<len(self.p_hist)))
        self.hist_flows=tree.edge_flows(self.p_hist)
        self.future_flows=tree.edge_flows(self.p_future)
        self.midtask=float(self.task_weights @ tree.centered_voltage(self.p_future))
        centered = tree.centered_voltage(self.p_hist)
        self.y=obs.value-centered[obs.experiments,obs.ports]
        self._build_primal()

    def _build_primal(self):
        tr=self.tree
        self.knots=[]; self.colmap={}
        col=0
        for e in range(tr.edges):
            knots=np.unique(np.r_[0.,self.hist_flows[:,e],self.future_flows[e]])
            self.knots.append(knots)
            for t in knots:
                if t!=0.:
                    self.colmap[(e,float(t))]=col;col+=1
        self.n=col
        def term(row,e,t,v):
            if float(t)!=0.:
                k=self.colmap[(e,float(t))]
                row[k]=row.get(k,0.)+float(v)
        rows=[];rhs=[]
        for e,knots in enumerate(self.knots):
            for s,t in zip(knots[:-1],knots[1:]):
                v={};term(v,e,t,+1.);term(v,e,s,-1.)
                rows.extend((v,{k:-z for k,z in v.items()}))
                rhs.extend((tr.d[e]*(t-s),tr.d[e]*(t-s)))
        self.n_lipschitz=len(rows)
        for z in range(len(self.obs.value)):
            h=self.obs.experiments[z]; b=self.obs.ports[z]
            v={}
            for e in np.flatnonzero(tr.C[:,b]):
                term(v,e,self.hist_flows[h,e],tr.C[e,b])
            rows.extend((v,{k:-val for k,val in v.items()}))
            rhs.extend((self.y[z]+self.obs.error[z],-self.y[z]+self.obs.error[z]))
        rr=[];cc=[];vv=[]
        for i,row in enumerate(rows):
            for j,z in row.items():
                if z!=0.:rr.append(i);cc.append(j);vv.append(z)
        self.A=sparse.coo_matrix((vv,(rr,cc)),shape=(len(rows),col)).tocsr()
        self.rhs=np.asarray(rhs)
        self.c=np.zeros(col)
        w=tr.C @ self.task_weights
        for e in range(tr.edges):
            if self.future_flows[e]!=0.:
                self.c[self.colmap[(e,float(self.future_flows[e]))]]+=w[e]

    def conditional(self):
        out=[]
        for sense in (1.,-1.):
            r=linprog(sense*self.c,A_ub=self.A,b_ub=self.rhs,
                      bounds=[(None,None)]*self.n,method='highs')
            if not r.success:
                raise RuntimeError('Conditional LP did not finish: '+r.message)
            out.append((self.midtask+float(self.c@r.x),r))
        return out[0][0],out[1][0],out

    def construct_source(self,optimizer_result):
        """A full constructive conventional IDENTIFICATION comparator.

        Given one feasible optimal LP solution, return *whole* stationary
        piecewise-affine edge laws. These are explicit physical-source
        witnesses attaining one task endpoint; both are equally informed
        potential hidden systems, not a unique truth estimate.
        """
        assert optimizer_result.success
        values=np.asarray(optimizer_result.x,float)
        laws=[]
        for e,knots in enumerate(self.knots):
            residuals=np.array([0. if float(t)==0. else values[self.colmap[(e,float(t))]]
                                for t in knots])
            m=float(self.tree.m[e]);k=knots.copy();v=residuals.copy()
            # Continuation by a zero-slope centered residual outside the
            # union of sampled flows preserves the source's inverse slope band.
            laws.append(lambda x,k=k,v=v,m=m:m*x+float(np.interp(x,k,v)))
        return laws

    def _dual_rows(self):
        """Rows for anchored one-dimensional KR norm: |a_g - B_g @gamma|."""
        tr=self.tree;nobs=len(self.obs.value)
        T=tr.C @ self.task_weights
        aa=[]; BB=[]; dd=[]
        for e,knots in enumerate(self.knots):
            # Signed atomic measure coefficient of task at the future knot,
            # minus selected past boundary readouts. On interval (s,t),
            # use cumulative mass to the RIGHT (the anchor mass at zero is immaterial).
            for s,t in zip(knots[:-1],knots[1:]):
                a=T[e]*(int(self.future_flows[e]>s)-int(0.>s))
                b=np.array([tr.C[e,self.obs.ports[k]]*(int(self.hist_flows[self.obs.experiments[k],e]>s)-int(0.>s))
                            for k in range(nobs)],float)
                if a!=0. or np.any(b!=0.):
                    aa.append(a);BB.append(b);dd.append(tr.d[e]*(t-s))
        return np.asarray(aa,float),np.asarray(BB,float).reshape((-1,nobs)),np.asarray(dd,float)

    def dual_certificate(self,sign=1.,minimax=False):
        """Upper certificate on sign*(task-midtask), or global minimax radius.

        The dual uses gamma signed, plus abs(B gamma-a) and abs(gamma)
        variables. This is a *source-complete* LP dual, not a generic loose bound.
        """
        a,B,d=self._dual_rows()
        a=sign*a
        ng=len(a); nh=len(self.obs.value)
        # variables gamma[nh], t_abs[ng], v_abs[nh]
        if ng:
            # B gamma - t <= a  /  -B gamma -t<= -a
            R1=sparse.hstack([sparse.csr_matrix(B),-sparse.eye(ng),sparse.csr_matrix((ng,nh))])
            R2=sparse.hstack([-sparse.csr_matrix(B),-sparse.eye(ng),sparse.csr_matrix((ng,nh))])
        else:
            R1=sparse.csr_matrix((0,2*nh));R2=R1
        R3=sparse.hstack([sparse.eye(nh),sparse.csr_matrix((nh,ng)),-sparse.eye(nh)])
        R4=sparse.hstack([-sparse.eye(nh),sparse.csr_matrix((nh,ng)),-sparse.eye(nh)])
        # B gamma - t<=a, -B gamma -t<= -a indeed t>=|B gamma-a|
        mat=sparse.vstack([R1,R2,R3,R4],format='csr')
        rhs=np.r_[a,-a,np.zeros(2*nh)]
        obj=np.r_[np.zeros(nh) if minimax else self.y,d,self.obs.error]
        bounds=[(None,None)]*nh+[(0,None)]*(ng+nh)
        r=linprog(obj,A_ub=mat,b_ub=rhs,bounds=bounds,method='highs')
        if not r.success: raise RuntimeError('Dual LP did not finish: '+r.message)
        val = (0. if minimax else sign*self.midtask) + r.fun
        return val,r.x[:nh],r

    def no_history(self):
        tr=self.tree
        baseline=self.midtask
        halfwidth=np.sum(np.abs((tr.C@self.task_weights)*self.future_flows)*tr.d)
        return baseline-halfwidth,baseline+halfwidth


def star_quotient(n_service, series_length=1,calibration=True):
    """One common trunk and n branches, with arbitrary serial refinements.
    Series subedges share the same subtree indicator. This representation
    has exactly same external response class as collapsing to effective edges
    when the interval bands of the series elements are summed.
    """
    ports=n_service+int(calibration)
    lines=[];lo=[];hi=[]
    for _ in range(series_length):
        lines.append(np.ones(ports));lo.append(.10/series_length);hi.append(.50/series_length)
    for i in range(ports):
        v=np.zeros(ports);v[i]=1.
        for _ in range(series_length):
            lines.append(v);lo.append(.30/series_length);hi.append(.80/series_length)
    return RootedTree(np.array(lines),np.array(lo),np.array(hi))


if __name__=='__main__':
    # Small nontrivial tree: four service ports plus one calibration branch;
    # two single-port experiments predict a first-time *simultaneous* task.
    t=star_quotient(4,series_length=1,calibration=True)
    S=.48; q=np.array([.12,.12,.12,.12,0.])
    ref=np.array([0.,0.,0.,0.,S])
    probe=np.array([q[0],0.,0.,0.,0.])
    def functions(e):
        if e==0: return lambda z:.12*z+.09*z*abs(z)
        return lambda z:(.35+.01*(e%4))*z+.07*z*abs(z)
    fs=[functions(e) for e in range(t.edges)]
    p_hist=np.array([ref,probe]); y=np.array([t.actual_voltage(p,fs) for p in p_hist])
    ob=Observations(ports=[1,0,1],experiments=[0,1,1],value=[y[0,1],y[1,0],y[1,1]],error=[1e-4]*3)
    c=np.zeros(t.ports);c[0]=1
    P=TreeTaskLP(t,p_hist,q,ob,c)
    lo,hi,_=P.conditional()
    upper,gup,_=P.dual_certificate(1.)
    lowneg,glow,_=P.dual_certificate(-1.)
    rho,grho,_=P.dual_certificate(minimax=True)
    print('star quotient, true x0:',t.actual_voltage(q,fs)[0])
    print('source-complete conditional interval:',lo,hi)
    print('dual bounds:',-lowneg,upper,'minimax radius:',rho,'gamma:',grho)
    print('no-history:',P.no_history())
    assert abs(hi-upper)<1e-8 and abs(lo+lowneg)<1e-8
    assert lo-1e-9 <= t.actual_voltage(q,fs)[0] <= hi+1e-9
