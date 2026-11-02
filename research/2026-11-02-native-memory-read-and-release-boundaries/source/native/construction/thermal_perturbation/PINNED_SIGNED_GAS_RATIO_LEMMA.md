# Independent normalized pin-ratio lemma for the signed clock background

2026-11-02. **Proved scalar-gas interface.** This does not by itself prove that arbitrary native Hamiltonian insertions possess the required mixed-gas representation. That exact representation is a separate construction gate.

## 1. General lemma

Let a finite-volume continuum gas have complex activity measure mu and symmetric pair factor h(x,y), |h|≤1. Let f=h−1. Suppose a(x)≥0 satisfies

    integral |mu|(dy) |f(x,y)| exp(a(y)) ≤ a(x),
    integral |mu|(dx) exp(a(x)) < infinity.

Use the absolutely convergent logarithm and rooted bound of Ueltschi, math-ph/0304003v3, Theorem 1 (primary source personally checked in the preceding rod audit).

A fixed external pin gamma may delete or phase-modify each background polymer separately by a measurable factor k_gamma(x) with |k_gamma(x)|≤1. Define

    L(gamma)=integral |mu|(dx) |1−k_gamma(x)| exp(a(x)).

Then, for any finite list of pins,

    exp(−sum_i L(gamma_i))
      ≤ |Z[mu product_i k_gamma_i]/Z[mu]|
      ≤ exp(sum_i L(gamma_i)).                         (1)

All involved partition functions are nonzero. Pair interactions between the fixed pins, if present, multiply this ratio separately; their modulus at most one only helps the upper bound.

### Proof without a positive-gas assumption

First add one pin by replacing its factor with k_u=1+u(k−1), 0≤u≤1. The unit disk is convex, so |k_u|≤1. The modified measure is dominated by |mu|, and the SAME KP condition and rooted estimate hold throughout this interpolation. The absolutely convergent logarithmic series gives

    |d/du log Z[mu k_u]|
      ≤ integral |mu|(dx)|k(x)−1| exp(a(x))=L(gamma).

This is a derivative with respect to the measure, not division by k_u, so zeros of an individual k_u cause no problem. Integration bounds the complex logarithm increment, hence also its real part. Repeat for each pin; already inserted factors have modulus at most one and do not increase the bound. This proves (1). No global operator norm, partition-function lower bound exp(−c volume), exponential operator monotonicity, or positive classical probability measure is used.

## 2. Full-time clock columns are legitimate pins IF their interaction factorizes

Suppose a fixed column trajectory gamma occupies a finite set C of clock sites for the whole imaginary-time circle. Its factor with an outside ordinary/wrap rod is zero for forbidden same-clock occupancy, otherwise a scalar phase of modulus at most one. Suppose it equals one outside the clocks in C and their bounded overlap neighborhood. Then L(gamma) depends only on |C| and the actual clock parameters, not on total volume or the detailed internal trajectory.

With the preceding rod audit's charge a0+b l, d=Delta−2t−b≥Delta/2 and exp(a0)≤2, the ordinary-rod contribution per affected clock is bounded by

    2 beta integral_0^beta 2t² exp(a0) exp(−d l) dl
       ≤16 beta t²/Delta.

The wrapping contribution per affected clock is at most

    2 (K−1) exp[−beta(Delta−2t−b)+a0].

If at most D|C| clocks are affected, then

    L(gamma) ≤ D|C| [16 beta t²/Delta + 2 Wcharged],
    Wcharged=(K−1)exp[−beta(Delta−2t−b)+a0].             (2)

The constants are conservative. The same statement holds for weighted majorants after incorporating their per-rod inflation. In particular a normalized external-gas factor costs exp[O(beta t²/Delta)|C|], not exp[O(volume)]. Excited states inside the columns are unrestricted; they must be charged in the column's OWN activity, not discarded.

(2) is conditional on genuine pairwise scalar pin factors. An arbitrary operator insertion is not automatically such a pin. Full-time column construction must establish that all affected clock fluxes are internal to C, that outside clocks still have constant initial-syndrome flux, and that all remaining interactions with outside rods are these scalar factors.

## 3. Matrix-valued exceptional columns

The same ratio estimate controls large logical columns without taking a matrix logarithm. Suppose the small-column/clock background is a scalar gas satisfying KP. Assume a large column trajectory gamma carries a finite logical operator A_gamma; compatible large columns multiply in the exact gas representation, and all remaining pair factors have modulus at most one. Assume every large column is an admissible test pin with L(gamma)≤a_large(gamma).

Expand by the set of large columns first. The scalar background remaining with those fixed columns is exactly a pinned partition function. Applying (1), bounding operator products by the product of their norms, and dropping all modulus-at-most-one interactions gives

    || W / Z_small − I_logical ||
      ≤ exp[ integral_large ||A_gamma|| exp(a_large(gamma)) d|nu|(gamma)]−1.  (3)

The integration convention includes the column's scalar activity. Formula (3) is a direct series bound, not an operator-log or simultaneous-diagonalization claim. It remains valid for noncommuting operator products if the exact gas specifies their chronological ordering; in the proposed disjoint-data-support representation compatible components in fact commute.

If a nonscalar component requires at least d/b distinct perturbation labels, a connected-label majorant lambda^m with bounded-degree counting would make the exponent in (3) at most C n lambda_0^(d/b). Bath-only columns are always scalar and need not be truncated. Only memory-touching exceptional columns must be anchored at O(n) memory labels, avoiding total bath-volume charges.

For actual positive projected Gibbs weights, (3) with remainder r<1 implies comparison to |Z_small| within factors 1±r (after the fixed logical multiplicity). A separate assertion that every intermediate signed scalar partition function is a positive probability weight is unnecessary. Differences of log|Z_small| are bounded by absolute complex log differences, and hence suffice for the positive witness ratio.

## 4. Remaining theorem gates

The following are not proved merely by (1)–(3):

1. Exact mixed-column/rod bijection for arbitrary dressed native V, including clock matrix units and data syndrome histories.
2. A bound on the integrated primitive-column activity, with every local clock dimension, unrestricted internal hopping history, repeated V label, bath trace and time-order multiplicity charged.
3. A simultaneous KP criterion for columns and rods, uniformly in syndrome. The column activity can be extremely small in beta-dependent constants; beta is fixed, so this does not require strength scaling with volume.
4. A local syndrome-influence estimate for the column-containing scalar logarithm. The existing polynomial stabilizer filling controls which initial syndrome bits a small closed data-Pauli product depends upon; it must not be charged as exp(the entire filling volume) in the column activity.
5. Exact anchoring and counting for exceptional memory-touching columns.

If these gates close, the earlier actual Gibbs rare-bad and logical-twirl argument can be reused without a T times global simulation error. This lemma supplies the normalized signed-background comparison needed at the most delicate ratio step; it does not itself declare the robust-native-memory theorem complete.
