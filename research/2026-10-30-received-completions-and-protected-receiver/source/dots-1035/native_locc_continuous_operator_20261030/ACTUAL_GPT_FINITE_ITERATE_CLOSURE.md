# Finite-iterate closure of the actual GPT table, without changing its native payload
2026-10-30. Useful-service interface lemma. This does NOT say one actual SUCCESS implements the closure and does NOT supply a uniform native CP credit.

## Exact source and result

The accepted LOCC payload uses the ordinary lexicographically first strictly improving local GPT table from `tanner_weighted_memory_20261029/EXPLICIT_GPT_TRANSACTION_CIRCUIT.md`, not the separately constructed orbit-minimizing table of another native theorem. That source defines f_h(y) by D_y(f)>0 and sets f_h=0 if no such mask exists. Each nonzero chosen mask strictly decreases the integer global U by at least one; all effects lie in the fixed correction set Q(h) inside its full reserved read footprint R_h.

Hold every other DATA correction fixed and repeatedly apply THIS SAME local rule, always evaluating the current relative syndrome. Only the finitely many energy views meeting Q(h) can change. Let K_h bound their total spectral range. For the source's conservative budgets, at most 2w views each with distance at most w give K_h<=2w^2. Thus after at most M=ceil(K_h)+1 evaluations the rule is at a fixed point. This bound is uniform in N and in the exterior raw syndrome. It does not require global low error density, because strict decrease and the fixed local range are the table's global properties.

The corresponding complete local Alice-check/Bob-correction CPTP map Phi_h satisfies

    Phi_h^(M+1)=Phi_h^M,       (Phi_h^M)^2=Phi_h^M.      (1)

This is an ANALYTIC idempotent closure of the actual channel, not a different one-step physical payload.

## Quantum proof on the full sector degeneracy

Write Pi_a^A and Pi_b^B for the actual joint LOCAL check projectors, including redundant constraints with zero incompatible projectors. One ideal clean transaction has DATA channel

    Phi_h(rho)=sum_(a,b) K_(a,b) rho K_(a,b)^*,
    K_(a,b)=Pi_a^A tensor P_(f_h(a XOR b)) Pi_b^B.

The signs and Pauli ordering are exactly those of the accepted explicit payload. The Pauli maps the complete local check eigenspace b to b+H_h f_h(a XOR b). Alice's a is unchanged. Consequently after the first projective read the sequence of future (a,b) records is DETERMINISTIC given (a,b_initial). Repeated measured reads do not introduce arbitrary new information about logical/gauge degeneracy. Products of Pauli masks may have phases, but these cancel within each Kraus channel and do not change the fixed-sector conclusion.

Strict integer decrease bounds the number of nonidentity masks by K_h. Once f_h=0, the next read projects onto the same already-measured a,b eigenspaces and its correction is identity. Therefore Phi_h acts identically on the image of Phi_h^M, including all coherent degeneracy/reference states. This proves Phi_h^(M+1)=Phi_h^M. Induction gives Phi_h^(M+k)=Phi_h^M for k>=0 and hence (1).

The argument would FAIL for a table allowing nonidentity zero-energy tie moves or for one that stores extra unmeasured control depending on the visit count. Neither is the actual lex-first D_y(f)>0 table. It also would fail if another hub altered the local raw syndrome between evaluations; isolation/competing-work control is a separate service premise.

## What this gives to native service and what it does not

On a mechanically clean, semantically true, actually isolated execution, EVERY successful native Bob terminal implements one evaluation of this same f_h. Clean rollback is DATA identity. Repeated true Alice reads preserve all Alice checks. Thus M successful evaluations suffice to reach the closure image, and the accepted actual finite-SUCCESS path can be concatenated M times at any fixed positive LOAD rates. This yields a finite favorable record with positive full-space lower probability after the appropriate initialization/guard handling; it does not turn intermediate resets into useful successes.

However an arbitrary controller/DATA-correlated initial state does not automatically give scalar clock density times Phi_h^M. A uniform weighted CP credit must represent the physical program/truth conditions and the finite stages or partial-closure decrements. No unavailable physical success counter may simply be inserted into the actual generator. Possible analytic tools are a finite tower of decrements Phi_h^j(V)-Phi_h^(j+1)(V), or an explicitly traced analysis latch in a future-event channel. Their locality, guard interactions and first-order drift still require proof.

This interface avoids modifying or replacing the accepted native payload just to obtain idempotence. It does NOT assert that the existing one-SUCCESS committed-chain credit for an already-idempotent payload applies verbatim. Nor does it solve the clean acquisition, nearby-activity, service-rate/noise-ratio or global energy-coverage obligations of a continuous-noise LOCC theorem.
