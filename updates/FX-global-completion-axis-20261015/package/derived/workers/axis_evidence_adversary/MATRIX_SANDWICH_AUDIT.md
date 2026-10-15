# Independent audit of the root-supplied matrix-sandwich lemma

Date: 2026-10-15. Status: conditional mathematical characterization; no acquired material response. The root agent supplied the candidate lemma by message. This file reconstructs it independently and audits its measurement interface and zero-floor edge case.

Let an unoriented chemical axis be represented by a unit vector n, identified with -n. Let dV be ordered-phase volume in a fixed region of interest, S its local long-range order, and

    M = integral nn^T dV,  trace M = f,
    W = integral S^2 nn^T dV.

Assume all domains in that region satisfy an independently established common bound 0<s<=S<=1. In particular, s is not a bulk average order parameter, a value from another specimen, or an assumed precursor value.

For 0<s<1 the exact feasible set of M given W,f is

    M symmetric, M >= 0, trace M=f, s^2 M <= W <= M,

where matrix inequalities are in the positive-semidefinite order. Necessity follows by integrating (S^2-s^2)nn^T and (1-S^2)nn^T, both positive semidefinite.

For sufficiency define

    P=(W-s^2 M)/(1-s^2),
    R=(M-W)/(1-s^2).

Both are positive semidefinite. Moreover P+R=M and P+s^2 R=W. Decompose each into spectral atoms: an eigenvalue lambda and unit eigenvector n contribute volume lambda at axis n. Set S=1 on P atoms and S=s on R atoms. These atoms realize exactly M,W and volume f. P and R need not commute; they are different subpopulations, so a common diagonal basis is unnecessary. This is an abstract realization over unrestricted admissible axes. If known parent grains or a substrate restrict allowed axis support, the spectral atoms may be unavailable; the sandwich is then necessary but not automatically sufficient for that support-constrained model. For known global x/y/z axes the support-constrained problem instead reduces to componentwise inequalities and a linear program.

Consequently every linear volume-axis contrast has sharp bounds from a 3x3 semidefinite optimization over that set. For the proposed D, use trace(diag(1,-1,0) M)/f with f>0. If f=0 then M=W=0 and normalized Q is undefined. A feasible trace must satisfy s^2 f<=trace W<=f, but these scalar conditions alone do not encode all matrix information.

At s=1, M=W and trace W=f. At s=0, allowing S=0 gives the closed feasible set W<=M, M>=0, trace M=f. If "ordered" requires S>0 almost everywhere, the exact set additionally has ker W=ker M. To prove necessity, v^T W v=0 implies integral S^2(v.n)^2 dV=0; positivity of S implies v^T M v=0. Since W<=M gives the reverse inclusion of kernels, the kernels agree. For sufficiency, restrict to their common support. The minimum generalized eigenvalue of (W,M) is positive there, giving a positive s^2 with W>=s^2 M; apply the preceding construction. The closed s=0 set is only a closure if extra volume in a null direction of W is permitted. For example M=diag(1/2,1/2,0), W=diag(1/10,0,0) satisfies the closed inequalities but cannot arise with S>0 on all ordered volume.

## Acquired versus missing information

The characterization starts only after W is an acquired, calibrated physical moment. It cannot turn an assumed scattering response into an observation. It needs:

- Absolute superlattice intensity calibration to volume and order, including incident flux, absorption, footprint, polarization, detector response, finite angular coverage and correct integration of broadened/split scattering.
- An independently acquired f for the same marked material. Bulk elemental volume, magnetic volume, an L10 Rietveld fraction, and a threshold-defined locally ordered fraction are different quantities.
- A valid common lower bound s for every included domain or a rigorous weaker model of heterogeneity. Reported powder S=.71 and film S=.87 are aggregate intensity estimates and provide no such lower bound.
- A verified additive intensity regime. The primary Frisk 2016 resonant-XRD study shows that antiphase domains within coherence can suppress or split a superlattice peak. Therefore a narrow Bragg window need not equal the intended integral of S^2.

When calibrated measurement uncertainty is a convex set C for W and an interval for f, include W and f as optimization variables in those sets. This is a decision operation only if the lower bound on the orthogonal-loading contrast remains separated from zero after accounting for all controls and uncertainty. Without measured f,s,W, an SDP result is conditional mathematics.

Even a certified change in M establishes a distribution change. It does not prove same-grain reorientation: dissolution, nucleation, growth, fragmentation, volume loss and whole-particle rotation can alter M. The same marked grains or a validated population/mass-balance tracking scheme remain necessary for the stronger rewrite claim.

`check_measurement_design.py` reconstructs P and R for an intentionally noncommuting synthetic example and checks the exact rational countermodels. The check is not a proof of the physical measurement model or experimental validation.
