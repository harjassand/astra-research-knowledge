# Finite auxiliary regulator after the ACTUAL anomaly-free symmetry disentangler

2026-11-03. Conditional on the audited doubled interface and static uniform gap. This pays a finite-volume ground/gap regulator, and gives an optional coercive UV completion with a genuine low-energy cutoff. It is NOT an ungauged-to-gauged continuum theorem or a fixed-local-dimension thermodynamic theorem.

## 1. Correct symmetry frame, not an assumed onsite axial action

Use the actual TPF anomaly-free-stack circuit D=WW' of 2601.04304v2, equations (58)–(60),(79)–(81), after adding theta ancillas in their uniform angular state. W is an integer rotor shear times a local floor/cochain phase. W' is the rotor-controlled local Majorana rotation. In the D† frame, the chosen anomaly-free matter-plus-ancilla U(1) acts only on theta angular momenta; the existing free bulk's charges remain onsite. Thus the full charge is an onsite integer combination of theta momenta and free-fermion charges. All individual rotor-momentum projectors commute with it, including the matter rotors which are neutral in this frame. Local gauge rotations also commute with the cutoff. The auxiliary theta Hamiltonian may be the bounded reset 1−|0><0| for the first construction, not theta kinetic energy: this keeps the starting finite-volume parent bounded and its ancilla ground explicit. This differs harmlessly in excited spectrum from the example ancilla kinetic Hamiltonian in TPF.

D is applied to the WHOLE interface Hamiltonian, not just to a rotor ground vector. No finite-momentum invariance of D itself is claimed. Onsite gaugeability survives after compression; a spectral theorem for dynamical gauge fields does not follow from this statement.

## 2. Explicit interacting ground regularity, with its phase actually fixed

The exact quasilocal parent's normalized ground is Ω(phi)=W_G(phi)|Bell>, with uniform rotor amplitude and the graded combined-fast canonical Gaussian rotation W_G. Add uniform theta ancillas and apply D†. This is not an arbitrarily phased eigenvector from diagonalization.

For a Hermitian one-body matrix h with spectrum outside (−g,g), F=sign(h) obeys, on every smooth chamber,

    ||∂F||_1 <= 2 ||∂h||_1/g.

One proof splits positive/negative spectral blocks. The off-diagonal derivative solves a Sylvester equation with positive generators >=g; its integral solution has trace norm bounded by the source trace norm/(2g). Allowing the block decompositions gives the displayed conservative constant. It is dimension-free in trace norm.

The canonical rotation generator is a fixed linear multiple of F (e.g. (pi/4) tau_y tensor F in the number-conserving doubled representation). Fermionic second quantization has operator norm at most the one-body trace norm, up to a fixed Majorana convention factor. Duhamel differentiation of its exponential therefore gives

    ||∂ W_G|| <= C_G ||∂h||_1/g,

with an absolute, conservatively chosen C_G=4pi. This bounds the derivative of the actual normalized phase-fixed many-body vector; it does not multiply scalar-component errors by Fock dimension. Fermionic grading F_grade=exp(i pi N2/2) is fixed, so adds no derivative.

The barycentric SU(2) texture has a chamberwise normalization lower bound c*>0 (the conservative cos(3pi/8)/sqrt(2) is enough). Each vertex phase has angle derivative bounded by 2pi times its explicit lift coefficient. Convex interpolation and normalization then bound texture derivatives by 2pi/c* times that coefficient. A rotor changes only its incident texture stencils; hence ||∂_j h||_1 <= r_j M C_texture plus the finite decoration contribution. Here r_j is the actual number of affected one-body orbitals, enormous but independent of total volume at fixed UV refinement. Decorations are chamberwise constant except for explicitly smooth finite rotations. No derivative is taken across a rounding wall.

For D†, inverse shears pull back floor hyperplanes to integer affine hyperplanes. At fixed other coordinates each such expression crosses at most 1+|a_j| half-integers over one coordinate period. Enumerate the finitely many gates in that coordinate's bounded-depth light cone, add these crossing counts, and add the periodic endpoint. This defines an explicit R_j. On each chamber, differentiate the elementary phase polynomials and bounded local Majorana rotations. Triangle/product rules, including shear coefficients, define B_j. The input Gaussian contribution is the sum of |shear coefficient| C_G r_k M C_texture/g over the finitely many input coordinates affected. All local floor arguments have bounded coefficients from the actual integer charges. R_j and B_j are acquired by finite local chamber enumeration and interval bounds; for a fixed stack/mesh/charges they are constants independent of volume. This prescription counts moving walls at almost every fixed value of other coordinates; measure-zero wall intersections do not change L² estimates.

The output amplitude has pointwise norm one. Its vector-valued coordinate Fourier coefficients satisfy

    ||Omega_hat_j(n; other angles)|| <= (B_j+2R_j)/(2pi |n|).

Consequently with m rotor coordinates and physical cutoff P_N,

    tau_N=||(1−P_N)Omega||² <= A/N,
    A=sum_j (B_j+2R_j)²/(2pi²).

This establishes the actual interacting-ground tail in the gaugeable frame. It asserts no bare kinetic energy for Ω; jumps generally make that energy infinite.

## 3. Pay the difference between exact and strictly finite-range parents

Let H be the exact bounded positive quasilocal parent, including theta resets and D† conjugation. Let HΩ=0, gap>=Delta and ||H||<=B. Construct symmetry-preserving finite-range H_R with ||H_R−H||<=delta. The explicit joint interaction tail yields R=O(log(C V/delta)) (plus the huge microscopic length) at finite volume. Symmetric local truncation/twirling is essential. Set V_R=H_R+delta I, so

    H <= V_R <= H+2delta I.

This shift avoids pretending that the finite-range ground equals Ω. A normalized trial chi_N=P_NΩ/sqrt(1−tau_N) obeys

    <chi_N,V_R chi_N> <= B tau_N/(1−tau_N)+2delta = e_N.

Minmax gives, for P_N V_R P_N,

    lambda0<=e_N, lambda1>=Delta, gap>=Delta−e_N,
    1−|<Omega,ground_N>|² <= e_N/Delta.

Taking delta<=Delta epsilon²/16 and N>=max(2A,8BA/(Delta epsilon²)) suffices, with slack, for O(epsilon) ground norm error and positive gap. The range grows logarithmically with volume/error. Every member is strictly finite range; this does NOT establish one fixed range and one fixed local dimension for all thermodynamic volumes.

Local rotor dimension is 2N+1; at a coarse site with s rotor species and f finite fermionic orbitals, dimension is 2^f(2N+1)^s. Total Hilbert dimension is 2^F(2N+1)^m, not polynomial. Logical qubits are F+m ceil(log2(2N+1)), polynomial at fixed microscopic parameters. The already audited Wilson UV constants remain astronomical.

## 4. Optional new coercive completion: finite thermal trace and paid low-energy capacity

The original bounded reset parent has infinitely many excitations at finite energy, even at fixed neutral charge (|n,−n>). No finite-rank approximation can uniformly approximate that original low-energy subspace. Its finite-temperature trace diverges. The preceding ground theorem does NOT fix this.

A permissible NEW regulator, after on-siting the subgroup, is

    H_kappa = V_R + kappa K,  K=sum_j L_j², kappa>0.

K commutes with every local gauge charge in this frame. Define H_kappa by its closed positive form; bounded V_R makes it self-adjoint on the standard K domain. This is not conjugating an unbounded kinetic operator through the discontinuous circuit.

Choose a trial cutoff N as above and kappa m N²<=e_target/4, with e_N<=e_target/2. Then

    E0(H_kappa)<=e_N+kappa mN²<=e_target,
    lambda1(H_kappa)>=Delta, gap>=Delta−e_target.

The same statements hold for P_L H_kappa P_L whenever L>=N. Both ground states have fidelity >=1−e_target/Delta with Ω. Thus adding weak physical kinetic energy preserves the paid finite-volume gapped ground sector, despite Ω itself having infinite K energy.

H_kappa>=kappa K has compact resolvent in finite volume and

    Tr exp(−beta H_kappa) <= 2^F [sum_{n in Z} exp(−beta kappa n²)]^m < infinity.

This is a new UV spectrum, not convergence of the divergent original partition function.

For every normalized input of H_kappa-energy expectation <=E, evolution preserves that expectation and

    ||(1−P_L)exp(−itH_kappa)psi|| <= sqrt(E/kappa)/(L+1).

Only bounded V_R couples retained/discarded momentum sectors. Writing B_R=||V_R||<=B+2delta, Duhamel gives comparison with the compressed evolution, using normalized projected input when defined,

    error <= (2+|t| B_R) sqrt(E/kappa)/(L+1).

Hence L>=N and L+1 >= (2+T B_R)sqrt(E/kappa)/epsilon pays uniform finite-energy real-time accuracy for THIS new H_kappa. This is polynomial in V,E,T,1/epsilon for the stated finite-volume ground-fidelity choice of kappa. It is not a low-energy approximation to every state of the old reset model. Spectral Schur complements also give low-energy effective corrections bounded by B_R²/[kappa(L+1)²−E], when the denominator is positive.

## 5. What is and is not implemented

The formulas pay local dimension and mathematical operator approximation, not a polynomial classical simulation. Generic dense matrices on a range-R ball cost (2L+1)^{O(R^d)} entries; with R~log V this is not a polynomial-time coefficient compiler. An efficient quantum oracle/block-encoding could exploit the actual controlled Gaussian circuit, local reset form, finite axial twirl and polynomial sign(h) evaluator rather than dense matrices. But a certified cutoff/quadrature and reversible-arithmetic compiler has NOT been supplied here. Do not label the full regulator polynomial gate cost merely from polynomial local dimension or qubit count.

Ground preparation, preserving a useful open chiral boundary instead of the fully gapped two-interface test system, uniform gauge-background bounds, gauge-field truncation and gauged continuum behavior remain separate. The useful new capability earned here is a finite-volume gaugeable finite-auxiliary gapped regulator, plus a modified coercive Hamiltonian with a precise finite-energy real-time cutoff contract. It is still not a practical predictive chiral-gauge simulation.

Primary circuit source: https://arxiv.org/html/2601.04304v2 . All resource inequalities above are derived here, conditional on the candidate interface inputs.

## Subsequent compiler audit update
POLYNOMIAL_QUANTUM_TERM_COMPILER.md now supplies a structured grid/block-encoding construction avoiding the dense-matrix cost in section5. Independent review in AUDIT_QUANTUM_COMPILER_SECTIONS4_8.md found the asymptotic gate claim supportable after valid-code, Hermiticity, integer local axial-generator and slice-variation repairs. The polynomial logical gate construction is therefore conditionally acquired at fixed microscopic constants; an executable end-to-end compiler, ground preparation, open chiral modes and gauge dynamics remain separate. Read this update rather than treating the original section5 compiler gap as still wholly untouched.
