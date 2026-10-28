The continuation now has **a certified model from coarse observations, a stronger executed baseline, and an exponential limit on generic acquisition**. Together they change where I would place the scientific effort.

The strongest new construction preserves hidden memory and learns from fresh preparations plus live/absorbed reports. It certifies future compositions of operations on a countably infinite source with no strict global contraction gap and infinite mean lifetime. The subsequent cost attack shows that even four controls and a known strict gap can require exponentially many experiments for a reusable predictor.

I have therefore moved the central question beyond acquiring a particular residual form:

> **What experimentally checkable structure makes a small representation sufficient for future compositions—and what does acquiring that structure cost?**

The complete proofs, executable work, observations, corrections, and scoped internal reviews are in [:chatgpt-content-reference{index="4"}](https://chatgpt.com/library?file_id=libfile_afa015edae2c8191ab7781fc23d9f0e3&account_id=personal).

## 1. A completed capability from coarse observations

The new source has two noncommuting operations. Its hidden state space consists of a fast two-state component and countably many progressively slower components. Every component has positive preparation probability. Each operation eventually absorbs a prepared trajectory, but the source’s mean lifetime is infinite and its operator norm is exactly one.

The learner receives only the controls it chose and whether the source remains alive. It receives no microscopic state labels, hidden dimension, transition matrices, or strict contraction bound. Every fresh preparation is charged. A surviving coarse label is never treated as a reset.

Two independently executed procedures now certify the same target: total-survival probability for **every finite fixed switching word**, to absolute error at most \(1/16\).

| Complete resource | Fixed control tapes plus lifetime acquisition | Fresh adaptive prefix acquisition |
|---|---:|---:|
| Primitive applications | 1,086,180 | **458,449** |
| Live/absorbed observations | 1,086,180 | **458,449** |
| Fresh preparations | 540,672 | **255,220** |
| Retained prefix nodes | 84 | **38** |
| Maximum retained prefix length | 7 | **5** |
| Uniform absolute survival error | \(1/16\) | \(1/16\) |

Each acquisition has its own false-certificate probability bound of \(0.001\), under its declared preparation and observation premises. These are executed software trajectories with exact rational acceptance checks.

The first dataset also certifies a compact, ordinary two-state model. Moment realization from its observed counts proposes

\[
T_0=
\begin{pmatrix}
0.632329&0.119580\\
0.119580&0.131730
\end{pmatrix},
\qquad
T_1=
\begin{pmatrix}
0.497697&0.070398\\
0.070398&0.112506
\end{pmatrix}.
\]

Starting this model uniformly and reading its total surviving mass gives

\[
\boxed{
\sup_w |f_{\mathrm{source}}(w)-f_{\mathrm{model}}(w)|
\le 0.062335817204 .
}
\]

The certificate covers words selected after inspecting the acquisition. The two-state dimension is a property of the approximation; the actual source remains infinite. This closes an approximate model-construction obligation that the earlier positive memory witness had left open. The ordinary proof and acquisition are in :chatgpt-content-reference{index="5"}[COARSE_SWITCHING_THEORY.md](producer-workspace/COARSE_SWITCHING_THEORY.md).

The adaptive procedure is the better executed route for the stated scalar prediction task. It saves **627,731 source applications** against the fixed-tape pipeline. Its representation is a small prefix predictor, with a bounded terminal extrapolation, rather than the same two-state matrix model. That distinction matters when comparing capabilities and costs.

## 2. How repetition experiments can control every switching tail

The useful structural premise is a **common reversible preparation**.

In symmetric coordinates, let the operations \(A_i\) be selfadjoint, positivity-preserving contractions. Let the preparation/readout vector \(v>0\) have unit norm and satisfy

\[
A_i v\le v
\quad\text{for every }i.
\]

For a countable classical source, \(v_j^2\) is the preparation distribution. The condition corresponds to reversible live dynamics with irreversible loss. It is a physical access premise, rather than a conclusion drawn from a few observed lifetimes.

For a chronological word \(w\),

\[
f(w)=\langle v,A_wv\rangle
\]

is its survival probability. Positivity ensures that every reachable vector remains in the same order interval:

\[
0\le A_wv\le v.
\]

This turns a scalar measurement into a uniform statement. For any integer \(m\ge1\),

\[
\sup_{|x|\le v}\|A_i^m x\|^2
=
\|A_i^m v\|^2
=
f(i^{2m}).
\]

The maximum is attained at the preparation vector itself. Thus repeated-operation survival measures the coefficient needed to control every vector in the relevant order interval.

The elementary spectral inequality

\[
1-\lambda^{2m}\le m(1-\lambda^2),
\qquad |\lambda|\le1,
\]

then gives

\[
\|x\|^2
\le
m\bigl(\|x\|^2-\|A_i x\|^2\bigr)
+
f(i^{2m})\left\|x/v\right\|_\infty^2 .
\]

Suppose simultaneous observed bounds establish

\[
s\ge\max_i f(i^{2m}).
\]

Applying that inequality at whichever action is selected next yields, for every word of length \(h\),

\[
\|A_wv\|^2
\le
z_h
:=
s+\left(1-\frac1m\right)^h(1-s).
\]

There is a useful further improvement for the scalar response. Split a word into two halves, reverse one half using selfadjointness, and apply Cauchy–Schwarz. For every word of length \(2h\),

\[
\boxed{f(w)\le z_h.}
\]

The limiting floor is \(s\), which is sharper than the \(\sqrt{s}\) floor obtained from a one-sided norm estimate.

In the executed acquisition, 8,192 capped lifetime trials per action established

\[
m=4,
\qquad
s=0.039498905686.
\]

The resulting bound certifies survival below \(1/16\) for **every switching word of length at least 26**. No estimate of the slowest hidden relaxation time enters that calculation.

This is an observable specialization of established weak-Poincaré machinery. The general passage from a functional inequality and a nonexpansive auxiliary norm to decay is already present in the primary literature, including Andrieu, Lee, Power and Wang. The contribution being assessed here is the finite native acquisition of a common numerical coefficient and its simultaneous use for the switched language. Historical priority for that complete contract has not been established. :chatgpt-content-reference{index="0"}

The assumptions are substantive. The saved counterexamples show that removing selfadjointness or the common order relation can allow persistent switched behavior even though every individual operation appears to decay.

## 3. Finite coverage turns that control into a reusable predictor

The remaining response information comes from mixed words.

For survival probabilities, irreversible absorption gives

\[
f(wu)\le f(w)
\]

for every continuation \(u\). Therefore, once an observed upper bound establishes \(f(w)\le\epsilon\), every extension of that prefix is also small.

A finite tree can exploit this:

- At retained branch words, keep a confidence interval for the actual response.
- At terminal prefixes, keep a sufficiently small survival upper bound.
- Require every nonterminal node to contain a child for every available action.

Every finite word either ends at a retained branch or extends a terminal prefix. That finite check covers the entire infinite language.

The same cover can certify a fitted positive model. At each branch, compare its prediction with both interval endpoints. At each terminal prefix, bound both actual and model survival. Both remain nonnegative and decrease under any suffix, so every later error is bounded by the larger prefix survival upper. This is how the ordinary two-state proposal obtained its every-word certificate.

The stronger adaptive procedure uses a slightly different terminal prediction. If a prefix has survival upper \(U\le2\epsilon\), it predicts \(U/2\) on that prefix and every extension. Every possible later survival lies in \([0,U]\), so the error is at most \(\epsilon\). This permits earlier termination than predicting zero.

That is an important reason the familiar adaptive method wins the executed comparison. It also exposes exactly what the accuracy target permits: a terminal prediction may stay at a small nonzero floor forever, even though the source eventually absorbs.

The guarantee concerns **unconditional absolute survival probabilities**. It provides no uniform relative-error guarantee for rare events, no certificate of normalized survivor states, and no control of lifetime moments. In fact, the certified finite model has finite mean lifetime while the actual source’s mean is infinite.

The comparison and its complete accounting are in :chatgpt-content-reference{index="6"}[ADAPTIVE_COARSE_COMPARISON.md](producer-workspace/ADAPTIVE_COARSE_COMPARISON.md).

## 4. Why inverse dissipation ceased to be the universal target

The earlier successful route centered on

\[
Q=D^*(I-A^2)^{-1}D,
\qquad D=AV-VT.
\]

That remains a valuable certificate when its form-domain and acquisition premises hold. The new coarse-interface work proves a serious limitation: **this quantity can be unbounded or statistically unacquirable while every requested output remains uniformly easy to approximate.**

A simple rare-component calculation shows the problem. Give a very slow hidden component preparation mass \(\eta\), with survival eigenvalue \(\lambda\) close to one. For a scalar fitted coefficient \(t<1\), its contribution to the centered inverse form is

\[
\eta\frac{(\lambda-t)^2}{1-\lambda^2}.
\]

This grows without bound as \(\lambda\uparrow1\). Yet changing that component changes every scalar word response by at most \(\eta\).

The statistical obstruction is equally direct. With finitely many preparations, an arbitrarily rare component can remain unvisited with arbitrarily high probability. Until it is prepared, the entire adaptive transcript—including very long words, stopping decisions and resets—can be identical to that of a benign source. Finite coarse observations therefore cannot supply a uniformly sound finite upper bound for the unrestricted centered form with useful emission probability.

The new infinite fixture makes the separation exact. Its slow blocks have preparation weights and activation rates satisfying

\[
\frac{p_n}{e_n}=\frac1{128}.
\]

For every finite word-feature embedding with strictly stable computational maps, some residual direction retains a nonzero leading component on all sufficiently slow blocks. Each contributes a positive amount to the inverse form; their sum diverges. The coarse survival cover still succeeds.

This changes the representation choice. A small perturbation in the observable task can destroy an internal energy certificate without significantly changing any requested response. The error metric therefore has to guide which physical quantity we try to acquire.

It also explains why the earlier boundary result survives. Genuine boundary states and observed irreversible loss supplied additional structure that made the local forms finite and measurable. The coarse construction addresses a different interface and a narrower output objective. Neither construction simply subsumes the other.

## 5. Strong existing methods already solve substantial parts of the problem

The continuation tested these directly.

### Single-operation prediction already has a powerful solution

Ordinary empirical survival estimation, using the Dvoretzky–Kiefer–Wolfowitz–Massart bound, controls an entire lifetime distribution at once. It does not require learning a finite hidden-state model. :chatgpt-content-reference{index="1"}

On the earlier two-rate coarse fixture, an executed batch of 4,000 fresh, finitely censored lifetimes cost 62,181,306 source applications and reports. It supplied an all-repetition-length survival band of radius \(1/32\), with failure below \(0.001\).

That cost belongs to that slower source and that task. It is not a comparison against the later switching experiment’s different source.

The result corrected an unnecessary research burden: a positive Hankel determinant establishes missing memory, but completing a finite-rank realization is unnecessary for predicting one monotone survival curve.

### Exact marginal laws still leave composition information missing

A smallest counterexample uses uniform preparation and

\[
A=\frac1{16}
\begin{pmatrix}
10&2\\2&2
\end{pmatrix},
\quad
B_+=\frac1{16}
\begin{pmatrix}
8&1\\1&2
\end{pmatrix},
\quad
B_-=\frac1{16}
\begin{pmatrix}
2&1\\1&8
\end{pmatrix}.
\]

The two possible sources are \((A,B_+)\) and \((A,B_-)\). A hidden swap conjugates the \(B\) matrices while preserving uniform preparation and total-live readout. Every individual-action lifetime law therefore agrees exactly, at every repetition length.

Their mixed responses differ:

| Response | Source \(+\) | Source \(-\) |
|---|---:|---:|
| \(AB\) survival | \(15/64\) | \(9/64\) |
| \(AAB-ABA\) | \(-1/256\) | \(5/256\) |

Even perfect marginal data leave the preferred order of two mixed programs unsettled. Repetition measurements can bound the switching tail under the common-order premise; mixed observations supply the remaining joint information.

### Familiar adaptive estimation is the strongest executed route here

The adaptive prefix procedure uses independent fresh data and no lifetime pilot. Its emitted finite cover verifies itself through observed prefix bounds and absorption monotonicity.

The acquired energy profile supplies a **class-level theorem about when finite coverage exists**. The adaptive procedure’s actual saving comes from ordinary experimental allocation and midpoint prediction. I have kept those contributions separate.

I also ran the retained scalar-echo compiler on the same fixed-tape observations, using three short dictionaries and exact common-metric checks. Its best boxed-interval bound was about \(9.69646\), hence vacuous beyond the physical probability range. That is a failure of the specified conservative certificate at those counts. It does not establish a lower bound against optimized moment-SDP, residual, or positive-realization methods.

Current verified spectral learning also already handles important infinite-dimensional regimes without a strict global gap. Finite data, residual certification and infinite hidden dimension alone cannot support a novelty claim for this programme. :chatgpt-content-reference{index="2"}

## 6. The next attack produced an exponential acquisition lower bound

After obtaining the finite cover and compact model, I tested whether a stronger representation or solver could make acquisition uniformly inexpensive over the coarse-access class.

The resulting lower bound is stronger than a criticism of prefix trees.

For every \(d\ge2\), the construction has:

- **Four** symmetric, nonnegative primitive controls.
- The same uniform preparation in every hypothesis.
- Exact live/dead observations.
- A supplied strict norm cap
  \[
  c=1-\frac1{20d}<1.
  \]
- Identical individual-action lifetime laws.
- Consequential mixed words of length at most
  \[
  H=3d+2.
  \]

Any learner that returns a reusable predictor with simultaneous error at most \(1/16\) for all words through that horizon, with unconditional success probability at least \(2/3\) on every source, must satisfy

\[
\boxed{
\mathbb E_0 N\ge\frac{2^d-1}{6}.
}
\]

Here \(N\) counts preparations whose trajectory executes an informative loss test. Both total preparations and primitive applications are at least \(N\).

### The mechanism

The hidden state includes a random Boolean coloring of \(\mathbb F_2^d\) and a position. In the baseline source, colors at distinct positions are independent. In a secret-\(w\) source, positions separated by one unknown nonzero vector \(w\) share a color.

Three involutive motion controls—one coordinate flip and two coordinate reflections—can synthesize any translation using at most \(3d\) operations. A fourth control tests the current color and destroys the trajectory on zero. Every operation also has the same independent loss factor \(c\).

Testing a color, translating by \(w\), then testing again has survival

\[
\frac{c^\ell}{4}
\quad\text{under the baseline},\qquad
\frac{c^\ell}{2}
\quad\text{under secret }w,
\]

with a gap of at least \(1/5\).

Under the baseline, each newly queried color is a fresh fair bit. Consequently, a prepared trajectory reaches only a constant expected number of distinct test positions before destruction. If \(D\) is that number,

\[
\mathbb E\binom D2\le2.
\]

Those pairs are the possible hidden relations exposed by the trajectory. Coupling the full adaptive experiment to a uniformly chosen persistent secret gives

\[
\operatorname{TV}(\text{baseline transcript},\text{secret-mixture transcript})
\le
\frac{2\mathbb E_0N}{2^d-1}.
\]

A uniformly accurate reusable predictor would distinguish the hypotheses using its answers on the finite witness family. That requires total variation at least \(1/3\), yielding the lower bound.

The proof covers adaptive controls, stopping and fresh preparations. Ordinary reversible motions, including returns to previously visited positions, remain available. The excluded additional capabilities are cloning, restoring a destroyed sample, or preparing a fresh trajectory while retaining a chosen hidden coloring.

### A strong equally informed upper route is included

When the whole source family is disclosed, testing every candidate relation with

\[
n=\left\lceil 50\log\frac{2(2^d-1)}{\delta}\right\rceil
\]

fresh trials identifies the baseline or secret with failure at most \(\delta\). It costs \((2^d-1)n\) preparations, at most \(H(2^d-1)n\) primitive applications, and at most twice that preparation count in endpoint reports.

Thus the upper and lower agree in exponential acquisition scale, up to polynomial and logarithmic factors. General future prediction may itself require exponential arithmetic; that cost is also retained.

The source state space is enormous, and the known gap decreases with \(d\). The motion operators can have negative eigenvalues. The result establishes a limit for symmetric nonnegative kernels; it leaves the positive-semidefinite-only subclass unresolved. Full proofs and exact small cases are in :chatgpt-content-reference{index="7"}[COARSE_INTERFACE_LIMIT.md](producer-workspace/COARSE_INTERFACE_LIMIT.md).

## 7. A constructive cost theorem survives the obstruction

The positive response is to charge an actual simplifying resource.

Let \(C_\epsilon\) be the size of the smallest complete prefix tree whose terminal prefixes all have true survival at most \(\epsilon\). This tree is canonical: stop at the first sufficiently small-survival prefix.

A fresh-batch adaptive learner need not know its size in advance. At visit \(j\), spend

\[
\delta_j=\frac{\delta}{j(j+1)}
\]

and choose the batch size before inspecting that batch. For the midpoint-terminal version,

\[
N_j=
\left\lceil
2\epsilon^{-2}
\log\frac{2j(j+1)}{\delta}
\right\rceil .
\]

When \(C_\epsilon<\infty\), this gives complete costs of order

\[
\boxed{
P=
O\!\left(C_\epsilon\epsilon^{-2}
\log(C_\epsilon/\delta)\right)
}
\]

for preparations, and

\[
\boxed{
S=
O\!\left(H_\epsilon C_\epsilon\epsilon^{-2}
\log(C_\epsilon/\delta)\right)
}
\]

for primitive applications and per-step reports. On the simultaneous confidence event, a sharper source bound uses the tree’s sum of depths.

The proof also controls rare failures rather than leaving expected cost undefined outside the confidence event. If \(B\) counts confidence failures,

\[
\mathbb E e^{\theta B}
\le
\exp\!\left(\delta(e^\theta-1)\right).
\]

The acquired tree has at most \(C_\epsilon+qB\) nodes and depth at most \(H_\epsilon+B\). This proves almost-sure termination and the same unconditional expected cost orders whenever the comparison cover is finite.

This is a sufficient resource bound for adaptive prefix estimation. A method exploiting additional structure may beat that tree size. The lower bound above shows why some such structure or stronger access must enter any general efficiency claim.

## 8. What remains valuable from P1, and the resulting agenda

The preceding results remain intact at their actual scopes.

The predecessor’s finite-rank scalar acquisition and static control constructions are retained. Their measurement counts still do not acquire numerical precision.

The completed boundary construction remains stronger for boundary transport. Its executed infinite-source acquisition used 12,036,469 source applications and observations and 1,758,723 preparations. It certified a point-model error below \(0.039906\) for every word. Familiar positive Galerkin interval propagation, using the same acquired physical form, gave the stronger transport-order interval

\[
[0.1080212656,\;0.1337115038].
\]

A direct test of that one program pair cost only 400,000 source applications, so reuse still has to earn its larger acquisition bill.

The complete \(g^{-3}\) calibration obstruction also remains. Even zero residual and fully visible survival do not remove the cost of learning retained rates accurately enough for long compositions. The accepted Astra undecidability foundations were preserved without a routine re-audit.

**The research decision is now sharper.** Inverse dissipation is one useful certificate. Observable output accuracy can remain finitely certifiable when that form diverges. At the same time, coarse access can conceal exponentially many consequential joint contexts, even when the marginal dynamics and a strict gap are known.

A foundation with the ambition of this assignment must therefore add something substantive: an acquired structural reason that a small set of joint contexts suffices, or a physical operation that exposes the missing information at a fully charged cost. A small fitted model alone does not provide that reason.

The present continuation establishes a working conditional capability, an improved existing implementation, and a precise obstruction to generic efficiency. The positive-semidefinite passive subclass is one concrete unresolved boundary: the four-control hardness construction uses reversible permutations with negative spectral modes, so it does not settle whether stronger physical passivity can make joint-context acquisition substantially easier.
