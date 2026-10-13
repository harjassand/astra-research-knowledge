#!/usr/bin/env python3
"""Reproduce CRAY's mass-action adjoint identities and their failure boundary.

These are synthetic algebra/numerics checks, NOT scientific performance benchmarks.
The fixture's microscopic constants are used only in simulator/oracle validation.
The conjugation controller is given stoichiometry, concentrations, reservoir
activities, baseline gates and a detailed-balance reference (all ones here).
No external data or network access is used.

Dependencies: Python 3.10+, numpy, scipy, sympy.
Run: python verify.py [--output results.json]
"""
from __future__ import annotations
import argparse
import json
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.optimize import root

@dataclass
class Reactor:
    y: np.ndarray         # m x n internal reactant stoichiometry
    yp: np.ndarray        # m x n internal product stoichiometry
    kappa: np.ndarray     # hidden common forward/reverse rate constant; q=1
    gates: np.ndarray
    fuels: np.ndarray    # each channel has its own forward chemostat
    wastes: np.ndarray   # and its own reverse chemostat

    @property
    def S(self) -> np.ndarray:
        return (self.yp-self.y).T

    def fluxes(self,c: np.ndarray) -> tuple[np.ndarray,np.ndarray]:
        if np.any(c<=0):
            raise ValueError('Concentrations must be strictly positive.')
        vf=self.gates*self.kappa*self.fuels*np.exp(self.y@np.log(c))
        vb=self.gates*self.kappa*self.wastes*np.exp(self.yp@np.log(c))
        return vf,vb

    def F(self,c: np.ndarray) -> np.ndarray:
        vf,vb=self.fluxes(c)
        return self.S@(vf-vb)

    def J(self,c: np.ndarray) -> np.ndarray:
        vf,vb=self.fluxes(c)
        return self.S@(vf[:,None]*self.y-vb[:,None]*self.yp)/c[None,:]

    def defect(self,c: np.ndarray) -> np.ndarray:
        vf,vb=self.fluxes(c)
        return np.einsum('r,ri,rj->ij',vf-vb,self.yp,self.yp)-np.einsum('r,ri,rj->ij',vf-vb,self.y,self.y)

    def noise(self,c: np.ndarray) -> np.ndarray:
        vf,vb=self.fluxes(c)
        return (self.S*(vf+vb)[None,:])@self.S.T


def compile_conjugate_controls(y,yp,c,gates,fuels,wastes):
    """Controller: no kappa, reaction flux, Jacobian or fitted kinetic model."""
    gates2=gates*np.exp((y+yp)@np.log(c))*fuels*wastes
    return 1/c,gates2,1/fuels,1/wastes


def fixture(y,yp,c,vf,vb,gates,kappa):
    return Reactor(y,yp,kappa,gates,
                   vf/(gates*kappa*np.exp(y@np.log(c))),
                   vb/(gates*kappa*np.exp(yp@np.log(c))))


def conjugate(r,c):
    d,eg,f,w=compile_conjugate_controls(r.y,r.yp,c,r.gates,r.fuels,r.wastes)
    return d,Reactor(r.y,r.yp,r.kappa.copy(),eg,f,w)


def normmax(a):
    return float(np.max(np.abs(a)))


def balanced_test():
    # Complexes 0, 2A, B, C. Equal positive net current around the last 3.
    y=np.array([[0,0,0],[2,0,0],[0,1,0],[0,0,1]],dtype=float)
    yp=np.array([[2,0,0],[0,1,0],[0,0,1],[2,0,0]],dtype=float)
    c=np.array([1.2,.8,1.5]); gates=np.array([1.,.8,1.1,.9])
    vf=np.array([2.,5.,4.,6.]); vb=np.array([2.,2.,1.,3.])
    r=fixture(y,yp,c,vf,vb,gates,np.array([.8,1.1,.7,1.3]))
    d,rr=conjugate(r,c); J=r.J(c); H=rr.J(d)
    C=np.diag(c); D=np.diag(d); M=r.defect(c); B=r.noise(c)
    a=np.array([.4,1.,.7]); lam=np.linalg.solve(J.T,-a)
    lam_physical=np.linalg.solve(H,-C@a)/d
    currents=vf-vb; grad=currents*(r.S.T@lam)
    affinity=np.log(vf/vb)
    u=affinity*(r.S.T@lam_physical)
    weights=np.array([1.,1.5,.7,1.1])
    ubar=np.dot(weights*gates,u)/np.dot(weights,gates)
    direction=u-ubar
    expected=float(np.sum(currents*affinity*(r.S.T@lam)**2))
    nudge=[]
    for eps in [1e-2,1e-3,1e-4,1e-5]:
        states=[]
        residuals=[]
        for sign in [1.,-1.]:
            sol=root(lambda h: rr.F(d*np.exp(h))+sign*eps*C@a,np.zeros(3),tol=1e-11)
            residual=normmax(rr.F(d*np.exp(sol.x))+sign*eps*C@a)
            if residual>1e-9:
                raise RuntimeError(f'Nudge solve residual {residual}')
            states.append(d*np.exp(sol.x)); residuals.append(residual)
        estimated=(states[0]-states[1])/(2*eps*d)
        nudge.append({'epsilon':eps,'adjoint_max_abs_error':normmax(estimated-lam),
                      'largest_stationarity_residual':max(residuals)})
    # Exact finite relocation at FIXED fluxes: a known-ECM comparator, not novelty.
    h=np.array([.05,-.03,.04])
    # Preserve the zero-affinity exchange: h_A must vanish.
    h[0]=0.
    vfp,vbp=r.fluxes(c*np.exp(h))
    ratio=np.ones(len(vf)); active=np.abs(currents)>1e-12
    ratio[active]=currents[active]/(vfp-vbp)[active]
    # Compare to formula using ONLY affinity, stoichiometry, h.
    rho=np.ones(len(vf))
    rho[active]=(-np.expm1(-affinity[active]))/(
        np.exp(y[active]@h)-np.exp(-affinity[active]+yp[active]@h))
    shifted=Reactor(y,yp,r.kappa,r.gates*rho,r.fuels,r.wastes)
    relocated=shifted.fluxes(c*np.exp(h))
    step=1e-3
    newgates=gates*np.exp(step*u)
    newgates*=np.dot(weights,gates)/np.dot(weights,newgates)
    changed=Reactor(y,yp,r.kappa,newgates,r.fuels,r.wastes)
    sol=root(lambda h: changed.F(c*np.exp(h)),np.zeros(3),tol=1e-11)
    cnew=c*np.exp(sol.x)
    if normmax(changed.F(cnew))>1e-9:
        raise RuntimeError('Finite design step did not reach a steady state.')
    out={
        'finite_step_size':step,
        'finite_step_objective_change':float(a@(cnew-c)),
        'finite_step_budget_error':float(np.dot(weights,newgates-gates)),
        'n_species':3,'n_reversible_pairs':4,'baseline_c':c.tolist(),
        'baseline_vplus':vf.tolist(),'baseline_vminus':vb.tolist(),
        'baseline_F_residual':normmax(r.F(c)),
        'conjugate_F_residual':normmax(rr.F(d)),
        'flux_swap_max_error':max(normmax(rr.fluxes(d)[0]-vb),normmax(rr.fluxes(d)[1]-vf)),
        'transpose_identity_error':normmax(C@J.T-H@D-M),
        'lyapunov_identity_error':normmax(J@C+C@J.T+B-M),
        'M_max_abs':normmax(M),'exact_adjoint_error':normmax(lam_physical-lam),
        'native_max_real_eigenvalue':float(np.linalg.eigvals(J).real.max()),
        'conjugate_max_real_eigenvalue':float(np.linalg.eigvals(H).real.max()),
        'gradient':grad.tolist(),'rate_free_direction':direction.tolist(),
        'budget_derivative':float(np.dot(weights*gates,direction)),
        'objective_derivative':float(grad@direction),
        'sum_of_squares_value':expected,
        'nudge_tests':nudge,
        'max_gate_fold_change':float(max((rr.gates/r.gates).max(),(r.gates/rr.gates).max())),
        'relocation_formula_error':normmax(rho-ratio),
        'relocation_current_error':normmax(relocated[0]-relocated[1]-currents)
    }
    assert out['exact_adjoint_error']<1e-11
    assert out['objective_derivative']>0
    assert abs(out['objective_derivative']-expected)<1e-11
    assert abs(out['budget_derivative'])<1e-11
    return out


def exact_counterexample():
    # Reversible pairs: 0 <-> 2A, A <-> B, B <-> 0.
    # At c=(1,1), vf=(2,3,3), vb=(1,1,1), j=(1,2,2).
    J=sp.Matrix([[-7,1],[3,-4]])
    H=sp.Matrix([[-9,3],[1,-4]])
    M=sp.Matrix([[2,0],[0,0]])
    a=sp.Matrix([1,sp.Rational(3,5)])
    lam=-J.T.inv()*a; naive=-H.inv()*a
    s=sp.Matrix([-1,1]); true_gradient=2*(s.T*lam)[0]
    wrong_gradient=2*(s.T*naive)[0]
    assert J.T==H+M
    assert true_gradient==sp.Rational(-6,125)
    assert wrong_gradient==sp.Rational(2,55)
    return {'J':str(J),'J_conjugate':str(H),'defect':str(M),
        'objective':'A + (3/5) B', 'true_A_to_B_log_gate_derivative':str(true_gradient),
        'naive_prediction':str(wrong_gradient),
        'native_max_real_eigenvalue':float(np.linalg.eigvals(np.array(J,dtype=float)).real.max()),
        'conjugate_max_real_eigenvalue':float(np.linalg.eigvals(np.array(H,dtype=float)).real.max()),
        'exact_sign_reversal_verified':True}


def random_balanced_tests(count=200,seed=1729):
    rng=np.random.default_rng(seed)
    worst={'swap':0.,'transpose':0.,'lyapunov':0.,'adjoint':0.,'M':0.,'stationarity':0.}
    mindot=float('inf')
    for _ in range(count):
        n=int(rng.integers(3,9))
        complexes=np.vstack([np.zeros(n),np.eye(n),2*np.eye(n)])
        k=len(complexes)
        # Connected ring: common nonzero circulation plus independent bidirectional traffic.
        y=complexes.copy(); yp=np.roll(complexes,-1,axis=0)
        traffic=np.exp(rng.uniform(-1,1,k)); current=float(rng.uniform(.2,2))
        vf=traffic+current; vb=traffic
        c=np.exp(rng.uniform(-.4,.4,n)); gates=np.exp(rng.uniform(-.3,.3,k))
        r=fixture(y,yp,c,vf,vb,gates,np.exp(rng.uniform(-.5,.5,k)))
        d,rr=conjugate(r,c); J=r.J(c); H=rr.J(d)
        C=np.diag(c); D=np.diag(d); M=r.defect(c)
        a=rng.normal(size=n); lam=np.linalg.solve(J.T,-a)
        est=np.linalg.solve(H,-C@a)/d
        vf2,vb2=rr.fluxes(d)
        vals={'swap':max(normmax(vf2-vb),normmax(vb2-vf)),
            'transpose':normmax(C@J.T-H@D-M),
            'lyapunov':normmax(J@C+C@J.T+r.noise(c)-M),
            'adjoint':normmax(est-lam),'M':normmax(M),'stationarity':normmax(r.F(c))}
        for key,val in vals.items(): worst[key]=max(worst[key],val)
        assert np.linalg.eigvals(J).real.max()<0
        assert np.linalg.eigvals(H).real.max()<0
        j=vf-vb; A=np.log(vf/vb); u=A*(r.S.T@est)
        direction=u-np.dot(gates,u)/gates.sum()
        gain=float((j*(r.S.T@lam))@direction); mindot=min(mindot,gain)
        assert gain>=-1e-10
    assert max(worst.values())<1e-9
    return {'fixtures':count,'seed':seed,'max_absolute_errors':worst,
            'minimum_objective_derivative':mindot,
            'all_native_and_conjugate_Jacobians_Hurwitz':True}


def non_complex_balanced_zero_defect():
    # b=(-1,3,-3,1) on complexes 0,X,2X,3X has zero moments 0,1,2.
    b=sp.Matrix([-1,3,-3,1])
    moments=[sum(b[k]*k**p for k in range(4)) for p in range(4)]
    assert moments==[0,0,0,6]
    return {'complex_imbalance':[int(t) for t in b],
            'zeroth_through_third_moments':[int(t) for t in moments],
            'meaning':'zero defect is strictly weaker than complex balance; formal higher-order fixture, not elementary chemistry demonstration'}


def saturation_counterexample():
    # Same baseline one-way fluxes, concentrations, gate and equilibrium constant.
    # Unknown saturation changes the conjugate response.
    rows=[]
    for K in [sp.Integer(1),sp.Integer(10)]:
        s,p=sp.Integer(2),sp.Integer(1)
        base_den=1+s/K+p/K
        kappa=base_den   # exactly vf=2, vb=1 at e=1
        sf,pf=1/s,1/p
        e_conj=s*p
        new_den=1+sf/K+pf/K
        j_conj=sp.factor(e_conj*kappa*(sf-pf)/new_den)
        rows.append({'K_S_equals_K_P':str(K),'baseline_one_way_fluxes':['2','1'],
            'mass_action_predicted_conjugate_current':'-1',
            'actual_conjugate_current':str(j_conj)})
    assert rows[0]['actual_conjugate_current']=='-8/5'
    assert rows[1]['actual_conjugate_current']=='-26/23'
    return rows


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',default='results.json')
    args=ap.parse_args()
    results={'status':'Synthetic reproducibility checks only; no physical experiment or speedup claim.',
       'balanced_example':balanced_test(),'exact_counterexample':exact_counterexample(),
       'random_complex_balanced_checks':random_balanced_tests(),
       'strict_boundary_example':non_complex_balanced_zero_defect(),
       'saturation_counterexample':saturation_counterexample()}
    out=Path(args.output); out.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__': main()
