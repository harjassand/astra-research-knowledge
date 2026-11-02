# Independent audit: asymmetric source–defect character bounds

2026-11-02. Reviewer: `producer-workspace/audit_exact_trace_polymer_gas`.

## Decisive result and scope

**The compressed decoder closes the source-to-defect row. Its naive reverse row can be superlinear and is NOT adequate. Both rows can nevertheless be closed for the SAME exact scalar-character interaction, using different upper bounds in the two directions.**

Use the actual interaction

    f(B,tau)=chi_B(tau)-1,

not an interaction declared whenever ANY intermediate compressed pairing occurs. For a stabilizer source B, a nonzero actual interaction implies BOTH:

1. contact with some NONZERO correction port in the compressed decoder pairing;
2. contact of the physical defect leaves with any chosen actual-check stabilizer filling of B.

Use (1) only for the source row and (2) only for the defect row. The latter costs a polynomial number of source-root placements at fixed source size, not an exponential of the filling volume. This gives linear charges in BOTH species under the precise hypotheses below.

**No symplectic/isometric lift identity is assumed or needed.** The transpose pairing is an exact matrix identity. The adjoint growth constant is a bound on ROW norms of the lifts, not automatically the existing COLUMN-norm lift constant K.

This is a completed scalar-character mixed-KP sublemma. It is NOT a proof that the annealed quantum source expansion has the required exact scalar factorization or beta-uniform rooted activities. Those are separate analytic premises.

## 1. Exact phase identity and common-lift scope

Write Pauli vectors over F2 and let Omega be the physical symplectic form. Let B be a physical stabilizer Pauli, including a possible fixed scalar phase. Normalize its syndrome character by its ground-sector eigenvalue. For any actual-check filling b_B,

    B / ground_eigenvalue(B) = product_a S_a^(b_B,a),
    chi_B(tau)=(-1)^(b_B dot tau).

If D(tau) is any correction with syndrome tau, then

    chi_B(tau)=(-1)^[B,D(tau)].

Indeed D takes a ground-sector state into sector tau, and commuting B past D produces precisely this eigenvalue ratio. Logical or stabilizer ambiguities in the correction do not matter because B itself is a stabilizer.

The admitted common-lift decoder has a binary correction decomposition

    D(tau)=sum_i L_i c_i(tau),

where L_i is the FIXED product of common cochain lifts from processing scale i to the physical scale. Include the finite terminal correction as a final summand. In the opposite sector, include the fixed local G map in L_i, and add the local H^2 tau summand separately. Phases of products of correction Paulis do not affect commutation.

Thus exactly

    [B,D(tau)] = sum_i (L_i^T Omega B) dot c_i(tau).

The expression L_i^T Omega B is merely a linear functional on the scale-i correction-coordinate space. That space need not have its own symplectic structure. In a one-type CSS sector this is the ordinary opposite-type dot pairing and Omega can be suppressed in notation.

In particular we NEVER use L_i^T Omega L_i=Omega, nor infer such an identity from cochain/logical equivalence. Fixed common lifts make the functional source-dependent but defect-independent. A branch-dependent-lift decoder would need a new argument or a larger explicitly charged union of possible adjoints; it is not silently covered here.

The source must genuinely be scalar on the code sector: a known stabilizer word is enough. Subdistance closed source words are stabilizers by the admitted distance theorem. An unidentified closed logical word is not covered by this scalar character argument.

## 2. Precise sufficient hypotheses

Let eta be a canonical contact-completed defect polymer, with physical occupied leaf syndrome tau_eta and mass M(eta)=|tau_eta|. Assume the already audited exact trace gas and:

**D1. Rooted entropy and activity.** For every typed trace vertex v, the number of mass-M canonical polymers containing v is at most A^M. Defect activity obeys

    |z_eta| <= exp(-beta epsilon_min M(eta)), epsilon_min>0.

**D2. Nonzero correction ancestry.** If the actual scale-i correction of eta has a nonzero coordinate, then

    M(eta) >= theta 2^i

for a uniform theta>0. The index i is the occupied PROCESSING scale, with the uniformly bounded intermediate-stage offset absorbed into theta. A ghost port at geometric height i is NOT enough.

**D3. Adjoint growth.** For a source S of size m with physical Pauli B_S supported on at most b m sites,

    |supp(L_i^T Omega B_S)| <= C_L m R^i

for fixed finite R>=1, C_L. The local H contribution satisfies the corresponding scale-zero bound. A product of uniformly row-sparse common lifts supplies D3; the actual bounded local chart maps have uniformly bounded row and column norms. A bound on columns alone would NOT supply it. R need not equal the correction support/lift column constant K.

**S1. Anchored local sources.** Each source S has a chosen physical root x_S, size m>=1, and spatial support of diameter at most C_s m around that root. Its data Pauli B_S is supported inside that source footprint. Bath-only sources with B=I have no character interaction. Fixed-range dressing only changes C_s.

**S2. Rooted source activity bound.** After including all time/internal labels and any desired source charge a_s m, the activities admit a uniform rooted bound of the form

    sum_(S: root=x, size=m) |w_S| <= C_s q^m.

Equivalently one may keep the e^(a_s m) tilt explicitly below. This is an ASSUMED analytic source estimate, not derived here from annealed Holder. If q itself grows like beta v, this lemma does not make it beta uniform.

**S3. Polynomial anchored stabilizer filling and root density.** Every B_S admitted to this scalar class has an actual Hamiltonian-check filling supported within physical distance R_fill(m)<=C_f(1+m)^p of supp(B_S). Physical source roots have polynomial ball growth, uniformly in volume (including any environment): the number of possible roots in a radius-r ball is at most C_r(1+r)^D.

The admitted filling theorem gives p=6 as a crude radius bound for each CSS sector; mixed Paulis are filled sectorwise. It explicitly uses ACTUAL check generators, not new checks. Bounded physical cell/check density and bounded-density finite-range local environments provide the required root growth. Bounded graph degree ALONE would not suffice: exponential ball growth at radius m^p could destroy the reverse estimate.

## 3. Why nonzero correction ancestry is valid

The selected full-trace component has the earned complete-owner charge recurrence

    Q_i(eta) <= 2^(-i) Q_0(eta) <= C 2^(-i) M(eta). A nonzero correction at processing scale i is supplied by an occupied layer component, whose input charge is at least one. No syndrome-dependent correction exists without its charged input owner, and the terminal decoder is zero on zero. Therefore 1<=Q_i(eta), yielding M(eta)>=2^i/C.

For an intermediate layer before/after the halving portion of a macrostep, changing i by a fixed integer only changes theta. For the opposite-sector prepass, Q_0^dual<=C_F |tau_eta| gives the same conclusion with a different theta. Local H corrections are scale zero. Potential correction ports with actual value zero do not imply this lower bound and are never used in the density estimate.

## 4. Source-to-defect row: exponential tail at each processing scale

Choose defect charge a_d M and set

    t = beta epsilon_min - a_d - log A > 0.

At a fixed correction port v at processing scale i, D1–D2 give

    sum_(eta: c_i(eta)[v]=1) |z_eta| e^(a_d M(eta))
      <= sum_(M>=ceil(theta 2^i)) exp(-t M)
      <= exp(-t theta 2^i)/(1-exp(-t)).

If f(B_S,tau_eta) is nonzero, the full parity pairing is odd. Hence at least one individual pairing has a common nonzero port. Union bounding those ports and applying D3 proves

    sum_eta |f(B_S,tau_eta)| |z_eta| e^(a_d M(eta))
      <= [2 C_L/(1-exp(-t))] m
           sum_(i>=0) R^i exp(-t theta 2^i)
      =: kappa_D(t) m.

The series is finite for every t>0. For fixed local constants it tends to zero as t tends to infinity. Uniformity in hierarchy depth follows by bounding the finite sum by this infinite one. Local H/direct terms can be included at i=0; a bounded number of sector/intermediate-layer types changes C_L.

This estimate honestly handles polynomially enlarged physical fillings without placing that whole filling in the source row. It uses thermally suppressed NONZERO high-scale corrections, not every halo port.

## 5. Why the naive reverse compressed-contact row fails

The correction support estimate gives roughly

    |c_i(eta)| <= C M(eta)/2^i.

A single scale-i correction coordinate can lift to K_col^i physical sites. Bounding all microscopic sources through this physical support therefore gives

    constant * M(eta) sum_(i<=log2(C M)) (K_col/2)^i.

This is superlinear when K_col>2, and logarithmically superlinear at equality. Worse, many such apparent contacts may cancel in the total phase. A small actual stabilizer generator, for example, measures one physical syndrome coordinate even if its pairings with individual correction scales are numerous.

Thus the interaction must NOT be replaced by the union of compressed contacts in the exact gas. The source-row union bound is only an upper bound for the actual interaction.

## 6. Defect-to-source row: use the independent filling certificate

For the SAME exact interaction, the physical filling identity gives

    f(B_S,tau_eta) != 0 => b_(B_S) dot tau_eta = 1
                       => supp(b_(B_S)) intersects supp(tau_eta).

Choose a physical occupied defect check j in this intersection. By S3, j is within C_f(1+m)^p of some site in supp(B_S). By source connectivity S1, the source root x_S is therefore within

    R_*(m)=C_f(1+m)^p+C_s m+O(1)

of j. There are at most P(m)=C(1+m)^(D max(p,1)) such possible source roots. The precise exponent is immaterial; its being a fixed polynomial is essential.

Using the rooted source activity bound and summing over the M physical defect leaves gives

    sum_S |f(B_S,tau_eta)| |w_S| e^(a_s m(S))
      <= 2 C_s M(eta) sum_(m>=1) P(m) (q e^(a_s))^m
      =: kappa_S(q,a_s) M(eta).

This is finite when q e^(a_s)<1 and tends to zero as q tends to zero. The number of filling generators does not appear inside an exponential. Different possible placements or internal source words are already counted in the rooted activity estimate. A source is overcounted if it meets several leaves, which is harmless for this upper bound.

An existential filling with the uniform anchored radius is enough: choose one deterministically for each B if desired. Different actual-check fillings yield the same character on valid syndromes. We do not count all fillings as independent source labels.

Crucially, the source-row and defect-row estimates are different majorants of the SAME |f|. There is no requirement to use one symmetric geometrical upper bound for both. Taking the UNION of the two majorant contact relations would lose the result. The exact relation, or their INTERSECTION as a common support majorant with |f|<=2, is adequate.

## 7. Conditional mixed-gas consequence

Suppose, additionally, an exact scalar source representation has been earned of the form

    Z = sum_(compatible defect collections Gamma)
        sum_(compatible source collections Lambda)
        product_eta z_eta product_S w_S
        product_(S,eta) chi_(B_S)(tau_eta).

Here same-species incompatibilities may be ordinary hard-core, and any other stated same-species factors must satisfy their own cluster hypotheses. This exact product formula is NOT obtained merely from an annealed absolute coefficient bound.

For the displayed character gas, cross Mayer factors are f=chi-1 in {0,-2}. Although their absolute value can be 2, |1+f|=1. Same-species hard-core factors have |1+f|<=1 as well. A connected-graph/tree partition identity therefore gives the usual tree majorant: every nontree factor has modulus at most one, leaving a product of |f| on the tree edges. The ordinary rooted-tree KP induction applies with these weighted Mayer edges.

Assume the self-species rows consume at most half the linear charges:

    defect self row <= (a_d/2) M,
    source self row <= (a_s/2) m.

The two audited mixed estimates complete the row conditions whenever

    kappa_D(t) <= a_s/2,
    kappa_S(q,a_s) <= a_d/2.

Choose beta sufficiently large for the first inequality and q sufficiently small for the second, with strict margins. This gives absolute mixed connected/Ursell convergence for the stated exact scalar gas, uniformly in volume and hierarchy depth. The reverse bound is environment-volume uniform only under the explicit root-density/locality premise.

## 8. Remaining analytic gate: do not overclaim

The scalar-character row obstruction is resolved by this asymmetric argument. The following do NOT follow from it:

- an exact quantum annealed source gas with independent, syndrome-independent activities w_S;
- simultaneous preservation of the annealed positive-trace Holder bounds under a Fourier/Pauli decomposition and complex interpolation;
- beta-uniform smallness of q at fixed perturbation strength;
- treatment or resummation of source words acting nontrivially on the logical sector;
- an operator/source-derivative estimate in place of a scalar character gas;
- endpoint/witness insertion bounds without their corresponding marked activity estimates.

The exact contact-completed defect gas and both mixed scalar rows are now available. The full native generic-perturbation phase claim still requires the actual source representation and its temperature-uniform activity control.

## Reviewed anchor for the physical filling premise

`producer-workspace/ALGEBRA_AND_FILLING_THEOREM.md`, Sections 6–7: actual X-check filling radius at most C m^6; opposite-sector actual Z-check filling through one bounded local duality application; final paragraph explicitly extends anchor locality to complete physical check support. The actual-family audit's native substitution supplement explicitly uses bounded check density to convert polynomial radius into a polynomial candidate-anchor bound. These are forward locality statements, not an inverse-Lipschitz or symplectic-lift assumption.
