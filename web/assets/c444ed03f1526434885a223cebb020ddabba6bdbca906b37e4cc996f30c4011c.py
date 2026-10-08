"""Finite Galerkin diagnostics and scalar certificate arithmetic.
No numerical case certifies the continuum heat kernel, trace or priority.
Run: OPENBLAS_NUM_THREADS=1 python3 outputs/research/sol_attractive_critical/thermal_checks.py
"""
import itertools
import json
import math
from pathlib import Path
import numpy as np

TOL=4e-9
J=1.


def model(K):
    pairs=list(itertools.combinations_with_replacement(range(1,K+1),2))
    Q=8*K+1
    phi=np.sqrt(2)*np.sin(np.pi*np.outer(np.arange(1,K+1),(np.arange(Q)+.5)/Q))
    v=np.array([phi[k-1]*phi[l-1]*(1 if k==l else np.sqrt(2)) for k,l in pairs])
    contact=2*v@v.T/Q
    energy=np.array([2*np.pi**2*(k*k+l*l) for k,l in pairs])
    return pairs,energy,contact


def heat(matrix,t):
    w,v=np.linalg.eigh(matrix)
    return (v*np.exp(-t*w))@v.T


remainder_ratios=[]
comm_margins=[]
cases=0
for K in (3,5,8,12):
    pairs,e,B=model(K)
    for theta in (.005,.01,.02):
        w=np.exp(-theta*e)
        H0=np.diag(w)
        dd=np.zeros((len(e),)*2)
        for i in range(len(e)):
            for j in range(len(e)):
                dd[i,j]=theta*w[i] if abs(e[j]-e[i])<1e-8 else (w[i]-w[j])/(e[j]-e[i])
        D=B*dd
        d1=2/(3*math.sqrt(math.pi))*math.sqrt(theta)
        d2=theta/6
        assert np.linalg.norm(D,2)<=d1+TOL
        for a,b in ((.1,.2),(.1,.7),(.3,.9)):
            Ta=heat(np.diag(e)+a*B,theta)
            Tb=heat(np.diag(e)+b*B,theta)
            Ea=Ta-H0+a*D
            Eb=Tb-H0+b*D
            ratios=[np.linalg.norm(Ea,2)/(a*a*d2),
                    np.linalg.norm(Eb,2)/(b*b*d2),
                    np.linalg.norm(Eb-Ea,2)/((b*b-a*a)*d2),
                    np.linalg.norm(a*Eb-b*Ea,2)/(a*b*(b-a)*d2)]
            remainder_ratios.extend(float(x) for x in ratios)
            # Finite Galerkin projection does not preserve the continuum
            # pointwise heat-kernel order. These inequalities are sampled
            # diagnostics only, not the positive-kernel argument's proof.
            assert max(ratios)<=1+TOL
            e0,e1=4*math.pi**2,20*math.pi**2
            q0=math.exp(-theta*e0)
            lead=math.sqrt(2)*(q0-math.exp(-theta*e1))**2/(e1-e0)
            ell=lead-2*q0*(a+b)*d2-2*d1*a*b*d2-2*a*a*(a+b)*d2*d2
            comm=np.linalg.norm(Ta@Tb-Tb@Ta,2)
            comm_margins.append(float(comm-(b-a)*ell))
            assert comm_margins[-1]>=-TOL
            cases+=1

# Conservative finite decimal enclosures used by the analytic certificate.
assert 9.8696<=math.pi**2<=9.8697
assert math.sqrt(2)>=1.4142
assert .6738<=math.exp(-.01*4*math.pi**2)<=.6739
assert .1388<=math.exp(-.01*20*math.pi**2)<=.1390
wlower=1.4142*(.6738-.1390)**2/(16*9.8697)
d1,d2=.0377,.001667
ell_pair=wlower-2*.6739*.8*d2-2*d1*.07*d2-2*.01*.8*d2*d2
ell_local=wlower-2*.6739*.3*d2-2*d1*.02*d2-2*.01*.3*d2*d2
assert ell_pair>=.00075
assert ell_local>=.0018
q_upper=[.6739,.2062,.02864,.001807,.00005173]
for k,q in enumerate(q_upper,start=1):
    assert math.exp(-.04*math.pi**2*k*k)<q
q6=math.exp(-.04*9.8696*36)
ratio=math.exp(-.04*9.8696*13)
tail=q6/(1-ratio)/(1-q6)
assert tail<.00000068
Sbar=math.prod(1/(1-q) for q in q_upper)*math.exp(.00000068)
assert Sbar<4
one_floor=((.6*.00075/4)**4)/256
cd=.0018**2/(8*16)
many_floor=math.exp(-217*.01/2)*(-math.expm1(-cd*.01))**2/4
assert one_floor>6e-19
assert many_floor>5e-21

out={"status":"FINITE-EVIDENCE","all_checks_passed":True,
     "Galerkin_response_cases":cases,
     "max_finite_remainder_over_bound":max(remainder_ratios),
     "min_thermal_commutator_margin":min(comm_margins),
     "free_grand_partition_upper":Sbar,
     "one_copy_full_trace_EB_certificate":one_floor,
     "every_n_full_trace_EB_certificate":many_floor,
     "certificate_local_response_margin":ell_local,
     "limitation":"Finite Galerkin algebra and scalar rounding diagnostics; continuum positivity, form limits and tensor theorem require the analytic proof."}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
