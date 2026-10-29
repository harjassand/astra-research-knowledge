"""All-phase barrier constants plus a matched positive conditional baseline.

The zero-hopping DP is an ordinary diagonal-model alternative, not a newly
claimed solution of frustrated quantum hopping. All truncation is bounded;
there is no uncharged local occupation cap or sampled thermal-state oracle.
"""
from collections import defaultdict
from fractions import Fraction as F
from math import comb, factorial, isqrt
from pathlib import Path
import json,sys,time
import mpmath as mp

sys.set_int_max_str_digits(0)
HERE=Path(__file__).resolve().parent
mp.mp.dps=80


def rec(q):return {'numerator':str(q.numerator),'denominator':str(q.denominator)}
def display(q,digits=35):return mp.nstr(mp.mpf(q.numerator)/q.denominator,digits)


def exp4_bounds(N=80):
    lo=sum((F(4)**j/factorial(j) for j in range(N+1)),F(0))
    nxt=F(4)**(N+1)/factorial(N+1)
    hi=lo+nxt/(1-F(4,N+2))
    assert lo>50
    return 1/hi,1/lo


def constants():
    start=time.perf_counter();r=32;d=comb(63,32)
    assert d*d*100**r>1323**r
    assert F(1600,1323)**64>4*(2*64+1)**2
    assert F(1600,1323)>F(131,129)**2
    e3lo=sum((F(3)**j/factorial(j) for j in range(9)),F(0))
    assert e3lo>20
    qlo,qhi=exp4_bounds()
    assert 1+2*qhi/(1-qhi**3)<F(21,20)
    assert F(5,3)**4<8
    rows=[]
    for M in (64,128,256):
        ratio=F(5,4)**M/(2*M+1)-2*F(8,25)**M
        variance=ratio-1
        n=variance*100
        rows.append({'M':M,'K_each':M,'optimal_rejection_expected_proposals_lower':rec(ratio),
                     'relative_variance_lower_display':display(variance),
                     'direct_sample_count_for_relative_RMSE_one_tenth_lower':-(-n.numerator//n.denominator),
                     'absolute_moment_budget':'2^(-10M)','required_moment_bits':10*M})
    return {'D32':d,'integer_margin_ratio':rec(F(d*d*100**32,1323**32)),
            'general_R64_start_ratio':rec(F(1600,1323)**64/(4*129**2)),
            'general_R_induction_ratio_margin':rec(F(1600,1323)-F(131,129)**2),
            'e3_exact_lower':rec(e3lo),'q_exp_minus_four_lower':rec(qlo),'q_exp_minus_four_upper':rec(qhi),
            'compiled_costs':rows,'seconds':time.perf_counter()-start,
            'scope':'Exact integer/Fraction constants for the all-size proof; no finite diagnostic is a premise of its quantifiers.'}


def positive_difference_DP(M=64,K=64,tolerance=F(1,10**12)):
    start=time.perf_counter();qlo,qhi=exp4_bounds();D=comb(K+M-1,K)
    energy_cut=0
    while D*qhi**(energy_cut+1)>tolerance:energy_cut+=1
    # difference vector d=alpha-beta: track positive mass, negative mass, energy.
    states={(0,0,0):1};updates=0;maximum_states=1
    possible=range(1,isqrt(energy_cut)+1)
    for site in range(M):
        nxt=dict(states)  # d_site=0
        for (p,n,e),count in states.items():
            for d in possible:
                ep=e+d*d
                if ep>energy_cut:break
                if p+d<=K:
                    key=p+d,n,ep;nxt[key]=nxt.get(key,0)+count;updates+=1
                if n+d<=K:
                    key=p,n+d,ep;nxt[key]=nxt.get(key,0)+count;updates+=1
        states=nxt;maximum_states=max(maximum_states,len(states))
    coeff=[0]*(energy_cut+1);masscoeff=[0]*(energy_cut+1)
    for (p,n,e),count in states.items():
        if p!=n:continue
        ways=count*comb(K-p+M-1,M-1)
        coeff[e]+=ways;masscoeff[e]+=p*ways
    assert coeff[0]==D
    def polynomial(c,q):
        out=F(0)
        for a in reversed(c):out=out*q+a
        return out
    zlo=polynomial(coeff,qlo);ztrunc_hi=polynomial(coeff,qhi)
    tail=D*D*qhi**(energy_cut+1);zhi=ztrunc_hi+tail
    assert (zhi-zlo)/zlo<tolerance*2
    energy_coeff=[e*a for e,a in enumerate(coeff)]
    energy_lo=polynomial(energy_coeff,qlo)/zhi
    energy_hi=(polynomial(energy_coeff,qhi)+2*K*K*tail)/zlo
    mass_lo=polynomial(masscoeff,qlo)/zhi
    mass_hi=(polynomial(masscoeff,qhi)+K*tail)/zlo
    out={
        'M':M,'K_each_flavor':K,'beta_U':4,'hopping':0,
        'one_flavor_state_count':str(D),'full_sector_state_count':str(D*D),
        'energy_cut':energy_cut,'local_occupation_cap':None,
        'max_DP_states':maximum_states,'integer_updates':updates,
        'max_count_bits':max(x.bit_length() for x in states.values()),
        'energy_coefficients':list(map(str,coeff)),
        'partition_lower':rec(zlo),'partition_upper':rec(zhi),
        'partition_relative_width_upper':rec((zhi-zlo)/zlo),
        'partition_log_display':mp.nstr(mp.log(mp.mpf(zlo.numerator)/zlo.denominator),40),
        'mean_squared_density_difference_lower':rec(energy_lo),
        'mean_squared_density_difference_upper':rec(energy_hi),
        'mean_squared_density_difference_per_site_display':display(energy_lo/M),
        'mean_positive_difference_mass_lower':rec(mass_lo),
        'mean_positive_difference_mass_upper':rec(mass_hi),
        'tail_partition_bound':rec(tail),'relative_tail_vs_ground_bound':rec(D*qhi**(energy_cut+1)),
        'target_relative_tolerance':str(tolerance),
        'seconds':time.perf_counter()-start,
        'scope':'Ordinary positive conditional/occupation calculation for the SAME diagonal t4,K=M model, with exact integer counts and rational exponential/tail bounds. No full Fock state, phase MC, artificial occupation cap, or hopping prediction.'}
    return out


def main():
    start=time.perf_counter();c=constants();d=positive_difference_DP()
    (HERE/'BOUND_CONSTANTS.json').write_text(json.dumps(c,indent=2)+'\n')
    (HERE/'CONDITIONAL_EXECUTION.json').write_text(json.dumps(d,indent=2)+'\n')
    summary={'bound_seconds':c['seconds'],'conditional_seconds':d['seconds'],
             'wall_seconds_after_imports':time.perf_counter()-start,
             'energy_cut':d['energy_cut'],'max_DP_states':d['max_DP_states'],
             'integer_updates':d['integer_updates'],'log_partition_display':d['partition_log_display'],
             'density_difference_per_site_display':d['mean_squared_density_difference_per_site_display'],
             'relative_interval_width_display':display(F(int(d['partition_relative_width_upper']['numerator']),int(d['partition_relative_width_upper']['denominator']))),
             'barrier_sample_count_M64':c['compiled_costs'][0]['direct_sample_count_for_relative_RMSE_one_tenth_lower'],
             'scope':'Matched diagonal ordinary comparator; no generic simulation advantage. All-M phase obstruction is the analytic proof.'}
    (HERE/'EXECUTION_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
