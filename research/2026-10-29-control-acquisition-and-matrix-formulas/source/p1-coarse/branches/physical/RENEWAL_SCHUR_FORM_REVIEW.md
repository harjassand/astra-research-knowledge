# Scoped proof: boundary renewal forms without a global source gap

28 October 2026. This note verifies the new renewal/Schur step and its
transfer to estimated boundary maps. It does not change the reviewed
multi-boundary experiment or re-audit the accepted dynamical energy theorem.
The ingredients are ordinary renewal probability, Schur complements and
spectral quadratic forms. The addition under development is their use in
an acquired all-program certificate with explicit observation costs.

## 1. Setting and claims

Let the live-state Hilbert space be

\[
\mathcal H=\mathbb R^r\oplus\ell^2(\Omega),\qquad
A=\begin{pmatrix}T&C^*\\C&B\end{pmatrix}.
\]

Here the finite first summand is the accessible boundary. A is symmetric,
entrywise nonnegative and substochastic. The hidden set Ω may be infinite.
The same argument applies to complex Hilbert notation, but the Markov
entries remain real. No assumption ||A||<1 or ||B||<1 is made.

Symmetry and substochasticity imply ||A||_2≤1. For finitely supported x,
Cauchy–Schwarz gives |(Ax)_j|²≤(Σ_k A_jk)(Σ_k A_jk|x_k|²), and summing
uses both row and column sums at most one. Density extends the inequality.
Thus A and its compression B are selfadjoint contractions.

Missing live-state probability enters a cemetery state. The source matrix
A is the killed live-state operator; the cemetery is not included in its
symmetric Hilbert-space matrix. The new interface distinguishes observed
irreversible absorption from a still-live outside state. The older single
outside symbol does not provide this information.

Put \(V=\binom{I}{0}\) and \(D=AV-VT=\binom{0}{C}\).
Define first-return matrices and two Schur sectors

\[
R=\sum_{n\ge0}C^*B^nC,\qquad
S=\sum_{n\ge0}(-1)^nC^*B^nC,
\]

\[
\Gamma_+=I-T-R,\qquad \Gamma_-=I+T-S.
\]

These finite matrices will be defined by absolutely convergent entries,
not by assuming globally bounded inverses of I−B or I+B.

Suppose a_j is the probability of absorption before the first positive-
time return to any boundary, starting at boundary j. Any sound lower
bounds \(\underline a_j\le a_j\) can replace a_j. Assume
κ_+=min_j \(\underline a_j\)>0. Then the stronger second-sector margin is

\[
\kappa_-=
\min_j\{2T_{jj}+\underline a_j\}>0.                  \tag{1}
\]

For acquisition, lower confidence endpoints for true T_jj must be used
in (1); replacing true diagonals by uncorrected proposals is not warranted.

The conclusions are the finite quadratic-form identities

\[
M=V^*(I-A^2)^{-1}V
=\tfrac12(\Gamma_+^{-1}+\Gamma_-^{-1}),              \tag{2}
\]

\[
Q=D^*(I-A^2)^{-1}D
=\tfrac12(R+S)
 +\tfrac12[R\Gamma_+^{-1}R+S\Gamma_-^{-1}S],          \tag{3}
\]

with inverse expressions on the left interpreted as spectral forms or
Abel limits. They are valid even when I−A² has no bounded inverse on H.
All products on the right have the displayed noncommuting order.

## 2. Renewal matrices exist even if hidden trajectories never terminate

For n≥0,

\[
F_{n+2}=C^*B^nC
\]

is the matrix of probabilities that the first step leaves the boundary,
the next n steps remain hidden, and the first return to the boundary is
at time n+2 with the specified endpoint. All entries are nonnegative.
T is the immediate, one-step boundary return matrix.

For each initial boundary j, the disjoint first-return events have total
probability at most one. Hence the entries of R converge absolutely. The
entries of S also converge absolutely, because the sum of the absolute
terms is the corresponding R entry. In finite boundary dimension this
implies operator-norm convergence of the finite matrices. In particular,

\[
R_{jk}\ge0,\qquad |S_{jk}|\le R_{jk},\qquad
T=T^*,\ R=R^*,\ S=S^*.                               \tag{4}
\]

Paths that never return and never absorb may have positive probability.
They do not invalidate the following inequality:

\[
\sum_k(T+R)_{jk}\le1-a_j\le1-\underline a_j.           \tag{5}
\]

Observed absorption by a finite cutoff is a subset of the event defining
a_j. Its lower probability bound is therefore sufficient. No assumption
that all trials eventually complete is needed.

For 0<z<1, norm-convergent Neumann series give

\[
R(z)=C^*(I-zB)^{-1}C,\qquad
S(z)=C^*(I+zB)^{-1}C.
\]

Both are positive semidefinite, because I±zB are positive definite.
Dominated convergence of their entries gives R(z)→R and S(z)→S.
Consequently R and S are positive semidefinite. This conclusion does not
assert that every individual F_n or every truncated tail is PSD.

## 3. Both sectors have observed lower bounds

For Γ_+=I−T−R, the off-diagonal entries are nonpositive. Its diagonal
dominance margin in row j is

\[
1-\sum_k(T+R)_{jk}\ge\underline a_j.
\]

Thus Γ_+≥diag(\(\underline a_j\))≥κ_+I.

For Γ_-=I+T−S, use (4) to bound the row-j Gershgorin margin:

\[
\begin{aligned}
1+T_{jj}-S_{jj}-\sum_{k\ne j}|T_{jk}-S_{jk}|
&\ge1+T_{jj}-R_{jj}-\sum_{k\ne j}(T_{jk}+R_{jk})\\
&=1+2T_{jj}-\sum_k(T+R)_{jk}\\
&\ge2T_{jj}+\underline a_j.
\end{aligned}                                       \tag{6}
\]

In fact this proves the matrix inequalities

\[
\Gamma_+\succeq H_+:=\operatorname{diag}(\underline a_j),\qquad
\Gamma_-\succeq H_-:=\operatorname{diag}(2T_{jj}+\underline a_j).
                                                               \tag{7}
\]

After subtracting the corresponding diagonal lower bound, each real
symmetric matrix is diagonally dominant with nonnegative diagonal, hence
PSD. In particular Γ_-≥κ_-I. This verifies the proposed sharper margin.
No commutation between T,R,S or either Schur sector is used.

The simpler common margin follows as well: |−T+S|≤T+R entrywise, so both
sectors have lower bound κ_+I. Equation (6) retains the useful diagonal
holding probability that this common-margin argument discards.

## 4. Abel regularization and the actual quadratic-form domains

For 0<z<1, I±zA and I±zB have bounded positive inverses. Define

\[
\Gamma_+(z)=I-zT-z^2R(z),\qquad
\Gamma_-(z)=I+zT-z^2S(z).
\]

Block inversion of I−zA gives upper-left block Γ_+(z)^{-1}. Its lower-right
block is

\[
(I-zB)^{-1}
+z^2(I-zB)^{-1}C\Gamma_+(z)^{-1}C^*(I-zB)^{-1}.
\]

For I+zA, replace I−zB by I+zB and Γ_+ by Γ_-. The lower-right correction
still has a plus sign: the two off-diagonal signs multiply. The exact
operator identity

\[
(I-z^2A^2)^{-1}
=\tfrac12[(I-zA)^{-1}+(I+zA)^{-1}]
\]

therefore implies

\[
M(z):=V^*(I-z^2A^2)^{-1}V
=\tfrac12[\Gamma_+(z)^{-1}+\Gamma_-(z)^{-1}],          \tag{8}
\]

\[
\begin{aligned}
Q(z)&:=D^*(I-z^2A^2)^{-1}D\\
&=\tfrac12[R(z)+S(z)]\\
&\quad+\tfrac{z^2}{2}
 [R(z)\Gamma_+(z)^{-1}R(z)
  +S(z)\Gamma_-(z)^{-1}S(z)].
\end{aligned}                                       \tag{9}
\]

All inverses and products in (8)–(9) are justified before taking a limit.
By §2 the finite matrices R(z),S(z) converge in norm. By §3 their limiting
Schur sectors are positive definite, so their inverses converge in norm.
The right sides have finite limits, exactly (2)–(3).

The spectral theorem identifies these limits. For x∈H,

\[
\langle x,(I-z^2A^2)^{-1}x\rangle
=\int_{[-1,1]}\frac{1}{1-z^2\lambda^2}\,d\mu_x(\lambda)
\uparrow\int_{[-1,1]}\frac{1}{1-\lambda^2}\,d\mu_x(\lambda).
                                                               \tag{10}
\]

An infinite value is allowed in (10) for a general hidden x. The finite
limits of (8)–(9), however, show that every column of V and D lies in the
domain of (I−A²)^{-1/2}, equivalently the actual range of
(I−A²)^{1/2}. Consequently the finite-dimensional maps

\[
K_V=(I-A^2)^{-1/2}V,\qquad K_D=(I-A^2)^{-1/2}D
\]

are bounded and satisfy K_V*K_V=M and K_D*K_D=Q. This establishes the
range premise needed by the dissipation theorem. It does not merely erase
an inaccessible component with a bare pseudoinverse.

The hidden operator may have norm one, continuous spectrum approaching
either endpoint, or unitary parts. The forms on the declared boundary and
defect columns are finite because of the finite Schur-sector bounds.
There is no assertion that (I−A²)^{-1} is bounded on all of H.

## 5. Local inverse bounds and estimated-map transfer

Inverse order in (7) yields

\[
M\preceq\tfrac12(H_+^{-1}+H_-^{-1})\preceq mI,
\qquad m=\tfrac12(\kappa_+^{-1}+\kappa_-^{-1}).         \tag{11}
\]

This is the local boundary inverse bound. It replaces the global factor
1/(1−a²) when transferring a certificate to an estimated boundary map.

Let \(\widehat T\) be an arbitrary computational proposal and
Δ=T−\(\widehat T\). Its source defect is

\[
\widehat D=AV-V\widehat T=D+V\Delta.
\]

The source factorization follows directly from §4:

\[
(I-A^2)^{-1/2}\widehat D=K_D+K_V\Delta.
\]

If Q≤qI and ||Δ||≤δ, (11) and the triangle inequality give

\[
\boxed{\
\widehat D^*(I-A^2)^{-1}\widehat D
\preceq(\sqrt q+\delta\sqrt m)^2I.
\ }                                                   \tag{12}
\]

The statement includes the required range property. A measured positive
definite computational budget W−\(\widehat T^*W\widehat T\), together
with an exact domination check for (12), can therefore feed the accepted
word-energy theorem. For nonselfadjoint proposals the primal and dual
computational maps must still satisfy that theorem's separate hypotheses;
source symmetry alone does not impose computational adjointness.

More directional bounds are possible. If Q≤θ_0²R_comp and
Δ*MΔ≤ε²R_comp, the same argument gives
\(\widehat Q\le(\theta_0+\epsilon)^2R_{comp}\).
For any t>0, matrix Young's inequality also gives

\[
\widehat Q\preceq(1+t)Q+(1+t^{-1})\Delta^*M\Delta.
\]

These formulas do not require Q,M,Δ or the computational budget to commute.

### Exact cross form, when useful

The same Schur blocks identify the noncommuting cross form N=K_V*K_D.
The inverse notation below is again a form pairing, not an assertion that
the unbounded inverse can be applied to D as an everywhere-defined operator:

\[
N:=V^*(I-A^2)^{-1}D
=\tfrac12[\Gamma_+^{-1}R-\Gamma_-^{-1}S].              \tag{13}
\]

The negative sign comes from the upper-right block of (I+A)^{-1}. Thus

\[
\widehat Q=Q+N^*\Delta+\Delta^*N+\Delta^*M\Delta.      \tag{14}
\]

N is generally not symmetric. Equation (14) can sharpen the triangle bound
when its uncertainty is certified; replacing its products by commuting
scalar expressions is invalid. At regularization z the right side of
(13) is z[Γ_+(z)^{-1}R(z)−Γ_-(z)^{-1}S(z)]/2.

### A scalar certificate from return and parity masses

Let r_* bound max_j Σ_k R_jk, and let e_* bound the row sums of
E=(R+S)/2. E is the matrix of first returns of even duration, after first
leaving the boundary. Both R and E are entrywise nonnegative and symmetric;
||R||≤r_* and ||E||≤e_*. Equation (4) implies ||S||≤r_*.
Therefore (3) gives the conservative but simple source bound

\[
Q\preceq\left[e_*+\tfrac12r_*^2
 (\kappa_+^{-1}+\kappa_-^{-1})\right]I
=(e_*+mr_*^2)I.                                     \tag{15}
\]

Taking e_*=r_* is also valid. Thus full numerical reconstruction of R and
S is not necessary for a sound operator bound, although their matrices can
give a sharper result. The finite acquisition and its confidence allocation
must still establish the row-mass bounds used in (15).

## 6. Finite censoring gives a norm tail bound, not automatic PSD order

Run a trial until the first positive-time boundary return, observed
absorption, or a fixed cutoff L. A trial that first returns at time one
contributes to T. First returns at times 2 through L contribute to

\[
R_L=\sum_{n=2}^L F_n,\qquad
S_L=\sum_{n=2}^L(-1)^{n-2}F_n.
\]

Let τ_j be the probability that the trial is still live and outside at L,
having had no intervening boundary return. Any later first return is a
subset of this censored event. Consequently, entrywise,

\[
R-R_L\ge0,\qquad |S-S_L|\le R-R_L,
\qquad\sum_k(R-R_L)_{jk}\le\tau_j.                    \tag{16}
\]

Both tails are symmetric. Thus for τ=max_j τ_j,

\[
\|R-R_L\|_2\le\tau,\qquad\|S-S_L\|_2\le\tau.          \tag{17}
\]

These bounds need no uniform hidden lifetime or global source gap. Sound
upper probability bounds for finite-cutoff censored outcomes can supply
τ. Observed finite-cutoff absorption supplies the lower bounds used in
§3. This argument requires an actual distinction between live outside
and absorbed states; the original outside-only receiver is insufficient.

Entrywise nonnegativity in (16) does not imply a PSD tail. For a finite
counterexample take

\[
T=\tfrac13I_2,\quad C=\tfrac1{10}I_2,\quad
B=\begin{pmatrix}0&1/2\\1/2&0\end{pmatrix}.
\]

The full block A is symmetric, entrywise nonnegative, and substochastic.
At cutoff L=2,

\[
R-R_2=\begin{pmatrix}1/300&1/150\\1/150&1/300\end{pmatrix},
\]

whose eigenvalues are 1/100 and −1/300. Therefore R≥R_L in Loewner order
cannot be inferred without an additional premise such as B≥0 or a
suitably chosen parity cutoff. The two-sided norm enclosure (17) remains
valid. Negative source eigenvalues do not invalidate the main Schur proof.

### Positive scalar acquisition for the conservative bound

The scalar row bounds in (15) can be obtained without signed near-canceling
means. For each initial boundary j, count the event “first left the
boundary, then returned by L, or remains live-censored at L.” Its
probability upper-bounds the row sum of R. Count “first left the boundary,
returned by L at an even duration, or remains live-censored at L” to
upper-bound the row sum of E=(R+S)/2. These are ordinary positive Bernoulli
events; no hidden state ID is needed.

The full R,S matrices remain available through the returned boundary ID
and parity, with censored-tail enclosures. S is a signed parity statistic,
but its nonzero outcomes are the rare excursion-return events themselves.
Its variance is therefore controlled by excursion-return probability;
it is not necessarily a subtraction of two probabilities near one.

This paragraph identifies a sufficient acquisition target, not a completed
statistical implementation. Confidence allocation, detector calibration,
preparation, stopping and complete execution costs belong to the new root
acquisition under construction.

## 7. Exact checks and scope of acceptance

`renewal_schur_checks.py` makes no stochastic acquisitions. It checks the
new identities on the two six-state noncommuting boundary fixtures and on
the four-state negative-hidden-eigenvalue counterexample. It verifies 39
exact rational identities: Q, M, the cross form, estimated-map transfer,
and their regularized versions at z=1/2,9/10,99/100. It also checks both
sector lower bounds, the stronger diagonal bounds, the local inverse
upper bound, (15), and finite-censor bounds at three cutoffs.

The two six-state examples have noncommuting R and Γ_+. The four-state
example attains the sharper negative-sector Gershgorin margin and verifies
the non-PSD tail explicitly. The companion `RENEWAL_SCHUR_CHECKS.json`
records these checks. They test the finite algebra; the ordinary proof
in §§2–4 supplies the infinite-dimensional and quadratic-form result.

Accepted at this scope: the renewal identities, both Schur-sector bounds,
finite source forms despite a possible global unit norm, local-M transfer,
and safe finite-censor norm tails. This note does not establish a new
physical readout, verify an infinite-source simulator, or certify the
root's forthcoming statistical acquisition code.

The ordinary first-return and Schur-complement algebra should be credited
as established machinery. A primary Markov-boundary antecedent is
C. D. Meyer, *Stochastic Complementation, Uncoupling Markov Chains, and the
Theory of Nearly Reducible Systems*, SIAM Review 31 (1989),
doi:10.1137/1031050. The proof here is self-contained and does not claim
that paper as an exact statement of this acquired program certificate.
The proposed addition is the finite observed-absorption/return acquisition
feeding the previously accepted all-word energy certificate, with the
new observation contract and full costs exposed.
