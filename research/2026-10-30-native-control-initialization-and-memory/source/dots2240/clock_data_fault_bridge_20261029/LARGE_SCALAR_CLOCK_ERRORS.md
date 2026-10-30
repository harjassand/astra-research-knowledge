# Large scalar clock errors: exact data semantics and bounded-deadline completion

2026-10-29, 21:32 UTC. Companion to DEADLINE_CELL_INSTRUMENT.md. This is a calibration-class contract, not a fully autonomous threshold or a novelty claim over ordinary Feynman-clock/adiabatic techniques.

## Exact class that is harmless to channel direction

For the bundled single-shot cell, allow arbitrary measurable real g(t) with

    0<g_min<=g(t)<=g_max,

and a clock Hamiltonian diagonal with value d_0(t) on ready and a common value d_1(t) on **all** excited Kraus labels, with |d_1-d_0|<=D. Also allow kappa(t) in[kappa_min,kappa_max], with kappa_min>0. These deviations need not be small. The clean Stinespring isometry remains invariant and the no-jump equations, after removing the common d_0 phase, are exactly

    a'=-ig(t)b,
    b'=-ig(t)a-[kappa(t)/2+i delta(t)]b.

They are clock-only scalar equations. Therefore the SUCCESS/MISS instrument in the companion remains exact with the resulting a,b,q. Large scalar rate/detuning deviations change the completion probability, not the completed channel Phi. No derivatives of the controls are required.

**Important restriction:** a direct multi-Kraus bundle does NOT generally tolerate distinct large detunings for its individual excited Kraus labels. Those can leave the intended Stinespring image and bias channel branches. Such errors must be small physical faults, or avoided by using an ordinary unitary Stinespring workspace and a separate Feynman clock. Arbitrary clock-diagonal detunings are harmless in that latter scalar-history-clock representation.

Static complex hopping phases can be removed by fixed clock basis phases. Arbitrarily fast complex phase/sign modulation is not covered: it can average away the drive and destroy uniform completion despite a pointwise nonzero magnitude.

## Explicit uniform two-level completion bound

Set

    T=1/[4(kappa_max+g_max+D)],
    M_b=kappa_max/2+D,
    I_*=min{T/16, g_min^2 T^3/[8(4+g_max^2 T^2+M_b T)^2]},
    c=kappa_min I_*>0.

For EVERY normalized initial two-level clock vector and EVERY measurable allowed control waveform, a no-emission interval of length T loses at least c of its squared norm. Hence

    q(t)<= (1-c)^floor(t/T).

This bound is deliberately loose but depends only on fixed local parameter ranges, not control smoothness, system size or runtime.

### Proof

Write I=int_0^T |b(t)|^2 dt. The no-jump norm obeys

    (|a|^2+|b|^2)'=-kappa(t)|b|^2,
    |a(t)|^2+|b(t)|^2>=exp(-kappa_max T)>3/4.

If I>=T/16 we are done. Otherwise choose t_1 in[0,T/4] and t_2 in[3T/4,T] with |b(t_i)|<=2sqrt(I/T). Then |a(t_1)|>=1/sqrt2, and

    |a(t)-a(t_1)|<=g_max sqrt(T I)

for t between them. Integrating b' gives

    g_min T/(2sqrt2)
      <=4sqrt(I/T)+(g_max^2 T+M_b)sqrt(T I).

Here positivity of g makes |a(t_1) int g|>=g_min T/(2sqrt2); all remaining integrals are bounded by Cauchy–Schwarz. Rearranging gives I>=the second term defining I_*. Norm loss is int kappa(t)|b|^2>=kappa_min I_*=c. Reapply the same argument to the normalized surviving no-jump state on each successive interval. Mixed/entangled clock states follow by convexity of the survival effect bound.

## Arbitrary finite unitary Feynman chains

For a fixed finite sequence U_0,...,U_(L-1), let history dressing W_j=U_(j-1)...U_0 and W=sum_j W_j tensor|j><j|. Propagation terms

    g_j(t) U_j tensor|j+1><j| + h.c.

are transformed by W into clock-only real hoppings. Any bounded scalar clock-diagonal Hamiltonian remains clock-only. A terminal reset into a dark DONE label applies the completed product and cannot repeat it. Thus exact data semantics survives all these large clock-only variations.

A uniform positive completion probability over any fixed positive interval also follows for a fixed finite chain under bounded measurable controls with g_j>=g_min>0. One rigorous existence argument is compactness: controls are weak-* compact in L-infinity, solutions are uniformly Lipschitz and have uniformly convergent subsequences; boundedness plus uniform convergence passes the integral ODE to the limit. If the infimum terminal occupation integral were zero, a limiting normalized trajectory would have terminal amplitude identically zero. Its terminal ODE and g_(L-1)>=g_min force the previous amplitude to vanish almost everywhere, hence identically; induction forces every amplitude to vanish, contradicting the nonzero initial norm. Thus the infimum is positive. Iterating gives an exponential survival bound uniform over the allowed waveforms. This argument proves existence, not a useful numerical constant; the preceding single-step bound is explicit and already suffices for fixed-size elementary FT gate cells.

A unitary Stinespring implementation must also prepare/discard its workspace correctly; these are ordinary local operations with their own fault budget. Nothing in the history dressing supplies a free recovery workspace.

## Capability assessment

This does provide a clean distinction between large **clock-only** uncertainty and small **matrix-direction** errors. Fixed deadlines need not realize a precision pulse area, and finite reset rates suffice. However, history-state gauge independence of the carried unitary is conventional Feynman-clock structure. Together with conventional FT it yields a carefully stated scheduled gate-synthesis corollary, not a new autonomous quantum-memory mechanism. The new accounting value is to make the admissible large-error class, retained-bath noise class, completion tails, and external-control costs explicit instead of conflating them.

## Primary comparator check (21:34 UTC)

- Kastoryano–Wolf–Eisert, *Precisely timing dissipative quantum information processing*, https://arxiv.org/abs/1205.0985 (PRL110,110501,2013), already supplies dissipative timing gadgets for sequential operations, conditional measurements and error correction. Our fixed externally scheduled deadline must be compared with that acquired timing resource, not with an artificially pulse-only baseline.
- *Efficiency of Feynman's quantum computer*, https://arxiv.org/abs/2309.09331 (PRA111,022615,2025), explicitly treats the Feynman circuit-to-time-independent-Hamiltonian clock framework. Exact history dressing is standard structure, not an asserted novelty here.
- *Impact of Imperfect Timekeeping on Quantum Control*, https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.131.160204 (2023), studies limitations from imperfect gate timing and distinguishes tasks for which timing changes rates rather than final states. This reinforces the need to state the allowed clock-only error class rather than claim timing errors disappear generally.

These comparisons support the restrained assessment: an explicit finite-rate, broad-clock-calibration contract is useful engineering/theorem bookkeeping, but no new computational capability beyond conventional controlled fault-tolerant circuits has been demonstrated.
