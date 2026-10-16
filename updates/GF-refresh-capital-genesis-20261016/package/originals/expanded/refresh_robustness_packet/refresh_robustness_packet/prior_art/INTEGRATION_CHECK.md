# Independent integration checks

Date: 2026-10-16. Read-only mathematical review of the supplied finite-pulse and Schur-resolution artifacts, including the pulse-check script. The script was not executed in this review.

## Finite constant pulse: PASS

For Phi_plus=(|00>+|11>)/sqrt(2) and Phi_minus=(|00>-|11>)/sqrt(2), both H_c and H_0 preserve their span. In that ordered basis,

    H_c = [[0,Omega],[Omega,0]],
    H_0 = [[0,0],[0,J]].

Subtracting J I/2 changes only a global phase. The remaining Hamiltonian squares to (Omega^2+J^2/4) I, so its exponential gives the exact transition probability

    Omega^2/(Omega^2+J^2/4)
      times sin^2(tau sqrt(Omega^2+J^2/4)).

For Omega>0, J=sqrt(5) Omega, tau=pi/Omega, this equals 4/9. With H_c=0 the same-duration identity branch fixes Phi_plus, giving hidden fair-branch average 2/9. The intended H_c-only pulse equals -ZZ, harmless global phase relative to ZZ. H_0 commutes with ZZ, XX and their joint-good projector, so its coarse odd component is exactly zero throughout the original representation.

The supplied script's matrices, normalized Bell states, Rabi frequency, and scalar result agree. Its compressed two-dimensional matrix assertions do not by themselves certify invariant-subspace leakage in a generic model, but invariance here follows directly from the displayed Pauli actions. An additional assertion H_c V=V X and its H_0 analogue would be a harmless strengthening of the check, not a correction needed for this example.

Conclusion: the finite witness rigorously defeats qualification from the original odd-only drift budget and endpoint-equivalent pulse compilation. It does not defeat a bound that charges the actual pulse-induced error, imposes a fixed baseline norm, or preserves the full joint-sector projector along the control path. The construction scales J with Omega; it is not a lower bound at a fixed bounded J as the pulse is made arbitrarily fast.

## Schur resolution bracket: PASS, with label-set scope

Let t=2h mu and r=pq. Before applying the probability cap, the bracket width is

    (Q+t) - [Q+max(0,t-r)] = min(t,r) <= pq.

The cap U=min(1,Q+t) can only reduce the width. The upper bound uses B positive semidefinite and |c^dagger z|<=mu ||z||_1. The lower bound uses z=0 or one nonzero phase-aligned coordinate, with B_jj=1. All these steps are valid at p=0 or q=0 by their direct formulas; no division by pq occurs.

The numerical example is exact: p=q=1/10000 gives Q=19999/100000000, h=9999/100000000, and for mu=1/4 the displayed U=49997/200000000, L=49995/200000000, width=1/100000000 are correct.

For the full binary label set, the maximum magnitude of a nonempty product of eta_a is max_a |eta_a|, since all factors have magnitude at most one and all singleton labels occur. Thus the O(m) arithmetic and O(1) additional-storage claim is valid, with p,q already available and all required multipliers supplied. This is an arithmetic-operation statement, not a floating-point certification or bit-complexity theorem.

Important scope: if only a restricted subset of syndrome labels is physically present, max_a |eta_a| can exceed the actual maximum good-to-bad coherence. It still supplies an upper-bound parameter, but the lower bound obtained by selecting its maximizing singleton is not justified unless that sector exists. Independent Pauli stabilizer generators on the full physical Hilbert space have all joint characters, so the usual full-sector setting is safe. Retaining padded empty sectors gives a conservative enlarged problem rather than the exact lower bound for the original restricted problem.

At absolute tolerance delta>=pq, either endpoint is within delta of the exact value, and U is a certified upper enclosure once arithmetic is exact or outward rounded. For many parents the product bracket must be propagated: the provided product_i(1+p_i q_i/L_i) multiplicative enclosure is valid when every L_i>0. Small per-parent absolute widths do not alone settle relative accuracy of a large product.

Optional elementary tightening: optimize the amplitude of the one-coordinate trial. For r>0 its improvement over Q is t^2/(4r) when t<=2r and t-r otherwise. This costs constant extra arithmetic after mu, and is never worse than max(0,t-r). It is unnecessary for the stated width<=pq guarantee and does not alter the computational prioritization conclusion.

Conclusion: both artifacts are suitable as concrete prioritization gates, with the full-label assumption explicit for the independent-generator lower bracket. Neither supports a novelty or hardware-performance claim by itself.
