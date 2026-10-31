# Independent whole review: backward controlled-observable admission

31 October 2026. Mathematical PASS on `BACKWARD_CONTROLLED_OBSERVABLE_ADMISSION_CANDIDATE.md`, SHA256 `f2d89255727d94d8a4e1a4af08c906e1e39c7fbff6149c40ee72b0f54b4d3a3c`, after reading its entire six sections. This is a separate theorem receipt, not a mutation of the earlier derivative-budget theorem, and does not certify hardware, calibration, new thresholds, priority, or an executable frontend.

## Backward observable and controls

The ideal propagator must include the actual source semigroup AND prescribed ideal local data instruments/controls while omitting K. The source-only generator commutes as a superoperator with these source-blind operations. Each future coefficient of K lies in the same eigenspace of G* with eigenvalue -r. Pulling it backwards through any sequence of unital CP data adjoints preserves that eigenspace and contracts its norm. Thus the e^{-r(s-t)} factor in (2) is valid, also for noncommuting data coefficients, retained local records, and arbitrary correlated input states. It is not an inference from ordinary two-point covariance decay.

The finite-horizon integral is Hermitian and norm-bounded. Differentiation on continuous pieces gives (3) with the displayed MINUS sign. At an instrument, the integral over the zero-length boundary is zero, and the future integral pulls through its adjoint: B_before=C*B_after. B(end)=0. Bounded measurable K and bounded piecewise regular controls suffice for the integral/absolutely-continuous pieces; finitely many instrument interfaces are explicitly handled. There is no physical implementation or numerical solution oracle for B in the theorem.

## Tilt identity and operator constants

For V=I+yB, the source/control/time derivative gives -2yK. The complex Hamiltonian tilt on the identity gives +2yK. Their cancellation leaves iy z*KB-iy zBK, which is Hermitian even when K and B do NOT commute. Its norm is at most 2|y||z|c||B||<=4R²c²/r. Since q=2Rc/r<=1/2, I<=2V, giving the squared-norm rate 8R²c²/r. This is the source of the constants in (6)-(7); no omitted control commutator remains.

At an ideal instrument with retained outcomes, C*V_after=V_before is an equality of effects. An initialized Stinespring representation therefore receives the weighted estimate exactly. It is not an outcome-by-outcome postselection assertion. Arbitrary ideal operation complexity is allowed only within the fixed data/record patch and source-blindness premise. Its actual implementation errors still have to be in the admitted physical model.

## Products, memory, and analytic fault interface

At each time the actual selected patches are disjoint in BOTH source and data. Consequently their weights commute, each generator term acts on one factor, and each allowed instrument is identity on all other active factors. Real outside couplings commute with the current weights but remain present in the physical dilation. This avoids applying a false general Lindblad product rule. Cross-patch instruments, hopping, or shared spectators that violate these relations are NOT included by merely being source-blind.

Inserting the initial weight costs at most 1+q. Removing it at its terminal boundary costs exactly nothing because B(end)=0. Subsequent source reuse, including a different data coupling, retains its state and correlations; no reset appears. At globally adaptive boundaries the old weights are gone, and new fixed compatible supports/uniform operator bounds are required. The explicit local-record restriction prevents hidden control fanout across simultaneously weighted patches.

For finite local systems with initialized Markov fields, bounded coefficients and finitely many instruments give one analytic common jump-history/Stinespring family in selected complex couplings. Its compact-polydisk norm is bounded by the weighted non-TP evolution, including all retained jump and outcome records. The norm applies to arbitrary finite source/data/reference inputs on the initialized-field subspace, not arbitrary incoming field states. Taking the square root of (6), then summing the positive Taylor degrees in each selected variable, yields exactly (R-1)^{-k} and (7). This is an inclusive amplitude premise, not a multiplication of marginal fault probabilities.

## Optimized and short-time bounds

For the radius in (8), q<=1/2, 4R²c²tau/r<=1/2, and 1/(R-1)<=2/R when R>=2. The stated maximum follows. The sharper integral of B in Section 5 is correct: it equals the integral of 2c(1-e^{-r(b-t)})/r. For q<1 the growth coefficient is 2R²c/(1-q), so this variant restores the short-time c*tau scale. The main receipt uses (7); no unimplemented numerical radius/short-time procedure is presumed.

## Consequence and limits

This does remove a real artificial admission cost: source-blind ideal local gate bandwidth, pulse count, and internal measurement count need not enter a variation budget when every actual unwanted coefficient remains in the acquired source decay eigenspace. It does not make ideal hardware free, suppress a source-independent bias, or acquire an unknown source generator. The exact-eigenspace restriction is substantial; the source properly declines an automatic approximate-J extension.

The thermal one-axis example remains an exact classical telegraph logical interface. The isotropic depolarizing example with X/Y/Z source coefficients is genuinely noncommutative but still has an ordinary constant-size exact solver for a single patch. The result earns a local all-selected certificate for networks under the disjoint-patch conditions, not a demonstrated architecture advantage. The earlier exact dephasing benchmark confirms that fixed-diffusion noise does not vanish, and ordinary elimination already provides its leading dissipator.

No load-bearing correction found. Root's separately forthcoming numerical diagnostics are not required by or included as evidence for this proof receipt.
