# Independent audit: one fixed shared noisy GPT baseline
2026-10-30. Reviewer: `producer-workspace/review_simple_compiler`.

## Verdict
**Scoped PASS for the modified deterministic GPT contract and its conditional charge-once positive-record extension.** An arbitrary fixed, globally inconsistent but locally well-formed baseline can be treated as static sparse defects of a single shared energy. The altered finite-work, active-density, physical-window, rooted D0/D1 and initial-defect charging arguments are valid with changed fixed constants.

This does **not** certify physical baseline generation, reliable storage/access, an eventual Pauli-frame switch, or a native initialization/memory theorem. It is conditional on one genuinely shared, time-independent baseline and the existing native positive-record fault/service bounds for the resulting actual enlarged interface. The simpler global-energy alternative being developed separately is not part of this frozen-source receipt.

No substantive counterexample was found. One implicit localization convention must be made explicit: on a selected execution component, restrict **both** e and eta to that component. A globally retained eta would add unrelated baseline energy and invalidate the local estimates. The source's repeated references to “B restricted to the component” support the intended convention; the precise definition is given in section 3 below.

## Frozen source and dependencies
Author-confirmed frozen source:
`producer-workspace/PERSISTENT_BASELINE_GPT_ANALYSIS.md`

SHA-256: `74a81ece8148f2b8b81f6b30869050a53ff7ae1c65062e3383d018a7cff04b17`.

The exact source is copied in `reviewed_sources/`. I read the governing `INTEGER_ENERGY_D0_D1.md`, explicit GPT finite circuit, accepted integrated Tanner receipt, original one-backward-chain contract, and initial-seed slab. Their exact hashes are in `SOURCE_SHA256.txt`. Tanner expansion, code rate/distance and the previously reviewed native positive-record theorem are imported, not re-proved here.

## 1. The biased energy is defined without a globally valid syndrome
For each potential view v, the chosen local check basis H_v is full row rank and has the stated local-code kernel. Thus every local bit string z_v has a preimage, and its minimum-weight preimage t_v(z_v) is a finite integer in [0,w]. No global consistency of the concatenation is required to define

    U_eta(e)=sum_v t_v(H_v e+eta_v).

Let B={v:eta_v!=0}, and D=union_{v in B} Q(v). Every reader of a potential view uses the same eta_v. This is exactly the assumption that provides a single energy rather than incompatible owner-specific energies.

For any f, adding its restriction to a minimum representative and reversing the comparison proves

    |U_eta(e+f)-U_eta(e)|<=2|f|.

The factor two is the exact incidence of a DATA bit in two sector energy views. Also

    |U_eta(e)-U(e)|<=w|B|,
    U_eta(e)<=2|e|+w|B|.

Both energies are functions of the full raw sector syndrome and remain invariant under same-syndrome or stabilizer replacements. The fixed eta does not alter that invariance.

The old table's incompatible-concatenation no-op rule is safe. On a compatible input, its computed affected-view energy difference is exactly the U_eta difference, regardless of whether the complete baseline is globally valid; outside affected views the energy is unchanged. On an incompatible input it does nothing. One may alternatively define all entries by direct local energy minimization. Strict decrease, not idempotence, is sufficient for this deterministic contract. Composing with an idempotent native credit would still require the intended orbit-minimizing table rather than silently inheriting an older lex-first table.

## 2. Active density and finite work
Only a bounded number b of candidate hubs can read a given defective view. Outside that neighborhood the complete raw input tuple agrees with the ordinary GPT tuple. Thus

    g_eta(e)>=g_0(e)-b|B|
            >=kappa U(e)-b|B|
            >=kappa U_eta(e)-(kappa w+b)|B|.

This remains valid with the incompatible-input no-op rule. The small-error/radius premise is the same as in the governing ordinary theorem. Confinement gives

    U_eta(e)>=h|e|_reduced-w|B|

when that representative is in the safe radius. For a restricted error of small, but not necessarily reduced, weight, use its no-heavier stabilizer representative for density and then restore locality through the original error plus D. No claim that the reducing representative stays in the original support is needed.

Every accepted correction decreases the nonnegative integer U_eta by at least one. With no new faults its total count is at most `2|e0|+w|B|`, and support mass is at most w times that count. Under the stated radius premise, a terminal no-active-hub state satisfies `U(e_final)<=b|B|/kappa`, hence the claimed O(|B|) reduced residual. This is a finite-work/residual statement, not a decoder for an arbitrary invalid global syndrome.

## 3. Exact localization convention
Use the full-read, energy-view, raw-check and fault-support clique graph. Include D in every execution/future-support set. Each defective Q(v) is connected and is contained wholly in one component.

For a union W of selected components define

    B_W={v in B : Q(v) is contained in W},
    eta_W(v)=eta_v for v in B_W, and 0 otherwise.

The restricted trajectory is `(e restricted to W, eta_W)`. Its energy counts only the views incident to its error or B_W; all other terms are zero. Because an energy view is a clique, it cannot simultaneously meet the relevant support in two distinct components. Full read cliques give the same accepted local decisions after restriction. Candidate locality is through the current error **or** D; a positive biased energy may be caused solely by a defective view.

All componentwise x_i, b_i and confinement estimates in the source must be read this way. In particular, after discarding a whole future component one discards its baseline defects too. Nonnegative energy additivity then justifies the nested-set contraction. Keeping global eta in x_i would be wrong, but is neither necessary nor the intended construction.

## 4. D0 and the physical-window inequality
In a localized component, fault support mass Q increases U_eta by at most 2Q, and the initial biased energy is at most `2|E_in|+w b_K`. Hence the accepted-move count is at most

    2|E_in intersect K|+w b_K+2Q(K).

Adding incoming support, bad-event support, correction supports and D gives

    |execution support| <= (1+2w)(|E_in|+Q)+(w+w^2)b_K.

Appending a sectorwise minimum-syndrome endpoint representative changes no biased decision and costs at most the usual factor two, by componentwise same-syndrome replacement. Thus the source's safe

    C_seed,eta=2(1+3w+w^2)

indeed yields `|K|<=C_seed,eta(|E_in intersect K|+Q(K)+b_K)`. It is unconditional: no good-service or small-error premise is used in D0 itself.

For the window proof, discard candidates whose full affected-view neighborhood meets B and pack the remaining full raw dependencies. Their number is at least `kappa_p U_eta,start-C_eta b_W`. The baseline is fixed, so these raw inputs persist until an actual move/fault changes them or their own hub is correctly evaluated. Any accepted biased move has strict U_eta decrease and resolves at most the same fixed number C_res of packed candidates. The no-op rule cannot block an unchanged packed uncorrupted candidate, since its original compatible raw input remains present.

The source's two counting inequalities therefore hold with the actual good-service miss majorant M:

    kappa_p U_eta,start <= C_res D_U+dQ+M+C_eta b_W,
    U_eta,end <= U_eta,start-D_U+2Q.

Eliminating D_U gives the claimed contraction with an additive static-defect term. This statement is conditional on the real evaluator reading the shared baseline as part of its complete dependencies; a frozen mathematical coefficient is not evidence of fault-tolerant physical access.

## 5. Rooted D1 constants and endpoint alternative
For a restricted suffix, let x be its initial biased energy, y its final biased energy, D_U the accepted decrease, q its fault mass and b its static defects. Confinement and finite work give

    |E_final| <= y/h+w b/h,
    D_U <= x-y+2q.

With `C0=max(w,1/h)`, and adding the explicit D footprint of size at most wb,

    |W| <= C0 x+(2C0+1)q+w(1+1/h)b.

This verifies the displayed suffix constants. The usual same-syndrome virtual start remains valid because eta is fixed and the entire raw syndrome trajectory, not merely its scalar energy, is preserved.

At the endpoint, write e_R for the final representative weight in selected components and b_R for their defects. If `w b_R>=h e_R/2`, then

    |W_R|<=e_R+w b_R<=(2w/h+w)b_R.

This is an essential static-density terminal alternative. Without it, the ordinary lower bound on final energy would fail near baseline defects.

Otherwise `x_R>=h e_R/2>=h|S|/2`. If no earlier slice has x_i at most a sufficiently large fixed multiple of `Q_suffix+M_i+b_i`, the window inequality contracts by a fixed theta<1. The initial bound `x_0<=4|W_0|` is correct: `2|E_0|<=2|W_0|`, and `w b_0<=2|W_0|` because every full defective view lies in W_0 and each DATA bit belongs to only two views. Hence

    |W_0| >= (h/8) theta^(-R)|S|.

Enlargement to original execution components meeting S preserves rooting and permits the actual incoming-support D0 charge. Choose R after the changed C_seed,eta so the ancestor expansion factor exceeds one. This establishes the required modified D1, with a fresh `Q+M+b` alternative and an ancestral D0 alternative containing `Q+b`.

## 6. Why the static defect set is paid once
The deterministic backward recursion is precise:
- at a first bad root or an ancestral D0 slice, stop if `Q(W)+b_W>=|W|/(2 C_seed,eta)`;
- otherwise incoming representative support has density at least `1/(2 C_seed,eta)` and supplies the preceding target;
- stop at any modified D1 fresh alternative `|W|<=C_bad(Q+M+b_W)`.

Each nonterminal ancestral slice grows geometrically backward, exactly as in the accepted one-chain proof. Only the terminal slice lacks that expansion, and target containment supplies the same bounded ratio to its successor. Thus the entire connected spacetime certificate volume is at most K_vol times the size of its one terminal slice. Adding static D to the deterministic support sets does not alter this proof of geometric volume control.

The terminal probability event uses **one** value b_W of the actual initial defect set. It is not the sum of its copies over the chain and is not treated as newly sampled noise at each time. If the initial residual is empty, the chain cannot continue past initialization without a terminal Q/static-density charge. A separate initial residual is handled by the reviewed seed-slab extension.

For a fixed W of M sites, suppose the native positive-record estimate gives

    E z^(Q+M_miss) <= rho_native(z)^M,

and a common initial baseline-defect majorant gives

    E z^b_W <= [1+p0(z^m-1)]^(cM),

where m,c absorb bounded duplication and incidence. The latter follows by expanding the generating function under local-stochastic initial bit errors; independence of those bits is unnecessary.

Even with arbitrary dependence between initial and later records, Cauchy-Schwarz and exponential Markov yield, for a terminal density a>0,

    Pr[Q+M_miss+b_W>=aM]
      <= { z^(-a) rho_native(z^2)^(1/2)
           [1+p0(z^(2m)-1)]^(c/2) }^M.

Choose fixed z large, then the native miss/fault parameters and p0 sufficiently small. This terminal base can be made small enough to pay the unchanged bounded-degree spacetime-animal entropy. Reuse of the same defect set at another possible root time creates correlations, but a union bound over root times does not require independence. Therefore the usual conditional `C N(1+t) exp(-cN)` envelope survives a linear cutoff, with changed constants.

This probability conclusion requires a **positive initial record/majorant common to all Pauli coefficient branches**, or an actual classical baseline error set. A branch-dependent fictitious eta cannot be inserted into a physical probability bound. Uniform future native estimates on the allowed initialized joint states and fixed logical-independent initialization are likewise required for any eventual reference-level channel claim. These are part of the missing physical initialization contract, not supplied by the deterministic energy calculation.

## 7. Regression and the actual failure mode
`check_biased_energy.py` independently tests a four-bit ring with four two-bit potential views, each bit in exactly two views and each local parity basis full row rank. It checks 4,096 Lipschitz identities, 1,024 local orbit-minimizer idempotence cases, finite work for all states, and 128 source states with globally impossible odd-parity baselines. All pass. This tests the biased-energy algebra, not Tanner expansion.

The inconsistent-copy obstruction is real and reproduced: two owners using targets 0 and 1 for one DATA bit yield the no-noise sequence 0,1,0,1,0,1,0. Each believes its own operation decreases its own energy, but no common decreasing energy exists. Independent corrupted per-hub copies therefore cannot be relabeled as a shared eta without a consistency mechanism.

## Remaining boundary
The receipt accepts a fixed shared baseline as a mathematical input, including its globally invalid concatenations. It does not provide:
1. a physical initial syndrome-record instrument with a common sparse mismatch certificate;
2. reliable static storage or a theorem for drifting baseline bits;
3. bounded-range shared access incorporated into actual lock/read/support budgets;
4. a charged, logically consistent final Pauli-frame reconciliation or noisy retrieval.

Those obligations are load-bearing. No conditional charge-once estimate is promoted here to an implemented native preparation-latency or unknown-coset memory theorem.
