# Warm-continuation result

The full all-copy qutrit Werner target remains **unresolved**. There is no negative admissible endpoint witness in this continuation.

I retained the stage-one Cauchy growth construction and tested a possible global replacement by unconstrained polynomial-square certificates. This produced exact auxiliary PPT separators and matching positive identities.

For the free rank-two factorization polynomial

\[
f_n(U,V)=q_n(UV^*)=\langle a\otimes b,W_n(a\otimes b)\rangle,\qquad
W_n=(I-O_3/2)^{\otimes n}\otimes O_2,
\]

I proved the uniform bounds

\[
\operatorname{dist}_\infty(W_n,\mathrm{decomposable})\ge1/7,
\]

and

\[
\operatorname{dist}_\infty\bigl((W_n+W_n^\Gamma)/2,
\mathcal S(\mathrm{PSD})\bigr)\ge1/8.
\]

Both constants are sharp at one copy. They are certified by explicit normalized rational positive matrices on \(6\)-by-\(6\), with matching decomposable/SOS identities. The second separator is itself unchanged by partial transpose. Product spectator pairs preserve both margins at every copy number.

Equivalently, one-copy positivity requires no added noise, yet a free-variable polynomial SOS requires exactly \(1/7\) times \(\|U\|_F^2\|V\|_F^2\) for complex variables, or \(1/8\) for real variables. More generally, throughout \(0\le t\le1\), the exact thresholds for \(q_{1,t}(UV^*)+\delta\|U\|_F^2\|V\|_F^2\) are:

| Property | Smallest \(\delta\) |
|---|---|
| Actual positivity | \(\max(0,t-1/2)\) |
| Real-variable SOS | \(\max(0,(3t-1)/4)\) |
| Complex-variable SOS | \(\max(0,2(3t-1)/7)\) |

The qualitative non-SOS phenomenon is prior work of Hiroshima (2010), found and read during opposition testing. It is not claimed as new. This block preserves explicit rational separators, attaining identities, exact thresholds and a copy-uniform obstruction; historical priority for those formulas is unestablished.

The strongest scope check is positive: orthonormality constraints admit an ordinary Lagrange-square certificate already at one copy. Therefore this obstruction does not exclude constrained SOS, rational multipliers or the actual orthonormal-frame \(\Gamma_n\) route. It excludes promoting an unconstrained quartic Gram matrix, or vanishing unweighted SOS noise, into an all-copy proof.

The complex separator also yields an explicit PPT activator \(\alpha\). With that additional entangled resource, local Bell projections produce the two-qubit state \((8I-5F_2)/22\), whose partial transpose has eigenvalue \(-1/11\), with success probability \(11/945\). This is an activation calculation, not a Werner-copy counterexample. Preparation of \(\alpha\) from the target Werner copies has not been established.

Complete proofs are in PROOF.md. Exact rational/symbolic checks in verify.py all pass; verification.json records the margins, parameterized identities, spectator embedding, activation contraction and constrained-SOS control. Stage-one and frozen-stage-one files were preserved.

The unresolved scientific obligation is still to prove subexponential growth of \(\Gamma_n\), or construct exact frames violating its Cauchy determinant. No positivity premise equivalent to that obligation has been assumed.
