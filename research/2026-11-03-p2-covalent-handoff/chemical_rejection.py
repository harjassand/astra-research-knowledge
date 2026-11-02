#!/usr/bin/env python3
"""CBT source-rate and chemical-damage frontier. Stdlib only.
CBT k2=9.19 M^-1s^-1 is a published free N-terminal cysteine assay rate;
its transfer to a peptide loom is not established. Other rates illustrative.
"""
from math import log,exp
def frontier(M,r=.01,eps_wrong=.005,eps_damage=.005,
             CBT_M=1e-3,k2=9.19,k_correct=0.):
    assert M>=2 and not M&(M-1)
    J=M-1; L=M.bit_length()-1
    k_wrong=k2*CBT_M
    assert k_wrong>k_correct
    t=log(J*r/eps_wrong)/(k_wrong-k_correct)
    Bserial=M*(M-1)//2;Btree=M*L-(M-1)
    crit_s=-log(1-eps_damage)/(t*Bserial)
    crit_t=-log(1-eps_damage)/(t*Btree)
    out={"fragments":M,"joins":J,"depth":L,"target_capture_rate":k_wrong,
         "t_challenge_s":t,"ideal_CBT_parallel_wall_h":t*L/3600,
         "serial_exposures":Bserial,"tree_exposures":Btree,
         "k_correct_max_serial":crit_s,"k_correct_max_tree":crit_t,
         "minimum_discrimination_ratio_tree":k_wrong/crit_t,
         "model_tree_retention_kcorrect_1e-8":exp(-1e-8*t*Btree),
         "model_serial_retention_kcorrect_1e-8":exp(-1e-8*t*Bserial)}
    assert abs(J*r*exp(-(k_wrong-k_correct)*t)-eps_wrong)<1e-12
    return out
if __name__=="__main__":
    for n in (16,32,64,128,1024):
        print("FRAGMENTS",n,frontier(n))
