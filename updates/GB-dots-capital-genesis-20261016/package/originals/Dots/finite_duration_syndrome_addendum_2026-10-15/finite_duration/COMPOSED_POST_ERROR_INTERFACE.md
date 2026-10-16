# Limited composition: finite correction latency plus a joint marked post-error

Status: reconstructed conditional interface, 2026-10-15. Uses the audited fixed-duration theorem and the previously verified joint character-instrument theorem. This is deliberately narrower than a finite-duration implementation of every bath-coupled pulse.

## Verdict and bound

The composition closes if the ideal correction circuit is gatewise independent of the persistent bath and the prescribed joint randomized post-error is an atomic channel at completion. Move only the ideal correction to its original start; leave all bath-coupled post-errors and all arbitrary bad gates in physical chronological order.

For the same fixed geometry and deterministic readout T, a sufficient full block budget is

    delta_total <= delta_ideal
                   + 2DN kappa^2 tau (Delta+2tau)
                   + F nu (Delta+2tau)
                   + N kappa tau
                   + kappa p N (Delta+2tau),

where p=delta_coh^2 is the uniform bad-character effect bound. delta_ideal means slow+fast ONLY. All geometry constants must be recomputed for the union of correction, error, randomizer, and ancilla supports.

With x=kappa*tau<=1, Delta=Cb/kappa, and Cb>=1, the added budget is at most

    A0 nu/kappa + B0 kappa*tau + C0 delta_coh^2,
    A0=F(Cb+2), B0=N[2D(Cb+2)+1], C0=N(Cb+2).

These are conservative constants, not physical threshold estimates. For original data-only Pauli noise sigma, use nu<=2sigma and A_sigma=2A0. Ancilla noise is separately included in nu and F.

## 1. Additional exact assumptions

1. Starts remain independent exogenous rate-kappa Poisson streams. Every duration is the same fixed tau, with fixed internal timing. The entire reserved memory/ancilla patch includes the correction circuit, coherent-error support, and detection-complete stabilizer-frame support. Geometrical conflict and external-noise dirtiness are functions of this primitive schedule, independently of quantum labels.
2. Every actually clean attempt starts with fresh reset private ancillas. Its correction circuit uses only data and those ancillas: EACH gate acts as identity on the persistent bath B. It realizes the original completed C_i jointly with every exterior reference. Private correction records are discarded/reset and cannot later recouple through an unmodeled channel.
3. At t=s+tau, after its correction circuit, each geometrically clean completed attempt applies one stipulated joint channel

       T_i(X)=|G_i|^-1 sum_g (g tensor I_B) U_i (g tensor I_B)
                                  X
                                  (g tensor I_B) U_i^dagger (g tensor I_B).

   Its memory support lies in the reserved patch. G_i is a detection-complete subgroup of code stabilizers for the error patch, and the patch contains no logical Pauli. The full joint operator bound ||U_i-I tensor V_i||<=delta_coh holds for every admissible causal physical record and normalized input, with V_i bath-only. B is a fixed finite-dimensional persistent bath; local ancillary resources are fixed finite-dimensional and reset as specified. There is no unbounded retained classical-output register. B can persist across attempts. Fresh frame choices are independent of the current input and U_i; their explicit frame registers are discarded or forever inaccessible. The effective mathematical character labels are not controller-accessible records.
4. This completion-time channel is atomic in the model. It is NOT replaced by a temporally extended sequence of bath-coupled gates interleaved with other bath operations without another theorem. The statement therefore charges finite correction-circuit latency but assumes the same exact post-error primitive as the earlier coherent theorem.
5. Conflicting, externally dirty, or terminally pending gadgets are arbitrary patch-local operations with possible bath coupling. Retain their individual operations in chronological order; they must still constitute a locally finite well-defined circuit. They need no coherent-strength guarantee. Any actual skip/abort is covered by the corresponding bad-attempt flags. External continuous memory-bath interactions, faulty clean syndrome circuits, leaked frames, and noisy timers are excluded.

Bath-only operations between events are allowed and remain in chronological order. Exogenous schedules cannot depend on the initial quantum state or on generated labels. Uniformity over initially correlated logical-bath-reference states is required for the joint-input claim below.

## 2. Why the restricted serialization is legal

Fix the exogenous start/noise schedule and horizon T. Move the ideal correction-circuit gates of each geometrically clean completed attempt back to its start. Each intervening operation either has disjoint reserved data/ancilla support, or would make that attempt conflicting/dirty. A remote joint error may act on the SAME bath B, but the correction gate acts as identity on B and has disjoint memory support. Thus they commute as joint channels even on entangled inputs.

Do NOT move the completion-time T_i. In particular do not exchange two post-error channels merely because their memory patches are disjoint: their shared-bath actions need not commute. Their actual order is preserved. The moved C_i remains before its own T_i. Equal fixed durations imply completion order agrees with start order, though the intervening bad gates and bath-only operations are still retained at their actual times.

Every pending prefix is treated as arbitrary local gates, never completed fictitiously. Hence for fixed T the endpoint channel equals the circuit with exact C_i at clean starts, omitted C_i at bad starts, individual bad gates at physical times, and the clean joint post-errors at their physical completions.

### Why composite bath-independence is insufficient

Gatewise bath independence is substantive. An isolated two-gate echo V,V^dagger can have composite channel Id_memory tensor Id_B. If V is CNOT from a memory qubit to a bath qubit and a remote operation Z_B occurs between the gates, the composite is V^dagger Z_B V=Z_memory Z_B. Moving the isolated identity past that operation loses a memory error. Thus an isolated reduced-memory C, or even a composite joint C tensor Id_B, does not justify serialization when its internal gates touch a bath also used remotely. Our hypotheses exclude this example.

## 3. Joint instruments, arbitrary bad gates, and correctability

For every clean completion the character operators

    U_chi=|G_i|^-1 sum_g chi(g)^* (g tensor I) U_i (g tensor I)

give the actual joint channel as sum_chi Ad_(U_chi). Completeness holds and

    sum_(chi!=0) U_chi^dagger U_chi <= p I, p=delta_coh^2.

This is a uniform FULL joint effect inequality, so it remains valid after arbitrary preceding bad gates and on initially correlated inputs. No reduced-system Pauli-channel substitution is used.

On each Pauli orbit, U_chi equals a representative patch Pauli P_chi times an ordered bath coefficient; take P_0=I. Arbitrary bad-gate Kraus operators are expanded in patch Paulis with auxiliary coefficients. The latter expansion can create sums of several Pauli histories; it need not produce a classical Pauli trajectory. All sums and coefficient orders are retained.

Each expanded term therefore has exact corrections at clean starts, omissions at bad starts, arbitrary patch Paulis at bad gates, and at most one representative Pauli at each nonzero clean character. The skipped-start envelope is the atomic map sat_(S_i) composed with F_i. Its output dominates the unchanged actual support. Zero characters add no support, while nonzero characters cause a bounded birth AT COMPLETION.

On a universally good support record every such expanded history is corrected by the SAME final decoder. Thus each decoded record Kraus operator has logical factor identity, and the aggregate good map is Id_logical tensor Lambda_g with Lambda_g CP trace-nonincreasing. The bad histories are not asserted to form an independent physical rare-fault mixture. This is precisely where the earlier joint-input CP good-map/completion argument is used.

### Actual-record predicate defining the CP good subchannel

Fix L and deterministic T. Let h be the actual exogenous start/noise record, and let chi be the chronological record of the actual character Kraus instruments on its geometrically clean completed attempts. Define B_actual(h,chi) using the literal slow/fast clock flags, the geometry-conflict/dirty/local-terminal flags, and guarded births at the actual completions with chi != 0. For arbitrary bad gadgets this definition includes their full allowed patches and skipped-start saturations, independently of which Pauli terms occur in their Kraus expansions. Let G(h,chi) be the deterministic predicate that this robust coarse process has no macroscopic escape in the required finite history. Use the fixed initialization, guard, connectivity, and escape conventions from the underlying memory certificate.

This is one input-independent predicate on ACTUAL records. It is not defined by a particular initial quantum state, a Pauli expansion coefficient, an auxiliary uniform variable, or a reference Bernoulli coupling. If G holds, the certificate covers EVERY Pauli history admitted by h,chi and every Pauli term of every arbitrary bad-gate Kraus operator. In particular it covers their coherent sums.

For fixed h, use the legitimate sequential joint character instruments and all other physical Kraus records r to define the recovered CP maps K_(h,chi,r). The good subchannel is obtained by summing/integrating these actual physical record maps with the indicator 1_G(h,chi), including the exogenous probability measure of h. A precise notation is

    Good(X) = integral dP(h) sum_(chi,r) 1_G(h,chi)
                         K_(h,chi,r) X K_(h,chi,r)^dagger.

Here K includes the fixed final recovery, with its Kraus index included in r. The expression is CP and trace-nonincreasing because its selection rule is fixed independently of X and selects actual instrument records. Common-decoder correctability makes each selected recovered Kraus operator have logical factor identity, hence Good=Id_logical tensor Lambda_g. The complementary actual-record sum Bad=Gamma-Good is also CP.

The auxiliary coupling in Section 4 is used ONLY to prove, separately for every initial joint state, that Pr_actual(G^c) is bounded by the input-independent reference-process escape estimate. Monotonicity of the robust envelope and flags gives that implication under each coupling. Although the coupling may depend on the input, neither G nor Good depends on that coupling. Never select the Kraus records in Good by whether a reference iid-mark trajectory succeeds. Consequently the uniform probability estimate bounds the effect Bad^*(I), and the existing trace-nonincreasing good-map completion argument supplies the stated joint-input diamond bound.

## 4. Same-parent reference marks with delayed births

Condition on the entire exogenous clock/noise schedule. The geometrically clean completed set is then fixed. The physical causal instrument at each such completion has conditional bad probability at most p for every admissible previous record and state. The uniform bound survives conditioning on independent future primitive increments; the protocol itself does not use those future increments.

A sequential uniform-variable coupling dominates the actual bad characters by iid Bernoulli(p) reference marks attached to their ORIGINAL parent starts. Attach independent unused marks to all other starts too. The reference marked-start field has its independent mark law conditional on the exogenous schedule. Only actual clean completions need the quantum effect bound; marks on bad/pending attempts are analytical overcounting, with their actual operations already charged separately.

Keep the reference birth at s+tau, not at s. Moving a birth backwards across an ideal correction would generally change the support history and is unnecessary. For a target slab [a,a+Delta], the starts that can give marked births in its guard have s in [a-tau,a+Delta] as a conservative window. The marked Poisson expectation is at most

    kappa p N (Delta+tau) <= kappa p N (Delta+2tau).

No selected clean-completion process is asserted Poisson. The rate calculation is for the original independently marked starts BEFORE selecting clean attempts.

The actual quantum-character coupling may depend on the initial joint state; the dominating reference distribution and its probability bound do not. Actual mathematical character labels must not be made available to future controllers unless an equivalent physical instrument and its required hypotheses are separately established.

## 5. Full packets, finite dependence, and endpoint boundary

A primitive packet now includes each start and its independent reference mark. Copy them JOINTLY in torus replay, with the noise primitives. A mark's delayed birth is a deterministic function of its parent start and fixed tau. Extra marked-birth flags enlarge no clock window beyond the conservative [a-2tau,a+Delta+tau] already used for conflicts.

Use the bounded-degree full spacetime dependency graph, fixed before b is chosen. Copy primitive streams once over the union of all required witness windows through their maximum right endpoint. Do not split or independently resample overlapping slab packets. Geometrical clean selection, external dirtiness, and terminal classification can all be reconstructed from the copied windows.

The terminal flag remains LOCAL: candidate starts in [a-tau,a+Delta] intersect [T-tau,T] at guarded locations. Its marginal is at most N kappa tau; it is empty for slabs missing that intersection. There is no global terminal event repeated into every slab. With clocks begun at zero and actually reset ancillas, there are no pre-zero in-flight gadgets. Startup conventions requiring another strip must add their cost explicitly.

## 6. Result and physical tradeoff

Provided the total marginal fits the previously established domination/eroder budget, the existing proof gives, for each deterministic T and one fixed ideal decoder,

    || Gamma_(L,T) - Id_logical tensor Lambda_(L,T) ||_diamond
       <= min(2, A L^4(1+kappa*T) exp(-cL)),

for a suitable CPTP auxiliary/bath map Lambda_(L,T). Here Gamma includes recovered logical output and the fixed finite-dimensional auxiliary/bath output retained under the specified model; tracing that output gives the usual joint-input comparison with Tr_B. The CP bad-map norm bound is uniform in the initial bath state. A conventional logical-only channel follows with fixed independent bath initialization.

This is pointwise in deterministic T. The T-dependent pending classification does not prove a single all-times physical homology event or an adaptive stopping-time bound. Constants and sufficiently large compatible L depend on the enlarged geometry and selected parameters, not on T or bath dimension under the existing finite-dimensional assumptions.

For fixed nu,tau, the coherent term leaves an available budget epsilon_star-C0*delta_coh^2. The rate-dependent pair has minimum 2sqrt(A0 B0 nu tau), provided its minimizing kappa is admissible. Consequently this sufficient recipe needs

    2sqrt(A0 B0 nu tau) + C0 delta_coh^2 < epsilon_star

together with the rate constraints. Failing this inequality does not establish a device impossibility. Nor does the composed theorem establish a finite-duration physical realization of the atomic joint twirl, reservoir engineering, leakage control, finite autonomous timing resources, or robustness to arbitrary continuous coherent noise.
