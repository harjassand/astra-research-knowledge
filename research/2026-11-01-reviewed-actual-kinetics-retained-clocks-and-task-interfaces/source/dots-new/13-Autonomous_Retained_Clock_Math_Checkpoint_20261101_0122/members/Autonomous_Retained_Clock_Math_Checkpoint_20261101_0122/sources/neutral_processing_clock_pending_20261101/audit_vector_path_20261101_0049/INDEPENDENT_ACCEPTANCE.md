# Independent acceptance: neutral vector and finite-path refinement

Date: 2026-11-01 UTC. Reviewer: independent reviewer of the root author's
conditional vector argument and subsequent sharper-storage derivation.

## Verdict and frozen bindings

**PASS:** the unchanged original weaker vector theorem, both chronological
orientations for the specified compact scalar-trial drift class, and the
conditional nonautonomous finite-path join.

**PASS:** the root author's sharper bound

  ||x(T)||^2<=d/4,
  ||u(T)-exp(-aT)e||^2<=d(1+d)/4,
  sup_T||u(T)-exp(-kT)e||
    <=(1/2)sqrt(epsilon(1+epsilon))+epsilon/exp(1).

The exact accepted rendering is
`NEUTRAL_VECTOR_AND_PATH_SHARP_V2.md`, SHA-256
`8da465ed3817a2e5cf0088cd0efba23e056a148422bf5a3120b96606a960a403`.
The root-authored refinement message was independently checked and transcribed
without changing its mathematics. Its unchanged text is
`ROOT_REFINEMENT_MESSAGE.txt`, SHA-256
`1e88f97db1502286a1de43fc4a99ae5cb1e9595ecbd03ec9bd8b8ba172ee1180`.
This is independent mathematical review of the root's argument, not a claim
that a second reviewer subsequently audited the reviewer's transcription.

The unchanged original candidate is `NEUTRAL_VECTOR_AND_PATH_ROOT.md`, SHA-256
`c3c9b693788febb28770bc153ce6594695e5f91fef23c5740783d18ae59ffb26`.
The base theorem is `PASSIVE_PORT_CLOCK_ROOT_V2.md`, SHA-256
`7696ef6f47f8003749e0b0fbbfdf8c067d1834e398d011c75c8cc075853a5579`.

## 1. Storage and vector constants

The weaker root's calculation is correct: ||x||^2<=2CY<=sigma*a/(a-sigma)^2
=d(1+d), and adding the squared scalar error d^2/4 gives d+(5/4)d^2.
Orthogonality, not a triangle inequality, justifies that sum.

The root's sharper refinement retains the dissipative integral. For sigma>0,

  X^2<=2CY-2Y^2/sigma,
  C<=b+Y/a,  b=1/sqrt(2a),
  gamma=(a-sigma)/(a sigma)>0,
  X^2<=2bY-2gamma Y^2
       =b^2/(2gamma)-2gamma(Y-b/(2gamma))^2
       <=d/4.

There is no improper maximization over independent C,Y: substituting the valid
upper bound C<=b+Y/a is legitimate because Y>=0. Maximization is then over Y
alone and may enlarge the feasible set, which is safe for an upper bound.
Adding the already earned scalar error d^2/4 proves d(1+d)/4. At sigma=0 the
storage inequality gives x=0 and the scalar law is exact. The rate-k triangle
correction epsilon/exp(1) uses a<=k, kq<=1+epsilon and aq>=1. All steps are
finite-horizon before taking the uniform supremum. No gap or optimality claim
was inserted.

## 2. Both actual chronological orientations

For observables, partial_s P_{s,t}=-L_s P_{s,t}. Thus
v(r)=P_{t-r,t}e satisfies v'=L_{t-r}v, initially e. This is NOT the same as
arbitrarily replacing P^* by P in the forward density equation.

For the base's actual compact transverse drift, write L_t=L0+s_amp(t)C.
Weighted divergence gives C^*=-C and the complete smooth bounded spatial flow
is measure preserving. Forward density has transport -s_amp(s+r)C; backward
observable has +s_amp(t-r)C. Both have zero real form contribution, the same
reference form domain, and the same neutral scalar trial. A locally bounded
measurable schedule remains locally bounded after finite-interval reversal.
The base's explicit proper Lyapunov estimate also uses only |s_amp|. Therefore
both equations are actual received weak energy evolutions, not merely formal
skew identities.

This concrete statement fixes a received trial psi(y), or another trial whose
neutrality is separately proved. It does NOT prove that an arbitrary global
phase-space approximation is fixed by the transverse field. No unrestricted
unbounded-mobility or feedback receiving is inferred.

## 3. Global mean-zero restriction

In a conservative model constants lie in the full reference kernel. The
restriction to H0={integral f d pi=0} is therefore necessary for the abstract
injective-reference statement. With finite pi, the full constant belongs to the
form domain; mean subtraction preserves that domain. The restricted form is
closed and densely defined on H0. In the connected uniformly elliptic
constant-SPD model, zero energy forces a constant function, so this restriction
is injective.

Actual full Markovness gives P1=1; common pi invariance gives P^*1=1. Both
orientations preserve H0 and are contractions. Positivity is used on the FULL
process when joining to paths, not asserted as a lattice Markov structure on
H0. A nonzero mean-zero psi still must earn finite inverse form and its current
certificate. Symmetry/oddness alone does not earn that inverse form or a useful
numerical epsilon. The actual global odd-trial/current and numerical path
certificate remain pending.

## 4. Finite-path join and exact initialization assumptions

The source path theorem is `ROOT_VECTOR_TO_PATH_THEOREM.md`, SHA-256
`d1eb7f96cd68e1c681baa4907f888265dbd16a233096d9a345a53003d53e4979`.
Its controlling independent audit is SHA-256
`592b28cb65e75da7f4ea4274754147892c1e1cb56ddf3dc25cda6ae3afc73bfe`.

For deterministic times, replace P_Delta by the actual P_{s,t} throughout the
path proof. Common invariance preserves the unconditional density bound
f_t<=R. Conditional Jensen is applied along ACTUAL label histories and then
integrated under this unconditional marginal. It never asserts bounded
hidden-state densities conditional on histories. The comparison must have the
SAME initial label distribution, with

  r_i=exp(-k Delta_i), Q_i(z,z')=(1+r_i zz')/2.

All comparison transitions are positive. Bernoulli KL<=chi-square gives exactly
R sum_i delta_i^2/(1-r_i^2), and Pinsker gives the stated TV bound. Reversibility
is not used in this path step. For a +/-1 label on the entire state space,
contraction gives delta_i<=sqrt(N)G(epsilon)+(1+r_i)eta.

The parameter k is a correlation-decay parameter: a symmetric continuous-time
two-state representation has flip rate k/2. This does not make the actual
physical record a renewal process.

Finite initial L2 cost D_init does NOT replace R in the quadratic KL theorem.
Only the separately proved linear TV alternative follows without R. The bound
for the same continuing trajectory uses the actual full process's Markov
conditional expectation; arbitrary record feedback or independent-random-
schedule mixing is not silently promoted into a Markov claim on an incomplete
state space.

## 5. Controlling cost correction and supplied counterexamples

The unchanged path audit above controls cost wording: J finite accumulator
states, fixed-cost transitions => O(nJ) arithmetic operations and O(J) space.
O(n) requires J fixed. Bit complexity, input decoding, exponential enclosures,
certificate construction and numerical error remain separately paid. Bounded
real-valued range alone does not imply a fixed state count.

The included audit provides explicit counterexamples for:

- replacing R by fixed L2 concentration in the quadratic KL bound;
- inferring deterministic-time guarantees at adaptive first-jump observations;
- equating bounded real accumulator range with cheap fixed-state computation.

Those boundaries remain active in the sharper-vector join. Finite sampled-path
TV controls absolute event errors; arbitrary unbounded observable expectation
errors or relative rare-event errors are not thereby bounded.

## 6. Nonclaims and verification

No actual global odd-trial/current construction, numerical rate/path bound,
physical preparation/control, iid restart, adaptive-control theorem,
continuous renewal, processed MFPT, quantum-fault claim, historical novelty,
universal cheap event oracle, or new executable interface is accepted.
Ordinary storage/passivity/Schur and entropy-chain arguments receive full credit.

The second package carries bound exact sources and stdlib-only rational algebra
regressions, not simulations or a finite test replacing the proofs. The first
proof ZIP remains immutable at SHA-256
`4072eb069be8fd4195619e10728f17ecf948bc1a3d5b61244658daeb33733388`.
No upload, helper agent, denied read, external retrieval or permission escalation
was needed.
