# Independent audit: bounded-body noise without a fixed noise-interaction graph

2026-10-30. Reviewed the initial root candidate `BOUNDED_BODY_NOISE_EXTENSION.md`, SHA-256 `60fa6455770350bd186e594fc634b2745341afa4d60d6a4e5a7d9efb38ef922e`, and its final physicality-clarified version, SHA-256 `f83b55e7ba248aab73a621c656bcc8e03d1ffe754ff229b66e581e3e5372726a`. The exact diff only makes the required full-CPTP/killed-compression premise explicit; both versions are preserved. Original inputs were not changed. Exact copies and hashes are in `reviewed_sources/` and `SOURCE_SHA256.txt`.

## Verdict

**PASS at the explicitly physical, well-posed scope below.** Noise-support cliques and a uniform *count* of noise supports through a site are unnecessary for the accepted continuous weighted-barrier/simple-compiler argument. Fixed bounded support cardinality and a pointwise **sum of joint cb norms through each physical site** suffice, even when supports are disconnected in the fixed nominal graph, change with time, or have a dense union. No new mathematical obstruction was found in the componentwise edge, drift, frame/dilation, boundary union, logical-factorization, or total-norm bridges.

The crucial extra proof, supplied in Section 6, is a cb-norm-only full-versus-killed comparison. It does not replace a cb bound by an unjustified Lindblad coefficient or Kraus-count bound.

The final reviewed source now incorporates the mandatory physicality clarification: HP and identity-annihilation of the summands plus mere existence of an evolution are not sufficient. The **full joint time-local dynamics** must be a well-posed physical generator with CPTP propagators on every time interval (the stated joint Hamiltonian/Lindblad model suffices). This ensures CP/trace-nonincreasing killing and the drift deletion inequality. The summands themselves may be signed HP maps. For an infinite-dimensional bath use bounded normal perturbation maps with normal preduals, measurable coefficients, and the regularity needed for the accepted joint propagator/compression construction. No new unbounded-generator existence theorem is claimed.

This audit imports, rather than re-proves, the accepted Tanner code/confinement/active-density hypotheses and the finite-rate full-Hilbert simple-compiler clean drift. It certifies the *new topology-free continuous-noise bridge* only.

## 1. Exact stronger noise contract

There are `N_phys=Theta(N)` physical DATA/controller sites of fixed finite dimensions. At each time, write the non-bath perturbation as normal local maps

    N_t* = sum_alpha N_alpha,t*,
    N_alpha,t* acts on Z_alpha,t and the retained bath, tensor identity elsewhere,
    1 <= |Z_alpha,t| <= q,
    N_alpha,t*(I)=0, and N_alpha,t* is HP,
    sup_(i,t) sum_(alpha:i in Z_alpha,t) ||N_alpha,t*||_cb <= eta.

The supports are sets of physical sites, not balls in a fixed noise graph. `q` is independent of N. The cb norm is that of the **joint** system/bath map, stable under arbitrary reference amplification. The map decomposition is fixed independently of the unknown logical input, and is measurable/well posed in time. Countable sums are harmless under the displayed absolute norm bound; the analogous integral formulation requires the corresponding measurable integrability assumptions.

Bath-only evolution is separated. It commutes with the DATA/controller potential and proof/frame circuits, and has no boundary or logical error term. Its regularity is covered only by the governing well-posedness hypothesis. A bounded average energy, a reduced-state fit, or an unbounded joint coupling does not imply this contract.

The nominal bounded-degree DATA graph and animal graph contain all full code/check/energy-view read supports, controller/reset/frame/credit supports, and container-overlap edges needed by the accepted proof. They **do not** contain noise-support cliques. Nominal per-move changed-token cliques remain indispensable to nominal animal completion; removing noise cliques does not remove those.

## 2. Disconnected-support canonical edge and source barrier

Work in one CSS sector. Let E be its fixed minimum representative, with every nominal-G component smaller than ell, and let p be any Pauli support of size at most s. Let F be the fixed minimum representative of `sigma(E)+sigma(p)`. Take connected components K of the induced graph on

    supp(E) union supp(p) union supp(F).

A stabilizer check meeting two such components would connect them by a nominal check-support edge. Hence the zero syndrome of `E xor p xor F` holds separately on each K. Replacing F inside K by `(E xor p) inside K` preserves its *entire* syndrome. Global minimum weight, including any fixed tie-breaking, therefore gives

    |F intersect K| <= |(E xor p) intersect K|,
    |K| <= |E intersect K|+|p intersect K|+|F intersect K|
        <= 2(|E intersect K|+|p intersect K|)
        <= 2(|E intersect K|+s).                    (2.1)

Nothing says that p is connected or lies in only one K; no such statement is needed. Every old E-component meeting K is wholly contained in K, because its old paths remain in the induced union graph.

By the accepted nominal J_x construction, these old components have disjoint containers and their actual source occupied mass is additive. For raw checks it is their confined syndrome mass; for the Tanner application it is the confined unary-energy mass. In the latter case nominal full energy-view/read footprints ensure that an energy view cannot see errors in different E-components. Thus at least `h|E intersect K|` actually occupied syndrome/energy vertices lie in the connected animal `J(K)`, with `|J(K)|<=D0|K|`. Arbitrary occupied flag tokens can only improve its weight. Consequently

    V_0(source) >= f_J(K)(source)
      >= exp{L[(h/2-uD0)|K|-hs]}.

With `u<=h/(4D0)` and `ell>=8s`, any `|K|>=ell` forces

    V_0(source) >= exp(L h ell/8) = M_edge.          (2.2)

If every K has size below ell and ell is below the relevant sector distance, the zero-syndrome Pauli `(E xor p xor F)|K` is a stabilizer. Their product is a stabilizer too, regardless of the number of components. Thus each edge has identity canonical logical action up to a syndrome-dependent scalar phase. It also has a component-safe target, since every F-component lies within one K.

The statement applies sectorwise to an arbitrary DATA Pauli. Tensoring with arbitrary controller/bath coefficients, and then summing its finite DATA Pauli expansion, does not change the logical conclusion. Physical support cardinality after nominal frame expansion, not bare correction-mask size, determines s.

## 3. Direct relative-factor cb bound; no noise graph counting

A proof avoiding subtle orbit language is available. In gauge coordinates write an animal as

    f_A = theta^(u|A|) product_(v in A) theta^(-x_v),

where the `x_v` are commuting local projectors (raw-check, nonlinear unary-energy, or repeated flag tokens). Dummy factors are identity. Every factor has eigenvalues in `[1,theta^(-1)]`. The nominal bounded support/incidence of these factors implies that a q-site noise term meets at most `m<=kq` factors, even when its q sites are arbitrarily distant.

Let D be the product of unaffected factors and G the product of affected factors. Then `f_A=c_A D G`, D has physical support disjoint from Z, D and G commute, and

    I <= G <= theta^(-m) I.

Locality means bimodularity over all operators outside Z, even with a common retained bath. Therefore

    N_Z*(f_A)=c_A D^(1/2) N_Z*(G) D^(1/2).

Since `N_Z*(I)=0`, HP and the cb norm give

    +/-N_Z*(G) <= ||N_Z*||_cb (theta^(-m)-1) I.

Congruence and `f_A>=c_A D` yield

    +/-N_Z*(f_A) <= C_q ||N_Z*||_cb f_A,
    C_q=theta^(-kq)-1.                              (3.1)

If the noise term meets no factor, the result is exactly zero. This proof does not require independent token bits, closure of the coarse token algebra, connected supports, or a Pauli probability interpretation. It works on the full raw-syndrome/label Hilbert space, with bath and reference retained.

Let `S_A` be the union of the physical supports of factors in A. Nominal geometry gives `|S_A|<=b|A|`. Sum *actual norms*:

    sum_(Z:Z meets S_A) ||N_Z*||_cb
       <= sum_(i in S_A) sum_(Z contains i) ||N_Z*||_cb
       <= b eta |A|.

Summing (3.1) over full animals proves

    N_t* V <= C_q b eta W.                          (3.2)

No count of possible partners or hyperedges appears. Constants depend on fixed q and the nominal apparatus, not on the union noise topology. Time dependence is handled pointwise, almost everywhere as appropriate.

## 4. Frame and local CP-dilation support/strength propagation

For any fixed-depth bounded-arity nominal unitary circuit U, let C(i) be the forward structural cone of an input physical site i and R(j) the backward structural cone of output site j. There are uniform constants a,r such that `|C(i)|<=a`, `|R(j)|<=r`. A conjugated term has support

    S(Z) subset union_(i in Z) C(i),   |S(Z)|<=a q,

and its joint cb norm is unchanged. For every output site j,

    sum_(Z:j in S(Z)) ||Ad_U N_Z* Ad_Udagger||_cb
      <= sum_(i in R(j)) sum_(Z:i in Z) ||N_Z*||_cb
      <= r eta.                                    (4.1)

This proves both bounded cardinality and bounded incident strength after the actual controller frame. It does not assert bounded degree for the expanded *noise* union.

For the positive credit circuit T, use its local unitary Stinespring dilation on fresh proof environments, with one bounded-dimensional environment per bounded patch gate. These environments are not the retained bath. The circuit remains fixed depth and bounded arity, so the same cone proof works on the enlarged physical/proof site set. There are O(N) such proof sites, but no physical hardware resource claim is made from introducing them.

Explicitly, if `T(O)=E[U_Tdagger (O tensor I_E) U_T]`, set

    M_Z=Ad_U_T (N_Z* tensor id_E) Ad_U_Tdagger.

Then

    N_Z*T(O)=E[U_Tdagger M_Z(O tensor I_E) U_T].

Apply Section 3 to M_Z, sum using (4.1), and apply the positive conjugation/compression. This gives the required

    N_t*F <= C eta T(W_+),   F=T(V_+).

A dressing gate disjoint from the system support commutes with a system/bath term because that gate acts trivially on the retained bath. Thus a shared bath does not spread the structural physical cone. The proof uses a bounded-patch dilation of the specified nominal credit channel, not an arbitrary nonlocal completion or a replacement of actual controller dynamics by a fresh-environment process.

## 5. A single universal high-potential boundary

Keep the fixed raw basin

    P = 1{both canonical sector representatives component-safe, V_0<M},
    M=M_edge/2.

Use s and k large enough for all actual nominal operators and all permitted noise operators after the finite nominal frame. Section 2 prevents a component-unsafe target from any P source. A bounded-support operator has matrix elements only between raw syndrome/label sectors differing in at most k factors; hence its source/target raw potentials obey a uniform ratio bound. Any target outside P must cross the V_0 cutoff, so its source has `V_0>=cM`, with fixed `c>0` (one may take the corresponding theta^k).

Choose the SAME projector for all times and all possible bounded-body supports:

    B=P 1{V_0>=cM},   R=P-B.

For every system operator A on any admissible support,

    Q A R=0,   Q=I-P.                               (5.1)

Equivalently every union of actual exit source blocks is contained in B. This is a projector inclusion, not a sum of exit probabilities over supports. The dense union of possible partners therefore costs no factor. The accepted dressed killed moment, `F>=V_0`, gives

    p_t=Tr(B rho_P(t)) <= C N/M.                    (5.2)

All controller sites are included in the support accounting, and the bath remains a spectator in P, B and R.

## 6. cb-only Duhamel comparison, killing and logical factorization

Let `Pi(X)=PXP`. A normal superoperator local to finite-dimensional system patch Z and arbitrary bath has an expansion in a finite basis of **system left/right multiplication maps**, with bounded normal bath coefficient maps:

    N_Z = sum_(alpha,beta) L_Aalpha R_Abeta tensor Phi_alpha,beta.

This is an algebraic expansion only. No coefficient norm sum is estimated and no bath matrix basis or bath dimension bound is used. From (5.1) and its adjoint, every summand maps `R rho R` to a P-supported output. Therefore

    (Id-Pi)N_Z(R rho R)=0.                          (6.1)

For positive P-supported rho with trace at most one and `p=Tr(B rho)`, gentle compression gives

    ||rho-R rho R||_1 <= 2 sqrt(p).

Since `||Id-Pi||_(1->1)<=2`, the *actual map norm*, not its expansion coefficients, gives

    ||(Id-Pi)N_Z(rho)||_1
       <=4 ||N_Z*||_cb sqrt(p).                     (6.2)

The same argument holds with any reference. This is the required replacement for the old Hamiltonian/jump-coefficient argument. It also includes local losses without separately counting hypothetical jump supports.

For killing, the full physical generator has CP/TNI compression `L_t^P=Pi L_t Pi` on P: equivalently it is the continuous limit of repeatedly applying the full short-time CPTP propagator and compressing by P. The perturbation summands do not separately need to be GKLS. Since `[P,F]=0`,

    (L_t^P)*(PFP)=P L_t*(F)P-P L_t*(QFQ)P.

The second term is positive by conditional positivity: `QFQ>=0`, its P block is zero, and `P E_(t+dt,t)*(QFQ)P>=0`; divide by dt and take the derivative. This recovers the killed drift deletion inequality without a bounded-norm total Kraus representation. In particular HP alone would not justify this step, which is why the full physical-generator qualification is essential.

The same finite-system-leg expansion proves logical factorization. In canonical coordinates every retained `P A_alpha P` is `I_L tensor a_alpha` by Section 2, P itself is identity on L, and bath maps act trivially on L. Consequently the entire compressed generator is `id_L tensor K_t`, even if its chosen local perturbation decomposition is signed. The physical killing makes its ancillary evolution CP/TNI. Fixed logical-independent initialization gives exactly `a_t id_L` after the specified ideal framed decoder, where `0<=a_t<=1` is input-independent.

Finally, nonempty supports satisfy

    sum_Z ||N_Z,t*||_cb
       <= sum_i sum_(Z:i in Z) ||N_Z,t*||_cb
       <= N_phys eta.                              (6.3)

Nominal terms contribute O(N) total norm, and bath-only terms have zero full-minus-killed difference. Duhamel, contractivity of full joint CPTP propagators and (5.2), (6.2), (6.3) give

    ||E_t Enc-E_t^P Enc||_diamond <= C N t sqrt(N/M).

Trace preservation bounds `1-a_t` by the same error. This yields the accepted decoded form, with no extra factor for the number of noise hyperedges.

## 7. Consequence, strict extension and scope separation

For the accepted fixed Tanner/simple-compiler family choose `ell=c_*N` below both accepted confinement/distance cutoffs, and choose all nominal graph and animal constants independently of the possible noise topology. A fixed sufficiently small eta depending on q and the nominal apparatus yields

    ||Dec_frame E_t Enc-id_L||_diamond
       <= min{2, C N^(3/2) t exp(-cN)}.

The finite-size/vacuum initialization qualification remains covered by the governing whole-receipt elementary extension. Physical site dimensions and nominal support constants may be enormous but remain fixed; the constants are not practical threshold estimates.

This really admits more than fixed noise degree. For example, on N physical qubit sites the Hamiltonian terms `h_ij=eta X_i X_j/[2(N-1)]` have `||i[h_ij,.]||_cb<=eta/(N-1)`. Every site's summed incidence is at most eta, while the noise union has degree N-1. Arbitrary measurable redistribution of a fixed incident norm budget among distant partners is equally allowed. This example is not necessary for the proof but makes the stronger class explicit.

This says nothing about removing conflict geometry from the separate stochastic ancestor/Poisson physical-cell witness theorem. The latter's conflict/coloring combinatorics do not follow from the operator drift proof and retain their separate assumptions and counterexamples. No unbounded-body support, unbounded joint bath strength, mean-energy-only protection, native two-site synthesis, fixed-dimensional Euclidean realization, noisy preparation/readout, or logical-correlated initial bath is newly covered.

## 8. Independent regression and completion record

`check_disconnected_edges.py` exhaustively checks minimum-representative component replacement for path repetition-check examples at n=8 and n=9, including fixed tie-breaking at n=8. It verifies 16,512 edges, including 9,856 disconnected two-site supports, and all 34,504 induced union components. It checks componentwise syndrome equality, the sharp `2(|E intersect K|+|p intersect K|)` bound, containment of old source components, and that a nontrivial kernel component reaches distance. All checks pass.

This is only an algebra regression, not a Tanner confinement test or a quantum-memory simulation. The general proofs above carry the result. A separate subreview independently verified the cb-only boundary estimate, generic local-superoperator logical factorization, and full-physical-generator qualification. No remaining bridge blocker was found, no external state was mutated, and no original source was edited.
