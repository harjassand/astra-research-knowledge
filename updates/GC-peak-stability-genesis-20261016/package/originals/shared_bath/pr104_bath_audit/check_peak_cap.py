"""Independent integral/boundary verification, not numerical fitting."""
import json, math
from scipy.integrate import quad
rows=[]
for J,tau,L,Lambda in [(1,2,2,3),(0.3,1,2,2),(.7,2,2,2),(.5,1,1,0),(.4,1,3,2)]:
    d=J/L; a=J*tau; q=(a-d*Lambda)/2
    assert 0<=q<=d+1e-14
    def V(u): return 2*d+(q-d)*(math.exp(-u)+math.exp(-(Lambda-u)))
    def direct(u):
        return d*quad(lambda v:math.exp(-abs(u-v)),0,Lambda,points=[u])[0]+q*(math.exp(-u)+math.exp(-(Lambda-u)))
    potential_error=max(abs(V(u)-direct(u)) for u in [0,Lambda/5,Lambda/2,Lambda])
    energy_direct=d*quad(V,0,Lambda)[0]+q*(V(0)+V(Lambda))
    e=math.exp(-Lambda)
    formula=2*d*d*(Lambda-1+e)+4*d*q*(1-e)+2*q*q*(1+e)
    assert potential_error<1e-12 and abs(energy_direct-formula)<1e-12
    assert all(V(u)>=V(0)-1e-12 for u in [0,Lambda/5,Lambda/2,Lambda])
    row=dict(J=J,tau=tau,L=L,Lambda=Lambda,q=q,potential_error=potential_error,energy_direct=energy_direct,formula=formula)
    if abs(L*tau-Lambda-2)<1e-12:
        row['unconstrained_boundary']=2*a*a/(Lambda+2)
        assert abs(formula-row['unconstrained_boundary'])<1e-12
    if abs(L*tau-Lambda)<1e-12:
        row['constant_rate_boundary']=2*J*J*(tau/L-(1-e)/(L*L))
        assert abs(formula-row['constant_rate_boundary'])<1e-12
    if Lambda==0: assert abs(formula-a*a)<1e-12
    rows.append(row)
print(json.dumps(dict(checks=rows,status='PASS',scope='Potential, kernel energy, and boundary formula checks only; global optimality is analytic.'),indent=2))
