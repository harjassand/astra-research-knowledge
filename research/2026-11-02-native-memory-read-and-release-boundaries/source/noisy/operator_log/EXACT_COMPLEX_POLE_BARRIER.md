# Exact local inverse-Pauli/Gibbs countertest: no uniform joint-analytic operator logarithm
1 November 2026, 22:41 UTC. Independent constructor follow-on. This is an exact structural obstruction to one proposed proof method, NOT a no-go theorem for real-parameter quasi-locality or physical preparation.

## Result
There is a bounded-degree, bounded-strength, nearest-neighbor/3-local qubit Hamiltonian family A_n and a single onsite Pauli P such that the derivative at zero inverse-noise strength of
 K_n(t,z)=-log[ exp(t(id-AdP)) exp(-z A_n) ]
has a genuine complex pole at |z|=Theta(1/n). The branch is fixed by K_n(0,z)=z A_n near z=0. Therefore no volume-independent disk of joint analyticity in weak Hamiltonian scale z and inverse-noise strength t can hold for this special inverse-Pauli/Gibbs structure. Positivity for sufficiently small real t,z does not remove the obstruction.

## Explicit physical Hamiltonian
On n qubits let N_i=(I-Z_i)/2. Give the boundary symbols fixed values N_0=1 and N_{n+1}=0. Set
 A_n = sum_{i=1}^n N_i + g sum_{i=1}^n N_{i-1} X_i (I-N_{i+1}),
where 0<g<1/4 is any fixed constant. Boundary terms use the displayed fixed symbols. Every term is Hermitian, bounded strength, and supported on at most three adjacent sites. The interaction degree is uniformly bounded. Take P=Z_1.

The domain-wall subspace D_n is spanned by |j>=|1^j 0^(n-j)>, j=0,...,n. It is invariant: the constrained flip only moves the domain wall left or right by one. In this subspace A_n is the (n+1)-dimensional irreducible Jacobi matrix J_n with
 (J_n)_{jj}=j, (J_n)_{j,j+1}=(J_n)_{j+1,j}=g.
The Pauli restricts to P_D=2|0><0|-I.
The spectral width Delta=E_max-E_min is between n and n+4g, by endpoint Rayleigh quotients and ||offdiag J||<=2g. Thus 2pi/Delta=Theta(1/n).

## Exact pole proof
Let E_a=E_min, E_b=E_max, and take real normalized Jacobi eigenvectors. Put u_c=<0|E_c>. Every u_c is nonzero: if the first component vanished, the three-term recurrence and g!=0 would force all components to vanish. The spectrum is simple and all other eigenvalues lie strictly between the extremes.

The unnormalized inverse-noise state's derivative at t=0 is
 S'_t=e^{-zA_n}-P e^{-zA_n}P.
Writing K'_t=-Dlog_{e^{-zA_n}}(S'_t), its offdiagonal (a,b) matrix element in the fixed energy basis is
 [K'_t]_{ab}= -z(E_a-E_b) (P e^{-zA_n}P)_{ab}/(e^{-zE_a}-e^{-zE_b}).
(The overall sign is irrelevant to the pole; it follows directly from the divided difference of log.)

Choose z_*=2pi i/Delta. Then e^{-z_*E_a}=e^{-z_*E_b}=:lambda. Within the invariant domain-wall block, the numerator is
 (P_D e^{-z_*J_n}P_D)_{ab}
 =4u_a u_b [M(z_*)-lambda],
 M(z)=sum_c u_c^2 e^{-zE_c}.
The weights u_c^2 are strictly positive and sum to one. After dividing by lambda, the endpoint phases are 1, while every interior phase is exp[-2pi i(E_c-E_a)/Delta] != 1. Hence
 Re[M(z_*)/lambda] < 1
for n>=2. Therefore M(z_*)!=lambda and the numerator is NONZERO. The denominator has a simple zero (Delta!=0); z_*!=0. A genuine simple pole follows.

This is a block of the full physical operator, so it cannot be canceled by states outside the domain-wall sector. Accidental cross-sector degeneracies do not affect the invariant-block argument. Taking the state normalized instead only adds a scalar log-partition-function contribution and does not affect this offdiagonal pole.

## What this rules out
* Volume-uniform complex Cauchy disks around z=t=0 for this operator logarithm.
* Uniform absolutely convergent multivariate Taylor/linked-cluster estimates that would imply such joint analyticity in weak local strengths and noise strength.
* The proposed inference: real-axis matrix-gas positivity + finite connected support => a uniform operator-log analytic cluster theorem.
* Treating the absence of matrix-gas zero eigenvalues as sufficient to select a holomorphic operator logarithm perturbatively in these variables. The obstruction is noncommutative exp/log derivative degeneracy, not Gibbs-operator singularity.

## What remains open
This does NOT prove failure of an exponentially cardinality-local real-parameter interaction representation, if its coefficient functions are nonanalytic/nonperturbative in z. Nor does it rule out resummed finite-difference cluster coefficients with a carefully proved real-axis bound, an efficient circuit representation based on real-time filters, or a direct physical preparer. It also does not directly establish this pole family inside the particular nontrivial code-reference Hamiltonian; it invalidates the proposed generic near-commuting theorem already at the Href=0 special case. Any extension to the fixed code must exploit additional structure or explicitly avoid the invalid joint-analytic route.

## Why the modular-flow identity does not close preparation
The exact K flow uses an exponentially decaying real-time kernel. In d-dimensional geometry, an LR radius O(v|s|) contains O((v|s|)^d) spins, so this implies at best a stretched-exponential support-cardinality bound exp[-c m^(1/d)/v]. The absolute nested-commutator series has a finite time radius and cannot be integrated termwise to infinity merely because v is small. Cutting at time O(1/v) leaves a nonzero constant tail exp[-c/v], which cannot silently be discarded at global inverse-polynomial error as N grows. The exact pole family supplies an independent algebraic diagnostic of this issue.

## Numerical files (secondary checks)
`test_log_complex_poles.py/.txt`: generic uniformly bounded interacting chain, n=2..9, nonzero residues and decreasing pole moduli. `verify_pole_highprecision.py/.txt`: n=5 generic-chain residue verified at 70 decimal digits, |residue|=0.000003004019820340727666605043940796531154312273217694. These numerics are not needed for the exact Jacobi-family proof above.
