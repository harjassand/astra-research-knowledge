[Skip to main content](https://arxiv.org/html/2608.06367v1#infobox)

Title:

Content selection saved. Describe the issue below:

Description:

[License: arXiv.org perpetual non-exclusive license](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2608.06367v1 \[math.AP\] 06 Aug 2026

# Quasiconvexity for the Dacorogna–Marcellini Energy

Giuseppe Bruno
Affiliation: University of Bern and Google DeepMindFederico Pasqualotto
Affiliation: University of California San Diego and Google DeepMind

August 24, 2026

###### Abstract

We prove that the planar Dacorogna–Marcellini energy
fγ​(A)=\|A\|4−2​γ​\|A\|2​detAf\_{\\gamma}(A)=\|A\|^{4}-2\\gamma\|A\|^{2}\\det A is quasiconvex exactly when
it is rank-one convex, i.e. if and only if
\|γ\|≤23\|\\gamma\|\\leq\\frac{2}{\\sqrt{3}}.
The proof uses a monotonicity property of the energy functional along the componentwise heat flow. As a corollary of our method, we show that for homogeneous quartic polynomials on 2×22\\times 2 matrices invariant by left and right rotation, quasiconvexity is equivalent to rank one convexity.

## 1 Introduction

Let Ω⊂ℝn\\Omega\\subset\\mathbb{R}^{n} be a bounded domain and consider a
first-order variational integral

|     |     |     |
| --- | --- | --- |
|  | ℐf​(u)=∫Ωf⁡(D​u​(x))​𝑑x,u:Ω→ℝm,\\mathcal{I}\_{f}(u)=\\int\_{\\Omega}f(Du(x))\\,\\mathrm{d}x,\\qquad u:\\Omega\\to\\mathbb{R}^{m}, |  |

where f:ℝm×n→ℝf:\\mathbb{R}^{m\\times n}\\to\\mathbb{R} is continuous. In the direct method
of the calculus of variations, weak lower semicontinuity of
ℐf\\mathcal{I}\_{f} allows one to pass to the weak limit of a minimizing
sequence and is therefore a fundamental property in existence results
\[ [5](https://arxiv.org/html/2608.06367v1#bib.bib5 "")\].
For scalar problems, ordinary convexity gives the relevant condition,
whereas for vector-valued maps the situation is more difficult.

Morrey introduced quasiconvexity in his study of this question
\[ [19](https://arxiv.org/html/2608.06367v1#bib.bib19 "")\]. An integrand
f:ℝm×n→ℝf:\\mathbb{R}^{m\\times n}\\to\\mathbb{R} is _quasiconvex_ if

|     |     |     |     |
| --- | --- | --- | --- |
|  | ∫Uf⁡(F+D​φ)​𝑑x≥\|U\|​f​(F)\\int\_{U}f(F+D\\varphi)\\,\\mathrm{d}x\\geq\|U\|f(F) |  | (1.1) |

for every bounded Lipschitz domain U⊂ℝnU\\subset\\mathbb{R}^{n}, every
F∈ℝm×nF\\in\\mathbb{R}^{m\\times n}, and every
φ∈W01,∞​(U,ℝm)\\varphi\\in W^{1,\\infty}\_{0}(U,\\mathbb{R}^{m}). When m=1m=1 or n=1n=1,
this condition is equivalent to convexity, whereas for m,n≥2m,n\\geq 2
it is much harder to check.

Since the definition is global in the perturbation φ\\varphi,
quasiconvexity is difficult to verify directly. Rank-one convexity
provides a simpler necessary condition: the integrand ff is
_rank-one convex_ if

|     |     |     |
| --- | --- | --- |
|  | f⁡((1−t)​A+t​B)≤(1−t)​f​(A)+t​f​(B)f\\bigl((1-t)A+tB\\bigr)\\leq(1-t)f(A)+tf(B) |  |

whenever t∈\[0,1\]t\\in\[0,1\], A,B∈ℝm×nA,B\\in\\mathbb{R}^{m\\times n}, and
rank⁡(A−B)≤1\\operatorname{rank}(A-B)\\leq 1. For a twice differentiable
integrand, this is equivalent to the Legendre–Hadamard inequalities

|     |     |     |     |
| --- | --- | --- | --- |
|  | D2​f​(A)​\[a⊗b,a⊗b\]≥0,a∈ℝm,b∈ℝn.D^{2}f(A)\[a\\otimes b,a\\otimes b\]\\geq 0,\\qquad a\\in\\mathbb{R}^{m},\\quad b\\in\\mathbb{R}^{n}. |  | (1.2) |

Every quasiconvex integrand is rank-one convex, and the question of
whether the converse holds is known as Morrey’s problem.

Polyconvexity provides a useful sufficient condition: an integrand is
_polyconvex_ if it is a convex function of all the minors of its
matrix argument. In dimension 2×22\\times 2, this means that

|     |     |     |
| --- | --- | --- |
|  | f⁡(A)=g⁡(A,detA)f(A)=g(A,\\det A) |  |

for some convex function g:ℝ2×2×ℝ→ℝg:\\mathbb{R}^{2\\times 2}\\times\\mathbb{R}\\to\\mathbb{R}, a
condition introduced by Ball in nonlinear elasticity
\[ [4](https://arxiv.org/html/2608.06367v1#bib.bib4 "")\]. Together, these notions satisfy

|     |     |     |
| --- | --- | --- |
|  | convex⟹polyconvex⟹quasiconvex⟹rank-one convex.\\text{convex}\\quad\\Longrightarrow\\quad\\text{polyconvex}\\quad\\Longrightarrow\\quad\\text{quasiconvex}\\quad\\Longrightarrow\\quad\\text{rank-one convex}. |  |

Although none of the reverse implications holds in full generality,
the last one is the most relevant here. Šverák constructed a
rank-one-convex integrand on
ℝ3×2\\mathbb{R}^{3\\times 2} which is not quasiconvex \[ [21](https://arxiv.org/html/2608.06367v1#bib.bib21 "")\]. This
settled the question in higher target dimension, but the construction
does not descend to ℝ2×2\\mathbb{R}^{2\\times 2}, which became the basic testing
ground for the gap between rank-one convexity and quasiconvexity.

The planar problem has also been studied by imposing additional
structure on the matrices or on the integrand. Müller proved that
rank-one convexity implies quasiconvexity on diagonal matrices
\[ [20](https://arxiv.org/html/2608.06367v1#bib.bib20 "")\], and Harris, Kirchheim, and Lin extended this result
to upper-triangular 2×22\\times 2 matrices
\[ [15](https://arxiv.org/html/2608.06367v1#bib.bib15 "")\]. Székelyhidi described the geometry of
rank-one-convex hulls in ℝ2×2\\mathbb{R}^{2\\times 2} and of quasiconvex hulls in
the symmetric subspace \[ [22](https://arxiv.org/html/2608.06367v1#bib.bib22 ""), [23](https://arxiv.org/html/2608.06367v1#bib.bib23 "")\].
Faraco and Székelyhidi proved a localization theorem for quasiconvex
hulls in ℝ2×2\\mathbb{R}^{2\\times 2}, while Kirchheim and Székelyhidi obtained
a characterization of incompatible sets of planar gradients
\[ [11](https://arxiv.org/html/2608.06367v1#bib.bib11 ""), [16](https://arxiv.org/html/2608.06367v1#bib.bib16 "")\]. For
rotationally invariant integrands, Dacorogna and Koshigoe showed that convexity and
polyconvexity can be tested on diagonal matrices, although the same
reduction is not valid for rank-one convexity and quasiconvexity
\[ [8](https://arxiv.org/html/2608.06367v1#bib.bib8 "")\]. A stronger conclusion holds in the
isochoric class from nonlinear elasticity, where Martin, Ghiba, and
Neff proved that every objective and isotropic rank-one-convex energy
on GL+​(2)\\mathrm{GL}^{+}(2) is polyconvex \[ [17](https://arxiv.org/html/2608.06367v1#bib.bib17 "")\].

Connections with quasiconformal mapping theory are organized around
the Burkholder integrands. Astala, Iwaniec, Prause, and Saksman proved
sharp quasiconcavity inequalities for these integrands under a
pointwise distortion restriction \[ [3](https://arxiv.org/html/2608.06367v1#bib.bib3 "")\]. Guerra and
Kristensen later obtained automatic polyconvexity and conditional
quasiconvexity results for nonnegative homogeneous isotropic
rank-one-convex integrands \[ [13](https://arxiv.org/html/2608.06367v1#bib.bib13 "")\]. More recently,
Astala, Faraco, Guerra, Koski, and Kristensen proved quasiconvexity of
the local Burkholder functional and obtained quasiconvex energies on
the set of matrices with positive determinant which are not
polyconvex \[ [2](https://arxiv.org/html/2608.06367v1#bib.bib2 "")\].

Finite elasticity provides another planar candidate family. For
objective and isotropic energies with an additive
volumetric–isochoric split, Voss, Martin, Ghiba, and Neff reduced part
of Morrey’s problem to the quasiconvexity of the rank-one-convex energy
Wmagic+W\_{\\mathrm{magic}}^{+}\[ [24](https://arxiv.org/html/2608.06367v1#bib.bib24 "")\]. Numerical tests based on
finite elements, derivative-free optimization, and neural networks
did not find a violation of quasiconvexity for this energy
\[ [25](https://arxiv.org/html/2608.06367v1#bib.bib25 "")\].

The Dacorogna–Marcellini family was introduced to study this planar
gap. For γ∈ℝ\\gamma\\in\\mathbb{R}, it is given by

|     |     |     |     |
| --- | --- | --- | --- |
|  | fγ​(A)=\|A\|4−2​γ​\|A\|2​detA,A∈ℝ2×2,f\_{\\gamma}(A)=\|A\|^{4}-2\\gamma\|A\|^{2}\\det A,\\qquad A\\in\\mathbb{R}^{2\\times 2}, |  | (1.3) |

where \|A\|\|A\| is the Frobenius norm. Dacorogna and Marcellini
introduced this quartic family in \[ [9](https://arxiv.org/html/2608.06367v1#bib.bib9 "")\]. Its
local convexity conditions can be computed exactly, while part of the
family lies beyond the polyconvex range, which makes it a useful model
for the planar problem.

The analysis of Dacorogna, Douchet, Gangbo, and Rappaz and of Alibert
and Dacorogna \[ [6](https://arxiv.org/html/2608.06367v1#bib.bib6 ""), [1](https://arxiv.org/html/2608.06367v1#bib.bib1 "")\] showed that

|     |     |     |     |
| --- | --- | --- | --- |
|  | fγ​ is convex\\displaystyle f\_{\\gamma}\\text{ is convex} | ⟺\|γ\|≤2​23,\\displaystyle\\Longleftrightarrow\\quad\|\\gamma\|\\leq\\frac{2\\sqrt{2}}{3}, |  |
|  | fγ​ is polyconvex\\displaystyle f\_{\\gamma}\\text{ is polyconvex} | ⟺\|γ\|≤1,\\displaystyle\\Longleftrightarrow\\quad\|\\gamma\|\\leq 1, |  |
|  | fγ​ is rank-one convex\\displaystyle f\_{\\gamma}\\text{ is rank-one convex} | ⟺\|γ\|≤23.\\displaystyle\\Longleftrightarrow\\quad\|\\gamma\|\\leq\\frac{2}{\\sqrt{3}}. |  |

The endpoint \|γ\|=2/3\|\\gamma\|=2/\\sqrt{3} is rank-one convex but not
polyconvex, while polyconvexity proves quasiconvexity only for
\|γ\|≤1\|\\gamma\|\\leq 1. This leaves the interval

|     |     |     |
| --- | --- | --- |
|  | 1<\|γ\|≤231<\|\\gamma\|\\leq\\frac{2}{\\sqrt{3}} |  |

open. Failure of quasiconvexity in this interval would provide a
counterexample to the planar implication, while validity up to the
endpoint would make the quasiconvexity and rank-one-convexity
thresholds coincide for the whole family.

The first investigations were numerical, and Dacorogna, Douchet,
Gangbo, and Rappaz found evidence for quasiconvexity at the endpoint
\[ [6](https://arxiv.org/html/2608.06367v1#bib.bib6 "")\]. Alibert and Dacorogna then proved that there
exists
ε>0\\varepsilon>0 such that

|     |     |     |
| --- | --- | --- |
|  | \|γ\|≤1+ε⟹fγ​ is quasiconvex,\|\\gamma\|\\leq 1+\\varepsilon\\quad\\Longrightarrow\\quad f\_{\\gamma}\\text{ is quasiconvex}, |  |

and hence obtained an explicit quasiconvex integrand which is not
polyconvex \[ [1](https://arxiv.org/html/2608.06367v1#bib.bib1 "")\]. Their argument crossed the
polyconvex threshold but did not reach the full rank-one-convexity
range, so the remaining gap continued to be studied numerically.
Gremaud used a simulated-annealing method, while Dacorogna and
Haeberly compared several numerical schemes, and both studies found
evidence that quasiconvexity persists throughout the rank-one-convex
range \[ [12](https://arxiv.org/html/2608.06367v1#bib.bib12 ""), [7](https://arxiv.org/html/2608.06367v1#bib.bib7 "")\]. Gutiérrez and
Villavicencio studied a broader optimization problem for quartic
polynomials without finding a planar counterexample
\[ [14](https://arxiv.org/html/2608.06367v1#bib.bib14 "")\]. Dong and Enakoutsa later reported
numerical violations for the Dacorogna–Marcellini family
\[ [10](https://arxiv.org/html/2608.06367v1#bib.bib10 "")\]. The different outcomes did not determine
the quasiconvexity threshold.

###### Theorem 1.

For \|γ\|≤2/3\|\\gamma\|\\leq 2/\\sqrt{3}, the function fγf\_{\\gamma} defined in
( [1.3](https://arxiv.org/html/2608.06367v1#S1.E3 "In 1 Introduction ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")) is quasiconvex.

Since quasiconvexity implies rank-one convexity, the known obstruction
beyond 2/32/\\sqrt{3} is also necessary. Thus

|     |     |     |
| --- | --- | --- |
|  | fγ is quasiconvex⟺fγ is rank-one convex⟺\|γ\|≤23.f\_{\\gamma}\\text{ is quasiconvex}\\quad\\Longleftrightarrow\\quad f\_{\\gamma}\\text{ is rank-one convex}\\quad\\Longleftrightarrow\\quad\|\\gamma\|\\leq\\frac{2}{\\sqrt{3}}. |  |

In particular, the whole interval
1<\|γ\|≤2/31<\|\\gamma\|\\leq 2/\\sqrt{3} consists of quasiconvex integrands which are
not polyconvex.

Our method also applied to more general invariant quartic homogeneous polynomials.

###### Theorem 2.

Let Q:ℝ2×2→ℝQ:\\mathbb{R}^{2\\times 2}\\to\\mathbb{R} be a homogeneous polynomial of degree 4 such that

|     |     |     |
| --- | --- | --- |
|  | Q⁡(U​F​VT)=Q⁡(F)for every ​F∈ℝ2×2​ and ​U,V∈S​O​(2).Q(UFV^{T})=Q(F)\\qquad\\text{for every }F\\in\\mathbb{R}^{2\\times 2}\\text{ and }U,V\\in SO(2). |  |

Then QQ is quasiconvex if and only if it is rank-one convex.

The proof of Theorem [2](https://arxiv.org/html/2608.06367v1#Thmtheorem2 "Theorem 2. ‣ 1 Introduction ‣ Quasiconvexity for the Dacorogna–Marcellini Energy") proceeds in the same way as the proof of Theorem [1](https://arxiv.org/html/2608.06367v1#Thmtheorem1 "Theorem 1. ‣ 1 Introduction ‣ Quasiconvexity for the Dacorogna–Marcellini Energy"), once one observes that every such polynomial admits a unique representation

|     |     |     |
| --- | --- | --- |
|  | Q⁡(F)=a​\|F\|4+b​\|F\|2​detF+c​(detF)2.Q(F)=a\|F\|^{4}+b\|F\|^{2}\\det F+c(\\det F)^{2}. |  |

for a,b,c∈ℝa,b,c\\in\\mathbb{R}.

### Proof strategy.

The proof uses a monotonicity argument rather than a direct estimate of
( [1.1](https://arxiv.org/html/2608.06367v1#S1.E1 "In 1 Introduction ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")). Given a compactly supported perturbation
φ\\varphi, we evolve it by the heat equation

|     |     |     |
| --- | --- | --- |
|  | φτ=eτ​Δ​φ.\\varphi\_{\\tau}=e^{\\tau\\Delta}\\varphi. |  |

As τ→∞\\tau\\to\\infty, the perturbation disappears, and differentiation
of the relative energy along this path reduces the proof to the
integrated second-variation inequality

|     |     |     |
| --- | --- | --- |
|  | ∫ℝ2∑i=12D2​fγ​(D​v)​\[∂iD​v,∂iD​v\],𝑑x≥0.\\int\_{\\mathbb{R}^{2}}\\sum\_{i=1}^{2}D^{2}f\_{\\gamma}(Dv)\[\\partial\_{i}Dv,\\partial\_{i}Dv\],\\mathrm{d}x\\geq 0. |  |

This step is related to the flow-interchange method of Matthes, McCann,
and Savaré \[ [18](https://arxiv.org/html/2608.06367v1#bib.bib18 "")\], since the functional is
studied along an auxiliary flow with simple long-time behavior.

Since the second-variation density need not be pointwise nonnegative,
we construct an
S​O​(2)×S​O​(2)SO(2)\\times SO(2)-invariant exact two-form
ωγ=d​αγ\\omega\_{\\gamma}=\\mathrm{d}\\alpha\_{\\gamma} on matrix space. Its pullback by a
gradient has zero integral,

|     |     |     |
| --- | --- | --- |
|  | ∫ℝ2(D​v)∗​ωγ=0.\\int\_{\\mathbb{R}^{2}}(Dv)^{\*}\\omega\_{\\gamma}=0. |  |

We choose ωγ\\omega\_{\\gamma} so that adding it to
the second-variation density makes the resulting expression
pointwise nonnegative, thereby changing the density without changing
its integral.

The rotational invariance of both the energy and the correction
reduces the pointwise inequality to matrices of the form
diag⁡(1,ρ)\\operatorname{diag}(1,\\rho). At the endpoint
\|γ\|=2/3\|\\gamma\|=2/\\sqrt{3}, it remains to prove that an explicit quadratic
form is nonnegative, while the intermediate values of γ\\gamma follow
by interpolation. The next section develops the heat-flow
criterion, and the final section constructs the exact correction and
verifies the pointwise inequality.

### Statement on AI use

We acknowledge the use of AI tools in both devising important ideas for this paper, and in the writing of the manuscript. In particular, the exact two-form used in the proof was found in an autonomous way by an AI assisted method using an agentic system, Gemini / Aletheia2.

### Acknowledgements

The authors acknowledge support from Thang Luong and Garrett Bingham (Google DeepMind) for providing access to the models used in the proof. We also acknowledge André Guerra for comments on a preliminary version of the manuscript.

## 2 Monotonicity under heat flow

To study the functional generated by fγf\_{\\gamma}, we use a strategy
related to the flow-interchange technique of Matthes, McCann, and
Savaré from Wasserstein gradient flow theory
\[ [18](https://arxiv.org/html/2608.06367v1#bib.bib18 "")\]. The idea is to compute the evolution of a functional
along an auxiliary flow rather than along its own gradient flow. Here, the auxiliary flow is the heat flow.

For A,B1,B2∈ℝ2×2A,B\_{1},B\_{2}\\in\\mathbb{R}^{2\\times 2}, define

|     |     |     |
| --- | --- | --- |
|  | ℰγ​(A,B1,B2)=∑i=12D2​fγ​(A)​\[Bi,Bi\].\\mathcal{E}\_{\\gamma}(A;B\_{1},B\_{2})=\\sum\_{i=1}^{2}D^{2}f\_{\\gamma}(A)\[B\_{i},B\_{i}\]. |  |

###### Lemma 3.

Fix γ∈ℝ\\gamma\\in\\mathbb{R}. Suppose that

|     |     |     |     |
| --- | --- | --- | --- |
|  | ∫ℝ2ℰγ​(D​v,∂1D​v,∂2D​v)​𝑑x≥0\\int\_{\\mathbb{R}^{2}}\\mathcal{E}\_{\\gamma}\\bigl(Dv;\\partial\_{1}Dv,\\partial\_{2}Dv\\bigr)\\,\\mathrm{d}x\\geq 0 |  | (2.1) |

whenever v⁡(x)=F​x+ψ⁡(x)v(x)=Fx+\\psi(x), with F∈ℝ2×2F\\in\\mathbb{R}^{2\\times 2} and
ψ\\psi in the Schwartz class. Then fγf\_{\\gamma} is quasiconvex.

###### Proof.

Fix F∈ℝ2×2F\\in\\mathbb{R}^{2\\times 2} and
φ∈Cc∞​(ℝ2,ℝ2)\\varphi\\in C\_{c}^{\\infty}(\\mathbb{R}^{2},\\mathbb{R}^{2}). Let

|     |     |     |
| --- | --- | --- |
|  | φτ=eτ​Δ​φ,Gτ=D​φτ,Aτ=F+Gτ.\\varphi\_{\\tau}=e^{\\tau\\Delta}\\varphi,\\qquad G\_{\\tau}=D\\varphi\_{\\tau},\\qquad A\_{\\tau}=F+G\_{\\tau}. |  |

Define

|     |     |     |
| --- | --- | --- |
|  | ℱ⁡(τ)=∫ℝ2\[fγ​(Aτ)−fγ​(F)−tr⁡(D​fγ​(F)​GτT)\],𝑑x.\\mathcal{F}(\\tau)=\\int\_{\\mathbb{R}^{2}}\\bigl\[f\_{\\gamma}(A\_{\\tau})-f\_{\\gamma}(F)-\\operatorname{tr}\\bigl(Df\_{\\gamma}(F)G\_{\\tau}^{T}\\bigr)\\bigr\],\\mathrm{d}x. |  |

For τ>0\\tau>0, integration by parts and
∂τAτ=Δ​Aτ\\partial\_{\\tau}A\_{\\tau}=\\Delta A\_{\\tau} give

|     |     |     |
| --- | --- | --- |
|  | ℱ′(τ)=−∫ℝ2ℰγ(Aτ;∂1Aτ,∂2Aτ)dx.\\mathcal{F}^{\\prime}(\\tau)=-\\int\_{\\mathbb{R}^{2}}\\mathcal{E}\_{\\gamma}\\bigl(A\_{\\tau};\\partial\_{1}A\_{\\tau},\\partial\_{2}A\_{\\tau}\\bigr)\\,\\mathrm{d}x. |  |

The hypothesis applied to vτ​(x)=F​x+φτ​(x)v\_{\\tau}(x)=Fx+\\varphi\_{\\tau}(x) shows that
ℱ\\mathcal{F} is nonincreasing. The heat kernel estimate in two dimensions gives

|     |     |     |     |
| --- | --- | --- | --- |
|  | ∥Gτ∥Lp≤Cpτ−(1−1/p)∥Dφ∥L1,p=2,3,4.\\\|G\_{\\tau}\\\|\_{L^{p}}\\leq C\_{p}\\tau^{-(1-1/p)}\\\|D\\varphi\\\|\_{L^{1}},\\qquad p=2,3,4. |  | (2.2) |

Since fγf\_{\\gamma} is quartic,

|     |     |     |     |
| --- | --- | --- | --- |
|  | \|fγ​(F+G)−fγ​(F)−tr⁡(D​fγ​(F)​GT)\|≤Cγ​(\|F\|2​\|G\|2+\|F\|​\|G\|3+\|G\|4).\\displaystyle\\bigl\|f\_{\\gamma}(F+G)-f\_{\\gamma}(F)-\\operatorname{tr}\\bigl(Df\_{\\gamma}(F)G^{T}\\bigr)\\bigr\|\\leq C\_{\\gamma}\\bigl(\|F\|^{2}\|G\|^{2}+\|F\|\|G\|^{3}+\|G\|^{4}\\bigr). |  | (2.3) |

Equations ( [2.2](https://arxiv.org/html/2608.06367v1#S2.E2 "In Proof. ‣ 2 Monotonicity under heat flow ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")) and ( [2.3](https://arxiv.org/html/2608.06367v1#S2.E3 "In Proof. ‣ 2 Monotonicity under heat flow ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")) imply
that ℱ⁡(τ)→0\\mathcal{F}(\\tau)\\to 0 as τ→∞\\tau\\to\\infty.

To justify the limit at zero, put

|     |     |     |
| --- | --- | --- |
|  | ℛF​(G)=fγ​(F+G)−fγ​(F)−tr⁡(D​fγ​(F)​GT).\\mathcal{R}\_{F}(G)=f\_{\\gamma}(F+G)-f\_{\\gamma}(F)-\\operatorname{tr}\\bigl(Df\_{\\gamma}(F)G^{T}\\bigr). |  |

Since ℛF\\mathcal{R}\_{F} is the sum of terms of degrees two, three, and
four in GG,

|     |     |     |     |
| --- | --- | --- | --- |
|  | \|ℛF(G)−ℛF(H)\|≤Cγ\[\\displaystyle\|\\mathcal{R}\_{F}(G)-\\mathcal{R}\_{F}(H)\|\\leq C\_{\\gamma}\\bigl\[ | \|F\|2​(\|G\|+\|H\|)+\|F\|​(\|G\|2+\|H\|2)\\displaystyle\|F\|^{2}(\|G\|+\|H\|)+\|F\|(\|G\|^{2}+\|H\|^{2}) |  |\
|  |  | +\|G\|3+\|H\|3\]\|G−H\|.\\displaystyle+\|G\|^{3}+\|H\|^{3}\\bigr\]\|G-H\|. |  |

Writing G0=D​φG\_{0}=D\\varphi and applying Hölder’s inequality gives

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
|  | \|ℱ(τ)−ℱ(0)\|≤Cγ\[\\displaystyle\|\\mathcal{F}(\\tau)-\\mathcal{F}(0)\|\\leq C\_{\\gamma}\\bigl\[ | \|F\|2​(‖Gτ‖L2+‖G0‖L2)​‖Gτ−G0‖L2\\displaystyle\|F\|^{2}(\\\|G\_{\\tau}\\\|\_{L^{2}}+\\\|G\_{0}\\\|\_{L^{2}})\\\|G\_{\\tau}-G\_{0}\\\|\_{L^{2}} |  |\
|  |  | +\|F\|(‖Gτ‖L32+‖G0‖L32)​‖Gτ−G0‖L3\\displaystyle+\|F\|(\\\|G\_{\\tau}\\\|\_{L^{3}}^{2}+\\\|G\_{0}\\\|\_{L^{3}}^{2})\\\|G\_{\\tau}-G\_{0}\\\|\_{L^{3}} |  |\
|  |  | +(∥Gτ∥L43+∥G0∥L43)∥Gτ−G0∥L4\].\\displaystyle+(\\\|G\_{\\tau}\\\|\_{L^{4}}^{3}+\\\|G\_{0}\\\|\_{L^{4}}^{3})\\\|G\_{\\tau}-G\_{0}\\\|\_{L^{4}}\\bigr\]. |  | (2.4) |

For p=2,3,4p=2,3,4, strong continuity of the heat semigroup gives

|     |     |     |
| --- | --- | --- |
|  | ‖Gτ−G0‖Lp=‖eτ​Δ​G0−G0‖Lp⟶0(τ→0).\\\|G\_{\\tau}-G\_{0}\\\|\_{L^{p}}=\\\|e^{\\tau\\Delta}G\_{0}-G\_{0}\\\|\_{L^{p}}\\longrightarrow 0\\qquad(\\tau\\to 0). |  |

The remaining norms in ( [2.4](https://arxiv.org/html/2608.06367v1#S2.E4 "In Proof. ‣ 2 Monotonicity under heat flow ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")) are
bounded for small τ\\tau. Hence
ℱ⁡(τ)→ℱ⁡(0)\\mathcal{F}(\\tau)\\to\\mathcal{F}(0) as τ→0\\tau\\to 0.
Monotonicity therefore implies ℱ⁡(0)≥0\\mathcal{F}(0)\\geq 0. Since
∫ℝ2D​φ​𝑑x=0\\int\_{\\mathbb{R}^{2}}D\\varphi\\,\\mathrm{d}x=0, this is

|     |     |     |
| --- | --- | --- |
|  | ∫ℝ2\[fγ​(F+D​φ)−fγ​(F)\]​𝑑x≥0.\\int\_{\\mathbb{R}^{2}}\\bigl\[f\_{\\gamma}(F+D\\varphi)-f\_{\\gamma}(F)\\bigr\]\\mathrm{d}x\\geq 0. |  |

For φ∈W01,∞​(Ω,ℝ2)\\varphi\\in W^{1,\\infty}\_{0}(\\Omega,\\mathbb{R}^{2}), choose
φj∈Cc∞​(Ω,ℝ2)\\varphi\_{j}\\in C\_{c}^{\\infty}(\\Omega,\\mathbb{R}^{2}) converging to φ\\varphi
in W1,4W^{1,4}. The estimate

|     |     |     |
| --- | --- | --- |
|  | \|fγ​(F+G)−fγ​(F+H)\|≤Cγ​(\|F\|+\|G\|+\|H\|)3​\|G−H\|\|f\_{\\gamma}(F+G)-f\_{\\gamma}(F+H)\|\\leq C\_{\\gamma}(\|F\|+\|G\|+\|H\|)^{3}\|G-H\| |  |

and Hölder’s inequality allow passage to the limit. This proves
( [1.1](https://arxiv.org/html/2608.06367v1#S1.E1 "In 1 Introduction ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")).
∎

## 3 The correction lemma

Let α\\alpha be a polynomial one-form on ℝ2×2\\mathbb{R}^{2\\times 2}, and let
ω=d​α\\omega=\\mathrm{d}\\alpha. If v⁡(x)=F​x+ψ⁡(x)v(x)=Fx+\\psi(x), where ψ\\psi is in
the Schwartz class, then

|     |     |     |
| --- | --- | --- |
|  | (D​v)∗​ω=d⁡((D​v)∗​α).(Dv)^{\*}\\omega=\\mathrm{d}\\bigl((Dv)^{\*}\\alpha\\bigr). |  |

Every coefficient of (D​v)∗​α(Dv)^{\*}\\alpha contains a derivative of
D​vDv, so this one-form is rapidly decreasing. Stokes’ theorem gives

|     |     |     |     |
| --- | --- | --- | --- |
|  | ∫ℝ2ωD​v​(∂1D​v,∂2D​v)​𝑑x=0.\\int\_{\\mathbb{R}^{2}}\\omega\_{Dv}\\bigl(\\partial\_{1}Dv,\\partial\_{2}Dv\\bigr)\\,\\mathrm{d}x=0. |  | (3.1) |

Fix \|γ\|≤2/3\|\\gamma\|\\leq 2/\\sqrt{3}. To prove the sufficiency assertion in
Theorem [1](https://arxiv.org/html/2608.06367v1#Thmtheorem1 "Theorem 1. ‣ 1 Introduction ‣ Quasiconvexity for the Dacorogna–Marcellini Energy"), Lemma [3](https://arxiv.org/html/2608.06367v1#Thmtheorem3 "Lemma 3. ‣ 2 Monotonicity under heat flow ‣ Quasiconvexity for the Dacorogna–Marcellini Energy") shows that it is
enough to prove ( [2.1](https://arxiv.org/html/2608.06367v1#S2.E1 "In Lemma 3. ‣ 2 Monotonicity under heat flow ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")). In general, its
integrand
ℰγ​(D​v,∂1D​v,∂2D​v)\\mathcal{E}\_{\\gamma}(Dv;\\partial\_{1}Dv,\\partial\_{2}Dv)
is not pointwise nonnegative. We therefore seek an exact two-form
ωγ\\omega\_{\\gamma} whose addition makes this expression pointwise
nonnegative. If this form has a polynomial primitive, its integral
vanishes by ( [3.1](https://arxiv.org/html/2608.06367v1#S3.E1 "In 3 The correction lemma ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")). Integrating the corrected
inequality then gives ( [2.1](https://arxiv.org/html/2608.06367v1#S2.E1 "In Lemma 3. ‣ 2 Monotonicity under heat flow ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")), and
Lemma [3](https://arxiv.org/html/2608.06367v1#Thmtheorem3 "Lemma 3. ‣ 2 Monotonicity under heat flow ‣ Quasiconvexity for the Dacorogna–Marcellini Energy") proves quasiconvexity.

###### Lemma 4.

If \|γ\|≤2/3\|\\gamma\|\\leq 2/\\sqrt{3}, there is an exact two-form
ωγ\\omega\_{\\gamma} on ℝ2×2\\mathbb{R}^{2\\times 2}, with homogeneous quadratic coefficients
and invariant under

|     |     |     |
| --- | --- | --- |
|  | A⟼O​A​UT,O,U∈S​O​(2),A\\longmapsto OAU^{T},\\qquad O,U\\in SO(2), |  |

such that

|     |     |     |
| --- | --- | --- |
|  | ℰγ​(D​v,∂1D​v,∂2D​v)+(ωγ)D​v​(∂1D​v,∂2D​v)≥0\\mathcal{E}\_{\\gamma}(Dv;\\partial\_{1}Dv,\\partial\_{2}Dv)+(\\omega\_{\\gamma})\_{Dv}(\\partial\_{1}Dv,\\partial\_{2}Dv)\\geq 0 |  |

for every v∈C2​(Ω,ℝ2)v\\in C^{2}(\\Omega,\\mathbb{R}^{2}).

###### Proof.

It is enough to check this property for γ=2/3\\gamma=2/\\sqrt{3}, and we are going to reduce to this case throughout the proof.

Step 1. The function fγf\_{\\gamma} is invariant under rotations on the
left and on the right. We impose the same invariance on the correcting
form. Since the correction must be exact, we write
ω=d​α\\omega=\\mathrm{d}\\alpha and seek an invariant one-form α\\alpha.
The coefficients of ℰγ\\mathcal{E}\_{\\gamma} are homogeneous of degree two
in its first matrix argument. Thus ω\\omega must have homogeneous
quadratic coefficients, and α\\alpha must have homogeneous cubic
coefficients.

Write A=(𝐚1∣𝐚2)A=(\\mathbf{a}\_{1}\\mid\\mathbf{a}\_{2}) and
B=(𝐛1∣𝐛2)B=(\\mathbf{b}\_{1}\\mid\\mathbf{b}\_{2}). For vectors in ℝ2\\mathbb{R}^{2}, set
𝐚×𝐛=a1​b2−a2​b1\\mathbf{a}\\times\\mathbf{b}=a\_{1}b\_{2}-a\_{2}b\_{1}. Two invariant linear
one-forms are

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
|  | θA​(B)\\displaystyle\\theta\_{A}(B) | =𝐚1×𝐛1+𝐚2×𝐛2,\\displaystyle=\\mathbf{a}\_{1}\\times\\mathbf{b}\_{1}+\\mathbf{a}\_{2}\\times\\mathbf{b}\_{2}, |  | (3.2) |
|  | ζA​(B)\\displaystyle\\zeta\_{A}(B) | =𝐚1⋅𝐛2−𝐚2⋅𝐛1.\\displaystyle=\\mathbf{a}\_{1}\\cdot\\mathbf{b}\_{2}-\\mathbf{a}\_{2}\\cdot\\mathbf{b}\_{1}. |  | (3.3) |

Let
J=(0−110).J=\\begin{pmatrix}0&-1\\\
1&0\\end{pmatrix}.
Then

|     |     |     |
| --- | --- | --- |
|  | θA​(B)=tr⁡(J​A​BT),ζA​(B)=tr⁡(A​JT​BT).\\theta\_{A}(B)=\\operatorname{tr}(JAB^{T}),\\qquad\\zeta\_{A}(B)=\\operatorname{tr}(AJ^{T}B^{T}). |  |

The one-forms in ( [3.2](https://arxiv.org/html/2608.06367v1#S3.E2 "In Proof. ‣ 3 The correction lemma ‣ Quasiconvexity for the Dacorogna–Marcellini Energy"))–( [3.3](https://arxiv.org/html/2608.06367v1#S3.E3 "In Proof. ‣ 3 The correction lemma ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")) have linear coefficients in AA. To make α\\alpha homogeneous of degree three, we
multiply them by the quadratic scalar quantities already present in the
definition of fγf\_{\\gamma}, namely \|A\|2\|A\|^{2} and detA\\det A. We use
the four-parameter ansatz

|     |     |     |     |
| --- | --- | --- | --- |
|  | α=c1​\|A\|2​θ+c2​(detA)​ζ+c3​\|A\|2​ζ+c4​(detA)​θ,ω=d​α,\\alpha=c\_{1}\|A\|^{2}\\theta+c\_{2}(\\det A)\\zeta+c\_{3}\|A\|^{2}\\zeta+c\_{4}(\\det A)\\theta,\\qquad\\omega=\\mathrm{d}\\alpha, |  | (3.4) |

where c1,c2,c3,c4∈ℝc\_{1},c\_{2},c\_{3},c\_{4}\\in\\mathbb{R}.

In terms of the entries of AA,

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
|  | θ\\displaystyle\\theta | =A11​d​A21−A21​d​A11+A12​d​A22−A22​d​A12,\\displaystyle=A\_{11}\\,\\mathrm{d}A\_{21}-A\_{21}\\,\\mathrm{d}A\_{11}+A\_{12}\\,\\mathrm{d}A\_{22}-A\_{22}\\,\\mathrm{d}A\_{12}, |  | (3.5) |
|  | ζ\\displaystyle\\zeta | =A11​d​A12−A12​d​A11+A21​d​A22−A22​d​A21.\\displaystyle=A\_{11}\\,\\mathrm{d}A\_{12}-A\_{12}\\,\\mathrm{d}A\_{11}+A\_{21}\\,\\mathrm{d}A\_{22}-A\_{22}\\,\\mathrm{d}A\_{21}. |  | (3.6) |

Every rotation commutes with JJ, since JJ itself is a rotation. If T⁡(A)=O​A​UTT(A)=OAU^{T}, with
O,U∈S​O​(2)O,U\\in SO(2), then

|     |     |     |     |
| --- | --- | --- | --- |
|  | (T∗​θ)A​(B)\\displaystyle(T^{\*}\\theta)\_{A}(B) | =tr⁡(J​O​A​UT​(O​B​UT)T)=tr⁡(J​A​BT),\\displaystyle=\\operatorname{tr}\\bigl(JOAU^{T}(OBU^{T})^{T}\\bigr)=\\operatorname{tr}(JAB^{T}), |  |
|  | (T∗​ζ)A​(B)\\displaystyle(T^{\*}\\zeta)\_{A}(B) | =tr⁡(O​A​UT​JT​(O​B​UT)T)=tr⁡(A​JT​BT).\\displaystyle=\\operatorname{tr}\\bigl(OAU^{T}J^{T}(OBU^{T})^{T}\\bigr)=\\operatorname{tr}(AJ^{T}B^{T}). |  |

The functions \|A\|2\|A\|^{2} and detA\\det A are invariant as well.
Consequently, α\\alpha and ω\\omega in ( [3.4](https://arxiv.org/html/2608.06367v1#S3.E4 "In Proof. ‣ 3 The correction lemma ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")) are
invariant under left and right multiplication. The form ω\\omega is exact and has homogeneous quadratic coefficients.

Step 2. For A,B∈ℝ2×2A,B\\in\\mathbb{R}^{2\\times 2},

|     |     |     |     |
| --- | --- | --- | --- |
|  | \|A+s​B\|2\\displaystyle\|A+sB\|^{2} | =\|A\|2+2​s​tr⁡(A​BT)+s2​\|B\|2,\\displaystyle=\|A\|^{2}+2s\\operatorname{tr}(AB^{T})+s^{2}\|B\|^{2}, |  |
|  | det(A+s​B)\\displaystyle\\det(A+sB) | =detA+s​tr⁡((cof⁡A)​BT)+s2​detB.\\displaystyle=\\det A+s\\operatorname{tr}\\bigl((\\operatorname{cof}A)B^{T}\\bigr)+s^{2}\\det B. |  |

Differentiating ( [1.3](https://arxiv.org/html/2608.06367v1#S1.E3 "In 1 Introduction ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")) twice gives

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
|  | D2​fγ​(A)​\[B,B\]=\\displaystyle D^{2}f\_{\\gamma}(A)\[B,B\]={} | 8​tr⁡(A​BT)2+4​(\|A\|2−γ​detA)​\|B\|2\\displaystyle 8\\operatorname{tr}(AB^{T})^{2}+4\\bigl(\|A\|^{2}-\\gamma\\det A\\bigr)\|B\|^{2} |  |
|  |  | −8​γ​tr⁡(A​BT)​tr⁡((cof⁡A)​BT)−4​γ\|A\|det2⁡B.\\displaystyle-8\\gamma\\operatorname{tr}(AB^{T})\\operatorname{tr}\\bigl((\\operatorname{cof}A)B^{T}\\bigr)-4\\gamma\|A\|^{2}\\det B. |  | (3.7) |

Step 3.
Fix a point x0∈ℝ2x\_{0}\\in\\mathbb{R}^{2} and constant matrices O,U∈S​O​(2)O,U\\in SO(2). Define

|     |     |     |
| --- | --- | --- |
|  | v~​(y)=O⁡(v⁡(x0+UT​y)−v⁡(x0)).\\widetilde{v}(y)=O\\bigl(v(x\_{0}+U^{T}y)-v(x\_{0})\\bigr). |  |

If A=D​v​(x0)A=Dv(x\_{0}) and Bi=∂iD​v​(x0)B\_{i}=\\partial\_{i}Dv(x\_{0}), then

|     |     |     |     |
| --- | --- | --- | --- |
|  | A~:=D​v~​(0)\\displaystyle\\widetilde{A}:=D\\widetilde{v}(0) | =O​A​UT,\\displaystyle=OAU^{T}, |  |
|  | B~i:=∂iD​v~​(0)\\displaystyle\\widetilde{B}\_{i}:=\\partial\_{i}D\\widetilde{v}(0) | =∑k=12Ui​k​O​Bk​UT.\\displaystyle=\\sum\_{k=1}^{2}U\_{ik}\\,OB\_{k}U^{T}. |  |

The invariance of fγf\_{\\gamma}, the orthogonality of UU, and the
skwe-symmetry of ω\\omega give

|     |     |     |     |
| --- | --- | --- | --- |
|  | ℰγ​(A~,B~1,B~2)\\displaystyle\\mathcal{E}\_{\\gamma}(\\widetilde{A};\\widetilde{B}\_{1},\\widetilde{B}\_{2}) | =ℰγ​(A,B1,B2),\\displaystyle=\\mathcal{E}\_{\\gamma}(A;B\_{1},B\_{2}), |  |
|  | ωA~​(B~1,B~2)\\displaystyle\\omega\_{\\widetilde{A}}(\\widetilde{B}\_{1},\\widetilde{B}\_{2}) | =ωA​(B1,B2).\\displaystyle=\\omega\_{A}(B\_{1},B\_{2}). |  |

By singular value decomposition, there exist O,U∈S​O​(2)O,U\\in SO(2) such that
O​A​UT=diag⁡(σ,τ)OAU^{T}=\\operatorname{diag}(\\sigma,\\tau), with σ≥\|τ\|\\sigma\\geq\|\\tau\|. It is therefore enough to restrict our reasoning to AA having the form Aρ=diag⁡(1,ρ)A\_{\\rho}=\\operatorname{diag}(1,\\rho),
with ρ∈ℝ\\rho\\in\\mathbb{R}.

Step 4.
At x0x\_{0}, we may write

|     |     |     |
| --- | --- | --- |
|  | B1=(ξ1ξ2η1η2),B2=(ξ2ξ3η2η3).B\_{1}=\\begin{pmatrix}\\xi\_{1}&\\xi\_{2}\\\<br>\\eta\_{1}&\\eta\_{2}\\end{pmatrix},\\qquad B\_{2}=\\begin{pmatrix}\\xi\_{2}&\\xi\_{3}\\\<br>\\eta\_{2}&\\eta\_{3}\\end{pmatrix}. |  |

At γ=2/3\\gamma=2/\\sqrt{3}, substitution in ( [3.7](https://arxiv.org/html/2608.06367v1#S3.E7 "In Proof. ‣ 3 The correction lemma ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")) gives

|     |     |     |
| --- | --- | --- |
|  | ℰ2/3​(Aρ,B1,B2)=Q1+Q2,\\mathcal{E}\_{2/\\sqrt{3}}(A\_{\\rho};B\_{1},B\_{2})=Q\_{1}+Q\_{2}, |  |

where Q1Q\_{1} and Q2Q\_{2} are given by

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
|  | Q1​(ρ,ξ1,ξ3,η2)=\\displaystyle Q\_{1}(\\rho;\\xi\_{1},\\xi\_{3},\\eta\_{2})={} | 4​(ρ−3)2​ξ12+4​(1+ρ2−2​ρ3)​ξ32\\displaystyle 4(\\rho-\\sqrt{3})^{2}\\xi\_{1}^{2}+4\\left(1+\\rho^{2}-\\frac{2\\rho}{\\sqrt{3}}\\right)\\xi\_{3}^{2} |  |
|  |  | +4​(2+4​ρ2−8​ρ3)​η22+4​(4​ρ−2​3​(1+ρ2))​ξ1​η2\\displaystyle+4\\left(2+4\\rho^{2}-\\frac{8\\rho}{\\sqrt{3}}\\right)\\eta\_{2}^{2}+4\\bigl(4\\rho-2\\sqrt{3}(1+\\rho^{2})\\bigr)\\xi\_{1}\\eta\_{2} |  |
|  |  | +83​(1+ρ2)​ξ3​η2,\\displaystyle+\\frac{8}{\\sqrt{3}}(1+\\rho^{2})\\xi\_{3}\\eta\_{2}, |  | (3.8) |
|  | Q2​(ρ,η3,η1,ξ2)=\\displaystyle Q\_{2}(\\rho;\\eta\_{3},\\eta\_{1},\\xi\_{2})={} | 4​(1+ρ2−2​ρ3)​η12+4​(4+2​ρ2−8​ρ3)​ξ22\\displaystyle 4\\left(1+\\rho^{2}-\\frac{2\\rho}{\\sqrt{3}}\\right)\\eta\_{1}^{2}+4\\left(4+2\\rho^{2}-\\frac{8\\rho}{\\sqrt{3}}\\right)\\xi\_{2}^{2} |  |
|  |  | +4​(1+3​ρ2−2​3​ρ)​η32+83​(1+ρ2)​η1​ξ2\\displaystyle+4(1+3\\rho^{2}-2\\sqrt{3}\\rho)\\eta\_{3}^{2}+\\frac{8}{\\sqrt{3}}(1+\\rho^{2})\\eta\_{1}\\xi\_{2} |  |
|  |  | +4​(4​ρ−2​3​(1+ρ2))​ξ2​η3.\\displaystyle+4\\bigl(4\\rho-2\\sqrt{3}(1+\\rho^{2})\\bigr)\\xi\_{2}\\eta\_{3}. |  |

Equations ( [3.5](https://arxiv.org/html/2608.06367v1#S3.E5 "In Proof. ‣ 3 The correction lemma ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")) and
( [3.6](https://arxiv.org/html/2608.06367v1#S3.E6 "In Proof. ‣ 3 The correction lemma ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")) give

|     |     |     |     |
| --- | --- | --- | --- |
|  | d​θ\\displaystyle\\mathrm{d}\\theta | =2​(d​A11∧d​A21+d​A12∧d​A22),\\displaystyle=2(\\mathrm{d}A\_{11}\\wedge\\mathrm{d}A\_{21}+\\mathrm{d}A\_{12}\\wedge\\mathrm{d}A\_{22}), |  |
|  | d​ζ\\displaystyle\\mathrm{d}\\zeta | =2​(d​A11∧d​A12+d​A21∧d​A22).\\displaystyle=2(\\mathrm{d}A\_{11}\\wedge\\mathrm{d}A\_{12}+\\mathrm{d}A\_{21}\\wedge\\mathrm{d}A\_{22}). |  |

At AρA\_{\\rho},

|     |     |     |
| --- | --- | --- |
|  | B1B2d​\|A\|22​(ξ1+ρ​η2)2​(ξ2+ρ​η3)d​detAρ​ξ1+η2ρ​ξ2+η3θη1−ρ​ξ2η2−ρ​ξ3ζξ2−ρ​η1ξ3−ρ​η2\\begin{array}\[\]{c\|cc}&B\_{1}&B\_{2}\\\<br>\\hline\\cr\\mathrm{d}\|A\|^{2}&2(\\xi\_{1}+\\rho\\eta\_{2})&2(\\xi\_{2}+\\rho\\eta\_{3})\\\<br>\\mathrm{d}\\det A&\\rho\\xi\_{1}+\\eta\_{2}&\\rho\\xi\_{2}+\\eta\_{3}\\\<br>\\theta&\\eta\_{1}-\\rho\\xi\_{2}&\\eta\_{2}-\\rho\\xi\_{3}\\\<br>\\zeta&\\xi\_{2}-\\rho\\eta\_{1}&\\xi\_{3}-\\rho\\eta\_{2}\\end{array} |  |

Using d⁡(g​ϑ)=d​g∧ϑ+g​d​ϑ\\mathrm{d}(g\\vartheta)=\\mathrm{d}g\\wedge\\vartheta+g\\,\\mathrm{d}\\vartheta, the correction splits as

|     |     |     |
| --- | --- | --- |
|  | ωAρ​(B1,B2)=C1​(ρ,ξ1,ξ3,η2)+C2​(ρ,η3,η1,ξ2),\\omega\_{A\_{\\rho}}(B\_{1},B\_{2})=C\_{1}(\\rho;\\xi\_{1},\\xi\_{3},\\eta\_{2})+C\_{2}(\\rho;\\eta\_{3},\\eta\_{1},\\xi\_{2}), |  |

where

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
|  | C1=\\displaystyle C\_{1}={} | \[−2​ρ​c1+3​ρ​c2+(4+2​ρ2)​c3−ρ2​c4\]​ξ1​ξ3\\displaystyle\\bigl\[-2\\rho c\_{1}+3\\rho c\_{2}+(4+2\\rho^{2})c\_{3}-\\rho^{2}c\_{4}\\bigr\]\\xi\_{1}\\xi\_{3} |  |
|  |  | +\[(4+2​ρ2)​c1−ρ2​c2−2​ρ​c3+3​ρ​c4\]​ξ1​η2\\displaystyle+\\bigl\[(4+2\\rho^{2})c\_{1}-\\rho^{2}c\_{2}-2\\rho c\_{3}+3\\rho c\_{4}\\bigr\]\\xi\_{1}\\eta\_{2} |  |
|  |  | +\[−(2+4​ρ2)​c1+c2+2​ρ​c3−3​ρ​c4\]​ξ3​η2\\displaystyle+\\bigl\[-(2+4\\rho^{2})c\_{1}+c\_{2}+2\\rho c\_{3}-3\\rho c\_{4}\\bigr\]\\xi\_{3}\\eta\_{2} |  |
|  |  | +\[2​ρ​c1−3​ρ​c2−(2+4​ρ2)​c3+c4\]​η22.\\displaystyle+\\bigl\[2\\rho c\_{1}-3\\rho c\_{2}-(2+4\\rho^{2})c\_{3}+c\_{4}\\bigr\]\\eta\_{2}^{2}. |  | (3.9) |

The second block is

|     |     |     |     |
| --- | --- | --- | --- |
|  | C2=\\displaystyle C\_{2}={} | \[−2​ρ​c1+3​ρ​c2+(2+4​ρ2)​c3−c4\]​η1​η3\\displaystyle\\bigl\[-2\\rho c\_{1}+3\\rho c\_{2}+(2+4\\rho^{2})c\_{3}-c\_{4}\\bigr\]\\eta\_{1}\\eta\_{3} |  |
|  |  | +\[−(4+2​ρ2)​c1+ρ2​c2+2​ρ​c3−3​ρ​c4\]​η1​ξ2\\displaystyle+\\bigl\[-(4+2\\rho^{2})c\_{1}+\\rho^{2}c\_{2}+2\\rho c\_{3}-3\\rho c\_{4}\\bigr\]\\eta\_{1}\\xi\_{2} |  |
|  |  | +\[(2+4​ρ2)​c1−c2−2​ρ​c3+3​ρ​c4\]​η3​ξ2\\displaystyle+\\bigl\[(2+4\\rho^{2})c\_{1}-c\_{2}-2\\rho c\_{3}+3\\rho c\_{4}\\bigr\]\\eta\_{3}\\xi\_{2} |  |
|  |  | +\[2​ρ​c1−3​ρ​c2−(4+2​ρ2)​c3+ρ2​c4\]​ξ22.\\displaystyle+\\bigl\[2\\rho c\_{1}-3\\rho c\_{2}-(4+2\\rho^{2})c\_{3}+\\rho^{2}c\_{4}\\bigr\]\\xi\_{2}^{2}. |  |

The ξ32\\xi\_{3}^{2}-coefficient in Q1Q\_{1} is
4​κ​(ρ)4\\kappa(\\rho), and κ⁡(ρ)=1+ρ2−2​ρ3=(ρ−13)2+23>0\\kappa(\\rho)=1+\\rho^{2}-\\frac{2\\rho}{\\sqrt{3}}=\\left(\\rho-\\frac{1}{\\sqrt{3}}\\right)^{2}+\\frac{2}{3}>0.
We impose that the corrected η22\\eta\_{2}^{2}-coefficient be equal
4​κ​(ρ)4\\kappa(\\rho) (this choice makes the eigenvectors of the η2\\eta\_{2}-ξ3\\xi\_{3} minor independent of ρ\\rho). Matching the powers of ρ\\rho in
( [3.9](https://arxiv.org/html/2608.06367v1#S3.E9 "In Proof. ‣ 3 The correction lemma ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")) gives
c3=3,c4=2c\_{3}=3,c\_{4}=2, and 2​c1−3​c2=8​32c\_{1}-3c\_{2}=8\\sqrt{3}.
Therefore, the ξ1​ξ3\\xi\_{1}\\xi\_{3}-coefficient in
Q1+C1Q\_{1}+C\_{1} is 4​(ρ−3)24(\\rho-\\sqrt{3})^{2}.
At
ρ=3\\rho=\\sqrt{3}, the ξ12\\xi\_{1}^{2}-coefficient vanishes. A
nonnegative quadratic form with a zero ξ12\\xi\_{1}^{2}-coefficient cannot
have a nonzero mixed term involving ξ1\\xi\_{1}. The
ξ1​η2\\xi\_{1}\\eta\_{2}-coefficient at ρ=3\\rho=\\sqrt{3} is
8​(c1−3)8(c\_{1}-\\sqrt{3}). Hence we set

|     |     |     |
| --- | --- | --- |
|  | c1=3,c2=−2​3,c3=3,c4=2.c\_{1}=\\sqrt{3},\\qquad c\_{2}=-2\\sqrt{3},\\qquad c\_{3}=3,\\qquad c\_{4}=2. |  |

The corresponding primitive and two-form are

|     |     |     |     |
| --- | --- | --- | --- |
|  | α+\\displaystyle\\alpha\_{+} | =(3​\|A\|2+2​detA)​θ+(3​\|A\|2−2​3​detA)​ζ,\\displaystyle=(\\sqrt{3}\|A\|^{2}+2\\det A)\\theta+(3\|A\|^{2}-2\\sqrt{3}\\det A)\\zeta, |  |
|  | ω+\\displaystyle\\omega\_{+} | =d​α+.\\displaystyle=\\mathrm{d}\\alpha\_{+}. |  |

For these coefficients, ( [3.9](https://arxiv.org/html/2608.06367v1#S3.E9 "In Proof. ‣ 3 The correction lemma ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")) becomes

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
|  | C1=\\displaystyle C\_{1}={} | 4​(ρ−3)2​ξ1​ξ3+4​3​(1+ρ2)​(ξ1​η2−ξ3​η2)−12​(ρ−13)2​η22.\\displaystyle 4(\\rho-\\sqrt{3})^{2}\\xi\_{1}\\xi\_{3}+4\\sqrt{3}(1+\\rho^{2})(\\xi\_{1}\\eta\_{2}-\\xi\_{3}\\eta\_{2})-12\\left(\\rho-\\frac{1}{\\sqrt{3}}\\right)^{2}\\eta\_{2}^{2}. |  | (3.10) |

Adding ( [3.10](https://arxiv.org/html/2608.06367v1#S3.E10 "In Proof. ‣ 3 The correction lemma ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")) to ( [3.8](https://arxiv.org/html/2608.06367v1#S3.E8 "In Proof. ‣ 3 The correction lemma ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")), we can write the corrected
block directly as

|     |     |     |
| --- | --- | --- |
|  | Q1+C1=4​(ξ1ξ3η2)​M1​(ρ)​(ξ1ξ3η2),Q\_{1}+C\_{1}=4\\begin{pmatrix}\\xi\_{1}&\\xi\_{3}&\\eta\_{2}\\end{pmatrix}M\_{1}(\\rho)\\begin{pmatrix}\\xi\_{1}\\\<br>\\xi\_{3}\\\<br>\\eta\_{2}\\end{pmatrix}, |  |

where

|     |     |     |
| --- | --- | --- |
|  | M1​(ρ)=((ρ−3)212​(ρ−3)22​ρ−32​(1+ρ2)12​(ρ−3)21+ρ2−2​ρ3−1+ρ22​32​ρ−32​(1+ρ2)−1+ρ22​31+ρ2−2​ρ3).M\_{1}(\\rho)=\\begin{pmatrix}(\\rho-\\sqrt{3})^{2}&\\frac{1}{2}(\\rho-\\sqrt{3})^{2}&2\\rho-\\frac{\\sqrt{3}}{2}(1+\\rho^{2})\\\\[2.0pt\]<br>\\frac{1}{2}(\\rho-\\sqrt{3})^{2}&1+\\rho^{2}-\\frac{2\\rho}{\\sqrt{3}}&-\\frac{1+\\rho^{2}}{2\\sqrt{3}}\\\\[2.0pt\]<br>2\\rho-\\frac{\\sqrt{3}}{2}(1+\\rho^{2})&-\\frac{1+\\rho^{2}}{2\\sqrt{3}}&1+\\rho^{2}-\\frac{2\\rho}{\\sqrt{3}}\\end{pmatrix}. |  |

The principal minors of M1​(ρ)M\_{1}(\\rho) are

|     |     |     |     |
| --- | --- | --- | --- |
|  | Δ1\\displaystyle\\Delta\_{1} | =(ρ−3)2,\\displaystyle=(\\rho-\\sqrt{3})^{2}, |  |
|  | Δ2\\displaystyle\\Delta\_{2} | =34​(ρ−3)2​\[(ρ−39)2+827\],\\displaystyle=\\frac{3}{4}(\\rho-\\sqrt{3})^{2}\\left\[\\left(\\rho-\\frac{\\sqrt{3}}{9}\\right)^{2}+\\frac{8}{27}\\right\], |  |
|  | Δ3\\displaystyle\\Delta\_{3} | =detM1​(ρ)=16​(ρ−3)2​(1−ρ2)2.\\displaystyle=\\det M\_{1}(\\rho)=\\frac{1}{6}(\\rho-\\sqrt{3})^{2}(1-\\rho^{2})^{2}. |  |

If ρ∉{−1,1,3}\\rho\\notin\\{-1,1,\\sqrt{3}\\}, all three are strictly positive,
so M1​(ρ)>0M\_{1}(\\rho)>0. Since
M1​(ρ)M\_{1}(\\rho) depends continuously on ρ\\rho and the set of
positive semidefinite matrices is closed, it follows at the three
critical values as well that M1​(ρ)≥0M\_{1}(\\rho)\\geq 0. Therefore

|     |     |     |
| --- | --- | --- |
|  | Q1+C1≥0for every ​ρ,ξ1,ξ3,η2∈ℝ.Q\_{1}+C\_{1}\\geq 0\\qquad\\text{for every }\\rho,\\xi\_{1},\\xi\_{3},\\eta\_{2}\\in\\mathbb{R}. |  |

For the second block, Q2+C2Q\_{2}+C\_{2}, we do not need to repeat the previous calculations. Indeed, the transformation in Step 3 with O=U=JO=U=J
is

|     |     |     |
| --- | --- | --- |
|  | Aρ⟼ρA1/ρ,ρ≠0,(ξ1,ξ3,η2)⟼(−η3,−η1,−ξ2),(η3,η1,ξ2)⟼(ξ1,ξ3,η2).\\begin{gathered}A\_{\\rho}\\longmapsto\\rho A\_{1/\\rho},\\qquad\\rho\\neq 0,\\\<br>(\\xi\_{1},\\xi\_{3},\\eta\_{2})\\longmapsto(-\\eta\_{3},-\\eta\_{1},-\\xi\_{2}),\\\<br>(\\eta\_{3},\\eta\_{1},\\xi\_{2})\\longmapsto(\\xi\_{1},\\xi\_{3},\\eta\_{2}).\\end{gathered} |  |

Thus, setting ξ1=ξ3=η2=0\\xi\_{1}=\\xi\_{3}=\\eta\_{2}=0, invariance and degree-two
homogeneity in AA give

|     |     |     |     |
| --- | --- | --- | --- |
|  |  | Q2​(ρ,η3,η1,ξ2)+C2​(ρ,η3,η1,ξ2)\\displaystyle Q\_{2}(\\rho;\\eta\_{3},\\eta\_{1},\\xi\_{2})+C\_{2}(\\rho;\\eta\_{3},\\eta\_{1},\\xi\_{2}) |  |
|  |  | =ρ2​\[Q1​(1/ρ,η3,η1,ξ2)+C1​(1/ρ,η3,η1,ξ2)\]≥0,ρ≠0.\\displaystyle\\qquad=\\rho^{2}\\bigl\[Q\_{1}(1/\\rho;\\eta\_{3},\\eta\_{1},\\xi\_{2})+C\_{1}(1/\\rho;\\eta\_{3},\\eta\_{1},\\xi\_{2})\\bigr\]\\geq 0,\\qquad\\rho\\neq 0. |  |

The three minus signs have disappeared because all terms are
quadratic monomials. At ρ=0\\rho=0 the non-negativity follows by continuity.

∎

## Appendix A The invariant quartic cone

In this appendix we briefly record how the argument for the
Dacorogna–Marcellini family extends to prove
Theorem [2](https://arxiv.org/html/2608.06367v1#Thmtheorem2 "Theorem 2. ‣ 1 Introduction ‣ Quasiconvexity for the Dacorogna–Marcellini Energy"). Set

|     |     |     |
| --- | --- | --- |
|  | s⁡(F)=\|F\|2,d⁡(F)=detF.s(F)=\|F\|^{2},\\qquad d(F)=\\det F. |  |

###### Proof of Theorem [2](https://arxiv.org/html/2608.06367v1\#Thmtheorem2 "Theorem 2. ‣ 1 Introduction ‣ Quasiconvexity for the Dacorogna–Marcellini Energy").

_Invariant representation._
We first show that every homogeneous quartic polynomial satisfying the
invariance assumption in Theorem [2](https://arxiv.org/html/2608.06367v1#Thmtheorem2 "Theorem 2. ‣ 1 Introduction ‣ Quasiconvexity for the Dacorogna–Marcellini Energy") has a
unique representation of the form

|     |     |     |     |
| --- | --- | --- | --- |
|  | Q⁡(F)=a​s​(F)2+b​s​(F)​d​(F)+c​d​(F)2.Q(F)=as(F)^{2}+bs(F)d(F)+cd(F)^{2}. |  | (A.1) |

Let

|     |     |     |
| --- | --- | --- |
|  | q⁡(x,y)=Q⁡(diag⁡(x,y)).q(x,y)=Q(\\operatorname{diag}(x,y)). |  |

Since QQ is homogeneous of degree four, qq is a homogeneous
quartic polynomial in xx and yy. Moreover, with

|     |     |     |
| --- | --- | --- |
|  | J=(0−110),J​diag⁡(x,y)​JT=diag⁡(y,x),J=\\begin{pmatrix}0&-1\\\<br>1&0\\end{pmatrix},\\qquad J\\operatorname{diag}(x,y)J^{T}=\\operatorname{diag}(y,x), |  |

and hence the rotational invariance of QQ gives
q⁡(x,y)=q⁡(y,x)q(x,y)=q(y,x). Every symmetric homogeneous quartic in two
variables has the form

|     |     |     |
| --- | --- | --- |
|  | q⁡(x,y)=A⁡(x4+y4)+B⁡(x3​y+x​y3)+C​x2​y2.q(x,y)=A(x^{4}+y^{4})+B(x^{3}y+xy^{3})+Cx^{2}y^{2}. |  |

On diagonal matrices, s=x2+y2s=x^{2}+y^{2} and d=x​yd=xy, so

|     |     |     |
| --- | --- | --- |
|  | x4+y4=s2−2​d2,x3​y+x​y3=s​d,x2​y2=d2.x^{4}+y^{4}=s^{2}-2d^{2},\\qquad x^{3}y+xy^{3}=sd,\\qquad x^{2}y^{2}=d^{2}. |  |

Thus ( [A.1](https://arxiv.org/html/2608.06367v1#A1.E1 "In Proof of Theorem . ‣ Appendix A The invariant quartic cone ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")) holds on every diagonal matrix.
Every matrix F∈ℝ2×2F\\in\\mathbb{R}^{2\\times 2} can be brought to a signed diagonal matrix by
proper rotations on the left and right. Since both sides of
( [A.1](https://arxiv.org/html/2608.06367v1#A1.E1 "In Proof of Theorem . ‣ Appendix A The invariant quartic cone ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")) are invariant under these rotations,
the identity holds for every FF. Finally, s2,s​d,d2s^{2},sd,d^{2} are
linearly independent already on diagonal matrices, which proves
uniqueness.

_Rank-one convexity._
We next determine rank-one convexity. By the rotational invariance it
is enough to test the direction

|     |     |     |
| --- | --- | --- |
|  | E11=(1000).E\_{11}=\\begin{pmatrix}1&0\\\<br>0&0\\end{pmatrix}. |  |

For
A=(xyzw)A=\\left(\\begin{smallmatrix}x&y\\\
z&w\\end{smallmatrix}\\right), direct
differentiation gives

|     |     |     |
| --- | --- | --- |
|  | D2​Q​(A)​\[E11,E11\]=12​a​x2+6​b​x​w+(4​a+2​c)​w2+4​a​(y2+z2)−2​b​y​z.D^{2}Q(A)\[E\_{11},E\_{11}\]=12ax^{2}+6bxw+(4a+2c)w^{2}+4a(y^{2}+z^{2})-2byz. |  |

Thus this expression is nonnegative for every AA if and only if

|     |     |     |
| --- | --- | --- |
|  | (12​a3​b3​b4​a+2​c)≥0,(4​a−b−b4​a)≥0.\\begin{pmatrix}12a&3b\\\<br>3b&4a+2c\\end{pmatrix}\\geq 0,\\qquad\\begin{pmatrix}4a&-b\\\<br>-b&4a\\end{pmatrix}\\geq 0. |  |

Equivalently, either

|     |     |     |     |
| --- | --- | --- | --- |
|  | a>0,\|b\|≤4​a,c≥−2​a+3​b28​a,a>0,\\qquad\|b\|\\leq 4a,\\qquad c\\geq-2a+\\frac{3b^{2}}{8a}, |  | (A.2) |

or a=b=0a=b=0 and c≥0c\\geq 0. By the Legendre–Hadamard
characterization ( [1.2](https://arxiv.org/html/2608.06367v1#S1.E2 "In 1 Introduction ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")), these conditions
describe the full rank-one convex cone.

_Reduction to the boundary family._
It remains to prove sufficiency for quasiconvexity. Suppose first that
a>0a>0, and set

|     |     |     |
| --- | --- | --- |
|  | t=b4​a,μ=c+2​a−3​b28​a.t=\\frac{b}{4a},\\qquad\\mu=c+2a-\\frac{3b^{2}}{8a}. |  |

Condition ( [A.2](https://arxiv.org/html/2608.06367v1#A1.E2 "In Proof of Theorem . ‣ Appendix A The invariant quartic cone ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")) says that \|t\|≤1\|t\|\\leq 1 and
μ≥0\\mu\\geq 0, and gives the decomposition

|     |     |     |     |
| --- | --- | --- | --- |
|  | Q=a​Wt+μ​d2,Wt=s2+4​t​s​d+(6​t2−2)​d2.Q=aW\_{t}+\\mu d^{2},\\qquad W\_{t}=s^{2}+4tsd+(6t^{2}-2)d^{2}. |  | (A.3) |

The term d2d^{2} is polyconvex, hence quasiconvex. We only have to
consider WtW\_{t}.

_Quasiconvexity of the boundary family._
We use the invariant one-forms θ\\theta and ζ\\zeta defined in
( [3.2](https://arxiv.org/html/2608.06367v1#S3.E2 "In Proof. ‣ 3 The correction lemma ‣ Quasiconvexity for the Dacorogna–Marcellini Energy"))–( [3.3](https://arxiv.org/html/2608.06367v1#S3.E3 "In Proof. ‣ 3 The correction lemma ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")). Define the cubic
one-form and its exact differential by

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
|  | αt\\displaystyle\\alpha\_{t} | =\[−3​t​s+6​(1−2​t2)​d\]​θ+\[3​s+6​t​d\]​ζ,\\displaystyle=\[-3ts+6(1-2t^{2})d\]\\theta+\[3s+6td\]\\zeta, |  | (A.4) |
|  | ωt\\displaystyle\\omega\_{t} | =d​αt.\\displaystyle=\\mathrm{d}\\alpha\_{t}. |  |

Both αt\\alpha\_{t} and ωt\\omega\_{t} are invariant under proper rotations
on the left and right.

By the same argument used in Step 3 of the proof of
Lemma [4](https://arxiv.org/html/2608.06367v1#Thmtheorem4 "Lemma 4. ‣ 3 The correction lemma ‣ Quasiconvexity for the Dacorogna–Marcellini Energy"), it suffices to take
A=Aρ=diag⁡(1,ρ)A=A\_{\\rho}=\\operatorname{diag}(1,\\rho). At the point under consideration,
write the derivative matrices as in the main proof:

|     |     |     |
| --- | --- | --- |
|  | B1=(ξ1ξ2η1η2),B2=(ξ2ξ3η2η3).B\_{1}=\\begin{pmatrix}\\xi\_{1}&\\xi\_{2}\\\<br>\\eta\_{1}&\\eta\_{2}\\end{pmatrix},\\qquad B\_{2}=\\begin{pmatrix}\\xi\_{2}&\\xi\_{3}\\\<br>\\eta\_{2}&\\eta\_{3}\\end{pmatrix}. |  |

Put

|     |     |     |
| --- | --- | --- |
|  | L=1+t​ρ,M=t+ρ,δ=1−t2.L=1+t\\rho,\\qquad M=t+\\rho,\\qquad\\delta=1-t^{2}. |  |

Differentiating WtW\_{t} and ( [A.4](https://arxiv.org/html/2608.06367v1#A1.E4 "In Proof of Theorem . ‣ Appendix A The invariant quartic cone ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")), and collecting
squares, gives

|     |     |     |     |
| --- | --- | --- | --- |
|  |  | D2​Wt​(Aρ)​\[B1,B1\]+D2​Wt​(Aρ)​\[B2,B2\]+(ωt)Aρ​(B1,B2)\\displaystyle D^{2}W\_{t}(A\_{\\rho})\[B\_{1},B\_{1}\]+D^{2}W\_{t}(A\_{\\rho})\[B\_{2},B\_{2}\]+(\\omega\_{t})\_{A\_{\\rho}}(B\_{1},B\_{2}) |  |
|  |  | =3​(2​L​ξ1+L​ξ3+M​η2)2+(L​ξ3−M​η2)2+4​δ​(ρ​ξ3−η2)2\\displaystyle={}3(2L\\xi\_{1}+L\\xi\_{3}+M\\eta\_{2})^{2}+(L\\xi\_{3}-M\\eta\_{2})^{2}+4\\delta(\\rho\\xi\_{3}-\\eta\_{2})^{2} |  |
|  |  | +3​(L​ξ2+M​η1+2​M​η3)2+(L​ξ2−M​η1)2+4​δ​(ρ​ξ2−η1)2.\\displaystyle\\quad+3(L\\xi\_{2}+M\\eta\_{1}+2M\\eta\_{3})^{2}+(L\\xi\_{2}-M\\eta\_{1})^{2}+4\\delta(\\rho\\xi\_{2}-\\eta\_{1})^{2}. |  |

This is nonnegative because \|t\|≤1\|t\|\\leq 1. The same covariance and
homogeneity argument gives the corresponding inequality for every
A∈ℝ2×2A\\in\\mathbb{R}^{2\\times 2}.

Now let v⁡(x)=F​x+ψ⁡(x)v(x)=Fx+\\psi(x), with ψ\\psi in the Schwartz class.
Exactness and ( [3.1](https://arxiv.org/html/2608.06367v1#S3.E1 "In 3 The correction lemma ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")) imply

|     |     |     |
| --- | --- | --- |
|  | ∫ℝ2(ωt)D​v​(∂1D​v,∂2D​v)​𝑑x=0.\\int\_{\\mathbb{R}^{2}}(\\omega\_{t})\_{Dv}(\\partial\_{1}Dv,\\partial\_{2}Dv)\\,\\mathrm{d}x=0. |  |

After integration, the pointwise inequality therefore yields

|     |     |     |
| --- | --- | --- |
|  | ∫ℝ2∑j=12D2​Wt​(D​v)​\[∂jD​v,∂jD​v\],𝑑x≥0.\\int\_{\\mathbb{R}^{2}}\\sum\_{j=1}^{2}D^{2}W\_{t}(Dv)\[\\partial\_{j}Dv,\\partial\_{j}Dv\],\\mathrm{d}x\\geq 0. |  |

The proof of Lemma [3](https://arxiv.org/html/2608.06367v1#Thmtheorem3 "Lemma 3. ‣ 2 Monotonicity under heat flow ‣ Quasiconvexity for the Dacorogna–Marcellini Energy") uses only that the integrand is
a homogeneous quartic, so it applies verbatim and shows that WtW\_{t}
is quasiconvex. Hence ( [A.3](https://arxiv.org/html/2608.06367v1#A1.E3 "In Proof of Theorem . ‣ Appendix A The invariant quartic cone ‣ Quasiconvexity for the Dacorogna–Marcellini Energy")) is
quasiconvex. In the remaining case a=b=0a=b=0, one has
Q=c​d2Q=cd^{2} with c≥0c\\geq 0, which was already covered above.

∎

## References

- \[1\]
J.-J. Alibert and B. Dacorogna,

An example of a quasiconvex function that is not polyconvex in
two dimensions,

_Arch. Rational Mech. Anal._ 117 (1992),
155–166,

[doi:10.1007/BF00387763](https://doi.org/10.1007/BF00387763 "").

- \[2\]
K. Astala, D. Faraco, A. Guerra, A. Koski, and J. Kristensen,

The local Burkholder functional, quasiconvexity and geometric
function theory,

arXiv:2309.03495 (2023),

[arXiv:2309.03495](https://arxiv.org/abs/2309.03495 "").

- \[3\]
K. Astala, T. Iwaniec, I. Prause, and E. Saksman,

Burkholder integrals, Morrey’s problem and quasiconformal
mappings,

_J. Amer. Math. Soc._ 25 (2012), no. 2,
507–531,

[doi:10.1090/S0894-0347-2011-00718-2](https://doi.org/10.1090/S0894-0347-2011-00718-2 "").

- \[4\]
J. M. Ball,

Convexity conditions and existence theorems in nonlinear
elasticity,

_Arch. Rational Mech. Anal._ 63 (1976/77),
337–403,

[doi:10.1007/BF00279992](https://doi.org/10.1007/BF00279992 "").

- \[5\]
B. Dacorogna,

_Direct Methods in the Calculus of Variations_,

second ed., Applied Mathematical Sciences, vol. 78, Springer,
New York, 2008,

[doi:10.1007/978-0-387-55249-1](https://doi.org/10.1007/978-0-387-55249-1 "").

- \[6\]
B. Dacorogna, J. Douchet, W. Gangbo, and J. Rappaz,

Some examples of rank one convex functions in dimension two,

_Proc. Roy. Soc. Edinburgh Sect. A_ 114
(1990), 135–150,

[doi:10.1017/S0308210500024318](https://doi.org/10.1017/S0308210500024318 "").

- \[7\]
B. Dacorogna and J.-P. Haeberly,

Some numerical methods for the study of the convexity notions
arising in the calculus of variations,

_ESAIM Math. Model. Numer. Anal._ 32 (1998),
no. 2, 153–175,

[doi:10.1051/m2an/1998320201531](https://doi.org/10.1051/m2an/1998320201531 "").

- \[8\]
B. Dacorogna and H. Koshigoe,

On the different notions of convexity for rotationally
invariant functions,

_Ann. Fac. Sci. Toulouse Math. (6)_ 2 (1993),
no. 2, 163–184,

[doi:10.5802/afst.762](https://doi.org/10.5802/afst.762 "").

- \[9\]
B. Dacorogna and P. Marcellini,

A counterexample in the vectorial calculus of variations,

in _Material Instabilities in Continuum Mechanics_
_(Edinburgh, 1985–1986)_, J. M. Ball (ed.), Oxford Sci. Publ., Oxford
Univ. Press, New York, 1988, 77–83.

- \[10\]
X. Dong and K. Enakoutsa,

Some numerical simulations based on Dacorogna example
functions in favor of Morrey conjecture,

arXiv:2211.11194 (2022),

[arXiv:2211.11194](https://arxiv.org/abs/2211.11194 "").

- \[11\]
D. Faraco and L. Székelyhidi, Jr.,

Tartar’s conjecture and localization of the quasiconvex hull
in ℝ2×2\\mathbb{R}^{2\\times 2},

_Acta Math._ 200 (2008), no. 2, 279–305,

[doi:10.1007/s11511-008-0028-1](https://doi.org/10.1007/s11511-008-0028-1 "").

- \[12\]
P.-A. Gremaud,

Numerical optimization and quasiconvexity,

_European J. Appl. Math._ 6 (1995), no. 1,
69–82,

[doi:10.1017/S0956792500001674](https://doi.org/10.1017/S0956792500001674 "").

- \[13\]
A. Guerra and J. Kristensen,

Automatic quasiconvexity of homogeneous isotropic rank-one
convex integrands,

_Arch. Rational Mech. Anal._ 245 (2022), no. 1,
479–500,

[doi:10.1007/s00205-022-01792-2](https://doi.org/10.1007/s00205-022-01792-2 "").

- \[14\]
S. Gutiérrez and J. Villavicencio,

An optimization algorithm applied to the Morrey conjecture in
nonlinear elasticity,

_Internat. J. Solids Structures_ 44 (2007),
no. 10, 3177–3186,

[doi:10.1016/j.ijsolstr.2006.09.017](https://doi.org/10.1016/j.ijsolstr.2006.09.017 "").

- \[15\]
T. L. J. Harris, B. Kirchheim, and C.-C. Lin,

Two-by-two upper triangular matrices and Morrey’s conjecture,

_Calc. Var. Partial Differential Equations_ 57
(2018), no. 3, article 73,

[doi:10.1007/s00526-018-1360-8](https://doi.org/10.1007/s00526-018-1360-8 "").

- \[16\]
B. Kirchheim and L. Székelyhidi, Jr.,

On the gradient set of Lipschitz maps,

_J. Reine Angew. Math._ 625 (2008), 215–229,

[doi:10.1515/CRELLE.2008.095](https://doi.org/10.1515/CRELLE.2008.095 "").

- \[17\]
R. J. Martin, I.-D. Ghiba, and P. Neff,

Rank-one convexity implies polyconvexity for isotropic,
objective and isochoric elastic energies in the two-dimensional case,

_Proc. Roy. Soc. Edinburgh Sect. A_ 147 (2017),
no. 3, 571–597,

[doi:10.1017/S0308210516000275](https://doi.org/10.1017/S0308210516000275 "").

- \[18\]
D. Matthes, R. J. McCann, and G. Savaré,

A family of nonlinear fourth order equations of gradient flow
type,

_Comm. Partial Differential Equations_ 34
(2009), 1352–1397,

[doi:10.1080/03605300903296256](https://doi.org/10.1080/03605300903296256 "").

- \[19\]
C. B. Morrey, Jr.,

Quasi-convexity and the lower semicontinuity of multiple
integrals,

_Pacific J. Math._ 2 (1952), 25–53,

[doi:10.2140/pjm.1952.2.25](https://doi.org/10.2140/pjm.1952.2.25 "").

- \[20\]
S. Müller,

Rank-one convexity implies quasiconvexity on diagonal
matrices,

_Int. Math. Res. Not._ 1999, no. 20, 1087–1095,

[doi:10.1155/S1073792899000598](https://doi.org/10.1155/S1073792899000598 "").

- \[21\]
V. Šverák,

Rank-one convexity does not imply quasiconvexity,

_Proc. Roy. Soc. Edinburgh Sect. A_ 120
(1992), 185–189,

[doi:10.1017/S0308210500015080](https://doi.org/10.1017/S0308210500015080 "").

- \[22\]
L. Székelyhidi, Jr.,

Rank-one convex hulls in ℝ2×2\\mathbb{R}^{2\\times 2},

_Calc. Var. Partial Differential Equations_ 22
(2005), no. 3, 253–281,

[doi:10.1007/s00526-004-0272-y](https://doi.org/10.1007/s00526-004-0272-y "").

- \[23\]
L. Székelyhidi, Jr.,

On quasiconvex hulls in symmetric 2×22\\times 2 matrices,

_Ann. Inst. H. Poincaré C Anal. Non Linéaire_ 23 (2006), no. 6, 865–876,

[doi:10.1016/j.anihpc.2005.11.001](https://doi.org/10.1016/j.anihpc.2005.11.001 "").

- \[24\]
J. Voss, R. J. Martin, I.-D. Ghiba, and P. Neff,

Morrey’s conjecture for the planar volumetric–isochoric split:
least rank-one convex energy functions,

_J. Nonlinear Sci._ 32 (2022), article 76,

[doi:10.1007/s00332-022-09827-4](https://doi.org/10.1007/s00332-022-09827-4 "").

- \[25\]
J. Voss, R. J. Martin, O. Sander, S. Kumar, D. M. Kochmann, and
P. Neff,

Numerical approaches for investigating quasiconvexity in the
context of Morrey’s conjecture,

_J. Nonlinear Sci._ 32 (2022), article 77,

[doi:10.1007/s00332-022-09820-x](https://doi.org/10.1007/s00332-022-09820-x "").
