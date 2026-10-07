"""Exact digital stochastic codec for Q_p G_L(X), with a Gaussian proof report.
All encoder/decoder probability arithmetic is rational or integer.
Normal draws/CDFs in diagnostics alone are floating and are not certified.
"""
from fractions import Fraction as F
import math, random, time, pathlib, json


def triangle_cdf(t,j,J):
    t=F(t)
    if not (0<=t<=1) or not (0<=j<J) or J<3: raise ValueError('bad triangle')
    x=J*t
    if j==0:
        if x<=1: return x-x*x/2
        if x<=J-1: return F(1,2)
        return F(1,2)+(x-(J-1))**2/2
    if x<=j-1: return F(0)
    if x<=j: return (x-(j-1))**2/2
    if x<=j+1: return 1-(j+1-x)**2/2
    return F(1)


def encode_bin(k,p,J,bits):
    N=1<<p
    if not 0<=k<N or not 0<=bits<2*N: raise ValueError('bad input')
    q,rem=divmod(J*(2*k+1),2*N)
    return (q+1)%J if bits<rem else q%J


def decode_bin(j,p,J,bits):
    N=1<<p; D=1<<(2*p+1)
    if not 0<=bits<D: raise ValueError('bad randomness')
    lo=0;hi=N-1;steps=0
    while lo<hi:
        mid=(lo+hi)//2
        n=triangle_cdf(F(mid+1,N),j,J)*D
        assert n.denominator==1
        if bits<n.numerator: hi=mid
        else: lo=mid+1
        steps+=1
    return lo,steps


def plan(radius,epsilon):
    L=1+F(radius);epsilon=F(epsilon)
    if L<1 or not 0<epsilon<1: raise ValueError('bad precision/radius')
    q=846*L*L/epsilon
    J=max(3,math.isqrt(q.numerator//q.denominator))
    while J*J<q: J+=1
    p=0
    while (1<<p)*epsilon<J: p+=1
    return {'J':J,'input_output_bits':p,'archive_bits':(J-1).bit_length(),
        'encoder_random_bits':p+1,'decoder_random_bits':2*p+1,
        'ideal_TV_upper':str(423*L*L/(J*J)),
        'input_midpoint_TV_upper':str(F(J,2*(1<<p))),
        'total_TV_upper':str(423*L*L/(J*J)+F(J,2*(1<<p))),
        'total_TV_upper_float':float(423*L*L/(J*J)+F(J,2*(1<<p)))}


def normal_cdf(x): return 0.5*(1+math.erf(x/math.sqrt(2)))


def numeric_fixture(theta,L,J,p):
    N=1<<p
    boundaries=[0.0]
    for k in range(1,N): boundaries.append(normal_cdf(L*math.tan(math.pi*(k/N-0.5))-theta))
    boundaries.append(1.0)
    pin=[boundaries[k+1]-boundaries[k] for k in range(N)]
    labels=[0.0]*J
    for k,prob in enumerate(pin):
        q,rem=divmod(J*(2*k+1),2*N)
        labels[q%J]+=prob*(1-rem/(2*N))
        labels[(q+1)%J]+=prob*rem/(2*N)
    out=[0.0]*N
    for j,weight in enumerate(labels):
        old=F(0)
        for k in range(N):
            now=triangle_cdf(F(k+1,N),j,J)
            out[k]+=weight*float(now-old);old=now
    tv=sum(abs(x-y) for x,y in zip(pin,out))/2
    bound=423*L*L/(J*J)+J/(2*N)
    assert tv<=bound+1e-12 and abs(sum(out)-1)<1e-12
    return {'theta':theta,'L':L,'J':J,'p':p,'TV_float':tv,'analytic_upper':bound}


def main():
    start=time.perf_counter(); exact=0
    # Exact finite-state checks: every rational CDF bin has a common dyadic denominator.
    for J in [3,5,8,13]:
        for p in [3,5,7]:
            N=1<<p; D=1<<(2*p+1)
            for j in range(J):
                vals=[triangle_cdf(F(k,N),j,J) for k in range(N+1)]
                assert vals[0]==0 and vals[-1]==1 and all(a<=b for a,b in zip(vals,vals[1:]))
                assert all((x*D).denominator==1 for x in vals)
                for k in [0,N//2,N-1]:
                    a=int(vals[k]*D);b=int(vals[k+1]*D)
                    if a<b:
                        for r in [a,b-1]:
                            got,steps=decode_bin(j,p,J,r);assert got==k and steps<=p;exact+=1
            for k in range(N):
                q,rem=divmod(J*(2*k+1),2*N)
                counts=[0]*J
                for r in range(2*N): counts[encode_bin(k,p,J,r)]+=1
                assert counts[q%J]==2*N-rem and counts[(q+1)%J]==rem
                exact+=1
    diagnostic=[numeric_fixture(theta,2.0,J,8) for J in [4,8,16,32] for theta in [-1.0,0.0,1.0]]
    plans=[plan(F(1),F(1,10)),plan(F(1),F(1,1000)),plan(F(10),F(1,1000))]
    result={'exact_probability_and_endpoint_fixtures':exact,'float_Gaussian_diagnostics':diagnostic,
        'plans':plans,'elapsed_seconds':time.perf_counter()-start,
        'scope':'Digital probability compiler is exact. Gaussian quadrature fixtures are floating diagnostics. No hardware Gaussian instrument/continuous-output claim.'}
    out=pathlib.Path(__file__).with_name('gaussian_codec_checks.json');out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'exact_fixtures':exact,'plans':plans,'elapsed_seconds':result['elapsed_seconds'],'output':str(out)},indent=2))

if __name__=='__main__': main()
