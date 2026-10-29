"""Floating diagnostic of PROOF.md; NOT a random-bit exact sampler.

Rotating marked Maxwell covariance dual and a bounded contour-ratio query.
No producer module is imported. Huber's credited linear factory is a direct
implementation of arXiv:1308.1562v2 Section 2.2, including its initialization
order (threshold uses the supplied margin before the .644 update).
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from math import exp, log, log1p, sqrt, cos, sin, pi, isfinite
from typing import Callable
import numpy as np


@dataclass
class Counts:
    queries: int = 0
    degree: int = 0
    max_degree: int = 0
    blocks: int = 0
    splits: int = 0
    rotations: int = 0
    singleton_uniform: int = 0
    initial_draws: int = 0
    proposals: int = 0
    factory_coins: int = 0
    factory_levels: int = 0

    def json(self):
        return asdict(self)


def unit(rng):
    x = rng.normal(size=3)
    return x / np.linalg.norm(x)


def perpendicular(n, rng):
    # Fixed chart, fresh uniform azimuth; no preferred physical orientation.
    axis = np.array([0., 0., 1.]) if abs(n[2]) < .8 else np.array([1., 0., 0.])
    a = np.cross(n, axis)
    a /= np.linalg.norm(a)
    b = np.cross(n, a)
    phi = 2*pi*rng.random()
    return cos(phi)*a + sin(phi)*b


def direction_pair(n, u, rng):
    z = perpendicular(n, rng)
    p, q = sqrt(u), sqrt(1-u)
    return p*n+q*z, q*n-p*z


def moment_sample(k: int, direction, t: float, initial_e: Callable,
                  rng, counts: Counts | None = None,
                  discard_rotations: bool = False, terminal_sample=None):
    """Bounded H with mean E(n^T E_t n)^k; discard flag is NEGATIVE CONTROL."""
    if k < 0 or not isinstance(k, (int, np.integer)) or not isfinite(t) or t < 0:
        raise ValueError('finite t>=0 and integer k>=0 required')
    if k == 0:
        return 1.
    n = np.asarray(direction, float)
    if n.shape != (3,) or abs(n@n-1) > 1e-10:
        raise ValueError('real unit direction required')
    counts = counts if counts is not None else Counts()
    stack = [(int(k), n, t)]
    value = 1.
    visited = splits = terminal_mass = 0
    while stack:
        q, n, remaining = stack.pop()
        counts.blocks += 1
        visited += 1
        if q == 1:
            if not discard_rotations and rng.random() >= exp(-remaining/2):
                n = unit(rng)
                counts.singleton_uniform += 1
            duration, separates = remaining, False
        else:
            wait = rng.exponential((q+1)/(q-1))
            duration = min(wait, remaining)
            separates = wait < remaining
            if not discard_rotations:
                rotations = int(rng.poisson(2*duration/(q+1)))
                counts.rotations += rotations
                for _ in range(rotations):
                    u = rng.beta(q+1, 1)
                    n, _ = direction_pair(n, u, rng)
        if not separates:
            if terminal_sample is None:
                e = np.asarray(initial_e(rng), float)
                x = float(n @ e @ n)
                if abs(x) > 1+1e-10:
                    raise ArithmeticError('input/direction bound violated; not clipped')
                terminal = x**q
            else:
                terminal = terminal_sample(q,n,rng)
                if abs(terminal) > 1+1e-10:
                    raise ArithmeticError('terminal sample bound violated; not clipped')
            value *= terminal
            terminal_mass += q
            counts.initial_draws += 1
        else:
            j = int(rng.integers(1, q))
            u = rng.beta(j+1, q-j+1)
            left, right = direction_pair(n, u, rng)
            stack.append((j, left, remaining-duration))
            stack.append((q-j, right, remaining-duration))
            counts.splits += 1
            splits += 1
    if visited > 2*k-1 or splits > k-1 or terminal_mass != k:
        raise AssertionError('finite degree accounting failed')
    return value


@dataclass
class CovarianceModel:
    matrices: np.ndarray
    probabilities: np.ndarray
    a: float
    b: float

    def __post_init__(self):
        self.matrices = np.asarray(self.matrices, float)
        self.probabilities = np.asarray(self.probabilities, float)
        if not (0 < self.a < self.b < 7*self.a/5):
            raise ValueError('receiver requires 0<a<b<7a/5')
        if self.matrices.shape != (len(self.probabilities), 3, 3):
            raise ValueError('covariance/probability shape')
        if np.any(self.probabilities < 0) or abs(sum(self.probabilities)-1) > 1e-12:
            raise ValueError('probabilities')
        for s in self.matrices:
            if np.max(abs(s-s.T)) > 1e-12:
                raise ValueError('symmetry')
            eig = np.linalg.eigvalsh(s)
            if eig[0] < self.a-1e-12 or eig[-1] > self.b+1e-12:
                raise ValueError('initial eigenvalue bracket')
        self.c = (self.a+self.b)/2
        self.h = (self.b-self.a)/2
        self.beta = self.c-4*self.h
        self.g = self.c+4*self.h
        self.C = (self.g/self.beta)**1.5
        self.es = (self.matrices-self.c*np.eye(3))/self.h
        self.mean_cov = np.einsum('i,ijk->jk', self.probabilities, self.matrices)
        self.mu = np.trace(self.mean_cov)/3
        self.cholesky = np.linalg.cholesky(self.matrices)

    def draw_e(self, rng):
        return self.es[int(rng.choice(len(self.es), p=self.probabilities))]

    def draw_initial(self, rng):
        i = int(rng.choice(len(self.es), p=self.probabilities))
        return self.cholesky[i] @ rng.normal(size=3)

    def covariance(self, t):
        return self.mu*np.eye(3)+exp(-t/2)*(self.mean_cov-self.mu*np.eye(3))

    def lower(self, v):
        return (self.g/self.b)**1.5*exp(-float(v@v)*(1/self.a-1/self.g)/2)

    def bounds(self):
        integral = (self.a*self.b/(self.g*(2*self.a-self.g)))**1.5
        degree = 6*self.h*(1/self.beta+self.a/(self.g*(2*self.a-self.g)))
        return dict(a=self.a,b=self.b,c=self.c,h=self.h,beta=self.beta,g=self.g,
                    C=self.C,I=integral,queries=19*self.C**2*integral,
                    total_degree=19*self.C**2*integral*degree)

    def moment(self,k,n,t,rng,counts):
        return moment_sample(k,n,t,self.draw_e,rng,counts)


@dataclass
class ResolvedVelocityModel:
    """Symmetric bounded initial velocities, with DECLARED Gaussian variance s.

    Represents the exact Maxwell solution initialized by mu_0 * G_s;
    equivalently the declared Gaussian-resolved output of the core solution.
    This is a different target from the unsmoothed core law.
    """
    positive_points: np.ndarray
    probabilities: np.ndarray
    radius: float
    variance: float

    def __post_init__(self):
        self.positive_points=np.asarray(self.positive_points,float)
        self.probabilities=np.asarray(self.probabilities,float)
        if self.positive_points.shape!=(len(self.probabilities),3):
            raise ValueError('symmetric table shape')
        if self.radius<=0 or self.variance<=4*self.radius**2:
            raise ValueError('require s>4R^2')
        if any(self.probabilities<0) or abs(sum(self.probabilities)-1)>1e-12:
            raise ValueError('probabilities')
        if max(np.linalg.norm(self.positive_points,axis=1))>self.radius*(1+1e-12):
            raise ValueError('supplied radius violated')
        self.c=self.variance
        self.h=self.radius**2
        self.beta=self.c-4*self.h
        self.g=self.c+4*self.h
        self.C=(self.g/self.beta)**1.5
        self.energy=float(np.einsum('i,ij,ij',self.probabilities,
                                   self.positive_points,self.positive_points))
        self.core_cov=np.einsum('i,ij,ik->jk',self.probabilities,
                                self.positive_points,self.positive_points)
        self.mu=self.energy/3

    def draw_core(self,rng):
        i=int(rng.choice(len(self.probabilities),p=self.probabilities))
        return self.positive_points[i]*(1 if rng.random()<.5 else -1)

    def draw_initial(self,rng):
        return self.draw_core(rng)+sqrt(self.variance)*rng.normal(size=3)

    def terminal(self,q,n,rng):
        projection=float(n@self.draw_core(rng))/self.radius
        value=1.
        for j in range(1,q+1): value*=projection**2/(2*j-1)
        return value

    def moment(self,k,n,t,rng,counts):
        return moment_sample(k,n,t,None,rng,counts,terminal_sample=self.terminal)

    def covariance(self,t):
        return ((self.variance+self.mu)*np.eye(3)
                +exp(-t/2)*(self.core_cov-self.mu*np.eye(3)))

    def lower(self,v):
        return (exp(-self.energy/(2*self.variance))*(self.g/self.variance)**1.5
                *exp(-float(v@v)*(1/self.variance-1/self.g)/2))

    def bounds(self):
        integral=(exp(self.energy/(2*self.variance))
                  *(self.variance**2/(self.g*(2*self.variance-self.g)))**1.5)
        degree=6*self.h*(1/self.beta+self.variance/(self.g*(2*self.variance-self.g)))
        return dict(radius=self.radius,variance=self.variance,energy=self.energy,
                    beta=self.beta,g=self.g,C=self.C,I=integral,
                    queries=19*self.C**2*integral,
                    total_degree=19*self.C**2*integral*degree)


def ratio_sample(v, t, model: CovarianceModel, rng, counts: Counts):
    counts.queries += 1
    xi = rng.normal(size=3)/sqrt(model.beta)
    z = xi-1j*np.asarray(v)/model.g
    norm2 = float(np.vdot(z,z).real)
    k = int(rng.poisson(2*model.h*norm2))
    counts.degree += k
    counts.max_degree = max(counts.max_degree, k)
    phase = (model.c/model.g-1)*float(xi@v)
    if k == 0:
        return model.C*cos(phase)
    theta = 2*pi*rng.random()
    vtheta = (z.real*cos(theta)+z.imag*sin(theta))/sqrt(norm2)
    norm = float(np.linalg.norm(vtheta))
    if norm == 0:
        return 0.
    h = model.moment(k, vtheta/norm, t, rng, counts)
    result = model.C*((-1)**k)*cos(phase+2*k*theta)*norm**(2*k)*h
    if abs(result) > model.C*(1+1e-10):
        raise ArithmeticError('bounded ratio failed; not clipped')
    return result


def linear_factory(coin, epsilon, rng, counts: Counts, multiplier=2.):
    """Huber 2014 v2, Section 2.2. Expected input <=9.5C/epsilon."""
    if not (0 < epsilon < 1 and multiplier > 1):
        raise ValueError('factory parameters')
    gamma = .5
    threshold = 2.3/(gamma*epsilon)  # Before min update: published order.
    epsilon = min(epsilon, .644)
    i, c = 1, float(multiplier)
    while True:
        counts.factory_levels += 1
        while True:
            counts.factory_coins += 1
            b = coin()
            geometric = int(rng.geometric((c-1)/c))
            i += -1+(1-int(b))*geometric
            if i == 0 or i >= threshold:
                break
        if i == 0:
            return 1
        if log(rng.random()) >= -i*log1p(gamma*epsilon):
            return 0
        c *= 1+gamma*epsilon
        epsilon *= 1-gamma
        threshold /= 1-gamma


def sample_velocity(t, model, rng, counts=None):
    counts = counts if counts is not None else Counts()
    while True:
        counts.proposals += 1
        v = sqrt(model.g)*rng.normal(size=3)
        margin = model.lower(v)/model.C
        if margin <= 0 or not isfinite(margin):
            raise ArithmeticError('floating factory margin underflow; not silently exact')
        def coin():
            w = ratio_sample(v,t,model,rng,counts)
            p = (1-w/model.C)/2
            if not 0 <= p <= 1:
                raise ArithmeticError('factory coin outside [0,1]')
            return rng.random() < p
        if not linear_factory(coin,margin,rng,counts):
            return v


def wild_velocity(t, model, rng):
    """Ordinary exact ideal Wild ancestry; no equilibrium truncation."""
    stack = [('node',float(t))]
    values = []
    leaves = collisions = 0
    while stack:
        kind, remaining = stack.pop()
        if kind == 'combine':
            a, b = values.pop(), values.pop()
            values.append((a+b+np.linalg.norm(a-b)*unit(rng))/2)
            collisions += 1
        else:
            wait = rng.exponential()
            if wait >= remaining:
                values.append(model.draw_initial(rng))
                leaves += 1
            else:
                stack.extend([('combine',0),('node',remaining-wait),('node',remaining-wait)])
    if len(values) != 1 or leaves != collisions+1:
        raise AssertionError('Wild accounting')
    return values[0], leaves


def declared_model():
    angle = pi/4
    r = np.array([[cos(angle),-sin(angle),0],[sin(angle),cos(angle),0],[0,0,1.]])
    matrices = np.array([np.diag([1.,1.05,1.1]), r@np.diag([1.08,1.,1.05])@r.T])
    return CovarianceModel(matrices,np.array([.5,.5]),1.,1.1)
