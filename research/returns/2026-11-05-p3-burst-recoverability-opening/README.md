# Opening: recoverable information under spatial burst damage

P3 asks whether alpha>d+1 is the sharp low-intensity threshold for recovering finite initial information when spatial burst radii have Pareto tail `P(R>r)=r^-alpha`. The supplied opening proves an architecture-independent obstruction and necessary resource scalings. It does **not** prove the matching recovery construction. Two dimensions, with candidate boundary alpha=3, are the first constructive target.

Read the [complete report](package/Astra_Burst_Recoverability_Question.pdf), [report text](package/report_text.txt), [final status](package/STATUS.txt), [construction and comparisons](construction-and-comparators.md), [readout and resources](readout-and-resources.md), [complete captured return](P3_OPPORTUNITY_OPENING_20261105_RETURN.txt), [original ZIP](original/Astra_Burst_Recoverability_Research_Package.zip), and [provenance](SOURCES.json). Only the capture header's local ZIP locator is replaced by its public archive path; all prompt, scientific and activity bytes remain unchanged.

**5 November constructive continuation:** [P2 now supplies the strict-Pareto positive construction](../2026-11-05-p2-burst-constructive-exchange/README.md) under this opening’s final scheduled-circuit contract: fixed one-bit seed, horizon-dependent input-independent finite hardware, arbitrary corruptible mutable state and total error at most 1/4 at sufficiently small fixed positive intensity. The [forced-output gadget and separated Poisson-source proof](../2026-11-05-p2-burst-constructive-exchange/forced-output-and-noise.md) replace the independent-repair-cone route. The [original implementation and paid encoding/readout costs](../2026-11-05-p2-burst-constructive-exchange/implementation-and-resources.md) are linked. Earlier unproved-converse labels below describe this original opening at its own version; they do not describe the later supplied construction. General non-Pareto finite-moment sufficiency and physical realization remain separate. Original producer files and their audit scopes are unchanged.

## The final finite-seed, uniform-horizon target

Fix dimension, burst law, sufficiently small positive intensity and a fixed nontrivial accuracy, such as binary error<=1/4. At commissioning completion every usable input-dependent record lies inside `C0=[-r0,r0]^d`. This includes backups, keys, mutable controller/decoder state and external records that can assist recovery. Outside resources have a joint law independent of the unknown bit; no later source reinjects it.

The seed radius may depend on the law, intensity and accuracy, but **not** on the requested horizon T. One uniform algorithm may generate finite input-independent hardware, wiring and schedules for each T, with all resources charged. Local state, degree, density, update rate and information speed v are bounded independently of T. Autonomous fabrication and translation-invariant self-organization are not extra requirements.

This final [uniform-horizon refinement](package/independent/fault_tolerance/uniform_horizon_refinement.md) governs the selection. It is neither one compulsory autonomous machine nor a weaker family allowed to increase its initially input-dependent seed with T. Immutable local gate laws and the bounded-rate input-independent schedule are declared premises; every mutable control record is exposed to faults.

The governing locality is strict finite-speed local circuits. Poisson local update clocks and Lieb-Robinson tails need an additional probabilistic-cone bridge. A physical platform must earn its gates, clock, noise law, commissioning and terminal interface.

## A reset burst can erase every accessible distinction

Burst centers form a Poisson process of intensity `lambda dz dt`. A radius-R burst affects `z+[-R,R]^d`. The negative theorem uses input-independent reset of all accessible mutable state in that cube, a subcase of the arbitrary-corruption class the positive theorem should tolerate. A known reversible flip is a different fault.

At time t, every initial-bit difference is inside `C_t=[-(r0+vt),r0+vt]^d`. Complete-cover resets by T have Poisson mean

```text
Lambda(T)=lambda 2^d integral_0^T E[(R-r0-vt)_+^d]dt
 =lambda 2^d/[v(d+1)]
  *E[(R-r0)_+^(d+1)-(R-r0-vT)_+^(d+1)].
```

The last expression is the expectation of the difference, not subtraction of separately infinite moments. With finite E R^d it is finite at each finite T. Coupling the two input worlds through the same outside resources, random faults and future controller randomness gives

```text
TV(P_0^T,P_1^T)<=exp[-Lambda(T)],
P_error(T)>=(1-exp[-Lambda(T)])/2,
I(B;X_T)<=exp[-Lambda(T)] H(B).
```

A complete-cover reset removes every accessible distinction. Even a free global decoder cannot beat this lower bound, so local adaptive repair, replication and subsequent computation cannot evade it within the support/propagation contract. The bound is uniform over the permitted horizon-specific hardware families with the same fixed seed radius.

Consequently, finite E R^d with infinite E R^(d+1) forces recovery error to 1/2 for every finite seed. Finite E R^(d+1) only removes this obstruction; it is not a sufficiency theorem.

## Finite local damage does not imply persistent information

A point is hit at finite rate `lambda 2^d E R^d`. Pareto exponents `d<alpha<=d+1` therefore have finite local hit rate but inevitable forgetting. In two dimensions, alpha=5/2 is a concrete example with finite mean damaged-area flux. Finite mean disturbance power additionally requires a declared energy-per-damaged-volume model; no universal erasure-energy law or instantaneous-power bound is inferred.

For scales a>=1, define `C_(d,alpha)=Gamma(d+1)Gamma(alpha-d)/Gamma(alpha)`. Then `E(R-a)_+^d=C_(d,alpha)a^(d-alpha)`. The complete-cone hazard grows as `T^(d+1-alpha)` for d<alpha<d+1, as log T at equality, and converges for alpha>d+1. Corresponding distinguishability bounds are stretched exponential, power law, or a nonzero upper limit respectively. That last limit is not achieved recovery.

If all information remains within radius `a(t) approximately t^gamma`, finite complete-cover hazard requires `gamma(alpha-d)>1`. Finite speed restricts gamma<=1. This is a necessary support-growth condition, without asserting that a filled cone or any expansion policy succeeds.

The [readout/resource page](readout-and-resources.md) gives the seed-extent and fixed-device ceilings. The [proposed multiscale construction](construction-and-comparators.md) remains the central missing operation. Earlier productive-control, repair and Gibbs/LTI results are preserved at their own scopes, with no physical reduction to this burst model. Capital ran no new scientific audit, check program or heavy build. Generated current retrieval was not rebuilt.
