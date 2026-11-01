#!/usr/bin/env python3
"""Rigorous deterministic candidate variance, not an actual-chain CLT.
All proof arithmetic is exact integer/rational/directed dyadic arithmetic.
The accepted scalar clock source is imported read-only and never changed.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,json,sys,time
SCALAR=Path(__file__).resolve().parent.parent/'inverse_clearance_clock_20261101'
sys.path.insert(0,str(SCALAR))
import validated_clock as vc
IV=vc.IV;Q=vc.Q

def exp_positive(z):
    """Enclose exp(z), z>=0, by scaling and a positive series/geometric tail."""
    assert z.lo>=0
    k=0
    while z.hi>Q//8:
        z=z/2;k+=1
    term=IV.exact(1);out=term
    n=18
    for j in range(1,n+1):
        term=term*z/j;out=out+term
    next_term=term*z/(n+1)
    remainder=next_term/(IV.exact(1)-z/(n+2))
    out=out+IV(0,remainder.hi)
    for _ in range(k):out=out*out
    return out

def exp_negative(z):return exp_positive(z).reciprocal()
def invpow(x,n):return (x**n).reciprocal()
def asF(x):return F(x,Q)

def forward_polynomial(degree,init):
    p=[F(0)]*(degree+1)
    for n in range(degree):
        p2=vc.conv(p[:n+1],p[:n+1]);p4=vc.conv(p2,p2)
        rhs=F(2) if n==2 else F(0)
        if n>=1:rhs+=3*p2[n-1]
        rhs+=F(9,8)*p4[n]
        p[n+1]=rhs/(n+1)
    assert all(not c or j%5==3 for j,c in enumerate(p))
    s0=F(1,2);R0=F(init['residual_max']);L=F(init['lipschitz'])
    delta3=R0/(s0*s0*(3-L*s0))
    assert vc.peval(p,s0)+delta3*s0**3<F(1,4)
    C=F(84,125)
    assert vc.peval(p,s0)/s0**3+delta3<C
    coeff=[IV.exact(p[j]) for j in range(3,degree+1,5)]
    def bounds(s):
        ss=IV.exact(s);x=ss**5
        v=coeff[-1]
        for c in reversed(coeff[:-1]):v=v*x+c
        ss3=ss**3
        pp=v*ss3
        return IV(pp.lo,(pp+delta3*ss3).hi)
    return bounds,delta3,C

def variance_rectangles(levels,qs):
    """Integrate decreasing q^2 against increasing l using endpoint bounds."""
    total=IV.exact(0)
    for i in range(len(levels)-1):
        dl=IV(max(0,levels[i+1].lo-levels[i].hi),levels[i+1].hi-levels[i].lo)
        assert dl.hi>=0
        lower=IV(qs[i+1].lo,qs[i+1].lo)**2*IV(dl.lo,dl.lo)
        upper=IV(qs[i].hi,qs[i].hi)**2*IV(dl.hi,dl.hi)
        total=total+IV(lower.lo,upper.hi)
    return total

def solve(grid_power=10,startup_steps=1024,E=8,order=5):
    start=time.monotonic_ns()
    a,initial,init=vc.startup(78)
    forward,delta3,C=forward_polynomial(78,init)
    for k in vc.OPS:vc.OPS[k]=0
    s0=F(1,2);s=initial;e=a
    nodes=[(a,s,s+F(3,4)*IV.exact(a)**2)]
    Hpieces=[];steps=0
    h0=F(1,1<<grid_power)
    while e<E:
        h=min(h0,F(E)-e)
        smid,_=vc.step(e,h/2,s,order)
        send,_=vc.step(e+h/2,h/2,smid,order)
        lstart=nodes[-1][2]
        lmid=smid+F(3,4)*IV.exact(e+h/2)**2
        lend=send+F(3,4)*IV.exact(e+h)**2
        assert lstart.lo>0
        Hmid=invpow(lmid,3)
        L=IV(lstart.lo,lstart.lo)
        V=F(1,2)*invpow(L,2)+F(3,2)*IV.exact(e+h)
        # |(l^-3)''| <= 12v^2/l^5+3v/l^7+(9/2)/l^4.
        M=12*V*V*invpow(L,5)+3*V*invpow(L,7)+F(9,2)*invpow(L,4)
        err=M*IV.exact(h**3/F(24))
        piece=Hmid*IV.exact(h)+IV(-err.hi,err.hi)
        assert piece.hi>=0
        Hpieces.append(IV(max(0,piece.lo),piece.hi))
        e+=h;s=send;nodes.append((e,s,lend));steps+=1
    Ef=F(E);slo,shi=map(asF,[s.lo,s.hi])
    time_tail=F(8,27)/Ef**3;U=shi+time_tail
    H0=F(64,135)/Ef**5
    Hlo=H0-F(256,189)*U/Ef**7
    Hhi=H0-F(256,189)*slo/Ef**7+F(2048,729)*slo*slo/Ef**9
    assert 0<Hlo<=Hhi<=H0
    H=IV.bounds(Hlo,Hhi)
    Js=[None]*len(nodes);Js[-1]=exp_negative(H)
    for i in range(len(Hpieces)-1,-1,-1):
        H=H+Hpieces[i];Js[i]=exp_negative(H)
    qs=[IV(max(0,Q-j.hi),min(Q,Q-j.lo)) for j in Js]
    inverse=variance_rectangles([n[2] for n in nodes],qs)
    # Relate inverse a>=e(s0) back to the exact forward s0.
    gap_e=a-F(init['forward_e_lower'])
    J0=IV((Js[0]*IV.exact(1-8*gap_e)).lo,Js[0].hi)
    assert J0.lo>0 and J0.hi<Q
    # e(s)/s^3 in [2/3,C] gives elementary regularized J startup.
    Klo=F(2,3)/(1+F(3,4)*C*C*s0**5)
    Khi=F(3,2)*C*C
    levels=[];qstart=[]
    for j in range(startup_steps+1):
        ss=s0*F(j,startup_steps);ee=forward(ss)
        levels.append(IV.exact(ss)+F(3,4)*ee*ee)
        if j==0:J=IV.exact(0)
        else:
            integ=IV.bounds(Klo*(s0**5-ss**5)/5,Khi*(s0**5-ss**5)/5)
            J=J0*IV.exact((ss/s0)**2)*exp_positive(integ)
        qstart.append(IV(max(0,Q-J.hi),min(Q,Q-J.lo)))
    startup=variance_rectangles(levels,qstart)
    gap_max=asF(nodes[0][2].hi)-asF(levels[-1].lo)
    assert gap_max>=0
    tail=F(4096,18225)*(F(8,117)/Ef**13+F(3,16)/Ef**8)
    total=startup+inverse+IV.bounds(0,gap_max+tail)
    lo,hi=asF(total.lo),asF(total.hi)
    out={'status':'RIGOROUS_DETERMINISTIC_CANDIDATE_VARIANCE_AUTHOR_PENDING_REVIEW',
         'meaning':'Integral (1-J)^2 dl along origin ODE orbit; not actual-chain CLT or finite-noise diffusion variance.',
         'bits':vc.BITS,'inverse_taylor_order':order,'inverse_grid_power':grid_power,
         'inverse_intervals':steps,'inverse_taylor_half_steps':2*steps,'startup_intervals':startup_steps,
         'terminal_e':str(Ef),'sigma_squared_lower':str(lo),'sigma_squared_upper':str(hi),
         'sigma_squared_decimal_outward':[vc.dec_down(lo,10),vc.dec_up(hi,10)],
         'total_width':str(hi-lo),'total_width_decimal_upper':vc.dec_up(hi-lo,12),
         'startup_variance_lower':str(asF(startup.lo)),'startup_variance_upper':str(asF(startup.hi)),
         'startup_width':str(asF(startup.hi-startup.lo)),
         'inverse_variance_lower':str(asF(inverse.lo)),'inverse_variance_upper':str(asF(inverse.hi)),
         'inverse_width':str(asF(inverse.hi-inverse.lo)),
         'gap_variance_upper':str(gap_max),'tail_variance_upper':str(tail),
         'tail_and_gap_charged_width':str(F(vc.ceilq(gap_max+tail),Q)),
         'tail_and_gap_rounding_excess':str(F(vc.ceilq(gap_max+tail),Q)-gap_max-tail),
         'target_width_less_than_1e_minus_3':bool(hi-lo<F(1,1000)),
         'J_at_s_half_lower':str(asF(J0.lo)),'J_at_s_half_upper':str(asF(J0.hi)),
         'H_tail_lower':str(Hlo),'H_tail_upper':str(Hhi),
         'startup_cubic_barrier_delta':str(delta3),'startup_e_over_s3_upper':str(C),
         'startup_regular_integrand_coeff_lower':str(Klo),'startup_regular_integrand_coeff_upper':str(Khi),
         'inverse_s_terminal_width':str(asF(s.hi-s.lo)),
         'integer_interval_operations':vc.OPS.copy(),'wall_nanoseconds_nonproof':time.monotonic_ns()-start,
         'scalar_code_sha256':hashlib.sha256((SCALAR/'validated_clock.py').read_bytes()).hexdigest(),
         'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--grid-power',type=int,default=10)
    p.add_argument('--startup-steps',type=int,default=1024);p.add_argument('--end',type=int,default=8)
    p.add_argument('--order',type=int,default=5);p.add_argument('--output',default='VARIANCE_CERTIFICATE.json')
    args=p.parse_args();assert args.grid_power>=1 and args.startup_steps>=1 and args.end>=2 and args.order>=2
    result=solve(args.grid_power,args.startup_steps,args.end,args.order)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','sigma_squared_decimal_outward','total_width_decimal_upper','inverse_intervals','startup_intervals','integer_interval_operations','wall_nanoseconds_nonproof']},indent=2))
