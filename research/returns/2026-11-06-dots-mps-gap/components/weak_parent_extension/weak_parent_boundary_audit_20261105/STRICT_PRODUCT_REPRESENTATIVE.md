# Independent audit: the fixed-block criterion has a strict-product representative

2026-11-05. This note independently verifies the exact representative reduction proposed in `PRIORITY_AND_GNS_AUDIT.md`. The reduction is algebraic. The stated periodic/GNS consequence is explicitly conditional on accepting the separate provisional finite-range proper-parent GNS candidate, whose unchanged proof is included under `dependencies/`.

## Verdict

The reduction is valid, with the normalization 1/(k-1) and all one-site translates retained. No spatial blocking, energy rescaling, subsequence of ring sizes, or assumption that the shifted two-site term is positive is needed.

It identifies the **periodic Hamiltonian and infinite dynamics**, not the open Hamiltonians or finite-level LTI SDPs. Consequently it adds a conditional GNS interpretation to the already established original-interaction LTI limit; it does not replace the original-h reset argument.

## 1. Exact assumptions and positivity

Let h>=0 be a nonzero two-site interaction on a finite-dimensional site with distinguished vector |0>, with h|00>=0. Let k>=2, X=X*, and c>0 satisfy the fixed-block condition

    B_k = sum_(i=1)^(k-1) h_(i,i+1) + X_1-X_k
        >= c Q_k,
    Q_k = I-|0^k><0^k|.

Define a range-k interaction on the original unblocked lattice by

    b = B_k/(k-1),     a=c/(k-1).

The expectation of B_k in |0^k> is zero: each h term vanishes and the two X expectations cancel. Since B_k is positive, B_k|0^k>=0. The coercive inequality therefore gives

    b>=a Q_k,    ker b=span{|0^k>}.

It also implies X|0> is proportional to |0>. Indeed B_k|0^k>=0 reduces to (X_1-X_k)|0^k>=0; the two distinct-site components orthogonal to the vacuum are orthogonal, so each vanishes. This is a consequence, not an extra assumption.

The norm is bounded by ||b||<=(k-1)^(-1)[(k-1)||h||+2||X||]. The individual two-site expression h+X tensor I-I tensor X can be indefinite; only B_k is required to be positive.

## 2. Proper-parent and open-gap properties of b

For an L-site open interval, L>=k, define the natural range-k open Hamiltonian

    H_b,L^open = sum_(x=1)^(L-k+1) tau_x(b).

Every site belongs to at least one translated block. The commuting diagonal projectors Q_[x,x+k-1] therefore satisfy

    sum_x Q_[x,x+k-1] >= I-|0^L><0^L|.

Consequently

    H_b,L^open >= a (I-|0^L><0^L|).

The kernel is exactly the product vacuum, and the positive open gap is uniformly at least a=c/(k-1). These facts are direct operator inequalities, not an invocation of an unproved original-h open gap.

The tensor A^0=1, A^s=0 for s!=0 has bond dimension D=1, primitive canonical transfer on the one-dimensional virtual algebra, and faithful invariant scalar density. Its boundary space on every block is precisely the vacuum line. Thus b satisfies the finite-range proper-parent hypotheses in the separate GNS candidate. It need not be a nearest-neighbor interaction; that candidate explicitly allows range r=k.

## 3. Exact periodic normalization

For a ring with N>=k, let tau_x cyclically translate by one physical site and sum over every x=1,...,N. Then

    sum_x tau_x(b)
      = 1/(k-1) sum_x sum_(i=1)^(k-1) h_(x+i-1,x+i)
          +1/(k-1) sum_x (X_x-X_(x+k-1))
      = sum_(j=1)^N h_(j,j+1).

Every original bond occurs exactly k-1 times. The two onsite sums are equal after cyclic reindexing. Hence

    H_b,N^per = H_h,N^per

as full operators, at every compatible ring length N>=k, not just asymptotically or on the vacuum sector. Original physical sites and energy units are unchanged. In particular the periodic gaps agree exactly.

The periodic vacuum is unique: the sum of the block vacuum-complement projectors dominates the full-ring vacuum-complement. Thus all large periodic chains meet the unique-ground requirement as well.

## 4. Open Hamiltonians are different

Let J=L-k+1. The exact open representative is

    H_b,L^open = 1/(k-1) sum_(j=1)^(L-1) w_j h_(j,j+1)
                 +1/(k-1) sum_(x=1)^J (X_x-X_(x+k-1)),

where

    w_j=max(0, min(j,J)-max(1,j-k+2)+1).

Interior bonds have weight k-1; weights taper at the ends. The onsite difference is equivalently the first k-1 X terms minus the last k-1 X terms, with overlaps canceling. Thus H_b,L^open-H_h,L^open is a uniformly bounded operator supported near the two physical boundaries, for fixed k,h,X.

It is generally nonzero. A bounded boundary perturbation can change a uniform open gap into a closing open gap; the explicit qutrit example in `COBOUNDARY_REPAIR.md` demonstrates exactly why open equality must not be asserted. Positivity of b does not imply positivity of every original onsite-shifted two-site term or every open sum of that shifted term.

## 5. Exact equality of infinite derivations and GNS Hamiltonians

For a local observable A, use the same derivation convention for both interactions, for example

    delta_h(A)=i sum_j [h_j,A].

Only finitely many commutators are nonzero. Thus the following reindexing is legitimate without a convergence or boundary-limit ambiguity:

    delta_b(A)
      = i/(k-1) sum_x sum_(i=1)^(k-1) [h_(x+i-1),A]
          + i/(k-1) sum_x [X_x-X_(x+k-1),A]
      = delta_h(A).

Finite-range interactions generate unique quasi-local dynamics agreeing with these local derivations, so the infinite automorphism groups coincide. Both leave the same product vacuum state invariant. In its GNS representation, the implementing unitary group is uniquely fixed by

    U_t pi(A)Omega = pi(alpha_t(A))Omega,
    U_t Omega=Omega.

Therefore the self-adjoint GNS generators are the same operator, with the same zero normalization, and their GNS gaps agree. There is no undetermined additive energy shift: both generators annihilate the cyclic vacuum vector.

## 6. Precise conditional consequence

The separately reviewed candidate `dependencies/PROPER_PARENT_GNS_CANDIDATE.md` explicitly treats positive **finite-range** proper primitive-MPS parents. Applying it to b with D=1 and range k gives, if that provisional result is accepted,

    lim_N gap(H_b,N^per) = gap_GNS(b).

By Sections 3 and 5,

    lim_N Delta_N(h) = gap_GNS(h).

Combining with the original-h fixed-block reset theorem in `COBOUNDARY_REPAIR.md` then gives

    lim_n gamma_n(h) = gap_GNS(h),
    gamma_n(h) >= Delta_n(h)-O(n^(-1/2)).

The quantitative lower comparison remains the original reset bound. The separate GNS candidate's finite-range reverse comparison can also be transferred to the same periodic spectra, but it is a different estimate with its own provisional review status.

This is an exact reduction of the whole fixed-block criterion class, including the all-species noncritical native PVBS specialization. It is not a theorem for arbitrary weak parents, not a proof that an appropriate X,k,c always exist, and not equality of gamma_n(h) with a finite-level hierarchy built from b. The original open gaps can remain entirely different.

The class is therefore weak-parent in the chosen nearest-neighbor decomposition but has a strict-product finite-range representative of the **same periodic and infinite dynamics**. This distinction should remain explicit in positioning any result.

## 7. Independent checks and provenance

`check_block_representative.py` tests the full operator identities, positive representative, open boundary-weight formula, and local derivation equality in three cases:

1. the closing-open-gap qutrit interaction with k=2;
2. a native repeated-anisotropy two-species PVBS interaction requiring k=3;
3. a diagonal model with B_3 positive but the individual shifted two-site interaction indefinite, checking that no extra two-site positivity assumption entered.

These finite-matrix tests support the exact counting argument; they are not the proof. The separate GNS candidate is included unchanged with its source hash in `UPDATE_PROVENANCE.json`. The priority audit is also preserved unchanged; its opening statement about being outside a frozen manifest describes the earlier v1 packet, not this updated v2 manifest.
