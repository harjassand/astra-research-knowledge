# Approximate adjoints can suffice for a uniform forward-word certificate

Private P3 mathematical audit, 2026-10-23. No new literature search,
experiment, or numerical benchmark. Earlier completed files are unchanged.

## 1. Answer

**Yes, with an exact qualification:** approximate reverse operations may
be used only to acquire a finite pool of ideal moments, with a justified
finite-protocol bias budget. Once those intervals enclose the ideal Gram
and residual matrices, a deterministic certificate can cover every future
word of the true forward actions without a calibration error multiplied
by the target horizon.

The finite bias bound must be independently warranted. A few successful
reversal tests do not supply it. Obtaining a useful physical upper bound
on the relevant adjoint defects remains **UNKNOWN**. Exact common
stationarity and contraction of the target forward actions are distinct
requirements; approximate reverse access does not repair their absence.

## 2. Finite calibration bias, including a useful refinement

Let the true forward Markov operators \(A_a\) preserve one probability
measure \(\pi\). They and their adjoints are contractions in
\(\mathcal H=L^2(\pi)\). Let \(|f|\le B\). Let executable reverse Markov
operators \(B_a\) satisfy

\[
\|B_a-A_a^*\|_{\mathcal H\to\mathcal H}\le\delta_a.
\tag{1}
\]

The reverse operators themselves need not preserve \(\pi\) for the
following finite-acquisition result. Each trial must still begin with the
stipulated initial law; a reverse trial that changes that law cannot be
followed by another trial and silently called stationary.

For a fixed finite ideal query \(q=(K_1,\ldots,K_m)\), each \(K_j\) is a
forward operator or its ideal adjoint. Replace each ideal adjoint by its
executable reverse to obtain \(\widehat K_j\). Put

\[
C_q=\langle f,K_1\cdots K_m f\rangle,\qquad
\widehat C_q=\langle f,\widehat K_1\cdots\widehat K_m f\rangle.
\]

The telescoping identity

\[
K_1\cdots K_m-\widehat K_1\cdots\widehat K_m
=\sum_{j=1}^m K_1\cdots K_{j-1}
(K_j-\widehat K_j)\widehat K_{j+1}\cdots\widehat K_m
\]

gives

\[
\boxed{|C_q-\widehat C_q|
\le B^2\sum_{j:\,K_j=A_{a_j}^*}\delta_{a_j}.}
\tag{2}
\]

**Proof.** Ideal prefixes are \(L^2(\pi)\) contractions. Actual suffixes
are Markov operators, so their action on \(f\) remains bounded by \(B\)
pointwise, and therefore has \(L^2(\pi)\) norm at most \(B\). Apply (1)
and Cauchy--Schwarz to each term. The sharper prefactor
\(\|f\|_2B\) is also valid.

This avoids an unnecessary exponential factor
\((1+\delta)^{\#\mathrm{reverses}}\): the observable is bounded, and the
actual suffix is Markov. For dictionary forward words of length at most
\(L\), the Gram/residual queries below have at most \(L+1\) reverse
occurrences. Their uniform calibration allowance is consequently at most
\(B^2(L+1)\max_a\delta_a\).

If an actual-query confidence interval encloses \(\widehat C_q\), enlarge
it by (2) to enclose \(C_q\). Initial-law error
\(\|\nu-\pi\|_{\rm TV}\le\epsilon_0\) adds at most
\(2B^2\epsilon_0\). Calibration confidence, sampling confidence,
preparation error, readout error, and arithmetic error require a joint
valid event or deterministic bounds; they are not interchangeable.

### A weaker finite-domain contract is enough

Full operator-norm control in (1) is stronger than necessary. For the
finite query pool, define actual suffix functions

\[
g_{q,j}=\widehat K_{j+1}\cdots\widehat K_m f
\]

at every replaced adjoint position. It suffices to have
\(\|(B_{a_j}-A_{a_j}^*)g_{q,j}\|_2\le B\delta_{q,j}\)
for this finite set. The proof of (2) is unchanged. Even individual
bilinear bounds on the telescoping terms suffice.

The domain must contain the functions actually reached inside those
queries. Agreement merely on \(f\), or on a feature span lacking the
needed suffixes, is insufficient. These functions may be implicit and
unobservable individually; naming their finite set does not supply a
cheap calibration experiment. An obtainable upper bound remains UNKNOWN.

## 3. Separate forward and adjoint learned operations

Take a finite dictionary of forward words and write
\(v_i=A_{b_i}f\), \(V z=\sum_i z_iv_i\), with \(Ve=f\). Define

\[
G=V^*V,\quad H_a=V^*A_aV,\quad
J_a^R=V^*A_a^*A_aV,\quad J_a^L=V^*A_aA_a^*V.
\]

The ideal scalar queries are respectively

\[
b_i^\dagger b_j,\quad b_i^\dagger a b_j,\quad
b_i^\dagger a^\dagger a b_j,\quad
b_i^\dagger a a^\dagger b_j.
\]

Here the dagger reverses word order and replaces each symbol by its
adjoint. Approximate reverse operations acquire biased versions, which
(2) encloses. The two \(J\) matrices generally differ.

Choose arbitrary candidate matrices \(T_a\) for \(A_a\) and \(U_a\) for
\(A_a^*\). Let

\[
\begin{aligned}
D_a&=H_a-GT_a,\\
R_a^R&=J_a^R-H_a^*T_a-T_a^*H_a+T_a^*GT_a,\\
R_a^L&=J_a^L-H_aU_a-U_a^*H_a^*+U_a^*GU_a.
\end{aligned}
\tag{3}
\]

These are exactly the residual Gram matrices of
\(E_a^R=A_aV-VT_a\) and \(E_a^L=A_a^*V-VU_a\).

For a target word \(w=a_1\cdots a_n\), put

\[
l_0=e,\quad l_j=U_{a_j}l_{j-1},\qquad
r_n=e,\quad r_{j-1}=T_{a_j}r_j.
\]

The corrected prediction is

\[
Q_w=e^*Gr_0+\sum_{j=1}^n l_{j-1}^*D_{a_j}r_j.
\tag{4}
\]

### Exact two-sided remainder bound

For \(C(w)=\langle f,A_{a_1}\cdots A_{a_n}f\rangle\),

\[
|C(w)-Q_w|
\le\sum_{i<j}
\|E_{a_i}^L l_{i-1}\|\,\|E_{a_j}^R r_j\|.
\tag{5}
\]

**Proof.** Set \(x_0=f\), \(x_j=A_{a_j}^*x_{j-1}\). Telescoping the
right approximation gives
\(C(w)-\langle f,Vr_0\rangle
=\sum_j\langle x_{j-1},E_{a_j}^Rr_j\rangle\).
The terms with \(x_{j-1}\) replaced by \(Vl_{j-1}\) give the correction
in (4). Meanwhile

\[
x_j-Vl_j=A_{a_j}^*(x_{j-1}-Vl_{j-1})+E_{a_j}^Ll_{j-1}.
\]

Contraction bounds the prefix error by the sum of preceding left
residual norms. Cauchy--Schwarz proves (5). No inverse, rank promise,
selfadjointness of \(A_a\), or exact physical reverse is used here.

## 4. Uniform target-horizon bound

For simplicity use Euclidean coefficient norms and \(\|e\|_2=1\).
Suppose the enclosed ideal quantities certify

\[
\|U_a\|_2\le r_L<1,\quad\|T_a\|_2\le r_R<1,\quad
R_a^L\preceq\kappa_LI,\quad R_a^R\preceq\kappa_RI.
\]

Then (5) implies, simultaneously for every forward word,

\[
\boxed{|C(w)-Q_w|
\le\frac{\sqrt{\kappa_L\kappa_R}}{(1-r_L)(1-r_R)}.}
\tag{6}
\]

Indeed the finite double sum is
\(\sqrt{\kappa_L\kappa_R}
\sum_{p,q\ge0,\ p+q\le n-2}r_L^pr_R^q\), bounded by the product of
two geometric series. Different positive-definite coefficient metrics
work with the corresponding residual inequalities and initial-norm
prefactors.

If centers satisfy \(\|G-G_c\|_2\le\eta_G\) and
\(\|D_a-D_{a,c}\|_2\le\eta_D\), then

\[
|Q_w-Q_{w,c}|\le\eta_G r_R^n+
\eta_D\sum_{j=1}^n r_L^{j-1}r_R^{n-j}
\le\eta_G+\eta_D\min\left\{
\frac1{1-r_L},\frac1{1-r_R}\right\}.
\tag{7}
\]

The empty word is handled directly. Equations (6)--(7) contain calibration
error through the finite moment intervals and resulting constants, with
no additional \(n\delta\) term. A poor calibration can still make the
bound uninformative or prevent certification of useful residual constants.

One finite simultaneous moment event supports all subsequent words and
all fits whose deterministic inequalities are checked on that event.
Adaptive expansion of the query pool requires valid confidence handling
for the added measurements and calibration domains.

## 5. Exact counterexample to an insufficient calibration domain

Let \(\pi\) be uniform on three states, \(f=(1,0,0)^\top\), and

\[
A=\begin{pmatrix}
1/2&1/3&1/6\\
1/3&1/3&1/3\\
1/6&1/3&1/2
\end{pmatrix},\qquad
E=\begin{pmatrix}0&1&-1\\0&-1&1\\0&0&0\end{pmatrix}.
\]

For \(0<\epsilon<1/6\), both \(B_\pm=A\pm\epsilon E\) are positive
doubly stochastic Markov matrices. The true \(A\) is selfadjoint. We have
\(E\mathbf1=Ef=0\), so \(B_\pm\) agree exactly with \(A^*=A\) on
\(\operatorname{span}\{\mathbf1,f\}\), even when agreement means the
full function rather than a scalar reading.

Nevertheless

\[
\langle f,B_\pm A f\rangle_\pi
-\langle Af,Af\rangle_\pi
=\pm\frac{\epsilon}{18}\ne0.
\]

The actual suffix \(Af\) falls outside the calibrated domain. The
minus sign underestimates the propagated Gram entry and can therefore
underestimate a squared residual. This example shows why a zero defect
reported only on \(f\) cannot be used as a zero bias allowance for all
Gram queries. Three states are enough; no stochastic simulation is used.

## 6. A per-step forward-stationarity error is a different problem

Let \(\pi\) be uniform on two states and consider the intended forward
operator \(A_0=I\) versus the actually applied

\[
A_\epsilon=\begin{pmatrix}1-\epsilon&\epsilon\\0&1\end{pmatrix}.
\]

The single-step perturbation has \(L^2(\pi)\) operator norm
\(\sqrt2\epsilon\), and the one-step stationarity defect is
\(\|\pi A_\epsilon-\pi\|_{\rm TV}=\epsilon/2\).
For \(f=(-1,1)^\top\), however,

\[
\langle f,A_0^n f\rangle_\pi=1,\qquad
\langle f,A_\epsilon^n f\rangle_\pi=(1-\epsilon)^n.
\]

Their difference tends to one. Small per-step forward error or
stationarity drift alone therefore does not imply a uniformly small
all-horizon discrepancy. This does not contradict (6): the perturbed
target forward operator violates the common-\(\pi\) contraction warrant.

If approximate reverse operations are themselves to be used as future
target actions, they need their own forward-action contract. If the
scientific target is a nominal ideal forward system but every real target
action is an approximation, the implementation discrepancy must also be
charged; it is not confined to the finite acquisition pool.

## 7. Implementation qualifications and stopping point of this audit

- \(H_a\) is generally nonsymmetric. \(J_a^L\) and \(J_a^R\) must both
  be acquired or otherwise bounded.
- Pure reversal of a forward word is not a valid alias. Full adjoint
  reversal, replacing symbols by daggers as well as reversing order,
  preserves the ideal real endpoint correlation. Approximate physical
  queries for aliased ideal quantities have separately charged biases.
- The retained corrected predictor is still an ordinary weighted
  automaton, with blocks
  \(\left[\begin{smallmatrix}U_a^*&D_{a,c}\\0&T_a\end{smallmatrix}\right]\).
  An equally informed retaining baseline gets this construction.
- A finite calibration error does not logically force target-horizon
  growth. A **warranted** bound on the relevant finite calibration defects
  is essential. No accessible physical procedure establishing that bound
  was supplied or invented here. Its availability and total cost remain
  UNKNOWN.
