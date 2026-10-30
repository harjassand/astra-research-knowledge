# Earned scientific checkpoint and next scope

The original fixed task is `packet/CONTROL_TASK.md`. This attempt constructs the requested gate in the averaged private-coin channel, with exactly known unit Pauli handles and only first local commutator motion. The proof and reported computations are frozen beside this capsule. Root read the complete proof and executed the lazy finite-parameter generator; a targeted source-exposed proof check is pending. No practical efficiency or historical-priority claim is accepted from a numerical diagnostic.

Each cycle has ten chronological unit-strength signed segments, all duration delta:

B(-sB), C(-sC), B(sB), C(sC), A(-sA), C(-sC), B(-sB), C(sC), B(sB), A(sA),

where sA,sB are fresh fair private signs and sC=sA*sB. Frozen at a common bath time, U=I-4i delta^3 F+O(delta^4), F=Z1 X2. Each handle has zero signed total duration.

In the exact bath interaction frame the three memory Pauli operators are norm-one Lipschitz functions under the supplied ||[H_M,sigma_j]||<=1 promise, with no bound on ||H_M||. Sign averaging eliminates every first-order term and second-order cross-handle term. The same-handle second-order survivor Q acts on memory alone. Writing K=(Q-Q^dagger)/2 gives Q+Q^dagger=-sum_j G_j^2 with G_j=integral f_j(t)S_j(t)dt=O(delta^2); thus Q-K=O(delta^4), K=O(delta^3). Only the ABC third-order character survives; midpoint freezing costs O(delta^4).

The proof controls the full channel variance, not only the mean unitary: for delta<=0.1 it obtains

|| E_s Ad_U - Ad_(exp(-4i delta^3 F) tensor exp(K)) ||_diamond <=10000 delta^4.

Fresh independent cycle signs and a bath fixed independently of those signs permit joint-channel telescoping. The bath factors need not commute with one another. N cycles give <=10000 N delta^4 relative to a data gate tensor an unknown deterministic bath-only unitary. This is uniform over initial DMR correlations but averaged over CURRENT private coins; it is not a guarantee for every realized sign history or a seed-aware output instrument.

Choose dyadic q>=4000/epsilon, delta=1/q, N approximately pi q^3/16. The family has duration O(epsilon^-2), O(epsilon^-3) segments and O(log(1/epsilon)) timing bits. Independent segment-time errors <=epsilon/(4m^2), m=10N, are covered by an interaction-frame switching-time comparison. At epsilon=0.1 the conservative explicit schedule has about 5.53e14 segments and duration 8.43e9, so this is an existence construction with no practical advantage. Existing drift-free five-pulse control remains the appropriate baseline within its different scope.

Exact Pauli coefficient/motion-weight checks and numerical static/moving-bath channel diagnostics are in `checks.txt`; the analytic proof, rather than floating-point residuals, carries the uniform guarantee. The generator stores a lazy schedule rather than materialising the huge word.

An important source correction applies equally to ALL physical continuations: `predecessor_supplement/` contains exact older Astra native sign-group/order-raising and coarse-uniform-gate originals retrieved after the initial packet was frozen. The initial packet omitted those exact originals. Sign projection, same-handle memory cancellation and polynomial unknown-gain compensation are therefore not new general inventions here. Those older constructions use stronger finite-order/static local-regularity expansions; the new claim is the arbitrary-time-dependent first-motion averaged-channel guarantee. Read the supplied originals when assessing the difference.

The common next scientific scope is in `CONTROL_NEXT_SCOPE.md` beside this capsule. It removes exact gain knowledge while keeping the first local-motion promise and original physical operations. Every continuation receives the same question and predecessor sources. No new representation or solution method is prescribed.
