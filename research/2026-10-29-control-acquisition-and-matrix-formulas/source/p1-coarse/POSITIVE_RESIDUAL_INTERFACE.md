# A residual flag is a stronger experimental operation

28 October 2026. This follows the precision failure in `THEORY.md`.

## 1. Conditional construction with coherent block encodings

Suppose, additionally, every primitive has an actually available coherently
controlled unitary block encoding with normalization one, its required
inverse operations, coherent reset preparation, and compatible ancillas.
These are stronger capabilities than scalar echoes or applying a
nonselective Lüders channel. They are not inferred from our data.

For a known dictionary coefficient vector x and map T_i, write

    D_i x = sum_j x_j A_i A_(w_j)b - sum_j (T_i x)_j A_(w_j)b.

Let C=||x||_1+||T_i x||_1. Prepare the LCU label amplitudes with weights
sqrt(|coefficient|/C), apply the signed selected word block encodings,
unprepare the label and inspect the shared success flags. The success
probability is exactly

    p = ||D_i x||^2 / C^2,

assuming ||b||=1; otherwise its normalization is also charged. A literal
SELECT implementation uses at most 2r(L+1) coherently controlled primitive
calls per trial for r dictionary words of maximum length L. Word products
use their own flag ancillas. State preparation, gates, ancillas, precision,
coherence and any unsuccessful attempts remain paid.

If no successes occur in N independent trials, the rule

    ||D_i x||^2 <= C^2 log(1/delta)/N

is a sound one-sided confidence certificate: if the inequality is false,
the zero-success probability is <=exp(-Np)<delta. This is a conditional
certificate, not a promise that the zero-success event will occur.

If W^-1=sum_k z_k z_k*, select k with probability C_k^2/S, where
C_k=||z_k||_1+||T_i z_k||_1 and S=sum_k C_k^2. The resulting success
probability is tr(W^-1 E_i)/S. Since E_i>=0, an upper bound on this trace
implies E_i<=epsilon^2 W. The normalization S, factor preparation and
coefficient precision are not free.

This is ordinary LCU combined with positive-event statistics, applied to
the learned source defect. With further coherent inverse/reflection access,
standard amplitude estimation is a stronger comparator. The eps^-2 trial
dependence is not a new optimal quantum-query claim.

## 2. Why the operation is unavailable in the present scalar interface

An applied Lüders channel maps density matrices and discards outcome/environment
records. It does not expose a block encoding of its Liouville operator on
vectorized states, signed coherent superpositions of histories, controlled
SELECT, or the required inverse. A matched passive port also does not
automatically supply any of those. The improved precision dependence above
therefore cannot be credited to the executed echo compiler.

There is a stronger obstruction to obtaining an *exact* positive residual
flag by ordinary classical postprocessing alone.

**Theorem (finite-transcript support obstruction).** Consider two sources
P_0,P_1. Assume every finite adaptive observation transcript has mutually
absolutely continuous laws under the two sources, including the same
independent internal randomness. Then no almost-surely terminating
algorithm using only these observations can output a nonnegative variable
Z with E_0 Z=0 and E_1 Z>0. In particular it cannot simulate a Bernoulli
flag whose probability is zero for one source and positive for the other.

**Proof.** Nonnegativity and E_0 Z=0 imply Z=0 almost surely under P_0.
For every integer n and k, the event {the algorithm has stopped by n,
Z>1/k} belongs to a finite transcript sigma-algebra and has P_0 measure
zero. Absolute continuity gives P_1 measure zero. Their countable union
contains {Z>0, stopping time finite}. Almost-sure termination under P_1
implies Z=0 there as well, a contradiction. QED.

**Concrete application.** Use the two positive contractions A_e,B_e from
`THEORY.md`, dictionary V=[b], and T=1-e. The defect norm squared is e^2
for A_e and zero for B_e. Give the receiver one independent binary sample
with mean q_k=1/4+f(k)/2 per chosen finite-length word. Both sources have
q_k in [1/4,3/4] for every k. Even an adaptive algorithm choosing arbitrarily
long finite words has mutually absolutely continuous finite transcript
laws. It cannot manufacture the exact positive defect flag above.

This is an application of the established Bernoulli-factory/support
obstruction, not a new general impossibility principle. It does not forbid
confidence intervals with nonzero failure probability, approximate flags,
signed unbiased estimators, or long direct experiments. Those remain
usable alternatives with their own costs. It explains why a genuine
interference/null detector would add access, rather than merely reformat
old scalar readings.

## 3. Scientific consequence

The precision bottleneck cannot be removed by declaring squared residuals
to be directly observed. One must either build and pay for a stronger
physical operation, accumulate sensitivity through sufficiently long
experiments, exploit stronger source structure, or accept a weaker
task certificate. The current scalar-word construction has not solved
that choice for broad real systems.

Primary context: Gilyén et al., QSVT/LCU,
https://arxiv.org/abs/1806.01838 ; Keane and O'Brien, Bernoulli factories
(1994); Nacu and Peres, *Fast simulation of new coins from old* (2005);
Jacob and Thiéry, *On nonnegative unbiased estimators*. The complete proof
of the exact support claim needed here is given above.
