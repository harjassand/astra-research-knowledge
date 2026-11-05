# Uniform equilibrium correlation decay does not give a computable finite-size crossover

Research addendum, 5 November 2026. Provisional proof; external peer review outstanding.

## Status and result

This note is conditional on the fixed-temperature construction and its all-translation-invariant-state conclusion in the delivered provisional manuscript *Exact accepting polymers and a fixed-temperature undecidable order parameter in two dimensions*. It does not provide an independent verification of that base theorem. The new steps below are the finite-volume boundary experiment, its exact pre-certificate behavior, the averaged-DLR limit, and the computability reduction. These steps do not assume full Gibbs uniqueness, spin FKG for the induced interaction, or a convergence theorem for centered boundary states.

**Main corollary.** In the base theorem's effective family of two-dimensional, finite-range, finite-integer-energy models at inverse temperature one, there is an explicitly prescribed finite-volume equilibrium experiment with a computable statistic m_M(L) such that:

1. If M never halts, m_M(L) > 0.9999999 for every L.
2. If M halts, m_M(L) tends to zero as L tends to infinity.
3. In either branch, m_M(L) > 0.9999999 whenever no accepting computation rectangle fits in the L by L box. The complete finite-volume spin law, not merely this statistic, then equals the law of two independent low-temperature Ising boxes with opposite fixed spin boundaries.
4. No total computable function of the compiled model description can give an upper bound on the eventual crossover index for every halting input. Even a total computable upper bound on the first crossing below 1/4 is impossible.

In the halting branch, nevertheless, all translation-invariant Gibbs states obey the same machine-independent equilibrium estimate

    |E_mu[O_0 O_x]| <= 10 (0.03)^{||x||_infinity},
    E_mu O = 0.

The conclusion concerns a specified opposite-boundary thermodynamic experiment. It is not a claim of sample complexity, Markov-chain mixing time, physical preparation time, arbitrary-boundary strong spatial mixing, or a numerical lower bound for a particular laboratory material.

## 1. The actual finite-volume boundary gas

Use the base construction's site alphabet and physical variables:

- spins s_v,r_v in {−1,+1};
- multiplicity b_v in {1,...,D};
- an auxiliary group variable g_e on each nearest-neighbor lattice edge;
- mismatch cost K=6 in each spin layer;
- a site energy E_v in {0,1}, reading the four incident group variables, b_v, and the equality indicator 1[s_v=r_v].

Let Lambda_L = {1,...,L}^2. Let E_L be the set of unoriented nearest-neighbor edges having at least one endpoint in Lambda_L. The experiment sums over all spins and b variables at sites of Lambda_L, and over all group variables g_e for e in E_L. Give the group variables counting measure, equivalently independent uniform reference measure after dropping a spin-independent constant. Fix exterior spins to

    s_v = +1,  r_v = −1,  v outside Lambda_L.

The finite Hamiltonian is exactly

    H_L = sum_{v in Lambda_L} E_v
          + 6 sum_{{v,w} in E_L} [1(s_v != s_w) + 1(r_v != r_w)].

No site factor centered outside Lambda_L is included. In particular the dangling group variables are summed freely, rather than fixed to the group identity or constrained by exterior tile factors. This distinction is essential for the exact Fourier identity.

This is a legitimate open/mixed-boundary physical gas. It is not falsely identified with the full fixed-exterior DLR kernel on precisely Lambda_L. In the ordinary site storage of the base model, the east and north group variables are owned by their lower/left endpoint. Consequently some west/south dangling variables are stored in a one-site exterior collar. Sample those coordinates as specified and set all other exterior coordinates arbitrarily, consistently with the fixed exterior spins. This embeds the experiment as a probability measure nu_{M,L} on the full physical configuration space S_M^{Z^2}.

All differences from an ordinary finite-box restriction are confined to a fixed-width collar. More precisely, for every finite set A such that every interaction meeting A is included among the terms of H_L and every variable in A is free, nu_{M,L} satisfies the full physical DLR equation on A exactly. In particular this holds whenever the fixed interaction neighborhood of A lies inside Lambda_L.

Define the observable and the measured statistic by

    O_v = (s_v − r_v)/2,
    m_M(L) = (1/L^2) sum_{v in Lambda_L} E_{nu_{M,L}} O_v.

For every fixed M and L this is a uniformly computable real: it is a ratio of explicit finite sums of integer multiples of exp(−n), with a strictly positive denominator. This statement makes no claim that brute-force evaluation is efficient.

## 2. Exact behavior before an accepting rectangle fits

Recall t=|T_M|, C0=10000(t+1), D=C0+t, and

    C = C0 + t exp(−1),
    a = (1−exp(−1))/C.

Summing each b_v gives C(1+a F_v). Uniformly summing all g_e, including the dangling ones, makes every unmatched nonzero edge color vanish by character orthogonality. The exact finite-volume spin weight is therefore

    exp(−H_Ising,L^{+,-}(s,r)) Xi_{M,L}(s,r),

up to the spin-independent factor C^{L^2}|G|^{|E_L|}, where

    Xi_{M,L}(s,r)
      = sum_{P compatible, accepting rectangles contained in Lambda_L}
          product_{gamma in P} a^{|gamma|} 1[s_anchor(gamma)=r_anchor(gamma)].

This is the actual partition factor of the chosen physical boundary gas. No conditional infinite-volume polymer gas has been substituted for it, and no crossing polymer is silently omitted from an infinite-volume conditional specification. The omission of exterior site factors and the free dangling integration are what impose zero exterior tile colors and confine every selected finite component to Lambda_L.

Let R_M be the least L for which an accepting rectangle can fit in Lambda_L, with R_M=infinity if none exists. If L<R_M, the only polymer collection is empty, so Xi_{M,L}=1 identically. Hence

    Law(s,r) = mu_{Ising,L}^{+} tensor mu_{Ising,L}^{−}

exactly. This equality applies to every spin observable in the box. It does not say that all auxiliary-variable distributions are identical between different machines.

The elementary plus-boundary Peierls estimate in the base manuscript is uniform in L and in the site v:

    P_{mu_{Ising,L}^{+}}(s_v=−1) <= epsilon,
    epsilon = 4 sum_{n>=4} n [3 exp(−6)]^n
            < 4.94 times 10^(−8).

Spin-flip symmetry gives E_{mu^-} r_v = −E_{mu^+} s_v. Therefore, whenever L<R_M,

    E O_v = E_{mu_{Ising,L}^{+}} s_v >= 1−2 epsilon,
    m_M(L) >= 1−2 epsilon > 0.9999999.                 (2.1)

The no-halting branch has R_M=infinity, so (2.1) holds at every size. If M halts after T_M actual transitions, the compiler's tableaux have one initial row and one row per transition, and minimum height two. Thus

    R_M >= max(2,T_M+1).

No estimate on the required tape width is needed for this lower bound.

## 3. Why the spatial average tends to zero for a halting machine

The all-TI theorem does not justify assuming that a centered limit of opposite-boundary boxes is translation invariant. We use explicit translation averaging instead.

Let theta_x view a full configuration from site x, and set

    bar_nu_{M,L} = (1/L^2) sum_{x in Lambda_L} (theta_x)_* nu_{M,L}.

The alphabet S_M is fixed and finite for each fixed M. The space of probability measures on its full configuration space is weakly compact. Therefore every sequence of L tending to infinity has a weakly convergent subsequence of bar_nu_{M,L}.

### Translation invariance

For every bounded continuous f and fixed lattice vector y, the difference between the averages indexed by Lambda_L and Lambda_L+y is bounded by

    ||f||_infinity |Lambda_L symmetric_difference (Lambda_L+y)| / L^2,

which tends to zero. Every weak limit is translation invariant.

### Physical DLR property

Fix a finite update set A and a local test function f. Let gamma_A be the full physical Gibbs kernel. The physical interaction is finite range with finite energies, so gamma_A f is continuous and depends on finitely many coordinates.

For all shifts x except those for which the interaction neighborhood of A+x reaches the boundary collar, the finite experiment satisfies the physical DLR equation on A+x exactly. The number of exceptional shifts is O_{A}(L). Therefore

    |bar_nu_{M,L}(f) − bar_nu_{M,L}(gamma_A f)|
      <= 2 ||f||_infinity O_A(L)/L^2 -> 0.

Passing to a weak limit gives the DLR identity for each finite A and each local f. Local functions determine probability measures, so the limit is a Gibbs measure for the original physical interaction. This argument needs neither an induced-spin effective interaction nor an infinite-volume boundary-gas identification.

### The scalar limit

By construction,

    bar_nu_{M,L}(O_0) = m_M(L).

If M halts, every subsequential limit just obtained is a TI physical Gibbs state, and the base theorem says its O mean is zero. If m_M(L) failed to tend to zero, a subsequence bounded away from zero would have a further convergent measure subsequence, contradicting that assertion. Hence

    M halts => lim_{L->infinity} m_M(L)=0.             (3.1)

No monotonicity in L is asserted.

## 4. The precise noncomputable bound

For a halting input define

    N_M = min{N>=1: |m_M(L)| <= 1/4 for every L>=N}.

Equation (3.1) makes N_M finite. Equation (2.1) gives N_M>=R_M. Let D_M denote the effective compiled description, including its designated observable and boundary protocol. The compiler produces D_M without knowing whether M halts.

**Theorem.** There is no total computable B from finite model descriptions to positive integers satisfying

    N_M <= B(D_M) for every halting M.                (4.1)

**Proof by numerical discrimination.** On input M compute D_M and L=B(D_M). Approximate the finite sum m_M(L) with error at most 1/16. If M halts, (4.1) gives |m_M(L)|<=1/4, so the approximation is at most 5/16. If M does not halt, (2.1) makes the approximation greater than 0.9374. Comparing with 1/2 decides halting. This is impossible. All numerical comparisons have a fixed positive gap.

**Equivalent exact proof.** Enumerate all tile assignments in Lambda_{B(D_M)} and check the finite matching and accepting conditions. A nonhalting input never yields a certificate. A halting input must yield one: otherwise (2.1) contradicts |m_M(B(D_M))|<=1/4. This is again a halting decision procedure.

The same argument rules out a total computable bound on

    kappa_M = min{L>=1: m_M(L)<=1/4},

which exists for every halting input: kappa_M>=R_M, so any proposed bound permits a finite certificate search. This stronger first-crossing obstruction avoids treating an eventual-tail index as something directly computable from its finite initial values.

### Quantifiers that must not be weakened or exaggerated

- B must be total on all compiled descriptions, with its guarantee required only on halting inputs. A partial procedure that is allowed to run forever on nonhalting inputs is not excluded; simulating M already finds an accepting certificate when one exists.
- Neither the exact N_M nor its partial computability is claimed. Recognizability of halting does not compute an exact eventual-tail index.
- The same contradiction excludes bounds depending only on alphabet size, description length, the fixed interaction support, the fixed energy scale, and the universal odd-correlation constants: these data are computable from M, so composing with such a bound gives B.
- At each fixed alphabet size there are only finitely many bounded-integer energy tables on the fixed support shapes. Thus their halting crossover indices have some finite maximum. The result is that there is no computable envelope of these maxima as the alphabet/description grows, not that one fixed alphabet supports arbitrarily large crossovers in this family.
- If BB(n) is the largest halting time among programs of length at most n in the chosen effective machine encoding, then max_{|M|<=n, M halts} N_M >= BB(n)+1. To reindex by physical-description length one must retain the computable compiler size overhead. No fixed-local-dimension Busy Beaver claim is made.
- The plateau is exact for the finite spin marginal relative to the two-Ising benchmark, not an indistinguishability theorem between arbitrary different Hamiltonian descriptions or all auxiliary measurements.

## 5. Two useful companion consequences

### 5.1 The original family never has full Gibbs uniqueness

This is a limitation of the construction, not an unproved assertion that full uniqueness might follow from its odd-observable theorem.

Repeat the finite-volume experiment with both exterior spin layers fixed plus. For each polymer collection its finite Edwards–Sokal representation is the two-layer FK model with vertical equality edges and the spin boundary wired to plus. Conditional on the polymers and all horizontal edges but one, a horizontal edge opens with probability either p or p/(2−p), where p=1−exp(−6). Thus its probability is at least

    q_1 = tanh(3).

This elementary finite-volume bound does not require the infinite-state recoloring lemma. It supplies iid Bernoulli(q_1) lower bonds in each layer. A site disconnected from the wired boundary is enclosed by a closed dual contour. The base manuscript's contour count gives

    P(site not connected to the plus boundary)
      <= delta = 4 sum_{n>=4} n [3(1−q_1)]^n
               < 7.90 times 10^(−7).

Being connected forces its spin plus; consequently each layer's minus-spin probability is at most delta. Translation-averaged subsequential limits are TI physical Gibbs states by Section 3, with common observable A=(s+r)/2 satisfying E A>=1−2 delta. The global simultaneous spin flip produces a distinct TI state with E A<=−1+2 delta.

For any two sites a union bound on the four spins in the plus-boundary experiment yields E[A_0 A_x]>=1−8 delta; the inequality survives the averaged limit. The equal mixture of the two globally flipped states has E A=0 and the same nondecaying two-point lower bound. This works for every machine, including halting machines. Therefore neither full Gibbs uniqueness nor all-observable correlation decay is an extension of the existing family. Achieving either would require a materially different construction and proof.

### 5.2 Computable pressure, undecidable directional differentiability

Add the real on-site field −h O_v, and let p_M(h) be the infinite-volume pressure. This field is only a probe; the integer-energy undecidability instance remains at h=0. The pressure is even, convex, and 1-Lipschitz in h.

Its values are uniformly computable with a simple surface estimate. Use ordinary free physical boxes, including exactly those interaction terms whose supports lie entirely in the box, and write p_{M,L}^{free}(h)=L^(−2) log Z_{M,L}^{free}(h). Tile a much larger square by L by L blocks. Each block contributes at most 2L crossing nearest-neighbor pairs of energy at most12, and at most2L crossing site factors of energy at most1. On-site probe fields do not cross block boundaries. Thus

    p_{M,L}^{free}(h) − 26/L <= p_M(h) <= p_{M,L}^{free}(h).   (5.1)

This holds uniformly in M and h. Finite partition functions are computable for computable h, so the pressure values are computable. The running time of finite-volume enumeration is not claimed to be uniform polynomial time.

The full-shift finite-range Gibbs variational principle identifies equilibrium measures with TI Gibbs measures. The one-sided derivatives of pressure obey

    p'_{M,+}(0) = max_{mu in G_TI(M)} E_mu O,
    p'_{M,−}(0) = min_{mu in G_TI(M)} E_mu O.

For completeness, this follows by writing p_M(h)=max_mu[F_M(mu)+h mu(O)]. The TI measure space is compact, entropy is upper semicontinuous, and mu(O) is continuous. A maximizing sequence at h approaching zero has an equilibrium subsequential limit at zero. The upper and lower secant bounds then give the displayed extrema.

If M halts, both derivatives are zero. If M does not halt, the product plus/minus and minus/plus phases give slopes above 1/2 and below −1/2. Therefore

    p_M is differentiable at h=0 iff M halts.

Directional differentiability at a fixed field is undecidable in this computable pressure family, even though pressure values have the explicit uniform finite-size error (5.1). This is not full differentiability as a functional of all perturbations, and does not imply uniqueness. No analyticity, field radius of analyticity, or linear-response identity is inferred from the odd-correlation bound alone.

## 6. Relation to known results and remaining scope

The general message that finite-size extrapolation can fail below an enormous crossover is not new. Bausch et al., *Size-driven quantum phase transitions*, PNAS 115 (2018), 19–23, construct quantum models with sharply different small- and large-system behavior; their thermal discussion requires a suitable low temperature and a precision-dependent comparison. The present conditional corollary has a different setting: a fixed positive temperature, classical finite integer energies, an exact finite-volume spin plateau, and a machine-independent exponential bound for the selected infinite-volume odd correlations. It is not advertised as a new general concept of size-driven behavior. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC5776787/ .

Bausch, Cubitt and Watson, *Uncomputability of phase diagrams*, Nature Communications 12, 452 (2021), also emphasize failures of finite-size phase-diagram extrapolation in quantum constructions. This note does not upgrade those results or claim their finite-temperature scope. Source: https://www.nature.com/articles/s41467-020-20504-6 .

Computability of pressure for computable finite-range lattice models is a known result, not a novelty claim here. See Gayral, Sablik and Taati, *Characterisation of the set of ground states of uniformly chaotic finite-range lattice models*, Nonlinearity (2025), Proposition 14; their result is broader than the elementary surface estimate needed in Section5.2. Author manuscript: https://lgayral.pages.math.cnrs.fr/articles/GaySabTaa25.pdf .

The new deliverable is the exact corollary and its boundary/DLR/quantifier proof, conditional on the base construction. Its foundational content is the separation between an infinite-volume selected-observable correlation length and a total computable certificate of finite-size thermodynamic reliability. It supplies no mechanism for physical hypercomputation: no finite observation can certify the no-halting branch, and no uniform computable stopping bound exists.

## 7. Verification record

An independent internal proof audit checked the actual boundary variables, the averaged physical DLR argument, the first-crossing and eventual-tail quantifiers, alphabet dependence, the common-sign nonuniqueness argument, and the pressure surface and derivative claims. It found no fatal issue in these corollaries. This remains an internal proof audit, conditional on the base manuscript, not external peer review or formal verification.

`check_constants.py` certifies the contour-series inequalities with exact rational arithmetic, checks the separated numerical thresholds, and exhaustively sums the single-layer plus-boundary Ising partition function for sides 1–4. Its results are saved in `numerical_checks.json`. The recorded base-manuscript hash identifies the provisional version used to derive the addendum. These checks certify the displayed numerical inequalities and check the finite Ising benchmark with floating-point sums only; they do not validate the base theorem or establish the asymptotic claims numerically.
