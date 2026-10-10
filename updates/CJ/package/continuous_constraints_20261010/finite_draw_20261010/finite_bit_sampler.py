#!/usr/bin/env python3
"""Capped high-precision sampler using deterministic rational certificates.

The probability/transport contract is supplied by probability_budget.py.
Unlike certified_draw.py, no floating-point Cholesky or solve is used here.
This is an implementation prototype, not an independently audited theorem.
"""
from __future__ import annotations
import argparse, hashlib, json, math, random, secrets, sys, time
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
from certified_draw import make_raw_input, acquire_certificate, N, M, D
from probability_budget import build_budget, enc, is_psd, asq

sys.set_int_max_str_digits(0)
HERE=Path(__file__).resolve().parent


def ceildiv(a,b):return -((-a)//b)
def nearest_ratio(a,b):
    assert b>0
    return (2*a+b)//(2*b)

def sufficient_bits(c,target):
    """Smallest nonnegative q with c*2^-q <= target, exact."""
    ratio=Q(c)/Q(target)
    q=max(0,ratio.numerator.bit_length()-ratio.denominator.bit_length())
    while Q(c,1<<q)>target:q+=1
    return q


def rounded_cholesky(knum,kden,diagonal_upper,target,min_eigenvalue=Q(1)):
    """Deterministic dyadic Cholesky with per-entry residual control.

    At each completed lower-triangle entry, exact residual magnitude is
    <= 3*(diagonal_upper+1)*2^-q. Select q so its row-sum bound <= target
    and target <= min_eigenvalue/4. A partially corrected K remains PD;
    its Schur pivot is positive. This prevents a precision-dependent abort.
    All square roots are floor integer square roots of rational numbers.
    """
    n=len(knum);target=min(Q(target),Q(min_eigenvalue)/4)
    c=3*n*(Q(diagonal_upper)+1)
    q=sufficient_bits(c,target)
    sc=1<<q
    ll=[[0]*n for _ in range(n)]
    for i in range(n):
        numerator=int(knum[i][i])*sc*sc-sum(x*x for x in ll[i][:i])*kden
        assert numerator>0,'Positive pivot invariant failed'
        ll[i][i]=math.isqrt(numerator//kden)
        assert ll[i][i]>0
        for j in range(i+1,n):
            numerator=int(knum[j][i])*sc*sc-sum(ll[j][k]*ll[i][k] for k in range(i))*kden
            ll[j][i]=nearest_ratio(numerator,kden*ll[i][i])
    la=np.array(ll,dtype=object)
    pp=la@la.T
    en=np.array(knum,dtype=object)*sc*sc-pp*kden
    delta=Q(max(sum(abs(int(x)) for x in row) for row in en),kden*sc*sc)
    guaranteed=c/(1<<q)
    assert delta<=guaranteed<=target
    return la,q,delta,{'fraction_bits':q,'exact_residual_bound':delta,
        'a_priori_residual_bound':guaranteed,'required_residual_bound':target,
        'positive_pivot_invariant':True,'method':'exact rational recurrence with integer square roots and dyadic rounding'}


def sqrt_midpoint(q,tolerance):
    bits=sufficient_bits(Q(1),tolerance)
    sc=1<<bits
    lo=math.isqrt((q.numerator*sc*sc)//q.denominator)
    a,b=Q(lo,sc),Q(lo+1,sc)
    assert a*a<=q<=b*b
    return (a+b)/2,{'lower':a,'upper':b,'midpoint_error_bound':Q(1,2*sc)}


def solve_transpose(lint,lbits,rhs,round_error=None,min_eigenvalue=Q(1),diagonal_upper=Q(1)):
    n=len(rhs);sc=1<<lbits;out=[Q(0)]*n
    xbits=None if round_error is None else sufficient_bits(2*n*(diagonal_upper+1)/min(Q(1),min_eigenvalue),round_error)
    for i in range(n-1,-1,-1):
        x=(rhs[i]-sum((Q(int(lint[j,i]),sc)*out[j] for j in range(i+1,n)),Q(0)))/Q(int(lint[i,i]),sc)
        out[i]=x if xbits is None else Q(nearest_ratio(x.numerator*(1<<xbits),x.denominator),1<<xbits)
    residual=[sum((Q(int(lint[j,i]),sc)*out[j] for j in range(i,n)),Q(0))-rhs[i] for i in range(n)]
    err2=sum((x*x for x in residual),Q(0))/min_eigenvalue
    if round_error is not None:assert err2<=round_error**2
    return out,{'fraction_bits':xbits,'residual_squared':sum((x*x for x in residual),Q(0)),
                'distance_squared_upper':err2}


def rational_K(b,lam):
    ld=math.lcm(*(x.denominator for x in lam));den=D*ld
    aa=sum((a.astype(object)*int(x*ld) for a,x in zip(b,lam)),np.zeros((N,N),dtype=object))
    return aa@aa.T+np.eye(N,dtype=object)*(den*den),den*den


def exact_fiber(b,x,z):
    xd=math.lcm(*(v.denominator for v in x));xi=[int(v*xd) for v in x]
    fd=D*xd
    f=[[sum(xi[k]*int(b[i][k,j]) for k in range(N)) for j in range(N)] for i in range(M)]
    sint=[[sum(f[i][k]*f[j][k] for k in range(N)) for j in range(M)] for i in range(M)]
    s=[[Q(v,fd*fd) for v in row] for row in sint]
    det=s[0][0]*s[1][1]-s[0][1]**2
    if det<=0:return None,s,None
    fz=[sum((Q(f[i][j],fd)*z[j] for j in range(N)),Q(0)) for i in range(M)]
    c=[(s[1][1]*fz[0]-s[0][1]*fz[1])/det,(s[0][0]*fz[1]-s[0][1]*fz[0])/det]
    y=[z[j]-sum((Q(f[i][j],fd)*c[i] for i in range(M)),Q(0)) for j in range(N)]
    residual=[sum((Q(f[i][j],fd)*y[j] for j in range(N)),Q(0)) for i in range(M)]
    assert residual==[Q(0)]*M
    return y,s,{'projection_residual':residual,'projection_rounding_error':Q(0)}


def acceptance_decision(lower_squared,upper_squared,cell_index,cell_bits):
    ulo,uhi=Q(cell_index,1<<cell_bits),Q(cell_index+1,1<<cell_bits)
    if ulo*ulo>upper_squared:return 'reject'
    if uhi*uhi<lower_squared:return 'accept'
    return 'interval_overlap_fallback'


def run_sampler(epsilon=Q(1,16),seed=None,bit_source=None,raw_input=None):
    from certified_normal import CertifiedNormal
    start=time.perf_counter();timings={}
    raw_input=Path(raw_input) if raw_input is not None else HERE/'RAW_INPUT.npz'
    raw=np.load(raw_input,allow_pickle=False)
    assert int(raw['denominator'])==D, 'This prototype requires common denominator 4096'
    b=[raw['B1'],raw['B2']]
    assert all(a.shape==(N,N) and a.dtype==np.int64 for a in b), 'This prototype requires two 128 by 128 int64 numerators'
    h,r,native=acquire_certificate(b,require_noncommuting=False)
    budget=build_budget(h,N,N,r,epsilon);rho=budget['primitive_error_rho']
    rng=bit_source if bit_source is not None else secrets.SystemRandom() if seed is None else random.Random(seed)
    mode='supplied_finite_bit_tape' if bit_source is not None else 'system_random_bits' if seed is None else 'deterministic_pseudorandom_replay'
    normal=CertifiedNormal(budget['primitive_error_bits'],budget['normal_cutoff_L0'],budget['normal_uniform_bits'])
    hg=[[int(v*D*D) for v in row] for row in h]
    hl,hbits,hdelta,hproof=rounded_cholesky(hg,D*D,max(h[i][i] for i in range(M)),rho,budget['H_eigenvalue_lower'])
    transcript=[]
    result={'scope':'Finite-bit capped implementation prototype under probability_budget transport proof',
        'independent_proof_audit':False,'randomness_mode':mode,'replay_seed':seed,
        'raw_input':{'filename':raw_input.name,'sha256':hashlib.sha256(raw_input.read_bytes()).hexdigest()},
        'dimensions':{'m':M,'p':N,'n':N},'native_certificate':native,
        'budget':budget,'H_factor':hproof,'trials':transcript}
    def finish(reason,x=None,y=None):
        if x is None:x=[Q(0)]*N;y=[Q(0)]*N
        result['terminal_reason']=reason;result['output']={'x':x,'y':y,'residual_squared':Q(0),
            'norm_squared':sum((z*z for z in x+y),Q(0))}
        assert result['output']['norm_squared']<=budget['output_norm_cap']**2
        result['timings_seconds']=timings;result['total_wall_seconds']=time.perf_counter()-start
        return result
    for trial in range(budget['trial_cap']):
        tr={'trial':trial+1,'normal_certificates':[]};transcript.append(tr)
        t=time.perf_counter();seed_results=[]
        for _ in range(r+2*N):
            proof=normal.draw(rng)
            zz=None if proof['fallback'] else proof['value']
            seed_results.append((zz,proof))
            tr['normal_certificates'].append(proof)
            if zz is None:
                tr['normal_fallback']=proof
                return finish('normal_tail_cell_fallback')
        timings['normal_generation']=timings.get('normal_generation',0)+time.perf_counter()-t
        zs=[z for z,_ in seed_results]
        if any(abs(z)>2*budget['normal_cutoff_L0'] for z in zs):return finish('normal_size_fallback')
        v=sum((z*z for z in zs[M:r]),Q(0));tr['V']=v
        if v<budget['V_implementation_min']:return finish('small_V_fallback')
        root,rootproof=sqrt_midpoint(Q(r)/v,rho)
        propbase,propproof=solve_transpose(hl,hbits,zs[:M])
        qlam=sufficient_bits(Q(M),rho)
        lam=[Q(nearest_ratio((root*x).numerator*(1<<qlam),(root*x).denominator),1<<qlam) for x in propbase]
        lamerr2=sum(((a-root*c)**2 for a,c in zip(lam,propbase)),Q(0))
        assert lamerr2<=rho*rho
        tr['proposal']={'lambda':lam,'V':v,'sqrt_certificate':rootproof,
                        'lambda_rounding_error_squared':lamerr2,'solve':propproof}
        s=sum((lam[i]*h[i][j]*lam[j] for i in range(M) for j in range(M)),Q(0))
        t=time.perf_counter();kn,kd=rational_K(b,lam)
        target=min(rho,rho*rho/(16*N))
        kl,kbits,kdelta,kproof=rounded_cholesky(kn,kd,1+s,target)
        detp=Q(math.prod(int(kl[i,i]) for i in range(N)),1<<(kbits*N))**2
        acbase=(1+s/r)**r/detp
        alo,ahi=max(Q(0),acbase*(1-kdelta)**N),min(Q(1),acbase*(1+kdelta)**N)
        assert 0<=alo<=ahi<=1 and ahi-alo<=rho*rho
        ubits=budget['per_acceptance_uniform_bits'];ui=rng.getrandbits(ubits)
        ulo,uhi=Q(ui,1<<ubits),Q(ui+1,1<<ubits)
        tr['precision_factor']=kproof
        tr['acceptance']={'squared_probability_lower':alo,'squared_probability_upper':ahi,
                          'squared_probability_width':ahi-alo,'uniform_cell_index':ui,'uniform_bits':ubits}
        timings['precision_and_acceptance']=timings.get('precision_and_acceptance',0)+time.perf_counter()-t
        tr['decision']=acceptance_decision(alo,ahi,ui,ubits)
        if tr['decision']=='reject':continue
        if tr['decision']=='interval_overlap_fallback':return finish('acceptance_overlap_fallback')
        t=time.perf_counter()
        x,xproof=solve_transpose(kl,kbits,zs[r:r+N],rho,1-kdelta,1+s)
        y,sx,yproof=exact_fiber(b,x,zs[r+N:])
        margin=[[sx[i][j]-2*budget['conditioning_t']*h[i][j] for j in range(M)] for i in range(M)]
        tr['conditioning']={'S':sx,'S_minus_2tH':margin,'positive_semidefinite':is_psd(margin)}
        if y is None or not is_psd(margin):return finish('fiber_conditioning_fallback')
        tr['output_numerics']={'X_solve':xproof,'Y_projection':yproof}
        norm2=sum((z*z for z in x+y),Q(0))
        if norm2>budget['output_norm_cap']**2:return finish('output_norm_fallback')
        tr['output_norm_squared']=norm2
        timings['output_solve_projection']=time.perf_counter()-t
        return finish('accepted',x,y)
    return finish('trial_cap_fallback')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--epsilon',default='1/16')
    ap.add_argument('--seed',type=int,default=None,help='Set only for reproducible pseudorandom replay; default uses OS-backed bits')
    ap.add_argument('--input',type=Path,default=HERE/'RAW_INPUT.npz')
    ap.add_argument('--output',type=Path,default=HERE/'FINITE_BIT_DRAW.json');args=ap.parse_args()
    report=run_sampler(Q(args.epsilon),args.seed,raw_input=args.input)
    args.output.write_text(json.dumps(enc(report),indent=2)+'\n')
    summary={'terminal_reason':report['terminal_reason'],'randomness_mode':report['randomness_mode'],
        'epsilon':str(report['budget']['epsilon']),'r':report['native_certificate']['r'],
        'trial_count':len(report['trials']),'trial_cap':report['budget']['trial_cap'],
        'primitive_error_bits':report['budget']['primitive_error_bits'],
        'total_wall_seconds':report['total_wall_seconds'],'timings_seconds':report['timings_seconds'],
        'residual_squared':str(report['output']['residual_squared']),
        'output_norm_squared_approx':float(report['output']['norm_squared']),
        'claim':'Coded end-to-end prototype; W1 guarantee depends on stated transport proof and bit-source model, not empirical statistics'}
    args.output.with_name(args.output.stem+'_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
