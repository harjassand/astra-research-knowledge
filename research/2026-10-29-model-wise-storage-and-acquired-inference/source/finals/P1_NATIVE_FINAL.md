**The strongest opening is now a theory of which physical information makes sustained dissipation identifiable.** I developed three complementary results, then pursued the main obstruction far enough to obtain a recovery theorem.

The distinction is substantive: a visible time arrow can reflect ongoing dissipation, asymmetry in the prepared ensemble, or hidden memory that persists throughout the observation. The results below concern path-reversal divergence under a declared physical reversal. Interpreting that divergence as thermodynamic entropy or heat still requires the appropriate native dynamics and reservoir model.

## 1. Fixed state counts and fixed clocks do not remove the ambiguity

I constructed the following general result.

For **any finite irreducible \(n\)-state source**, any fixed observation horizon \(T\), and any positive tolerances \(\delta,\eta\), there is an irreducible **\(4n\)-state hidden model** such that:

- Its entire observed path law on \([0,T]\) is within total variation \(\delta\) of the source’s.
- Its sustained physical-reversal divergence rate is below \(\eta\).
- **Every microscopic state has the same fixed escape rate \(\Lambda\)**, independent of the requested accuracy.
- The visible readout is even under the model’s reversal.

The construction introduces a hidden orientation. One orientation runs \(Q\); the other runs its stationary adjoint \(Q^*\). Their stationary weights are \(1-\epsilon,\epsilon\), with switching rates \(\kappa\epsilon,\kappa(1-\epsilon)\). Before equalizing the clocks, the sustained rate and preparation boundary are exactly

\[
\sigma=\kappa(1-2\epsilon)^2,
\qquad
B=(1-2\epsilon)\log\frac{1-\epsilon}{\epsilon}.
\]

Coupling the source and the forward orientation gives the full-path guarantee

\[
\operatorname{TV}\!\left(P_{\mathrm{lift}}^{[0,T]},P_Q^{[0,T]}\right)
\le
\epsilon+(1-\epsilon)\left(1-e^{-\kappa\epsilon T}\right).
\]

An additional invisible bit equalizes all escape clocks while preserving that observed path law exactly. Its sustained rate still tends to zero.

**The remaining resources are small switching rates, small stationary weights, slow orientation relaxation, and distinguishability from the reversed preparation.** A fixed maximum clock does not control those resources.

There is an important interpretation correction: the orientation occupies one bit. Although \(B\) diverges, its divergence from an *unbiased* bit stays below \(\log 2\). Thus \(B\) is neither an unbounded stored-bit count nor automatically an unbounded preparation-work cost.

The parity-boundary correction and an oriented-ring special case already appear in Kim–Lee–Jeong. The contribution developed here is the arbitrary-source construction, its fixed state and clock accounting, and its quantitative finite-observation consequence. Historical priority of that combined theorem remains unestablished. :chatgpt-content-reference{index="0"}

The ordinary proof passed independent review. Exact rational controls also verified the construction on a nonuniform three-state source, including stationarity, reversed support, the entropy formulas, and the full-path projection identity.

:chatgpt-content-reference{index="5"}[ORIENTATION_MEMORY_AND_SUSTAINED_ENTROPY.md](producer-workspace/ORIENTATION_MEMORY_AND_SUSTAINED_ENTROPY.md)

## 2. Following the failure produced a precise recovery condition

The governing finite-window identity is

\[
D(P_{\mathrm{hidden}}^{[0,T]}
\Vert \mathcal R_\Theta P_{\mathrm{hidden}}^{[0,T]})
=
B+T\sigma.
\]

Consequently, a genuinely supplied bound \(B\le B_{\max}\) restores a rate inference from an observed divergence lower bound \(I_T\):

\[
\sigma\ge \frac{[I_T-B_{\max}]_+}{T}.
\]

I then pursued a different way to exclude persistent orientation memory. Suppose the **forward hidden dynamics** has a certified Dobrushin contraction coefficient at most \(\beta<1\) after a specified time \(s\). If \(\Delta_T\) is the total-variation asymmetry between the observed forward and reversed path laws, then

\[
\boxed{
\sigma\ge
\frac{2\Delta_T^2}
{\left(\sqrt T+\dfrac{\sqrt s}{1-\beta}\right)^2}.
}
\]

A bounded reversal-odd observed statistic can supply a certified lower bound on \(\Delta_T\). The proof works with a contraction bound for either the forward or physically reversed hidden dynamics; **it requires no operation implementing microscopic reversal**.

The acquisition obligation remains real. Ordinary visible correlation decay, finite irreducibility, and an upper escape-rate bound do not establish this uniform hidden contraction. The counterexample explains why: its microscopic clocks stay fixed while its orientation relaxation becomes arbitrarily slow.

This recovery theorem identifies a sufficient missing input after the failure. It does not claim that the input has been acquired.

## 3. Genuine regenerative access retains a nonzero entropy floor

The orientation construction does **not** invalidate the native-event results. A certified singleton microscopic port fixed under reversal is additional information. Returning to it removes hidden memory; returning to an ordinary visible symbol may retain that memory.

For the resolved native interface, let \(K_{ij}(t)\) denote excursion-flux densities and \(d_{ij}\) direct fluxes. Define

\[
J=
\sum_{ij}\int K_{ij}(t)\log\frac{K_{ij}(t)}{K_{ji}(t)}\,dt
+
\sum_{i\ne j}d_{ij}\log\frac{d_{ij}}{d_{ji}}.
\]

I proved a matching converse: **\(J\) is the exact robust intrinsic-entropy floor** over finite hidden completions approaching the record in weighted \(L^1(1+t)\). The construction preserves port weights, integrated endpoint fluxes, direct fluxes, native port clocks, and total hidden mean exactly. The corresponding per-time floor is \(J/W\).

For records produced by finite sources, exact attainment by one finite model has a complete criterion:

\[
E=J
\quad\Longleftrightarrow\quad
\frac{K_{ij}(t)}{K_{ji}(t)}
=
C_{ij}e^{\delta_{ij}t}
\]

for every nonzero directional pair. Under equal reversed escape clocks, those ratios must be constant.

Exact matching can nevertheless differ radically from finite-accuracy matching. For

\[
K_{12}(t)=e^{-t},
\qquad K_{21}(t)=te^{-t},
\]

the observable divergence is \(J=1\), but **every exact finite fixed-port completion has infinite microscopic reversal divergence**. Finite approximants preserve the total mean and approach entropy \(1\). The exact short-time zero carries structural information that finite samples do not establish.

The approximation’s state counts, rates and coefficient precision are retained explicitly. This is a completion theorem, with no computational advantage claimed over direct evaluation of the supplied record.

:chatgpt-content-reference{index="6"}[ENTROPY_COMPLETION_CONVERSE.md](producer-workspace/ENTROPY_COMPLETION_CONVERSE.md)

## 4. The all-even class admits a complete equilibrium-compatibility theory

For stationary finite-alphabet, memoryless observations of all-even hidden systems, I constructed a different characterization:

> An observed law lies in the finite reversible-CTMC observation closure **if and only if** its path probabilities extend consistently to every finite rational metric tree, including subdivision of an edge into durations that add correctly.

The representation proof builds a common hidden probability space from repeated rooted patterns. Root gluing supplies multiplication; symmetric couplings supply reversible kernels; time subdivision forces one semigroup.

Every finite part of the extension problem is an LP. Compactness makes the hierarchy **complete for finite incompatibility and for detecting a strictly positive robust entropy floor**. This reaches beyond reflected-history CP tests: current Astra N507 already provides a law passing that entire CP family while excluding hidden equilibrium.

The tree representation and positive-extension machinery have substantial antecedents, including Aldous and complete causal-inflation hierarchies. The specific addition under investigation is the metric-subdivision bridge to finite continuous-time observation closure and its entropy consequence. :chatgpt-content-reference{index="1"}

This supplies a foundational criterion across unbounded hidden dimension and rates. It does not establish an efficient algorithm or an optimal numerical entropy estimate. Existing hidden-network optimization remains the strong comparator, including its superior result on the earlier population example; established approaches already optimize over substantial time-symmetric information under their stated model restrictions. :chatgpt-content-reference{index="2"}

:chatgpt-content-reference{index="7"}[COMPLETE_EQUILIBRIUM_INFORMATION.md](producer-workspace/COMPLETE_EQUILIBRIUM_INFORMATION.md)

## Scientific position

The new work separates three boundaries: **generic coarse observation, genuine regenerative access, and a physically warranted all-even model**. It also identifies quantitative hidden-memory decay as another sufficient input that can change the conclusion.

The decisive remaining bridge is to establish such preparation or memory guarantees for a native physical source class through warranted physics or acquisition. A fitted hidden model does not supply that guarantee by itself.

All proofs, exact code, substantive internal reviews, source comparisons and corrections are preserved. The previous acquired record and midpoint-operation theorem retain their original scope. No new native observations or physical operations were performed.

[**:chatgpt-content-reference{index="4"}**](https://chatgpt.com/library?file_id=libfile_732fe99c22f0819194aef19ab09088c8&account_id=personal) contains the complete new work and the unchanged immediate predecessor archive.