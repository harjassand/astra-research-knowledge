# Independent audit: volume-uniform symmetric imaginary-time product formula

Date: 2026-10-29 UTC. Auditor: `test_thermal_counting_bridge/audit_uniform_trotter`.

## Verdict

**PASS.** The proposed elementary argument establishes a volume-uniform
second-order log-partition-density approximation for arbitrary bounded-degree,
bounded-strength, finite-spin, (k)-local Hamiltonians. It needs neither a
stoquasticity assumption nor a geometric decomposition nor a high-temperature
restriction on the target inverse temperature. The number of time slices can
depend on inverse temperature and target density error, but not on volume.

This receipt audits the physics approximation only. It makes **no assessment of
the counting-complexity reduction**, arithmetic precision, weight compilation,
or the supplied exact-counting algorithm. It makes **no novelty claim** and does
not claim the argument is a new theorem in the literature.

## Assumptions and definitions

Let (H=\sum_{a=1}^{m}h_a) on (n) sites. Each (h_a) is Hermitian,
has nonempty support of size at most (k\ge1), and has spectral norm at most
(J\ge0). Every site belongs to at most (D\ge1) term supports. Thus
(m\le Dn). Empty-support scalar terms can be removed and handled exactly.
The cases (m=0) or (J=0) are exact and need no bound.

The term-overlap graph has maximum degree at most (k(D-1)). A proper coloring
uses (q\le k(D-1)+1) colors. Write (H=\sum_{j=1}^{q}H_j), with each
(H_j) a sum of pairwise disjoint-support terms. Set

\[
 E_j(t)=e^{-tH_j/2},\quad Q(t)=E_q(t)\cdots E_1(t),\quad
 P(t)=Q(t)^\dagger Q(t),\quad M=\sum_{\ell=1}^{q}k^\ell.
\]

For β≥0, integer (r\ge1), δ=β/r, and (x=JM\delta), the accepted
bound is

\[
\boxed{
 \frac1n\left|\log\operatorname{Tr}e^{-\beta H}
 -\log\operatorname{Tr}P(\beta/r)^r\right|
 \le \frac{2Dr}{M}(\sinh x-x)
 \le \frac{DJ^3M^2e^x\beta^3}{3r^2}.
}
\]

In particular, taking (r\ge JM\beta) replaces (e^x) by (e).
For any fixed β and density error ε>0, an integer

\[
 r\ge\max\left\{JM\beta,
 \sqrt{eDJ^3M^2\beta^3/(3\epsilon)}\right\}
\]

is sufficient. This bound is loose in its local constants but independent of n.
For free-energy density, divide the log-partition-density error by β when
β>0.

## Checks of the decisive steps

### 1. Local conjugation has a volume-independent power-series majorant

Consider (F(t)=U(t)h_aU(t)^{-1}), where (U) is a prefix/suffix product
of at most (q) colored layer exponentials in the order relevant below.
During one layer, only gates whose supports intersect the current support cone
need be retained. Since the gates in a layer are disjoint, at most (s) gates
are active on a cone of size (s); the next cone has size at most (ks).
Starting from size at most (k), at most

\[
k+k^2+\cdots+k^q=M
\]

local gates are retained. All removed gates commute with the operator at the
point at which they are removed. The cone is an upper bound fixed from supports,
so the same removal is valid at every real or complex t and for both signs of t.

Each retained conjugation is

\[
 e^{-t\operatorname{ad}_{h_b}/2},\qquad
 \|\operatorname{ad}_{h_b}/2\|\le\|h_b\|\le J,
\]

as a linear map in the spectral operator norm. Multiplying its absolutely
convergent power series shows

\[
\|[t^p]F(t)\|\le J\frac{(JM)^p}{p!}.
\]

This coefficient estimate does not use an extensive norm ‖H‖.

Every factor in (U(t)) is a Hermitian exponential, and the ordered product
satisfies (U(-t)=U(t)^{-\dagger}). Therefore, for real t,

\[
 F(t)^\dagger=F(-t),\qquad
 \operatorname{Herm}F(t)=\tfrac12(F(t)+F(-t)).
\]

Odd Taylor coefficients are anti-Hermitian; even coefficients are Hermitian.
Consequently

\[
\|\operatorname{Herm}F(t)-h_a\|
\le J\big(\cosh(JMt)-1\big),\qquad t\ge0.
\]

### 2. Relative propagator cancels full-H imaginary-time evolution

Define (R(t)=Q(t)e^{tH/2}). Exact differentiation gives

\[
 R'(t)=G(t)R(t),\qquad
 G(t)=Q'(t)Q(t)^{-1}+\tfrac12Q(t)HQ(t)^{-1}.
\]

Let (U_{>j}(t)=E_q(t)\cdots E_{j+1}(t)), with the empty product equal
to I. Since (E_j' E_j^{-1}=-H_j/2),

\[
 G(t)=\frac12\sum_{j=1}^q\sum_{a\in j}
 \left(\operatorname{Ad}_{Q(t)}h_a
       -\operatorname{Ad}_{U_{>j}(t)}h_a\right).
\]

The local (h_a) terms cancel when Hermitian parts are taken and the bound from
step 1 is applied. Hence

\[
 \|\operatorname{Herm}G(t)\|
 \le mJ\big(\cosh(JMt)-1\big).
\]

This is the key point: no full-H imaginary-time conjugation is estimated. All
conjugations to be bounded have constant layer depth.

### 3. Two-sided relative Loewner bound, not an additive global norm bound

For each vector v, exact differentiation gives

\[
 \frac{d}{dt}\|R(t)v\|^2
 =2\langle R(t)v,\operatorname{Herm}G(t)R(t)v\rangle.
\]

Scalar Grönwall in both directions, using R(0)=I, yields

\[
 e^{-2b}I\preceq R(\delta)^\dagger R(\delta)\preceq e^{2b}I,
 \qquad b=\frac mM(\sinh x-x).
\]

Since (R^\dagger R=e^{\delta H/2}P(\delta)e^{\delta H/2}), congruence by
(e^{-\delta H/2}) gives

\[
e^{-2b}e^{-\delta H}\preceq P(\delta)
\preceq e^{2b}e^{-\delta H}.
\]

### 4. Operator-monotone logarithm avoids an invalid power step

Logarithm is operator monotone on positive definite matrices. Applying it to
the preceding sandwich is valid, and scalar prefactors commute with everything:

\[
-2bI-\delta H\preceq\log P(\delta)
\preceq2bI-\delta H.
\]

Thus ‖log P(δ)+δH‖≤2b. The proof does **not** claim that raising the
Loewner sandwich to the r-th power preserves Loewner order; that generally
invalid inference is unnecessary.

### 5. Log partition is spectral-norm Lipschitz

For Hermitian A,B, the min-max principle gives

\[
 |\log\operatorname{Tr}e^A-\log\operatorname{Tr}e^B|
 \le\|A-B\|.
\]

This follows by comparing their ordered eigenvalues; it does not require the
matrix exponential to be operator monotone. Apply it with
(A=r\log P(\beta/r)) and (B=-\beta H), then use m≤Dn. Finally,
(\sinh x-x\le x^3e^x/6) for x≥0 gives the displayed simplified bound.

## Lower-order fallback also passed

Discarding Hermitian-part cancellation gives

\[
\|G(t)\|\le mJ(e^{JMt}-1)
\]

and the weaker but sufficient guarantee

\[
\frac1n|\log Z-\log Z_r|
\le\frac{2Dr}{M}(e^x-1-x)
\le DJ^2M e^x\frac{\beta^2}{r}.
\]

Both arguments have been checked algebraically. Numerical examples can be
helpful regression tests but are not needed for this proof and cannot establish
the volume-uniform result by themselves.

## Scope boundaries

- Local dimension may be any finite value for the analytic bound; an algorithmic
  statement additionally needs a fixed/local representation bound.
- Local strengths J must be bounded independently of volume for constant r.
- Degree means term-support incidence, not an unstated graph-degree surrogate.
- Positivity of P comes from (Q^\dagger Q); individual matrix entries may have
  signs or complex phases.
- No thermodynamic-limit existence or differentiability is assumed.
- A global O(n) log-partition error is appropriate for density approximation;
  it is not a constant multiplicative approximation of the partition function.
- This receipt does not settle whether constant-precision local weights are
  sufficient for the proposed signed-counting reduction.
