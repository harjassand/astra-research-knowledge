"""Independent literal all-b/affine-gamma family replay in SymPy QQ.

Only root's own QQ LDL helper is reused. No author maps/verifiers imported.
"""
from pathlib import Path
from itertools import combinations, combinations_with_replacement as cw
import hashlib
import json
import time
import sympy as s
from independent_common import exact_ldl, field, basis

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'quartic_alternative/combined_full_cone/output_flow_extension'


def main():
    start=time.monotonic()
    raw=(SOURCE/'EXACT_FLOW_FAMILY.json').read_bytes()
    grow=(SOURCE/'GAMMA_BOUND.json').read_bytes()
    data=json.loads(raw);gamma=json.loads(grow)
    point=json.loads((ROOT/'EXACT_SYMMETRIC_TARGET.json').read_text())
    p=list(map(s.Rational,point['coefficients']))
    assert p==list(map(s.Rational,data['target_coefficients']))
    a=s.symbols('a0:4');y=s.symbols('y0:6');variables=a+y
    f=sum(v*w for v,w in zip(p,basis(a)))
    q=a[0]*a[3]-a[1]*a[2]
    j1=s.Matrix([y[0],y[1],y[3],y[4]])
    j2=s.Matrix([y[1],y[2],y[4],y[5]])
    jj=s.Matrix([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
    monoms=[s.Poly(a[i]*a[j]*y[k]*y[l],*variables).monoms()[0]
            for i,j in cw(range(4),2) for k,l in cw(range(6),2)]
    lambdas=[dict(zip(monoms,map(field,data[key]))) for key in ('L0','L1')]

    def apply(poly,index):
        pp=s.Poly(poly,*variables,domain=s.QQ)
        assert set(pp.monoms())<=set(monoms)
        return sum((field(c)*lambdas[index][e] for e,c in pp.terms()),s.QQ.zero)

    def positive_moment(index,addition=False):
        z=[ai*yj for ai in a for yj in y]
        m=[[apply(zi*zj,index)+(apply(zi*zj,1) if addition else 0)
            for zj in z] for zi in z]
        return exact_ldl(m,data['moment_end_LDL_pivots' if addition else 'moment0_LDL_pivots'])

    d0=positive_moment(0)
    de=positive_moment(0,True)
    triples=list(combinations(range(4),3))
    for index in range(2):
        eta=list(map(field,data['closedness_eta'+str(index)]))
        assert len(eta)==16
        count=0
        for i,j in combinations(range(4),2):
            for k,l in cw(range(4),2):
                coefficient=a[k]*a[l]
                def omega(u,v):
                    return coefficient if (u,v)==(i,j) else (
                        -coefficient if (v,u)==(i,j) else s.S.Zero)
                dform=[s.Poly(s.diff(omega(v,w),a[u])-s.diff(omega(u,w),a[v])
                              +s.diff(omega(u,v),a[w]),*a)
                       for u,v,w in triples]
                closure=[field(poly.coeff_monomial(ai)) for poly in dform for ai in a]
                assert apply(coefficient*(j1[i]*j2[j]-j1[j]*j2[i]),index)==sum(
                    (v*w for v,w in zip(eta,closure)),s.QQ.zero)
                count+=1
        assert count==60
    polys=[]
    for energy in (f,q*q):
        hess=s.hessian(energy,a)
        identity=(j1.T*hess*j1)[0]+(j2.T*hess*j2)[0]
        mixed=(j1.T*hess*jj*j2)[0]+(j2.T*hess*jj*j1)[0]
        polys.append((identity,mixed))
    g=field(data['gamma_upper'])
    assert g==field(gamma['used_rational_upper_bound'])>0
    ef,ejf=polys[0];ed,ejd=polys[1]
    mixed=[apply(ejf,0),apply(ejf,1)-g*apply(ejd,0),apply(ejd,1)]
    assert mixed==[s.QQ.zero]*3==list(map(field,data['mixed_identities']))
    powers=[apply(ef,0),apply(ef,1)-g*apply(ed,0),-g*apply(ed,1)]
    bern=[powers[0],powers[0]+powers[1]/2,sum(powers,s.QQ.zero)]
    assert powers==list(map(field,data['energy_power_coefficients']))
    assert bern==list(map(field,data['energy_Bernstein_coefficients']))
    assert all(v<0 for v in bern)
    # Literal finite rank-one bound, not an acquired optimizer optimum.
    aa=list(map(s.Rational,gamma['A']))
    eta=list(map(s.Rational,gamma['eta']))
    direction=s.Matrix([eta[0],eta[1],0,0])
    replace=dict(zip(a,aa))
    curvature=(direction.T*s.hessian(f,a)*direction)[0].subs(replace)
    detderivative=sum(s.diff(q,ai)*di for ai,di in zip(a,direction)).subs(replace)
    assert curvature==s.Rational(gamma['F_curvature'])>0
    assert detderivative==s.Rational(gamma['det_derivative'])!=0
    ratio=field(curvature/(2*detderivative**2))
    assert ratio==field(gamma['exact_gamma_upper_bound'])<=g
    detcurvature=(direction.T*s.hessian(q*q,a)*direction)[0].subs(replace)
    assert detcurvature==2*detderivative**2
    out={
        'status':'ROOT_INDEPENDENT_LITERAL_ALL_B_ALL_GAMMA_FLOW_FAMILY_PASS',
        'family_sha256':hashlib.sha256(raw).hexdigest(),
        'gamma_bound_sha256':hashlib.sha256(grow).hexdigest(),
        'engine':'SymPy QQ exact derivatives, exterior derivatives and rational LDL; no author imports',
        'positive_endpoint_moment_pivots':[len(d0),len(de)],
        'literal_exterior_basis_checks':120,
        'mixed_parameter_coefficients':list(map(str,mixed)),
        'strict_negative_energy_Bernstein_coefficients':list(map(str,bern)),
        'rank_one_gamma_upper_bound':str(ratio),
        'used_gamma_upper_bound':str(g),
        'seconds':time.monotonic()-start,
        'scope':'Pure symmetric target minus nonnegative gamma det²; all canonical b and gamma in the proved interval. Extension to all constant uniformly coercive output-coupled flows uses the separately reviewed target-symmetry averaging proof. No combined unknown-energy/unknown-flow or arbitrary-monotonicity claim.'}
    (ROOT/'INDEPENDENT_FLOW_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
