"""Direct complex marked receiver for symmetric INITIAL VELOCITY laws.

The direct complex covariance kernel is root's construction, whole-reviewed
in ROOT_COMPLEX_REVIEW.md. This explicit physical-even-moment adapter is
new code. All implementations are floating diagnostics of an ideal theorem.
"""
from dataclasses import dataclass
from math import exp,sqrt,cos,sin
import importlib.util,sys
from pathlib import Path
import numpy as np
from angular_dual import Counts,linear_factory
from initial_oracle import moment as product_moment

_path=Path(__file__).resolve().parents[1]/'root_complex_collision'/'complex_dual.py'
_spec=importlib.util.spec_from_file_location('resolved_root_rotation',_path)
_root=importlib.util.module_from_spec(_spec);sys.modules[_spec.name]=_root;_spec.loader.exec_module(_root)
rotation=_root.rotation  # Ordinary Gaussian-quaternion Haar primitive only.


@dataclass
class Work(Counts):
    genealogical_blocks:int=0
    terminal_queries:int=0
    singleton_trace:int=0
    source_polynomial_multiplies:int=0


class BoundedSymmetricSource:
    def __init__(self,points,probabilities,radius):
        self.points=np.asarray(points,float);self.probabilities=np.asarray(probabilities,float)
        assert self.points.shape==(len(self.probabilities),3)
        assert np.all(self.probabilities>=0) and abs(sum(self.probabilities)-1)<1e-12
        assert radius>0 and max(np.linalg.norm(self.points,axis=1))<=radius*(1+1e-12)
        self.radius=radius;self.kappa=radius**2
        self.cov=np.einsum('i,ij,ik->jk',self.probabilities,self.points,self.points)
        self.energy=float(np.trace(self.cov))

    def draw_core(self,rng):
        v=self.points[int(rng.choice(len(self.points),p=self.probabilities))]
        return v*(1 if rng.random()<.5 else -1)

    def terminal(self,q,z,rng,count):
        count.terminal_queries+=1;count.initial_draws+=1
        v=self.draw_core(rng)
        x2=(z@v/self.radius)**2
        value=1.+0j
        for j in range(1,q+1):value*=x2/(2*j-1)
        return value

    def singleton(self,z,t,rng,count):
        count.terminal_queries+=1;count.initial_draws+=1
        v=self.draw_core(rng)/self.radius
        if rng.random()<exp(-t/2):return (z@v)**2
        count.singleton_trace+=1
        return float(v@v)/3*(z@z)


class ProductSignSource:
    """Optional acquired O(Jq^2) deterministic terminal; no mixture oracle."""
    def __init__(self,vectors,kappa):
        self.vectors=np.asarray(vectors,float);self.kappa=float(kappa)
        assert self.vectors.ndim==2 and self.vectors.shape[1]==3 and self.kappa>0
        self.cov=self.vectors.T@self.vectors
        assert np.linalg.eigvalsh(self.cov)[-1]<=self.kappa*(1+1e-12)
        self.energy=float(np.trace(self.cov))

    def draw_core(self,rng):
        return rng.choice([-1.,1.],size=len(self.vectors))@self.vectors

    def terminal(self,q,z,rng,count):
        count.terminal_queries+=1
        value,work=product_moment(q,z,self.vectors,self.kappa)
        count.source_polynomial_multiplies+=work
        if abs(value)>1+1e-9:raise ArithmeticError('uncertified floating moment outside analytic norm bound')
        return complex(value)

    def singleton(self,z,t,rng,count):
        count.terminal_queries+=1
        if rng.random()<exp(-t/2):return (z@self.cov@z)/self.kappa
        count.singleton_trace+=1
        return self.energy/(3*self.kappa)*(z@z)


class Model:
    def __init__(self,source,variance):
        self.source=source;self.s=float(variance);self.h=source.kappa
        assert self.s>self.h>0
        self.a=self.s-self.h;self.g=self.s+self.h
        self.C=(self.g/self.a)**1.5

    def lower(self,v):
        return exp(-self.source.energy/(2*self.s))*(self.g/self.s)**1.5*exp(
            -float(v@v)*(1/self.s-1/self.g)/2)

    def covariance(self,t):
        mu=self.source.energy/3
        return (self.s+mu)*np.eye(3)+exp(-t/2)*(self.source.cov-mu*np.eye(3))

    def draw_initial(self,rng):
        return self.source.draw_core(rng)+sqrt(self.s)*rng.normal(size=3)

    def bounds(self):
        integral=exp(self.source.energy/(2*self.s))*(self.s**2/(self.g*self.a))**1.5
        degree=1.5*self.h*(1/self.a+self.s/(self.g*self.a))
        return dict(kappa=self.h,s=self.s,beta=self.a,g=self.g,C=self.C,I=integral,
                    queries=19*self.C**2*integral,total_degree=19*self.C**2*integral*degree)


def complex_moment(q,z,t,source,rng,count):
    if q==0:return 1.+0j
    stack=[(q,np.asarray(z,complex),float(t))];out=1.+0j
    count.genealogical_blocks+=1
    while stack:
        q,z,left=stack.pop();count.blocks+=1  # Raw iterations, not genealogical block count.
        if q==1:
            out*=source.singleton(z,left,rng,count)
            continue
        wait=rng.exponential()
        if wait>=left:
            out*=source.terminal(q,z,rng,count)
            continue
        count.rotations+=1
        r=rotation(rng);za=(z+r.T@z)/2;zb=(z-r.T@z)/2
        ua=float(np.vdot(za,za).real);ub=float(np.vdot(zb,zb).real)
        if abs(ua+ub-1)>1e-10:raise ArithmeticError('rotation norm drift')
        j=int(rng.binomial(q,ua/(ua+ub)))  # Floating normalization explicitly not certification.
        if j:stack.append((j,za/sqrt(ua),left-wait))
        if j<q:stack.append((q-j,zb/sqrt(ub),left-wait))
        if 0<j<q:
            count.splits+=1;count.genealogical_blocks+=2
    if abs(out)>1+1e-9:raise ArithmeticError('bounded complex sample failed')
    return out


def ratio(v,t,model,rng,count):
    count.queries+=1
    xi=rng.normal(size=3)/sqrt(model.a);z=xi-1j*v/model.g
    norm2=float(np.vdot(z,z).real);q=int(rng.poisson(model.h*norm2/2))
    count.degree+=q;count.max_degree=max(count.max_degree,q)
    h=complex_moment(q,z/sqrt(norm2),t,model.source,rng,count) if q else 1.+0j
    phase=(model.s/model.g-1)*float(xi@v)
    value=model.C*(((-1)**q)*(cos(phase)+1j*sin(phase))*h).real
    if abs(value)>model.C*(1+1e-9):raise ArithmeticError('ratio bound failed')
    return value


def sample_velocity(t,model,rng,count):
    while True:
        count.proposals+=1;v=sqrt(model.g)*rng.normal(size=3)
        margin=model.lower(v)/model.C
        if margin<=0:raise ArithmeticError('floating factory margin underflow')
        def coin():return rng.random()<(1-ratio(v,t,model,rng,count)/model.C)/2
        if not linear_factory(coin,margin,rng,count):return v
