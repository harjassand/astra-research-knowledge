# Fixed-form differential representation: result and disposition

The strongest result from this branch is an exact fixed-template theorem for **finite Hermitian matrix polynomials in commuting variables**. Its proof also shows why the original polynomial consequence should not be promoted as a new foundational positivity principle: familiar real algebraic machinery already implies it.

For

\[
 p_L(x)\propto\exp\!\left[-L\sqrt{1+|x/L|^2}\log\sqrt{1+|x/L|^2}\right],
\]

and \(P(0)\succ0\),

\[
 P(g)\succ0\ \forall g\in\mathbb R^m
 \quad\Longleftrightarrow\quad
 P(-\partial)p_L\succ0\ \hbox{everywhere for all sufficiently large }L.
\]

Existence of even one \(L\) with semidefinite output is also equivalent. The proof gives a relative operator sandwich and exact normalization. The profile is fixed across all degrees and finite matrix sizes; the sufficient broadening is instance dependent. The constant-kernel semidefinite extension is included.

The hypothesis removed from the *construction* is dependence of the density shape on the entire unknown margin function. No uniform lower bound or positive leading homogeneous form is imposed. This follows because the strict Krivine–Stengle Positivstellensatz applied to \(\det P\) already supplies an algebraic lower bound. A finite exponential derivative expansion then controls the whole tail. This proof does not need the general PR94 compact-distribution theorem.

The most concrete quantitative result is a sharp example. For

\[
 Q(s,t)=(st-1)^2+s^2,
\]

the radial family

\[
 p_{L,\beta}(x)\propto
 \exp\!\left[-\frac L{1+\beta}
 \left((1+|x/L|^2)^{(1+\beta)/2}-1\right)\right]
\]

can regularize \(Q(-\partial)\) for all sufficiently large \(L\) exactly when \(0<\beta\le1/5\). The resulting sharp tail exponent is \(6/5\), **within this specified density family**. For any \(\beta>1/5\), a remote valley gives negative output for every fixed \(L\). Every nondegenerate Gaussian also fails, even with freely chosen covariance and mean. A sequence of strictly positive scalar polynomials rules out a single fixed power exponent greater than one for the whole polynomial class.

The finite-dimensional restriction has an exact obstruction. The degree-two operator polynomial

\[
 \operatorname{diag}_{n\ge1}
 \frac{(g-n)^2+e^{-2n^2}}{n^2+e^{-2n^2}}
\]

is normalized and boundedly positive at each finite real \(g\), but no member of the fixed logarithmic family regularizes it. Thus this sharpened corollary does not inherit the dimension independence of the supplied bounded-quantum-tuple result. The general margin-adapted PR94 theorem is not contradicted.

Two tempting promotions are closed negatively. Commuting partial derivatives erase free commutators, so the representation does not imply noncommutative sums-of-squares positivity. An explicit Pauli substitution witnesses failure. A positive differential output also does not give a positive Green function or a positive inverse for prescribed PDE sources; \(1+\partial^2\) is an elementary counterexample.

**Disposition:** retain the fixed-form theorem, margin-to-tail estimate, sharp scalar example, and infinite-operator obstruction as a proof-backed mathematical corollary and useful classification boundary. Do not promote this branch to an efficient positivity algorithm, a new Hilbert-17 solution, a free noncommutative Positivstellensatz, a new measurement capability, or exceptional foundational significance. Exact historical priority for the fixed-template wording remains uncleared.

`PROOF.md` contains the complete arguments and primary-source comparisons. `checks.py` and `checks.json` verify five finite symbolic identities, the commutator counterexample, and selected high-precision tail evaluations. Those checks are not a proof of global positivity. `SOURCE_RECEIPTS.json` pins the actual PR94 source commit and acquired primary webpages.
