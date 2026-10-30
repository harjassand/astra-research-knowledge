# Independent review: CP noise cavity and mixed signed bad-box norm theorem
2026-10-30. Reviewer: `challenge_live_busy_energy`.

## Verdict, binding source and non-promotion
**Scoped PASS for the abstract CP-cavity theorem and the mixed inclusive signed-box norm bound, CONDITIONAL on the stated freshly supplied finite-support service-witness contract (3.1), with the precise premises below.**

Frozen source read and copied verbatim:

`autonomous_qca_native_bridge_20261030/CP_NOISE_CAVITY_AND_MIXED_BAD_BOX_V1.md`

SHA-256 `33a89f263fc79d87309f9649886fe9091db25e1353e315708469d91ace8d21ea`.

The earned conclusion is norm locality of a signed family of box maps:

    ||B_F||_diamond <= eta_box^{|F|},
    eta_box = p+B(2^K v eta T)^{1/K},
    p=(alpha^{-1}e^{-rT})^{1/P}.

It is NOT semantic correctness of good boxes as ideal asynchronous QCA locations. It does not solve inherited dirty first retirement, leading asynchronous rectangles, recursive progress/damage attribution, encoded initialization, or physical final output. The new generic-Stinespring-payload witness construction must be audited separately: the compiler note's currently qualitative service wording and old numerical witnesses are not silently promoted by this receipt.

The author explicitly requested this conditional scope and confirmed two important premises: every nominal D_v acts on the complete finite hardware site v ONLY, as identity on the retained external bath; and Z_h is a positive witness on the alive {0,1} fewer-than-two-SUCCESS counter space, not an un-killed absorbing completed sector. Those clarifications are used below.

## 1. Precise locality, instrument and regularity hypotheses
The cavity construction is applied to the PHYSICAL generator first. Passive counters are attached afterward to designated nominal jump summands that the cavity demonstrably retains. One must not first enlarge the generator by arbitrary record couplings and then pretend their partial trace has the same onsite-dissipator reduction.

The nominal generator has arbitrary bounded finite-support Hamiltonian terms and system-only onsite dissipators, plus a common bath-only generator. Actual perturbation pieces may be bounded normal HP maps, non-CP and not individually trace-preserving. Their aggregate is the bounded trace-preserving difference between actual and nominal dynamics. The actual total generator/propagators must remain physical. The incident cb budget is the PER-SITE budget in this source; this receipt does not replace it by the separate global-budget noise model.

For a uniform mixed-box bound, physical noise supports have the stated fixed cardinality AND radius. The finite patch volume v, simultaneous overlap number K, overlap neighborhood size D and witness packing number P must be bounded independently of lattice size and time horizon. Bounded cardinality with arbitrary distant partners alone would not give the claimed fixed D or B; that broader noise model is not accepted here.

For a retained unbounded bath, use exactly the source's bath-only common generator B plus bounded normal K(u), common core, locally norm-integrable/piecewise norm-continuous coefficients and bounded-perturbation/product-limit setting. Merely asserting that formal terms commute is insufficient. Witnesses and analytic counters have no external bath support, and all statements are reference-stable trace-class cb/diamond statements.

## 2. The physical CP cavity is valid despite non-CP local noise pieces
For complete hardware sites S, let R_S append their maximally mixed state, T_S trace them out, and

    E_S M=Id_S tensor(T_S M R_S).

Both R_S and T_S are channels. Complete amplification and composition show ||E_S M||_diamond<=||M||_diamond. Tensor-product reduction gives

    E_S^2=E_S,    E_S E_T=E_(S union T).

If M has system support Z and acts as identity outside it, E_S M has support contained in Z\S and the same bath. In particular it fixes M whenever Z misses S. Therefore

    L-L^S=sum_{Z meeting S}(I-E_S)N_Z,
    ||(I-E_S)N_Z||_diamond<=2||N_Z||_diamond.

No CP property of N_Z is invoked.

In the bounded finite-dimensional case, reduce the ACTUAL GKLS generator:

    L_red=T_S L R_S.

For an actual jump J with S matrix blocks J_ab, the reduced jump family is J_ab/sqrt(d_S). Both gain and complete loss match that family after tracing with tau_S. The Hamiltonian becomes its normalized partial trace. Thus L_red is GKLS on the complement.

Write H0=H_out+H_touch and let barH be the normalized S trace of H_touch. A nominal dissipator supported strictly inside S reduces to ZERO because it is trace-preserving and acts on no complementary/bath factor. A nominal outside dissipator is unchanged. Consequently

    L0+E_S N
      = Id_S tensor L_red
          +sum_{v in S}D_v
          -i[H_touch-Id_S tensor barH, .].          (2.1)

This is a sum of a GKLS generator, the explicit nominal onsite dissipators, and a Hamiltonian commutator. It is CPTP and retains the designated nominal reset jumps on S as genuine separate instruments. It can restore such jumps even when the actual perturbation cancelled them; it is an ANALYTICAL cavity, not an instrument decomposition of the original actual channel.

The partial-trace Hamiltonian correction is indispensable. Without subtracting Id_S tensor barH, the reduced Hamiltonian is counted twice when H_touch has a nonzero S average. Cross-boundary Hamiltonians themselves cause no CP obstruction.

### Necessary exclusion, not a counterexample within the accepted scope
If a nominal `onsite` jump is allowed to act jointly on an external bath, (2.1) can fail. For example, take J=Z_S tensor sigma^-_bath, actual L=0, and N=-D[J]. The purported cavity is

    D[Z tensor sigma^-]-D[I tensor sigma^-].

On |+>_S|1>_bath its derivative has expectation -1 in the orthogonal state |+>_S|0>_bath. It is not even a positive-generator tangent. This is why the strict system-only onsite premise, explicitly confirmed by the author, matters. Cross-boundary nominal dissipators are likewise not covered.

## 3. Unbounded bath: the supplied product argument closes the actual CP claim
Let actual L=B+K, where B is the bath-only C0 CPTP generator and K is bounded. The reduced candidate is B+K_red, K_red=T_S K R_S. Bounded perturbation theory supplies its C0 evolution as a linear semigroup; positivity is then established by the reduction product, not assumed:

    [T_S exp((t/n)(B+K))R_S]^n.

Each factor is CPTP and its derivative on the common core is B+K_red. The contraction Chernoff/product-limit argument in the stated setting identifies its strong trace-class limit with the candidate reduced semigroup. Strong trace-class convergence preserves positivity and trace on every input. The same reasoning after each finite reference amplification gives complete positivity and trace norm one.

Adding the bounded nominal onsite GKLS summands and bounded Hamiltonian correction in (2.1) is justified by the corresponding bounded-perturbation/Trotter product, whose factors are CPTP. This supplies the full cavity, not only the reduced evolution. Piecewise norm-continuous time dependence follows from step approximation and bounded Duhamel continuity. Normality follows from having the trace-class predual maps. No finite-bath approximation or bath reconstruction is required.

These arguments are conditional on the stated analytic setting. They do not license an arbitrary unbounded system-bath realization that lacks the common-domain/product-limit property.

## 4. Fresh service witnesses, packing and one conversion per window
Assume the actual nominal lifted service instrument supplies

    alpha I<=Z_h<=I,
    (L0^rec-J_h^kill)^*Z_h<=-r Z_h.

The alive counter is {0,1}: a first SUCCESS changes 0 to 1; a further SUCCESS from 1 completes the requirement and its gain is deleted in the killed instrument. There is no completed absorbing sector included in the lower-bound identity. This witness must be rebuilt for the actual finite payload/rollback alphabet. The present review treats that construction as an explicit input, as requested by the author.

For a buffered packed subset A, supports are disjoint and no nominal term meets two. Products of the Z_h commute. The exact local product rule, including the designated killing gains, yields

    K_A^*Z_A<=-r|A|Z_A,
    Z_A=product_{h in A}Z_h,
    alpha^{|A|}I<=Z_A<=I.

For the native owner-specific SUCCESS channels, the requested additional killed gains are genuine distinct/union subinstrument gains. Killing the remaining tests only subtracts positive operators when acting on positive Z_A. It cannot spoil the bound. This is not an arbitrary subtraction of a map from a GKLS generator.

If all tested physical witness patches are cut, the remaining total perturbation acts as identity on their physical factors and on their passive counters. Its adjoint annihilates Z_A because the total outside perturbation is identity-annihilating. Thus the same killed drift holds EXACTLY in every such cavity and restoration interpolation, not merely up to O(eta).

Define the Schrödinger congruence C_Z(rho)=sqrt(Z_A)rho sqrt(Z_A). The transformed killed propagator is CP and obeys

    ||C_Z U_kill(t,s) C_Z^{-1}||_diamond
        <=exp[-r|A|(t-s)].                         (4.1)

Indeed its adjoint sends I below that scalar multiple of I. Also ||C_Z||<=1 and ||C_Z^{-1}||<=alpha^{-|A|}. A derivative insertion acting outside the witness/counter support commutes with C_Z, so its weighted cb norm is exactly its ordinary cb norm.

Therefore a product of any number of derivative insertions inside one window has only ONE alpha^{-|A|} conversion and the total decay exp(-r|A|T). The time subintervals sum to T; no conversion is charged at each insertion. Choosing |A|>=|S_window|/P gives

    alpha^{-|A|}e^{-r|A|T}
       <=p^{|S_window|},
    p=(alpha^{-1}e^{-rT})^{1/P}<1.

Fresh counter attachment/forgetting at consecutive windows are CP contractions. Multiplying the window estimates gives p^{|S|}, even with arbitrary incoming correlations and arbitrarily many unmarked faults. This is the key service factor in the mixed bound.

## 5. Instrument compatibility and the exact Boolean identity
For sets V subset U of boxes, write C_{U,V} for the map with U's patches cut and the event that all V service tests succeed. Choose the nominal jump labels once. In a U cavity, all those jumps are genuine separate summands; forgetting unwanted passive counters gives the same C_{U,V}. This compatibility is required only WITHIN the same cavity, not between different cavity generators. Set G_A=C_{A,A}; G_empty is the actual unmodified channel.

For restored labels R and service-failure labels S=F\R,

    L_x=L0+E_S product_{i in R}[(1-x_i)E_i+x_i Id]N.

The product is a convex combination of union-cavity projections. Hence L_x is CPTP at every x, and each constituent retains the fixed nominal reset summands for S. Attach ONLY those passive records after constructing the physical cavity. The lifted killed generator is polynomial in x with fixed designated S killing gains. Its derivatives therefore come only from the projected noise, not from a parameter-dependent record convention.

At vertex 1_D, D subset R, the cut set is U=F\D. Expanding all-S failure by inclusion-exclusion gives

    H_S(1_D)=sum_{V subset S}(-1)^{|V|}C_{F\D,V}.

In sum_R D_R H_(F\R), fix U,V and collect its coefficient. It is

    sum_{V subset S subset U}(-1)^{|U|-|S|+|V|},

which vanishes unless U=V, in which case it equals (-1)^{|V|}. Thus exactly

    B_F=sum_{A subset F}(-1)^{|A|}G_A
        =sum_{R subset F}D_R H_(F\R).              (5.1)

No positivity of B_F or of mixed differences is assumed. The second Möbius inversion defining E_R also gives sum_R E_R=G_empty and sum_{R containing F}E_R=B_F exactly. Every term in E_R has the declared cut/success property outside R, but the signed map itself is not a physical subchannel of the actual process.

## 6. Mixed derivative magnitude and bounded-overlap combinatorics
At a time in the corresponding window, a nonempty generator derivative block A is

    E_S product_{i in A}(I-E_i)
          product_{i in R\A}[(1-x_i)E_i+x_i Id]N.

It vanishes unless some noise support meets every A patch. Thus |A|<=K. A derivative involving different nonoverlapping time windows also vanishes. Remaining convex projection factors have norm at most one; each (I-E_i) costs at most two. Choosing any one label in A, the per-site incident budget summed over its at-most-v-site patch bounds the relevant total strength by v eta. Hence each allowed derivative block has integrated norm at most

    q_*=2^K v eta T.

Every derivative retains E_S and therefore acts as identity on every S witness support and all passive counters. This remains true when restored and service patches overlap; in fact some such derivatives can vanish. The weighted commutation used in section 4 is exact.

The mixed Duhamel derivative is a sum over SET PARTITIONS pi of R. Each block corresponds to one generator derivative insertion. The temporal orderings of the distinct blocks partition their time cube, so the norm integrations yield product-block bounds with no remaining factorial. Every block has at most K labels; hence a partition has at least |R|/K insertions. For q_*<=1 its contribution is bounded by

    p^{|S|} q_*^{|R|/K}.

Only subsets of the bounded overlap neighborhood can form a block with a chosen label. Exposing the block of the least remaining label gives at most 2^D choices per stage. Therefore the number of allowed partitions is at most B^{|R|}, and the source's conservative B=2^{D+1} suffices. This bound includes partitions into singleton blocks and any physically overlapping insertion locations; it is not an assumption that the insertions commute.

Integration over x in [0,1]^R does not enlarge the uniform estimate. Consequently

    ||D_R H_S||_diamond
       <=p^{|S|}B^{|R|}q_*^{|R|/K}.

Summing over R in (5.1) gives exactly

    ||B_F||_diamond<=[p+B q_*^{1/K}]^{|F|}.         (6.1)

Here K>=1 can be chosen conservatively; a noise-free exceptional case is interpreted directly. Fixed witness/support constants are selected first, then T sufficiently long that p is small, then eta sufficiently small that q_*<=1 and B q_*^{1/K} fits the desired margin. T is not used to change the witness radius or packing constants after the fact. The construction is uniform in finite lattice size and number of tested windows.

## 7. Independent diagnostics and evidentiary limits
`check_cavity_and_boolean.py` independently checks an eight-dimensional system/system/bath fixture whose actual perturbation CANCELS one nominal onsite dissipator, adds a joint bath jump and adds a joint Hamiltonian. Thus the chosen N decomposition is genuinely not a GKLS decomposition. Results:

- cavity reconstruction residual 1.12e-16;
- omitting the Hamiltonian partial-trace correction produces norm error 0.62;
- commuting union-projection residual zero;
- cavity channel Choi minimum about -4.6e-17 and trace-preservation residual below 9e-17;
- the mixed Boolean identity for five labels and arbitrary compatible within-cavity classical instruments has residual below 7e-16;
- the excluded nominal system/bath-dissipator example has the predicted negative tangent -1.

These are finite algebra diagnostics, not an actual generic-payload service proof, asynchronous semantics proof or threshold simulation. The theorem rests on sections 1–6 and its explicit service contract.

## 8. Standard comparator and exact remaining boundary
The inclusive fault-path norm/resummation mechanism must be compared with the source's primary AGP and Terhal–Burkard methods; this receipt makes no novelty claim for Möbius inclusion-exclusion, Duhamel resummation or coherent-environment fault paths. The narrow additional role checked here is the actual CP cavity that preserves specified nominal onsite reset instruments despite signed local calibration perturbations, and its compatibility with a supplied killed-service witness.

An arbitrarily small eta_box is NOT yet a native autonomous-QCA threshold. A good native box may contain dirty leading retirement, delayed fresh attempts or an unmatched asynchronous causal cut. No deterministic bounded-damage/leading-rectangle theorem is inferred from (6.1). Nor does the conditional service input prove a correct attempted QCA update on every initial dirty prefix. Those semantic and hardware-instantiation obligations remain explicit. All earlier accepted reviews and interfaces are preserved unchanged.
