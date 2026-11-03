# Independent audit: shared-rotor disentangler and finite auxiliary regulator

2026-11-03. Audited `SHARED_ROTOR_DOUBLE_DISENTANGLER.md` and `FINITE_AUXILIARY_COERCIVE_REGULATOR.md`, including primary TPF2601.04304v2 equations58–60 and79–81. This audit uses the DIRECTLY DECLARED map, not an unverified identification with the source's printed phase/order conventions.

## Verdict

The exact compact-angle on-siting algebra, finite-volume ground/gap compression, and optional new coercive completion pass. The claims are appropriately finite-volume and concern an explicitly modified ultraviolet spectrum when kinetic energy is added. They do not establish a fixed local dimension/range thermodynamic regulator, polynomial gate compilation, or a gauged continuum theory.

Two presentation requirements should be enforced:
1. Use normalized K=sum_e n_e with ground eigenvalue zero as the working definition. Any background charge is a separately declared INTEGER local countercharge. Do not import the literal source Eq73's constant into a proof that elsewhere assumes K_ground=0.
2. For a polynomial finite-energy cutoff claim, explicitly choose kappa=e_target/(4mN^2), or a comparable inverse-polynomial value. The inequality kappa<=that alone also permits exponentially smaller choices and does not imply polynomial cutoff size.

## 1. Exact bosonic cocycle and compactness

Use period-one angles throughout this derivation. For one base let A be its BOSONIC axial weight and v its integer shear weight. Write

  m=round(d(u+v theta)), b=round(theta),
  r=round(d theta), c=round(Au), l=round(u),
  omega=theta cup(A m-dc-A v db) cup dm
        +A v dtheta cup(db-r) cup(m-dl).

This is the ordered simplicial cochain formula; no graded-commutative replacement of cup products is used. Define the ket map

  D_B|u,theta>=exp(+2pi i integral sum_alpha omega_alpha)
               |u+v theta,theta>.

For a COMMON real shift theta->theta+beta, m,r,c,l are unchanged and b changes by an integer zero-cochain k. After integrating exact coboundaries on the closed triangulation,

  integral Delta omega
   = beta A integral m cup dm
     +A v integral[dtheta cup dk cup(m-dl)-theta cup dk cup dm].

The bracket is exactly d[theta cup dk cup(m-dl)] and integrates to zero. The remaining dc,db,dk terms multiplied by constant beta are also exact. Thus the phase difference is PLUS beta A S of the output rotor. This proves the desired sign for the declared ket convention. Negating the phase would negate that scalar axial action.

Compactness can be proved without a numerical test:
- For any integer zero-cochain n, u->u+n gives m->m+dn, c->c+A n, l->l+n. Both displayed factors are unchanged exactly.
- Under theta->theta+n, m->m+v dn, b->b+n, r->r+dn. The first term changes by an integer cochain. The second changes, modulo integer cochains, by A v^2 dtheta cup(db-r) cup dn.
- Summing bases cancels the remaining noninteger term when sum A v^2=0.

For (A,v)=(2,2),(-8,1), this coefficient is 8-8=0. The shear is an integer unimodular torus automorphism. Therefore D_B is a genuinely well-defined compact-rotor unitary BEFORE any momentum cutoff. For manifestly periodic individual phase gates, group the two base contributions on each simplex before exponentiating; their anomalous compact-shift terms cancel locally. These phase gates have bounded support and can be colored into bounded depth.

Independent exact-rational tests on the actual closed 27-vertex/162-tetrahedron complex checked 24 configurations, including 37 nonzero cocycle examples. Uniform-shift equality, matter integer-shift invariance, and theta integer-shift phase invariance modulo one all passed EXACTLY. Files: `audit_compact_cochain_exact.py` and `audit_compact_cochain_exact_results.json`. These are implementation checks; the preceding cochain algebra is the proof.

## 2. Fermionic dressing, output order, and normalized charges

Set n_e=(1-i gamma_e gamma'_e)/2, an integer-spectrum projector. Use its phase-corrected graded conjugate in copy2. Define K_c=sum_e n_e,c; then both pairing vacua have K_c=0. If a chosen particle-hole/reference convention requires a fixed charge offset, distribute its declared integer value over local reference cells and include the corresponding theta phases. The literal source Eq73 is not needed.

In turns the gate is exp(2pi i a_alpha theta_j(e) n_e,alpha,c), NOT an unrescaled radian exponential. Its periodicity is exact for integer a_alpha. The matching depends on CURRENT/OUTPUT phi. A common shift phi_alpha->phi_alpha+v_alpha beta leaves its vorticity and matching unchanged, including after coordinate wrap. Consequently

  R(phi+v beta,theta+beta)R(phi,theta) dagger
    =exp(2pi i beta sum_alpha a_alpha(K_1+K_2')).

Within each matching the bilinear projectors commute; alternative controlled edges cannot simultaneously be active when they conflict. Even gates in the two copies commute as well. Local edge coloring gives bounded circuit depth. No odd gate or half-integer compact phase is being used.

For D=R_OUTPUT D_B, direct action on a ket gives first the scalar cocycle above, then exactly this fermionic ratio. Hence D T_theta(beta) D dagger is the intended matter-plus-ancilla subgroup action. This proves the ORDER without relying on the ambiguous literal WW' rendering. Multiplying two full shared-rotor bosonic shears instead would be wrong: there is only one phi per base and one shear.

The phase-corrected second generator is +F K* F dagger, not its negative. The bosonic weights are therefore 2a while each of the two fermionic factors has weight a. On-siting retains the same-charge canonical doubling rather than inserting an inverse copy.

## 3. Concrete stack and onsite cutoff compatibility

For (a,v)=(1,2),(-4,1), the original four-Weyl charge lists are (3,-1,-1,-1) and (-3,-5,4,4). Their total linear and cubic sums vanish. Canonical doubling repeats both lists. Removing a +/-3 vectorlike pair, if an actual mass is supplied, leaves {-5,-1,-1,-1,4,4}, twice in the doubled construction. This is a genuinely chiral Abelian test, not the Standard Model. No mass-removal operation is inferred merely from this arithmetic.

After D dagger, the selected subgroup acts on theta momenta and the existing onsite free-fermion integer charges, with explicit onsite backgrounds where required. Matter rotors and decoration fermions are neutral under the disentangled subgroup. Thus every physical onsite rotor Fourier projector commutes with every corresponding local charge rotation. Compressing the WHOLE transformed Hamiltonian preserves the global subgroup and its onsite representation. This is the correct order: on-site first, then physical momentum cutoff. No assertion that D preserves momentum-cutoff subspaces is needed or true in general.

This earns a gaugeable matter representation. It does not by itself introduce dynamical gauge links or prove the spectrum of a gauged model.

There are two shared matter rotor coordinates plus one common theta ancilla per relevant boundary vertex, not four independent matter rotors. Separate physical boundaries contribute their separate vertex counts.

## 4. Actual phase-fixed ground regularity and Fourier tails

The uniform fast gap gives a dimension-free trace-norm derivative bound for sign(h). On positive/negative spectral blocks its derivative is obtained from a Sylvester equation with denominator at least 2g. The displayed conservative bound ||partial sign(h)||_1<=2||partial h||_1/g is valid.

Differentiating the canonical quadratic Gaussian exponential by Duhamel bounds the full many-body vector derivative by a fixed constant times this one-body trace norm. The proposed C_G=4pi has ample convention slack. There is no multiplication by the Fock-space dimension. A local rotor affects only a fixed number of actual one-body matrix entries, so ||partial_j h||_1 is bounded independently of total volume at fixed UV refinement.

The barycentric normalization lower bound and piecewise affine lifts give bounded derivatives within each chamber. All chamber walls are finitely many local rounding hyperplanes. The integer shear and finite-depth disentangler pull them back to finitely many integer affine hyperplanes with explicitly bounded coefficients. Hence the proposed local enumeration of R_j and B_j is valid. No differentiability across a jump is asserted.

The normalized output wavefunction has pointwise fermionic norm one: the shear is Haar-measure preserving and the remaining fiber operations are unitary. Vector-valued integration by parts in one coordinate therefore gives

  ||Omega_hat_j(n)|| <=(B_j+2R_j)/(2pi |n|).

Summing both Fourier tails and then the commuting coordinate-projector union bound yields exactly tau_N<=A/N with A=sum_j(B_j+2R_j)^2/(2pi^2). The periodic seam must be included in R_j. This does not imply finite bare kinetic energy; jumps can make it infinite.

## 5. Finite-volume compression uses the known canonical trial state

For exact positive H with H Omega=0, gap Delta and norm B, and ||H_R-H||<=delta, the shift V_R=H_R+delta I satisfies H<=V_R<=H+2delta. The normalized projected canonical state has energy at most

  e_N=B tau_N/(1-tau_N)+2delta.

This follows from H Omega=0; it is not an assumption that the unknown ground of H_R has the same Fourier tails.

On the compressed space, minmax gives lambda_0<=e_N and lambda_1>=Delta. Equivalently, compression of Delta(I-|Omega><Omega|) has at most one eigenvalue below Delta. The ground is unique for e_N<Delta and its squared overlap with Omega is at least 1-e_N/Delta. The stated choices N>=max(2A,8BA/(Delta epsilon^2)) and delta<=Delta epsilon^2/16 have sufficient slack for O(epsilon) vector error and a positive gap.

Because the exact parent has an acquired summable exponential interaction expansion, choosing a finite-volume GLOBAL norm tolerance costs range O(log(C V/delta)), with fixed microscopic locality constants and harmless logarithmic corrections for support-volume factors. No fixed-range thermodynamic theorem is claimed in this step.

## 6. Optional kinetic completion: domains, spectra, and real-time bound

The old bounded reset model really has infinite low-energy capacity and divergent thermal trace. The proposed H_kappa=V_R+kappa sum_j L_j^2 is a NEW Hamiltonian. Its quadratic form is closed and positive; bounded V_R gives operator domain D(sum L_j^2). This operation is performed in the physical onsite frame, not by conjugating an unbounded kinetic operator through a discontinuous circuit.

The finite Fourier trial lies in this domain and has kinetic energy <=mN^2. Choosing e_N<=e_target/2 and kappa mN^2<=e_target/4 gives a ground energy below e_target. Since H_kappa>=V_R>=H, the second minmax level remains >=Delta and the ground gap is >=Delta-e_target. The same argument applies after a larger cutoff L>=N. It never requires Omega itself to have finite kinetic energy.

In finite volume, the rotor Laplacian has compact resolvent, and a bounded perturbation preserves it. The heat-trace bound follows from minmax eigenvalue ordering (not from a false operator-monotonicity assertion for exponentials):

  Tr e^(-beta H_kappa) <=2^F [sum_(n in Z)e^(-beta kappa n^2)]^m.

For a state of energy expectation <=E, positivity implies uniform-in-time discarded norm <=sqrt(E/kappa)/(L+1). The kinetic operator commutes with the cutoff; only bounded V_R couples the two sectors. Projecting the Schrödinger equation, applying Duhamel to that bounded coupling, and paying normalization of the initial projection yields

  ||state_exact(t)-state_cutoff(t)||
       <=(2+|t|B_R)sqrt(E/kappa)/(L+1).

The argument extends from operator-domain vectors to all finite-energy form-domain vectors by approximation. The spectral Schur bound with denominator kappa(L+1)^2-E is also valid whenever positive, since the discarded block has that lower bound and its cross coupling is bounded by B_R.

To make the polynomial statement definite, take kappa=e_target/(4mN^2), with e_target an explicit fixed multiple of Delta epsilon^2. Then, at fixed microscopic parameters, A=O(m), B=O(V), N is polynomial in V and epsilon^-1, kappa^-1 is polynomial, and the displayed real-time cutoff is polynomial in V,E,T,epsilon^-1. Arbitrarily smaller kappa need not have this property.

## 7. Resource interpretation

Polynomial LOCAL dimension means fixed onsite fermion multiplicity f and fixed rotor-species count s: 2^f(2N+1)^s. Keep the normal lattice explicit; do not pack a growing slab or range-R ball into one nominal site and then call f fixed. Total Hilbert dimension remains exponential, while logical qubit count is F+m ceil(log2(2N+1)).

A generic dense interaction on a logarithmically growing ball has superpolynomial coefficient-table/gate cost. The notes correctly do not infer a polynomial-time compiler from qubit count or local dimension. The inherited Wilson UV constants and all interaction radii remain enormous. No efficient ground preparation, finite-energy approximation to the old reset spectrum, fixed-cutoff thermodynamic limit, gauge-field regulator, or continuum claim has been proved here.

Primary circuit source inspected: TPF2601.04304v2, https://arxiv.org/html/2601.04304v2 . Its cochain formula and mechanism are inputs; the sign, compactness, output-order intertwining, and resource inequalities above were checked directly under the declared conventions rather than asserted to be a verbatim reading of its printed equations.
