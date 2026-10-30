# Gain compensation at first-motion regularity

The arbitrary-accuracy unknown-gain question remains **UNRESOLVED** in
this continuation. I established two quantitative barriers and a finite
coarse-accuracy construction, with their precise scopes below.

The completed ten-segment construction extends to gains in [1,2]^3,
with a uniform one-cycle full-diamond bound 50000 delta^4 for delta<=0.01.
Its clean data angle is 4 delta^3 h, h=g_A g_B g_C. Static gain uncertainty
therefore survives as an unknown logical amplitude, even though moving
memory and initial correlations are handled correctly.

Any program assembled only from completed, gain-blind phases
exp(-i alpha h F), their inverses, products and arbitrary classical
mixtures has a **worst-case full-diamond error of at least
0.583910227452** against the requested pi/4 gate. This includes arbitrary
probability distributions of the total signed phase, not just bounded
word counts. The proof uses positivity of a 9x9 moment Toeplitz matrix at
the admitted gain products h=1,...,8. A vanishing compilation residual
cannot remove this constant obstruction. This is not a theorem about all
native programs.

I also constructed an admitted, coin-independent moving bath for every
fixed balanced flat word whose frozen coefficients vanish through degree
two. Its normalized first-order control primitive has positive area c_A.
The bath is H_delta(t)=sign(F_A(t/delta)) sigma_z/2, meets every supplied
local-motion bound, and produces reduced-channel error at least
c_A^2 delta^4 at explicitly bounded small scales. Thus fixed higher-order
words cannot receive a uniform o(delta^4) per-cycle remainder merely by
importing the predecessor's stronger regularity argument. In particular,
an exact 46-segment degree-five word has leading pure-control term
16 i g_A^3 g_B g_C delta^5 F but c_A=65. Its first four frozen
coefficients vanish; the quartic moving-bath noise remains. A per-cycle
lower bound is not silently accumulated into an all-policy impossibility.

There is a concrete finite construction within the restricted phase
interface: a capped geometric distribution of logical phases followed by
the gain-uniform cubic implementation. For every eta>0 it has full-diamond
error at most sqrt(5554/7969)+eta, approximately 0.834836+eta, uniformly
over the original bath class and all DMR inputs. This substantial error
ceiling is coarse progress, not a usable high-fidelity gate. The lazy
generator reports actual duration, switches, coins and timing precision;
the enormous counts carry no efficiency claim.

Files:

- `PROOF.md`: gain-uniform primitive estimate, phase-positivity lower
  bound, explicit coarse construction and moving-bath quartic witness.
- `phase_schedule.py`: finite capped-geometric sampler and lazy legal
  native schedule, with exact rational resource bounds.
- `checks.py`: standard-library exact Pauli/gain-polynomial checks for
  the 10- and 46-segment words, primitive-area checks and independent
  moment-witness diagnostics.
- `noise_diagnostic.py`: an 8x8 check of the analytic quartic
  entanglement-infidelity coefficient. At unit gains the prediction is
  4421 for the degree-five word; the ratio is 4419.88 at delta=0.00125.
- `checks.txt` and `resources_example.txt`: executed outputs.

For eta=0.01 the explicit coarse construction uses at most
2.7708e24 native segments, duration 4.1288e16 and 175 absolute binary
timing places. Those resources approximate a gate with error ceiling
about 0.835; they illustrate an existence construction, not practical
performance.

The exact checks and analytic inequalities carry their stated mathematical
scope. There is no independent audit, hardware validation, efficiency or
priority claim. Polynomial gain compensation and native sign projection
were already present in the supplied predecessor originals.

The remaining scientific target is a native policy outside the completed
phase-only interface with a uniform first-motion channel analysis, or an
all-policy lower bound covering such policies. Neither has been acquired
here.
