# Selectable CNOT pulses on running native banks: construction to test
30 October 2026. Root new construction candidate, not an accepted gate theorem.

## Why this is not the already accepted finite-group tracker
The earlier REUSABLE_FINITE_GROUP_FRAME.md already provides arbitrary command histories on a FIXED number of colocated blocks and a fixed finite transversal group, with one permanent frame and no per-command restart. It is stronger than an unnecessary reproof of two-bank CNOT repetition. Its explicit limitation is changing partners across an unbounded collection of banks without growing grouped onsite dimension.

The present target is a register of many native CSS Tanner banks with a fixed bounded-degree bank-interaction graph. An externally supplied schedule selects matchings of bank edges. Corresponding DATA sites on selected neighboring banks have actual two-site CNOT pulse couplings, in addition to their existing native hub/resource couplings. The physical degree stays bounded if the bank graph does; local dimension does not grow with bank count or circuit length. A selected gate acts transversally on ALL corresponding encoded logical coordinates, not an arbitrary chosen logical coordinate within a positive-rate bank. One designated logical coordinate per bank is a possible paid low-rate use; unused coordinates need not be claimed individually addressable.

We do not claim a self-dual code, transversal Hadamard, non-Clifford universality, or an autonomous noisy instruction distributor. The task is actual selectable encoded entangling/linear reversible operations while retaining the same dirty native apparatus. An ordinary informed implementation may use exactly this pulse/relaxation route; no speedup or novelty is asserted.

## 1. Proposed actual cycle
After a fixed native-relaxation interval, freeze the selected banks' nominal native DATA/controller/monitor generators using declared bounded scheduled controls. Weak perturbations remain on. Apply the actual constant-duration transversal CNOT pulse, a product of disjoint two-resource-site Hamiltonian evolutions. Re-enable the SAME native memory hardware on each selected bank and allow a fixed relaxation interval before another gate involving that bank. No controller reset, physical forest inverse, ideal decoder, or clean-gate snapshot is inserted.

The abrupt bounded coefficient-switch implementation has no state kick. If finite ramps are demanded, use the actual first-initiation-off support construction and owner-local payload footprints; do not call strong remaining payload weak noise. Native clocks/workspace/locks may remain busy and entangled with DATA when frozen. It is exactly this prefix history that must be paid.

## 2. Actual available recovery estimates
The accepted global memory contract gives a positive killed state preserving arbitrary logical information, a canonical radius/energy basin, and full-versus-killed complete error poly(N)(1+T)exp(-cN). Its physical exponential witness obeys

 e^(-q_t N)e^(s' E)<=F<=e^(gN)e^(sE)

in the same canonical chart. The raw logarithmic drift has a scalar entropy consequence on positive killed states: if m=Tr(F rho), the positive proof pullback and scalar Jensen give

 d(log m)/dt <=-k log m+rho N,

with the actual constants and warm domain. This receiving step must be checked against the exact global source, not inferred from the upper envelope alone. For subnormalized killed states the pullback preserves their mass; m log(m/trace rho)>=m log m provides the conservative same inequality.

The original full-Hilbert singleton BUSY witness separately gives

 d(log m_busy)/dt<=-lambda_busy log m_busy+rho_busy N,
 e^(2c delta M_BUSY)<=G_busy<=e^(2C delta M_BUSY).

It holds for warm states and arbitrary retained correlations, not only from ready initialization. Thus one fixed dwell can reduce the source exponent from a fixed warm value toward its stationary coefficient, and can reduce a warm BUSY exponent toward its small activity floor. Exact pointwise energy/BUSY cut thresholds and dwell constants must be acquired from these two actual inequalities.

## 3. Gate input is a positive common span, not a clean controller
At the exogenous gate time, cut only in the proof to canonical energy E<=e_in N and physical BUSY<=b_in N, inside the existing logical basin. Transfer the BUSY tail from the full state to the positive killed state as in the accepted live-BUSY endpoint. The true logical target/reference is retained, and virtual cuts cost their actual gentle/complete norm error.

The canonical-to-bare forest has nonidentity DATA action on at most a fixed footprint per busy owner. Therefore every coefficient has a physical DATA error support bounded by its canonical support plus f M_BUSY. Its arbitrary controller/bath coefficients remain. Transversal physical CNOT maps the intended product code to itself and spreads a Pauli support by at most two. When the SAME native forest chart is restored for the target logical state, the preexisting active-prefix footprints contribute another fixed multiple of M_BUSY. Ready owners cannot become nonready just because DATA was acted on: their A0/W0/FREE predicate is DATA-independent. Other history defects can be charged only within the already busy footprints, not as a clean new controller.

The needed deterministic receiving form is thus

 r_after <=C_r (r_before+M_BUSY_before+ell),
 M_BUSY_after <=M_BUSY_before+C_b ell,
 E_after <=C_E (r_before+M_BUSY_before+ell),

where ell bounds new local pulse/ramp insertions. Derive the constants from the actual forest/read/owner predicates; this source does not grant them by calling the gate transversal. The independent source-handoff conversion from strong-ready input is not automatically the same arbitrary-live-prefix claim.

## 4. Price the finite pulse by a legitimate bath comparison
In the interaction picture of the intended disjoint CNOT pulses, a q-site perturbation has support on at most2q DATA/controller sites, with unchanged fixed-norm constants. All nominal native operations are off in the pulse window. Apply the accepted reduced-bath reference construction, not deletion of HP summands:

 Lbar_B=Tr_system L(I/d tensor dot),
 Delta_e=N_e-Id tensor Tr_system N_e E.

Its reference is CPTP and its total local insertion norm is O(eta N) for this finite pair of banks. The tail beyond ell=delta_p N is exp(-c_p N) for sufficiently small fixed eta times pulse duration. Low orders stay in the common local-error span of the actual logical CNOT and the existing sparse prefix state. No bath-volume cost or stochastic Pauli trajectory is introduced.

For many disjoint bank pairs one may use pairwise bounds and a union/hybrid factor equal to the number of scheduled operations. The relevant noise norm remains per physical site; unselected banks and discarded factory work are retained as a shared bath only where no nominal coupling to the selected DATA remains.

## 5. The cycle must close a strict budget, not just one pulse
Choose source cut thresholds and pulse insertion allowance so the deterministic bound in section3 enters the SAME native warm radius, BUSY and moment margin. Pointwise spectral envelope compression then supplies a warm exponent nu_out. A subsequent fixed dwell must return to the section3 input thresholds with exponentially small tails. The stationary energy/activity floors must be strictly below those thresholds; the actual tunable small-first-edge/noise family may supply this, but numerical or symbolic inequalities must be written and checked together.

With those uniform inequalities, virtual good-cut channels compose through arbitrary retained history. A conservative telescoping error bound for L scheduled gates is L poly(N)exp(-cN), plus the ordinary memory horizon term. There is no need to invent independent gate faults. N of order log(L/epsilon) then controls a finite requested computation within the earned horizon. The physical schedule includes the actual fixed dwells, ramps and pulses.

Without the strict budget closure, repeated multiplication of error radii would invalidate the claimed arbitrary-length use. This is the central unresolved obligation, together with the live-prefix receiving constants. The source boot is now available from the separately reviewed ordinary factory; it need not be assumed cold on every command.
