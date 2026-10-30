# CP noise cavities and a mixed native service/fault-box bound
2026-10-30. Governing new candidate V1. Independent review pending. No whole autonomous-QCA theorem is asserted.

## Useful result and scope

For a nominal native generator with arbitrary local Hamiltonians but ONLY onsite dissipators, there is an exact analytical CP cavity: remove the perturbation's action on a chosen finite set of complete hardware sites by averaging those sites out of the perturbation. The resulting generator remains CPTP and contains the original onsite reset channels on that set as genuine separate instruments. This uses the actual noisy GKLS generator, not a fictitious record lift.

Combining these cavities with finite-support nominal SUCCESS-return witnesses gives a signed spacetime-box fault expansion with an inclusive local-noise norm bound. A bad box can be either a local continuous-noise contribution or a nominal service failure. The bound is arbitrarily small by first choosing a fixed long service window, then a fixed small physical perturbation strength. This is a physical native-controller box theorem, not yet the paper's virtual asynchronous-QCA threshold theorem.

## 1. Setup and explicit regularity

Work on a finite lattice of grouped finite-dimensional hardware sites, plus an arbitrary retained bath and reference. Let

    L0 = -i[H0,·] + sum_v D_v + L_bath

be the nominal generator. H0 is a bounded sum of finite-support Hamiltonians; each D_v is a sum of resolved GKLS dissipators supported on ONE complete hardware site v. The bath-only generator is common to every comparison. The actual generator is

    L(u) = L0 + N(u),       N(u)=sum_Z N_Z(u),

where the bounded normal perturbations have physical support Z of bounded cardinality/radius and incident budget sum_(Z contains v)||N_Z(u)||_cb<=eta. Individual N_Z need not be CP or GKLS. The total perturbation annihilates the identity in the adjoint. Bath-only terms may instead be included in the common bath generator. All bounds below are on trace-class cb/diamond norms, hence reference-stable.

The finite-dimensional proof needs only an actual GKLS generator at every time. For an unbounded bath generator B, use the standard common-core setting L(u)=B+K(u), with bounded normal K(u), locally norm-integrable/piecewise-continuous coefficients and the corresponding well-defined interval propagators. The reduced cavity generator is justified by the repeated-reduction product in Section 2, not merely by a formal derivative. A still more general unbounded realization must supply this same bounded-perturbation/product-limit property; it is not inferred from the word 'commutes.'

## 2. CP cavity theorem

For a finite set S of COMPLETE physical sites, write tau_S=I_S/d_S. Define

    R_S(rho)=tau_S tensor rho,      T_S=Tr_S,
    E_S(N)=Id_S tensor (T_S N R_S).

E_S is a norm-one projection on superoperators. Projections for different site sets commute, with E_S E_T=E_(S union T). It preserves support in the following sense: E_S N_Z acts only on Z\S and the bath; if Z misses S, E_S N_Z=N_Z.

**Claim.** L^S:=L0+E_S N is a GKLS generator, and every nominal dissipator D_v for v in S remains a separately identifiable GKLS summand of it. Moreover

    L-L^S = sum_(Z meets S) (I-E_S)N_Z,
    ||(I-E_S)N_Z||_cb <= 2||N_Z||_cb.                  (2.1)

No new physical operation is being added: L^S is an analytical comparison dynamics.

**Proof, bounded case.** The reduced generator L_red=T_S L R_S is GKLS on the complement. Explicitly, expand each actual jump J into S matrix blocks J_ab; its reduced dissipator has jump operators J_ab/sqrt(d_S). The reduced Hamiltonian is the normalized partial trace of the actual Hamiltonian. This is equivalently the derivative of a CPTP reduced channel at the identity.

Partition the NOMINAL Hamiltonian as H0=H_out+H_touch, with H_out supported outside S, and let barH=T_S(H_touch tau_S). All nominal dissipators are either wholly inside or wholly outside S. The nominal reduction is

    T_S L0 R_S = L_bath + sum_(v outside S)D_v
                -i[H_out+barH,·].

Consequently

    L^S = Id_S tensor L_red + sum_(v in S)D_v
          -i[H_touch-Id_S tensor barH,·].               (2.2)

Every term is a valid GKLS generator or Hamiltonian commutator. This proves CP, the separate nominal-reset decomposition, and (2.1). Cross-boundary nominal dissipators would invalidate this reconstruction and are NOT allowed by the lemma. Arbitrary cross-boundary Hamiltonians are harmless.

**Unbounded bath justification.** With B bath-only and K bounded, R_S,T_S commute with the bath evolution and the candidate reduced generator is B+T_S K R_S. On a common core, the product

    [ T_S exp((t/n)(B+K)) R_S ]^n

converges to exp(t(B+T_S K R_S)) by the bounded-perturbation/Chernoff product argument. Every factor is CPTP, so the strong trace-class limit is CPTP, including every finite reference extension. Piecewise-continuous time dependence follows by step approximation and bounded Duhamel continuity. This provides the required reduced normal propagator under the stated regularity; no bath reconstruction or finite-dimensional bath approximation is assumed.

## 3. Physical nominal service contract

For each native hub h, a tested window counts enough actual nominal SUCCESS events to guarantee a fresh complete attempted channel (two is a safe choice for the rollback machine). Use only passive finite record counters, initialized at the window's start. Their preparation is an analytical instrument annotation, not a physical feedback operation.

The substituted finite Stinespring/rollback generator must provide a finite-support witness Z_h, supported on physical patch S_h plus its passive counter, satisfying

    alpha I <= Z_h <= I,
    (L0^rec - J_h^kill)^* Z_h <= -r Z_h,               (3.1)

with alpha,r>0 independent of N and the input/bath/reference. J_h^kill is the actual nominal gain whose occurrence completes the service requirement. Its physical reset support lies inside S_h. These are the real finite-return witnesses, not virtual dirty-history flags. For the new payload their constants/supports must be reconstructed, not copied numerically from the old LOCC machine.

There is a fixed packing number P such that any set of hub labels contains a subset of at least 1/P of its size whose witness supports are disjoint and no single nominal term meets two supports. For such a packed subset A, the product witness Z_A=prod_h Z_h has alpha^|A| I<=Z_A<=I and killed drift -r|A|Z_A. Extra killed gains for other requested service failures only subtract positive operators and cannot spoil this upper bound.

In a cavity whose cut-site union contains every S_h under test, all remaining perturbation acts outside these witnesses. Its adjoint vanishes on them (the total outside perturbation is identity-annihilating). Equation (3.1) and its product version therefore hold EXACTLY, with no small-noise correction. The records are genuine because (2.2) retains their nominal reset channels as separate summands.

For a window of length T with all tests in a set A required to fail, the resulting CP/TNI event map has norm at most

    p0^(|A|/P),       p0=alpha^(-1) exp(-rT),           (3.2)

once T is large enough that p0<1. In different consecutive windows, initialize new passive counters and use the same uniform bound on their arbitrary incoming state. No independence is claimed.

## 4. The compatible good-box family

Tile physical time into windows of the fixed length T. A box i=(h,j) is hub h's test in window j; its cut region is S_h during that window. For any finite set A of boxes define G_A as follows:

1. During each window, replace N by E_(union of the active A patches) N.
2. In this actual cavity dynamics retain the passive nominal service records for the boxes in A.
3. Keep the CP event that EVERY A-service test succeeds; forget the passive records afterward.

Thus G_empty is the ACTUAL unmodified channel. Every G_A is a well-defined CP/TNI map, but it is not asserted to be a subchannel of G_empty. This distinction is essential. If more cavities/records are included, forgetting a counter gives the corresponding marginal instrument for that SAME cavity generator.

Define the inclusive bad-box map

    B_F = sum_(A subset F) (-1)^|A| G_A.                (4.1)

For any finite universe I of boxes, the signed exact-fault maps

    E_R = sum_(A subset R) (-1)^|A| G_((I\R) union A)

satisfy sum_R E_R=G_empty and sum_(R contains F)E_R=B_F. Each term in E_R has nominal-noise-free, successfully serviced patches at every box outside R. Whether that property suffices for the required asynchronous logical simulation is a separate deterministic theorem.

## 5. Mixed noise-restoration/service-failure identity

Partition F into restored-noise labels R and service-failure labels S=F\R. Keep all S patches cut. For i in R introduce x_i in [0,1], acting during its own window, and set

    L_x = L0 + E_S prod_(i in R)[E_i+x_i(I-E_i)] N.      (5.1)

All E's here are time-dependent according to their windows and commute pointwise. The product is a convex combination of union-cavity projections, so (5.1) is CPTP at every x. It retains the nominal records of all S tests. Let H_S(x) be its CP event map in which all S tests fail. Mixed finite differences restore the R labels:

    D_R H_S = sum_(A subset R)(-1)^(|R|-|A|)H_S(1_A).

Then the exact Boolean identity is

    B_F = sum_(R subset F) D_R H_(F\R).                (5.2)

To verify it, expand failure_S by inclusion-exclusion in success records, and sum over the cut supersets. For a fixed success set A, all extra cut-set coefficients cancel by (1-1)^m, leaving precisely (-1)^|A| G_A. This uses only the compatible cavity instrument marginals, not positivity of B_F.

## 6. Uniform mixed derivative bound

Let v bound the number of physical sites in a witness patch. Let K bound the number of simultaneous box patches that any perturbation support Z can meet. Let D bound the number of other simultaneous labels that can share some perturbation support with a given box. These are fixed finite geometric constants. Set

    q = 2^K v eta T,

and require q<=1. A generator derivative with respect to a nonempty block A of restoration labels is zero unless |A|<=K and a physical perturbation support meets every patch in A. Otherwise its integrated cb norm is <=q: each (I-E_i) costs at most 2, the remaining convex projection factors have norm <=1, and the incident budget at any one patch bounds the total strength by v eta.

Crucially, every such derivative still has the E_S factor and therefore acts as the identity on every service-witness support in S. It commutes with all their positive weighting congruences, even when R and S patches overlap.

In each time window select a buffered packing of the S labels, form their product Z, and use the weighted cb norm induced by rho -> sqrt(Z)rho sqrt(Z). The killed cavity propagator contracts in this norm at rate r times the packing size. Derivative insertions have the SAME cb norm after this congruence, since they act outside its support. Splitting a window at insertion times incurs its alpha conversion only once, not once per insertion. Changing windows likewise incurs at most one conversion per selected service label. Thus the complete derivative expression retains the factor

    p^|S|,           p=p0^(1/P).                       (6.1)

The mixed Duhamel derivative is a sum over set partitions pi of R: each block A in pi corresponds to one generator derivative insertion. Each block has size at most K, so there are at least |R|/K insertions. Their time orderings partition the corresponding time cube; no factorial remains after the norm integrations. Allowed blocks containing a fixed label lie in its bounded overlap neighborhood, so the number of allowed partitions is at most B^|R| for a fixed B (the crude choice B=2^(D+1) suffices). Consequently

    ||D_R H_S||_diamond
       <= p^|S| B^|R| q^(|R|/K).                       (6.2)

The case R=empty is the genuine cavity miss bound; S=empty uses ordinary CPTP contraction. Integrating the derivative over x does not enlarge these uniform bounds. The proof allows the bath to retain all correlations; no normalized rare-event state is used.

Summing (6.2) in (5.2) proves

    ||B_F||_diamond <= [p + B q^(1/K)]^|F|.             (6.3)

Thus eta_box=p+B(2^K v eta T)^(1/K) is a local inclusive bad-box strength, uniform in total system size and number of time windows. First fix the finite native hardware and service witness. Then choose a fixed T making p sufficiently small. Finally choose eta sufficiently small. All are constants independent of the computation size; the resulting threshold may be extremely small.

## 7. Remaining nontrivial bridge

Equation (6.3) does NOT by itself supply the source paper's asynchronous universality theorem. The missing deterministic step is to show that the signed exact-fault family E_R admits the same kind of bounded-damage/correct-cut simulation used by that theorem: a good native box has no perturbation on its full protected patch and enough actual attempts, but it need not correspond to one synchronized ideal QCA location. Inherited dirty prefixes, finite marching-clock errors, delayed valid attempts and progress through the recursive hierarchy must be assigned to bounded-overlap damage regions or causal witnesses. The source's Section VII leaves that formal asynchronous threshold proof open as well.

Encoded initialization and final physical output remain paid interfaces. This candidate removes the false actual-record-lift assumption at the physical service/noise level, not those separate operations. It is neither a practical threshold estimate nor a novelty claim about ordinary fault-path inclusion/exclusion.

## Primary comparator

Aliferis, Gottesman and Preskill, [quant-ph/0504218](https://arxiv.org/abs/quant-ph/0504218), Section 8, already formulate inclusive local fault-path norm bounds with arbitrary extra faults and common environments. Terhal and Burkard, [quant-ph/0402104](https://arxiv.org/abs/quant-ph/0402104), Appendix A, give a first-fault resummation for Hamiltonian noise. The present analytic work must be compared with those methods, not advertised as inventing coherent fault paths. Its specific role is a CP cavity preserving native onsite reset instruments under broad joint-generator calibration perturbations.
