"""Exact-model numerical checks of a finite-stage resource theorem.

Uses high-precision products, an independent polygon-area calculation, and
random closed positive-factor paths. These are mathematical computations,
not empirical evidence or a numerical proof of global optimality.
"""
from pathlib import Path
import json,random,time
import mpmath as mp

mp.mp.dps=100
P=Path(__file__).resolve().parent
I=mp.eye(2)
start=time.perf_counter()

def R(t):
    c,s=mp.cos(t),mp.sin(t)
    return mp.matrix([[c,-s],[s,c]])

def anisotropy(k,alpha):
    r=R(alpha)
    return r*mp.diag([mp.exp(-k),mp.exp(k)])*r.T

def norm(M):
    return mp.sqrt(sum(v*v for v in M))

def mincost(N,theta):
    theta=abs(theta)
    if theta==0:
        return mp.mpf(0)
    if not N>2+2*theta/mp.pi:
        return mp.inf
    return N*mp.acosh(mp.cos(mp.pi/N)/mp.cos((mp.pi+theta)/N))

def point(M):
    return mp.matrix([(M[0,0]+M[1,1])/2,(M[0,0]-M[1,1])/2,M[0,1]])

def lorentz(u,v):
    return u[0]*v[0]-u[1]*v[1]-u[2]*v[2]

def tri_area(u,v,w):
    det=mp.det(mp.matrix([[u[0],v[0],w[0]],
                          [u[1],v[1],w[1]],
                          [u[2],v[2],w[2]]]))
    den=1+lorentz(u,v)+lorentz(v,w)+lorentz(w,u)
    return 2*mp.atan2(det,den)

def polygon_area(vertices):
    pts=list(map(point,vertices))
    return sum(tri_area(pts[0],pts[j],pts[j+1]) for j in range(1,len(pts)-2))

def product_and_polygon(factors):
    G=mp.eye(2);vertices=[I]
    for H in factors:
        G=H*G
        vertices.append(G.T*G)
    return G,vertices

tests=[]
angles=[mp.mpf('.01'),mp.pi/12,mp.pi/3,mp.pi/2,
        mp.pi-mp.mpf('0.001'),mp.pi,-mp.pi/3]
for N in [3,4,5,6,8,16,64]:
    for theta in angles:
        cost=mincost(N,theta)
        if not mp.isfinite(cost):
            continue
        ell=cost/N
        delta=mp.sign(theta)*(mp.pi+abs(theta))/N
        factors=[anisotropy(ell,j*delta) for j in range(N)]
        G,vertices=product_and_polygon(factors)
        area=polygon_area(vertices)
        err=norm(G-R(theta))
        areaerr=abs(area-2*theta)
        assert err < mp.mpf('1e-85')
        assert areaerr < mp.mpf('1e-85')
        tests.append({'N':N,'theta':mp.nstr(theta,18),'minimum_s':mp.nstr(cost,18),
                      'minimum_worst_condition_number':mp.nstr(mp.exp(2*ell),18),
                      'matrix_residual':mp.nstr(err,8),
                      'signed_polygon_area':mp.nstr(area,18),
                      'area_residual':mp.nstr(areaerr,8)})

rng=random.Random(472905)
random_tests=[]
for N in [3,4,5,6,8,12]:
    for trial in range(20):
        ks=[mp.mpf(str(rng.uniform(.02,3.0))) for _ in range(N-1)]
        alphas=[mp.mpf(str(rng.uniform(-3.14,3.14))) for _ in range(N-1)]
        factors=[anisotropy(k,a) for k,a in zip(ks,alphas)]
        G,_=product_and_polygon(factors)
        S=G*G.T
        # det S=1, so this is its exact 2x2 inverse square-root formula.
        last=(S**-1+I)/mp.sqrt(mp.trace(S)+2) if hasattr(mp,'trace') else (S**-1+I)/mp.sqrt(S[0,0]+S[1,1]+2)
        factors.append(last)
        G,vertices=product_and_polygon(factors)
        theta=mp.atan2(G[1,0],G[0,0])
        klast=mp.acosh((last[0,0]+last[1,1])/2)
        actual=sum(ks)+klast
        lower=mincost(N,theta)
        area=polygon_area(vertices)
        holonomy_error=norm(R(area/2)-G)
        assert holonomy_error < mp.mpf('1e-65')
        assert actual >= lower-mp.mpf('1e-60')
        random_tests.append({'N':N,'trial':trial,'theta':mp.nstr(theta,15),
                             'sum_k':mp.nstr(actual,15),'lower_s':mp.nstr(lower,15),
                             'ratio':mp.nstr(actual/lower,15),
                             'signed_area':mp.nstr(area,15),
                             'winding_shift':int(mp.nint((area/2-theta)/(2*mp.pi))),
                             'holonomy_residual':mp.nstr(holonomy_error,8)})

out={'scope':'Exact-model verification; no physical data or global-proof-by-sampling claim',
     'decimal_precision':mp.mp.dps,'attainer_checks':tests,
     'random_closed_polygon_checks':random_tests,
     'wall_seconds':time.perf_counter()-start}
(P/'finite_stage_checks.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'attainer_count':len(tests),'random_count':len(random_tests),
                  'pi_N5':next(v for v in tests if v['N']==5 and abs(mp.mpf(v['theta'])-mp.pi)<mp.mpf('1e-16')),
                  'largest_matrix_residual':max(float(t['matrix_residual']) for t in tests),
                  'largest_holonomy_residual':max(float(t['holonomy_residual']) for t in random_tests),
                  'wall_seconds':out['wall_seconds']},indent=2))
