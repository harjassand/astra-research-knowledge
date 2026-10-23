# Independent challenge and constructive extension: entropy versus bath displacement

Authoring role: `/root/cycle11_entropy_drift_challenge`.
Date: 23 October 2026, Australia/Brisbane.

## Status and source boundary

**PASS for the principal's bulk entropy/drift theorem.** The extension below proves a stronger all-normal-initializer, actual-root version. It does not establish the proposed (O((bk)^2)) pressure bound. It does establish an all-block-length (O(b)) entropy-per-call ceiling under nonpositive displacement, enough to pair with Cycle10's operational lower bound and determine the order in that construction class.

Read source: the exact Cycle10 native extraction at `starting_source/Astra_Amplification_Cycle10_PRO1_20261023/`, specifically `QUADRATIC_CAPACITY_FLOOR.tex`, its governing device and displacement definitions, and the actual direct-history representation in `contributions/hamming_response/physical_hamming_check.py`. No old suite was replayed. The new direct-history diagnostic is separately named `physical_pressure_check.py`.

The mathematical statements here concern the actual device

\[
U=\begin{pmatrix}R&S_1&S_2\\S_1^*&0&0\\S_2^*&0&0\end{pmatrix},
\qquad V=\sqrt a U+i\sqrt b I,
\qquad a=1-b.
\]

(R^2=P_0), \(\sum_jS_jS_j^*=I-P_0\), \(S_j^*S_j=I\); the root is present. The one-call charge is (q=\operatorname{diag}(0,1,1)), and (Q=\sum_{i=1}^kq_i). The bounded displacement is (G=Q-W^*QW), with (\|G\|\le k). A positive value means outward bath displacement. Initial input and bath are a product; correlations within the input and within the bath are unrestricted.

## 1. A root-retaining tilted completely positive map

For \(\lambda\ge0\), define the normal CP map on bounded bath operators

\[
\Psi_\lambda(X)=\operatorname{Tr}_{\mathbb C^3}
[(e^{-\lambda q}\otimes I)V^*(e^{\lambda q}\otimes X)V].
\]

The expression is CP because the input weight can equivalently be split into two square roots before the partial trace. This is an analytic map; it is not a physical bath operation or a change to the forward channel.

A direct block calculation gives the exact whole-bath identity

\[
\Psi_\lambda(I)=F_\lambda(b)I-a(e^\lambda-1)P_0,
\qquad F_\lambda(b)=3b+a(e^\lambda+2e^{-\lambda}).                 \tag{1}
\]

Indeed the input-zero diagonal block of \(Ue^{\lambda q}U\) is

\[
P_0+e^\lambda(I-P_0),
\]

while each colored input diagonal block is (I). The interference term

\[
i\sqrt{ab}(Ue^{\lambda q}-e^{\lambda q}U)
\]

has zero input diagonal. Adding the (b e^{\lambda q}) contribution and weighting the two colored inputs by (e^{-\lambda}) proves (1). No commutation with an arbitrary bath operator is assumed.

Since \(\lambda\ge0\), (1) implies

\[
\Psi_\lambda(I)\le F_\lambda I,
\qquad \Psi_\lambda^k(I)\le F_\lambda^k I.                    \tag{2}
\]

The second statement follows by induction and positivity of the same CP map. It uses all (k) calls to the same evolving bath.

## 2. Log compression and the all-normal pressure bound

Let \(\tau\) be any normal bath density, with no finite-entropy or finite-depth-moment assumption. Purify it into \(|\psi_\tau\rangle\) with an auxiliary factor that the device does not touch. Define the isometry

\[
B:\mathbb C^{3^k}\longrightarrow \mathbb C^{3^k}\otimes E\otimes E',
\qquad Bv=(W\otimes I_{E'})(v\otimes|\psi_\tau\rangle).
\]

Let

\[
M=B^*Q_{\rm out}B,
\qquad D_\tau=Q-M=\operatorname{Tr}_E[(I\otimes\tau)G].
\]

In general \([M,Q]\ne0\): coherent initial bath depths can make this commutator nonzero. The proof below does not assume it vanishes.

Set \(T=e^{\lambda Q_{\rm out}}\), which is bounded and strictly positive. Operator concavity of logarithm under an isometric compression gives

\[
\lambda M=B^*(\log T)B\le\log(B^*TB).                       \tag{3}
\]

This is a legitimate operator Jensen statement for logarithm. It is **not** the generally false operator Jensen statement for exponential. One elementary justification uses the compression inverse inequality

\[
(B^*TB+sI)^{-1}\le B^*(T+sI)^{-1}B,
\]

followed by the integral representation of logarithm. All matrices on the compressed input are finite dimensional, and (T) has a positive lower bound.

Trace exponential is monotone for the Loewner order on finite Hermitian matrices, by eigenvalue monotonicity. Applying that fact to (3), then Golden–Thompson, yields

\[
\begin{split}
\operatorname{Tr}e^{-\lambda D_\tau}
&\le\operatorname{Tr}\exp[-\lambda Q+\log(B^*TB)]\\
&\le\operatorname{Tr}(e^{-\lambda Q}B^*TB).                 \tag{4}
\end{split}
\]

No claim that the exponential function itself is operator monotone is made.

The last trace in (4) is

\[
\operatorname{Tr}\tau\,
\operatorname{Tr}_{A^k}[e^{-\lambda Q}W^*e^{\lambda Q}W]
=\operatorname{Tr}\tau\,\Psi_\lambda^k(I).                 \tag{5}
\]

To see the order, trace the last qutrit first in the ordered interaction word. Its input and output weights produce one application of \(\Psi_\lambda\); iterate toward the first qutrit. The bath is not reinitialized between these maps. Combining (2), (4), and (5) gives

\[
\boxed{\operatorname{Tr}e^{-\lambda D_\tau}
\le[3b+a(e^\lambda+2e^{-\lambda})]^k},
\qquad\lambda\ge0.                                      \tag{6}
\]

This holds for every normal initializer and every finite (k), with the actual root retained.

## 3. Entropy/displacement tradeoff and full operator consequence

For any input density \(\rho\), positivity of relative entropy against

\[
e^{-\lambda D_\tau}/\operatorname{Tr}e^{-\lambda D_\tau}
\]

gives

\[
S_2(\rho)\le\frac\lambda{\ln2}\operatorname{Tr}(\rho D_\tau)
+\log_2\operatorname{Tr}e^{-\lambda D_\tau}.                 \tag{7}
\]

No charge-preservation assumption on \(\rho\) is needed. Choose
\(\lambda=(\ln2)/2\); then

\[
\boxed{S_2(\rho)\le k c(b)+\tfrac12
\operatorname{Tr}[(\rho\otimes\tau)G]},
\qquad
c(b)=\log_2[2\sqrt2(1-b)+3b].                              \tag{8}
\]

The choice minimizes the scalar envelope in (6) over nonnegative \(\lambda\) when the displacement is only known to be nonpositive. It is not an optimization of the actual quantum partition function.

Because (8) holds for every normal \(\tau\), it is equivalent to the bath-operator lower bound

\[
\boxed{D_b(\rho)=\operatorname{Tr}_{A^k}[(\rho\otimes I)G]
\ge2[S_2(\rho)-kc(b)]I_E.}                                \tag{9}
\]

All quantities in (9) are bounded; infinite mean depth causes no undefined subtraction.

Thus every density with nonpositive full bulk drift obeys

\[
\frac{S_2(\rho)}k\le c(b)
=\frac32+\log_2\left[1+
\left(\frac3{2\sqrt2}-1\right)b\right].                    \tag{10}
\]

In fact, one nonpositive expectation in any independently chosen bath state already suffices for (10). A full bulk operator condition is stronger. This upper is uniform over all block lengths, not only (bk\) bounded. Its small-(b) excess is

\[
\frac{3/(2\sqrt2)-1}{\ln2}\,b+O(b^2).
\]

Cycle10 supplies actual strictly inward-drift inputs and arbitrary-reference codes with a positive constant times (b\) excess. Consequently the optimal entropy-per-call excess in that admitted inward-drift construction class has order (\Theta(b)=\Theta(\beta^2)\). This does not prove a full channel-capacity upper or feedback result.

## 4. Independent check of the originally proposed prefix pressure

For a bath state supported at one depth (h\ge k), no path hits the vacuum before its last call. After purification, (M=B^*Q_{\rm out}B) commutes with total input charge. Set

\[
K=D_\tau-a(2Q-kI),\qquad
\sigma=\operatorname{diag}(1/2,1/4,1/4)^{\otimes k}.
\]

For every real (t), diagonalize (M) within each total-charge sector and apply scalar Jensen to each vector's spectral measure of (Q_{\rm out}\). This gives

\[
\operatorname{Tr}\sigma e^{-tK}
\le\left[a\cosh(tb)+b\cosh(ta)\right]^k.                   \tag{11}
\]

The exact trace on the right follows from the following physical identity. On an input computational charge pattern (x), every stay mask yields a distinct output charge pattern. Therefore its contribution to a diagonal function of output charge is orthogonal to every other mask. Its squared norm is the corresponding product of (a\) and (b\), independent of prefix colors or coherences. This identity is used only after retaining the coherent word; it is not a classical-noise replacement for the physical channel.

Equation (11) holds for every coherent or mixed analytic prefix, never physically prepared. It is a full exponential-moment bound. At fixed (t) and small (b\), however, its logarithm is

\[
bk(\cosh t-1)+O(kb^2),
\]

which is (O(bk)\), not (O((bk)^2)\) as (bk\downarrow0\). The stronger target pressure bound remains unproved and is not asserted here. The new all-(k\) order consequence (10) does not require it.

## 5. Challenges of the principal's further consequences

### Uniform escape for a charge-preserving repeated input

Suppose \([\rho,Q]=0\) and \(\delta=2[S_2(\rho)-kc(b)]>0\). Equation (9) gives (D_b(\rho)\ge\delta I\), and automatically (\delta\le k\). The inherited homogeneous-increment effects obey

\[
\Phi_\rho^*e^{-tL}
=\left(\sum_\Delta e^{-t\Delta}A_\Delta\right)e^{-tL}.
\]

Set (t=\delta/(2k^2)\), \(\lambda_-=1-\delta^2/(4k^2)\). For \(|\Delta|\le k\), the elementary Taylor bound at (kt\le1/2\) gives

\[
e^{-t\Delta}\le1-t\Delta+k^2t^2.
\]

Therefore \(\Phi_\rho^*e^{-tL}\le\lambda_-e^{-tL}\), globally including the root. For every normal initializer,

\[
\Pr(L_m\le H)\le e^{tH}\lambda_-^m.
\]

No finite initial mean is required, since (0\le e^{-tL}\le I\). This is an escape statement. It supplies neither an entropy-growth theorem nor a coherent-information or capacity converse by itself.

### Fixed-call code entropy and depth expenditure

For a deterministic unassisted (n\)-call encoder/decoder with logical dimension (K\), let the full-diamond error be \(\epsilon\le1\), and let \(\rho\) be its encoded maximally mixed input on the (n\) ports. The decoded Bell-output state has half trace distance at most \(\epsilon/2\) from a pure state. Hence

\[
S(RD)\le h_2(\epsilon/2)+\epsilon\log_2K.
\]

Araki–Lieb and (S(R)=\log_2K\) give

\[
I(R:D)\ge2[(1-\epsilon)\log_2K-h_2(\epsilon/2)].
\]

Data processing through the fixed bath channel and decoder yields
\(I(R:D)\le I(R:A^n)\le2S(\rho)\), including a general CPTP encoder. Therefore

\[
S(\rho)\ge(1-\epsilon)\log_2K-h_2(\epsilon/2).
\]

Combining with (9) proves the proposed displacement lower bound. At the actual \(\tau_\pi\), whose initial mean depth is (1/2\), finite propagation justifies ordinary mean-depth accounting. A rate above (c(b)\) has positive linear mean-depth expenditure as \(\epsilon\to0\). This statement assumes an ordinary fixed-(n\), initially product-bath unassisted code, and does not cover unspecified feedback or hidden side resources.

The inherited lower code still needs a separately documented final-depth estimate before identifying a matching depth-budget operation. Small recovery error alone is not a bath-depth estimate. For diagonal \(\tau_\pi\), the inherited cutoff overflow and finite propagation appear sufficient; the principal is checking that receiving use explicitly.

## 6. Necessary-premise counterexamples

### Initial input/bath independence cannot be dropped

Use one actual call, one vacuum seed, (0<\beta\le1/32\), and

\[
\alpha=\sqrt{1-\beta^2},\quad
\delta=\frac\beta{8\alpha},\quad g=\frac18.
\]

For each (j=1,2\), on the orthogonal pair

\[
|0\rangle|j\rangle_E,\qquad |j\rangle|\mathrm{vac}\rangle_E,
\]

put the joint-state block

\[
\begin{pmatrix}1/4-\delta/2&ig\\-ig&1/4+\delta/2\end{pmatrix}.
\]

The direct sum is positive and normalized. The input marginal has charge

\[
q=1/2+\delta,
\qquad S_2(\rho_A)=h_2(q)+q>3/2+\beta/16.
\]

The strict displayed bound follows, for example, from
\(1-h_2(1/2+\delta)\le4\delta^2\), valid in this small interval, and \(\delta<1/8\). On each edge pair the actual device is \(\alpha X+i\beta I\), and direct evaluation gives total outward drift

\[
2a\delta-4g\alpha\beta=-\alpha\beta/4<0.
\]

But \(c(b)-3/2<b/8<\beta/16\) in the same range. Thus (8) would be false if the product initialization premise were omitted. This is an actual-device correlated-initializer counterexample, not an abstract matrix. Such input/bath correlation is unavailable in the stipulated operation.

### The sign of the tilt matters at the root

At (b=0\), one call from vacuum has \(D_\tau=q\). For \(\lambda<0\),

\[
\operatorname{Tr}e^{-\lambda D_\tau}=1+2e^{-\lambda}
>e^\lambda+2e^{-\lambda}=F_\lambda(0).
\]

Thus the global root-retaining envelope (6) requires \(\lambda\ge0\). The bulk prefix result (11), derived separately, is valid for real (t\). The two scopes must not be conflated.

## 7. Evidence, primary comparison, and cost scope

The new diagnostic retained the root exchange and all amplitudes for (V=(6U+iI)/\sqrt{37}\). It checked (k=1,2,3\) for five initializers: bulk basis, coherent bulk colors/seeds, vacuum, coherent depths, and a normalized depth-(0,1,2\) truncation of actual \(\tau_\pi\). It checked isometry, log compression, pressure versus tilted trace, the root envelope, and the real-(t\) bulk pressure. All 15 cases passed. The necessary-independence counterexample was also checked on its actual four-dimensional edge subspace. A coherent-depth example has \(\|[M,Q]\|\simeq0.119906\), demonstrating that the strengthened logarithm proof addresses an actual noncommuting case.

Observed script-body time: approximately (0.023\) seconds. Peak RSS reported on Linux: (26{,}016\) KiB. These are replay diagnostics, not discovery or review costs. Total inference/discovery/review cost is unknown. No dense matrix remotely approaching the operational inner dimension was constructed.

Primary comparison read: Hansen and Pedersen, *Jensen's Operator Inequality*, arXiv:math/0204049, Theorem 2.1 (isometry compression) and Theorem 2.4 (trace Jensen); published Bull. London Math. Soc. **35** (2003), 553–564, DOI 10.1112/S0024609303002200. Full preprint accessed. Golden's original publisher abstract for *Lower Bounds for the Helmholtz Function*, Phys. Rev. **137** (1965), B1127, DOI 10.1103/PhysRev.137.B1127, was read; its full subscription article was not obtained. The standard finite-dimensional Golden–Thompson inequality is the second ingredient in (4).

These established matrix inequalities are not novel. The receiving mathematical use here is the exact tilted CP envelope of the actual root-retaining device and its conversion into a uniform entropy/displacement law. Historical originality of that complete device-specific statement has not been established. Internal challenge is not external certification, implementation efficiency, physical utility, or integration.

Source URLs: https://arxiv.org/pdf/math/0204049 and https://journals.aps.org/pr/abstract/10.1103/PhysRev.137.B1127 . Parent should open these directly before citing the web reference IDs.
