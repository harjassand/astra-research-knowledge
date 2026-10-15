# Information limits of exact scalar quantum regularization

The exact all-linear-marginal contract does not create new state information. For a scalable family of anticommuting observables, every radial positive regularizer is a classical randomization of a spherical projective measurement with an explicit circuit. Its statistical performance is never better for any decision problem. The source's smooth positive-definite regularizers are strictly worse locally, and increasing their smoothing scale makes information per copy tend to zero.

More decisively, even nonradial regularizers cannot distinguish a pair of orthogonal two-qubit states with opposite response to the same control. This is an actual response task that ordinary static coordinate estimates cannot solve; the exact positive representation cannot solve it either. A single additional Pauli measurement does solve it.

These are internal mathematical derivations with exact finite algebra checks. The general spin-factor Fisher-information bound has recent primary prior art, identified below. No new operational quantum advantage is established. The large-scale asymptotic is conditional on the source's uniform relative-error estimate; the other limitations do not depend on its existence proof.

## Contract and notation

Let \(A_1,\ldots,A_m\) be bounded Hermitian operators and let \(p\) be a scalar probability law. Suppose a normalized positive operator-valued measure \(M\) satisfies

\[
\widehat M(t)=\widehat p(t)e^{iA(t)},\qquad
A(t)=\sum_jt_jA_j.                                      \tag{1}
\]

The Fourier convention is \(\widehat M(t)=\int e^{it\cdot x}M(dx)\). The source for this contract is the supplied *sources/regularization_pasted.txt*. Positivity and (1) are assumptions here; the universal existence theorem is not re-audited in this result.

For the constructive comparison, fix \(m\ge2\), a finite-dimensional representation of Hermitian Clifford generators

\[
\Gamma_i\Gamma_j+\Gamma_j\Gamma_i=2\delta_{ij}I,
\qquad A_j=a\Gamma_j,\qquad a>0.                         \tag{2}
\]

Write \(d=\dim\mathcal H\), \(\Gamma(u)=\sum_ju_j\Gamma_j\), and

\[
r_j(\rho)=\operatorname{Tr}(\rho\Gamma_j),\qquad |r|\le1.
\]

The symbol \(a\) is the physical observable scale; \(s=|x|\) below is a measurement radius. This avoids using the same symbol for both.

## 1 Exact identifiability cannot expand under scalar convolution

**Proposition 1.** For any two trace-class states \(\rho,\sigma\),

\[
\operatorname{Tr}(\rho M(\cdot))=
\operatorname{Tr}(\sigma M(\cdot))
\quad\Longleftrightarrow\quad
\operatorname{Tr}[(\rho-\sigma)e^{iA(t)}]=0
\quad\text{for all }t\in\mathbb R^m.                    \tag{3}
\]

This holds on an arbitrary Hilbert space for bounded \(A_j\). It requires no exponential moments of \(p\).

**Proof.** A probability characteristic function is continuous and equals one at zero, so \(\widehat p\ne0\) on some neighborhood of zero. Equality of the two outcome laws and (1) imply that

\[
f(t)=\operatorname{Tr}[(\rho-\sigma)e^{iA(t)}]
\]

vanishes there. For each fixed real \(t\), \(z\mapsto f(zt)\) is entire because \(A(t)\) is bounded and \(\rho-\sigma\) is trace class. It vanishes on a real interval around zero, hence vanishes at \(z=1\). The converse follows from (1) and uniqueness of characteristic functions. \(\square\)

In finite dimension, define the accessible real operator space

\[
\mathcal S_A=\operatorname{span}_{\mathbb R}
\{I,\operatorname{Re}e^{iA(t)},\operatorname{Im}e^{iA(t)}:
t\in\mathbb R^m\}.
\]

Equivalently it is the span of \(A(t)^k\), or of the corresponding fully symmetrized words. A linear quantity \(\operatorname{Tr}(\rho B)\) is identifiable from arbitrarily many exact \(M\) samples, uniformly over all states, precisely when \(B\in\mathcal S_A\). If \(B\notin\mathcal S_A\), choose a traceless Hermitian \(D\in\mathcal S_A^\perp\) with \(\operatorname{Tr}(DB)\ne0\); sufficiently small perturbations \(I/d\pm\epsilon D\) witness failure. A nonlinear target is identifiable only if it is constant on the same state fibers.

Zeros of \(\widehat p\) can make direct inversion unstable without enlarging these fibers. Exact uniqueness says nothing about finite-sample conditioning. In generic tuples, \(\mathcal S_A\) can be much larger than the span of \(I,A_1,\ldots,A_m\); Proposition 1 is not a claim that coordinate expectations always suffice.

## 2 All Clifford regularizers see only one spin vector

The Clifford relation gives

\[
e^{ia\Gamma(t)}=
\cos(a|t|)I+i\sin(a|t|)\Gamma(t/|t|).                  \tag{4}
\]

Consequently

\[
\mathcal S_A=\operatorname{span}_{\mathbb R}
\{I,\Gamma_1,\ldots,\Gamma_m\}.                       \tag{5}
\]

Fourier uniqueness applied to every matrix coefficient orthogonal to this space shows that every effect of \(M\) lies in (5). Let

\[
\nu(dx)=d^{-1}\operatorname{Tr}M(dx).
\]

There is a measurable \(b:\mathbb R^m\to\mathbb R^m\) such that

\[
M(dx)=\nu(dx)[I+\Gamma(b(x))],\quad |b(x)|\le1,
\quad \int b\,d\nu=0.                                  \tag{6}
\]

Indeed all coefficient measures are absolutely continuous with respect to the positive trace measure, and the two eigenvalues of \(I+\Gamma(b)\) are \(1\pm|b|\). The exact statistical model is therefore

\[
P_r(dx)=\nu(dx)[1+r\cdot b(x)].                         \tag{7}
\]

This conclusion holds for **every scalar noise law**, with no radial hypothesis. The ambient Hilbert-space dimension adds no visible state parameters to (7).

For a known scalar function \(f\) and a unit vector \(u\),

\[
f(a\Gamma(u))=
\frac{f(a)+f(-a)}2I+
\frac{f(a)-f(-a)}2\Gamma(u).                            \tag{8}
\]

All expectations of nonlinear functions of a single linear combination reduce to ordinary spin-vector estimates. This includes its entire spectral law, characteristic function, and spectral tail probabilities. State nonlinearities, ordered products, commutators, and intervention responses are different targets; the next example separates them.

## 3 An invisible bit with an opposite measurable response

Take \(m=4\), \(d=4\), and

\[
\Gamma_1=X\otimes I,\quad\Gamma_2=Y\otimes I,\quad
\Gamma_3=Z\otimes X,\quad\Gamma_4=Z\otimes Y.
\]

Put

\[
Q=i\Gamma_1\Gamma_2=-Z\otimes I,
\qquad \rho_\pm=\frac{I\pm Q}{4}.                     \tag{9}
\]

These are normalized positive states with orthogonal supports. Both have \(r=0\). Thus **every POVM satisfying (1), for any scalar noise, has exactly the same output law on them**. No number of repeated uses, nonlinear decoder, rare-event estimator, or adaptive classical postprocessing can distinguish them. Equal-prior decision error stays \(1/2\).

Now apply the same known control to either state:

\[
U_\theta=e^{-i\theta\Gamma_2/2}.
\]

The Pauli algebra gives

\[
U_\theta^\dagger\Gamma_1U_\theta
=\cos\theta\,\Gamma_1-\sin\theta\,Q,
\qquad
\operatorname{Tr}(U_\theta\rho_\pm U_\theta^\dagger\Gamma_1)
=\mp\sin\theta.                                       \tag{10}
\]

Their response derivatives at zero are \(-1\) and \(+1\). Measuring \(Q=-Z\otimes I\) distinguishes them perfectly in one copy; measuring the response after \(\theta=\pi/2\) does so as well. The regularized static record cannot predict this response, despite containing all noisy linear-combination spectral distributions.

The example extends to every \(m\ge4\): \(Q=i\Gamma_1\Gamma_2\) is trace-orthogonal to \(I,\Gamma_1,\ldots,\Gamma_m\), and \(\rho_\pm=(I\pm Q)/d\) have the same properties. Moreover \(I/d\) and \((I+Q)/d\) are indistinguishable by \(M\), although their purities are \(1/d\) and \(2/d\), and their entropies differ by one bit. The family \((I+\theta Q)/d\) is invisible for every \(|\theta|\le1\), so this is not confined to boundary states.

Controls before measurement change the accessible operator space and can remove this obstruction, but the acquired control and the new measurement records are then part of the task. The static scalar-convolution identity does not supply them. Collective measurements on several copies are likewise a different resource.

## 4 Radial regularization is dominated by a spherical projective measurement

Suppose now that \(p\) is radial. Orthogonal covariance of the scalar and vector coefficients in (4) implies that (6) has the polar form

\[
M(ds,dn)=q(ds)\,\sigma_m(dn)
\big[I+\eta(s)\Gamma(n)\big],\qquad |\eta(s)|\le1,       \tag{11}
\]

where \(\sigma_m\) is uniform probability on \(S^{m-1}\), and \(q\) is a probability law independent of the state. An atom at \(s=0\) is an uninformative outcome, represented by \(\eta(0)=0\). This decomposition also covers radial laws without smooth densities.

Define

\[
N(dn)=[I+\Gamma(n)]\sigma_m(dn).                        \tag{12}
\]

To implement \(N\), choose an independent uniform axis \(v\in S^{m-1}\), projectively measure \(\Gamma(v)\), obtain \(z\in\{-1,+1\}\), and report \(n=zv\). The effect density of the reported \(n\) is exactly (12).

**Theorem 2.** \(N\) Blackwell-dominates every radial \(M\) satisfying (1).

**Proof by an explicit state-independent simulator.** From an \(N\) outcome \(n\), draw \(s\sim q\) independently and a sign \(e\) with

\[
\Pr(e=+1\mid s)=\frac{1+\eta(s)}2.
\]

Report \(x=sen\), with \(x=0\) at zero radius. The density at direction \(n'\) is

\[
\tfrac{1+\eta(s)}2[I+\Gamma(n')]
+\tfrac{1-\eta(s)}2[I-\Gamma(n')]
=I+\eta(s)\Gamma(n'),
\]

which is (11). \(\square\)

This compares entire statistical experiments. It applies to every loss function, every prior on arbitrary input states, every number of independently prepared copies, and every classical estimator or decision rule. It includes nonlinear state targets whenever those are identifiable. Data processing gives the associated testing and information inequalities.

The two experiments are statistically equivalent **if and only if** \(|\eta(s)|=1\) for \(q\)-almost every \(s\). Sufficiency follows by recovering \(n=\eta(|x|)x/|x|\). Necessity follows from the Fisher-information calculation below. The exact qubit construction in the supplied source is one instance of the equivalence case. For a smooth positive-definite density, \(|\eta(s)|<1\) at every finite radius, and the comparison is strict.

The simulator is an exact statistical statement. An efficient sampler for arbitrary \(q\) is not inferred. For the scientific tasks in (8), the comparator has a direct efficient estimator and needs neither \(q\) nor its inversion.

## 5 Quantitative cost that no nonlinear decoder removes

Consider the legitimate local family

\[
\rho_r=(I+\Gamma(r))/d,\qquad |r|<1.
\]

At \(r=0\), the score of (7) is \(b(x)\). Its classical Fisher information is

\[
F_M(0)=\int bb^T\,d\nu,\qquad
\operatorname{tr}F_M(0)\le1.                            \tag{13}
\]

For (11), write

\[
\zeta=\mathbb E_q\eta(s)^2.
\]

The exact contract with \(a>0\) forces \(\zeta>0\): otherwise every effect would be scalar, contradicting (4) near zero.

Then

\[
F_M(0)=\frac{\zeta}{m}I_m,
\qquad F_N(0)=\frac1mI_m.                               \tag{14}
\]

Any locally unbiased \(n\)-copy estimator of \(r\), using independent copies measured by \(M\), has covariance at least

\[
\frac{m}{n\zeta}I_m.                                    \tag{15}
\]

The spherical report \(\widehat r=mn\) is unbiased and has covariance \(mI_m-rr^T\), attaining the center benchmark for one copy. Physical means \(a r_j\) have an additional factor \(a^2\) in these covariance expressions.

The testing statement does not assume an unbiased estimator. For known unit \(u\), compare \(\rho_0=I/d\) and \(\rho_{hu}=(I+h\Gamma(u))/d\), \(0<|h|\le1\). Their one-copy chi-squared divergence is exactly

\[
\chi^2(P_{hu}\Vert P_0)=\frac{h^2\zeta}{m}.             \tag{16}
\]

For \(n\) independent copies it is \((1+h^2\zeta/m)^n-1\). Equal-prior decision error at most \(1/3\) requires total variation at least \(1/3\), and \(\operatorname{TV}\le\frac12\sqrt{\chi^2}\) gives

\[
n\ge\frac{\log(13/9)}{\log(1+h^2\zeta/m)}
\ge\frac{m\log(13/9)}{h^2\zeta}.                       \tag{17}
\]

A projective measurement of the known \(\Gamma(u)\) distinguishes these states with \(O(h^{-2})\) preparations. Universality costs order \(m/\zeta\) in this specific known-direction task; the exact representation does not evade that cost.

For another exact comparison, the total variation between the \(M\) laws of \(\rho_{hu}\) and \(\rho_{-hu}\) is

\[
|h|\mathbb E_q|\eta(s)|
\frac{\Gamma(m/2)}{\sqrt\pi\,\Gamma((m+1)/2)}.           \tag{18}
\]

The spherical measurement has the same expression with \(\mathbb E|\eta|=1\); the tailored projective measurement has variation \(|h|\).

### Raw noise variance and the strict endpoint

Assume the radial scalar noise has covariance \(vI_m\). The exact first and second moments imply

\[
\mathbb E_q[s\eta(s)]=ma,\qquad
\mathbb E_qs^2=m(a^2+v).
\]

Cauchy–Schwarz yields

\[
a^2+v\ge\frac{ma^2}{\zeta}\ge ma^2.                   \tag{19}
\]

The familiar \(v\ge(m-1)a^2\) lower bound also follows from the information contraction. If the exact radial contract has finite third moments and \(m>1\), equality in that variance bound is impossible. Equality would force \(s=ma\), \(\eta=1\) almost surely, i.e. the fixed-radius report \(X=ma n\). Its third directional operator moment is

\[
\int (u\cdot x)^3M(dx)=\frac{3m^2a^3}{m+2}\Gamma(u).
\]

The scalar-convolution identity instead requires

\[
[a^3+3av]\Gamma(u)=(3m-2)a^3\Gamma(u).
\]

The coefficients differ by \(-4(m-1)a^3/(m+2)\). Hence

\[
v>(m-1)a^2\quad(m>1).                                  \tag{20}
\]

This strict inequality does **not** establish a uniform positive gap above the endpoint or solve the optimal-noise problem.

## 6 The smooth universal family loses information at large scale

This subsection takes the supplied uniform relative-error estimate as a premise. For fixed \(m,a,c\), \(0<c<1/(2a)\), let

\[
V_L(x)=cL f(|x|/L),\quad
f(s)=\sqrt{1+s^2}\log\sqrt{1+s^2},\quad
p_L\propto e^{-V_L}.
\]

Equation (7) in the supplied source bounds the relative operator error by \(C/L\) uniformly in \(x\), with \(C\) fixed once \(m,a,c\) and the cutoff are fixed. On Clifford generators both sides of the radial density commute with \(\Gamma(n)\). Let \(g_L(s)=V_L'(s)\ge0\). Its two scalar eigenvalue densities obey

\[
\lambda_\pm(s)=p_L(s)e^{\pm a g_L(s)}[1+\delta_\pm(s)],
\qquad |\delta_\pm|\le C/L.
\]

For large \(L\), write

\[
\eta_L(s)=\tanh[a g_L(s)+\epsilon_L(s)],
\qquad
\epsilon_L=\tfrac12\log\frac{1+\delta_+}{1+\delta_-},
\quad |\epsilon_L|=O(L^{-1})                            \tag{21}
\]

uniformly. The scalar trace density is

\[
\nu_L(dx)=p_L(x)\cosh(a g_L(|x|))[1+O(L^{-1})]dx.
\]

Put \(x=\sqrt{L/c}\,y\). Laplace scaling gives \(p_L(x)dx\to\varphi_m(y)dy\), the standard Gaussian law, and

\[
\sqrt L\,g_L(\sqrt{L/c}|y|)\longrightarrow\sqrt c|y|.
\]

The convergence needed here is dominated: \(f(s)\) is bounded below by a positive constant times \(\min(s^2,s)\), and

\[
0\le f'(s)=s\frac{1+\log\sqrt{1+s^2}}{\sqrt{1+s^2}}
\le s.
\]

After increasing a fixed lower bound on \(L\), these bounds give an integrable exponential envelope after rescaling, even with the \(\cosh(a g_L)\) factor. They control the required second and fourth moments. Equation (21), \(|\tanh z|\le|z|\), and dominated convergence give

\[
\boxed{\zeta_L\sim\frac{mca^2}{L},\qquad
F_{M_L}(0)\sim\frac{ca^2}{L}I_m.}                       \tag{22}
\]

The optimal local variance per physical mean is asymptotically at least \(L/c\) per shot, while the spherical measurement has variance \(ma^2\). The raw coordinate report has second moment \(a^2+v_L\sim L/c\), so it is asymptotically efficient at the center among locally unbiased estimators. Nonlinear decoding cannot remove this leading local information loss. For the testing problem (17), which does not require unbiasedness, \(n=\Omega(L/(ca^2h^2))\) is necessary.

This is a fixed-\(m,a,c\), \(L\to\infty\) statement. It gives neither a certified useful value of the source's sufficient \(L_0\) nor a uniform approximation as \(m\) grows. The practical construction remains gated by those constants.

## 7 An explicit comparator circuit and complete resource boundary

For \(n_q\) qubits take the canonical generators

\[
\Gamma_{2k-1}=Z_1\cdots Z_{k-1}X_k,\quad
\Gamma_{2k}=Z_1\cdots Z_{k-1}Y_k,\quad
\Gamma_{2n_q+1}=Z_1\cdots Z_{n_q}.
\]

Use any prefix with \(2\le m\le2n_q+1\). Adjacent products have local support:

\[
\Gamma_{2k-1}\Gamma_{2k}=iZ_k,\quad
\Gamma_{2k}\Gamma_{2k+1}=iX_kX_{k+1}\ (k<n_q),\quad
\Gamma_{2n_q}\Gamma_{2n_q+1}=iX_{n_q}.
\]

For a supplied unit axis \(v\), a descending Givens sweep uses \(m-1\) rotations

\[
U_j(\theta)=\exp[\theta\Gamma_j\Gamma_{j+1}/2]
\]

to map \(\Gamma(v)\) to \(\Gamma_1\). In coefficient coordinates each rotation sends

\[
(v_j,v_{j+1})\mapsto
(v_j\cos\theta+v_{j+1}\sin\theta,
-v_j\sin\theta+v_{j+1}\cos\theta).
\]

Choosing \(\theta=\operatorname{atan2}(v_{j+1},v_j)\) eliminates the second entry. Applying the resulting \(U\) to the specimen and measuring \(X_1\) implements the binary projective measurement. Each rotation is a one-qubit rotation or a nearest-neighbor \(XX\) rotation; count and sequential depth are \(O(m)\), with no matrix of dimension \(2^{n_q}\) compiled.

An ideal \(N\) sample uses one state preparation, \(m-1\) such rotations, one single-qubit readout, a state reset, and \(O(m)\) classical random variates/arithmetic to sample and normalize a Gaussian axis. The record takes \(O(mb)\) bits when coordinates have \(b\)-bit precision. Continuous exact axes are an idealization: finite control and arithmetic accuracy must be charged.

If each of the \(m-1\) gates has operator error at most \(\epsilon_g/(m-1)\), telescoping bounds the circuit operator error by \(\epsilon_g\) and the conditional binary-outcome error by a constant times \(\epsilon_g\), uniformly over states and a fixed selected axis. The report \(am\,u\cdot n\) is bounded by \(am\), so conditional total variation error \(\tau\) introduces bias at most \(2am\tau\).

A finitely supported axis record has total variation one from the continuous ideal record. Finite axis precision must instead be compared after common quantization or by a coupling: if an approximate unit axis \(\widetilde v\) can be coupled to uniform \(v\) with \(\mathbb E|v-\widetilde v|\le\alpha\), coupling the binary outcomes gives mean-report bias at most \(2am\alpha\). Combining this with gate error, a sufficient per-gate accuracy for target mean error \(\varepsilon\) is order \(\varepsilon/(am^2)\), and a sufficient axis-coupling error is order \(\varepsilon/(am)\). This costs \(O(\log(am^2/\varepsilon))\) angle bits per gate; an axis sampler meeting the stated coupling guarantee and fault-tolerant rotation synthesis remain implementation inputs. No energy or calibration figure is supplied by this algebra.

For \(K\) fixed unit directions, median-of-means applied to spherical reports gives

\[
n=O\!\left(\frac{ma^2}{\varepsilon^2}
\log\frac K\delta\right)                               \tag{23}
\]

preparations for simultaneous additive error \(\varepsilon\) and failure probability \(\delta\). Postprocessing costs \(O(Km)\) arithmetic per stored vector naively; it can be streamed. Acquisition and reset costs multiply this shot count and are not specified by the state model.

For precisely the functionals in (8), an even simpler matched baseline chooses \(j\) uniformly, measures the Pauli string \(\Gamma_j\), and reports \(amz e_j\). It has the same second moment \(ma^2\) in every unit direction. Pauli strings can be measured through local basis measurements and a classical parity, using \(O(n_q)\) local readouts and no entangling gates. This discrete baseline does not realize the exact scalar-convolution contract, which the scientific estimation task does not require.

The circuit description concerns qubit encodings. Interpreting odd Majorana operators as directly measurable on a physical fermionic substrate would additionally require an appropriate parity reference or control interface; that resource is not provided here.

## 8 Primary comparators and defensible scope

The Fisher-information tradeoff is already covered more generally by Koichi Yamagata, [An attainable Gill–Massar-type bound for spin-factor models](https://arxiv.org/html/2609.23020v1), submitted 19 September 2026. Theorem 1 describes the full attainable SLD-normalized Fisher region over finite-outcome single-copy POVMs, and Section 2 proves the positive projection onto the spin factor. Equations (13)–(15) above are the elementary center specialization, extended directly to the present continuous experiment. The explicit radial garbling and scalar-convolution response obstruction are the relevant applications here; historical novelty of these applications is not claimed.

Joint-measurement versus shadow comparisons must use the established relationship, not equate an exact positive representation with a new information resource. McNulty, Maciejewski and Oszmaniec, [Estimating Quantum Hamiltonians via Joint Measurements of Noisy Non-Commuting Observables](https://arxiv.org/abs/2206.08912), explicitly connect joint measurements and classical shadows and obtain matched performance in their setting. For physically relevant even-degree fermionic observables, Majsak, McNulty and Oszmaniec, [A Simple and Efficient Joint Measurement Strategy for Estimating Fermionic Observables and Hamiltonians](https://arxiv.org/abs/2402.19230), provide efficient measurement and sample-complexity comparators. Neither paper is used as a substitute proof of this result.

The foundational scalar-convolution theorem may still have mathematical interest. The present result closes a particular proposed route to scientific capability: extending the qubit implementation to an arbitrarily large Clifford representation cannot add information through smoothing, and cannot supply response or nonlinear state information absent from the operator space. A different tuple with a richer accessible space could avoid that obstruction, but its measurement compilation, information conditioning, and comparison to the best task-specific protocol must then be established afresh.

## Verification and open gates

*checks.py* verifies the two-qubit identities exactly, Clifford anticommutation in small canonical representations, adjacent-generator support, the Givens compiler numerically, and the third-moment endpoint contradiction with exact rational arithmetic. *checks.json* records actual outputs. These checks support finite algebra and compiler formulas, not the general analytic proofs, large-scale asymptotic, universal positivity, or hardware performance.

The result's status is **NO NEW OPERATIONAL CAPABILITY ESTABLISHED**. The strongest established outcome within this analysis is the explicit domination and response obstruction. The asymptotic has the stated source premise. An optimal regularizer, a useful finite sufficient smoothing scale, a hardware implementation, and advantage for a richer non-Clifford task remain unestablished.
