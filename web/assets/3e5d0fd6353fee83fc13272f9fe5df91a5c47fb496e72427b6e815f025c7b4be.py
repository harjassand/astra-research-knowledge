"""Small scalar potential diagnostics; no eigensolver or external dependencies."""
import json,math
from pathlib import Path

def density_phi(z): return math.exp(-z*z/2)/math.sqrt(2*math.pi)
def cdf(z): return .5*math.erfc(-z/math.sqrt(2))
def sf(z): return .5*math.erfc(z/math.sqrt(2))
def interval_mass(z,w):
    if w>=0: return sf(w)-sf(z)
    return cdf(z)-cdf(w)
def potential(x,a,tau):
    z=(x-tau)/math.sqrt(tau);w=z-a/math.sqrt(tau)
    mass=interval_mass(z,w)
    first=density_phi(z)-density_phi(w)
    second=-z*density_phi(z)+w*density_phi(w)
    vp=1-first/(math.sqrt(tau)*mass)
    curvature=(first*first/(mass*mass)-second/mass)/tau
    return vp*vp/4+curvature/2,curvature

rows=[]
for tau in [.05,.1,.25]:
    for a in [2.,4.,8.,16.,32.]:
        values=[potential(-2+(a+4)*i/600,a,tau) for i in range(601)]
        rows.append({'tau':tau,'length':a,'sampled_partner_potential_min':min(v[0] for v in values),
                     'sampled_curvature_min':min(v[1] for v in values),
                     'sampled_curvature_max':max(v[1] for v in values)})
        assert min(v[1] for v in values)>-1e-8
        assert max(v[1] for v in values)<1/tau+1e-8
        assert min(v[0] for v in values)>=.25-1e-8
mills=[]
for z in [-8,-4,-2,-1,-.5,0,.5,1,2,4,8]:
    m=density_phi(z)/cdf(z)
    assert 3*m+2*z>1
    mills.append({'z':z,'m':m,'three_m_plus_two_z':3*m+2*z})
out={'status':'DIAGNOSTIC_ONLY','potential_fixtures':rows,'mills_fixtures':mills,
     'scope':'Sampled scalar potential/curvature and Mills bounds; no exact-gap eigenfunction acquisition or MI quadrature'}
Path(__file__).with_name('heated_potential_check.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'status':out['status'],'potential_fixtures':len(rows),
                  'minimum_sampled_partner_potential':min(r['sampled_partner_potential_min'] for r in rows)}))
