# Concrete native GPT payload replacement for the committed-credit theorem

2026-10-30. This constructs the **new** idempotent native payload selected by root for this audit. It does not claim that the old lex-first-improving circuit was already idempotent. The old exact instance is preserved as `reviewed_sources/LEX_FIRST_GPT_INSTANCE.md`, SHA-256 `16800ef773d2d3d07d6b94aad92b0d12f83177b3e207dfe88852fc58ab638080`.

This addendum is part of the accepted instance together with the frozen `COMMITTED_CHAIN_CP_CREDIT.md`. It changes the finite table and corresponding finite clock list, not the two-site-Hamiltonian/onsite-reset architecture. It does not establish acquisition service or a native continuous-noise threshold.

## 1. Fixed read and correction resources

Use the already accepted Tanner code/local-energy instance at one fixed admissible Delta. Put w=Delta^2. For each hub h=(sector,vertex), correction masks are f subset Q(h), |Q(h)|=w. Retain exactly the old FULL read footprint

    V_h={v: Q(v) intersects Q(h)},
    R_h=union_(v in V_h) Q(v),
    |V_h|<=2w,    |R_h|<=2w^2.

The raw list consists only of this hub's CSS-sector check bases H_v in those energy views. It has m_h<=2w^2 rows. Duplicate checks can remain; inconsistent outcomes have zero projector. Neither the rule nor tie choices depend on the opposite CSS sector. Every resource in R_h remains part of acquisition/consistency, not merely the eventually selected correction mask.

## 2. Fully specified new truth table

Retain the same precomputed local distance tables

    t_v(z)=min{|r|:H_v r=z}.

For each consistent m_h-bit raw record y and each w-bit mask f in the fixed lexicographic order, compute

    E_y(f)=sum_(v in V_h) t_v(y_v+H_v f).

Set f_new,h(y)=0 if E_y(0)=min_f E_y(f). Otherwise select the lexicographically first mask attaining the minimum. Set f_new,h(y)=0 on inconsistent redundant records. This is a completely finite, deterministic algorithm for every table entry, independent of N and of unknown noise.

The affine update identity E_(y+H_h f)(g)=E_y(f+g) proves that the selected output is an orbit minimum and that a second selected correction is identity. Measurement of the complete local raw record makes the resulting CPTP channel idempotent on all operators. The active set is unchanged: it is precisely the set admitting some improving mask. Every nonidentity move decreases total integer energy by at least one and changes at most 2w unary energy tokens, so the accepted active-density and beta=1/(2w) interfaces still hold. Opposite-sector mixed decrements vanish because the table is sector-local.

## 3. Actual finite native gate-list substitution

Allocate the same types of private hub registers as the old accepted synthesis: Y for the m_h raw bits, A for w output bits, and reusable clean reversible scratch. The algorithm below specifies every gate in the new list.

1. **Raw extraction:** for each listed stabilizer, in the old fixed order, prepare the corresponding Y bit in |+>, apply its controlled single-resource Pauli factors in a fixed resource order, then apply H to that Y bit. This realizes sum_y Pi_y tensor |y> and uses the same commuting checks and full footprint as before.
2. **New table oracle:** iterate through all y0 in binary lexicographic order, and then through output bits j=1,...,w. Whenever f_new,h(y0)_j=1, apply a NOT to A_j controlled on Y=y0. Implement zero-controls by conjugating the relevant Y bits with X. Use the same accepted exact finite multicontrol-NOT/Toffoli decomposition and reusable clean scratch as in the old synthesis; uncompute its scratch after each controlled operation.
3. **Conditional DATA correction:** in fixed resource order over Q(h), apply the sector Pauli on resource q controlled by A_q.
4. Leave Y and A retained in workspace. Do **not** uncompute the extracted raw record after changing DATA. Reset the ENTIRE workspace only through the actual complete terminal/abort instrument.

Thus the new unitary U_h,new has

    <workspace s|U_h,new|0> = K_h,s,
    Phi_h(rho)=sum_y F_new,h(y) Pi_y rho Pi_y F_new,h(y)^dagger.

The extra scratch/output labels can be redundant in this Kraus family; summing the complete terminal instrument is the intended channel. No global minimum decoder or new ideal jump is inserted.

The gate-count estimate remains

    L_h=O(m_h(w+2)+w m_h 2^(m_h)+w),
    n_workspace=O(m_h+w)=O(w^2).

The same bound holds because only which table-controlled NOTs are present has changed. Both the actual list and its length are recomputed from the new table—not reused from the lex-first list.

## 4. Native physical terms after the replacement

Keep the reset-first distinct A and C architecture. Introduce one distinct C position for every prefix of the NEW gate list. For each successive payload U_t, use the same actual-ownership checked Feynman edge:

    g_t ( |C_t><C_(t-1)| tensor U_t tensor |o_h><o_h|_(target) + adjoint ).

A DATA-touching gate uses its one actual resource as target. A hub-only gate may use a fixed designated resource r0 in R_h as the ownership-checked partner, exactly as allowed by the governing generator. Therefore every term acts on at most the hub qudit and one resource qudit. It does not use an all-lock Hamiltonian projector. All workspace/clock registers are included in the grouped hub qudit.

For every new C_t and every resource consistency test, create the same distinct failed-test abort leaf R_(C_t,j). Its reset-first/ownership-retention convention is unchanged: no cleanup from C or attached abort phases before complete workspace reset to Q0. The irreversible complete commitment A_k,W -> C0,0 is unchanged. Terminal and every abort reset retain separately resolved workspace labels at equal rate and reset all the new workspace registers. Hub monitor labels are enlarged to the NEW clock alphabet and remain workspace-blind.

One may pad the new lists with identity hub gates to a common finite length L_max, using the same designated owned partner. Choose common positive hopping, monitor and terminal rates. This makes the committed scalar clock/monitor matrix identical across padded hubs; alternatively solve each of the finitely bounded local matrix types and take the worst constants. Padding has fixed overhead at fixed Delta and does not change Phi_h.

The complete actual C generator used for the resolvent therefore has the NEW path length/clock projectors. No old waiting-tail constant or resolvent is transplanted. The fixed read incidence is unchanged, while local dimension/phase counts and all constants depending on L_h are explicitly recomputed.

## 5. Full-Hilbert and resource consequences

The forest gauge applies to any such finite ownership-checked gate list. On a partial ownership mask it starts each remaining C-path component at identity and uses only resources actually tagged o_h. This remains true for the new table gates, even on arbitrary dirty workspace. The actual full-Hilbert history flags therefore retain the governing commuting/no-creation identities.

The clean input U_h,new|DATA,0> has deterministic raw-syndrome output after the retained-workspace terminal instrument. This supplies the exact good/dirty terminal cross-block statement used by the committed-credit proof. The unitary on dirty workspaces need not be monomial; the accepted raw spectral-envelope reset charge handles it.

All changed quantities are finite functions of the selected fixed local code/Delta. There remain O(N) native grouped sites, bounded-degree hub/resource connectivity, bounded Hamiltonian arity two, onsite complete resets, and fixed positive rates. These facts only instantiate the committed-credit lemma; the still-missing acquisition/cleanup weighted service is not inferred from them.

## Exact governing versions

- Old explicit lex-first GPT instance: `16800ef773d2d3d07d6b94aad92b0d12f83177b3e207dfe88852fc58ab638080`.
- Accepted new orbit-minimizing DATA-rule transfer: `producer-workspace/INDEPENDENT_TRANSFER_REVIEW.md`, `d0402686d92479d5877cc2401e94183abfa7a7420d469e2465505b70cc59c85d`.
- The actual reset-first A/C separation, complete commitment and reset-before-release rules remain those in `producer-workspace/RESULT.md`, whose exact hash is in the current audit's source manifest.

No old payload, source or governing receipt was overwritten.
