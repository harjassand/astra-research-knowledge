# Priority and operational scope

The mathematical claim established internally is a strict finite-covariance obstruction for one fixed scalar-convolution contract, together with an exact positive dependent construction. It is not a claim of historical priority or a new information advantage. External review remains outstanding.

## Primary-source comparators checked on 2026-10-15

- [Vasudevrao, Karthik, Reena, Sudha and Usha Devi, *Margenau–Hill operator valued measures and joint measurability*, arXiv:2111.13934v3; IJQI 20(07), 2250023 (2022)](https://arxiv.org/html/2111.13934v3). Section V.1, equations (17)–(20), explicitly derives the same sharp four-corner Pauli operator measure, then replaces its Bloch coefficients by an unsharpness parameter. That is direct antecedent for the kernel and its compatibility geometry. It does not impose a single additive scalar probability multiplier on the sharp characteristic operator, nor optimize the covariance of such a multiplier. The four-corner kernel itself is established mathematics.

- [Patra and Pan, *Margenau–Hill distribution as a Necessary and Sufficient Signature of Measurement Incompatibility*, arXiv:2609.37144v1](https://arxiv.org/html/2609.37144v1); [APS accepted-paper record](https://journals.aps.org/pra/accepted/10.1103/bkk8-16p1). The primary text's equations (1), (11), and (13) formulate unsharp dichotomic effects and their symmetrized products. This is a close contemporary comparator. Its claims are not premises of this proof. The inspected formula does not optimize additive scalar convolution of the fixed sharp kernel; its compatibility threshold cannot be inserted as an attaining scalar-noise construction.

- [Busch, Lahti and Werner, *Heisenberg uncertainty for qubit measurements*, arXiv:1311.0837v3; PRA 89, 012129 (2014)](https://arxiv.org/abs/1311.0837). This establishes substantial earlier theory of qubit measurement error tradeoffs. The error metric must be matched before comparing constants. The moment comparator below is derived directly rather than attributed to a theorem with a possibly different metric.

- [Ghosh, Roughgarden and Sundararajan, *Universally Utility-Maximizing Privacy Mechanisms*, arXiv:0811.2841; SIAM J. Comput. 41(6), 1673–1693 (2012)](https://arxiv.org/abs/0811.2841), [published primary record](https://epubs.siam.org/doi/abs/10.1137/09076828X). The independent-noise likelihood-ratio constraint is mathematically a discrete additive privacy constraint. Double-geometric mechanisms and their utility optimality have a substantial earlier literature. Section 6 of `PROOF.md` gives the exact inequality needed here from a short direct dual proof. That independent comparator should not be promoted as a new discovery without a much more specific historical claim.

- [Pomatto, Strack and Tamuz, *Stochastic Dominance Under Independent Noise*, author-hosted manuscript](https://www.tamuz.caltech.edu/papers/fosd.pdf). Appendix A, Lemma 1, reproduces a scalar signed-measure convolution-positivity theorem credited to Ruzsa–Székely and Mattner. This establishes antecedents for positive smoothing with ordinary moments. It does not by itself give the present matrix positivity cone or its variance optimum. Existence of some regularizer is not the new claim here.

The search was selective, not an exhaustive review of operator convolution, quasi-probability smoothing, optimal privacy mechanisms, or positive-multiplier theory. No inspected primary source settled whether the particular global constant, lattice-optimizer reduction, or the full dependent extremal problem already appears elsewhere. Exact priority is **UNKNOWN**. Independent derivation is not evidence of historical novelty.

## Ordinary joint-measurement comparator, derived in the same moment metric

In unit scales, let an unbiased POVM have first moments \(\sigma_z,\sigma_x\), scalar second-moment excesses \(V_1,V_2\), and scalar mixed moment \(C I\). Positivity of its moment Gram matrix, followed by a Schur complement, gives

\[
\begin{pmatrix}
V_1I & C I-i\sigma_y\\
C I+i\sigma_y & V_2I
\end{pmatrix}\succeq0,
\qquad V_1V_2\ge C^2+1.
\]

Thus total excess variance is at least \(2\). It is attained by the four-outcome POVM

\[
G_{\epsilon\eta}=\tfrac14
 (I+\epsilon\sigma_z/\sqrt2+\eta\sigma_x/\sqrt2),
\]

with reported outcomes \((\sqrt2\epsilon,\sqrt2\eta)\). Its first moments are the desired Pauli matrices, both second moments are \(2I\), and the mixed moment is zero. This construction is compatible with established unsharp-qubit measurement theory.

The theorem in `PROOF.md` shows that no scalar additive regularization of the fixed sharp Margenau–Hill kernel can attain this noise cost: every such law has total excess at least \(2.662175\ldots\). The difference comes from the stronger representation contract.

## Measurement information and implementation

The positive construction has a mathematical POVM, not a demonstrated physical apparatus. Its finite covariance means its reported coordinates are unbiased estimators of the two Pauli expectations. At the maximally mixed state, each coordinate's one-copy variance is

\[
1+U_0/2=2.601421071574\ldots.
\]

The independent scalar-convolution optimum has coordinate variance \(3\). Dependence therefore improves these particular estimators within the scalar-convolution class. The ordinary unbiased four-outcome comparator above has coordinate variance \(2\), which is better. No general Fisher-information, tomography, discrimination, sample-complexity, or computational advantage over optimal measurements has been proved.

The explicit POVM is centrally symmetric. Write its pair of opposite outcome effects as

\[
E_y=p_y(I+r_y\cdot\sigma),\qquad
E_{-y}=p_y(I-r_y\cdot\sigma),\qquad |r_y|\le1.
\]

One ideal mathematical realization chooses the unordered pair with probability \(2p_y\), performs the binary unsharp spin measurement with Bloch vector \(r_y\), and reports the selected sign. That binary measurement is a projective spin measurement along \(r_y/|r_y|\) followed by classical bit flipping, with the zero-vector case implemented by a fair bit. Thus the construction does not supply a new quantum primitive beyond ordinary qubit measurements and classical randomization.

The scalar trace distribution is exactly the convolution of the supplied noise with four uniform corners. It can be sampled by a finite rational mixture over the 4-by-4 absolute-index core, followed by independent geometric extensions when an index equals 3, and uniform signs. This observation supplies a concrete classical route to selecting measurement labels. It does not make the signed corner operators in the original kernel physical effects.

The support is countably infinite. Exact sampling has finite expected tail length, but no bounded worst-case number of random bits or output bits. An exact realization also calls for an infinite family of ideal measurement axes. Finite implementations need separately specified tail truncation, rotation precision, and output-error tolerances. The present proof does not provide experimental calibration, fabrication, energy, reset, or wall-clock costs.

## Supplied versus acquired inputs and cost boundary

The theorem assumes supplied Pauli directions, supplied scale factors \(a,b\), a known state-independent apparatus model, and exact access to the chosen POVM. It does not acquire an unknown Hamiltonian, unknown measurement directions, an unknown state, or an unknown noise law. The mathematical covariance is not an acquisition or calibration cost.

A practical comparison must charge copies, direction calibration, random-label generation, angle precision, recording of unbounded outcomes, truncation bias, classical estimation, energy, reset, and the cost of the matched competing apparatus. The explicit construction loses in the simple unbiased-coordinate variance comparison with the ordinary four-outcome POVM. It can be useful as a representation-theoretic separation without being an improved measurement technology.

## Exact exponential-domain boundary for this finite kernel

This observation uses only the four atoms, not any inherited analytic moment-transfer theorem. If the scalar noise has a finite moment generating function at \(g=(s,t)\), direct integration of the four shifts gives

\[
\int e^{sx+ty}M(dx\,dy)
=m_\nu(s,t)\cosh s\cosh t
 [I+\tanh s\,\sigma_z+\tanh t\,\sigma_x].
\]

A normalized positive POVM integrates a strictly positive scalar function to a positive definite matrix. Therefore every point of the noise's finite moment domain must satisfy

\[
\boxed{\tanh^2 s+\tanh^2 t<1.}
\]

The constructed rational geometric tails have a rectangle of finite exponential moments strictly inside this region. All polynomial moments are compatible with this boundary; all exponential moments are impossible. No tail-domain assumption was used to derive the strict variance lower bound.
