#!/usr/bin/env python3
"""Independent rational verification of frozen infinite-lattice certificates.

No optimizer, LP solver or author verifier is imported. Universal extension
rests on the analytic support and tail arguments in DEPENDENT_AUDIT.md.
"""
from fractions import Fraction as F
from pathlib import Path
from decimal import Decimal, localcontext
import hashlib
import json

HERE = Path(__file__).resolve().parent
SNAP = HERE/'snapshots_20261015_first'
DUAL = SNAP/'dependent_noise_dual_sol'


def load(path):
    return json.loads(path.read_text())


def dual_certificate(path):
    certificate = load(path)
    K = certificate['K']
    c = tuple(map(F, certificate['center']))
    bound = F(certificate['proved_lower'])
    assert K >= 0 and all(abs(a) < 2*K+4 for a in c)
    # This box contains every node affected by a finite-support multiplier.
    coefficients = {(i,j):(2*i-c[0])**2+(2*j-c[1])**2
                    for i in range(-K-1,K+2) for j in range(-K-1,K+2)}
    for i,j,uz,ux,weight in certificate['multipliers']:
        uz,ux,weight = F(uz),F(ux),F(weight)
        assert weight >= 0 and uz*uz+ux*ux == 1
        assert -K-1 <= i <= K and -K-1 <= j <= K
        corners = [(i,j,1,1),(i+1,j,-1,1),
                   (i,j+1,1,-1),(i+1,j+1,-1,-1)]
        for a,b,sz,sx in corners:
            coefficients[a,b] += weight*(uz*sz+ux*sx-1)
    assert all(a >= bound for a in coefficients.values())
    # Any other node has |i| or |j| >= K+2. The inequalities above on c
    # ensure the triangle lower bound is positive before squaring.
    exterior = min((2*K+4-abs(a))**2 for a in c)
    assert exterior >= bound
    return c,bound,{'file':path.name,'center':list(map(str,c)),
                    'bound':str(bound),'affected_nodes':len(coefficients),
                    'multipliers':len(certificate['multipliers']),
                    'exterior_cost_lower':str(exterior),
                    'entire_lattice_status':'PASSED_EXACT_WITH_ANALYTIC_EXTERIOR'}


def rectangle_minimum(corners, h=F(1,4)):
    # B(t,u) is bilinear interpolation of the four certified costs.
    # The exact correction is -h²[t(1-t)+u(1-u)].
    a,b,c,d = corners
    hh = h*h
    ax,ay,cross = b-a-hh,c-a-hh,d-b-c+a
    def value(t,u):
        return a+ax*t+ay*u+cross*t*u+hh*(t*t+u*u)
    def clip(x):
        return min(F(1),max(F(0),x))
    points = {(F(i),F(j)) for i in (0,1) for j in (0,1)}
    for t in (F(0),F(1)):
        points.add((t,clip(-(ay+cross*t)/(2*hh))))
    for u in (F(0),F(1)):
        points.add((clip(-(ax+cross*u)/(2*hh)),u))
    determinant = (2*hh)**2-cross**2
    if determinant > 0:
        t = (-2*hh*ax+cross*ay)/determinant
        u = (cross*ax-2*hh*ay)/determinant
        if 0 <= t <= 1 and 0 <= u <= 1:
            points.add((t,u))
    # A non-positive Hessian determinant cannot hide a strict interior
    # minimum: a saddle is excluded; a flat minimizer reaches an edge.
    return min((value(t,u),t,u) for t,u in points)


def upper_certificate(path):
    certificate = load(path)
    N,rho = certificate['N'],F(certificate['rho'])
    table = {(i,j):F(p) for i,j,p in certificate['p_table']}
    assert N >= 1 and 0 < rho < 1
    assert set(table) == {(i,j) for i in range(N+1) for j in range(i+1)}
    assert all(p >= 0 for p in table.values())
    def capped(i,j):
        i,j = sorted((min(i,N),min(j,N)),reverse=True)
        return table[i,j]
    margins = []
    directions = set()
    first_cells = {}
    for i in range(N+1):
        for j in range(i+1):
            p,q,r,s = (capped(i,j),rho*capped(i+1,j),
                       rho*capped(i,j+1),rho*rho*capped(i+1,j+1))
            mass = p+q+r+s
            z,x = p+r-q-s,p+q-r-s
            margin = mass*mass-z*z-x*x
            assert mass >= 0 and margin >= 0
            margins.append(margin)
            if mass > 0:
                for a,b in ((z,x),(x,z)):
                    for sz in (-1,1):
                        for sx in (-1,1):
                            directions.add((sz*a/mass,sx*b/mass))
                first_cells[i,j] = (mass,z,x)
    multiplicities = [F(1)]+[F(2)]*(N-1)+[2/(1-rho)]
    square_sums = [F(0)]+[F(2*i*i) for i in range(1,N)]
    square_sums.append(2*(N*N/(1-rho)+2*N*rho/(1-rho)**2
                         +rho*(1+rho)/(1-rho)**3))
    normalization = F(0)
    second = F(0)
    for i in range(N+1):
        for j in range(N+1):
            base = rho**(i+j)*capped(i,j)
            normalization += base*multiplicities[i]*multiplicities[j]
            second += 4*base*(square_sums[i]*multiplicities[j]
                              +multiplicities[i]*square_sums[j])
    assert normalization > 0
    trace = second/normalization
    assert trace == F(certificate['trace_covariance_exact'])
    assert normalization == F(certificate['normalizing_mass'])
    assert second == F(certificate['unnormalized_trace_second_moment'])
    assert trace <= F(certificate['proved_upper'])
    assert table[0,0]*table[1,1] != table[1,0]**2
    # Positive-quadrant cells (0,0) and (1,0) have the same output signs.
    # Nonproportional effects show that signs alone are not sufficient.
    M0,Z0,X0 = first_cells[0,0]
    M1,Z1,X1 = first_cells[1,0]
    sign_defect = (Z0*M1-Z1*M0,X0*M1-X1*M0)
    assert any(a != 0 for a in sign_defect)
    return {'file':path.name,'N':N,'rho':str(rho),'tail_types':len(margins),
            'minimum_scaled_determinant':str(min(margins)),
            'trace_exact':str(trace),'trace_decimal':float(trace),
            'rounded_upper':certificate['proved_upper'],
            'distinct_normalized_effect_directions':len(directions),
            'finite_outcome_type_upper_bound':4*(N+1)**2,
            'signs_not_sufficient_exact_witness':{'positive_cells':[[0,0],[1,0]],
                                               'nonproportional':True},
            'infinite_tail_status':'PASSED_EXACT_WITH_ANALYTIC_CAP_REDUCTION'}


def older_upper():
    certificate = load(SNAP/'dependent_order_noise_sol/exact_construction_certificate.json')
    C = certificate['C']
    rho = F(certificate['q'])
    N = 3
    eta = (1-rho)/(1+rho)
    margins = []
    for i in range(N):
        for j in range(N):
            p,q,r,s = C[i][j],C[i+1][j],C[i][j+1],C[i+1][j+1]
            S,X,Y = p+q+r+s,p+r-q-s,p+q-r-s
            margins.append(S*S-X*X-Y*Y)
    for j in range(N):
        x,y = C[N][j],C[N][j+1]
        margins.append((1-eta*eta)*(x+y)**2-(x-y)**2)
    margins.append(1-2*eta*eta)
    assert all(m > 0 for m in margins)
    m = [F(1),F(2),F(2),2/(1-rho)]
    t = [F(0),F(2),F(8),2*(9/(1-rho)+6*rho/(1-rho)**2
                             +rho*(1+rho)/(1-rho)**3)]
    Z = sum(m[i]*m[j]*C[i][j] for i in range(4) for j in range(4))
    trace = 4*sum((t[i]*m[j]+m[i]*t[j])*C[i][j]
                  for i in range(4) for j in range(4))/Z
    assert trace == F(5949040524880,1857425454953)
    assert trace == F(certificate['normalized_trace'])
    return {'trace_exact':str(trace),'trace_decimal':float(trace),
            'core_strip_tail_checks':len(margins),'status':'PASSED_EXACT'}


def compact_handwritten_upper():
    N,rho = 2,F(1,5)
    table = {(0,0):F(1),(1,0):F(3,20),(1,1):F(1,20),
             (2,0):F(1,500),(2,1):F(9,1000),(2,2):F(1,500)}
    def mass(i,j):
        a,b = sorted((min(i,N),min(j,N)),reverse=True)
        return table[a,b]*rho**(max(i-N,0)+max(j-N,0))
    expected = [F(7,400),F(151,1000000),F(73,250000),
                F(41,1562500),F(41,1562500),F(9,9765625)]
    margins = []
    for i in range(N+1):
        for j in range(i+1):
            a,b,c,d = mass(i,j),mass(i+1,j),mass(i,j+1),mass(i+1,j+1)
            S,X,Y = a+b+c+d,a+c-b-d,a+b-c-d
            margin = S*S-X*X-Y*Y
            assert S > 0 and margin > 0
            margins.append(margin)
    assert margins == expected
    m = [F(1),F(2),2/(1-rho)]
    t = [F(0),F(2),2*(N*N/(1-rho)+2*N*rho/(1-rho)**2
                      +rho*(1+rho)/(1-rho)**3)]
    Z = sum(m[i]*m[j]*mass(i,j) for i in range(N+1) for j in range(N+1))
    C = 4*sum((t[i]*m[j]+m[i]*t[j])*mass(i,j)
              for i in range(N+1) for j in range(N+1))
    assert Z == F(153,80) and C == F(2819,400)
    assert C/Z == F(2819,765) < 4
    assert table[0,0]*table[1,1] != table[1,0]**2
    return {'normalization':str(Z),'unnormalized_second_moment':str(C),
            'trace_exact':str(C/Z),'trace_decimal':float(C/Z),
            'six_determinants':list(map(str,margins)),
            'status':'PASSED_EXACT_COMPLETE_TAIL_TYPES'}


def radial_constant_diagnostic():
    with localcontext() as ctx:
        ctx.prec = 75
        t = Decimal('1.5')
        for _ in range(20):
            t -= (2*t**3-3*t-2)/(6*t*t-3)
        sqrt2 = Decimal(2).sqrt()
        w = sqrt2*t
        L = 4*(sqrt2-1)*t*t*(t+1)/(2*t*t-1)
        alternative = (2-sqrt2)*w**3/2
        assert abs(L-alternative) < Decimal('1e-70')
        return {'L0_decimal_diagnostic':str(L),
                'author_last_digit_correction':'Use approximately 2.66217523319253; PROOF.txt optional decimal ending 5337 differs in the last few printed digits.',
                'proof_scope':'The algebraic expressions agree analytically under 2t^3-3t-2=0. Decimal computation is not a proof premise.'}


def main():
    bounds = {}
    duals = []
    for path in sorted(DUAL.glob('adaptive_dual_K*.json')):
        center,bound,record = dual_certificate(path)
        for c in (center,center[::-1]):
            bounds[c] = max(bound,bounds.get(c,F(0)))
        duals.append(record)
    h = F(1,4)
    rectangles = []
    for i in range(4):
        for j in range(4):
            x,y = i*h,j*h
            corners = [bounds[c] for c in [(x,y),(x+h,y),(x,y+h),(x+h,y+h)]]
            lower,t,u = rectangle_minimum(corners,h)
            rectangles.append({'lower_corner':[str(x),str(y)],'bound':str(lower),
                               'minimizer':[str(x+h*t),str(y+h*u)]})
    universal = min(F(r['bound']) for r in rectangles)
    uppers = [upper_certificate(path) for path in sorted(DUAL.glob('certified_upper_N*.json'))]
    best = min(uppers,key=lambda r:F(r['trace_exact']))
    rounded_lower = F(universal.numerator*10**7//universal.denominator,10**7)
    assert universal < F(best['trace_exact'])
    manifest = HERE/'DEPENDENT_SNAPSHOT_MANIFEST.json'
    for record in load(manifest)['files']:
        p = HERE/record['snapshot']
        assert hashlib.sha256(p.read_bytes()).hexdigest() == record['sha256']
    result = {'status':'PASSED_INDEPENDENT_RATIONAL_CERTIFICATE_VERIFICATION',
              'universal_trace_covariance_lower_exact':str(universal),
              'universal_lower_decimal':float(universal),
              'rounded_lower':str(rounded_lower),
              'best_explicit_infinite_upper':best,
              'rounded_gap':str(F(best['rounded_upper'])-rounded_lower),
              'dual_certificates':duals,'free_mean_rectangles':rectangles,
              'infinite_upper_certificates':uppers,
              'older_exact_upper':older_upper(),
              'compact_handwritten_upper':compact_handwritten_upper(),
              'radial_constant_evaluation':radial_constant_diagnostic(),
              'global_optimum':'UNRESOLVED',
              'scope':'All Borel scalar laws on R² with finite covariance, conditional on the analytically audited Fourier-POVM contract and quotient reduction.',
              'limits':'Internal exact certificate verification, not external review or formal verification; no finite-grid optimizer is promoted.'}
    (HERE/'DEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','universal_trace_covariance_lower_exact',
                    'universal_lower_decimal','rounded_lower','best_explicit_infinite_upper',
                    'rounded_gap','global_optimum']},indent=2))


if __name__ == '__main__':
    main()
