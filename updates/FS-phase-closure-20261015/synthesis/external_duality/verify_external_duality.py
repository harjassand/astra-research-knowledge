#!/usr/bin/env python3
"""Finite exact algebra only. Analytic theorems are proved in the report."""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import subprocess

import sympy as sp

ROOT=Path(__file__).resolve().parent
ASTRA=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-phase-closure-20261015')
PIN='846f185763ed3a27310fad4ce9471ba324d1e5f4'


def main():
    actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ASTRA,text=True).strip()
    assert actual==PIN
    a1,a2,k1,k2,z1,z2,r,N=sp.symbols('a1 a2 k1 k2 z1 z2 r N',nonzero=True,real=True)
    av=sp.Matrix([a1,a2]);zv=sp.Matrix([z1,z2]);params=(a1,a2,k1,k2)
    monomials=[]
    for powers in itertools.product(range(5),repeat=4):
        if sum(powers)!=4:continue
        f=sp.prod(v**p for v,p in zip(params,powers))
        monomials.append(f)
        j=sp.Matrix([sp.diff(f,a1),sp.diff(f,a2)])
        h=sp.expand(r**4*f.subs({a1:z1/r,a2:z2/r}))
        for i,z in enumerate((z1,z2)):
            assert sp.expand(sp.diff(h,z)-r**3*j[i].subs({a1:z1/r,a2:z2/r}))==0
        expected=r**3*(4*f-(av.dot(j)))
        assert sp.expand(sp.diff(h,r)-expected.subs({a1:z1/r,a2:z2/r}))==0
        assert sp.expand(f.subs(dict(zip(params,[N*v for v in params])))-N**4*f)==0
    assert len(monomials)==35

    fv,aj,D,lam=sp.symbols('f aj D lambda',real=True)
    # div(r^3 j)=r^3(div j+3 a.j), and partial_r h=r^3(4f-a.j).
    euler=-(D+3*aj)+(4*fv-aj)-4*lam
    residual=fv-aj-D/4
    assert sp.expand(euler-4*(residual-lam))==0
    assert sp.expand(-D/4-(aj-fv)-residual)==0

    # Exact constant-phase dual for the supplied G, using rows [a;k].
    A=sp.Matrix([[a1,a2],[k1,k2]])
    u=a1*a1+k1*k1;v=a2*a2+k2*k2;q=A.det()
    G=3*(u+v-2*q)**2+sp.Rational(35,24)*u*u+q*q-sp.Rational(5,2)*q*u
    f=G.subs({k1:0,k2:1})
    value=sp.simplify(f.subs({a1:0,a2:0}))
    slope=[sp.simplify(sp.diff(f,a).subs({a1:0,a2:0})) for a in (a1,a2)]
    assert value==3 and slope==[-12,0]

    # Terminal positivity is an inequality set, not a linear subspace.
    s,t=sp.symbols('s t',real=True)
    Q=sp.Matrix([[0,sp.Rational(1,2)],[sp.Rational(1,2),0]])
    assert sp.expand((sp.Matrix([s,t]).T*Q*sp.Matrix([s,t]))[0]-s*t)==0
    assert (s*t).subs({s:1,t:-1})==-1
    assert (s*t).subs({s:1,t:1})==1
    assert Q.det()==-sp.Rational(1,4)

    # mu=0 convex counterexample: F(A)=|A e1|^4, n=e1, r=r(y).
    ry=sp.symbols('r_y',real=True)
    badA=sp.Matrix([[0,ry],[0,0]])
    assert (badA[:,0].dot(badA[:,0]))**2==0

    # Rough-direction logarithmic test: exact derivative and Euler signs.
    x=sp.symbols('x',real=True)
    rr=sp.Function('r')(x);eta=sp.Function('eta')(x)
    eps=sp.symbols('epsilon',positive=True)
    psi=eta**4/(rr+eps)**3
    expected_dpsi=4*eta**3*sp.diff(eta,x)/(rr+eps)**3-3*eta**4*sp.diff(rr,x)/(rr+eps)**4
    assert sp.simplify(sp.diff(psi,x)-expected_dpsi)==0
    aa,zz,cc=sp.symbols('A_grad_eta A_grad_r Czero',real=True)
    lhs=3*eta**4*zz/(rr+eps)**4
    rhs=4*eta**3*aa/(rr+eps)**3+eta**4*cc/(rr+eps)**3-4*lam*eta**4*rr**3/(rr+eps)**3
    euler_test=4*eta**3*aa/(rr+eps)**3-3*eta**4*zz/(rr+eps)**4+eta**4*cc/(rr+eps)**3-4*lam*eta**4*rr**3/(rr+eps)**3
    assert sp.simplify(rhs-lhs-euler_test)==0
    mu=sp.symbols('mu',positive=True)
    X,B,constant,mroot=sp.symbols('X B C mroot',real=True)
    budget_remainder=mu*X**4/4-constant*B*X**2*mroot+constant**2*B**2*mroot**2/mu
    assert sp.expand(budget_remainder-(mu*X**2-2*constant*B*mroot)**2/(4*mu))==0

    output={
        'status':'PASS',
        'scope':'finite exact identities only; Harnack, mass-value convexity, weak dual attainment and boundary trace are analytic arguments in report',
        'astra_pin':actual,
        'quartic_monomials_checked':len(monomials),
        'Euler_flux_residual_factor':'4',
        'constant_phase_G_value':str(value),
        'constant_phase_G_flux':[str(x) for x in slope],
        'terminal_toy_quadratic_determinant':'-1/4',
        'global_negative_replication_energy_factor':'N^4',
        'rough_logarithmic_test_derivative_and_Euler_signs':'exact identity PASS',
        'paid_phase_budget_Young_completion':'exact square PASS',
        'rough_phase_budget':'E >= mu X^4/4-C(K^8+K^4)M',
        'primary_harnack_source':'E. DiBenedetto and N. S. Trudinger (1984), Corollary 3, printed p307',
        'positive_rank_one_bound':'explicit input mu>0; automatic classification not imported',
        'dual_flux_class':'L^(4/3), divergence in L^1; global positive groundstate required',
        'smooth_dual_attainment':'NOT CLAIMED',
        'full_quasiconvexity':'OPEN',
        'historical_novelty':'UNKNOWN',
        'external_review':'UNKNOWN'
    }
    (ROOT/'verification.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
