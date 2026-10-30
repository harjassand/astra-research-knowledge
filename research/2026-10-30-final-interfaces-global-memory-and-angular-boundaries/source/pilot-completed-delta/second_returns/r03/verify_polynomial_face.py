"""Local exact fixtures for the complete nonhomogeneous polynomial face.

Reconstructs the lower-degree mechanism, a normal-form example, and a
forbidden cubic term that no finite Euclidean quadratic stiffness repairs
globally. Reads only the expressly supplied partner data and own phase2
data. All writes are in this directory.
"""
from pathlib import Path
import json
import sys
sys.dont_write_bytecode = True
import sympy as s
from cubic_rigidity import construct, av, monomials, powers, tau, t

HERE = Path(__file__).resolve().parent
PARTNER = HERE.parents[2] / 'first_returns' / 'r08'


def homogeneous(poly,degree):
    pp = s.Poly(s.expand(poly),*av)
    return s.Add(*(co*s.prod(z**e for z,e in zip(av,pw))
                   for pw,co in pp.terms() if sum(pw)==degree))


def main():
    L,D,F,m,K = construct()
    records = json.loads((HERE/'cubic_rigidity_data.json').read_text())
    assert records['rank_16_on_entire_open_branch']
    assert records['translation_rank_4_on_entire_open_branch']
    assert L == s.Matrix([[s.sympify(x,locals={'tau':tau}) for x in row]
                          for row in records['constraint_entries']])
    assert D == s.Matrix([[s.sympify(x,locals={'tau':tau}) for x in row]
                          for row in records['translation_entries']])
    a,b,c,d = av
    T,q = sum(z*z for z in av),a*d-b*c
    u = s.Rational(1,30)
    Fs,Ds,Ls = F.subs(tau,u),D.subs(tau,u),L.subs(tau,u)

    # Interface: read the completed partner's actual exposing vector and face,
    # without invoking its data-writing acquisition programs.
    ex = json.loads((PARTNER/'exposing_1_30.json').read_text())
    face = json.loads((PARTNER/'face_1_30.json').read_text())
    E = s.Matrix([s.Integer(z) for z in ex['integer_exposing_functional']])
    quartic_powers = ex['monomial_powers']
    quartic_monomials = [s.prod(z**e for z,e in zip(av,p)) for p in quartic_powers]
    fv = s.Matrix([s.Poly(Fs,*av).coeff_monomial(mon) for mon in quartic_monomials])
    face_matrix = s.Matrix([[s.Rational(z) for z in row] for row in face['constraint_matrix']])
    assert face_matrix.rank()==34 and face_matrix*fv==s.zeros(64,1)
    assert (E.T*fv)[0]==0
    ell_T4 = (E.T*s.Matrix([s.Poly(T*T,*av).coeff_monomial(mon)
                            for mon in quartic_monomials]))[0]
    ell_q2 = (E.T*s.Matrix([s.Poly(q*q,*av).coeff_monomial(mon)
                            for mon in quartic_monomials]))[0]
    assert ell_T4>0 and ell_q2>0

    # If the quartic part vanishes, the cubic must be rank-one affine.
    # Six actual rank-one directions already kill all 20 cubic coefficients.
    row_directions = [s.eye(4)[:,i] for i in range(4)]
    row_directions += [s.Matrix([1,1,0,0]),s.Matrix([0,0,1,1])]
    cubic_affine_columns = []
    for mon in monomials:
        column = []
        hh = s.hessian(mon,av)
        for rr in row_directions:
            pp = s.Poly(s.expand((rr.T*hh*rr)[0]),*av)
            column.extend(pp.coeff_monomial(z) for z in av)
        cubic_affine_columns.append(s.Matrix(column))
    zero_quartic_matrix = s.Matrix.hstack(*cubic_affine_columns)
    assert zero_quartic_matrix.rank()==20

    # The entire cone's lineality is exactly affine + scalar*determinant.
    all_powers = [(i,j,k,deg-i-j-k) for deg in range(5)
                   for i in range(deg+1) for j in range(deg+1-i)
                   for k in range(deg+1-i-j)]
    all_monomials = [s.prod(z**e for z,e in zip(av,pw)) for pw in all_powers]
    lower_monomials = [mon for mon,pw in zip(all_monomials,all_powers) if sum(pw)<=2]
    affine_directions = [s.eye(4)[:,i] for i in range(4)]
    affine_directions += [s.Matrix(v) for v in
                          ([1,1,0,0],[0,0,1,1],[1,0,1,0],
                           [0,1,0,1],[1,1,1,1])]
    assert all(rr[0]*rr[3]-rr[1]*rr[2]==0 for rr in affine_directions)
    columns = []
    for mon in all_monomials:
        hh = s.hessian(mon,av)
        column = []
        for rr in affine_directions:
            pp = s.Poly(s.expand((rr.T*hh*rr)[0]),*av)
            column.extend(pp.coeff_monomial(z) for z in lower_monomials)
        columns.append(s.Matrix(column))
    lineality_matrix = s.Matrix.hstack(*columns)
    assert lineality_matrix.rank()==64
    null_basis = s.Matrix([[s.Poly(N,*av).coeff_monomial(mon)
                            for N in [s.Integer(1),a,b,c,d,q]]
                           for mon in all_monomials])
    assert null_basis.rank()==6
    assert lineality_matrix*null_basis==s.zeros(lineality_matrix.rows,6)

    r_generic = 4-12*tau/(1+3*tau*tau)
    laplacian_F = s.factor(sum(s.diff(F,z,2) for z in av))
    assert s.cancel(laplacian_F-8*(r_generic+2)*T)==0

    # An admissible nonhomogeneous example with an indefinite quadratic Q.
    B = s.Matrix([s.Rational(1,2),-s.Rational(1,3),s.Rational(2,5),-s.Rational(3,7)])
    mass = s.Rational(2)
    Q = T-3*q
    affine = a+2*b-3*c+4*d+5
    shifted = Fs.subs(dict(zip(av,s.Matrix(av)+B)),simultaneous=True)
    good = s.expand(mass*shifted+Q+affine)
    leading = homogeneous(good,4)
    assert s.expand(leading-mass*Fs)==0
    cubic = homogeneous(good,3)
    cv = s.Matrix([s.Poly(cubic,*av).coeff_monomial(mon) for mon in monomials])
    recovered_B = s.simplify(Ds[16:20,:].inv()*cv[16:20,:]/mass)
    assert recovered_B==B
    assert Ls*cv==s.zeros(16,1)
    remainder = s.expand(good-mass*Fs.subs(dict(zip(av,s.Matrix(av)+recovered_B)),simultaneous=True))
    recovered_Q = homogeneous(remainder,2)
    assert s.expand(recovered_Q-Q)==0
    assert s.Poly(remainder-recovered_Q,*av).total_degree()<=1
    assert (E.T*s.Matrix([s.Poly(leading,*av).coeff_monomial(mon)
                           for mon in quartic_monomials]))[0]==0
    v1,v2,z1,z2 = s.symbols('v1 v2 z1 z2',real=True)
    rank_one = (v1*z1,v1*z2,v2*z1,v2*z2)
    assert s.expand(Q.subs(dict(zip(av,rank_one)),simultaneous=True)
                    -(v1*v1+v2*v2)*(z1*z1+z2*z2))==0
    assert (s.hessian(Q,av)/2).eigenvals()=={s.Rational(-1,2):2,s.Rational(5,2):2}
    # The additional Laplacian evaluation exposes the individual translated
    # ray modulo null Lagrangians inside the now-classified full face.
    translated_generator = mass*shifted-7*q+affine
    generator_laplacian_at_minus_B = s.expand(sum(s.diff(translated_generator,z,2) for z in av)).subs(
        dict(zip(av,-B)),simultaneous=True)
    assert generator_laplacian_at_minus_B==0
    good_laplacian_at_minus_B = s.expand(sum(s.diff(good,z,2) for z in av)).subs(
        dict(zip(av,-B)),simultaneous=True)
    assert good_laplacian_at_minus_B==8

    # The inherited strict minor-support gap survives this concrete addition.
    upper = s.Rational(917884501,33110)
    lower = s.Rational(227527416931,8195929)
    Rp = s.Matrix([0,55,-4,0]); Rm = s.Matrix([1,0,0,-2])
    Qp = Q.subs(dict(zip(av,Rp)),simultaneous=True)
    Qm = Q.subs(dict(zip(av,Rm)),simultaneous=True)
    upper_good = mass*upper+Qp/220
    lower_good = mass*lower+Qm/(-2)
    assert lower_good-upper_good>0

    # Forbidden cubic C=a^3. Normalise the actual acoustic K by K0 in the
    # quotient algebra; K0 never vanishes at a real root of m.
    mp = s.Poly(m.as_expr().subs(tau,u),t)
    Ks = K.subs(tau,u)
    invK0 = s.invert(s.Poly(Ks[0],t),mp).as_expr()
    Kh = Ks.applyfunc(lambda z:s.rem(s.expand(z*invK0),mp.as_expr(),t))
    assert Kh[0]==1
    R = s.Matrix([1,t,0,0])
    Hrank = s.hessian(Fs,av).subs(dict(zip(av,R)),simultaneous=True)
    rem = lambda p:s.factor(s.Poly(p,t).rem(mp).as_expr())
    assert all(rem(z)==0 for z in Hrank*Kh)
    forbidden_cv = s.Matrix([s.Poly(a**3,*av).coeff_monomial(mon) for mon in monomials])
    assert Ls*forbidden_cv != s.zeros(16,1)
    stiffness = s.symbols('kappa',nonnegative=True)
    scale = -(stiffness*(1+t*t)+1)/3
    base = scale*Kh
    bad = Fs+a**3+stiffness*T
    # Obtain only the second and fourth line coefficients by differentiation.
    Hess_bad = s.hessian(bad,av)
    second = s.expand((R.T*Hess_bad.subs(dict(zip(av,base)),simultaneous=True)*R)[0]/2)
    assert rem(second+1)==0
    fourth = s.factor(Fs.subs(dict(zip(av,R)),simultaneous=True))
    assert fourth==(1+t*t)**2
    # delta^2=1/F(R); cos^2 averages to 1/2, cos^4 to 3/8.
    delta2 = 1/fourth
    mean_gap = s.factor(-delta2/2+3*fourth*delta2**2/8)
    assert mean_gap == -1/(8*(1+t*t)**2)

    out = {
        'ordinary_polynomial_space_dimension':70,
        'classified_exposed_face_dimension':20,
        'lineality_dimension':6,
        'lineality_basis':['1','a','b','c','d','det A'],
        'full_rank_one_affinity_matrix_shape':[135,70],
        'full_rank_one_affinity_matrix_rank':64,
        'fixed_translation_exposed_face_dimension':7,
        'translated_exposed_ray_modulo_null_Lagrangians':True,
        'general_lifting_theorem':'Any exposed homogeneous planar quartic ray of the ROC or QC cone lifts under translation to an exposed ray of its degree<=4 polynomial cone modulo affine+determinant null Lagrangians. Proof uses the leading-part functional plus Hessian trace at one base, not the angular rank calculation.',
        'translated_ray_exposing_functional':'ell_tau(p_4) + Delta_A p(-V)',
        'matrix_space_laplacian_of_F':str(laplacian_F),
        'generic_cubic_constraint_shape':[16,20],
        'generic_cubic_rank':16,
        'generic_cubic_nullspace':'Exactly span{partial_a F,partial_b F,partial_c F,partial_d F}',
        'partner_seed_face_rank':34,
        'partner_exposer_annihilates_leading_part':True,
        'partner_exposer_on_T_squared':str(ell_T4),
        'partner_exposer_on_det_squared':str(ell_q2),
        'zero_quartic_cubic_constraint_shape':[24,20],
        'zero_quartic_cubic_constraint_rank':20,
        'admissible_example':{
            'quartic_mass':str(mass),'translation_B':list(map(str,B)),
            'recovered_translation_matches':True,
            'quadratic_remainder':str(Q),
            'quadratic_eigenvalues':{'-1/2':2,'5/2':2},
            'rank_one_quadratic_value':'|v|^2 |xi|^2',
            'nonpolyconvex_support_upper':str(upper_good),
            'nonpolyconvex_support_lower':str(lower_good),
            'nonpolyconvex_strict_gap':str(lower_good-upper_good),
            'strict_Jensen_gap':'2*gap_F(M+B,phi) + integral |Dphi|^2',
            'individual_ray_exposer_on_this_example':'8',
        },
        'translated_generator_fixture':{
            'energy':'2*F_*(A+B)-7*det(A)+a+2b-3c+4d+5',
            'exposing_functional_value':'0',
        },
        'forbidden_cubic_example':{
            'energy':'F_*(A)+a^3+kappa*|A|^2, kappa>=0',
            'Cubic_constraint_nonzero':True,
            'acoustic_K_normalized_entries':list(map(str,Kh)),
            'acoustic_modulus':str(mp.as_expr()),
            'rank_one_R':list(map(str,R)),
            'base_scale_s':str(scale),
            'base_matrix':'s*K_hat(t)',
            'second_line_coefficient_mod_m':'-1',
            'fourth_line_coefficient':str(fourth),
            'periodic_amplitude_squared':str(delta2),
            'exact_negative_mean_gap':str(mean_gap),
            'scope':'Global all-matrix obstruction. The required base gradient grows linearly with the quadratic stiffness; no bounded-strain no-go is claimed.',
        },
        'quasiconvexity_scope':'Known only at tau=1/6 and on the inherited |tau-1/30|<2^(-206) arc. On other branch parameters the normal form classifies rank-one convexity, not quasiconvexity.',
    }
    path = HERE/'polynomial_face_results.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'all_exact_assertions_passed':True,'output':str(path),
                      'nonpolyconvex_example_gap':out['admissible_example']['nonpolyconvex_strict_gap'],
                      'forbidden_cubic_mean_gap':str(mean_gap)},indent=2))


if __name__=='__main__':
    main()
