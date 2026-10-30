# A bounded-speed raw-latch ingress has an irreducible error floor
30 October 2026. Root elementary lower bound. No historical novelty claim. This strengthens the explicit pre-copy waiting example by allowing copying and noise simultaneously.

## Contract
A uniformly random bit m is initially supplied ONLY in one physical latch B: rho_m(0)=|m><m|_B tensor sigma_C. All available targets, controllers and other systems C initially have the same state for both m. There is no external noiseless m-dependent controller or additional correlated source. The processor may use arbitrary time-dependent CPTP dynamics, extra ancillas, intermediate operations and final decoding, subject to the following finite ingress constraint.

Split its generator before an imposed noise event as L_B(t)+L_C(t)+L_int(t). The first two do not transmit information from B to C. The incident coupling has induced trace norm at most J on Hermitian operators, uniformly in time. For Hamiltonian incident terms, J may be chosen as twice the sum of their operator norms. A bounded incident sum, rather than bounded degree alone with unbounded gate strengths, is necessary. All systems eventually available to the decoder are included in B,C; an inaccessible reset reservoir is not.

Allow the adversary just one ordinary local noise channel on B, at rate lambda>0:

 L_reset(rho)=lambda[(I_B/2) tensor Tr_B rho-rho].

This is a local CPTP replacement generator with completely bounded trace norm at most2lambda. It belongs to any admitted local-noise class containing onsite resets of sufficiently small rate. Taking lambda=eta/2 fits a norm budget eta. The reservoir carrying away the erased distinction is never returned to the processor. All other adversarial noise can be zero.

## Information cannot leave the raw latch instantly
Let rho_m^0(t) be the normalized process conditioned on no replacement yet. The replacement clock has state-independent rate, so this is exactly evolution under the intended generator. Set Delta_C(t)=Tr_B(rho_0^0(t)-rho_1^0(t)). Initially it is zero. The B-only generator disappears under partial trace and the C-only channel is trace-norm contractive. Variation of constants and contractivity of the full intended CPTP evolution give

 (1/2)||Delta_C(t)||_1
 <=(1/2) integral_0^t ||L_int(u)(rho_0^0(u)-rho_1^0(u))||_1 du
 <=Jt.

This bound does not presume classical trajectories, uncorrelated targets after time zero, or a particular copy circuit.

At a first replacement at time s the resulting pair of accessible states is (I_B/2) tensor rho_m,C^0(s). Its trace distance is at most min(1,Js). All subsequent processing, including further noisy or noiseless correction and arbitrary growth of the memory, is a channel. It cannot increase this distinction. The final optimal discrimination error conditional on that first replacement is therefore at least (1-Js)/2 for Js<=1.

To make the bound especially conservative, GIVE the decoder the first replacement time as an extra classical flag. That flag is independent of m. Conditional decoding can only improve performance; hence any lower bound with this flag also holds without it. For a total operation duration T and any tau<=min(T,1/J), first replacement density lambda exp(-lambda s) gives

 error >= (1/2) integral_0^tau lambda exp(-lambda s)(1-Js) ds.       (1)

Other histories contribute a nonnegative error and can be discarded in this lower bound. Choose tau=min(T,1/(2J)) for J>0:

 error >= [1-exp(-lambda tau)]/4.                                 (2)

For T>=1/(2J) and weak lambda/J this is a strictly positive floor of order lambda/J, independent of final storage size. If J=0, no information ever leaves B and any tau<=T gives the stronger (1-exp(-lambda tau))/2. Equation (1), rather than a Taylor approximation, is the asserted bound.

## Meaning and limits
Concurrent copying does not remove this particular bounded-ingress limitation. Later redundancy can suppress retention failure but cannot reconstruct a source distinction erased before it reached the available targets. The current capture theorem should therefore retain a small seed/acquisition parameter; final block size need not and, under this contract, cannot drive every raw-bit error to zero at fixed incident strength and local noise.

This is a worst-case-noise result, not a statement that every noise channel creates the floor. It does not apply to redundantly furnished inputs, initially m-dependent DATA or controllers, instantaneous ideal external readout/reporting, unbounded incident coupling, or access to the reset reservoir. A true measurement outcome may already have correlated quantum DATA; the bound applies to the explicitly stated product-input subcase, not to all such sources. It does not obstruct a downstream code that tolerates a fixed small local seed-error rate. It also supplies no many-record local-stochastic lower law: shared-noise correlations are a separate issue.
