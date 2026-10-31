"""Adaptive spectral decision envelope, via vector actions and explicit LPs.

The learner sees only coefficient matvecs and conservative norm/noise bounds.
It uses a randomized, fully reorthogonalized Lanczos implementation, with the
classical exact-arithmetic gap-free iteration count. The fixed coherent action
errors are bounded operators; double roundoff is audited numerically rather than
claimed to be an interval-arithmetic implementation. The theorem file supplies
a conservative construction for general query-dependent bounded noise.

The generator is diagonal plus rank-one for fast simulation. H0 has simple
spectrum and H1 has all off-diagonal entries nonzero, so the generated algebra
is the full matrix algebra. The learner does not receive those factors.
"""
import json
import math
import argparse
import os
import time
from pathlib import Path

import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import linprog

OUT = Path(__file__).parent


def clip(poly, a, b, tol=1e-10):
    if len(poly) == 0:
        return []
    answer = []
    for p, q in zip(poly, poly[1:] + poly[:1]):
        fp, fq = float(a @ p - b), float(a @ q - b)
        pin, qin = fp <= tol, fq <= tol
        if pin:
            answer.append(p)
        if pin != qin:
            answer.append(p + (q-p)*(fp/(fp-fq)))
    return answer


def cells_and_vertices(planes):
    cells, vertices = [], {}
    for j, plane in enumerate(planes):
        poly = [np.array([-1.,-1.]), np.array([1.,-1.]),
                np.array([1.,1.]), np.array([-1.,1.])]
        for k, other in enumerate(planes):
            if k != j:
                poly = clip(poly, plane[1:]-other[1:], other[0]-plane[0])
        if poly:
            cells.append(poly)
            for point in poly:
                vertices[tuple(np.round(point, 10))] = point
    return cells, list(vertices.values())


class Experiment:
    def __init__(self, n=1024, facets=7, seed=4, nu=.004, eta=.0001):
        self.n, self.rng, self.nu, self.eta = n, np.random.default_rng(seed), nu, eta
        angles = 2*np.pi*np.arange(facets)/facets
        self.base_planes = np.c_[.8+.08*np.sin(3*angles), .7*np.cos(angles), .7*np.sin(angles)]
        group = np.arange(n) % facets
        self.diags = self.base_planes[group].T.copy()
        # H0 has simple spectrum with probability one.
        self.diags[0] += nu*self.rng.uniform(-1,1,n)
        self.ranks = [None]
        for _ in range(2):
            w = self.rng.normal(size=n)
            w /= np.linalg.norm(w)
            self.ranks.append(w)
        self.bias = eta*self.rng.uniform(-1,1,(3,n))
        self.bounds = np.max(np.abs(self.base_planes),axis=0) + nu + eta
        self.action_calls = 0

    def action(self, i, v):
        self.action_calls += 1
        out = (self.diags[i]+self.bias[i])*v
        if i:
            w = self.ranks[i]
            out += self.nu*w*np.dot(w,v)
        return out

    def observed_pencil_action(self, u, v):
        out = self.action(0,v)
        for i in range(2):
            if u[i]:
                out += u[i]*self.action(i+1,v)
        return out

    def audit_base(self, u):
        return float(np.min(self.base_planes[:,0]+self.base_planes[:,1:]@u))

    def audit_model_radius(self,u):
        return self.nu*(1+np.abs(u).sum())


class Learner:
    def __init__(self, action, n, bounds, eta, epsilon=.06, tau=.006, confidence=.01, seed=713):
        self.action, self.n, self.bounds = action, n, bounds
        self.eta, self.mu, self.epsilon, self.tau = eta, 3*eta, epsilon, tau
        self.confidence, self.rng = confidence, np.random.default_rng(seed)
        self.queries, self.steps, self.oracle_log = 0, 0, []
        self.cache = {}

    def matvec(self,u,v):
        z=self.action(0,v)
        for i in range(2):
            if u[i]:
                z+=u[i]*self.action(i+1,v)
        return z

    def oracle(self,u):
        key=tuple(np.round(u,10))
        if key in self.cache:
            return self.cache[key]
        self.queries+=1
        delta=6*self.confidence/(np.pi**2*self.queries**2)
        B=float(self.bounds[0]+np.abs(u)@self.bounds[1:])
        # Kuczynski-Wozniakowski-style gap-free randomized Lanczos bound.
        # The convenient published form targets absolute error tau/2; this is
        # more conservative than the tau error subtracted below.
        k=min(self.n,1+math.ceil(.5*math.log(2.75*self.n/delta**2)*math.sqrt(B/self.tau)))
        Q=np.zeros((self.n,k))
        q=self.rng.normal(size=self.n)
        q/=np.linalg.norm(q)
        alphas,betas=[],[]
        previous=np.zeros(self.n)
        beta=0.
        for j in range(k):
            Q[:,j]=q
            w=self.matvec(u,q)-beta*previous
            alpha=float(q@w)
            w-=alpha*q
            # Two passes prevent loss of orthogonality.
            for _ in range(2):
                w-=Q[:,:j+1]@(Q[:,:j+1].T@w)
            alphas.append(alpha)
            next_beta=float(np.linalg.norm(w))
            if next_beta<1e-13 or j==k-1:
                break
            betas.append(next_beta)
            previous,q=q,w/next_beta
            beta=next_beta
        used=len(alphas)
        self.steps+=used
        values,vecs=eigh_tridiagonal(np.asarray(alphas),np.asarray(betas),select='i',select_range=(0,0))
        v=Q[:,:used]@vecs[:,0]
        v/=np.linalg.norm(v)
        expectations=np.array([v@self.action(i,v) for i in range(3)])
        observed=float(expectations[0]+u@expectations[1:])
        local_noise=self.eta*(1+np.abs(u).sum())
        lower=observed-self.tau-local_noise
        plane=expectations.copy()
        plane[0]+=self.mu
        answer=(lower,plane)
        self.cache[key]=answer
        residual=float(np.linalg.norm(self.matvec(u,v)-observed*v))
        self.oracle_log.append(dict(u=u.tolist(),iterations=used,lower=lower,
                                    residual=residual,delta=delta))
        return answer

    def acquire(self):
        _,first=self.oracle(np.zeros(2))
        planes=[first]
        history=[]
        while True:
            cells,verts=cells_and_vertices(planes)
            # Boundary and cell corners, not a user-supplied grid.
            worst=0.
            for z in verts:
                lower,plane=self.oracle(z)
                F=float(np.min(np.asarray(planes)[:,0]+np.asarray(planes)[:,1:]@z))
                gap=F-lower
                worst=max(worst,gap)
                if gap>self.epsilon:
                    planes.append(plane)
                    history.append(dict(planes=len(planes),u=z.tolist(),failed_gap=gap))
                    break
            else:
                return np.asarray(planes),verts,worst,history


def solve_task(planes,c,constraints=None):
    A=np.c_[-planes[:,1:],np.ones(len(planes))]
    b=planes[:,0]
    if constraints:
        C,h=constraints
        A=np.vstack([A,np.c_[C,np.zeros(len(C))]])
        b=np.r_[b,h]
    res=linprog(np.r_[c,-1.],A_ub=A,b_ub=b,bounds=[(-1,1),(-1,1),(None,None)],method='highs')
    if not res.success:
        raise RuntimeError(res.message)
    return res.x[:2],-res.fun


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--n',type=int,default=1024)
    args=parser.parse_args()
    model=Experiment(n=args.n)
    learner=Learner(model.action,model.n,model.bounds,model.eta)
    start=time.perf_counter()
    planes,verts,vertex_gap,history=learner.acquire()
    acquire_seconds=time.perf_counter()-start
    # Independent dense control grid is an audit, not used for acquisition.
    axis=np.linspace(-1,1,151)
    grid=np.array([(x,y) for x in axis for y in axis])
    envelope=np.min(planes[:,0,None]+planes[:,1:]@grid.T,axis=0)
    base=np.min(model.base_planes[:,0,None]+model.base_planes[:,1:]@grid.T,axis=0)
    radius=model.nu*(1+np.abs(grid).sum(axis=1))
    uniform_gap_upper=float(np.max(envelope-base+radius))
    lower_gap_bound=float(np.min(envelope-base-radius))
    # Future costs and additional resource constraints are generated after learning.
    calls_before=model.action_calls
    rng=np.random.default_rng(911)
    tasks=[]
    online_start=time.perf_counter()
    for j in range(60):
        c=rng.uniform(-.55,.55,2)
        C=np.array([[1.,.6],[-.3,1.]])
        h=np.array([rng.uniform(.1,1.5),rng.uniform(.1,1.2)])
        u,V=solve_task(planes,c,(C,h))
        # Latent simple model gives an independent upper bound on true optimum:
        # |f-f0| <= 3*nu uniformly. Base LP optimum +3nu is an upper bound.
        _,baseV=solve_task(model.base_planes,c,(C,h))
        true_value_lower=model.audit_base(u)-model.audit_model_radius(u)-float(c@u)
        tasks.append(dict(c=c.tolist(),u=u.tolist(),certificate_interval=[V-learner.epsilon,V],
                          independent_regret_bound=float(baseV+3*model.nu-true_value_lower)))
    online_seconds=time.perf_counter()-online_start
    result=dict(n=model.n,control_dimension=2,base_facets=len(model.base_planes),
                epsilon=learner.epsilon,coherent_action_error_per_operator=model.eta,
                generic_perturbation_norm_per_operator=model.nu,
                learned_planes=len(planes),final_cell_vertices=len(verts),
                spectral_queries=learner.queries,lanczos_steps=learner.steps,
                full_vector_coefficient_actions=model.action_calls,
                full_column_reconstruction_action_baseline=3*model.n,
                stored_envelope_scalars=int(planes.size),
                explicit_dense_coefficient_scalars=3*model.n**2,
                acquisition_seconds=acquire_seconds,certified_max_vertex_gap=vertex_gap,
                independent_grid_gap_upper_bound=uniform_gap_upper,
                independent_grid_lower_gap_bound=lower_gap_bound,
                future_tasks=len(tasks),future_experimental_actions=model.action_calls-calls_before,
                total_future_lp_seconds=online_seconds,
                max_independent_future_regret_bound=max(t['independent_regret_bound'] for t in tasks),
                max_lanczos_residual=max(t['residual'] for t in learner.oracle_log),
                caveat='Lanczos confidence bound is exact-arithmetic; floating-point audit is empirical. General bounded-noise constructive oracle is proved separately.',
                planes=planes.tolist(),history=history,tasks=tasks,oracle_log=learner.oracle_log)
    (OUT/f'results_n{args.n}.json').write_text(json.dumps(result,indent=2))
    brief={k:v for k,v in result.items() if k not in ('planes','history','tasks','oracle_log')}
    print(json.dumps(brief,indent=2))
    # Publication-style artifact, with no image synthesis involved.
    os.environ.setdefault('MPLCONFIGDIR','producer-workspace/spectral_envelope_matplotlib')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(10,4),constrained_layout=True)
    cells,_=cells_and_vertices(planes)
    for poly in cells:
        arr=np.vstack([poly,poly[0]])
        axes[0].plot(arr[:,0],arr[:,1],color='#235789',lw=1)
    acquisitions=np.array([h['u'] for h in history])
    if len(acquisitions):
        axes[0].scatter(acquisitions[:,0],acquisitions[:,1],color='#c1292e',s=22,zorder=3)
    axes[0].set(xlabel='control u1',ylabel='control u2',title=f'{len(planes)} learned witness planes; {model.n} physical states',aspect='equal')
    im=axes[1].imshow((envelope-base+radius).reshape(len(axis),len(axis)).T,
                      extent=[-1,1,-1,1],origin='lower',vmin=0,vmax=learner.epsilon,cmap='viridis',aspect='equal')
    axes[1].set(xlabel='control u1',ylabel='control u2',title='Independent upper bound on envelope error')
    fig.colorbar(im,ax=axes[1],label='margin error')
    fig.savefig(OUT/f'envelope_demo_n{args.n}.png',dpi=180)


if __name__=='__main__':
    main()
