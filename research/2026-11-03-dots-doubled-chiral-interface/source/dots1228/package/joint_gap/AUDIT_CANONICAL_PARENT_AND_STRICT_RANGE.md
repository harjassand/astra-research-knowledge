# Independent audit: same-chirality canonical double, collective gap, and strict-range transfer

2026-11-03. Audited the current `ACTUAL_FAST_PARENT_AND_COERCIVITY.md`, `GRADED_PURIFICATION_AND_STABILITY_ENTRY.md`, `EXPLICIT_JOINT_POLYNOMIAL_LOCALITY.md`, and `PRODUCT_FRAME_STABILITY_AND_SYMMETRIC_TRUNCATION.md`, against the previously audited actual Wilson two-face family. `ROOT_CANONICAL_DOUBLE_PARENT.md` contains an earlier flattened-parent presentation; the strengthened retained-fast-Hamiltonian version is the result assessed here.

## Verdict and precise scope

The collective construction and the specialized strict-range stability bridge survive this audit. The proof is not merely a collection of endpoint transition amplitudes: it supplies an exact product-frame excitation grading, a collective uniform gap, an acquired joint-locality expansion, and the coercivity needed to protect the gap under symmetric finite-range approximation.

The result applies to the specified SAME-CHIRALITY DOUBLED fast system, with the explicitly phase-corrected conjugate decoration, two covariant massed faces (or its gapped half-space limit), bounded rotor operators, and infinite-dimensional L2(S1) rotor factors. The original quadratic free bulk is retained. This does NOT yet imply a finite-qudit regulator, a finite device with an exposed gapless remote surface and the same global gap, or the full anomaly-free/gauging/continuum contract. No practicality or novelty claim follows from this audit.

## 1. Representation and the graded Gaussian convention

The second physical state is psi tensor F psi*, F=exp(i pi N_2/2), when the COMBINED fast state has even parity. The same onsite correction MUST act on the second axial generator and decoration Hamiltonian:

  Q_A,2=F Q_A,1* F dagger,

not minus that operator. The scalar cochain charge therefore retains its sign. The draft now does this explicitly. Purifying separately parity-changing free and decoration factors and dropping their relative phase would not be equivalent; the combined preparation avoids that error.

The Majorana coordinate transformation C=direct_sum(-X) need not itself be orientation-preserving. It is only a coordinate change on the second-copy Majoranas; the physical preparation is the conjugated orthogonal exponential, which has determinant +1 and an even Gaussian lift. This distinction avoids an apparent odd-mode-count parity problem. I independently tested generic even states with n=1 and n=3 fast modes, in addition to the worker/root's even-mode-count checks. Errors were 1.6e-16 and 6.3e-16, with the predicted positive Bell overlaps 2^(-n/2). Results: `audit_odd_mode_purification_results.json`.

There is also an analytic phase check: the covariance rotation is a fixed-angle pure pairing rotation in Bell quasiparticle coordinates. Its vacuum overlap is the positive product of cos(pi/4) factors; thus it selects the same canonical ray as the normalized rank-one projection of Bell, without a phase oracle. The explicit exponential, rather than independent occupied eigenvectors, fixes its lift.

Free matrix conjugation here does not reverse the Wilson root. The declared onsite spin/flavor real-structure intertwiner takes the conjugate hopping matrices back to the same real-space Wilson Hamiltonian. The free vector charges are interchanged, while the axial particle charges are retained. Therefore the mixed A V^2 coefficient is not negated by a V-charge sign exchange. This is not the earlier inverse-anomaly dual-fiber construction. This check concerns the explicit representation and chirality; it is not a blanket classification of every possible interacting lattice SPT invariant.

## 2. Exact collective gap while retaining the physical fast Hamiltonian

Let f_i be the fixed onsite Bell quasiparticle annihilators. After conjugation by the controlled Gaussian W and subtraction of the actual vacuum energy, a quadratic Hamiltonian with Bell as an exact ground state has no scalar or pairing terms. Pair creation would produce an independent two-quasiparticle component when acting on Bell; self-adjointness also removes its adjoint. Consequently

  K_ref(phi)=sum f_i dagger A_ij(phi) f_j,
  g N_Bell <= K_ref <= R N_Bell.

The matrix A is positive and its spectrum is the actual excitation-energy spectrum. The inequality holds on the full Fock space. No flat-band replacement of the physical h has occurred.

With H_rot the independent bounded reset Hamiltonian, K_ref+H_rot preserves N_Bell. Its zero-fast-excitation sector is precisely H_rot; every other sector costs at least g. Thus the untwirled parent has unique finite-volume ground and gap min(g,1), even though K_ref need not commute with H_rot.

The same normal-ordering argument applies to Q_ref=W dagger Q_A W. Exact static charge cancellation makes its Bell-vacuum eigenvalue ZERO, not merely configuration independent. Hence

  Q_ref(phi)=sum f_i dagger q_ij(phi) f_j,

with no scalar and no pairing terms. This is the decisive exact fact: its exponential preserves COMMON N_Bell and acts as identity on its zero sector for EVERY rotor wavefunction, not just the rotor product state.

Therefore the axial-twirled reset Hamiltonian K_rot is positive, preserves N_Bell, and equals H_rot on N_Bell=0. K_ref+K_rot retains the same unique finite-volume ground and gap min(g,1). No interpolation gap or phase-consistency hypothesis was inferred from the earlier endpoint construction.

## 3. Actual excitation coercivity, not a global-gap shortcut

For each rotor site v and axial angle beta, the difference

  D_v=R_beta (1-P_v) R_beta dagger -(1-P_v)

annihilates Bell tensor EVERY rotor state. Conditional expectation onto a ball using Bell outside and any fixed product rotor reference preserves that stronger kernel. Each self-adjoint shell O_X consequently satisfies

  |<O_X>| <= ||O_X|| <1-P_Bell,X>
            <= ||O_X|| sum_(i in X)<n_i^Bell>.

The summable quasilocal shell norms, including center/support counting, give

  -C N_Bell <= K_rot-H_rot <= C N_Bell.

Together with positivity and the fast bound this yields exactly

  c(N_Bell+H_rot) <= K_sym <= C'(N_Bell+H_rot),
  c=min(1,g/(C+1)), C'=max(1,R+C).

All constants are independent of lateral volume and normal thickness when the normal lattice sites remain explicit. This is genuinely stronger than a uniform global gap. Grouping an entire L-layer slab into one site would invalidate the asserted L independence and must not be done. Replacing individual Bell occupation counts by one onsite product-vacuum projector changes only the fixed onsite multiplicity constants.

## 4. Joint locality and the scalar counterterm are acquired

The explicit binomial series is valid:

  sign(h)=sum_k (h/R)c_k(1-h^2/R^2)^k,
  c_k=binom(2k,k)/4^k, q=1-g^2/R^2<1.

Each grouped term has norm <=q^k and degree 2k+1. Its matrix entries have both finite fermion range and finite rotor-coefficient support. Bounding the grouped matrix coefficient is legitimate; expanding and taking absolute values of all walk coefficients would instead create an unnecessary exponential loss. With polynomial ball growth, summing entries, anchors, and support-volume weights costs only powers of k. Thus the displayed weighted interaction series converges for q exp(4 mu r0)<1. This verifies JOINT rotor–fermion locality, not only fiberwise decay.

The controlled Gaussian exponential is therefore a finite-time quasilocal automorphism on the actual combined algebra. It acts on bounded rotor reset kernels without any rotor derivative assumption. Rounding walls cause bounded measurable coefficients, not an unbounded kinetic-energy domain problem.

Likewise, |h|=h sign(h) has degree-2k+2 terms bounded by R q^k. Taking the diagonal internal trace costs the FIXED onsite dimension, never the full volume. This constructs E0_free=Tr(h-|h|)/2 as local scalar densities, with the appropriate additional normal-ordering constants for the actual representation. Do not apply this formula to a redundant BdG matrix without its factor correction.

After subtracting a rotor-independent bulk energy reference, each finite-degree density difference vanishes beyond its hopping distance from the controlled boundary. The remaining tails are summable in normal depth. The counterterm is genuinely quasilocal near the interface. It is not a supplied global ground-energy oracle and does not replace the original quadratic hopping matrix. Its finite-degree approximation is exactly symmetry invariant: diagonal in rotor coordinates for A, and internal-trace invariant under the V-covariant conjugation.

A fully explicit strictly local approximation can use finite polynomial terms and finite-patch evolution of their controlled quadratic generator to dress each rotor reset. Their finite fermionic matrix exponentials give bounded kernels on a finite rotor stencil. Lieb–Robinson estimates control this replacement uniformly. Thus the finite-range construction need not rely on computing a conditional expectation of an inaccessible infinite environment exactly.

## 5. Filtered-spectral-flow stability: independent algebra check

The specialized stability lemma is valid with the acquired coercivity and locality inputs. It is NOT an application of generic stability of arbitrary gapped Hamiltonians, nor a global-form shortcut to Yarotsky's local hypotheses.

Under the provisional gap >=1/2, use an even filter f with integral one and Fourier support strictly inside that gap. For EACH perturbation term V_x,

  B_x=integral f(t) e^(itH_s) V_x e^(-itH_s) dt

has no matrix elements between the ground line and excited spectrum. This remains true for infinite-dimensional onsite rotor Hilbert spaces: it is a spectral-measure statement, not a finite eigensum assumption.

With D_mn=i[1-fhat(E_m-E_n)]V_mn/(E_m-E_n) and S'=i D S, the signs are correct:

  V+i[H_s,D]=sum_x B_x,
  d(S dagger H_s S)/ds=sum_x S dagger B_x S.

The explicit kernel w(t)=sign(t)/2-integral_0^t f(u)du satisfies w'=delta-f and supplies this SAME generator. It is integrable, with ||w||_1=integral |t|f(t)dt. The bump-squared construction gives a compatible positive f and rapidly decaying w.

Each transformed B_x preserves the product vacuum line. Subtracting its own scalar expectation gives A_x Omega=0 EXACTLY term by term. Product-vector conditional shells then annihilate their local product vacuum, yielding

  -epsilon C_stab N <= sum_x A_x <= epsilon C_stab N.

This does not follow merely from annihilation by the total perturbation; the draft correctly establishes the needed termwise statement. Initial support-radius labels and polynomial ball-volume factors must be included in C_stab; they are explicitly accounted for.

Integrating the derivative identity after subtracting the evolving ground energy gives

  S_s dagger H_s S_s-E_s >= K-epsilon C_stab N
                            >=(1-epsilon C_stab/c)K.

Choosing epsilon C_stab/c<=1/4 improves the provisional gap to >=3/4 and prevents the first crossing of 1/2. Bounded isolated-eigenvalue perturbation theory starts this continuation in every finite volume, even though the starting interval from total operator norm could depend on volume. The improved estimate is uniform and extends the interval to s=1. There is no range/threshold circularity: C_stab is fixed in a chosen interaction class BEFORE selecting the final truncation radius.

Spectral filtering generally reduces exponential tails to sufficiently rapid stretched-exponential/almost-exponential tails. One must not claim the filtered flow remains exponentially local. The required polynomial moments are nevertheless finite, and the locality constants are uniform for a fixed bootstrap gap and interaction-norm bound. This is enough for the proof.

## 6. Strict range, symmetry, and retained bulk

Keep H_fast EXACTLY. Approximate only the scalar counterterm and dressed reset interactions, then apply the exact bounded-depth axial twirl (and V twirl if necessary). The resulting Hamiltonian is strictly finite range; twirling enlarges support by only a fixed circuit radius. Positivity of each dressed-reset term survives. The whole approximated Hamiltonian need not have the original ground exactly, which is precisely why the stability argument is required.

The difference from the quasilocal parent is small in a fixed, slightly weaker weighted interaction norm. Conjugating by W preserves smallness in another fixed weaker norm. Choose the range only after fixing the stability threshold. This is a valid application of the preceding lemma.

Because reset centers lie on the interface and finite-degree counterterm densities have finite walk support, the final additional interactions vanish beyond a finite interface strip (apart from removable constant bulk energy densities). The original free quadratic bulk remains literally unchanged there. This is stronger than merely preserving its spectrum or phase.

## 7. Half-space passage and limits of the conclusion

The audited two-massed-face single-particle gap holds uniformly for every L>=2. Polynomial local data and the controlled generators therefore converge locally as the remote face recedes; their uniform tails give convergence of the corresponding quasilocal automorphisms. The same fixed truncation/stability constants work for all L when four-dimensional lattice geometry is retained.

For local observables, the finite-volume ground-state gap inequality passes to the canonical half-space state by local convergence and summable commutator tails. It supplies a gap in that state's GNS representation. There is no normalizable infinite-volume W|product> vector in a single finite Fock space being assumed. Statements about an infinite global ground-energy trace or total charge must be replaced by densities, symmetry automorphisms, and relative indices.

Removing the far mass in a FINITE slab is a different operation and deliberately creates gapless remote degrees of freedom. The two-face global-gap theorem cannot be retained after that deletion. A separate attachment/decoupling analysis is needed for a finite chiral device. Likewise this argument supplies no physical momentum cutoff of the rotor factors and no Standard Model or continuum theorem.

## Primary machinery checked

Nachtergaele–Sims–Young, arXiv1810.02428v2, explicitly treats infinite-dimensional onsite factors, locally normal product-state localizing maps, transformed interactions, and spectral-flow locality; relevant sections are 3–6, Proposition4.5, Lemma5.1, and the spectral-flow theorems. https://arxiv.org/html/1810.02428 . The application here uses bounded interactions throughout.

Michalakis–Zwolak, arXiv1109.1588v3, SectionV supplies the termwise filtered ground-projector strategy and SectionVI the local-annihilation relative-bound strategy. https://arxiv.org/pdf/1109.1588 . Their general stability hypotheses are not imported wholesale: exact product-vacuum localization and the independently acquired coercivity replace that step in the present deduction.

The graded even-fermion extension is implemented with even product reference states and even interactions: disjoint even operators commute, and localizing maps preserve parity. There is no nonlocal Jordan–Wigner substitution or normalized infinite-dimensional trace in the proof.
