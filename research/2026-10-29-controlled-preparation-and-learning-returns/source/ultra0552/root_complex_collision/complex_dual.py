"""Direct complex-mark operation. Floating diagnostics, no bit-exact claim."""
from dataclasses import dataclass
from math import exp,sqrt,cos,sin,pi
import importlib.util,sys
from pathlib import Path
import numpy as np

sys.dont_write_bytecode=True
_p=Path(__file__).resolve().parents[1]/'t_collision_operation'/'angular_dual.py'
_s=importlib.util.spec_from_file_location('root_factory_source',_p)
_a=importlib.util.module_from_spec(_s);sys.modules[_s.name]=_a;_s.loader.exec_module(_a)
Counts=_a.Counts

def rotation(rng):
    w,x,y,z=rng.normal(size=4);r=sqrt(w*w+x*x+y*y+z*z);w/=r;x/=r;y/=r;z/=r
    return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],
                     [2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],
                     [2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])

def complex_moment(q,z,t,draw_e,rng,count):
    if q==0:return 1.+0j
    stack=[(q,np.asarray(z,complex),t)];out=1.+0j
    while stack:
        q,z,left=stack.pop();count.blocks+=1
        if q==1:
            e=draw_e(rng);count.initial_draws+=1
            out*=z@e@z if rng.random()<exp(-left/2) else np.trace(e)/3*(z@z)
            continue
        wait=rng.exponential()
        if wait>=left:
            e=draw_e(rng);count.initial_draws+=1;out*=(z@e@z)**q
            continue
        count.rotations+=1;r=rotation(rng)
        za=(z+r.T@z)/2;zb=(z-r.T@z)/2
        ua=float(np.vdot(za,za).real);ub=float(np.vdot(zb,zb).real)
        assert abs(ua+ub-1)<1e-10
        # Sum normalization only pays floating drift; exact theorem has ua+ub=1.
        j=int(rng.binomial(q,ua/(ua+ub)))
        if j:stack.append((j,za/sqrt(ua),left-wait))
        if j<q:stack.append((q-j,zb/sqrt(ub),left-wait))
        if 0<j<q:count.splits+=1
    assert abs(out)<=1+1e-9
    return out

@dataclass
class Model:
    matrices:np.ndarray
    probabilities:np.ndarray
    a:float
    b:float
    def __post_init__(self):
        self.matrices=np.asarray(self.matrices,float);self.probabilities=np.asarray(self.probabilities,float)
        assert 0<self.a<self.b and abs(self.probabilities.sum()-1)<1e-12
        for s in self.matrices:
            assert np.max(abs(s-s.T))<1e-12
            e=np.linalg.eigvalsh(s);assert e[0]>=self.a-1e-12 and e[-1]<=self.b+1e-12
        self.c=(self.a+self.b)/2;self.h=(self.b-self.a)/2;self.C=(self.b/self.a)**1.5
        self.es=(self.matrices-self.c*np.eye(3))/self.h
        self.mean=np.einsum('i,ijk->jk',self.probabilities,self.matrices);self.mu=np.trace(self.mean)/3
    def draw_e(self,rng):return self.es[int(rng.choice(len(self.es),p=self.probabilities))]
    def covariance(self,t):return self.mu*np.eye(3)+exp(-t/2)*(self.mean-self.mu*np.eye(3))

def ratio(v,t,model,rng,count):
    count.queries+=1;xi=rng.normal(size=3)/sqrt(model.a);z=xi-1j*v/model.b
    r2=float(np.vdot(z,z).real);q=int(rng.poisson(model.h*r2/2))
    count.degree+=q;count.max_degree=max(count.max_degree,q)
    h=complex_moment(q,z/sqrt(r2),t,model.draw_e,rng,count) if q else 1.+0j
    phase=(model.c/model.b-1)*float(xi@v)
    value=model.C*(((-1)**q)*(cos(phase)+1j*sin(phase))*h).real
    assert abs(value)<=model.C*(1+1e-9)
    return value

def exact_velocity(t,model,rng,count):
    if not model.b<2*model.a:raise ValueError('this exact expected-cost receiver needs b<2a')
    while True:
        count.proposals+=1;v=sqrt(model.b)*rng.normal(size=3)
        ell=exp(-float(v@v)*(1/model.a-1/model.b)/2)
        if ell==0:raise ArithmeticError('floating margin underflow')
        def coin():return rng.random()<(1-ratio(v,t,model,rng,count)/model.C)/2
        if not _a.linear_factory(coin,ell/model.C,rng,count):return v

def approximate_velocity(t,model,queries,rng,count):
    while True:
        count.proposals+=1;v=sqrt(model.b)*rng.normal(size=3)
        average=sum(ratio(v,t,model,rng,count) for _ in range(queries))/queries
        # This clipping is the DEFINED approximate algorithm, not hidden numerical repair.
        if rng.random()<min(model.C,max(0,average))/model.C:return v

def model(a=1.,b=1.8):
    r=np.array([[cos(pi/4),-sin(pi/4),0],[sin(pi/4),cos(pi/4),0],[0,0,1.]])
    h=b-a
    ss=np.array([np.diag([a,a+.5*h,b]),r@np.diag([a+.9*h,a+.1*h,a+.4*h])@r.T])
    return Model(ss,np.array([.5,.5]),a,b)
