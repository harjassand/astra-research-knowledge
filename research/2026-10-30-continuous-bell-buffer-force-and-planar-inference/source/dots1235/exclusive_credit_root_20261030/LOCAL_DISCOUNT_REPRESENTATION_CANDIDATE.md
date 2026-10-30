# Local discount representation and direct conservative tilt
2026-10-30. Root algebraic construction; actual native hypotheses are not yet verified. No continuous LOCC theorem is claimed.

## Exact representation under explicit multiplicative-domain hypotheses
Let V>0. For each i let T_i be UCP, and suppose T_i(V)=V D_i, where D_i>0 commutes V. Suppose the D_i commute pairwise and D_j is in the multiplicative domain of T_i with T_i(D_j)=D_j whenever i!=j. Then

    (product_i T_i)(V)=V product_i D_i.

Proof: pull every already-created D_j through the next map using the multiplicative-domain equality, and induct. This is a statement about the maps on the specified observable, not an assumed identity on all operators.

For a local success credit, D_i=I-t A_i a_i with d_i=V a_i, 0<=A_i a_i<=I. Thus (1-t)I<=D_i<=I. If D_i are bounded-support local factors, the square root and inverse square root of their commuting product are products of local factors, each with norm/inverse norm bounded independently of system size. A local conjugated operator sees only factors whose supports meet its support; factors disjoint from it commute and cancel. Fixed footprint degree gives a constant-size enlarged cone, without paying the exponentially small GLOBAL product lower bound.

## Why exclusion can supply the hypotheses
If two nonidentity credit Kraus families are supported inside orthogonal source sectors P_i P_j=0, then every Kraus of T_i commutes D_j=I-P_j B_j P_j, and T_i fixes D_j. Hence D_j belongs to its multiplicative domain. No commutation of their mutually excluded DATA operations is required.

For nonexclusive pairs the actual normalized decrement a_j, controller coefficient A_j and all semantic/ownership guards must commute EVERY Kraus of T_i. Disjoint correction masks do not suffice. The full read footprint and raw-syndrome influence footprint must be checked. A mathematical current-syndrome dependency cannot be silently replaced by the captured classical programme outside the true guarded source.

The original source-preserving A/C map is compatible with this route. A virtual branch that resets A0 to Q0 can change ACTIVE to FREE and activate a neighboring source; it does not inherit the exclusion proof.

## Direct tilted generator avoids an inverse CP-map order argument
Write W0=V product_i D_i and S=W0^(1/2). The similarity

    L_w(O)=S^(-1) L^*(S O S) S^(-1)

is a completely positive semigroup generator. Let Delta=-L_w(I). If the actual no-LOAD raw inequality establishes Delta>=0, this is subunital. Define

    L_c(O)=L_w(O)+{Delta,O}/2.

It is a conservative GKLS generator: write the transformed generator as sum J'_e† O J'_e + K'† O+O K', then use Delta=-(sum J'_e†J'_e+K'†+K') to obtain the usual loss sum and Hamiltonian from the anti-Hermitian part of K'. Each J'_e=S J_e S^(-1), and K'=S K S^(-1) in the matching convention, has finite support when the preceding local-factor cancellation holds. This construction does NOT require every elementary Delta_e to be positive. Positivity of the total Delta and any service decomposition used subsequently must still be proved.

Conventions: the original Heisenberg generator is J_e† O J_e+K†O+OK. With the displayed S, transformed J'_e=S J_e S^(-1), transformed K'=S K S^(-1), and its adjoint is S^(-1)K†S. These formulas should be used directly rather than mixing Schrödinger and Heisenberg similarities.

## Scientific payoff and unresolved obligations
This route may allow debt and availability to be constructed directly in the conservative tilted process around the credited raw observable. It does not require an idempotent GPT table, order preservation by T inverse, or a new physical reset. It also does not automatically preserve the earlier weighted-debt/exposure witnesses: their zero-debt sectors, finite service paths, value-blindness and guard commutants must be checked after the local tilt. Weak Bob LOAD creates explicit positive activity charges and must be handled, not included in a falsely subunital baseline. A global useful-service inequality and continuous logical lifetime remain open.

## Full weak-LOAD completion does not require subunitality
The algebraic identity constructing L_c is valid even if total Delta is indefinite: the tilted evolution is still completely positive, although no longer subunital. The conservative GKLS generator follows from cancellation of its Hermitian K' part, not positivity of Delta. Accordingly one may retain the full actual weak-LOAD generator if its REAL operator estimate is

 Delta >= useful_service + debt_service - C lambda t sum ACTIVE_h.

That negative part can be paid by an activity witness. The relative-dressing first-order cancellation also requires only Hermitian Delta. Positivity is necessary only where a subunital or killing interpretation is expressly used. The restored LOAD generator must not be bounded as an undifferentiated O(lambda N) source; its raw C lambda t ACTIVE bound and actual negative entry decrement are load-bearing.
