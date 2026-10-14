"""Exact information-boundary examples for cubic clocks and prep controls."""
from fractions import Fraction as F
from itertools import combinations
import json
import independent_check as c

# Four-bit reversible heat-bath model: target bit 0, three strongly occupied
# context bits, and deliberately slow but degree-zero context clocks on 1..3.
old=(c.FIELDS,c.EDGES,c.KAPPA,c.CLOCK_COEFFS)
c.FIELDS=(F(1),F(10**6),F(10**6),F(10**6))
c.EDGES={}
c.KAPPA=F(1)
c.CLOCK_COEFFS={0:{():F(1)},1:{():F(1,10**6)},2:{():F(1,10**6)},3:{():F(1,10**6)}}
P=c.p0_vector()
def eq_mean(cubic):
    L=c.full_generator(cubic=cubic)
    u=c.solve(L,[F(1)]*len(c.STATES))
    return c.inner(P,[F(1)]*len(P),u)
base=eq_mean(F(0)); eps=F(1,10**15); cubic=F(1)-eps; hidden=eq_mean(cubic)
queries=[()] + [(j,) for j in (1,2,3)] + list(combinations((1,2,3),2))
unchanged=all(c.attempt(0,sum(1<<j for j in S))==c.attempt(0,sum(1<<j for j in S),cubic=cubic) for S in queries)
assert unchanged and hidden>base
cubic_result={'n':4,'fields':[str(x) for x in c.FIELDS],'target':0,'reaction_kappa':'1','other_clock':'1/1000000',
 'degree3_coefficient':str(-cubic),'hidden_context_attempt':'1/1000000000000000',
 'degree0_1_2_context_queries':len(queries),'all_those_clock_readings_unchanged':unchanged,
 'energy_law_same':True,'baseline_mean':str(base),'hidden_clock_mean':str(hidden),
 'mean_ratio_exact':str(hidden/base),'mean_ratio_float':float(hidden/base),
 'status':'exact finite countermodel; cubic law is outside the acquired degree<=2 premise'}

# One-coordinate detailed-balance law with W(1)/W(0)=3/2 and a reaction
# hazard at state 1. The preparation operation can double the microscopic
# clock in one physical model, making it observationally identical to a model
# whose free clock is itself twice as fast.
def one_bit_mean(attempt):
    r=F(3,2); W=[F(1),r]; q01=attempt*r/(1+r); q10=attempt/(1+r); k=F(1)
    L=[[q01,-q01],[-q10,q10+k]]
    u=c.solve(L,[F(1),F(1)])
    # Equilibrium weights normalized from W.
    p=[x/sum(W) for x in W]
    return c.inner(p,[F(1),F(1)],u)
# Free law 1, prep multiplies clock by 2; second free law 2, prep factor 1.
a_free_1=F(1); prep_factor_1=F(2); a_free_2=F(2); prep_factor_2=F(1)
r=F(3,2); downhill=lambda a: a*max(F(1),r)/(1+r)
obs1=downhill(a_free_1*prep_factor_1);obs2=downhill(a_free_2*prep_factor_2)
assert obs1==obs2
prep_result={'energy_ratio':'3/2','reaction_kappa':'1','model_1':{'free_attempt':str(a_free_1),'prep_factor':str(prep_factor_1),'prepared_downhill_rate':str(obs1),'free_equilibrium_mean':str(one_bit_mean(a_free_1))},
 'model_2':{'free_attempt':str(a_free_2),'prep_factor':str(prep_factor_2),'prepared_downhill_rate':str(obs2),'free_equilibrium_mean':str(one_bit_mean(a_free_2))},
 'prepared_observations_equal':True,'free_mean_ratio':str(one_bit_mean(a_free_1)/one_bit_mean(a_free_2)),
 'status':'exact control-dependence countermodel; the source avoids it only by assuming preparation/readout preserves the original conditional clock'}

(c.FIELDS,c.EDGES,c.KAPPA,c.CLOCK_COEFFS)=old
print(json.dumps({'cubic_hidden_clock':cubic_result,'preparation_clock_invariance':prep_result},indent=2))
