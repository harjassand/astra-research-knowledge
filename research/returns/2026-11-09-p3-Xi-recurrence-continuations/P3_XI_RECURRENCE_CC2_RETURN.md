# P3 Xi completed return

Source: https://chatgpt.com/c/6af0a937-daa0-83ec-99c5-8df8b56023e0
Model: normal-web GPT-6 standard, Extra High. Turn: cc2c9661-3977-4b42-a9c7-5356baad99d3. Response: 37585dcf-411d-4e60-a2f2-60a6da0a9c5f. Completed: 2026-11-08T18:33:01.128Z.
ZIP: none supplied in the visible return.

## Actual prompt

Resolve the SAME FULL weak-reversibility recurrence question. You own all ideas, representations, methods and source order and may challenge the framing.

For EVERY finite mass-action network on arbitrary finite d species, arbitrary molecularity/linkage classes, every constant rate vector kappa_r>0 and initial population x0, suppose every reaction lies on a directed complex cycle. The minimal CTMC has
    Lf(x)=sum_r kappa_r*(x)_{y_r}*[f(x+y'_r-y_r)-f(x)],
with native falling factorials. Construct a proof of nonexplosion and finite mean return on every nonabsorbing reachable class, hence unique class-stationary probability and full TV convergence; absorbing singletons separate. Or exhibit an actual same-model network/rates/class with proved failure. Include all dimensions, disabled boundary sources and unbounded classes. No complex balance/added outflow/supplied drift or moment certificate/bounded-count/efficient-oracle substitute.

Your complete a18a519c return supplies a genuinely global candidate operation:
    g(x)=max_{enabled complexes c}(x)_c,
    V(x)=sum_i log(x_i!)-log g(x)
        =min_{enabled c}sum_i log((x_i-c_i)!).
V is proper on nonabsorbing states. For s->t and x'=x-s+t,
    Delta V=log[g(x)/(x)_s]-log[g(x')/(x')_t].
A reaction from a maximal source is nonincreasing, and expected positive increment per EMBEDDED jump is <=K_kappa*J/e. This is not physical-time drift or nonexplosion. Your earlier radial nonexplosion scope at mass-changing degree<=2 remains credited once.

Your reversible unit-rate A<->2A+B,A<->3A+3B,A<->4A+4B example is positive recurrent/product-Poisson; at x_n=(n,0), E[V(X_k)-V(x_n)] tends0 for each FIXED jump count k. It excludes a uniform negative constant per fixed number of jumps for THIS potential, not a time-normalized stopped-Foster inequality.

ROOT personally checked a potentially useful distinction on THAT exact example: leading-path expansion gives
    E_xn Delta V at3jumps=-(log n)/(6n)+O((log n)/n^2),
    E_xn physical elapsed time to3jumps=2/(3n)+O(1/n^2).
Thus their ratio is asymptotic to -(log n)/4. A leading negative path is (n,0)->(n+2,3)->(n+1,2)->(n,1), probability1/(6n)+O(n^-2), increment -log(n-1); leading positive2jump excursions cancel after their3rd jump. An independent exact-rational-transition diagnostic at n=100,1000,10000,100000 agrees with these limits; it is not a general recurrence proof or a physical-time Foster certificate. Use or discard this optional observation and any method. The general boundary/linkage/nonexplosion/integrability construction is still genuinely absent.

Actually read scoped predecessors:
* Kriebelv1.2.4,22Aug2026 https://aleckriebel.com/research/positive-recurrence-bimolecular-reaction-networks/paper-v1.2.4.pdf Theorem2.1/Lemmas2.2,3.2-3.3/Prop4.3/Lemma5.3: binary ONE-linkage native marked-target episodes.
* Wiuf-Xu2012.07954v3 https://arxiv.org/html/2012.07954v3 H1-H5/Theorem4.8/Cor4.10: stoichiometric rankONE, not higher rank.
* Agazzi-Laurence2610.31550v1 https://arxiv.org/html/2610.31550v1 Theorem4.1/Assumptions1-5/Definition4.2/Cor4.3/AppendixA.1: PLANAR bulk/stopped drift with nondegeneracy/no-ghost/no-horizontal-leading restrictions, boundary/jump-width and integrable mean-stopping obligations. Announced all-two-species work in preparation is not an acquired proof.

Pursue FULL resolution persistently with scientist autonomy. The proper max-envelope is useful capital; neither another candidate energy, a method obstruction nor a complex-graph entropy identity alone resolves the whole theorem.

you may use all subagents avaible
All inherited source/access/transfer holds apply to every subagent, including unknown identities. The failed OpenAI Uniform-Permanence GitHub tree and EVERY older failed original/transfer remain HELD: no retry/raw/PDF/mirror/alternate/identifying recovery/held-source injection. Also preserve the reported NSF par.nsf.gov/servlets/purl/10314785 fulltext-timeout hold; no argument is imported from it. No attachments, new model/worker/resource/account/spending, Sol or Dots action.

## Available user-visible activity

Worked for 18m 39s

I’ll check the three scoped papers at their stated theorem boundaries, then test the max-envelope potential against continuous-time return estimates and look for an actual weakly reversible counterexample. I’ll treat the conjecture as unresolved unless a complete proof or same-model failure can be established.

Analyzed the paper

Tested global behavior, constructed stationary measure, and sought Lyapunov structure

Strengthened arguments and tested multiscale cycle proof strategies

Searched 18 websites

The key issue is now narrower: the max-envelope identity controls individual jumps, but it does not yet provide a negative drift over a stopping interval whose expected physical duration is integrable. I’m testing that distinction directly, rather than treating the three-jump calculation in the reversible example as evidence of a universal drift theorem.

Reassessed recurrence

Reframed and clarified the stochastic recurrence proof approach

Searched 10 websites

I also checked a possible comparison argument: weak reversibility lets us choose a complex-balanced reference network with the same reaction graph and rates differing only by fixed channel factors. That does not by itself transfer positive recurrence. A valid comparison would still have to control how those factors accumulate along arbitrarily long population paths, especially near boundary faces. I have not established that control.

Assessed the recurrence argument

Assessed the theorem and evaluated recurrence-based proof gaps and options

Searched 1 website

## Complete response

# Full weak-reversibility recurrence problem — result

**Status: unresolved.** I have not constructed a valid proof of universal nonexplosion and positive recurrence, nor found a weakly reversible mass-action network with a proved failure.

The investigation did yield a useful structural reduction and a stronger inequality for the existing max-envelope potential. Neither supplies the missing finite-return-time argument.

## 1\. Every weakly reversible network has a complex-balanced reference with the same reaction graph

This follows directly from weak reversibility, without restrictions on dimension, molecularity or linkage classes.

For every reaction \(r\), choose a directed complex cycle containing it. Sum the unit circulations of these cycles to obtain strictly positive numbers \(a_r\) satisfying

\[
\sum_{r:y_r=c}a_r
=
\sum_{r:y'_r=c}a_r
\qquad\text{for every complex }c.
\]

Define a reference mass-action chain using rate constants \(\widetilde\kappa_r=a_r\)\.

Its product-Poisson distribution

\[
\nu(x)=\frac{e^{-d}}{\prod_i x_i!}
\]

is stationary. Indeed, its stationary flux along an edge lifted from residual population \(\rho\) is

\[
\nu(\rho+y_r)\widetilde\kappa_r(\rho+y_r)_{y_r}
=
\frac{e^{-d}a_r}{\rho!}.
\]

The complex-circulation identities make incoming and outgoing fluxes agree at every population state.

Furthermore,

\[
\sum_x\nu(x)\widetilde\Lambda(x)
=
\sum_r a_r<\infty.
\]

Thus the reference process is nonexplosive and positive recurrent on each nonabsorbing reachable class.

Since the original network has finitely many reactions, constants \(0<m\leq M<\infty\) exist such that

\[
m\widetilde\kappa_r
\leq\kappa_r
\leq M\widetilde\kappa_r
\qquad\text{for every }r.
\]

**Consequently, every network in the conjecture is a bounded channelwise rate perturbation of a complex-balanced, product-Poisson recurrent network.**

This is an exact structural fact, not the desired recurrence theorem. Bounded comparisons of transition rates alone do not generally transfer positive recurrence between Markov chains. The required stability result for this special class of mass-action perturbations has not been proved here.

In particular, the reference distribution \(\nu\) is not necessarily stationary for the original rates \(\kappa\)\.

## 2\. A stronger global bound for the max-envelope potential

Recall

\[
g(x)=\max_{c\leq x}(x)_c,
\qquad
V(x)=\log(x!)-\log g(x),
\]

where the maximum is over genuine source complexes.

For a reaction \(s\to t\) and \(x'=x-s+t\), the established identity is

\[
V(x')-V(x)
=
\log\frac{g(x)}{(x)_s}
-
\log\frac{g(x')}{(x')_t}.
\]

The second logarithm is nonnegative. Therefore,

\[
(\Delta V)_+\leq\log\frac{g(x)}{(x)_s}.
\]

Let \(\bar\kappa_s\) be the sum of outgoing rate constants from source \(s\), and let

\[
\Lambda(x)=\sum_s\bar\kappa_s(x)_s.
\]

Conditioning on the source of the next embedded jump gives

\[
\begin{aligned}
\mathbb E_x\left[e^{(\Delta V)_+}\right]
&\leq
\sum_{s\leq x}
\frac{\bar\kappa_s(x)_s}{\Lambda(x)}
\frac{g(x)}{(x)_s}\\
&=
\frac{g(x)}{\Lambda(x)}
\sum_{s\leq x}\bar\kappa_s\\
&\leq
\frac{\sum_s\bar\kappa_s}
{\min_s\bar\kappa_s}.
\end{aligned}
\]

Hence

\[
\boxed{
\sup_{x\text{ nonabsorbing}}
\mathbb E_x[e^{(\Delta V)_+}]
\leq
\frac{\sum_s\bar\kappa_s}{\min_s\bar\kappa_s}
<\infty.
}
\]

This strengthens the previously established uniform first-moment bound to an exponential-moment bound of order one, for **all dimensions, all molecularities, all linkage classes and all positive rates**\.

It is still an embedded-jump inequality. It does not establish negative expected drift or control the accumulation of infinitely many jumps in finite physical time.

## 3\. Why these operations do not close the theorem

The reference-network reduction suggests proving that the factorial confinement of a complex-balanced chain survives every fixed positive perturbation of its reaction-rate constants.

The max-envelope inequality suggests a different route: obtain enough negative drift over suitably chosen stopping intervals to compensate for positive increments.

Neither route is complete.

For the first, no uniform stationary-measure comparison or return-time theorem has been established that handles arbitrarily long excursions and rate imbalances among linkage classes.

For the second, what is missing is a proper energy \(W\) and integrable stopping times \(\tau_x\) satisfying, outside a finite set,

\[
\mathbb E_x[W(X_{\tau_x})-W(x)]
\leq-\beta\,\mathbb E_x[\tau_x],
\qquad \beta>0,
\]

together with the localization and nonexplosion conditions required to apply the stopped-process criterion.

The negative three-jump physical-time drift in the supplied reversible example confirms that vanishing drift per fixed jump count does not preclude such an estimate. It does not establish the estimate for arbitrary networks.

## 4\. Verified literature boundary

The three scoped predecessors remain restricted\:

- **Kriebel, Theorem 2.1\:** one linkage class, molecularity at most two. Its marked-target method does not directly settle arbitrary molecularity or linkage classes. citeturn540567view0
- **Wiuf–Xu, Theorem 4.8 and Corollary 4.10\:** the positive-recurrence conclusion applies to stoichiometric rank one under the stated structural hypotheses. citeturn540567view1
- **Agazzi–Laurence, Theorem 4.1 and Corollary 4.3\:** planar stopped-drift construction requiring additional assumptions and compatible boundary dissipation. citeturn540567view2

The ConStRAINeD collaboration publicly reports an all-two-species result, but lists its full manuscript as *in preparation*\. Its publication page also explicitly identifies arbitrary-dimensional recurrence as unresolved. citeturn414525view0

## Final determination

The new work establishes two facts: a weakly reversible network always admits a complex-balanced reference with the same reaction channels, and the max-envelope potential has uniformly exponentially integrable upward increments at embedded jumps.

Neither implies the required recurrence theorem.

I cannot provide a valid unrestricted proof of nonexplosion and finite mean return, and I cannot exhibit an actual counterexample satisfying all the stipulated mass-action and weak-reversibility conditions. **The full mathematical question remains open on the evidence established here.**
