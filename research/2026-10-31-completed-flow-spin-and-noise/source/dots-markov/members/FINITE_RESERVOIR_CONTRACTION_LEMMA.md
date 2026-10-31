# Finite reservoir contractions are charged operations, not free oracles

Root lemma candidate, 31 October 2026. Intended only for an explicitly stored d-by-d reservoir matrix, not a black-box exponentially large system matrix. Independent review pending.

## 1. Dissipative exponential at binary-encoded time
Suppose Z+Z^dagger<=0 and a certified bound m>=||Z|| is known. Given a nonnegative finite-word time u and target absolute operator error delta, compute F=exp(uZ) by scaling and squaring. Choose s so ||uZ/2^s||<=1, with s=O(log(2+mu)). On the scaled argument use a Taylor polynomial of degree O(s+log(1/delta)); the factorial tail gives operator error at most delta/(100*3^s).

Every exact intermediate exponential is a contraction. If an approximate intermediate has error e<=1, one squaring gives error at most 2e+e^2 plus the multiplication error. Choosing each arithmetic error at most delta/[100(s+1)3^s] controls the final error by delta. This requires O(s+log(1/delta)+log d) working bits, with polynomial guard factors for matrix arithmetic, not a number of operations proportional to mu. Each matrix multiply is a finite d-dimensional operation. Rounding after each step keeps rational bit sizes bounded.

If Z itself is computed from certified finite input, approximate it sufficiently accurately that u||Delta Z|| is O(delta). Duhamel with the contraction bound gives ||exp(u(Z+Delta Z))-exp(uZ)||<=u||Delta Z||exp(u||Delta Z||). The needed additional bits are logarithmic in 1+u. Do not evaluate a decayed exponential and then divide by an underflowed scalar; evaluate the SHIFTED dissipative generator directly.

The result Fhat has norm at most 1+delta. Replacing it by Ftilde=Fhat/(1+delta) gives a certified contraction within 2delta of F. This small rescaling is charged to the error.

## 2. A normalization-one unitary dilation
For a contraction Ftilde, use the Julia unitary

U_F = [[Ftilde, sqrt(I-Ftilde Ftilde^dagger)],
       [sqrt(I-Ftilde^dagger Ftilde), -Ftilde^dagger]].

The intertwining identity Ftilde sqrt(I-Ftilde^dagger Ftilde)=sqrt(I-Ftilde Ftilde^dagger)Ftilde proves unitarity. Its top-left block is Ftilde with normalization ONE. This is essential: a sqrt(d) normalization at each virtual interval would accumulate along a word and defeat the intended resource claim.

Both square-root arguments M are positive contractions. Starting X0=I, the Newton iteration

X_(k+1)=(X_k+M X_k^-1)/2

commutes with M in exact arithmetic. For each eigenvalue m0 in[0,1], its scalar error x_k-sqrt(m0) is nonnegative and decreases by at least a factor two. Also 2^-k<=x_k<=1. Therefore O(log(1/delta)) iterations give absolute square-root error delta even when M has zero eigenvalues. No spectral gap for M is assumed.

For finite arithmetic, symmetrize each iterate and round at fixed precision. At iteration k the inverse norm is bounded by 2^(k+1) provided the accumulated error is below 2^(-k-1). The iteration map has a conservative Lipschitz bound at most 2^(2k+2) on that neighborhood. Thus O(B^2+B+log d) guard bits for B=O(log(1/delta)) suffice to preserve positive invertibility and final error O(delta). Exact rational matrix inversion within a step has polynomial bit complexity in d and the fixed working precision; round the new iterate before the next step so denominators do not grow across iterations unchecked. This proves a polynomial-bit square-root construction, not merely a formal matrix function.

## 3. Finite unitary synthesis, including coherent variable input
The computed dilation matrix is uniformly close to an exact unitary of dimension 2d. Stable QR/Givens elimination produces a product of O(d^2) two-level rotations and phases. All arithmetic is on an explicitly given matrix. A pair of entries with norm below a chosen absolute tolerance may be skipped with a charged error; otherwise its normalization denominator is bounded below by that tolerance. Approximate rotations are themselves unitary, and their operator errors telescope through the product. Near-unitarity keeps final column pivots well conditioned. Choose per-rotation arithmetic and synthesis errors polynomially smaller than delta/d^2.

This can also be seen through the QR factor of a matrix within eta of a unitary: its Gram matrix is within O(eta) of I; finite Cholesky/triangular estimates give an upper factor within O(poly(d)eta) of I. Hence its computed unitary factor is within O(poly(d)eta) of the desired dilation. Taking eta correspondingly smaller only adds logarithmic d guard precision. The small-pivot absolute-error rule avoids any promise about a relative error at a zero matrix entry.

If u is a quantum time register, perform the finite matrix arithmetic reversibly on u, store the rotation parameters, apply the corresponding two-level rotations to the reservoir register, then uncompute the parameters. Binary-controlled angle synthesis implements each finite angle; no table over 2^(time bits) values is stored. All branch-dependent arithmetic has a fixed polynomial bound and can be padded reversibly. Uniform per-u operator error gives the same error for coherent time superpositions.

Consequently F(u) has a normalization-one block encoding to error delta with cost polynomial in d, input/time bit lengths, log(2+mu), and log(1/delta), with source matrix computation charged. No large system matrix is accessed: the system's unknown quantum state is untouched except by its separately supplied operator encodings.

## 4. Interface to dark-sector excursions
For the Markov completion, Z=lambda(Df+cI/2) is dissipative on the fast reservoir sector. The word's scalar factor supplies exp(-lambda c u/2), while this lemma supplies the remaining contraction. The no-jump source may alternatively cap lambda*c*u at a logarithmic threshold, in which case even a source-conditioned fixed-step matrix scheme is polynomial. Timing perturbations must be bounded using lambda||Df+cI/2||, and digital-matrix error is charged separately. All matrix-size and source-conditioning factors remain explicit.

This lemma is a finite-dimensional arithmetic/synthesis construction. It is not a practical implementation, a black-box fast-forwarding theorem, or a substitute for the complete first-event isometry and private-time error ledger.
