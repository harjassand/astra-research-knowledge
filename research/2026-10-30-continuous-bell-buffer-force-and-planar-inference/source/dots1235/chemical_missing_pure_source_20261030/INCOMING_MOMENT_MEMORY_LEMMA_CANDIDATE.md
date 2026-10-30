# Incoming-moment memory across a killed fast episode
Status: new personal local derivation, not reviewed and not part of the four frozen A-catalytic global proof files.

Consider a multi-seed generalization with minimum A multiplicity a0, 1<=a0<m. Every fast complex contains at least a0 A, contains mA and a0 A+(m-a0)X_i for each reservoir, and each latter source has an A-increasing edge. Set v=m-a0>0. Work on active A>=a0 and large conserved N; normalized clearing hazard is k_D(A)_m. Optional nonnegative competitors only improve the inequalities below.

For every fixed s>0, write f_s(A)=(1+A)^-s. The same source-dominance calculation as for log A gives

    Q f_s <=-c_s A^(a0-s-1)N^v  for A<=epsilon_s N,
    |Q f_s|<=C_s N^(m-s-1)      for A>=epsilon_s N.

For the first inequality, A-producing sources give the negative term. An A-decreasing edge must have source A-degree at least a0+1, so its positive contribution is smaller by O(A/N). Falling factorials are comparable to powers for A>=a0, including the finitely many threshold values, with fixed constants.

Let g_s(A)=(1+A-m)^-s on the clearing-enabled states A>=m. Choose C1>=(m+1)^s, so g_s<=C1 f_s pointwise. Define F_s=C1 f_s+C2 N^-s. For the killed generator K=Q-k_D(A)_m,

    K F_s + k_D(A)_m g_s
       <= C1 Qf_s-C2 k_D(A)_m N^-s <=0

for sufficiently large N: in the low-A region Qf_s<=0; in the high-A region the last negative term is order N^(m-s), versus possible positive Qf_s of order N^(m-s-1). Finite-state killed Dynkin therefore yields

    E[(1+A_after)^-s ; clearing before competitors]
       <=C_s[(1+A_initial)^-s+N^-s]
       <=C'_s(1+A_initial)^-s.                         (M)

This retains incoming composition instead of replacing every output by the worst-case reset envelope. No mixing or conditional-on-observed-output bound is asserted.

There is also a useful mean bound T(A)<=C(1+A)^-m. Indeed choose F_m as above. For a0<=A<m, Qf_m is negative of order N^v, so K F_m<=-1 after multiplying by a fixed constant. For m<=A<=epsilon_m N, Qf_m<=0 and (A)_m f_m is bounded below by a positive fixed constant. For A>=epsilon_m N the killing term is order1 and any positive Qf_m is O(1/N). Thus K(CF_m)<=-1 globally for large N, and stopped Dynkin gives the claimed mean. This is an incoming-A upper bound, not a strict-power uniform-in-N mean.

Consequently fast immigration before clearing has probability <=C(1+A_initial)^-m at fixed B, while all inverse moments propagate according to (M). These estimates may control successive low-walk race factors without forgetting A after each reset. A global multi-seed theorem does NOT follow: at a0>=3 a small-A section state may have time/occupation ratio bounded away from0, and scalar section drift need not have a pointwise gap. A further composition-sensitive section potential or exact phase elimination is still required.
