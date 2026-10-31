# Independent review: energy-weighted activity and frozen resource ledger

31 October 2026. Two separate outcomes: PASS for the local energy-weighted count lemma and structural Gibbs certificates; PASS for reproduction of the displayed-cap resource ledger, with its precision and operation proxies explicitly not a gate-level certification. Neither outcome improves the frozen complete compiler automatically.

## 1. Sources actually read

The complete `ENERGY_WEIGHTED_ACTIVITY_ADDENDUM_CANDIDATE.md` was read and hashed as `ac06ea4451f653db3824792b259a553057ca053639e59a784c87b6a2cbb320f3`.

The complete `../native_resource_audit_20261031/resource_ledger.py` was read, SHA `a32ca4c0bbe13e06393c8faf52994c1866b63b7329b679f85b28b8a83b85b568`. Its JSON has SHA `8f41f68a8c517a740f4a45f11c01619316f5f9e963eb20aaa62190c10d9131d6`. All 30 JSON rows were regenerated in memory independently by importing the actual module and calling its case function; every row matched exactly. The saved source/JSON were not modified.

The relevant displayed formulas were checked directly against frozen native whole source `f503c80089c85006856e6ca1ea8b536bb36e0aa4931db071320a33a056a07192`. The prior native count and whole receipts remain dependencies, rather than being silently replaced by this addendum.

## 2. Energy-form commutator bound

Use P = |psi><psi|, Q = I-P, and H supported on Q. All operators may be tensored with an arbitrary reference. The acquired form bound on Q i[K,H] Q gives an absolute QQ expectation at most a_E E, where E = Tr(H rho).

For the cross term, the state-dependent Cauchy–Schwarz inequality applied to H^(1/2) K P and H^(1/2) Q gives

|Tr(P K H Q rho)| <= sqrt(Tr(P K H K P rho)) sqrt(E)
                      <= r_E sqrt(Tr(P rho)) sqrt(E)
                      <= r_E sqrt(E).

The other cross term is its conjugate up to the commutator sign. Thus the total absolute expectation is at most a_E E + 2 r_E sqrt(E). This does not require PKP = 0; the PP Hamiltonian part commutes with H. The expectation argument is on normalized test states, and yields an operator bound. It does not apply normalized-state Jensen to an unnormalized tilted evolution.

## 3. Tilted activity bound and controls

For u = exp(theta)-1 <= min(1, kappa/(16h)), set a = 4u/kappa and W = I+aH. The earlier native source calculation supplies source/count drift at most -a kappa lambda H/4. The QQ coherent part is at most a sqrt(lambda) a_E E. Under sqrt(lambda) >= 8 a_E/kappa this spends at most a kappa lambda E/8. The remaining expression is

 -a kappa lambda E/8 + 2a r_E sqrt(lambda E)
 <= 8a r_E^2/kappa = 32u r_E^2/kappa^2.

This is an elementary optimization in sqrt(E). Consequently the tilted adjoint generator is bounded by that scalar times I, hence by that scalar times W. Since I <= W <= (5/4)I, the inherited conservative factors 2 for the initial state and each prescribed joint instrument are valid. The stated MGF and Chernoff count cap follow for arbitrary inputs and references and the specified physical unraveling. H0 acts only on the system as before.

The high-rate condition and certificate acquisition are substantive. An inverse-energy oracle or an optimal form norm is not obtained for free. Zero injection or zero form bounds can be treated by their actual certificates; this is not a hidden numerical zero test. The allowed tilt still scales with h/kappa, so neither the tail allowance nor arbitrary source interventions become dimension-free. This is a count improvement, not a new no-jump operator or complete channel circuit.

## 4. Concrete Gibbs certificates, including noncommuting system operators

For the direction-merged source, Pi_j acts on spin j and is diagonal on its neighbor controls. It commutes with Z_i for i != j. Since Pi_j psi = 0, Pi_j Z_i psi = 0 for i != j. In P K H K P every term with either coupling index different from j therefore vanishes, not merely its scalar average. The result is

 P K H K P = sum_j <psi|Z_j Pi_j Z_j|psi> A_j^2 tensor P.

Each coefficient lies in [0,1]. Hence r_E^2 = sum_j alpha_j^2 is a supplied upper certificate even when the A_j do not commute. No unknown thermal correlation needs estimation for this energy-weighted bound. The same commutation argument works with nonzero fields, but would not acquire the separate centering needed by the full compiler.

The local two-dimensional commutator satisfies ||[Z_j,Pi_j]|| = 2 sqrt(r_0 r_1) <= 1. Therefore ||Q i[K,H] Q|| <= sum_j alpha_j = b, and conjugating by H_Q^(-1/2) yields the acquired certificate a_E = b/g. The source's notation 'a_E <= b/g' means that this is a sufficient upper bound on the required form norm; choosing the declared certificate equal to b/g is valid.

For the separate zero-field open-chain certificate, C_ij = <Z_i Z_j> is the path product of tanh J. Its absolute row sums are at most 1+2 sum_(k>=1)t^k = (1+t)/(1-t). C is a positive correlation matrix. With B v = sum_i |i> A_i v, B^dagger(C tensor I)B = sum_ij C_ij A_i A_j remains a valid positive operator identity without commutativity. Exact centering gives PKQKP = PK^2P. Using t <= 1/40 yields the stated 41/39 times sum_i alpha_i^2 bound. The factor is conservative because tanh(1/40) < 1/40.

The text correctly does not supply a smaller-normalization offdiagonal block encoding for free. A complete positive-sector and finite-bit receiver using those unequal block normalizations would need a new operation and resource proof.

## 5. What the ledger actually computes

The ledger fixes T = 1, original b = 1, alpha_0 = 1, and p = 0. Its normalized constants are exactly g = 19/20, kappa = 20/39, h = alpha_H = 20n/19, alpha_L^2 = 40n/19, B = 20/19 and mu = (19/20)lambda. The code's first lambda is the upward ceiling of the normalized high-branch threshold. Independent exact rational checks verified that all 30 cases satisfy that threshold.

The chosen tau = 1/256 is within the required factor-two window below 1/(128B). Wcap = 258 includes one extra safe slot beyond ceil(1/tau)+p+1 = 257. Mcap, Scap, the integer padded amplification A, its degree 2A+1, beta/sigma/eta, endpoint floor, virtual cap, timing floors and bisection depths reproduce the frozen high-branch formulas with conservative extra ceilings and halved endpoint lower bounds. The implementation uses interval arithmetic rather than an exact irrational comparison. Its positive finite interval endpoints are numerical ledger objects, not a synthesized arithmetic circuit.

The padded slot proxy is exactly Scap * (2A+1) * (Kcap+1). At n = 4, epsilon = 1/100 and lambda = 305954 it is 3,123,922,221, with Scap = 4151, A = 256 and Kcap = 1466. This number is a count of conservatively padded source-kernel slots under this protocol, before the real kernel, arithmetic, source encoding or consumer cost. It is neither a lower bound on all algorithms nor an implemented quantum gate count.

The saved `bits_kernel_tolerance` field requires particular caution: it uses beta/[10^4 * 100 * (Kcap+1)]. The frozen theorem instead subdivides by the actual capped total number of relevant operations and tightens internal LCHS/SVA tolerances. The arbitrary multiplier 100 does not enumerate those operations, binary-duration slots or quadrature internals. Therefore this field is only an illustrative outer precision proxy, not a certified final primitive tolerance or executable full error allocation. This limitation does not affect the exact reproduction of the cap and slot arithmetic. The author/root were notified of it before this receipt.

## 6. Fair comparison and scope

The generic stack-action field is Hs + sqrt(mu B) + mu alpha_L^2. That is an input normalization/action scale for an ordinary algorithm, not its gate count. The classical uniformization field n*lambda is a Poisson tick expectation; the flip bounds use the actual heat-bath rate interval [400/841,441/841] implied by the weak rational chain weights. These are three different computational quantities. A smaller number in one column does not establish a runtime crossover, speedup, lower bound, or advantage.

The ledger is useful precisely because the frozen compiler's already large conservative slot counts make a practical claim unearned. The new energy-weighted count could improve its physical count factor, but all source/window/kernel/amplification budgets would first have to be recomputed and rebound; this receipt does not do so. Ordinary exact low-dimensional solvers, classical trajectories, gauge choices and other acquired simulation methods remain relevant comparators.

No additional scientific correction is needed to the energy-weighted addendum. The ledger is accepted only as the explicitly limited displayed-cap/proxy audit described above. No new whole compiler, practical resource estimate, novelty claim or implementation is admitted.
