# Independent whole-proof and receiver review

## Verdict and source boundary

**Accepted for the precise raw architecture, structural equivalence and mathematical receiving interfaces stated below, after repairing the qualitative receiver's work-accounting validation.** The ordinary proof, exact rational cone constructor, discrete generator inequalities and final qualitative receiver were independently reconstructed. No mathematical theorem correction was required. The repaired accounting issue did not produce a false recurrence conclusion, but did admit a false zero-work receipt; its original acceptance and corrected rejection are preserved as a regression.

This is internal mathematical/code review, not external refereeing, historical-priority clearance, a security audit, or a general weak-reversibility theorem.

| Final object | SHA256 |
|---|---|
| `PROJECTIVE_SUPPORT_THEOREM.md` | `439c727065e56787308d9b0007d76a504c05cb8d1c1eeb75077578de06624014` |
| `projective_mass.py` | `bfb4421b8c353067f3ec504e1cc62135f706d530be7fd83800042a371268d234` |
| `structural_receiver.py` | `f70468cfd58c5b2874f7e6d7fc78c5fc75cfb3ffd68f438b937855e33d69c5d8` |
| `results.json` | `172ab1a0125d2254326723a90ad51135debda87917a8ee9fb79783b4671e78ef` |
| `exercise_results.json` | `1a203aa8ed898b467268708826317ed2f6200d112d3ba19edce86ab3fe6de23b` |
| `qualitative_results.json` | `f654ba5b76ea04eb4720714ac76d6ba6529895a1a0ce45c6a0b55247158f7254` |

The initial receiver hash was `be9c6a31c6910c8f45ee2c5196d7ac729691ad889f17dd35b8000283034a3020`; its initial qualitative results hash was `0fa0512816b29b701151187c59edc56fcaa241e1d9ea9203353f423ebc2758f9`. Only the receiver and its output changed at this review boundary. Both old objects and final frozen copies are retained under `independent_audit/`. The proof, quantitative code and quantitative outputs stayed unchanged.

## 1. The structural result really earns the missing acquisition step

The family has `n>=2`, one directly immigrating/dying coordinate A, total-conservative internal channels, and full weak reversibility. Let `p=max(2,maximum internal source order)`. The finite support test uses only order-p channels. It is a leading-field support test, **not** literal one-copy stochastic activation.

The proof establishes an exact equivalence:

- every singleton support closure reaches A;
- some degree has a homogeneous polynomial in the Bernstein coefficient box whose highest-order generator polynomial has nonnegative boundary coefficients and strictly positive pure-satellite coefficients.

The successful direction does not assume a favorable polynomial or stationary-fiber oracle. I checked its complete constructive chain:

1. Raw rate bounds give `C=max(1,p^3 sum rates)` and a short rational horizon `T=1/(4C)`.
2. Equal-block Euler propagation through at most `n-1` support additions gives the uniform terminal A lower bound from the stated rational level recursion. The two conservative survival factors still exceed the recursion's factor one quarter. Earlier-coordinate bounds are maintained through the remaining horizon.
3. Infinity-norm derivative estimates, the binomial/geometric Jacobian bound, and the Hessian chain rule give the stated `3CT^2` Hessian bound for the finite Euler sum.
4. Its exact discrete coboundary and Taylor remainder give a strictly positive directional derivative on `A=0`, once the explicit M bound is met.
5. The homogeneous Euler components have nonnegative coefficients and sum to `N^p`. Compositions, homogenization and averaging therefore preserve the entire Bernstein box. No pure-A coefficient may be forced to one in this completeness construction.
6. Homogenization transfers the tangential Lie derivative because `v dot grad N=0`.
7. The falling-factorial identity for elevated coefficients is exact. The displayed error bound is conservative; an independent with/without-replacement coupling gives the stronger per-monomial error `q(q-1)/(2r)`. Finite elevation therefore produces the required positive coefficient cone.

A crucial interface distinction is correctly retained in the final proof: derivative/Hessian estimates concern the **inhomogeneous** map `y+h v(y)`, not the homogeneous coefficient map `y_i N^(p-1)+h v_i`. They agree on the simplex, and only the tangential derivative is transferred afterward.

The negative direction is also valid and finite. Failed support closure yields a nonempty invariant simplex face disjoint from A. At a maximum of any candidate H on that face, its derivative along an inward Euler step is nonpositive. Strict positive boundary-cone drift would make that derivative positive. Thus the returned closed face obstructs **every degree of this fixed-raw-top-order cone**, without an infinite search.

The structural theorem allows positive real rates mathematically; the executable constructor and receiving interface use exact rational rates. The latter distinction is explicit rather than hidden in numerical tolerances.

## 2. One cone receipt gives the claimed global count-process bound

I independently expanded the actual falling-factorial generator, not just its fluid leading term. If H has degree d, then the leading part has degree `q=d+p-1`, and the remainder has degree at most `q-1`. The raw coefficient bounds imply

    L_internal H >= beta sum_j B_j^q-K A N^(q-1)-C_R(N+1)^(q-1).

Every negative A-containing monomial is at most `A N^(q-1)`; the absolute-coefficient remainder bound is valid on every nonnegative integer state. These are acquired finite computations after the polynomial is found.

The denominator `(N+1)^(d+p-2)` is essential. It makes the full exact internal quotient

    -epsilon L_internal H / [(N+1)^(q-1) h],

and reduces adverse leading terms to order A and remainder terms to a constant. The Bernstein box gives `0<=H<=N^d` and `partial_A H<=d N^(d-1)`. The discrete death correction is bounded as stated; immigration uses the uniform positive lower bound on h. Neither an extinction-face limit nor a derivative at a negative count is used.

Sign-sensitive denominator bounds, epsilon absorption and the split `A>=N/2` versus satellite total greater than `N/2` yield exactly the reported `C0-kappa N`. N zero is separately covered. I found no missing boundary stratum or stationary averaging premise.

Full source coefficients, Bernstein coefficients, the exact H/LH/leading/remainder polynomials, K, C_R, beta, epsilon, radius, rational-power Foster expression and conservative bit bounds were independently reconstructed from the raw receipt. Both exact solver paths and all residuals were checked.

## 3. Recurrence, nonexplosion and moments have the right scope

Nonexplosion already follows from a simpler conventional comparison: only constant-rate immigration increases total population, so initial N plus its Poisson count confines the process to a finite count set on each finite time interval. Arbitrarily high internal order does not cause explosion inside that finite set. This is not presented as a new nonexplosion principle.

Weak reversibility gives a feasible return path for every enabled jump by translating a reverse complex path by the nonnegative residual population. Communicating classes are therefore closed. The normlike Foster inequality yields classwise positive recurrence, without global irreducibility. The full-WR guard matters: top-order accessibility alone can coexist with transient communicating classes.

The stationary exponential-moment proof is noncircular. Stopped exponential Dynkin gives `P_s W<=aW+b`, with `a<1`; invariant-measure concave truncation and Fatou then give `pi(W)<=C_F/zeta`. No initial assumption `pi(W)<infinity` is made. Comparability with `t^N` proves the moment at exponent `log t`, including its endpoint. Repeating for arbitrary larger t proves every finite exponential count moment. These tails follow from the exact count-specific generator inequality, **not** generic fluid stability.

## 4. The cone hierarchy is not a stability decision

The invariant-face obstruction is exact for the specified strict leading cone, but lower-order restoration can make the network stable anyway. The all-rate-one full-WR example

    0<->A, A<->B, A<->C, 2B<->2C

has obstructing top support `{B,C}`, yet

    V=4^A 5^(B+C),       LV/V=3-A/4-(B+C)/5.

The constructor and qualitative interface correctly leave actual stability UNKNOWN when returning the all-degree cone obstruction. Independent exact checks reproduce this conventional comparator. Earlier accepted certificates with individually neutral higher-order channels can similarly succeed when the new raw-top-order criterion fails. They must remain available in parallel.

For the small opposing-pure-ray family, a linear weight cannot be positive on both pure B and pure C rays. The polynomial search really crosses that particular linear-cone obstruction. But the independently derived nonsmooth inventory

    P=A+eta min(B,C)

also gives a direct regenerative lower bound for the whole positive-rate family. Its proof is retained in `independent_audit/mechanism/MECHANISM_AND_COMPARATOR.md`. Polynomial degree two is not uniquely necessary for this example. The broader result is automatic acquisition and the exact finite support-vs-cone boundary, not a claim that a chosen smooth polynomial defeats all conventional Lyapunov methods.

## 5. Qualitative and quantitative outputs are genuinely separate

The qualitative interface reconstructs the raw architecture, full graph return property and support paths directly. It can certify the structural theorem without forming H, searching polynomial degrees, performing Euler steps, computing the huge scalar Euler bound, or using a stationary law. It returns no numerical Foster constants, tail prefactor, mixing rate or sampler.

I guarded the quantitative entry points to raise if called and successfully ran the qualitative interface on an encoded order `p=10^6` case. The supplemental order `10^50` receipt and a five-species four-stage support chain with the open coordinate last were also independently reconstructed. Their finite raw/support validation is not credited with expanding the corresponding count propensities or Euler polynomials.

A capped quantitative search can still return explicit-certificate UNKNOWN when qualitative recurrence is already certified. The main proof and receipts distinguish these statuses correctly. A basis cap is **not** a total resource cap: polynomial preprocessing, scalar bound arithmetic, memory and total rational bit-work are not capped by it. The final README states this limitation accurately.

### Accounting repair actually required

The original qualitative verifier checked path validity but accepted a receipt claiming zero support-reaction scans and zero coordinate-test work while verifying four support steps. I reproduced this exactly; it was a receipt-accounting defect, not a false recurrence proof.

The final receiver independently replays the deterministic first-enabled support scan, binds the complete trace, and checks both recorded scan counts. The original zero-count receipt is now rejected. The regression script loads both frozen versions to demonstrate the transition. Mathematical conclusions, executed-work claims and numerical-output claims are all separately checked in the final tests. The receiver remains ordinary research validation code, not a hardened malicious-input service or formal proof assistant.

## 6. Independent exact execution

`independent_audit/verify_projective.py` uses its own polynomial expansion, falling-factorial construction, forward-elimination solver and finite constraint/basis reconstruction. Candidate code supplies receipts only. It verifies every boundary constraint and replays the first positive basis, including exhausted preceding degrees.

| Case | Degree / raw order | Total candidate-basis attempts paid through acceptance | Independent ordinary states | Targeted states |
|---|---:|---:|---:|---:|
| Opposing-rays demo | 2 / 2 | 10628 | 680 | 25 |
| Cubic lift | 2 / 3 | 15320 | 680 | 25 |
| Base 65/64 | 2 / 2 | 10628 | 680 | 25 |
| Base 100, compact constant | 2 / 2 | 10628 | 680 | 25 |
| Additional rational-rate two-species quartic case | 1 / 4 | 12 | 231 | 20 |
| Species-permuted demo | 2 / 2 | 8307 | 286 | 25 |

Totals: **3,237 additional ordinary exact generator checks and 145 targeted checks**, including counts `10^50`. The stronger intermediate polynomial-production and quadratic/power drift bounds were checked, not only the final linear inequality. These finite tests supplement the ordinary all-state proof and are not a simulation-based recurrence claim.

Sixteen quantitative receipt mutations were rejected, covering H, LH, leading/remainder polynomials, Bernstein coefficients, constraints, residuals, active basis, beta, K, remainder bound, denominator degree, formal Euler M/degree description, Foster coefficient and bit bound.

The qualitative audit rejected **21 receipt or rebound-raw mutations**, including false support additions, missing seeds, wrong roles/orders, broken WR, false recurrence/instability conclusions, unsupported execution claims and the repaired zero-work receipt. Exact-domain invalid inputs were also rejected. Null normalization, split-rate input and permutation controls passed.

All three main outputs, plus the supplemental qualitative controls, replay byte-identically. The independent larger-support reconstruction checks the five-species chain and encoded order `10^50` without relying only on the parent's assertions.

## 7. Essential cubic scaling control, not just accepted syntax

For the cubic lifted demo, the constructor acquires

    H=2AC+(2/3)BC,

which differs from the base demo's H. I independently verified the exact identity `L3=(N-2)L2` for this **same acquired H**. Its leading quartic polynomial equals `-8/3` at direction `(1,0,1)`. At the recorded states `(n,0,n)`, with n up to `10^50`, the unattenuated denominator `(N+1)^2` gives positive quotient and the corrected denominator `(N+1)^3` gives negative quotient. Both exact recorded quotient values were independently recomputed.

A separate earlier control uses the base H on direction `(4,3,3)`, where the cubic lift has leading drift `-30n^4`; it is also valid but is not confused with the constructor's different first vertex. This distinction records the corrected original wrong-ray test assumption rather than hiding it.

## 8. Costs and unexecuted formal witness

The base demo exhausts 330 degree-one bases and accepts after 10,298 degree-two attempts, 685 nonsingular, among 31,824 candidate degree-two bases. Its actual degree-two expansion records 280 formal multiplication term pairs, 45 nonzero generator monomials across six basis polynomials, and small coefficient sizes. The operation counter was inspected at its loop; independently reconstructed monomial counts and coefficient-bit maxima agree.

Its 56,192,254,840 possible finite exception states are bounded analytically, not enumerated. Its Foster constant is factored, with conservative unreduced numerator/denominator bit bounds 13937/6977, and the 12,000-bit serialization guard prevents an expanded decimal conversion claim. Small and large requested bases exercise the same compact mode.

The formal support-to-polynomial termination construction is incomparably larger. Independent scalar arithmetic for the tiny base demo reproduces

    M=3114770565929806197921153024,
    initial homogeneous degree=2^(3114770565929806197921153023),

before further coefficient elevation. **Only the scalar arithmetic and factored degree were executed.** No such polynomial or coefficient list was materialized. The formal recipe proves unbudgeted acquisition termination; it is not a practical worst-case algorithm claim. The inexpensive qualitative receiver and actual low-degree LP search remain distinct outputs.

## 9. Ordinary machinery, audit history and final limits

The independent mechanism notes reconstruct the entire support/Euler/coefficient-elevation argument without an inaccessible theorem as a premise. They also retain the nonsmooth comparator, the stable all-degree obstruction, exact coefficient-elevation tests and the arbitrary-order scaling counterexample. Their byte-identical copies are included under `independent_audit/mechanism/`.

`SOURCE_SCOPE.md` separately records the main agent's inspected primary-source scope: ordinary Petri-net/invariant-face geometry, queueing fluid comparisons, the distinction between fluid stability and exponential tails, and classical Pólya positivity. This review does not upgrade abstract-only or one-page source inspection into a full-paper proof audit. No historical priority is established, and no denied or gated transfer was retried.

Minor independent harness issues were identified and corrected without changing the candidate mathematics: newly proposed in-memory tuples needed normalization to the JSON receipt representation, and one supplemental script's output path duplicated the working directory. Their terminal failures were inspected before corrective execution. The substantive receiving-accounting repair and the parent's earlier wrong-ray/serialization test corrections are explicitly preserved. No pending execution or uncertain transfer remains in this audit.

The accepted result is restricted but consequential: a finite raw leading-support test is exactly the boundary of a particular acquired polynomial certificate hierarchy, and the resulting class has a count-specific all-exponential Foster theorem with a separate finite qualitative interface. It is not a recurrence decision for arbitrary conservative internal dynamics or arbitrary weakly reversible networks. Earlier accepted packages and previously delivered archives were left untouched.
