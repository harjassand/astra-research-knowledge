# Product-frame stability and exact-symmetry finite-range truncation

## Status and what is NOT assumed

This is a proof bridge for the specific collective-parent construction. It does not assert stability of arbitrary gapped Hamiltonians, and does not assume that W is finite depth. Its inputs are a volume-uniform quasilocal unitary W, an exactly symmetric state Psi=W Omega, and the stated bounded-interaction locality estimates. The separate Gaussian construction must actually establish those inputs in the JOINT rotor–fermion operator norm, not only for each fixed rotor fiber.

The proof is dimension-independent at the onsite Hilbert-space level: product-vector conditional expectations and bounded-operator Lieb–Robinson/spectral-flow estimates work for L²(S¹) rotor factors. No charge cutoff is used here.

## 1. Setup and the excitation-number comparison

Let the actual site graph have polynomial ball growth v(r)=sup_x |B_r(x)|. To obtain bounds uniform as normal slab thickness L grows, KEEP the normal direction as explicit 4D lattice sites with a fixed number of fermionic factors per UV site. Rotor factors occur only on the designated coarse boundary sites; their coupling stencil may have the already-paid large fixed UV refinement radius. Do NOT package an entire L-layer slab into one site and then claim L-independent constants. Fixed UV/coarse refinement and fixed onsite factor multiplicity give volume/L-independent locality constants. Choose an even product vector Omega=⊗_x Omega_x and

    q_x=1-|Omega_x><Omega_x|,    N=sum_x q_x.

Using sums of individual rotor-reset and Bell projectors instead merely changes fixed onsite comparison constants. First consider Hpar=W N W†; Section1b below treats the strengthened original-fast-Hamiltonian parent. Let U_beta be the actual axial symmetry, with uniformly finite-depth bounded-range action, and assume U_beta Psi is a phase times Psi. Define

    R_beta=W† U_beta W,
    Hsym=integral U_beta Hpar U_beta† d beta,
    K=W† Hsym W=integral R_beta N R_beta† d beta.

Each R_beta preserves the product vacuum line. Each conjugated N has a unique vacuum and gap one, so K has that same vacuum and gap at least one, without invoking stability.

Assume R_beta and its inverse obey uniform quasilocal estimates. In particular, for A_x(beta)=R_beta q_x R_beta† and the product-vacuum conditional expectation E_r onto B_r(x), suppose

    ||A_x(beta)-E_r(A_x(beta))|| <= a(r),

uniformly in volume,x,beta, with sum_r v(r)a(r)<infinity (exponential tails suffice).

E_r is id_inside tensor the vacuum state on the exterior. It is a unital completely positive norm contraction, and is well defined with infinite-dimensional onsite factors. Since A_x Omega=0,

    E_r(A_x) Omega_Br=0.

Set D_0=E_0(A_x), D_r=E_r(A_x)-E_(r-1)(A_x). Then ||D_0||<=1 and ||D_r||<=a(r)+a(r-1). Each self-adjoint D_r annihilates the local vacuum projector P_Br. Consequently

    -||D_r|| N_Br <= D_r <= ||D_r|| N_Br,
    N_Br=sum_(j in Br) q_j.

Summing the telescoping decomposition and then x gives

    R_beta N R_beta† <= C N,
    C=1+sum_(r>=1) v(r)[a(r)+a(r-1)].

Apply the same estimate to R_beta† and conjugate it to obtain the reverse inequality. Thus

    c N <= K <= C N,     c=C^(-1).

This is an excitation-number form estimate, not merely a spectral gap. The proof is volume uniform and does not involve onsite dimension.


## 1b. Retaining the original quadratic fast Hamiltonian

The physically stronger parent is

    Hpar=Hfast-E0(phi)+W N_rot W†,

not a replacement of the original fast bulk by conjugated onsite projectors. Suppose

    Kref=W†(Hfast-E0)W,
    g N_Bell <= Kref <= R_fast N_Bell,

with constants g>0,R_fast fixed by the uniform fast spectral bounds. Because the physical fast part is exactly symmetric, [Kref,R_beta]=0. In product frame the symmetry-averaged Hamiltonian is

    K=Kref+integral R_beta N_rot R_beta†.

From Kref>=g R_beta N_Bell R_beta† and the previous comparison for N=N_rot+N_Bell,

    K >= min(1,g) integral R_beta N R_beta†
      >= min(1,g) c N.

The upper bound is K <= (R_fast+C)N. The untwirled parent has gap at least gamma0=min(1,g), and every twirled copy shares its vacuum, so the average retains gap at least gamma0. Rescale K and perturbations by gamma0 to apply Section3 verbatim. There is no need to replace the original quadratic h by a finite-depth projector Hamiltonian.

The scalar E0(phi) is generally not a finite-range function and must not be silently treated as a harmless constant. For an ordinary number-conserving single-particle matrix h,

    E0(phi)=sum_x tr_internal[(h-sqrt(h²))/2]_(xx).

Use the correct additional factor for a redundant Nambu representation if present. A uniform gap g and norm bound R_fast permit an exponentially convergent polynomial approximation to sqrt on [g²,R_fast²]. Each polynomial diagonal is a finite sum of closed walks in the original finite-range h, with rotor dependence on a finite stencil. Thus its internal trace is an exactly local, exactly periodic, symmetry-invariant scalar density. Replacing E0 by this finite-degree approximation does NOT change h itself. Its exponentially small weighted interaction tail is included in the perturbation V_R of Section4. The internal trace dimension stays fixed when normal sites are kept explicit; no hidden L factor is introduced.

## 2. Why Yarotsky cannot simply be quoted

Yarotsky, math-ph/0412040, allows infinite-dimensional onsite Hilbert spaces, but its relative perturbation condition is local: each phi_x must satisfy a form inequality against the corresponding finite-support classical term h_x. The global inequality cN<=K<=CN does not by itself supply that decomposition. Therefore the shortcut of setting a=(C+c)/2 and citing its alpha<1 theorem is not used below.

## 3. Applicable stability lemma

Let K be a bounded, sufficiently rapidly decaying interaction with unique product vacuum Omega, gap >=1, and K>=cN. Suppose its interaction norm and locality bounds are uniform in finite volume. Let V be a perturbation of strength epsilon in a fixed exponential (or sufficiently rapid stretched-exponential) weighted interaction norm. Then there is a positive threshold epsilon_*(c,J,decay,lattice), independent of volume and onsite Hilbert dimension, such that

    K+sV has a unique ground state and gap >=3/4,
    0<=s<=1,    epsilon<epsilon_*.

Here J records the unperturbed weighted interaction norm. The proof below is a direct spectral-flow bootstrap. It does not need a separate claim about local ground spaces or local gaps of K.

### 3a. Bootstrap and term-by-term filtered flow

Assume temporarily that H_s=K+sV has a unique ground line with gap >=1/2 for s in an interval beginning at zero. Choose a real even filter f with integral one, Fourier transform supported in (-1/2,1/2), and rapidly decaying time tails. Such filters and the associated locality estimates are standard spectral-flow machinery.

Write V as a sum of anchored local/quasilocal terms V_x (or include an additional initial-radius label). Define

    B_x(s)=integral f(t) exp(it H_s) V_x exp(-it H_s) dt.

For every x individually, [B_x(s),P_s]=0, because the Fourier filter removes all matrix elements between the ground line and the excited spectrum. This term-by-term statement is essential: a global vacuum-annihilation statement alone is insufficient for the next localization argument.

Let D_s=sum_x D_x(s), with spectral multiplier

    D_x(s)_(mn)=i[1-fhat(E_m-E_n)]/(E_m-E_n) * (V_x)_(mn),

using the continuous value at zero. Equivalently D_x is a rapidly decaying time integral of the evolved V_x. Let S_s solve S'_s=i D_s S_s, S_0=1. Then S_s P_0 S_s†=P_s, and exactly

    d/ds [S_s† H_s S_s]=sum_x S_s† B_x(s) S_s.

This follows since V+i[H_s,D_s]=sum_x B_x(s). The filter and generator can be chosen with the usual almost-exponential tails; no finite-dimensional eigensum is needed to define them.

### 3b. Product-vacuum localization of the transformed perturbation

Each transformed Btilde_x=S_s† B_x(s) S_s preserves the vacuum line. Put

    b_x(s)=<Omega,Btilde_x Omega>,
    A_x(s)=Btilde_x-b_x(s)1.

Then A_x(s) Omega=0 EXACTLY, for each x. Lieb–Robinson bounds for H_s, filtered dynamics, and the spectral flow give a uniform quasilocal tail estimate of the form

    ||A_x(s)-E_r(A_x(s))|| <= epsilon b(r),

and ||A_x(s)||<=epsilon b_0, after the initial-support summations are included in b. The function b has all required polynomial moments. For example a Gevrey/standard almost-exponential filter gives a sufficiently rapid stretched-exponential tail. Constants depend on J, decay, the fixed bootstrap gap1/2, and lattice growth, not on volume or onsite dimension.

Vacuum conditional expectations now give an EXACT local-annihilation decomposition: E_r(A_x) annihilates Omega_Br, and every telescoping shell does likewise. Hence, as quadratic forms,

    -epsilon C_stab N <= sum_x A_x(s) <= epsilon C_stab N,

where one admissible recorded constant is

    C_stab=b_0+sum_(r>=1) v(r)[b(r)+b(r-1)].

The initial-radius labels of a general interaction add the corresponding weighted support-volume sums to this expression; these are finite by the chosen interaction norm. No thermodynamic trace or finite onsite dimension is used.

Integrating the exact derivative identity gives

    S_s† H_s S_s-E_s = K + integral_0^s sum_x A_x(u) du,

where E_s is the ground energy. Therefore

    S_s† H_s S_s-E_s >= K-epsilon C_stab N
                         >= (1-epsilon C_stab/c)K.

If epsilon C_stab/c<=1/4, the gap is >=3/4 throughout the bootstrap interval. This contradicts a first decrease to1/2 and extends the result to all s in[0,1]. Finite-volume bounded perturbation theory starts the interval; all final constants are volume independent. Rank-one ground-state continuation rules out splitting/degeneracy along the path.

A convenient threshold is

    epsilon_* = min(epsilon_LR, c/(4 C_stab)),

where epsilon_LR is any fixed bound used to keep the perturbed interaction/Lieb–Robinson constants within the selected uniform class. C_stab can be obtained from those explicit locality/filter tails. It is an existence certificate, not a numerical claim that these constants are small.

## 4. Apply the lemma to an exactly symmetric finite-range truncation

For the simple parent let h_x=W q_x W†, with exponentially small localization tails. For the strengthened Section1b parent, apply this construction ONLY to the dressed rotor-reset terms; keep Hfast exactly and separately include the finite-degree scalar E0 approximation just described. Choose a product-state conditional expectation E_(x,R) onto B_R(x). Define the strictly finite-range physical Hamiltonian

    H_R = integral U_beta [sum_x E_(x,R)(h_x)] U_beta† d beta.

If necessary also average over onsite vector symmetry; that does not increase support. A finite-depth axial symmetry increases the support radius by a fixed amount ell_A, uniformly in beta. Therefore H_R is exactly symmetric and has interaction radius <=R+ell_A. Its individual averaged terms remain bounded and positive. Its ground state need not be exactly Psi; that is why stability is needed.

The difference Delta_R=H_R-Hsym is exponentially small in a slightly weaker weighted interaction norm. For clarity, if ||h_x-E_r h_x||<=A exp(-mu r), then h_x-E_R h_x has norm <=A exp(-mu R) and tails bounded by A exp[-mu max(r,R)]. Measuring it at exponent mu'<mu produces strength <=A exp[-(mu-mu')R]. The finite-depth symmetry changes only fixed constants/radius offsets.

Conjugating by W maps Delta_R to V_R=W†Delta_R W, still small in a weaker fixed weighted norm. For appropriate constants fixed by W and the symmetry,

    epsilon_R <= C_tail exp(-mu R/2)

(after a harmless further reduction of decay rate). Thus choose, for example,

    R >= (2/mu) log[4 C_tail C C_stab]

and also large enough for the epsilon_LR threshold. This is finite and independent of system volume. Apply Section3 to K+V_R. The original physical interpolation Hsym+sDelta_R then stays gapped, unique, and exactly symmetric. H_R is the required bounded-range endpoint of this stability step.

Because the path is uniformly gapped and the starting state is a quasilocal unitary image of a product state, the endpoint stays short-range entangled and introduces no intrinsic topological order or spontaneous symmetry breaking. This statement is conditional on the original collective construction actually having the asserted symmetric product-frame parent; it does not validate an incorrect physical doubling, symmetry action, or retained chiral boundary.

## 5. Infinite rotor factors, domains, and resource limits

All terms used here are bounded operators. N uses vacuum/reset projections, not an unbounded bare J². Finite-volume Hamiltonians are bounded self-adjoint operators even though local rotor Hilbert spaces are infinite dimensional. The product-state conditional expectation uses a vector state, not normalized matrix trace; no finite-dimensional trace is smuggled into the proof. Bounded-interaction Lieb–Robinson bounds and spectral flow extend to arbitrary onsite Hilbert spaces. Fermionic factors are handled with even operators and even product vectors in the graded local algebra.

The Haar average may be understood as a strong/weak operator integral if rotor symmetry is not norm continuous. Uniform finite-depth support and uniform norm bounds make that sufficient; norm continuity of the floor-valued charge functions is not assumed.

This pays bounded interaction range, symmetry, and a uniform gap for the truncation STEP. It does not supply a finite rotor charge cutoff. The local Hilbert space remains L²(S¹) times finite fermion factors. Constants can be enormous because the static Wilson construction already has large local resources, and the locality length of W depends on its uniform free gap. Those constants must be inserted, not ignored, before any practical claim.

## Primary-source support and provenance

* Michalakis–Zwolak, arXiv:1109.1588v3, SectionV, Lemma1 and Proposition1: filtered dynamics creates terms individually commuting with the ground projector; SectionVI gives the local-annihilation relative-bound strategy. The proof above specializes the latter to exact product-vacuum conditional expectations rather than asserting its general LTQO assumptions for K.
* Nachtergaele–Sims–Young, arXiv:1810.02428v2, Sections3–6: bounded-interaction locality, conditional expectations, compositions, and spectral flow, explicitly allowing infinite-dimensional onsite Hilbert spaces.
* Yarotsky, math-ph/0412040: infinite onsite Hilbert spaces are allowed, but its local relative-form hypothesis is stronger than the global form comparison. It is not used as a black-box shortcut here.

The product-frame bootstrap and its application to this averaged parent are deductions in this note. Novelty is not established. A final audit should check that the actual W and symmetry family meet the JOINT operator-norm weighted locality inputs uniformly in volume.

## Explicit compatible filter pair

One can avoid leaving the filter abstract. Pick a nonzero real even C-infinity bump ghat supported in[-1/8,1/8], let g be its inverse Fourier transform, and set f(t)=|g(t)|²/integral|g|². Then f>=0, integral f=1, and fhat is supported in[-1/4,1/4], strictly inside the bootstrap gap1/2. All polynomial moments of f are finite; choosing a Gevrey bump gives the usual stretched-exponential tails. Define

    w(t)=sign(t)/2-integral_0^t f(u)du.

Then w'=delta-f, what(omega)=i[1-fhat(omega)]/omega, and integral|w(t)|dt=integral|t|f(t)dt. This w is exactly the generator kernel used above, with D_s=integral w(t) tau_t^(H_s)(V)dt. Thus the filtered derivative identity and spectral-flow generator use a compatible pair, rather than two independently selected filters.

## Explicit finite-patch implementation alternative

For implementation, the local approximant need not call a conditional expectation of a globally computed W. If W is given by the claimed fixed-time quasilocal generator with explicit local polynomial/telescoping terms, truncate that generator to a fixed joint support radius and restrict its evolution to B_R(x). Define h_x^(R)=W_(x,R) q_x W_(x,R)†, using only that finite patch's rotor and fermion data. Standard Lieb–Robinson comparison of full and restricted dynamics gives a uniform exponentially small approximation error after suitable fixed radius buffers. Symmetry-average these terms as in Section4. They are positive bounded finite-patch operators, although they need not commute or share the original ground state. Stability handles that difference. Thus vacuum conditional expectations are proof tools, not an assumed global ground-state or nonlocal-coefficient oracle for implementing H_R.

## Input reconciliation with the actual parent

`ACTUAL_FAST_PARENT_AND_COERCIVITY.md` supplies the strengthened parent rather than a flattened replacement. Its polynomial telescoping of sign(h_phi) acquires JOINT rotor–fermion generator terms: each degree-n entry uses a finite hopping-path stencil, while coefficient bounds and polynomial site-pair/support counts retain exponential decay. The same construction supplies the scalar E0 densities. This is the correct locality input for this note; fixed-phi matrix decay alone would not have sufficed. Its exact Bell-excitation sector argument gives a second, somewhat stronger derivation of product coercivity. The filtered-flow signs and vacuum shell step have also been checked independently by that constructor.

An additional resource caveat remains: bounded reset projectors on infinite rotor Hilbert spaces have infinitely degenerate excited sectors. This proof does not make the finite-volume Gibbs partition function trace class, nor does it acquire a finite charge cutoff. Adding a confining bare J² after nonlocal dressing is not covered automatically. The zero-temperature Hamiltonian/gap statement and finite-dimensional/thermal implementation are different claims.

## A noncircular recipe for the stability tail constants

The symbol C_stab does not depend on the selected truncation radius R. One way to instantiate it is as follows. First fix a weaker exponential interaction norm and a normalized perturbation class of strength<=1. Bounded-interaction Lieb–Robinson estimates for every H_s in that class give fixed constants C_L,mu,v. After absorbing support-count polynomials by weakening mu, a normalized anchored perturbation has a localization bound of the form

    ||tau_t(V_x)-E_r tau_t(V_x)||
       <=epsilon min(2,C_L exp(v|t|−mu r/4)).

Splitting the time integrals at |t|=mu r/(8v) therefore gives valid filtered tails, with enlarged fixed prefactors if needed,

    b_B(r)=C_L exp(−mu r/8)
           +2 integral_(|t|>mu r/(8v)) f(t)dt,
    b_D(r)=C_L ||w||_1 exp(−mu r/8)
           +2 integral_(|t|>mu r/(8v)) |w(t)|dt.

Both have all polynomial moments. The shell decomposition of D_s defines an explicit finite weighted interaction norm C_D times epsilon in a fixed stretched-exponential class. Set epsilon_LR<=min(1,1/C_D), so the auxiliary s-time evolution has a uniform finite-time locality bound. Write its resulting local-observable tail as C_S |X| ell_S(r), where ell_S is a fixed sufficiently rapid stretched-exponential function, obtained from that weighted norm and the lattice's F-function convolution constant.

Localize B_x first at radius r/2 and then conjugate it by the auxiliary evolution. A permissible normalized tail for Btilde_x is

    b(r)=2 b_B(floor(r/2))
         +C_S v(ceil(r/2)) ell_S(floor(r/2)),

with b_0 enlarged to cover small radii and the scalar subtraction. Inserting this b into the displayed C_stab sum gives a finite, volume-independent threshold. All ingredients are norms, tail integrals, and lattice growth/convolution constants fixed BEFORE choosing R. The choice epsilon_R<=epsilon_* can therefore be met by increasing R without the Yarotsky range-threshold circularity. This is an existence/resource recipe; no assertion of practically small constants is made.
