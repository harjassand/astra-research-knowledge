"""Independent reconstruction for the frozen physical packets.

This file does not import producer code. Fraction checks are exact;
mpmath eigensystems/quadrature are independent numerical diagnostics.
The analytic whole-axis arguments are audited separately in REVIEW.md.
"""
from fractions import Fraction as Q
from itertools import permutations
from pathlib import Path
from math import factorial
import json
import mpmath as mp

mp.mp.dps = 90
HERE = Path(__file__).resolve().parent
rows = []


def mm(x):
    if isinstance(x, Q):
        return mp.mpf(x.numerator) / x.denominator
    return mp.mpf(x)


def polyadd(a, b):
    ans = [Q(0)] * max(len(a), len(b))
    for i, x in enumerate(a): ans[i] += x
    for i, x in enumerate(b): ans[i] += x
    return ans


def polymul(a, b):
    ans = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): ans[i+j] += x*y
    return ans


def charpoly(a):
    """det(tI-a), ascending coefficients, direct Leibniz formula."""
    n = len(a)
    ans = [Q(0)]
    for p in permutations(range(n)):
        parity = sum(p[i] > p[j] for i in range(n) for j in range(i+1, n))
        term = [Q((-1) ** parity)]
        for i in range(n):
            term = polymul(term, [-a[i][p[i]], Q(int(i == p[i]))])
        ans = polyadd(ans, term)
    return ans


def solve(a, b):
    n = len(a)
    aug = [list(map(Q, a[i])) + [Q(b[i])] for i in range(n)]
    for k in range(n):
        i = next(i for i in range(k, n) if aug[i][k])
        aug[k], aug[i] = aug[i], aug[k]
        z = aug[k][k]
        aug[k] = [x/z for x in aug[k]]
        for i in range(n):
            if i != k:
                z = aug[i][k]
                aug[i] = [x-z*y for x, y in zip(aug[i], aug[k])]
    return [r[-1] for r in aug]


def laplacian(n, edges):
    a = [[Q(0) for _ in range(n)] for _ in range(n)]
    for i, j, k in edges:
        a[i][i] += k; a[j][j] += k
        a[i][j] -= k; a[j][i] -= k
    return a


# A connected non-star graph checks that the incident and total spring costs
# are distinct and that the compliance moment is not a star-only identity.
mass = [Q(1), Q(1, 5), Q(3, 10), Q(1, 2)]
graph = [(0, 1, Q(2)), (0, 2, Q(4)), (0, 3, Q(5)),
         (1, 2, Q(7)), (2, 3, Q(11))]
L = laplacian(4, graph)
a = [[L[i][j]/mass[i] for j in range(4)] for i in range(4)]
b = [r[:] for r in a]; b[0][0] += 4
ca, cb = charpoly(a), charpoly(b)
assert ca[0] == 0 and -cb[0]/ca[1] == 2
assert ca[-2] - cb[-2] == 4
x = solve([r[1:] for r in L[1:]], mass[1:])
C = sum(m*y for m, y in zip(mass[1:], x))
inverse_sum = -cb[1]/cb[0] + ca[2]/ca[1]
assert inverse_sum == Q(1, 2) + C/2
trace2 = lambda z: sum(z[i][j]*z[j][i] for i in range(4) for j in range(4))
E = trace2(b) - trace2(a)
assert E == 16 + 8*11 == 104
assert sum(k for _, _, k in graph) == 29 and 29*C >= 1
rows.append({'case': 'exact non-star graph', 'C': str(C),
             'inverse_endpoint_sum': str(inverse_sum), 'E': str(E),
             'incident_springs': '11', 'total_springs': '29',
             'alpha_characteristic_ascending': list(map(str, ca)),
             'beta_characteristic_ascending': list(map(str, cb))})


# Independently expand every coefficient of the root-count entire function.
# Four coordinates correspond to lambda, mu, nu_stiffness, eta_compliance.
for n in range(1, 41):
    d = lambda j: Q(2**(2*j-1), factorial(2*j)) if j >= 1 else Q(0)
    raw = [d(n), 2*d(n-1), 4*d(n-2), -d(n+1)]
    normalized = [x/d(n) for x in raw]
    expected = [Q(1), Q(n*(2*n-1)) if n >= 2 else Q(0),
                Q(n*(n-1)*(2*n-1)*(2*n-3)) if n >= 3 else Q(0),
                -Q(4, (2*n+2)*(2*n+1))]
    assert normalized == expected
quartic = polymul(polymul([0, 1], [-1, 1]), polymul([-1, 2], [-3, 2]))
third = [quartic[k]*k*(k-1)*(k-2) for k in range(3, 5)]
assert third == [-72, 96]
rows.append({'case': 'entire-series coefficients', 'n_checked': 40,
             'quartic_ascending': list(map(str, quartic)),
             'third_derivative_ascending': list(map(str, third))})


def g(w):
    return (w/mp.sinh(w))**2 if w else mp.mpf(1)


def objective(edges):
    return mp.quad(g, [0, edges[0]]) + sum(
        mp.quad(g, [edges[i], edges[i+1]]) for i in range(1, len(edges), 2))


def star(m, k):
    m = list(map(mm, m)); k = list(map(mm, k)); n = len(m)
    L = mp.matrix(n)
    for j, z in enumerate(k, 1):
        L[0, 0] += z; L[j, j] += z; L[0, j] -= z; L[j, 0] -= z
    D0 = mp.matrix([[L[i, j]/mp.sqrt(m[i]*m[j]) for j in range(n)] for i in range(n)])
    Dpi = D0.copy(); Dpi[0, 0] += 4/m[0]
    alpha = list(mp.eigsy(D0, eigvals_only=True))
    beta = list(mp.eigsy(Dpi, eigvals_only=True))
    assert abs(alpha[0]) < mp.mpf('1e-70')
    endpoints = []
    for i in range(n):
        if i: endpoints.append(mp.sqrt(alpha[i]))
        endpoints.append(mp.sqrt(beta[i]))
    C = sum(mj*mj/kj for mj, kj in zip(m[1:], k))/(sum(m[1:])**2)
    T = sum(beta)-sum(alpha)
    B = mp.fprod(beta)/mp.fprod(alpha[1:])
    inv = sum(1/z for z in beta)-sum(1/z for z in alpha[1:])
    E = sum(z*z for z in beta)-sum(z*z for z in alpha)
    assert abs(T-4/m[0]) < mp.mpf('1e-65')
    assert abs(B-4/sum(m)) < mp.mpf('1e-65')
    assert abs(inv-(sum(m)/4+sum(m[1:])**2*C/sum(m))) < mp.mpf('1e-65')
    assert abs(E-(16+8*sum(k))) < mp.mpf('1e-60')
    return endpoints, C, E


def dual(edges):
    if len(edges) == 3:
        basis = lambda w: [w*w, 2*w**4, -1]
    else:
        basis = lambda w: [w*w, 2*w**4, 4*w**6, -1]
    return mp.lu_solve(mp.matrix([basis(w) for w in edges[:len(basis(edges[0]))]]),
                       mp.matrix([-w**3*g(w) for w in edges[:len(basis(edges[0]))]]))


def record(label, mass, springs):
    edges, c, e = star(mass, springs)
    jj = objective(edges)
    rows.append({'case': label, 'masses': list(map(lambda v: mp.nstr(mm(v), 48), mass)),
                 'springs': list(map(lambda v: mp.nstr(mm(v), 48), springs)),
                 'C': mp.nstr(c, 48), 'E': mp.nstr(e, 48),
                 'edges': [mp.nstr(z, 48) for z in edges], 'J': mp.nstr(jj, 48)})
    return edges, jj


main_edges, jmain = record('k4 supplied cap', [1, 1], [4])
lm, mu, eta = dual(main_edges)
assert mu > 0 and eta > 0
_, jp = record('optimized pendant k20', [1, 1], [20])
_, j44 = record('R44 rational finite star', [1, Q(1,20), Q(19,20)], [5, Q(1805,99)])
assert jp > j44


def qstar(t, H, c, d):
    """Obtain branch poles from the independently inverted rational response."""
    t, H, c, d = map(mm, (t, H, c, d))
    sig = [(c-mp.sqrt(c*c-4*d))/2, (c+mp.sqrt(c*c-4*d))/2]
    kap = t+H-c
    k1 = (t*H-d-kap*sig[0])/(sig[1]-sig[0]); k2 = kap-k1
    mass = [1, k1/sig[0], k2/sig[1]]
    assert abs(sum(mass)-2) < mp.mpf('1e-70') and min(mass+[k1,k2]) > 0
    return mass, [k1, k2]


specs = [('R79 severe-cap star', Q(28144153,971605), 400,
          Q(698227683,1943210), Q(1125766120,194321)),
         ('R79 almost minimum stiffness', Q(8154867599,204211900), 64,
          Q(171361086787,2042119000), Q(65238940792,51052975))]
for label, t, H, c, d in specs:
    # Exact small-t expansion of q gives tau; C=4*tau here.
    tau = c/(t*H) - d*(t+H)/(t*H)**2
    assert 4*tau == Q(1,20) and t*H/d == 2
    mass, springs = qstar(t,H,c,d)
    _, jj = record(label, mass, springs)
    assert jp > jj


def joint(h):
    h = mm(h); b = 1-h; C = mp.mpf(1)/20
    H = (24*C-1+2*h+mp.sqrt((1-2*h-24*C)**2-96*C*h*h))/(2*C)
    edges, _, _ = star([1,h,b],[H,24-H])
    lm, mu, nu, eta = dual(edges)
    w = edges[-1]
    residual = w**3*g(w)+lm*w*w+2*mu*w**4+4*nu*w**6-eta
    return residual, edges, H, (lm,mu,nu,eta)


hlo = mp.mpf('0.06552741459340005487388219669883060107690')
hhi = mp.mpf('0.06552741459340005487388219669883060107692')
assert joint(hlo)[0] > 0 > joint(hhi)[0]
hr = mp.findroot(lambda h: joint(h)[0], (hlo,hhi), solver='secant', tol=mp.mpf('1e-80'))
res, edges, H, coeffs = joint(hr)
assert abs(res) < mp.mpf('1e-70') and coeffs[2] > 0 and coeffs[3] > 0
j_joint = objective(edges)
assert jp > j_joint
rows.append({'case':'R44 joint-cap optimum reconstruction', 'h':mp.nstr(hr,75),
             'H':mp.nstr(H,75), 'J':mp.nstr(j_joint,75),
             'dual_lambda_mu_nu_eta':list(map(lambda z:mp.nstr(z,75),coeffs)),
             'fifth_edge_residual':mp.nstr(res,12),
             'gain_over_optimized_pendant':mp.nstr(jp-j_joint,55)})


def low_edges(A, r, B=mp.mpf(2)):
    t = r*r; s2 = (t+A+mp.sqrt((t+A)**2-4*B*t))/2
    return [mp.sqrt(B*t/s2),r,mp.sqrt(s2)]


rhat = mp.findroot(lambda r: dual(low_edges(2+r*r/20,r))[1], (mp.mpf(5.2),mp.mpf(5.4)))
Ahat = 2+rhat*rhat/20
j_inf = objective(low_edges(Ahat,rhat))
assert Ahat < 4 and j_inf < j_joint
rows.append({'case':'common trace-escape infimum', 'r':mp.nstr(rhat,70),
             'A':mp.nstr(Ahat,70), 'J':mp.nstr(j_inf,70)})


# Derivatives at the collapsing high band, independent direct quadrature.
def split(delta):
    high = mp.mpf(64); C=mp.mpf(1)/20
    A=4-delta; B=2*high/(high+delta)
    t=(A-B)/(B*((1+C)/2-1/B+delta/(high*(high+delta))))
    c=(B*t+(t+A)*(high+delta)-t*high)/4
    kap=t+high-c
    edges=low_edges(A,mp.sqrt(t),B)+[mp.sqrt(high),mp.sqrt(high+delta)]
    return objective(edges),kap


dJ=mp.diff(lambda d:split(d)[0],mp.mpf(0))
dK=mp.diff(lambda d:split(d)[1],mp.mpf(0))
assert dJ < 0 and abs(dK-mp.mpf(255)/128) < mp.mpf('1e-65')
rows.append({'case':'R79 branch splitting derivative','dJ_ddelta':mp.nstr(dJ,60),
             'dkappa_ddelta':mp.nstr(dK,60)})


a=mp.sqrt(2)
lam0=lambda r:r*g(r)*(r/mp.tanh(r)-mp.mpf(5)/2)
eta0=lambda r:r**3*g(r)+lam0(r)*r*r
r0=mp.findroot(lambda r:a**3*g(a)+2*lam0(r)-eta0(r),(mp.mpf(5),mp.mpf(6)))
slope=eta0(r0)/4
jrig=mp.quad(g,[0,a])
asym=[]
for cs in ['0.001','0.0001','0.00001']:
    c=mp.mpf(cs); b=2*c*r0*r0/(2+c*r0*r0); h=1-b
    H=1/(c*c); k=b*b/(c-h*h/H)
    edges, comp, _=star([1,h,b],[H,k])
    assert abs(comp-c) < mp.mpf('1e-70')
    jj=objective(edges)
    # The first order acoustic and optical widths are reconstructed separately.
    actual_acoustic=(a-edges[0])/c
    acoustic_limit=a*r0*r0/(2*(r0*r0-2))
    actual_optical=(edges[2]-edges[1])/c
    optical_limit=r0**3/(2*(r0*r0-2))
    asym.append({'C':cs,'saving_div_C':mp.nstr((jrig-jj)/c,40),
                 'acoustic_width_div_C':mp.nstr(actual_acoustic,30),
                 'optical_width_div_C':mp.nstr(actual_optical,30),
                 'total_springs':mp.nstr(H+k,30)})
rows.append({'case':'R44 small compliance asymptotic', 'r0':mp.nstr(r0,70),
             'slope':mp.nstr(slope,70),
             'acoustic_width_limit':mp.nstr(acoustic_limit,40),
             'optical_width_limit':mp.nstr(optical_limit,40), 'actual_networks':asym})

(HERE/'independent_checks.json').write_text(json.dumps(rows,indent=2)+'\n')
print('PASS: exact non-star matrix/resource identities and series coefficients;')
print('PASS: independent 90-digit matrices, all-band quadrature, dual root residuals,')
print('      positive inverses, branch-splitting derivatives, and sharp-slope diagnostics.')
for row in rows:
    print(row['case'],row.get('J',row.get('slope','')))
