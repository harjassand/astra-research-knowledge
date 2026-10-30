# Exact extensive failure of the linear credit under arbitrarily weak local data noise

This is a failure of the proposed LINEAR corrected observable, not an impossibility theorem for finite-rate controllers.

Take independent identical damped Rabi clocks and disjoint one-bit correction channels that remove an occupied bit. For a connected-animal product f_A(x)=exp(a m)theta^{m-s}, m=|A| and s occupied sites in A, define d_h=(1-theta) f_A if h is occupied, otherwise zero. Thus sum_h d_h=(1-theta)s f_A.

For an isolated clock let Y=i(sigma^- - sigma^+), L*n=gY-kappa n and L*Y=2g(1-2n)-kappa Y/2. Put
b=kappa^2/(kappa^2+8g^2), c=2g kappa/(kappa^2+8g^2),
mu=(b+sqrt(b^2+4c^2))/2,
A=mu I-b n-cY.
Then A>=0 and L*A=kappa n-r I with r=4g^2 kappa/(kappa^2+8g^2). In the ready state <A>=mu>0.

The linear corrected animal has all-ready expectation
F=f_A[1+epsilon mu(1-theta)s].
The exact clean derivative at all-ready is
L*F=-epsilon r(1-theta)s f_A.

Now add independent local data-excitation Lindblad noise at any rate gamma>0 on every site. Each empty site becomes occupied; this is standard bounded-strength local Markovian noise, not a global perturbation. With e=m-s empty sites, its exact derivative is
N*F=gamma e f_A[(theta^{-1}-1)(1+epsilon mu(1-theta)s)+epsilon mu(1-theta)/theta].
For s and e both proportional to m, clean loss is O(m f_A), while noise gain is positive O(gamma m^2 f_A). No nonzero, volume-independent gamma can be absorbed by the clean W-scale drift of this observable. The failure occurs immediately in the all-ready clock state; high reset only changes constants, not the extra factor m.

For the full path-graph animal sum, take an alternating occupied/empty configuration and c>1/2, so long intervals have exponentially increasing weights in their length. Its largest intervals dominate up to polynomial factors, and the same m versus m^2 discrepancy survives. The single-animal identity already pinpoints the exact term that any full-sum proof must cancel or resum; estimating it by O(W) is invalid.

Independent disjoint updates therefore DO NOT remove the robust-noise obstruction even though their reset/data cross terms have a favorable clean sign. A multiplicative per-animal clock credit is the natural next target because one physical local error would then change only boundedly many factors.
