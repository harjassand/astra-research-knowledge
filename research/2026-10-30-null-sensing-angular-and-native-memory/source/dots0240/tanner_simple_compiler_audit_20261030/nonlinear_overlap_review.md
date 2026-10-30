# Focused independent review: nonlinear Tanner tokens and overlapping decrements

2026-10-30. This is a targeted audit of the NEW bridge in `LINEAR_EXPONENT_FINITE_CONTROLLER.md`, not a repeat audit of GPT density, the original quantum boundary theorem, or the accepted simple-compiler theorem. Inputs and exact hashes are recorded below. No source was edited.

## Result

**The nonlinear unary-token map does not obstruct the required idempotence or bounded-patch inequalities.** The new bridge is valid with the explicit raw-sector formulation and completion lemma below. No new expansion or token-only persistence premise is needed.

A precision matters: `d_h=(I-Phi_h^*)V` is generally a function of FULL RAW syndrome and the auxiliary flags, not just of unary energy-token occupation. A monomial map of raw sectors need not preserve the coarser algebra generated only by energy tokens. Equal-energy raw records can have different correction responses. All diagonal algebra, source-sector, and four-term calculations below therefore use the full raw-syndrome/auxiliary-label algebra. The manuscript's statement that raw monomiality makes the token update deterministic is valid **from a fixed raw source sector**, not from a token configuration alone.

## 1. The new local rule is idempotent and retains exactly the active set

Fix a hub h. Its allowed masks are all subsets of its fixed support Q(h), hence form an additive binary group. Its complete raw read contains every local view whose energy can change under such a mask. Consequently the finite orbit of a read record y is invariant under every allowed correction, and minimizing the affected energy minimizes total energy within that orbit (the omitted terms are constant).

The rule is:

- if the zero mask is any minimum, select identity;
- otherwise select one fixed minimum mask.

A strictly improving mask exists if and only if the zero mask is not a minimum. Thus the active set is unchanged from the existence-based GPT density statement. A nonidentity selected move reduces integer total energy by at least one. The accepted bound on the number of changed unary tokens is at most 2|f|<=2 Delta^2, giving the same positive surplus beta.

After one application, each measured raw input sector has moved to a minimum raw sector. The channel has already removed coherences between distinct local measured records. On the second application it measures the resulting block-diagonal minimum record and applies identity. Thus Phi_h^2=Phi_h on all operators. The rule must keep identity on EVERY already minimal record, including ties; moving between equal-energy minima would invalidate the inactive-payer argument below and need not be idempotent.

The token full-animal lemma gives d_h>=0. Idempotence then gives exactly

    Phi_h^* d_h=0,    Delta_h d_h=-d_h,
    Delta_h=Phi_h^*-I.

These identities do not require d_h to be token-only.

## 2. Deterministic raw updates and a fixed overlap patch

Let y denote a full raw-syndrome sector, with arbitrary fixed auxiliary flag configuration c. Let H_h(y) be the deterministic raw target under the selected conditional Pauli at h. On any raw-diagonal observable A,

    (Phi_h^* A)(y,c)=A(H_h(y),c).

The hypothetical channels leave the gauge flags fixed. If h is inactive at y, H_h(y)=y exactly, not merely at the level of total energy or token occupation.

For two overlapping hubs h,j, choose a fixed connected animal-graph patch P_hj containing:

1. every energy token that could change under ANY allowed mask on Q(h) or Q(j), over all raw source records;
2. bounded dummy paths joining those token footprints through the complete read-footprint overlap.

Such a patch exists with uniformly bounded size p. The accepted unary graph attaches affected-view tokens to relevant data dummies, and full read footprints are cliques in the DATA graph. Overlapping read footprints therefore give a bounded connected union. If desired its finitely many fixed paths can be added before choosing graph constants. Use the full possible token footprint, not merely the actual changed set at the source: an equal-energy raw change can change h's chosen correction and hence which h tokens change.

The union is still bounded at fixed Delta, even though the sharper per-orbit variable-token bound uses only 2|Z| tokens. All actual token changes in the four raw states

    y, H_j(y), H_h(y), H_h(H_j(y))

lie in P_hj. Flags do not change. Write p for a common upper bound on these patch cardinalities.

## 3. Explicit paying-move proof of the overlap inequality

For one animal A put v_A(y,c)=f_A(y,c). The contribution of A to Delta_j d_h is

    v_A(H_j y)-v_A(H_h H_j y)-v_A(y)+v_A(H_h y).       (1)

Each of the four values differs from v_A(y) by a ratio between theta^p and theta^(-p), because only token vertices in P_hj can differ. Expression (1) vanishes if A misses P_hj. Hence

    |Delta_j d_h(y,c)|
       <=4 theta^(-p) sum_{A:A meets P_hj} f_A(y,c).  (2)

If j is inactive at y, its complete raw update is the identity. The two pairs in (1) cancel EXACTLY, so Delta_j d_h(y,c)=0. This remains true even though another raw record with the same energy tokens could have a different d_h.

If j is active, its actual token-change set D_j(y) is nonempty, lies in P_hj, and has the accepted strict removal surplus. The reviewed per-move bound therefore gives

    d_j(y,c)>=q sum_{B connected:D_j(y) subset B} f_B(y,c),
    q=(1-theta)/2>0.                                (3)

For every A in (2), set B=A union P_hj. It is connected, contains D_j(y), adds at most p vertices, and obeys

    f_B(y,c)>=theta^(u p) f_A(y,c),    u=1-c_exp>0.

(The exponent parameter c_exp is distinct from the auxiliary flag configuration c.) At most 2^p source animals A yield a fixed B. Therefore

    sum_{A:A meets P_hj} f_A(y,c)
       <=2^p theta^(-u p)
            sum_{B:D_j(y) subset B} f_B(y,c).

Combining (2) and (3) proves the uniform bound

    |Delta_j d_h|<=C d_j,
    C=4 q^(-1) 2^p theta^(-(1+u)p).                 (4)

Both sides are full-raw-diagonal operators, so the sectorwise bound is exactly the claimed Loewner/absolute-value bound. Swap h and j to obtain the stronger absolute bound |Delta_h d_j|<=C d_h, hence in particular the one-sided inequality Delta_h d_j<=C d_h used by geometric blocker service.

No N-dependent factor enters. There is one bounded-patch completion per source animal and a bounded preimage count. This proof applies to the full untruncated animal sum and works with arbitrary spectator flag-token occupation. For two hubs in the SAME CSS sector it applies exactly as written. For opposite-sector hubs, the actual GPT table reads only its own sector: EXPLICIT_GPT_TRANSACTION_CIRCUIT.md specifies one hub per (sector, vertex) and a basis of the local sector check space. An opposite-sector correction leaves that entire raw record, all its energy tokens, and its selected mask unchanged; it also leaves the gauge flags unchanged. Thus Delta_j d_h=0 exactly for opposite-sector h,j. This is what permits summing the two sector potentials without trying to charge an animal in one graph to a payer in the other graph. Arbitrary cross-sector-dependent tie-breaking would need a separate argument and is not being imported. For disjoint full read supports one uses the original exact channel/clock commutator cancellation; there is no need to claim that distant animal mixed differences vanish.

## 4. What equal-energy raw changes do and do not invalidate

The accepted Tanner receipt correctly rejects token-only candidate persistence: identical local energy can conceal distinct raw cosets with different responses to a proposed mask. That observation does not refute (4), for two separate reasons:

- An inactive selected channel makes NO raw correction, by the identity-on-minimum rule. It cannot conceal a nontrivial equal-energy transition while having d_j=0.
- An active selected channel makes a strict total-energy decrease and therefore has the positive actual token charge (3), even if some individual local views change raw record at equal energy. The fixed P_hj includes the full possible read/update footprint, so changes of h's chosen mask are bounded and paid.

The unsafe shortcut would be to identify d_h with a token-only function, or to infer that no token change implies no change of every raw-dependent correction decision under arbitrary errors. The argument above makes neither inference.

## 5. Full-Hilbert monomial wording

The XOR/controlled-Pauli unitary normalizes the FULL raw-syndrome/auxiliary-label diagonal algebra. A gauged reset maps each raw/label source sector to one raw/label target sector. Consequently each source has a definite unary-token target and the actual raw bad-reset per-move charge can be evaluated sectorwise. This does not imply an autonomous transition law on energy-token configurations, and none is required.

For the other compiler interfaces the same fine algebra is sufficient: zero-drive raw reset/credit action preserves raw diagonality; the basin projector is raw-syndrome/flag diagonal; and raw stabilizer covariance ensures the dressed observable remains raw-syndrome diagonal. Those observations explain why nonlinear tokenization is compatible with the already accepted proof, but this focused note does not re-audit its CP-similarity or killed-process estimates.

## Exact source hashes

- `LINEAR_EXPONENT_FINITE_CONTROLLER.md`: `262ad8345f510e45f761703e8cf5a1dc83d6b1bd9e331daf502344e0e56ab858`
- `independent_tanner_transfer_audit_20261030/INDEPENDENT_REVIEW.md`: `29cb917e28daf6965d1e95036d4ae672ec33174f08afbca986e638fa0221693e`
- Both the original and reviewed-copy `UNARY_ENERGY_LIFT.md`: `ccc4cc644ccc9923fe64e3cd336a12414847d015baeef78b2c6d11058e418995`
- `simple_compiler_whole_audit_20261030/WHOLE_RECEIPT.md`: `4d699d76e1e0585f5c93b78b93c7054dd7e05eb8c46421d48037a1efbf7f04a8`
- Sector-local raw-table definition in `tanner_weighted_memory_20261029/EXPLICIT_GPT_TRANSACTION_CIRCUIT.md`: `16800ef773d2d3d07d6b94aad92b0d12f83177b3e207dfe88852fc58ab638080` (read only for the new bridge's actual cross-sector decision scope).
