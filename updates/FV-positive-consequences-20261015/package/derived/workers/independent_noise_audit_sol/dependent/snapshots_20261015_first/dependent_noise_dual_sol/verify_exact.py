"""Standalone exact verifier. Uses only the Python standard library.

It checks dual inequalities on their entire finite support and handles all
remaining lattice nodes analytically. Mean interpolation then handles all
centers, and the accompanying proof handles every lattice coset.
"""
from fractions import Fraction as Q
from pathlib import Path
import json

OUT=Path(__file__).resolve().parent

def verify_dual(path):
    r=json.loads(path.read_text())
    K=r['K'];cx,cy=map(Q,r['center']);lower=Q(r['proved_lower'])
    nodes={(i,j):(2*i-cx)**2+(2*j-cy)**2
           for i in range(-K-1,K+2) for j in range(-K-1,K+2)}
    for i,j,u,v,y in r['multipliers']:
        u,v,y=Q(u),Q(v),Q(y)
        assert y>=0 and u*u+v*v==1
        assert -K-1<=i<=K and -K-1<=j<=K
        for da,db,sx,sy in [(0,0,1,1),(1,0,-1,1),(0,1,1,-1),(1,1,-1,-1)]:
            nodes[i+da,j+db]+=y*(u*sx+v*sy-1)
    assert min(nodes.values())>=lower
    outside=min((2*K+4-abs(cx))**2,(2*K+4-abs(cy))**2)
    assert outside>=lower
    return (cx,cy),lower

def quad_min(l00,l10,l01,l11,h):
    # Local coordinates t,u in [0,1]. This exact quadratic lower-bounds
    # the centered cost at every point of the complete rectangle.
    hh=h*h
    ax=l10-l00-hh;ay=l01-l00-hh
    b=l11-l10-l01+l00
    def clamp(x):return max(Q(0),min(Q(1),x))
    candidates=[(Q(t),Q(u)) for t in (0,1) for u in (0,1)]
    for t in (Q(0),Q(1)):candidates.append((t,clamp(-(ay+b*t)/(2*hh))))
    for u in (Q(0),Q(1)):candidates.append((clamp(-(ax+b*u)/(2*hh)),u))
    determinant=4*hh*hh-b*b
    if determinant>0:
        t=(-2*hh*ax+b*ay)/determinant
        u=(b*ax-2*hh*ay)/determinant
        if 0<=t<=1 and 0<=u<=1:candidates.append((t,u))
    # If the Hessian is indefinite, an interior stationary point cannot
    # be a minimum. If singular, a minimizing flat line reaches an edge.
    value=lambda t,u:l00+ax*t+ay*u+b*t*u+hh*(t*t+u*u)
    answer=min((value(t,u),t,u) for t,u in candidates)
    return answer

def verify_upper(path):
    r=json.loads(path.read_text());N=r['N'];rho=Q(r['rho'])
    p={(a,b):Q(c) for a,b,c in r['p_table']}
    assert 0<rho<1
    assert set(p)=={(a,b) for a in range(N+1) for b in range(a+1)}
    assert min(p.values())>=0
    def value(i,j):
        a,b=sorted((min(i,N),min(j,N)),reverse=True)
        return p[a,b]
    determinant=[]
    for i in range(N+1):
        for j in range(i+1):
            a=value(i,j);b=rho*value(i+1,j);c=rho*value(i,j+1);d=rho*rho*value(i+1,j+1)
            S=a+b+c+d;Z=a-b+c-d;X=a+b-c-d
            assert S>=0 and S*S>=Z*Z+X*X
            determinant.append(S*S-Z*Z-X*X)
    d=[Q(1)]+[Q(2)]*(N-1)+[2/(1-rho)]
    s=[Q(0)]+[Q(2*i*i) for i in range(1,N)]
    s.append(2*(N*N/(1-rho)+2*N*rho/(1-rho)**2+rho*(1+rho)/(1-rho)**3))
    Z=C=Q(0)
    for i in range(N+1):
        for j in range(N+1):
            a,b=sorted((i,j),reverse=True)
            q=rho**(i+j)*p[a,b]
            Z+=q*d[i]*d[j]
            C+=4*q*(s[i]*d[j]+d[i]*s[j])
    assert Z>0
    trace=C/Z
    assert trace==Q(r['trace_covariance_exact'])
    assert trace<=Q(r['proved_upper'])
    assert p[0,0]*p[1,1]!=p[1,0]*p[1,0] # Dependence is exact.
    return trace,Q(r['proved_upper']),min(determinant)

def main():
    lower_by_center={}
    verified=[]
    for path in sorted(OUT.glob('adaptive_dual_K*.json')):
        center,lower=verify_dual(path)
        for p in (center,center[::-1]):lower_by_center[p]=max(lower_by_center.get(p,Q(0)),lower)
        verified.append(path.name)
    h=Q(1,4)
    rectangles=[]
    for i in range(4):
        for j in range(4):
            x,y=Q(i,4),Q(j,4)
            values=[lower_by_center[p] for p in [(x,y),(x+h,y),(x,y+h),(x+h,y+h)]]
            lower,t,u=quad_min(*values,h)
            rectangles.append({'lower_corner':[str(x),str(y)],'lower':str(lower),
                               'minimizer':[str(x+h*t),str(y+h*u)]})
    minimum=min(Q(r['lower']) for r in rectangles)
    readable=Q(minimum.numerator*10**7//minimum.denominator,10**7)
    uppers=[]
    for path in sorted(OUT.glob('certified_upper_N*.json')):
        trace,upper,det=verify_upper(path)
        uppers.append({'file':path.name,'trace_exact':str(trace),'upper':str(upper),
                       'trace_float':float(trace),'minimum_scaled_determinant':str(det)})
    best=min(uppers,key=lambda r:Q(r['upper']))
    result={'verification':'PASSED using exact rational arithmetic only',
            'universal_lower_exact':str(minimum),'universal_lower_readable':str(readable),
            'universal_lower_float':float(minimum),'best_upper':best,
            'gap_using_readable_bounds':str(Q(best['upper'])-readable),
            'dual_files_verified':verified,'mean_rectangles':rectangles,'upper_files_verified':uppers,
            'scope':'all scalar probability measures on R^2 with finite covariance and full Fourier POVM positivity'}
    (OUT/'EXACT_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['dual_files_verified','mean_rectangles','upper_files_verified']},indent=2))

if __name__=='__main__':main()
