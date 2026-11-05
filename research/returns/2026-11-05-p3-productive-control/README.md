# Productive feedback control when interventions change the failure law

The supplied construction uses finite local uncertainty bounds to certify an entire optimal useful-work policy across every finite damage depth, without accurately predicting its rare absolute value. Unlike the earlier common-invariant comparison, these actions change both worsening and repair probabilities and have different invariant laws. The same package gives finite-mission guarantees, attained rare-evidence boundaries and an independent productive-repair resource theorem. These are conditional mathematical capabilities, with synthetic acquisition and exact certificates; a physical apparatus, historical novelty and civilisation-changing advantage remain unestablished.

Read the [complete report](package/Astra_Productive_Control.pdf), [governing TeX](package/report.tex), [acquisition and forecast separation](policy-and-evidence.md), [mission and rare-hazard boundaries](missions-and-rare-hazards.md), [repair and physical resources](productive-repair-and-resources.md), [status](package/STATUS.txt), and [source register](package/sources/GOVERNING_SOURCES.json). The [original ZIP](original/Astra_Productive_Control_Research_Package.zip), [complete captured return](P3_PRODUCTIVE_CONTROL_20261105_RETURN.txt), and [publication provenance](SOURCES.json) retain the supplied evidence. Only the capture header's local ZIP locator is replaced by its public archive path; all prompt, scientific and activity bytes remain unchanged.

A subsequent [spatial burst-recoverability opening](../2026-11-05-p3-burst-recoverability-opening/README.md) changes the fault model and proves a finite-seed causal-cone erasure obstruction. Its matching recovery construction is unproved; the final horizon quantifiers, physical readout floors and strong existing comparisons are linked. No physical reduction from the skip-free or repair models here is assumed. This complete original archive and all nested predecessors are preserved unchanged.

## A declared actual operating cycle

Damage is i=0,...,N, with failure at N. Each safe cycle lasts a fixed finite Delta and completes positive useful reward r_i(a) before its transition. Action a worsens damage by one with probability p_i(a), repairs by one with probability q_i(a), otherwise holds; downward motion reflects at zero. A uniform `p_i(a)>=p_min>0` is assumed.

The cycle kernel is an actual interface premise. A small time step that silently omits multiple events does not establish it. Reliable state sensing, transition support, uniform operating envelopes, actuator costs and future validity must be justified for a physical installation.

## Forward differences certify a policy without its absolute value

Set `c_i(a)=r_i(a)/p_i(a)`, `rho_i(a)=q_i(a)/p_i(a)`. The exact maximum expected useful work, among all admissible randomized history-dependent policies, is

```text
d0=max_a c0(a),
di=max_a [ci(a)+rho_i(a)d_(i-1)],
V_i^(N)=sum_(j=i)^(N-1) dj.
```

The maximizing action is optimal at state i. The recursion does not contain N: one rule on nonnegative integers restricts to an optimum for every finite threshold and every safe initial state. The Bellman inequality is `p_i(a)d_i>=r_i(a)+q_i(a)d_(i-1)`. A reward-plus-value supermartingale verifies all policy quantifiers; absorption is integrable with the uniform bound `E T_N<=N/p_min^N`.

Forward recursion for skip-free controlled processes is established machinery, explicitly credited to Wijngaard-Stidham and Serfozo. The construction fixes its objective, initialization and uncertainty quantifiers; it does not invent dynamic programming.

## A finite prefix and an invariant tail

Suppose uniform earned envelopes give `p_a^-<=p_i(a)<=p_a^+`, corresponding q and reward bounds, and define

```text
c_a^-=r_a^-/p_a^+,    c_a^+=r_a^+/p_a^-,
rho_a^-=q_a^-/p_a^+, rho_a^+=q_a^+/p_a^-.
```

Finite interval comparisons certify an initial prefix. If one action star has `rho_star^->1` and exceeds every competitor's upper rho, set

```text
D_box=max_(b!=star) (c_b^+-c_star^-)_+/(rho_star^--rho_b^+).
```

Once a certified lower bound on the preceding d reaches D_box, star dominates every competitor and preserves that lower interval thereafter. Prefix comparisons exclude the selected action itself. This finite certificate covers every fixed state-dependent Markov kernel inside the envelopes, without numerical homogeneity. Learning those envelopes at one state still requires homogeneity or an independently earned transfer guarantee; unrestricted state rows need their own coverage.

## Explicit useful operation and an honest comparator

The two nominal actions are:

| Action | Worsening p | Repair q | Hold | Completed useful units |
| --- | --- | --- | --- | --- |
| A | 0.1 | 0.2 | 0.7 | 3 |
| B | 0.2 | 0.7 | 0.1 | 2 |

Their nonabsorbing stationary-weight ratios p/q are 1/2 and 2/7. There is no common invariant law to cancel. The affine expressions are `30+2d` and `10+3.5d`, giving the exact optimum A at zero and B at every positive safe damage state. Every cycle completes at least two useful units, including the terminal cycle's reward.

```text
V0^(N)=(68/5)[(7/2)^N-1]-4N,
V_alwaysB^(N)=(28/5)[(7/2)^N-1]-4N.
```

The gain against always B, the stronger fixed comparator at large depth, tends to 17/7, about 2.43. Comparing only against always A would exaggerate the useful feedback gain. An equally informed ordinary direct policy method can use the same certificate.

## Resource-priced objective and scope

For measured useful output g and measured operating energy e, including charged sensing/control, the same theorem handles positive reward `r=g-chi e` and maximizes `E[W-chi E_op]` under a separate throughput floor. In the nominal equal-energy example the same controller remains optimal for `0<=chi e0<2`. Equal actual energy is a premise, and other prices need recomputed reward intervals and certificates. A hard total fuel cap, switching cost, variable duration, general risk objective or changing environment is a different control problem.

The [preceding prevention package](../2026-11-05-p3-direct-prevention/README.md) is preserved unchanged in the new archive. Its common-Gibbs-law mean result and all-safe-start initialization keep their original scopes. The included exact P2 predictive-preparation source has a loaded LTI/finite-energy/private-timing contract; no bridge to this damage process is asserted. Capital performed no new proof audit, simulation, source execution or heavy build. Generated current retrieval was not rebuilt.
