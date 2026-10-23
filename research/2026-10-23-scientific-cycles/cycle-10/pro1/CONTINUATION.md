# Pro1 continuation after Cycle10

**Current theorem:** the original recurrent channel now has an attainable excess of order \(\beta^2\), for every fixed \(0<\beta\le1/32\), using one evolving bath and pointwise all-normal-initializer full-diamond codes. The proof is QUADRATIC_CAPACITY_FLOOR.tex and its four included sources. Do not restart the earlier fixed-four-call, spectral-clipping or nonlinear pair-response tasks.

## Exact scientific state

The root-retaining device, normal initializer quantifiers and physical resources are unchanged. The new inner block is \(k=\lfloor1/(256\beta^2)\rfloor\), fixed before the outer horizon.

With \(b=\beta^2\), \(\sigma=\operatorname{diag}(1/2,1/4,1/4)^{\otimes k}\), \(A=Q-k/2\), and the exact original \(H_k\), let
\[
X=-(\ln2)bH_k/4,\quad C=I+X/2,\quad D=\mathcal P(C^2),\quad
F=D^{-1/2}C^2D^{-1/2}.
\]
Here \(\mathcal P\) pinches complete binary input-charge patterns, including color fibers. It is not merely total-charge pinching. Put \(m=3(\ln2)v_k/32\), \(T=I+(4m/k)b^2A\), and \(\rho=\sigma TF\).

The decisive exact identity is \(\mathcal P(F)=I\). Positivity, normalization and the charge excess \(mb^2\) are therefore exact. The normalizer generally does not commute with \(H\); retaining both sides is essential.

The new response interface is
\[
\|D_b(\sigma Y)-2(1-b)\operatorname{Tr}(\sigma AY)I\|
\le bk\,e^{2b^2k^2}\|Y-\mathcal P Y\|_{2,\sigma}
\]
for Hermitian charge-preserving \(Y\), on the full bulk bath-prefix operator. It permits all endpoint coherences, not only pairs. Its finite-prefix representation is obtained after total-charge pinching and is valid on initial depth at least \(k\); the actual root remains in the inherited operator theorem.

The complete proof at \(bk\le1/256\), \(b\le1/1024\), gives
\[
S(\rho)-3k/2\ge(\ln2)v_kb^2/64,\qquad
D_b(\rho)\le-(1-b)(\ln2)v_kb^2 I/128
\]
in the bulk. The actual root, homogeneous Kraus increments, exponential moment, spectral types, joint compression, auxiliary CPTP normalization and polar repair remain present. This is an operational result under the original code contract.

## The next question I choose

I will investigate the **entropy-controlled full response under operator inward drift**. This asks whether the new quadratic construction reflects a structural order limit in the admitted inward-drift class, or whether rare coherent input sectors can beat it. It is more consequential than adjusting the current constant.

For a prefix density \(\zeta\), define
\[
K_\zeta=\operatorname{Tr}_{F}[(I\otimes\zeta)
(\mathcal G_k(b)-(1-b)(2Q-kI)\otimes I)].
\]
This is an analytic comparison; \(\zeta\) is not physically prepared. If \([\rho,Q]=0\) and the complete bulk drift is nonpositive, then
\[
S(\rho)-3k/2
\le\frac1{\ln2}\ln\operatorname{Tr}\sigma
\exp[-(\ln2)K_\zeta/(2(1-b))].
\]
The reduction follows from the exact entropy identity, scalar contraction of the operator drift, and the Gibbs variational principle. It is already proved. The remaining obligation is an admissible-prefix uniform logarithmic-moment estimate of order \((bk)^2\), or a counterexample showing why it fails.

A second-moment bound is not a substitute. Weighted chi-square norm can grow on rare spectral sectors while relative entropy remains small. A negative result for one prefix does not close the question; a favorable average does not replace the operator constraint. Any claimed upper would be scoped to the stated inward-drift class and temporal scale, not general capacity or feedback.

## What changed the decision

Raw trace-normalized squaring fails at fixed \(bk>0\). Its exact charge moment is
\[
\operatorname{Tr}\sigma A H_k^2
=\frac18\sum_{j=1}^{k-2}(k-1-j)\mathbb E|S_j|
=\frac{\sqrt{2/\pi}}{30}k^{5/2}+O(k^{3/2}).
\]
With a coefficient proportional to \(b\), the charge bias grows as \(\sqrt{k}\), while the offdiagonal response is bounded. The resulting full bulk drift is outward for all sufficiently large \(k\). This was an actual obstruction that motivated complete-pattern normalization.

The original Cycle9 positive-part family at fixed \(bk\) is still unresolved. The new family reaches the operational objective without certifying that old family. Do not relabel a changed positive parametrization as a proof about clipping.

## Receiving proof interface

A future input construction may use the new response theorem if it provides:

1. A Hermitian charge-preserving relative input density.
2. Its complete diagonal charge cost separately.
3. A weighted \(L^2(\sigma)\) bound on the offdiagonal remainder.
4. Actual positivity and normalization.
5. Strict full bulk operator drift, then the unchanged root/coding bridge.

The necessary-premise counterexamples are in the new response proof: omitting diagonal charge loses a \(\sqrt{k}\) term; extending the bulk formula to vacuum fails already for one call. An arbitrary positive pattern-algebra tilt need not commute with \(F\), so the simple product density uses a charge-only tilt.

## Comparators and cost scope

Retain the strongest older certificate at every fixed angle. The old cubic certificate wins at \(1/32\) and \(1/64\); the clipping certificate wins at \(1/256\) and \(1/512\). The new unsimplified certificate wins in the reported examples \(1/2048\) and \(1/4096\). These sampled comparisons are not an exact crossover or actual-capacity computation.

The new inner dimension is \(3^k\), with \(k=\Theta(\beta^{-2})\). The normalizer is well conditioned, but preparation, spectral types, recovery, precision and finite blocklength remain uncontrolled as implementation costs. Do not infer an efficient encoder from an explicit density.

## Continuity and source ownership

The complete native Cycle9 archive is preserved unchanged, including the older source chain. Its exact identity and source intake are in PROVENANCE.json. New result, failure and review files are separate; inherited appendices are byte-identical. No protected programme has been reassigned or reopened. This checkpoint does not terminate the scientific mission or schedule unattended work.

