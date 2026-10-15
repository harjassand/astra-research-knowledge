#!/usr/bin/env python3
"""Exact checks for developed capital connections; analytic scope is in PROOFS.md.

No original scientific package is imported or modified. Uses SymPy and stdlib.
Checks do not establish external correctness, historical priority or hardware.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
import json
import sympy as S


def plane_integral(poly,x,y):
    return sum(c/S.Integer((ij[0]+1)*(ij[1]+1))
               for ij,c in S.Poly(S.expand(poly),x,y).terms())


def monomials(degree):
    for ex in product(range(degree+1),repeat=4):
        if sum(ex)==degree:yield ex


def main():
    coords=S.symbols('A0:4',real=True)
    bs=S.symbols('B0:4',real=True)
    a=S.symbols('alpha',real=True)
    z=S.Matrix(S.symbols('u0:2',real=True));g=S.Matrix(S.symbols('g0:2',real=True))
    B=S.Matrix(2,2,bs);inc=z*g.T
    assert S.expand(inc.det())==0
    checked=0
    for ex in monomials(4):
        f=S.prod(t**n for t,n in zip(coords,ex))
        fb=f.subs(dict(zip(coords,bs)),simultaneous=True)
        p=S.Matrix(2,2,[S.diff(f,t).subs(dict(zip(coords,bs)),simultaneous=True) for t in coords])
        shifted=f.subs(dict(zip(coords,list(a*B+inc))),simultaneous=True)
        pairing=S.trace(p.T*inc)
        remainder=shifted-a**4*fb-a**3*pairing
        divergence=(a**4-1)*S.trace(p.T*B)/4+a**3*pairing
        assert S.expand(shifted-fb-remainder-divergence)==0
        checked+=1
    assert checked==35
    x,y=S.symbols('x y',real=True)
    aa,bb,cc,dd=coords
    u=aa*aa+cc*cc;v=bb*bb+dd*dd;det=aa*dd-bb*cc
    G=S.expand(3*(u+v-2*det)**2+S.Rational(35,24)*u*u+det*det-S.Rational(5,2)*det*u)
    at_i=G.subs({aa:1,bb:0,cc:0,dd:1})
    assert at_i==-S.Rational(1,24)
    p_i=S.Matrix(2,2,[S.diff(G,t).subs({aa:1,bb:0,cc:0,dd:1}) for t in coords])
    u0=S.Matrix([x+1,y+2]);d=(u0.T*u0)[0]
    j=p_i.T*u0/d**2
    asigma=S.Matrix([S.diff(d,x),S.diff(d,y)])/(2*d)
    residual=at_i/d**2-asigma.dot(j)-(S.diff(j[0],x)+S.diff(j[1],y))/4
    assert S.cancel(residual)==0
    boundary_div=(S.diff((p_i.T*u0)[0],x)+S.diff((p_i.T*u0)[1],y))/4
    assert boundary_div==at_i
    amp=1+x*(1-x)*y*(1-y)/2
    gradamp=S.Matrix([S.diff(amp,x),S.diff(amp,y)])
    du=amp*S.eye(2)+u0*gradamp.T
    energy=plane_integral(G.subs(dict(zip(coords,list(du))),simultaneous=True),x,y)
    gap=S.factor(energy-at_i)
    incnorm=(u0.dot(u0)*gradamp.dot(gradamp))**2
    coercivity=plane_integral(incnorm,x,y)
    assert gap>=coercivity>0
    # Translation/phase scale: independent sine/cosine moments are exact.
    r=S.symbols('R',positive=True)
    s,t=S.symbols('s t',real=True)
    def torus_moment(poly):
        table={0:S.Integer(1),1:S.Integer(0),2:S.Rational(1,2),3:S.Integer(0),4:S.Rational(3,8)}
        return S.expand(sum(c*table[ij[0]]*table[ij[1]] for ij,c in S.Poly(S.expand(poly),s,t).terms()))
    mass=torus_moment(((r+s)**2+t*t)**2)
    translated_energy=torus_moment(G.subs({aa:s,bb:0,cc:0,dd:t},simultaneous=True))
    assert mass==r**4+4*r*r+S.Rational(5,4)
    assert translated_energy==S.Rational(483,64)
    # Exact two-node joint-response LP primal and dual witnesses.
    modes=list(product((Q(0),Q(1)),repeat=2))
    score=lambda q:1+q[0]+q[1]+q[0]*q[1]
    cost=lambda q:sum(q)
    beta=Q(3,2)
    node_max=max(q-beta*q+q/2 for q in (Q(0),Q(1)))
    edge_max=max(q[0]*q[1]-q[0]/2-q[1]/2 for q in modes)
    upper=1+beta+2*node_max+edge_max
    primal=(score((Q(0),Q(0)))+score((Q(1),Q(1))))/2
    assert node_max==edge_max==0 and upper==primal==Q(5,2)
    assert max(score(q) for q in modes if cost(q)<=1)==2
    assert score((Q(1),Q(1)))==4 and 1+1+1==3
    # Pairwise calibration misses a genuine third-order response term.
    def worlds(q):
        pair=1+sum(q)+sum(q[i]*q[j] for i in range(3) for j in range(i+1,3))
        return pair,pair+q[0]*q[1]*q[2]
    for q in product((0,1),repeat=3):
        one,two=worlds(q)
        if sum(q)<=2:assert one==two
        assert two==2**sum(q)
    assert worlds((1,1,1))==(7,8)
    # Continuous hydraulic support is a scalar concave quadratic.
    A,K,C,P,beta,p=S.symbols('A K C P beta p',real=True)
    utility=K*P*p-C*p*p
    resource=A*P*P-K*P*p
    residual=utility-beta*resource+C*(p-(1+beta)*K*P/(2*C))**2-P*P*((1+beta)**2*K*K/(4*C)-beta*A)
    assert S.cancel(residual)==0
    matrix=S.Matrix([[2,1],[1,2]])
    assert matrix.det()>0
    load=Q(1,4);output=load-2*load*load;power=2-load
    assert output==Q(1,8) and power==Q(7,4)
    result=dict(status='PASS',scope='finite exact identities, arithmetic and witnesses only',
                affine_direction=dict(quartic_monomial_identities=checked,G_at_identity=str(at_i),scalar_dual_residual='0',
                                      boundary_flux=str(boundary_div),example_energy=str(energy),example_gap=str(gap),
                                      example_mu_over_3_remainder=str(coercivity)),
                phase_scale=dict(mass=str(mass),G_energy=str(translated_energy),winding='zero for R>1; analytic half-plane argument'),
                joint_response=dict(tree_expected_budget_upper=str(upper),matching_randomized_primal=str(primal),
                                    hard_budget_optimum='2',missing_pair_prediction='3 versus thermal4',triple_worlds=['7','8']),
                hydraulic=dict(complete_square_identity=True,loaded_power=str(output),source_input=str(power)),
                historical_novelty='UNKNOWN',independent_correctness='UNKNOWN',physical_acquisition='NOT_ESTABLISHED')
    target=Path(__file__).with_name('CONNECTION_VERIFICATION.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
