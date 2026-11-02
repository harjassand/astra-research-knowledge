# Independent receipt: exact inverse-Pauli operator-log complex pole

2026-11-01. **PASS, with the analytic-method scope stated below.**

Audited root: `../EXACT_COMPLEX_POLE_BARRIER.md`, SHA256 `8b4a5736584af03bc64a8344c7847012c3d4dae5225b14b0bf769e6864cb2400`. Read the constructor notes and numerical scripts. This receipt proves the special-structure obstruction directly; no literature warning is used in place of proof.

## 1. Full physical chain, not an independently chosen spectral toy

Let 0<g<1/4 be fixed, N_i=(I−Z_i)/2, N_0=1, N_(n+1)=0, and

    A_n = Σ_i N_i + g Σ_i N_(i−1) X_i (I−N_(i+1)).

Each summand is Hermitian because its factors act on different sites. It has support on a contiguous interval of at most three qubits, norm at most max(1,g), and every site meets a uniformly bounded number of terms. Thus zA_n is a genuine bounded-degree, uniformly bounded-strength family as z varies; the argument does not posit small global ||zA_n||.

For |j>=|1^j 0^(n−j)>, only flips i=j and i=j+1 can survive, with the endpoint cases omitted. All others are killed by one of the two neighbor projectors. Hence the domain-wall subspace is invariant, and since A_n is Hermitian it is reducing. In that subspace it is exactly the tridiagonal Jacobi matrix J with diagonal 0,...,n and adjacent off-diagonals g. The physical onsite P=Z_1 also preserves the subspace and restricts to 2|0><0|−I. Consequently both the Gibbs exponential and the inverse-noise superoperator preserve this block. Other physical sectors cannot cancel any of its matrix elements.

The endpoint Rayleigh quotients give E_min≤0 and E_max≥n. The hopping norm is at most 2g, giving E_min≥−2g and E_max≤n+2g. Thus n≤Delta:=E_max−E_min≤n+4g.

## 2. Nonzero residue

The Jacobi matrix has simple spectrum. An eigenvector with first component zero has every component zero by the three-term recurrence, so each spectral endpoint amplitude u_c=<0|E_c> is nonzero. Choose real eigenvectors. Their squared amplitudes are strictly positive and sum to one.

Write S(t,z)=exp[t(id−Ad_P)] exp(−zA_n), and let K(t,z) be the analytic logarithm germ near (0,0) with K(0,z)=zA_n. This germ exists in every finite volume near the identity. For a=minimum and b=maximum energies, divided differences give

    (∂_t K)(0,z)_(ab)
      = z Delta (P exp(−zJ) P)_(ab)
        / (exp(−zE_a)−exp(−zE_b)).

At z*=2πi/Delta, write lambda=exp(−z*E_a)=exp(−z*E_b). Expanding P=2uu^T−I in the energy basis yields

    (P exp(−z*J) P)_(ab)
       = 4 u_a u_b [M(z*)−lambda],
    M(z)=Σ_c u_c² exp(−zE_c).

For n≥2 there is at least one interior eigenvalue. Each interior normalized phase exp[−2πi(E_c−E_a)/Delta] has real part strictly below one; endpoint phases are one. Strictly positive weights therefore imply Re(M(z*)/lambda)<1. No cancellation is possible in M−lambda. The numerator is nonzero.

The denominator has derivative Delta lambda at z*, hence a simple zero. The residue of this matrix element is exactly

    z* (P exp(−z*J)P)_(ab) / lambda != 0.

The pole modulus is 2π/Delta=Theta(1/n). The residue may be very small; its nonvanishing, not a uniform lower bound, is all the analyticity obstruction requires.

## 3. Branch-independent formulation and quantifiers

This is not an artifact of choosing the principal scalar logarithm after eigenvalue phases wind. Suppose a holomorphic matrix K(t,z) existed on a product neighborhood containing t=0 and z=z*, agreed with the germ near zero, and satisfied exp(−K)=S. The identity theorem forces K(0,z)=zA_n. Differentiate the exponential identity in t. In the (a,b) energy entry, the derivative map multiplies (∂_t K)_(ab) by

    −∫_0^1 exp[−(1−s)zE_a−s zE_b] ds.

At z=z* this multiplier is zero, whereas the required derivative of S is −(P exp(−z*J)P)_(ab), which is nonzero. Contradiction. This also covers any hypothetical logarithm with additional cross-sector components: the exponential derivative is entrywise in the full energy basis, so those components cannot repair this entry.

Therefore there cannot exist a volume-independent positive complex z-radius and t-radius on which this germ extends jointly holomorphically for every n. Nor can uniformly absolutely convergent multivariate Taylor/coefficient bounds hold if they imply such a neighborhood. It is sufficient to restrict all local Hamiltonian couplings to the single direction z and use one onsite noise coordinate t. A claimed stronger independent-coupling analytic theorem would restrict to this forbidden slice.

The noise is exactly the intended inverse of a Pauli channel: exp[t(id−Ad_P)] is C_q^−1 with q=(1−exp(−2t))/2. Since q is analytic with nonzero derivative at t=0, replacing t by q cannot remove the obstruction.

Trace normalization is irrelevant to this off-diagonal contradiction. The inverse-noise map is trace preserving, so Tr S(t,z)=Tr exp(−zA_n). Whenever normalization and its logarithm germ are defined, normalization adds only log Z(z) times the identity to K, with no t dependence. Possible complex zeros of Z cannot restore a missing uniform analyticity domain.

## 4. Independent exact-family diagnostic

Saved and ran `test_exact_jacobi_pole.py`, with output `exact_jacobi_results.txt`. For n=2,...,7, g=0.2 it builds the FULL 2^n-dimensional physical chain and checks A V=VJ and P V=V P_D, the spectral-width bounds, the spectral-weight numerator identity, and the residue limit along z=z*+h.

The residue limit was checked at h=10^−5,10^−6,10^−7; its relative discrepancy decreases by approximately a factor ten each time. At n=7 the last relative discrepancy is about 1.02×10^−5 and |residue|≈2.72×10^−10. An initial overly tight tolerance at fixed h=10^−6 failed due to this ordinary O(h) finite-offset error; replacing it with the explicit convergence check resolved the diagnostic, without changing the mathematical argument. No finite computation is used to infer the all-n strict positivity of spectral weights or the all-n pole.

The author's other numerical scripts concern generic chains and are secondary corroboration, not the explicit Jacobi-family proof.

## 5. Exact scope

This refutes a volume-uniform JOINT complex-analytic/Taylor-Cauchy operator-log closure, including the inference that real-axis positivity plus connected support automatically supplies such a closure. Invertibility of exp(−zA_n) does not imply this logarithm can be continued jointly with inverse noise: the obstruction is the differential of the exponential at a noncommutative resonance.

It does NOT prove failure of real-axis exponentially cardinality-local descriptions, nonanalytic or resummed real-axis methods, efficient preparation by a different construction, or the admitted ideal Gibbs encoder based on exponentials. It is a counterexample at H_ref=0; embedding it into a particular nontrivial code reference is not established here. Fixed-volume real analytic neighborhoods and positivity for sufficiently small real parameters are fully compatible with this result.

The constructor's modular-flow caution is correctly a limitation of the stated estimate: an exponential real-time tail combined only with d-dimensional LR radius yields a stretched-exponential cardinality estimate, not the desired exponential-cardinality theorem. This is not a lower bound on the true locality, and the complex pole alone does not exclude all real-axis closure arguments. No physical-preparation or universal memory no-go conclusion is licensed.
