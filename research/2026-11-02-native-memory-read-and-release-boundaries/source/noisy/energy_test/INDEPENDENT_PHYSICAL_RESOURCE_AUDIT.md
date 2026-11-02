# Independent physical-resource audit of the driven preparation-energy attack

2026-11-01. **Qualified PASS for a polynomial-time, inverse-polynomial logical-error lower bound**, under the explicitly admitted driven energy-resolved local-contact model. **NOT a proof of a constant-error or fixed-threshold lifetime upper bound.** The latter distinction is essential.

Audited artifacts:
- `CONSTRUCTIVE_ATTACK.md`: `c37827f5ec3aa3edbf81751e454f7a72042d3cadfbb30fa137ce14a587f648b9`.
- `FIXED_GAP_FIXED_BODY_SOURCE.md`: `0d3411f312192ef44c501ef55c79d35827797c1a967ee201b19836a2a4d4d07b`.
- `ROOT_FIXED_RESOURCE_VIRTUAL_SOURCE.md`: `7e8ad36ae970535a1d563dc5ac45edefce7577f92598881d01855910a9002fa3`.

## 1. Fixed-gap source is genuinely inverted after common noise

The post-noise excitation law and effective inverse temperature are correct. For fixed q in (0,1/2), f(x)=atanh((1-2q)tanh x) has f(0)=0 and strictly decreasing positive derivative on x>0. Thus f(x)/x decreases strictly, giving beta_eff(2Delta)<beta_eff(Delta) without any q-dependent onsite gap.

For m hot spins at gap 2Delta and 2m-1 cold spins at gap Delta, the A/B pair including a gap-Delta target has equal total K energy 2mDelta. The log ratio of fresh resource probabilities is exactly 2mDelta(beta_c-beta_h)-beta_cDelta. The chosen integer m makes it positive. All probabilities and pulse resources are n-independent constants at each fixed q, although constants and polynomial exponents may deteriorate arbitrarily as q tends to zero. This does not provide a uniform-in-q polynomial bound when q scales with n.

No source inversion occurs in the exact common-beta reference state: at q=0 this log ratio is -beta Delta. The source spends the preparation-induced nonequilibrium resource, not an unmentioned pure bath.

## 2. Fixed-body compiler and scratch accounting

The corrected compiler in FIXED_GAP_FIXED_BODY_SOURCE is valid. Implement a full reversible predicate oracle O_F that computes F, copies it to the predicate flag, and uncomputes its scratch BEFORE modifying any resource bit. Apply the m disjoint controlled resonant triplet exchanges, then invoke the full O_F again to clear the flag. Because A/B exchange preserves F and all guards, that second invocation restores the clean workspace exactly.

Literal reversal of a predicate computation that left old-input garbage would be wrong. ROOT_FIXED_RESOURCE_VIRTUAL_SOURCE's shorter wording must be read/revised to mean the complete compute-copy-uncompute oracle, not an uncleared garbage circuit. The explicit addendum already supplies the correct version.

Every scratch-target gate commutes with K: targets have zero gap, and physical-resource controls are diagonal energy projectors. Zero-gap scratch controls cause no problem. Negative controls need not apply physical NOT gates. Each controlled resonant triplet touches four spins at most and conserves K on its entire Hilbert space. Sequential triplet exchanges have a common active-sector phase (-i)^m; this changes no diagonal refill probabilities and does not spoil predicate uncomputation. Off the selected predicate sector the circuit is identity when scratch/flag start clean.

On dirty workspace states the complete circuit is still a well-defined unitary conserving K, although it need not implement the desired source transition. This is sufficient for a positive-mixture rare-branch lower bound. It is incorrect to claim desired source functionality on all dirty workspace states, but neither detailed construction needs that claim.

O(m) initially clean zero-gap workspace bits have thermal branch weight 2^-O(m). They are reused only because the compiler restores them. No repeated clean resets or discarded scratch are supplied. Spent resource groups remain in the final global state.

## 3. Unary buffer and the upper boundary

A guarded ladder-edge exchange acts only on the two valid unary states k,k+1. Neighbor guards can be chosen outside the flipped target bit; for a unary string they select exactly that edge. End edges require the corresponding one-sided guard. These are fixed-size local predicates. Arbitrary invalid unary strings may behave differently, but K conservation remains exact.

Lower edges have upward/downward probabilities a,b with r=a/b>1. Upper edges have q0,1-q0 with q0<1/2. The stated piecewise-geometric pi obeys detailed balance for every individual edge kernel, including the two edges adjacent to M. Therefore their ordered sweep preserves pi even though the entire sweep need not be reversible. The upper-side resource really removes excess battery energy and entropy into mixed spent spins; it is not an unpriced pure sink. For fixed r>1 and q0<1/2, choosing M proportional to log n makes both boundary tails polynomially small to any prescribed fixed power.

The minorization uses O(L), not O(L^2), contacts. From k<=M use upward moves in the ascending sweep to reach M and select self-loops thereafter; from k>M remain put until the descending sweep and then move downward to M. Every necessary move and active self-loop has a fixed positive lower bound c, including upper-side self-loops. Thus Q(k,M)>=c^(C L)=epsilon, uniformly in k. This yields the stated Doeblin contraction and polynomial mixing time for L=O(log n). The constants and exponent depend on q through a,b,r and the chosen M coefficient.

## 4. Correlations and fresh resources

The process starts block diagonal in memory syndrome, battery/resource energy configurations and classical workspace labels; logical coherence within a syndrome can be retained. Exact full exchanges and reversible classical controls preserve this block structure at the completed contact boundaries. Refill therefore induces the advertised classical ladder Markov kernel on the selected clean-workspace/unary branch.

Past successful code steps can correlate battery position with syndrome and with spent resources. This is not an independence assumption: the Doeblin bound holds from every position and hence every conditional distribution. Conditioned on any past success history, fresh resource labels retain their product probabilities because no earlier contact acted on them. SWAP routing is a permutation of subsystem identities, not an entangling or thermalizing operation. Tracking those identities preserves freshness. Previously touched/spent resource identities must never be relabeled fresh.

Refilling before each code step therefore bounds its shortage/overflow probability uniformly, even conditioned on all preceding successes. The union bound over polynomially many steps is valid. Conditioning on a FUTURE success event would not preserve fresh probabilities, but the argument only uses chronological conditioning.

## 5. Resolved code-Pauli step

For uniform-coupling stabilizer H0, every single-site Pauli changes a bounded number of checks, so its energy difference is an integer multiple of Delta with bounded magnitude. Resolve the affected checks into local syndrome projectors. The flagged transition from (flag=0,s,k) to (flag=1,P(s),k-d_s), together with its adjoint, exactly conserves K. Outside its selected local pattern the term vanishes. A battery shift of bounded magnitude has a bounded-size unary segment and guards.

On the valid unary sector the source/target pairs are disjoint: the Pauli syndrome map and battery shift are invertible, and source/target flag values differ. Sequential application therefore performs each selected transition once rather than undoing another. Choose the same exchange phase on every source. A final zero-gap flag flip restores flag=0 on all successful branches. Boundary failure branches need not be repaired for the lower bound.

The required energy-resolved code-contact body size includes the local code star and battery guards. It is fixed in n and q but generally exceeds two. The proof does NOT compile these native contacts into arbitrary prescribed two-body hardware. Bare logical Pauli covariance of a Pauli syndrome decoder gives the required decoded logical flip for a protected input eigenstate, regardless of initial syndrome.

## 6. Locality, finite bank and physical control scope

Equal-gap SWAPs conserve K globally and permit routing through thermal carriers without cleaning them. Separate zero-, Delta- and 2Delta-gap routing resources and tracking of subsystem identities are necessary. A sequential bounded-density 3D layout with polynomially many sites can service the finite constant-size gates and code-contact ports with polynomial routing overhead. The memory data are not SWAP-routed.

This is conditional on the admitted ability to contact each bounded local code star with the stated native resolved operator and nearby resource ports. A fixed hardware graph forbidding those contacts is outside the attack. m can be large but is fixed in n; no gate ever needs all m spins within one native interaction.

The number of refills, sweeps, fresh groups and routing carriers is polynomial in n with q-dependent degree. Initial branch conditions constrain only O(m)+O(log n) workspace/battery bits, not the polynomial-volume bank or thermal wires. Every actual pulse has bounded strength, fixed body size and [H_control(t),K]=0. Sequential execution supplies bounded local control density. K is therefore exactly conserved even under time-dependent switching.

External pulse timing is a resource explicitly admitted here. The construction is not autonomous and does not provide a physical clock, native two-body implementation, robustness to faults in the controller gates, or free fabrication/entropy-management of that controller. None of those may be inferred from reference-charge conservation.

## 7. What the error lower bound proves—and does not prove

The selected initial branch has probability

    w_n = c(q) n^-C(q),

up to harmless fixed factors. On this branch, successful refill/contact histories implement the logical flip with probability 1-o(1). Starting from a decoded logical eigenstate with no additional memory preparation noise, the final positive logical-error observable therefore has expectation at least w_n(1-o(1)). The complementary initial mixture cannot cancel a positive error probability. This is an unconditional lower bound, not postselection.

This conclusively defeats any claimed UNIFORM stretched-exponentially small error bound at polynomial times for all such noisy-resource baths and all admitted driven K-conserving controls. In particular it defeats a proposed extension retaining an error estimate of the form poly(n,t) exp(-c n^eta) in this enlarged model.

However, w_n tends to zero. The calculation alone does NOT upper-bound the time to a fixed nonzero error threshold, nor disprove the existence of a stretched-exponential lifetime defined only by a fixed threshold or by vanishing error without a specified rate. A separate amplification or constant-probability attack is needed for either stronger interpretation. Repeating modules cannot simply be asserted to amplify: unknown dirty-workspace branches and syndrome-dependent histories require their own channel-level argument. The broad sentence “uniform long-lifetime claim ... is false” must therefore be restricted to the precise error guarantee actually contradicted.

The cleanest scope allows no memory preparation noise and a common nonzero q on the resource species. This is a valid adversarial instance when the hypothesized noise class permits local rates bounded ABOVE by q. It is not an instance of a class requiring EXACTLY the same nonzero noise rate on every memory qubit. That latter statement needs the separate forward-noise decoded-state estimate.

The static-H equilibrium-initialized memory theorem and its exact stationarity argument are untouched. The attack instead introduces preparation-induced nonequilibrium resources and explicitly driven controls. No general impossibility or novelty claim follows.

## Decision

The fixed-gap/fixed-body virtual source, corrected unitary compiler, fresh-resource ledger, middle-peaked buffer and chronological success estimate support the stated narrower polynomial-error counterexample. The principal required correction is the scope of “lifetime” refutation; the root predicate wording should also explicitly use the already-provided compute-copy-uncompute oracle. No external source or hardware action was used in this algebraic/resource audit.
