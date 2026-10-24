# Why the new physical block theorem cannot be extended by free pinching

24 October 2026, root construction; independent check requested. This is a counterexample to a proof mechanism, not to the conjectured entropy bound.

Let A=C2 direct-sum C and R=C2. Use the unnormalized faithful baseline

 sigma_epsilon=(Phi2+epsilon I4) direct-sum epsilon I2,

where Phi2 projects onto (|00>+|11>)/sqrt2 in the first physical plane. Normalize by Z=1+6epsilon when using density states. Let X=|Phi2_vector><0| and H have only off-diagonal physical-plane/third-level blocks X and X*. Thus Tr_A H=0 and physical pinching Delta(H)=0.

The input BKM metric is exactly

 g_sigma(H)=2 ln[(1+epsilon)/epsilon].

At the output, the baseline has top block Phi2_J/2+epsilon I4 and bottom block (1/4+epsilon)I2. The transposed off-diagonal tangent has squared norm1/4, of which one quarter lies in the Phi2_J top eigenspace and three quarters lie in its orthogonal complement. Consequently

 g_Nsigma(NH)=(1/2)ln[(1/2+epsilon)/(1/4+epsilon)]
                  +(3/2)ln[(1/4+epsilon)/epsilon].

The ratio tends to3/4 as epsilon decreases to zero. At the exact rational epsilon=1/100 it is already strictly above1/2. The adjacent interval certificate verifies this without extrapolation. Normalizing sigma multiplies both metrics by the same Z and does not change their ratio. Multiplying H bysqrt2 makes all its entries rational if desired.

For sufficiently small nonzero t, rho=sigma/Z+tH is a faithful state with the same reference marginal, and Delta(rho)=sigma/Z. The local BKM ratio implies

 2D(Nrho||NDelta(rho))−D(rho||Delta(rho))>0.

This is exactly F(rho)−F(Delta(rho))>0. Therefore adding physical cross-sector coherence can increase the target objective; pinching is not a monotone route from arbitrary states to the proved2⊕1 block class. A global half-contraction of this pinching coherence is false.

The block baseline itself has a finite safety margin. This construction does not show that the increase overcomes that margin, and no violation of F<=−ln3 is asserted. A successful global proof must account for both the block margin and the coherence gain rather than discarding either.

## Stronger version: BOTH marginals exactly uniform

The failure is not repaired by imposing the actual uniform physical marginal. On A=R=C3, put

 sigma_e=(1−e)[(2/3)Phi2+(1/3)|22><22|]+e I9/9,
 H=|Phi2_vector><22|+|22><Phi2_vector|.

Here Phi2 is embedded in levels0,1 of both factors. Both marginals of sigma_e are I3/3, and BOTH partial traces of H vanish. Physical2⊕1 pinching kills H. For0<e<1 the baseline is faithful. The exact metrics are

 g_sigma(H)=6/(1−e) ln[(6−5e)/(3−2e)],
 g_Nsigma(NH)=9/(3−e).

The output tangent connects two disjoint pairs of baseline eigenvectors, all with eigenvalue(3−e)/18; its squared Hilbert–Schmidt norm is1/2. Thus the ratio tends to1/(2ln2)>1/2 and remains strictly above1/2 at e=1/100 by the appended interval calculation.

This construction stays inside the actual uniform-input comparison, not a different operating point. At zero regularization, completing its coherence produces the maximally entangled qutrit state and reaches the known equality boundary. The gain therefore illustrates how a finite block margin can be consumed, not an established violation beyond that margin.
