# A concrete global representation tested and falsified

The bulk/strip obstruction suggests replacing sector selection by a global residual-activity norm. Let d_y be complex outgoing rate, let s_y be a positive stationary weight for the finite embedded complex chain, and test

    nu_alpha(x)=[sum_available_y s_y^(1/alpha)/(x−y)!]^alpha,
    mu_alpha(x)=nu_alpha(x)/q(x),

where q is the actual physical total rate. The division by q automatically adds the correct inverse-activity polynomial suppression on many bounded-coordinate strata. Unlike a sector partition, the selector is everywhere positive and contains no cutoff zeros. This is an actual proposed global construction, not an assumption.

It fails, even for the deficiency-zero single-linkage cycle

    0 --1--> A+B --2-->2A+3B --3-->0.

The embedded complex chain is a directed cycle, so take s_y=1 for all three vertices (normalization is irrelevant). At x=(n,1),

    nu(x)=(n+1)^alpha/(n!)^alpha,
    q(x)=1+2n.

Incoming0→A+B from(n−1,0) contributes n^alpha/(n!)^alpha. The other possible incoming reaction is2A+3B→0 from(n+2,4). Its incoming flux equals

    (n!)^(−alpha) R_n [1+1/(6(n+1))+1/(24(n+1)(n+2))]^alpha,

where

    R_n=72(n+2)(n+1)/[72(n+2)(n+1)+8(n+2)+1]→1.

Therefore

    (n!)^alpha (L*mu_alpha)(n,1)
      =n^alpha−(n+1)^alpha
       +R_n[1+1/(6(n+1))+1/(24(n+1)(n+2))]^alpha
      →1

for every fixed0<alpha<1. Hence the adjoint is positive on an infinite boundary sequence. These states lie in the communicating class of0 for every n≥1. From0, fire0→A+B exactly3n−2 times, then2A+3B→0 exactlyn−1 times to reach(n,1). Conversely, fireA+B→2A+3B exactly3n−2 times, then2A+3B→0 exactly2n−1 times to return to0. Every stated firing is enabled.

The network is complex balanced at c_A=3/8,c_B=4/3, so this is emphatically not a recurrence counterexample. It shows that matching leading maximal-source/fast-cycle balance is insufficient: the next incoming residual layer has a positive constant contribution that survives after the leading n^alpha terms cancel. Exact phase-resolvent corrections, not merely a positive algebraic softmax of residual factorials, are needed.

Scripts test_residual_power.py and test_residual_softmax.py were used only to locate the failure; the displayed limit is the proof. Earlier finite positive defects were not promoted to asymptotic claims without this derivation.
