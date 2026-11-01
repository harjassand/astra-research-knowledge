ASTRA: ACQUIRED RARE LIFETIMES IN DRIVEN STOCHASTIC NETWORKS
Research developed 1 November 2026 (Australia/Brisbane)

Strongest result
=================
We derived and executed a finite-confidence method for rare coarse-target
mean hitting times and additive deadline probabilities in a specified family
of nonreversible Markov systems. The strongest executed variant learns an
unknown interacting Gibbs law on a binary path from local marked calibration,
computes a rare cylinder's mass and conditional initial states, and performs
short recrossing simulations. No rare collective hit is needed during its
source calibration. Every statistical, structural and computational interface
is specified in the proofs.

The central mathematical composition is:
  acquired errors in weights and stationary circulation
    -> simultaneous rare-target mean robustness
    -> finite nonreversible exponential-killing receiver
    -> a uniform additive lifetime-law certificate.

At fixed weights, bounded local cycle geometry controls the effect of rate
errors without multiplying them by the enormous target mean. With unknown
weights, the corresponding theorem is
   |log(Mhat_A/M_A)| <= 3u+K v,
where u bounds pointwise unnormalized log-weight error, v bounds log error
in each positive stationary cycle flow, and K=csc(pi/ell) for maximum cycle
length ell. It is simultaneous in every target A and does not need a gap.
A separately earned symmetric-part gap g controls computational screening:
   R_s/[b(1+s/g)] <= M_A <= (1+s/g)R_s/b,
   R_s=1/(p r_s)-1/s,
   r_s=s+E_(pi|A) sum_(y outside A) q_xy P_y(Exp(s)<tau_A).
That boundary quantity is acquired by a positive short simulation.

These are mathematical constructions with numerical executions, not a
physically calibrated reliability product. Established potential theory,
Poisson clumping, inverse-Ising calibration, transfer matrices, concentration
and uniformization provide much of the method. Precise historical originality,
superiority to the strongest equally informed implementation, and a new broad
feasibility class have not been established. The comparisons preserve this
finding rather than claiming an exponential advantage over existing methods.

Read in this order
===================
1. main/MAIN_PROOF.txt: source contract, ordinary comparators, nonreversible
   finite screening theorem, common-law rate robustness, positive receiver,
   all paid costs, and the 64-bit execution.
2. main/UNKNOWN_GIBBS_PROOF.txt: strengthened weights/flows theorem and an
   end-to-end local acquisition construction for an unknown stationary law.
   Includes the 80-bit execution and its physical-interface limitations.
3. main/LIFETIME_LAW.txt: complex-potential proof of the complete additive
   deadline envelope, independent of reversibility.
4. main/SOURCES_AND_COMPARISONS.txt: pinned Astra ingredients, ordinary
   predecessors, what changed, and what novelty remains unestablished.
5. main/RESULTS_AND_LIMITATIONS.txt: consolidated numbers, failure examples,
   cost distinctions and unclosed physical obligations.

Independent mathematical reconstructions and executable audits are in
control/rare_audit, computation, and physics. They are complementary checks
inside this research effort, not external peer review. Ordinary proofs supply
the theorems; numerical fixtures diagnose implementations and false extensions.

Executed results
=================
A. Known uniform invariant law, unknown primitive rates
  64 bits, 2^64 states, 127 local permutation-clock primitives.
  Three targets each fix 48 bits and leave 16 free; p=2^-48 exactly.
  25389896 synthetic calibration marks over 200000 model-time units.
  30000 boundary trials per target, screen s=0.07454, fitted gap>=1.4908.
  Expected excursion duration <=13.4156157768 time units.
  126339512 excursion categories +90000 initial boundary proposals.
  Joint ideal-sampling confidence >=0.998527301001297196.

  True mean intervals:
    contiguous_48: [2730187267329.94532, 3233413517204.21966]
    distributed_48:[3156125098750.55129, 3767886732624.58410]
    alternating_48:[3603611131741.37055, 4301773523846.95458]

  At deadline 10^12, true hit-probability intervals:
    contiguous_48: [0.266017931669702306,0.306688053201699761]
    distributed_48:[0.233101453283862398,0.271555777894074667]
    alternating_48:[0.207420340015854170,0.242323996262942797]

  The first and third means are distinguishable despite identical stationary
  rarity. The deadline envelopes are likewise disjoint. This tests kinetic
  information beyond stationary mass. It is not a physical reliability claim.

B. Unknown interacting Gibbs law and driven cycles
  80 bits, 2^80 states, 80 site factors,79 pair factors,79 cycle coefficients.
  397 local synthetic Poisson-count exposures, each of duration16000000000.
  Sequential acquisition exposure:6352000000000 model-time units.
  Recorded selected positive-transition counts:3395200038575.
  Expected selected-channel attempts:7616000000000.
  Expected whole-device attempts if background clocks remain live:
     1511776000000000.
  Clamp/reset/holding/readout work is a separate physical-control resource.
  Aggregate software generation of counts does not remove any acquisition cost.

  Two targets each fix64 bits and leave16 free; their masses are acquired.
  40000 boundary trials per target; screen s=1/40; true and fitted gap>=1/2.
  Expected excursion duration<=40;255204742 excursion categories plus80000
  initial boundary proposals;1280000 exact conditional free-bit draws total.
  Joint ideal-sampling confidence>=0.998643047653664544.

  Acquired true target-mass intervals:
    contiguous_64: [4.90160629446340669e-20,6.00565790159636414e-20]
    alternating_64:[5.85300334600195084e-20,7.17135030463205996e-20]
  True mean intervals:
    contiguous_64: [184296830911796719,334329003633724406]
    alternating_64:[214402305191922311,397144932468048295]
  At deadline10^17, true hit-probability intervals:
    contiguous_64: [0.258519610950583684,0.418766626720007761]
    alternating_64:[0.222597655968665833,0.372751757502539058]

In both experiments, means start from the TRUE stationary law conditioned
outside the target. The receiver initializes its simulations under its FITTED
conditional law; the sensitivity theorem transfers the result between laws.
The 80-bit deadline proof propagates uncertainty in target mass as well.

Proof, probability and arithmetic distinctions
==============================================
All final interval endpoints use exact rational arithmetic and outward decimal
rounding. Exponential confidence allowances and deadline CDF endpoints use
positive Taylor sums with justified remainders. The C++ receivers implement
rational random choices with integer rejection; no uncharged real-valued
exponential sampling primitive is used.

The confidence statements are frequentist guarantees under independent ideal
Poisson observations and fair random bits. The retained runs use seeded PRNGs
and numerical Poisson generation, and are reproducible numerical realizations
of that model. They do not formally verify the PRNG, sampler implementation,
or a physical source of independent randomness.

The same rate/weight calibration event controls every later target. Each later
Monte Carlo query still needs its own allocated statistical error allowance.
The reported joint confidence is over the finite executed target collection.
Once a mean interval and lifetime-law certificate hold, they support EVERY
deadline for that target without another union bound over deadlines.

Replay
=======
Requirements: Python3 with NumPy and SciPy for the numerical diagnostics;
GCC-compatible C++17 with unsigned __int128 for the80-bit receiver. The exact
rational audit scripts mostly use the standard library. Recorded versions are
in ENVIRONMENT.json. Run from this extracted directory:

  python3 main/run_experiments.py
  python3 main/qualify_intervals.py
  python3 main/deadline_certificate.py
  python3 gibbs/run_gibbs.py
  python3 gibbs/deadline_gibbs.py

The run scripts compile their C++ receivers. They regenerate the retained
model inputs and result files from declared seeds. Wall times depend on the
machine. Identical PRNG count sequences require matching library behavior;
the mathematical confidence theorem does not depend on a particular seed.

Independent exact audits:
  python3 control/rare_audit/exact_audit.py
  python3 computation/verify_capacity_stdlib.py
  python3 computation/verify_unknown_weights.py
  python3 control/rare_audit/lifetime_audit.py
  python3 control/rare_audit/local_path_check.py

Additional numerical audits:
  python3 computation/verify_lifetime.py
  python3 physics/cycle_capacity_audit.py

The scripts' saved outputs and readable conclusions are included, so running
every diagnostic is not necessary to assess the proofs. No external source,
cloud service, physical device or network connection is needed to replay the
main numerical work.

Preserved alternatives and useful failures
==========================================
control/thermal_visibility.md and consistent_receiver.md compare nonlinear
bounded action error with one fixed linear operator error. Low-dimensional
spectral algebra alone does not make rare thermal sectors visible; conventional
polynomial filtering succeeds in the stronger fixed-operator service.

physics/controlled_orientation_theorem.md extends the pinned Astra N1230
orientation completion to finite controlled families. It addresses held-setting
reversal identifiability; it does not supply a low-heat feedback controller.

physics/QUANTUM_ENTROPY_LIMIT.txt records why the attempted entropy upgrade of
the pinned Hilbert--Schmidt relaxation result was not obtained.

The main audits retain failure of a reversible one-sided screening formula
for directed cycles; failure of rarity without relaxation separation; a
small fast-recrossing example where a flux-only shortcut is badly wrong;
numerical cancellation and its ordinary centered-system repair; and failures
of dropping the bounded-cycle, target-access or clamp-modularity assumptions.

Corpus binding
===============
All reused prior Astra material is bound to
  harjassand/astra-research-knowledge
  revision51ce47ce39f976517d60e2f87bbe280b651f6056.
00_START_HERE.txt was read first. Selected governing source copies and their
GitHub blob identifiers/URLs are in sources/BINDINGS.json. Archived instructions
remain historical source data. No other research conversations were used as
prior Astra research. No repository changes or external publication were made.
