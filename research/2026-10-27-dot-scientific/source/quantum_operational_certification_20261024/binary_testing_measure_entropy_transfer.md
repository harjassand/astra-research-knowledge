# Exact scalar transfer for balanced two-source trace entropy

25 October 2026. Root derivation with independent mathematical review. Governing
external ingredient is Frenkel's2023 integral formula, not a physical common
measurement. Historical priority of this consequence has not been established.

## The positive testing measure

Let A,X be faithful positive matrices on the SAME finite-dimensional space. Set
h(t)=Tr(A-tX)_+ for t>=0. This is convex, nonincreasing and eventually zero.
For small positive t the pencil is positive, so h(t)=Tr A-t Tr X. Let mu=h'' in
the distributional sense, a finite positive measure supported in a compact
subinterval of(0,infinity). Then
h(t)=integral(r-t)_+ mu(dr),
integral mu=Tr X, integral r mu=Tr A.
The first identity follows by integrating h'' twice with the zero boundary
conditions at infinity. The moments follow at t0 and from the right derivative.

The abstract classical positive densities r and1 on this measure space match
Tr(alpha A+beta X)_+ and Tr(alpha A+beta X)_- for EVERY real alpha,beta.
For opposite signs use h and the trace identity TrY_+-TrY_-=TrY; for equal signs
positivity/negativity and the two moments suffice. No simultaneous Helstrom
measurement, physical simulator, positive decoder or sufficient statistic is
asserted. The measure represents a testing CURVE, not one acquired experiment.

## All positive-mixture relative entropies

For Y=alpha A+beta X and Z=gamma A+delta X with nonnegative coefficients and
nonzero mixtures, Frenkel Theorem6 expresses Umegaki D(Y||Z) as Tr(Y-Z) plus a
positive integral of the negative trace of (1-t)Y+tZ. Every such pencil has the
same positive/negative trace as its classical counterpart, hence
D(Y||Z)=integral (alpha r+beta) log[(alpha r+beta)/(gamma r+delta)] mu(dr).
The trace term is essential for unequal traces and is matched by the moments.
Classical interchange of the nonnegative integral follows by Tonelli. Faithful
finite source matrices keep r in a compact positive interval.

Primary source, actually read: P. E. Frenkel, Integral formula for quantum
relative entropy implies data processing inequality, arXiv:2208.12194v4,
Theorem6, https://arxiv.org/html/2208.12194 . The theorem explicitly allows
positive semidefinite matrices with unequal traces. It is not a statement that
quantum experiments are physically classical.

## Balanced entropy identity and scalar-equivalence theorem

Write S(Y)=-Tr Y log Y. Suppose alpha_j,beta_j>=0 and real coefficients c_j obey
sum c_j alpha_j=sum c_j beta_j=0. Then EXACTLY
sum c_j S(alpha_j A+beta_j X)
 =integral sum c_j[-(alpha_j r+beta_j)log(alpha_j r+beta_j)] mu(dr).
To prove it, rewrite the left side as -sum c_j D(alpha_j A+beta_j X || A+X).
The reference-log contribution cancels by BOTH balance conditions. Apply the
previous divergence identity and cancel its classical reference log(r+1).

Therefore any scalar inequality of this balanced form, with optional linear
terms a Tr A+b Tr X, holds for all positive matrices if and only if it holds for
all nonnegative scalars. Sufficiency follows by integrating the scalar inequality;
necessity is the one-dimensional case. Singular finite matrices follow by
A+epsilon I,X+epsilon I and entropy continuity. Do not reuse the faithful
h'(0+) formula at singular A without accounting for the possible endpoint atom.

The theorem covers entropy of nonnegative linear mixtures of TWO fixed positive
sources. It does NOT cover arbitrary products/log-Euclidean means, partial
transposes, three or more independent sources, general matrix-valued functional
calculus inequalities, or an unbalanced combination of entropies. It gives no
physical classicalization and does not solve the nine-state Hesse target.

## Complete fixed-prior SDPI for a binary classical input

As a direct consequence, let T be any finite-output classical channel with TWO
input symbols and faithful fixed prior pi. Its fixed-prior scalar Umegaki SDPI
constant equals the constant after allowing arbitrary finite quantum reference:
for arbitrary positive A0,A1, K=A0+A1, Y_y=T_y0 A0+T_y1 A1,

sum_y Tr Y_y(logY_y-log((Tpi)_y K))
 <= eta(T,pi) sum_i Tr Ai(logAi-log(pi_i K)).

Zero output-prior symbols are omitted. The difference of the two sides is a
balanced two-source entropy combination plus linear trace terms, so the scalar
inequality lifts exactly by the theorem. Normalization is harmless by
homogeneity. Scalar references give the matching lower bound. This is fixed-
PRIOR, binary transmitted alphabet, arbitrary quantum-reference dimension; it
is different from the earlier arbitrary-alphabet/qubit-reference GLOBAL theorem.
No reduction of a general multi-symbol quantum-memory problem to binary symbols
is asserted.

## Actual receiving use

The theorem transfers a scalar diagonal-slack inequality in the1 plus adjoint
coherent SU3 channel to arbitrary noncommuting operator weights x,c. Together
with the independently proved sharp binary filter budget, it closes the b=0
coherent face. This is an actual use, not just an archive citation; see the
corresponding coherent-face proof. The general WH3 bound remains open.
