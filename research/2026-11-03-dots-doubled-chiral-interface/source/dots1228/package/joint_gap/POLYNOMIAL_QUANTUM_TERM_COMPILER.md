# Polynomial quantum compiler for the finite auxiliary Hamiltonian

2026-11-03. Constructive gate/block-encoding result at fixed audited microscopic Wilson parameters and fixed anomaly-free charge stack. This closes the dense-local-matrix compilation gap in FINITE_AUXILIARY_COERCIVE_REGULATOR.md. It does not supply efficient classical simulation, ground preparation, useful physical constants, or a fixed-local-dimension thermodynamic limit.

## 1. Input and output contract

Input: a finite system with V microscopic sites, m total rotor coordinates, the actual cochain/shear formulas D=R D_B, finite-range radius r, Fourier cutoff |n_j|<=L, and requested Hamiltonian operator-norm compilation error epsilon_H. There are T=O(V) anchored bounded terms, of norm at most lambda (allowing a polynomial radius factor), plus the diagonal completion kappa sum L_j². All paid microscopic constants may be enormous. Each term uses at most f fermionic modes and p rotor coordinates in a buffered patch, where f,p are polynomial in r and the spectral-polynomial degree k. Neither 2^f nor (2L+1)^p is enumerated.

Output: a quantum block encoding of a Hamiltonian H_alg on the finite cutoff space, with ||H_alg-P_L H_kappa P_L||<=epsilon_H, and EXACT commutation of its encoded Hamiltonian block with the onsite gauged U(1). Normalization and gate count are polynomial in V,L,r,k,1/epsilon_H and the fixed microscopic constants. All integer/floor decisions are computed on exact grid integers; numerical elementary functions receive separate uniform error budgets.

The output is a finite-dimensional quantum Hamiltonian algorithm, not a list of all its matrix entries. Approximate elementary quantum gates contribute to the certified block-encoding error in the usual way. An integer charge-copy construction below defines an exactly symmetric Hamiltonian block even when the underlying coefficient approximation is imperfect.

## 2. Tensor quadrature without the exponential dimension factor

Put d=2L'+1. For one angle theta and an operator-valued bounded-variation function A(theta), define the continuous Fourier compression

 Phi(A)_(nm)=integral exp[i(m-n)theta] A(theta) dtheta/(2pi),  |m|,|n|<=L'.

Define Phi_S by the S-point uniform trapezoid rule, with S>2L'. Both Phi and Phi_S are unital completely positive maps: they compress multiplication by A with, respectively, the continuous Fourier isometry and the exactly orthonormal discrete Fourier isometry. Thus they have operator norm1, including with arbitrary additional quantum/operator-valued spectator factors.

A Banach-valued bounded-variation Riemann-sum estimate gives

 ||integral B(theta)dtheta/(2pi)-S^-1 sum_j B(2pi j/S)|| <= Var(B)/S.

This follows interval by interval by comparing the chosen sample to every point in that interval and summing variation. Applying it to exp[i(m-n)theta]A(theta), followed by a d-by-d block row-sum bound, yields

 ||Phi(A)-Phi_S(A)|| <= d[Var(A)+4pi L'||A||_infinity]/S.       (1)

For p coordinates, telescope the tensor maps one coordinate at a time. All remaining continuous/discrete maps are contractions, so

 error <= (d/S) sum_j [Var_j(A)+4pi L'||A||_infinity].         (2)

Here Var_j is a uniform slice variation bound in coordinate j. There is NO factor d^p. Applying an entrywise quadrature estimate to the complete d^p-dimensional matrix would lose this crucial property and is not the compiler.

## 3. The reset coordinate also has polynomial cost

Every unaveraged dressed reset has the form I-A(phi)P_0,v A(phi)†, where A is a finite-patch fermionic unitary multiplication operator and P_0,v projects one rotor onto uniform angle. Other rotor coordinates are spectators. For fixed spectator angles define

 C_n=integral exp(-in theta) A(theta)dtheta/(2pi),
 C=[C_(-L');...;C_(L')].

The compressed reset projector is CC†. Its grid version is C_S C_S†. Since multiplication by A is unitary and both Fourier embeddings are isometries, ||C||,||C_S||<=1. The one-dimensional quadrature bound gives

 ||C-C_S|| <= sqrt(d)[Var_v(A)+2pi L']/S,
 ||CC†-C_S C_S†|| <=2 sqrt(d)[Var_v(A)+2pi L']/S.             (3)

For any spectator coordinate j, the operator-valued function CC† has norm<=1. Uniform slice BV does NOT imply BV in the L-infinity norm of the active variable: moving walls make that shortcut invalid. Instead write C=integral v(theta) tensor A(theta) dtheta/(2pi), with ||v(theta)||=sqrt(d). For every partition in spectator coordinate j, integrate the variation sum at each fixed active theta. This gives Var_j(C)<=sqrt(d) Var_j(A), where the right side is the uniform slice bound. The same proof works for the grid C_S. Therefore Var_j(CC†), Var_j(C_S C_S†)<=2sqrt(d) Var_j(A). Apply (2) to those spectator coordinates. One sufficient total bound is

 E_grid <= [2 sqrt(d)(V_A+2pi L')
            +(p-1)d(2sqrt(d)V_A+4pi L')]/S,                       (4)

where V_A bounds every coordinate variation of A. This also covers a sum/average of such resets by linearity. Only one active integration coordinate is introduced per original heat-bath reset; the number of spectator rotor coordinates may grow with the patch.

## 4. The actual disentangler does not defeat that bound

The cochain phase and the matching rotation R are diagonal in rotor angles and unitary on the finite fermions. The only coordinate motion in D is the fixed integer shear phi_alpha -> phi_alpha+v_alpha theta, applied ONCE for the shared doubled rotor. Pull this shear outside the term. The remaining term is exactly of the form in Section3, with A a product of the cochain phase, matching rotations, the axial-twirl rotation, and the Gaussian purification patch unitary.

A fixed-stack unimodular shear sends Fourier vectors in the original box |n_j|<=L into a box |n_j|<=L'=c_D L, where c_D is the maximum relevant absolute row sum of the inverse-transpose integer shear. Thus it suffices to prove (4) on that larger box. On an S-point common phase grid, the shear is an EXACT reversible modular-integer permutation. Choose S>2L' so no input Fourier label aliases. The norm estimate on the larger box bounds its compression to the sheared original input subspace. There is no exponential expansion into sheared basis vectors.

For the concrete stack v=(2,1) with one shared theta, the shear matrix on (phi_1,phi_2,theta) is [[1,0,2],[0,1,1],[0,0,1]], so c_D=4 suffices for either relevant transpose/inverse-transpose Fourier box bound. A common power-of-two S is convenient: the triangular integer shear remains invertible modulo S. Exact half-open floor conventions are evaluated before any approximate trigonometric arithmetic.

## 5. Polynomial variation bounds for the ACTUAL coefficient unitaries

All cochain floor arguments are fixed integer affine combinations of phase coordinates. Along one coordinate they have at most the sum of their absolute integer coefficients plus one crossings per local gate. The number of gates in a patch is polynomial in p,f. Between walls the cochain phases are fixed-degree explicit polynomials and the matching rotations are ordinary bounded quadratic exponentials. Their derivative norms and total variation are polynomial in p,f and the fixed charge weights. Across a wall any unitary jump has norm at most2. Products of unitaries satisfy Var(AB)<=Var(A)+Var(B), without a Fock-dimension factor.

For the actual Gaussian patch generator use the grouped spectral polynomial

 p_k(h)=sum_(j=0)^k (h/R)c_j(1-h²/R²)^j,
 c_j=binom(2j,j)/4^j.

The Hamiltonian entries needed for a retained generator entry are evaluated in a buffer containing every degree-(2k+1) path. A cutoff patch is NOT presumed spectrally gapped. Its compression satisfies ||h_patch||<=R, so B=1-h_patch²/R² has norm<=1. Differentiating the grouped powers gives

 ||partial p_k(h_patch)|| <= (k+1)² ||partial h_patch||/R.    (5)

Indeed the j-th derivative is bounded by (1+2j)||partial h||/R and c_j<=1. No sum of absolute monomial coefficients is taken. The original bulk gap is used only to bound the global polynomial-approximation error before restriction, q^(k+1)/(1-q), q=1-g²/R².

The actual barycentric texture has chamber derivative ||partial h||<=M/c_* with the paid positive spinor norm c_*. Fermionic second quantization of an f-mode quadratic derivative has norm at most a fixed multiple of f times its one-particle norm. Unitary Duhamel differentiation then gives

 ||partial exp(i G_patch(phi))|| <= C f(k+1)² M/(R c_*).

It does NOT give exp(f), exp(2^f), or an eigenvector-conditioning denominator. Adding finitely many wall jumps and the other coefficient gates produces an explicit polynomial V_A. The scalar E0 density, obtained from h p_k(h) and a per-site trace, has a similarly polynomial variation bound and is handled directly by (2).

## 6. Reversible arithmetic and Gaussian gates

For a term label and the phase-grid registers:

1. Compute local edge differences, floors, cup products and integer shear data reversibly. Grid coordinates are integers; these comparisons and modular additions are exact. Smooth phases, normalization, and h entries are evaluated to b-bit precision. The texture denominator is bounded below by c_*.
2. Compute the necessary buffered one-body polynomial matrix using k matrix multiplications. Even dense one-body arithmetic costs O(k f_buffer^3) arithmetic operations, not 2^f. Reversible fixed-precision implementations add a polynomial overhead in b and log S.
3. Form the quadratic purification generator G_patch=sum_ab g_ab i gamma_a gamma_b with O(f²) coefficients. To avoid any unearned eigenvector or Gaussian-QR conditioning claim, use a simple product formula. Its summed term norm is at most C f². First-order Trotter with n_steps=O(f^4/eta_G) has uniform unitary error eta_G. This uses O(f^6/eta_G) elementary pair rotations; Jordan–Wigner strings or fermionic swaps cost at most another polynomial factor (O(f) within a patch, or O(V) with a fixed global ordering). Better Gaussian synthesis is optional, not required for polynomiality.
4. Uncompute coefficient arithmetic. The rotor registers were unchanged throughout controlled Gaussian evolution. Cochain scalar phases and local matching rotations require only polynomially many additional controlled rotations.
5. Implement P_0,v by a QFT, an exact test for momentum zero, and inverse QFT. Equivalently a reset term is the LCU (I-A R_0 A†)/2 with R_0=2P_0-I, so its normalization is1. The active momentum-zero state is exact in the finite grid model. QFT/gate synthesis error is budgeted separately.

Pointwise circuit errors perturb the encoded reset by at most twice the unitary error. They need not themselves have a variation bound: first compare the ideal grid to the continuum by (4), then the implemented grid to the ideal grid uniformly. Binary arithmetic precision b=O(log(poly(f,k,S)/eta_G)) suffices with explicit propagation bounds. Floor decisions never use approximated real angles.

Fast quadratic terms are LCU sums of O(f²) fermionic Pauli words with computed coefficients. Scalar E0 terms use the computed bounded scalar and a controlled rotation. No dense Fock matrix or dense rotor kernel is stored.

## 7. Axial averaging and EXACT final charge pinching

The pre-disentangler axial average is implementable as a finite average of controlled local matching rotations and scalar cochain phases. In the doubled compact convention each matching projector and each distributed countercharge has integer spectrum. Restrict to the causal support of the term. A uniform cyclic phase register larger than twice that support's charge range reproduces the Haar average exactly in the ideal arithmetic model; its size is polynomial in f,p and fixed charges. This average introduces no exponential gate count.

After D† and physical Fourier cutoff, the gauged charge on a support is

 Q_X=sum_(theta in X) L_theta+sum_(free orbitals in X) q_a n_a+known integer offsets.

Matter phi rotors are neutral. Hence its finite integer range has width O(pL+f q_max+offsets). Numerical approximation before pinching need not respect this charge.

There is a more robust exact implementation than approximate phase rotations. Given any block encoding U of an approximate term A_tilde, compute the INPUT integer Q_X into a clean ancilla register. Apply U. Subtract the OUTPUT integer Q_X from that register. Accept only ancilla value zero, together with U's original acceptance ancillas. The resulting Hamiltonian block is EXACTLY

 Pinch(A_tilde)=sum_q P_q A_tilde P_q.

Use an integer register larger than twice the charge range, so equality cannot alias. Charge computation uses exact reversible integer addition and fermion-occupation controls. This needs O(log(pL+f q_max)) ancilla bits and polynomial gates, with no loop over all charge sectors and no approximate continuous-symmetry rotation. Pinching is norm contractive. Since the target compressed term is symmetric, its error cannot increase. This establishes exact U(1) invariance of the encoded finite Hamiltonian independently of floating coefficient errors. Usual gate-synthesis errors in the block-encoding unitary remain a separate implementation error; the integer-equality construction itself is exact.

## 8. Total resource closure, including the coercive completion

Allocate eta=epsilon_H/(C T lambda) to each normalized term, including quadrature, coefficient evaluation, Gaussian evolution and block-encoding errors. Take a power-of-two grid with

 S >= max(4L'+2,
          C eta^-1 p(2L'+1)[sqrt(2L'+1)V_A+L'+1]).                     (6)

This is polynomial, not exponential, in the cutoff, patch size and inverse error. Quantum registers use log S bits per rotor, not S basis amplitudes stored classically. The local spectral degree is

 k=O((R/g)² log(poly(V,f)/eta)),

using the explicit binomial tail. The geometric buffer and purification radius grow polynomially in k and logarithmically in the global finite-volume accuracy. At fixed microscopic parameters, f,p are polynomial in log(V/eta), with large fixed lattice/refinement constants.

One intentionally conservative per-term bound is

 G_term <= poly(k,f_buffer,b,log S)+O(f^7/eta),

plus a polynomial factor if globally routed Jordan–Wigner strings are used. LCU selection may simply loop over all T labels, so a total block-encoding query costs at most T times that polynomial; efficient address oracles are not assumed. Its normalization may be chosen

 alpha <= C T lambda + kappa m L²,

also polynomial. The kinetic completion kappa sum L_j² is diagonal binary arithmetic and is compiled exactly up to scalar rotation precision.

From FINITE_AUXILIARY_COERCIVE_REGULATOR.md, the trial cutoff N is polynomial in V and inverse desired ground error; choose kappa=e_target/(4mN²). For finite-energy real-time error epsilon up to time t, its larger evolution cutoff

 L+1 >= (2+t B_R)sqrt(E/kappa)/epsilon,

with L>=N, is polynomial in V,E,t,1/epsilon. Substituting it into (6), alpha and G_term preserves polynomial scaling. Taking epsilon_H<=epsilon/(2t) pays simulation error from the approximate Hamiltonian. Ordinary bounded-Hamiltonian block-encoding simulation or even an inefficient polynomial product formula then has polynomial gate cost in those variables. This is an actual gate-count closure, not a qubit-count claim.

Constants inherit the astronomical Wilson UV refinement, small g/R, long purification range, and weak kappa. The polynomial assertion is asymptotic with those FIXED and does not imply a practically usable chiral simulator.

## 9. Executed checks and scope

check_polynomial_grid_compiler.py validates a two-rotor, one-fermion unitary reset with a moving floor wall. Operator-norm errors against a fine reference decrease approximately as1/S: 0.03459 atS16,0.01708 at32,0.008389 at64,0.004056 at128. The integer charge-equality mask commutes with Q exactly and agrees with discrete twirling to6.25e-16. Dense matrices occur only in this small validation, not in the compiler construction.

Outstanding independent gates remain the complete physical near-interface/open-chiral-surface contract, gauged-background/dynamical-gauge control, and practical resource improvement. The present result addresses finite-volume coefficient/gate acquisition for the already specified finite auxiliary Hamiltonian.


Audit correction: uniform slice BV and L-infinity-valued BV were distinguished after the moving-wall audit. The spectator-reset estimate now pays sqrt(d), as derived in Section3. This changes polynomial exponents but does not restore an exponential rotor-dimension factor.

## Explicit valid-code and Hermiticity safeguards (compiler audit)

A rotor's logical input is the valid integer code n in[-L,L] inside ceil(log2(2L+1)) qubits. Define the explicit isometry J by mapping that signed integer to n modulo S in a padded grid register, followed by the S-point QFT. Both its input domain test and its inverse output acceptance test use exact integer comparisons. Every encoded term is sandwiched by these valid-code isometries and their acceptance projectors. Padding states are not additional physical rotor states and cannot couple to the accepted physical Hamiltonian block. Charge pinching alone would not enforce this. If a full qubit Hamiltonian rather than a subspace encoding is desired, extend by an explicit positive invalid-code penalty and zero cross blocks; the valid sector stays invariant.

Hermiticity is construction-enforced despite finite arithmetic: synthesize A once, and use the EXACT reversed gate list for A† in A R0 A†. Use a QFT circuit and its exact reversed inverse. The resulting conjugated reflection is Hermitian exactly as an ideal logical circuit even if its intended angles were approximated. For fast terms use real coefficients of Hermitian Pauli strings, and real scalar approximants. Alternatively replace any computed block by (A+A†)/2 via a two-branch LCU, which is contractive on error to a Hermitian target. Valid-code compression and integer charge pinching preserve Hermiticity. No eigensolver or dense symmetrization is required.

Fixed-precision matrix recurrence is also stable with polynomial precision. Keep the approximate B=1-h²/R² norm at most1+O(1/k); then k repeated products amplify roundoff by at most a fixed exponential in that O(1) total, not exp(k). Per-entry arithmetic precision O(log(poly(k,f_buffer)/eta)) suffices after accounting for matrix-dimension norm conversion and all k steps. Explicit Hermitian/antisymmetric averaging of the one-body generator preserves these error bounds.

## A concrete asymptotic substitution and simulation interface

If the fixed-microscopic ledger has A_tail<=aV, B<=bV and m<=cV, with volume-independent Delta>0, the finite auxiliary theorem permits N=O(V²/epsilon_g²) and the explicit choice kappa=e_target/(4mN²)=Theta(epsilon_g^6/V^5), where e_target is a fixed multiple of Delta epsilon_g². One may take

 L=O(V²/epsilon_g² +(1+tV)sqrt(E) V^(5/2)/(epsilon_t epsilon_g³)).

Here epsilon_g is the target ground error and epsilon_t the finite-energy real-time cutoff error; constants retain all paid microscopic factors. This is only one conservative resource choice. Radius O(log²(V/errors)) from the open-surface worker still gives f,p polynomial in log(V/errors), so it fits the compiler unchanged. The worker confirmed that its physical patch uses the exact unitary exponential of a bounded polynomial quadratic generator; its Taylor truncation is used only in an analytical locality comparison. Its coefficient bound B_poly^(2J) costs O(kJ) precision bits and is not an instruction to enumerate walks.

For the obtained Hermitian alpha-normalized block encoding, standard Hamiltonian simulation applies. Low–Chuang, arXiv:1610.06546v3, Theorem1 and its Section6 proof give O(alpha t+log(1/epsilon_sim)) controlled block-encoding queries (a weaker polynomial query bound would already suffice here). The input unitary, inverse, and preparation circuits are the explicit circuits above, not additional data-access or ground-state oracles. Taking epsilon_H<=epsilon_sim/(2 max(t,1)) bounds the evolution error caused by coefficient compilation by t epsilon_H. Multiply the query bound by the explicit per-query gate bound in Section8, and add polynomial ancilla/phase synthesis overhead. Thus the full finite-energy dynamics gate count is polynomial in V,E,t,1/epsilon_g,1/epsilon_t,1/epsilon_sim at fixed microscopic parameters.

Primary simulation source inspected: https://arxiv.org/html/1610.06546v3 . The new acquisition work here is the controlled cochain/Gaussian/cutoff block encoding; qubitization itself is an established component.

A fully elementary polynomial simulation fallback avoids treating QSP phase synthesis as an extra oracle. Split time into r=max(1,ceil(alpha |t|/log2)) segments. For each segment use the truncated Taylor polynomial in the encoded A=H_alg/alpha, with positive LCU magnitudes (alpha |t|/r)^j/j! and phases(-i)^j. Encode A^j by j calls to the acquired unitary with fresh acceptance ancillas. Add a zero-block branch so the total LCU normalization is exactly2. Factorial weights are computed by a recurrence; their state preparation and controlled selection cost polynomial in the truncation degree. One oblivious-amplitude-amplification step maps an exact unitary block U/2 to U; a truncated block has polynomially controlled error. Choosing the Taylor error conservatively O(epsilon_sim²/r²) makes total amplified state error O(epsilon_sim), with degree O(log(r/epsilon_sim)). Thus O(r polylog(r/epsilon_sim)) acquired-oracle calls and polynomial gate/ancilla overhead suffice, without an uncomputed matrix function or optimized phase-list oracle. This is the standard truncated-Taylor/LCU mechanism of Berry–Childs–Cleve–Kothari–Somma, https://arxiv.org/abs/1412.4687, specialized to powers of the block encoding already constructed here. It is less efficient than optimized qubitization but enough for the asserted polynomial capability.
