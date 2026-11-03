# Finite-resource rotor regulators without a false bare-momentum assumption

Primary source personally read: https://arxiv.org/html/2601.04304v2 , Sections 2.1–2.4, 3.2, 3.4, 4.1, 5 and Appendix B/D. Section 5 explicitly warns that the floor-function circuits do not preserve naive finite-angular-momentum domains. Section 4.1 does not specify/verify the required free-fermion/rotor interface. The results below apply to completed rotor components, not that missing interface.

## A. Positive construction: physical finite-qudit regulator for completed CP ground sectors

Take a finite closed lattice with d rotor coordinates (and any finite fermion factors). The completed commuting-projector construction has

    H=S H0 S†, H0=sum_x (1-|0><0|)_x,
    Ω=S|0...0>, HΩ=0, gap Δ=1, ||H||<=v=#terms.

S is the paper's finite-depth local swindle/disentangler circuit. Assume the relevant physical onsite U(1) generators are the ordinary integer rotor charges (or specified onsite integer combinations and fermion occupations), as in the constructed rotor setting. Let P_N be the tensor product of physical momentum windows |L_j|<=N, retaining finite fermion factors. It commutes with that onsite symmetry. Define H_N=P_N H P_N on Ran P_N.

**Exactly preserved:** finite-dimensional tensor-product sites, bounded spatial interaction range, global onsite U(1), positivity, and a quantitatively controlled finite-volume ground sector.

**Deliberately lost:** the compressed local terms are generally neither projectors nor mutually commuting. Consequently this is NOT a finite-dimensional commuting-projector Hall model.

### Earn the Fourier tail from the actual gates
The gates in Eqs. (9),(22)–(23),(58)–(60),(81) consist of integer linear shears, phases involving nearest-integer functions of linear forms, and finite controlled fermionic rotations. On a fundamental coordinate cube they are piecewise smooth with finitely many hyperplane cuts. For fixed degree, circuit depth, simplex size and fixed integer charges, the number of gates touching any coordinate is bounded independently of system volume.

The initial zero-momentum rotor state has constant angular wavefunction. After the circuit, at almost every fixed value of the other coordinates, Ω as a function of one angle has a unit-norm finite-component amplitude, at most R jump points (including a possible boundary mismatch), and derivative norm <=B between jumps. B and R are computed by enumerating the local gate cuts and differentiating each smooth branch. They depend on charge magnitudes and local circuit complexity and are NOT assumed universal if those parameters grow. The shear's integer coefficients must be included in these bounds. Fermionic pairing changes only add bounded local matrix jumps/derivatives.

Integration by parts, including jumps, bounds the m-th partial Fourier coefficient in norm by (B+2R)/(2pi|m|). Parseval plus the union bound for commuting coordinate cutoffs gives

    τ_N := ||(1-P_N)Ω||² <= d(B+2R)²/(2pi² N).

Thus discontinuities produce a paid algebraic Fourier tail rather than an invalid finite kinetic-energy estimate. No claim that Ω lies in the domain of the bare ΣL² is made.

### Ground energy, gap, and ground state
For φ_N=P_NΩ/sqrt(1-τ_N),

    <φ_N,H_N φ_N> = <(1-P_N)Ω,H(1-P_N)Ω>/(1-τ_N)
                       <= v τ_N/(1-τ_N) = δ_N.

Minmax and H>=Δ(1-|Ω><Ω|) imply

    0<=λ0(H_N)<=δ_N,   λ1(H_N)>=Δ,
    gap(H_N)>=Δ-δ_N.

The finite ground state's fidelity with Ω is at least 1-δ_N/Δ. Therefore N=O(v d(B+R)²/(Δ epsilon²)) suffices for O(epsilon) ground-state norm accuracy and retains a positive gap. For v,d proportional to volume, this conservative cutoff grows quadratically in volume. It is NOT a fixed-local-dimension thermodynamic-limit theorem.

### Actual implementation cost and locality
Each compressed term is a matrix on the finite qudits inside its original bounded spatial support. Matrix entries are constant-dimensional integrals over angular coordinates of known piecewise-smooth gate functions and Fourier modes. Partition at the known floor hyperplanes or use a certified cell quadrature with boundary-cell error; bounded support and fixed charges make the entry calculation polynomial in N and inverse entry precision (although the polynomial degree can be large). Choose entry precision small enough to bound the local matrix norm and sum over v terms. Enforce exact charge blocks; if desired average local terms over onsite U(1) before compression, which preserves spatial support and the invariant sum. Numerical PSD correction inside charge blocks adds a separately charged operator-norm perturbation. The total many-body Hilbert dimension is (2N+1)^d times the fermionic dimension; this is finite-resource but NOT polynomial-time classical simulation in volume.

### Actual time-evolution guarantee, not just a variational state
For this ground-sector construction,

    ||exp(-it H_N)φ_N - Ω|| <= ||φ_N-Ω|| + t sqrt(v δ_N)

is a conservative bound from ||H_N φ_N||²<=v<φ_N,H_Nφ_N>. Alternatively use the actual finite ground eigenvector: after aligning its known energy phase, its evolution differs from the exact stationary ground state by at most O(sqrt(δ_N/Δ)), uniformly in time. Global phases are irrelevant to ground-state expectation values. This does NOT establish driven/response dynamics after arbitrary local insertions.

Uniform finite-volume Hall/flux response additionally needs a twist-dependent family with a uniform tail/gap and controlled current/twist derivatives. Zero-flux ground-state fidelity does not earn quantized Hall convergence. No such claim is made.

## B. Sharp obstruction: CP energy alone does NOT bound finite resources
For H0 above, a single excited rotor |m>, any nonzero integer m, costs exactly one unit of energy. Hence its energy<=1 sector is already infinite dimensional. With exact total charge fixed to zero, the states |m,-m> on two rotors have energy2 for arbitrary m and are mutually orthogonal. Conjugation by S preserves all of these facts.

For every finite-rank approximation there is a normalized vector in this energy<=2, charge-zero sector orthogonal to its range. Thus no uniform norm approximation on that low-energy sector is possible at error<1, regardless of adapted cutoff ingenuity. This is a precise resource obstruction, not just a numerical pathology. It persists even before the discontinuous conjugation.

A specified family of prepared states or an additional coercive energy/moment bound is essential. Generic bounded local operators can create arbitrary charge tails and are not such a bound.

## C. Adapted projector theorem for coercive rotor components
Suppose an already completed component is explicitly

    H=U H_b U†, H_b=c Σ_j L_j² + V, ||V||=v<infinity,

with V bounded/local and [H_b,Q0]=0 for a specified onsite integer charge Q0. Define P_N=⊗1_{|L_j|<=N}, and adapted cutoff P̃_N=U P_N U†. It commutes with UQ0U†, and its domain is U Dom(H_b), not the naive bare-derivative domain.

For normalized initial ψ with <ψ,H_b ψ><=E, exact energy conservation gives

    ||(1-P_N)exp(-itH_b)ψ|| <= sqrt((E+v)/c)/(N+1)=r_N.

Because kinetic energy commutes with P_N, projected Schrödinger evolution has forcing only P_N V(1-P_N). Duhamel therefore gives, comparing to normalized projected initial data,

    ||exp(-itH_b)ψ - exp(-itP_NH_bP_N) P_Nψ/||P_Nψ||||
          <= (2+t v) r_N.

Conjugation by U transfers this bound exactly. The cutoff is polynomial in T, sqrt(E+v), 1/epsilon and 1/sqrt(c). Locality is preserved in logical coordinates; U expands observable support by only its finite light cone. It does NOT assume bounded bare angular momentum of Uψ.

But Ran P̃_N is generally NOT a tensor product of finite-dimensional physical onsite subspaces. In logical coordinates the preserved charge is Q0; individual physical onsite charges need not preserve Ran P̃_N. Local gauging/Hall response cannot be inferred merely from preservation of the global transformed symmetry. This is exactly where a seemingly paradoxical adapted finite commuting-projector Hall regulator ceases to satisfy the no-go hypotheses.

This theorem applies directly to the explicitly conjugated quadratic rotor trivial-boundary Hamiltonians (or an explicitly specified bounded perturbation thereof), not automatically to the full chiral interface. Replacing the flat onsite projector by L² changes the excited-state energy contract; one must say so.

## D. Completed 1+1D Villain/Luttinger component: exact spectral regulator, but nonlocal
For a ring of L sites, gauge fixing the integer Villain links leaves winding w in Z, compact zero-mode momentum p in Z, and L-1 harmonic normal modes. Above the zero-point energy, the quadratic Hamiltonian in Eq. (8) has

    E= (2pi² U0/L) p² + (J0/(2L)) w² + Σ_{k=1}^{L-1} ω_k n_k,
    ω_k=2sqrt(U0 J0)|sin(pi k/L)|.

Thus restricting the displayed energy to E_cut is an explicit finite-rank projector commuting with H and both momentum/winding charges. Its dimension is at most

    (2floor sqrt(E_cut L/(2pi²U0))+1)
    (2floor sqrt(2L E_cut/J0)+1)
    Π_{k=1}^{L-1}(1+floor(E_cut/ω_k)).

Conjugate this subspace by the actual Villain C and anomaly-free W, and include finite quadratic ancilla energy cutoffs. Spectra and undriven evolution within that sector are EXACT; charge preservation follows by conjugating the commuting charges, not by pretending floor terms preserve bare cutoffs. A state of mean excitation energy E has tail probability<=E/E_cut and therefore O(sqrt(E/E_cut)) projection error, uniformly in time.

The price is that normal-mode/total-energy truncation is not a strictly local tensor-product lattice regulator. Local observables become generally dense matrices. A bounded observable's expectation on states within the retained invariant subspace is represented exactly by compression; after an insertion, dynamical correlations require an additional energy-tail bound for that inserted state. Arbitrary bounded insertions have no automatic such bound. Finite smooth vertex/shift insertions can be priced from their explicit action on quadratic kinetic/potential energy; this is not supplied by the abstract word 'local'.

The gauged extension with dynamical link fields and the free-fermion/rotor interface require their own specified Hamiltonian and coercivity estimates. They have not been smuggled into this Gaussian solution.

## E. Exact U(1) link shifts cannot survive a finite cutoff as unitary shifts
If E is a finite-dimensional electric field and a unitary link U satisfies [E,U]=U, then U†EU=E+1; taking traces is impossible. Thus a finite-resource gauge link must give something up. The standard truncated shift T_N=sum_{m=-N}^{N-1}|m+1><m| obeys [E,T_N]=T_N exactly, preserves U(1) charge/Gauss covariance, but is not unitary. Gauge-invariant local hopping products can use it, at the cost of cutoff-boundary dynamics. Their errors require a specified electric-energy tail and transition-rate bound. A cyclic unitary shift instead preserves only a finite cyclic charge law, not the exact U(1) commutator. No exact finite link shortcut repairs the missing interface.

## Bottom line
There IS a constructive symmetry-preserving finite-resource ground-sector regulator for the completed rotor CP models, obtained by physical compression, with explicit Fourier-tail/gap estimates. It gives up commutativity and does not yet certify Hall response. There IS an exact finite-energy regulator for completed ungauged Villain quadratic components, but it gives up strict lattice locality. Adapted projectors give controlled dynamics for specified coercive components, but not a finite physical onsite tensor-product regulator. There is a rigorous impossibility of uniform finite-rank truncation of the flat CP low-energy sector itself. None of these supplies the still-unwritten symmetric free-fermion/rotor interface.

## F. Concrete local-circuit constants and vector-valued tail proof

Here is an executable definition of B,R, avoiding a component-count factor. Write the explicit bounded-depth circuit on a closed bounded-degree lattice, and pull each gate's angular arguments back through the integer shears later in the circuit. Every argument is an integer-affine function, modulo its explicitly listed branch cuts. For coordinate j, only gates in its finite circuit light cone enter. On that light cone enumerate all pulled-back floor/mod-one tests ℓ(x)=a·x+b. Let A_g be the integer linear map implementing the shear pullback for gate g. Count ordinary coordinate wrapping among these tests. A sufficient cut count is

    R_j <= 1 + Σ_{tests ℓ in the j light cone} (ceil |a_j| + 2).

Equivalently use a_j=(a_original A_g)_j before expanding the tests. The leading 1 includes the periodic endpoint. For fixed other coordinates, a test crosses at most ceil|a_j|+1 integer/half-integer levels as x_j varies through one period. Parallel tests give no additional cuts unless the slice lies identically on a discontinuity; such exceptional slices have measure zero, and gate values there can be set arbitrarily without changing the L2 operator. Moving cuts and intersections are therefore handled by Fubini, not by assuming fixed cut locations.

On every cell evaluate each gate's derivative operator norm. For scalar phases exp(i p_g), take the sum of absolute coefficients of ∂_j p_g on the unit cube after the shear pullback (including maximum bounded integer values of floor factors). For fermionic rotations exp(θ γγ'), each Majorana bilinear has operator norm one, so charge each angle derivative's absolute bound. Products of controlled rotations are bounded by the sum of these derivative bounds using the unitary product rule. Thus one explicit sufficient constant is

    B_j = Σ_{g in the j light cone} Σ_l |(A_g)_{lj}| b_{g,l},

where b_{g,l} is the maximum branchwise operator derivative bound for the original gate argument l, computed by the coefficient-sum rule. If a gate includes a smooth polynomial dependence, its polynomial derivative coefficient sum supplies b_{g,l}. The actual Eqs.(23),(60),(81) are finite formulas, so these are finite arithmetic operations on fixed-size neighborhoods. Use B=max_j B_j and R=max_j R_j. Integer charges, local degree and depth determine the constants; if any grow, their growth is explicitly charged through A_g,b_g and the test list. In bounded-degree fixed-charge fixed-depth families B,R do not grow with volume.

For almost every other-coordinate slice, regard Ω(x_j, x_rest) as a vector in the ENTIRE remaining finite fermionic/internal space, not a list of scalar entries. Integer shears preserve the initially constant rotor density, and controlled fermionic gates are unitary, so ||Ω(x_j,x_rest)||=1. Between cuts, ||∂_jΩ||<=B_j; at each cut, the vector jump has norm<=2. Vector-valued integration by parts gives

    ||∫_0^1 e^(-2pi i m x_j) Ω(x_j,x_rest) dx_j||
          <= [∫||∂_jΩ||dx_j+Σcuts||jump Ω||]/(2pi|m|)
          <= (B_j+2R_j)/(2pi|m|).

Square, integrate over x_rest, and apply vector-valued Parseval. Since Σ_{|m|>N}m^-2<=2/N,

    ||(1-P_{j,N})Ω||² <= (B_j+2R_j)²/(2pi²N),
    ||(1-Π_jP_{j,N})Ω||² <= Σ_j(B_j+2R_j)²/(2pi²N).

There is NO factor equal to the number of fermionic components and NO assumption of finite bare kinetic energy. For ground-state norm error epsilon and gap at least Δ/2, a directly usable choice is to require

    τ_N <= min(1/2, Δ epsilon²/(8v), Δ/(4v)),

and set N to the ceiling of [Σ_j(B_j+2R_j)²/(2pi²)] divided by that target. This makes the volume dependence explicit, and allows a separate numerical-assembly norm-error budget smaller than Δ epsilon²/constant.

## G. Check the quadratic repair on the actual swindle, not a hypothetical U

Appendix B Eq.(89) defines S as the alternating two-layer swindle, and explicitly asserts that S commutes with the GLOBAL onsite symmetry ⊗U0(g). On a compatible finite closed/even-periodic layer geometry this is the relevant identity. If U0 consists of the specified onsite rotor rotations, replace the onsite precursor projector by J_i² and add any necessary symmetry-invariant finite fermion penalty. This new precursor commutes with global U0, so

    H_new=S(Σ_i J_i² + finite fermion penalties)S†

is exactly globally symmetric and has the same product-conjugated ground state. Its terms remain commuting but unbounded. Adapted momentum/energy cutoffs now have genuine coercive resource bounds; this is a valid repair of the flat-energy degeneracy objection for this MODIFIED Hamiltonian.

It does not preserve the original excited-state spectrum. More importantly, the physical charge density pulled into logical coordinates, S† Q_i S, need not map P_N into itself. Thus preservation of the GLOBAL charge does not implement local gauge transformations or a charged finite physical link theory. The adapted range is not a tensor product of finite physical onsite spaces. Those are the precise missing interfaces, rather than a blanket prohibition on finite-error approximation.

Finally, ordinary physical momentum basis vectors need not belong to Dom(H_new). Therefore P_N H_new P_N can be undefined/infinite as a quadratic form. Do not combine the successful physical compression in A with this unbounded repair without proving a domain inclusion. Construction A intentionally compresses the ORIGINAL BOUNDED commuting-projector Hamiltonian.
