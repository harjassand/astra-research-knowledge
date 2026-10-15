#!/usr/bin/env python3
"""Exact algebra behind the complete acoustic-contact face description.

No optimizer, floating-point eigensolver, sampled parameter grid, or untrusted
pickle is used.  Positivity and extremality implications are in REPORT.md.
"""
from itertools import combinations
from pathlib import Path
import hashlib
import json
import sympy as s

HERE = Path(__file__).resolve().parent
R = s.Rational


def equal(lhs, rhs, name, checks):
    if isinstance(lhs, s.MatrixBase):
        assert lhs.shape == rhs.shape
        assert all(s.cancel(v) == 0 for v in lhs-rhs), name
    else:
        assert s.cancel(lhs-rhs) == 0, name
    checks.append(name)


def main():
    checks = []
    a,b,c,d,al,be,ga,de,n,m,t = s.symbols('a b c d alpha beta gamma delta n m t', real=True)
    x = s.Matrix([a,b,c,d])
    u = a*a+c*c
    v = b*b+d*d
    w = a*b+c*d
    j = a*d-b*c
    H = ((a-d)**2+(b+c)**2)**2
    F = al*H+be*u*u+ga*j*j+de*u*j
    rank_one = s.Matrix([n,m,0,0])
    acoustic = s.expand((rank_one.T*s.hessian(F,x)*rank_one)[0])
    # The infinitesimal target-rotation action preserves all four generators.
    rotation = s.Matrix([-c,-d,a,b])
    for name, polynomial in [('H',H),('u2',u*u),('j2',j*j),('uj',u*j)]:
        equal((s.Matrix([s.diff(polynomial,xi) for xi in x]).T*rotation)[0],0,
              'target_rotation_'+name, checks)

    # The first necessary PSD matrix, with the off-diagonal sign changed by a
    # diagonal congruence, is the exact conformal acoustic limit below.
    eta,zeta = s.symbols('eta zeta', real=True)
    conformal = {a:eta/2,d:eta/2,b:-t*(eta+zeta)/2,c:t*(eta+zeta)/2,n:t,m:1}
    limit_polynomial = ((6*be+de)*eta*eta-2*de*eta*zeta+ga*zeta*zeta)/2
    equal(acoustic.subs(conformal, simultaneous=True),
          t*t*limit_polynomial + t**4*(2*be+de)*(eta+zeta)**2/2,
          'first_PSD_conformal_limit', checks)
    xx,yy = s.symbols('xx yy', real=True)
    offdiag = {a:0,d:0,b:2*xx-yy,c:yy,n:1,m:0}
    equal(acoustic.subs(offdiag, simultaneous=True),
          2*(8*al*xx*xx-2*de*xx*yy+(2*be+de)*yy*yy),
          'second_PSD_offdiagonal_test', checks)
    equal(acoustic.subs({a:0,d:0,b:4*be+de,c:de,n:1,m:0}, simultaneous=True),
          2*(2*be+de)*(8*al*(2*be+de)-de*de),
          'explicit_negative_alpha_witness', checks)

    # Reconstruct the entire contact subspace in the nine-coefficient invariant
    # representation.  Nonnegative acoustic forms have zero first derivatives
    # at a contact, hence these are necessary linear constraints.
    basis = [u*u,v*v,u*v,w*w,u*w,v*w,u*j,v*j,w*j]
    f = s.Matrix(s.symbols('f0:9'))
    allF = sum(f[i]*basis[i] for i in range(9))
    all_acoustic = s.expand((rank_one.T*s.hessian(allF,x)*rank_one)[0])
    contact = {a:1,b:0,c:0,d:1,n:0,m:1}
    equations = [all_acoustic.subs(contact)] + [s.diff(all_acoustic,xi).subs(contact) for xi in list(x)+[n,m]]
    EC,zero = s.linear_eq_to_matrix(equations, list(f))
    assert all(q == 0 for q in zero)
    assert EC.rank() == 5
    generators = [H,u*u,j*j,u*j]
    coefmon = sorted(set().union(*(set(s.Poly(poly,*x).monoms()) for poly in basis)))
    BM = s.Matrix([[s.Poly(poly,*x).coeff_monomial(mon) for poly in basis] for mon in coefmon])
    GM = s.Matrix([[s.Poly(poly,*x).coeff_monomial(mon) for poly in generators] for mon in coefmon])
    coeffs = BM.gauss_jordan_solve(GM)[0]
    assert coeffs.rank() == 4
    equal(EC*coeffs, s.zeros(EC.rows,4), 'four_generators_span_full_contact_subspace', checks)

    # Universal threshold-family acoustic Schur reduction.
    p,q,h,k,r = s.symbols('p q h k r', real=True)
    coords = s.Matrix([p,q,h,k])
    transform = {a:(h+p)/2,d:(h-p)/2,b:(q-k)/2,c:(q+k)/2}
    Fr = (al*H+r*(r-1)*u*u/6+j*j+r*u*j).subs(transform, simultaneous=True)
    direction = s.Matrix([n,m,n,-m])
    acoustic_r = s.expand((direction.T*s.hessian(Fr,coords)*direction)[0])
    M = s.hessian(acoustic_r,coords)/2
    L = M[2:,2:]
    L_expected = s.Matrix([[n*n*(r+1)**2/2, -m*n*(r+1)/2],
                           [-m*n*(r+1)/2,(3*m*m+n*n*r*(r+2))/6]])
    equal(L,L_expected,'conformal_block',checks)
    equal(L.det(),n**4*r*(r+1)**2*(r+2)/12,'conformal_block_determinant',checks)
    Schur = (M[:2,:2]-M[:2,2:]*L.inv()*M[2:,:2]).applyfunc(s.cancel)
    Schur_expected = s.Matrix([
        [12*al*n*n+4*al*m*m-r*((5*r*r+14*r+8)*n*n+3*m*m)/(2*(r+1)**2*(r+2)),
         8*al*m*n-3*r*m*n/(2*(r+1)*(r+2))],
        [8*al*m*n-3*r*m*n/(2*(r+1)*(r+2)),
         4*al*n*n+12*al*m*m-3*r*n*n/(2*(r+2))]])
    equal(Schur,Schur_expected,'universal_Schur_identity',checks)
    alstar = 3*r/(8*(r+2))
    lowSchur = Schur.subs(al,alstar)
    square = r/(2*(r+2))*((2*r+1)*n*p/(r+1)+3*m*q)**2 + 3*r*r*m*m*p*p/(2*(r+1)**2)
    equal((s.Matrix([p,q]).T*lowSchur*s.Matrix([p,q]))[0], square,
          'sharp_acoustic_SOS', checks)
    T = s.Matrix([h,k])+L.inv()*M[2:,:2]*s.Matrix([p,q])
    equal(acoustic_r,(T.T*L*T)[0]+(s.Matrix([p,q]).T*Schur*s.Matrix([p,q]))[0],
          'full_square_completion',checks)

    # Exact one-boundary-generator decomposition for all delta != 0 cases.
    rho = (6*be+de)/de
    lam = de*de/(6*be+de)
    alphafloor = de*de/(8*(2*be+de))
    sharp = lambda rr: 3*rr*H/(8*(rr+2))+rr*(rr-1)*u*u/6+j*j+rr*u*j
    equal(lam*sharp(rho)+(ga-lam)*j*j+(al-alphafloor)*H,F,
          'global_one_generator_decomposition',checks)
    equal(ga-lam,(ga*(6*be+de)-de*de)/(6*be+de),
          'determinant_square_remainder',checks)
    # Both spectrahedral matrices have rank one on each sharp generator.
    bstar = r*(r-1)/6
    P = s.Matrix([[6*bstar+r,r],[r,1]])
    Q = s.Matrix([[8*alstar,r],[r,2*bstar+r]])
    equal(P,s.Matrix([r,1])*s.Matrix([r,1]).T,'first_boundary_rank_one',checks)
    equal(Q.det(),0,'second_boundary_rank_one',checks)

    # Independently check the support-gap non-polyconvexity construction
    # communicated by contact_face_priority_audit after the cone derivation.
    Jr = sharp(r)
    atI = {a:1,b:0,c:0,d:1}
    FIsharp = Jr.subs(atI)
    gradI = s.Matrix([s.diff(Jr,xi).subs(atI) for xi in x])
    ell = s.symbols('ell',real=True)
    equal(s.diff(Jr-ell*j,b,c).subs(atI),ell-r-2,
          'polyconvex_support_lambda_forced',checks)
    supportgap = Jr-FIsharp-(gradI.T*(x-s.Matrix([1,0,0,1])))[0]-(r+2)*(j-a-d+1)
    simplegap = Jr-(r+2)*j-R(2,3)*r*(r+2)*a+(r+2)*(r+1)/2
    equal(supportgap,simplegap,'polyconvex_support_gap',checks)
    pathgap = supportgap.subs({a:1+t,b:0,c:0,d:1-(r+1)*t})
    equal(pathgap,t**3*(r+2)*((9*r**3+36*r*r+40*r+12)*t-8*r)/24,
          'polyconvex_support_path_exact',checks)
    equal(s.Poly(s.cancel(pathgap),t).nth(3),-r*(r+2)/3,
          'polyconvex_support_nonzero_cubic',checks)
    # A discrete anisotropic input symmetry; no continuous right-rotation
    # invariance is inferred from this identity.
    Btrans = {a:3*b,b:(2*r+1)*a,c:3*d,d:(2*r+1)*c}
    equal(Jr.subs(Btrans,simultaneous=True),9*(2*r+1)**2*Jr,
          'sharp_discrete_right_symmetry',checks)
    Msharp=M.subs(al,alstar)
    equal(Msharp.det(),R(9,16)*r**4*n**4*m**4,
          'sharp_acoustic_determinant',checks)
    equal(Msharp.subs({n:0,m:1})*s.Matrix([0,0,1,0]),s.zeros(4,1),
          'old_contact_kernel',checks)
    equal(Msharp.subs({n:1,m:0})*s.Matrix([0,r+2,0,1-r]),s.zeros(4,1),
          'new_contact_kernel',checks)
    Qgeneral=s.Matrix([[8*al,de],[de,2*be+de]])
    equal(Qgeneral*s.Matrix([r+2,-3]),s.Matrix([8*al*(r+2)-3*de,de*(r-1)-6*be]),
          'minimal_exposed_face_second_zero',checks)
    da,db,dc=s.symbols('diffusion_a diffusion_b diffusion_c',real=True)
    DD=s.Matrix([[da,db],[db,dc]])
    BB=s.Matrix([[0,2*r+1],[3,0]])
    nq=-(2*r+1)
    equal(DD+BB*DD*BB.T/(3*nq),s.diag(da+nq*dc/3,dc+3*da/nq),
          'natural_diffusion_average',checks)

    # Optimize the cone generated by the inherited interval, H, u^2, j^2.
    mass,delta,beta = s.symbols('mass delta beta', nonzero=True, real=True)
    equal(mass*(delta/mass)*(delta/mass-1)/6,
          delta*delta/(6*mass)-delta/6,'single_atom_beta_cost',checks)
    lower,upper = -R(21,8),-R(5,2)
    kap = R(3,16000)
    rate = 3-kap
    r0 = -R(41,16)
    lam0 = R(40,41)
    example = R(120,41)*H+R(95,64)*u*u+j*j-R(5,2)*u*j
    original_base = 3*H+r0*(r0-1)*u*u/6+j*j+r0*u*j
    equal(example,lam0*original_base+R(1,41)*j*j,
          'strict_QC_conic_example',checks)
    FI = example.subs({a:1,b:0,c:0,d:1})
    FJ = example.subs({a:1,b:0,c:0,d:-1})
    equal(FI,-R(1,64),'example_negative_conformal_value',checks)
    equal(64**2*FI+FJ,-R(31977,2624),'example_four_atom_witness',checks)
    equal(lam0/R(2500000),R(1,2562500),'example_strict_Jensen_constant',checks)
    # At beta=145/96, delta=-5/2, gamma=1 the smallest inherited
    # generator mass is 20/21, attained by r=-21/8.
    equal(rate*R(20,21),R(15999,5600),'optimal_generated_QC_alpha_example',checks)

    receipt = {
        'status':'EXACT_PASS','sympy_version':s.__version__,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'exact_check_count':len(checks),'checks':checks,
        'contact_constraint_rank':5,'contact_face_dimension':4,
        'sharp_alpha':'3*r/(8*(r+2))',
        'rank_one_convex_cone':[
            'Matrix([[6*beta+delta,delta],[delta,gamma]]) >= 0',
            'Matrix([[8*alpha,delta],[delta,2*beta+delta]]) >= 0'],
        'generator_domain':'r < -2 or r > 0; plus H, u^2, j^2',
        'all_sharp_generators_nonpolyconvex_support_gap':True,
        'full_invariant_cone_sharp_rays_nonexposed':True,
        'strict_QC_example':{'alpha':'120/41','beta':'95/64','gamma':'1','delta':'-5/2',
                             'Jensen_constant':'1/2562500'},
        'scope':'Exact algebra only. Positivity, exposed-face, extremality and QC transfer arguments are in REPORT.md. No QC theorem for all sharp generators is asserted.'
    }
    (HERE/'FACE_EXACT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(f'EXACT_PASS: {len(checks)} algebraic checks; contact face dimension 4; full two-LMI ROC cone')


if __name__ == '__main__':
    main()
