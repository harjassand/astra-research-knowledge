"""Comparison model ONLY. No fits, no imported author code, no measured-channel claim.
Units: seconds and radians/second. Standard-library implementation.
"""
import math, json

def weights(T, flips, delta, phase):
    """Exact integrals of ideal toggling y over hold cells; next update at phase.
    phase in (0,delta], instantaneous flips strictly within (0,T).
    """
    assert T>=0 and delta>0 and 0<phase<=delta
    cuts=sorted(set([0.,T]+[x for x in flips if 0<x<T]+[phase+k*delta for k in range(max(0,math.ceil((T-phase)/delta))) if 0<phase+k*delta<T]))
    out={}
    for a,b in zip(cuts,cuts[1:]):
        mid=(a+b)/2
        cell=math.floor((mid-phase)/delta)
        sign=(-1)**sum(f<mid for f in flips)
        out[cell]=out.get(cell,0.)+sign*(b-a)
    return list(out.values())

def conditional_W(T,flips,delta,phase,sigma):
    return math.exp(-sigma*sigma*sum(a*a for a in weights(T,flips,delta,phase))/2)

def hahn_uniform(T,delta,sigma):
    """Exact phase average for T <= delta; ideal instantaneous Hahn only."""
    assert 0<=T<=delta and sigma>=0
    if sigma==0:return 1.
    return 1-T/delta+math.sqrt(math.pi)*math.erf(sigma*T/2)/(sigma*delta)

def tests():
    assert abs(conditional_W(.02,[.01],.1,.05,1000)-1)<1e-14
    assert abs(conditional_W(.02,[],.1,.05,100)-math.exp(-2))<1e-14
    assert abs(conditional_W(.02,[.01],.1,.01,100)-math.exp(-1))<1e-14
    for T in [.0007555,.0155655,.0290445,.1]:
        numeric=sum(conditional_W(T,[T/2],.1,(j+.5)*.1/20000,1000) for j in range(20000))/20000
        assert abs(numeric-hahn_uniform(T,.1,1000))<1e-7
    # A-B-A, phase-zero resonant pi rotations, order a,b,s.
    A=[[0,0,-1j],[0,1,0],[-1j,0,0]]
    B=[[1,0,0],[0,0,-1j],[0,-1j,0]]
    def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    U=mul(A,mul(B,A))
    assert U==[[0,-1,0],[-1,0,0],[0,0,-1]]
    assert mul(U,U)==[[1,0,0],[0,1,0],[0,0,1]]
    return 'PASS: analytic uniform-phase Hahn against quadrature, hold weights, and exact three-pulse swap.'

if __name__=='__main__':
    print(tests())
    print(json.dumps({'warning':'Ideal comparison model only; uniform update phase is stipulated, pulse errors omitted. No fitted or measured echo benefit.', 'delta_s':.1, 'illustrative_sigma_rad_per_s':1000, 'points':[{'T_s':T,'W_ideal':hahn_uniform(T,.1,1000),'Fchi_ideal':(1+hahn_uniform(T,.1,1000))/2,'Fchi_lower_bound_any_sigma':1-T/.2} for T in [.0007555,.0155655,.0290445]]},indent=2))
