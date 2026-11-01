# Independent finite coherent receiver and correlated release audit

**Decision: ACCEPT the frozen declared-model proof and exact sufficient release budget, with the source-marginal wording qualification and physical-service boundaries below.** No fatal mathematical/code error was found. This is not acceptance of hardware feasibility, a novel cancellation principle, the necessity of the nuisance source, or an architecture-level advantage.

Audit directory: `coherent_receiver_release_independent_audit_20261031_2204UTC`.
Input directory: `../coherent_phase_receiver_20261031`.
Original 13-file input manifest SHA-256: `2e40e9b9f7c27eadbeb2c5d8d5953a260ccb8e13d642151f2e7f9f75b0198fbe`.
Root geometric lemma SHA-256: `144f70e7e19e0c65d0dbcb515bbdf57de7b886d0d667257e7a331e9a5f337331`.
All 13 literal files were size/hash verified before copying. Frozen proof/code/certificate inputs were not executed in place and were rechecked unchanged at completion. During final review the constructor supplied a controlling qualification without changing those 13 files. The accepted revised manifest SHA-256 is `f6a94625ec16d3927f9552ae6a8aa160860dc27478b96a79c2f2d42602c493be`; it binds 15 entries, adding `SOURCE_BRANCH_QUALIFICATION.md` (SHA-256 `8c5cdd8965f3b9351fdbe74ac19c9db5e4690ce498ddd57d3ac6d2f7cbadf8cf`) and the exact original manifest as `MANIFEST_PRE_BRANCH_QUALIFICATION.json`. All 15 revised entries were independently verified. Acceptance is confined to that qualified binding; historical exploratory notes, a new B-squared bus capability and any optional high-order cutoff extension are outside this freeze.

## 1. Source/entire-field overlap and common-relative-operator join

The positive-data branch is the initialized vacuum-input damped TLS with H=cX and L=sqrt(lambda) sigma-minus. Projecting every output time bin onto the constant coherent pulse gives the coherent-bra drift `-iH-L*L/2+beta* L-|beta|^2/2`; with beta=-2ib this is precisely the candidate 2x2 matrix. The fixed source phase change makes it real symmetric B. Its negative trace and determinant 4b^4 give negative semidefiniteness; its nonnegative off-diagonal entries give positive ground-to-ground overlap. Thus `a=<0|exp(TB)|0>` is the *source AND entire emitted field* overlap, not a fidelity of the reduced source or an inference from emitted power.

Conjugating the source by Z and the emitted field by number parity reverses the data-conditioned drive while preserving the source-field coupling and initial state. It gives the same real reference overlap in the negative-data branch. The common receiver dilation contains the routing vacuum, internal-loss vacuum, source field, retained source and cavity at the endpoint. Causal reordering preserves the order of each source-bin/receiver-bin encounter; source interactions with future bins commute with receiver interactions on past bins because their only common data control is conserved Z. Consequently the common-space relative operator is indeed `O=R U_-* U_+`, with norm at most one. It must not be formed after discarding source/cavity/field correlations.

**Root lemma independently accepted.** Decompose `psi=a psi0+sqrt(delta) chi`. The two cross terms are each bounded by `sqrt(1-|f0|^2)` using orthogonal projection of O psi0 and O* psi0. The diagonal remainder is bounded by `delta(1+|f0|)`. This proves the complex-coherence inequality, including contractions that are nonunitary or non-normal. Replacing `1-|f0|` by `R>=|1-f0|` yields `R+2delta+2sqrt(2delta R)`. No phase rotation is being silently performed. The difference of two qubit dephasing channels has diamond norm exactly `|f-g|`: a diagonal output phase rotates the off-diagonal difference to the real `(Id-Ad_Z)/2` form, whose norm is one, and a plus input attains it. This justifies the complete-channel receiving, including arbitrary references.

The separate moment proof is also sound: `D'=lambda(p^2-D)`, the cold energy bound, and the displaced-field number identity give the stated vector estimate. It does not equate incoherent photon number directly with logical error. The exact coherent projection is the stronger ordinary calculation used in the budget.

### Wording qualification — now supplied by the controlling addendum

The main proof's Section 1 sentence that the “source marginal is the ordinary driven damped qubit” must be read **conditional on fixed data Z=+1 or -1**, or as a statement about the autonomous joint source+data generator after tracing the downstream receiver. It is not literally a single driven-qubit source marginal for arbitrary data superpositions. For initial data |+>, the unconditional source is a mixture of opposite-drive branches; its initial y derivative is zero, versus -2c in the +Z branch. Section 3 correctly fixes the positive branch, and the source-population bound holds for both branches and their mixture, so this wording does not invalidate the proof or release bound. The independently inspected `SOURCE_BRANCH_QUALIFICATION.md` now states exactly this controlling interpretation and is accepted; no code/certificate replay changes were necessary.

## 2. Actual cascade, loss, coherent phase and retained cavity

The signs of the series Hamiltonian `Im[Lc* sqrt(eta) Ls]` and combined output jump produce the correct one-way cascade. Tracing the downstream subsystem leaves the source+data dynamics unchanged even for initially correlated upstream/downstream states. A separately reconstructed coherent-input cascade with `L_source=beta Z` reproduces the candidate complex formula with routing loss and internal loss; it does not rely on the candidate source-cascade implementation.

The coherent amplitudes satisfy `alpha_- = conjugate(alpha_+)`. The cross-generator trace gives `d log f/dt=-8b^2-2i chi alpha_+^2`; integration at chi=k/2 gives the stated finite-time expression and secular loss `8b^2(1-eta k_e/k)`. Both the deterministic phase and cavity endpoint memory are retained. The cavity is generally occupied at T; replacing its trace by a vacuum projection changes the independently calculated coherence (by about 0.039 in two diagnostic cases), so a hidden ringdown/reset would not be harmless.

The receiver is passive but requires a supplied dispersive coupling valid on the occupied photon sectors. Finite Fock diagnostics do not certify the infinite-dimensional model. Here the analytical common-dilation comparison and exact coherent solution, rather than cutoff convergence, supply that theorem. No numerical high-sector extension is accepted from this audit. A count-MGF tail alone would not certify a real receiver without the actual passive number-conservation premise, received low-sector model/error and a valid outside-sector comparison.

## 3. Finite ramp and actual correlated-source SWAP join

For any real ramp satisfying |chi(t)|<=k/2, the coherent amplitude is bounded by `4b sqrt(eta k_e)/k`. The derivative of f then has modulus at most 24b^2, giving the stated finite ramp charge. The actual source keeps running; its coherent overlap must be evaluated at T+t_switch, as the certificate does. This is not a free source shutoff, cavity reset, infinite-slew control specification or residual-chi tolerance.

Once chi is exactly zero in the ideal declared model, downstream source/cavity processing is data-independent. One-way semicausality permits it to be traced from the memory-error comparison without resetting its correlated state. On the remaining source,D,M,reference state, direct generator calculation gives precisely

- `R'=-i[H0,R]-ic[Z_D,Y]`;
- `Y'=-i[H0,Y]-ic[Z_D,R]-(lambda/2)Y`.

This closure is valid for arbitrary initial correlations, not just a product source state. In the H0 interaction picture, trace-norm commutator bounds give the stated (R2). Positivity of source blocks gives `||Y0||_1<=2sqrt(p0(1-p0))`; the reachable cold-source population bound yields `16b^2/lambda+8b^2 tau`. The result is applied uniformly to every original data/reference input, not composed as a fictitious source-independent reduced map after tracing the apparatus.

An ideal SWAP transfers the old data state irrespective of the memory's old state, but real gate input range, new-memory hardware and its isolation are paid. After actual isolation, any trace-preserving operation on the old apparatus leaves the output-memory reduced state unchanged, despite retained correlations. This closes the previously identified trace-at-T versus release gap **conditional on the explicitly supplied chi-off, finite source-blind SWAP and subsequent isolation services**.

## 4. Exact certificate audit and ordinary comparator

The 2x2 exponential uses a valid row-sum operator-norm bound for symmetric B, scaling to at most 1/4, a conservative degree-48 Taylor tail, conservative rounding, and Euclidean semigroup contraction. The squaring-error recurrence is bounded by shifting the error by one rounding allowance and using `(1+x)^N-1<=2Nx` in the asserted range. Therefore its rational overlap interval is justified; the 100-bit integer square-root ceilings and lower-overlap substitution give rigorous upper budgets. The rational-square lambda frontend restriction is a computational restriction, not a physical no-go.

The reference bound uses `(1+kT/32)^(-16)>=exp(-kT/2)` and `|1-exp(w)|<=|w|` for Re(w)<=0. Its uncorrected complex phase is included. The release certificate independently reassembles exactly to

**0.009690440319143791 < 0.01**, comprising before-SWAP upper **0.008214190319143791**, correlated-source SWAP upper **0.00047625**, and **supplied—not established—other error 0.001**.

The unchanged-source lower bound was also independently derived rather than assumed from an earlier package. Its exact telegraph equation is `f''+(lambda/2)f'+4lambda b^2 f=0`, f(0)=1, f'(0)=0. Contractivity gives `f(t)>=1-8b^2 t`; substituting this into the integral for -f' and bounding the turn-on integral below by `T-2/lambda` yields the stated clipped lower bracket. This is a valid unchanged-source comparator, not proof against equally equipped coherent feedback, DD/QEC, a source-free layout or another useful-mediator architecture.

## 5. Executed evidence

- Author suite replay: **14 exact, 26 floating, 7 high-precision checks**; separate cascade script also replayed its 3 symbolic checks and 6 diagnostics.
- Scalar certificate JSON, release certificate JSON, cascade diagnostic JSON and author test-result JSON reproduced **byte-identically**.
- `independent_join_audit.py`: **374 recorded assertions**, including 90 general-contraction geometry fixtures, two vacuum-bin source/field-projection convergence checks, four independently built coherent-input cavity checks with loss and phase, arbitrary correlated-cavity/source moment identities, and complete finite cascade/ramp/SWAP examples. Repeated assertion counts are not being advertised as unrelated physical experiments.
- The full release propagation retains the source and cavity state and uses a data/reference Bell pair and a non-ground memory. At lambda4096, b0.2, k128, routing0.999 and external fraction0.999, with the stipulated ramp/SWAP times, the finite-cutoff normalized released Choi trace error was **0.005913061425933093**. The actual SWAP difference from swapping the same correlated preswap state was **0.0001909008559956135**, below **0.00047625**. These are floating finite-cavity diagnostics; a Choi trace error is not itself the worst-input diamond distance, and cutoff agreement is not certification.
- Subsequent old-apparatus unitary evolution was independently checked not to change the isolated memory/reference state.
- `independent_certificate_audit.py`: **12 independent 110-digit overlap evaluations**, including zero time/drive and rational-square decay extremes, lie in the claimed intervals. Exact rational release assembly, square-root inequalities and the declared frontend restriction were separately checked.
- All **70** parameter rows remain: **19 sufficient-budget passes, 51 failures**. A failed upper bound is not a physical lower bound.

## 6. Physical services, historical ownership and completion

The exact model requires cold initialized source/cavity and vacuum input; actual Markov source/output validity; one-way routing and its loss, spectral response and any nonnegligible transport latency; the conditional passive cavity and dispersive validity; independent local copies; graph gates; chi switching; finite SWAP strength/error; and a separately isolated memory with a specified holding/consumer interval. The common-space circuit reordering is not permission to ignore real propagation latency or switch exposure. The stipulated epsilon_impl must genuinely bound all residual errors over the actual reachable input family; its value was not acquired by this calculation.

The source does not produce the desired graph interactions here. It has not been established to be unavoidable, and a source-free or different ordinary architecture may win. The same memory, controls and access must be offered to comparators. The next useful-mediator/B-squared bus request is outside this audit.

Primary-source inspection supports ordinary ownership: [Gough and James](https://arxiv.org/html/0707.0048) develops series/cascade quantum networks and optical/direct feedback; [Szigeti et al.](https://arxiv.org/html/1401.4493) supplies no-knowledge decoherence cancellation with actual observation/control resources; [Saiphet et al.](https://arxiv.org/html/2010.06904) shows the importance of finite delay and noncommuting controls. These are mechanism/context checks, not hardware support for the candidate.

**Completed:** whole-proof/source-bound review, all three joins, exact bindings and replays, independent adversarial diagnostics, cost/comparator review and this receipt. **Denied actions:** none. **Pending/uncertain:** only the explicitly unearned actual component/service evidence and architecture-selection question; no running tool process remains. No equipment, outreach, purchases, publication, source-input mutation, external agents or denied-source retries occurred. One initial test invocation used the parent directory and did not execute a script; it was rerun in the unique audit copy after the known file-not-found result. No helper agents were used.
