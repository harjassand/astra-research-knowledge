"""Small synthetic-coefficient tests. No physical property table is asserted."""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from nasa_secant import nasa7_h,nasa7_s0,nasa7_h_secant,splice_diagnostics

R=np.array([300.,260.])
low=np.array([[3.5,1e-4,-2e-8,1e-12,-5e-17,0.,1.],
              [3.7,2e-4,-3e-8,2e-12,-8e-17,1200.,2.]])
high=np.array([[2.9,8e-4,-3e-8,2e-12,-1e-17,0.,0.],
               [3.1,6e-4,-2e-8,3e-12,-2e-17,0.,0.]])
# Construct continuous synthetic h and s at the test splice, explicitly.
high[:,5]+=(nasa7_h(1000.,low,R)-nasa7_h(1000.,high,R))/R
high[:,6]+=(nasa7_s0(1000.,low,R)-nasa7_s0(1000.,high,R))/R
pairs=[(300.,2700.),(2700.,300.),(999.9999,1000.0001),
       (1000.-1e-10,1000.+1e-10),(1000.,1000.),(850.,850.+1e-10),
       (300.,999.),(1001.,2700.)]
rows=[]
for tl,tr in pairs:
    got=nasa7_h_secant(tl,tr,low,high,R)
    lo,hi=min(tl,tr),max(tl,tr)
    # Independent high-accuracy quadrature in beta; split at the thermo splice.
    if lo==hi:
        want=nasa7_h(lo,low if lo<=1000 else high,R)
    else:
        cuts=[lo]+([1000.] if lo<1000<hi else [])+[hi]
        want=np.zeros(2)
        for l,h in zip(cuts[:-1],cuts[1:]):
            a=low if h<=1000 else high
            weight=(h-l)*lo*hi/((hi-lo)*l*h)
            # Algebraically stable beta interpolation; no reciprocal subtraction.
            for i in range(2):
                f=lambda s:nasa7_h(l*h/(h+s*(l-h)),a,R)[i]
                want[i]+=weight*quad(f,0,1,epsabs=1e-7,epsrel=2e-13)[0]
    err=float(np.max(np.abs(got-want)/np.maximum(1,np.abs(want))))
    sym=float(np.max(np.abs(got-nasa7_h_secant(tr,tl,low,high,R))))
    assert err<2e-12,(tl,tr,got,want)
    assert sym==0.
    rows.append({'TL_K':tl,'TR_K':tr,'max_relative_quadrature_error':err,
                 'endpoint_swap_absolute_error_J_per_kg':sym})
diag={k:np.asarray(v).tolist() for k,v in splice_diagnostics(low,high,R).items()}
result={'scope':'Synthetic NASA7 coefficients; no project mechanism was loaded or modified.',
        'splice_diagnostics':diag,'rows':rows}
Path(__file__).with_name('nasa_secant_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
