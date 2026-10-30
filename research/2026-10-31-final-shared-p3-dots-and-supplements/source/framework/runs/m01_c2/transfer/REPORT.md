# A successful restricted transfer to the exceptional face

The positive rank-one Hessian quadrature transfers to the actual F0=|w|⁴+2|z|²|w|² and yields a new compatible theorem beyond the frozen characteristic-polarized triads. It does **not** prove global QC of P0 or of the full exceptional face.

The stronger result applies to every globally ROC polynomial with leading cF0, c>0, every admissible cubic in the actual eight-dimensional space, and its actual quadratic. It gives:

* **An all-amplitude resonant triad:** for phi=a e1 sin(x+theta0)+b e2 sin(y+theta1)+d(e1+e2) sin(x+y+theta2), the energy gap at every mean is at least 2c times the fourth gradient moment. All amplitudes and phases are allowed.
* **A genuine overlap:** for psi=e1 sin x+e2 sin y+(e1+e2) sin(x+y-delta1)+(1/2,1/4) sin(2x+y-delta1-delta2), the gap is at least (3/2)c times the fourth gradient moment, uniformly in both relative phases, every mean and every overall amplitude. Its four relative amplitudes are fixed.
* **Unbounded separated blocks:** any finite mixture of these block types at frequency scales 9^j, with their potentials divided by their scale, satisfies gap >= c times the total fourth gradient moment. The constant is independent of the number of blocks. Each block can have its own proper output rotation and allowed parameters.

P0 has c=1. The original task's leading quartic is F0/3, so c=1/3 there. These are restricted compatible inequalities, not an assertion that the block classes exhaust or are dense in gradients.

The scientific bridge was derived rather than imported with Ultra's different quartic. For fixed P0, only five matching conditions are required: its cubic moment and four translation moments to retain all means. Their minimum-cost quadrature is a finite five-by-five Gram calculation. On the triad it gives

    E_min = kappa² 2ABD(A+B+2D)/(2AB+D(A+B)),

where A=a²,B=b²,D=d² and kappa=cos(theta0+theta1-theta2). Thus matching every other lower cubic was not imposed on the fixed-polynomial problem.

A simpler explicit construction then earns the full-face result. The field's original three rank-one rays suffice; unlike Ultra's twelve-mode example, no covariance exchange is needed for this eight-mode face. In conformal coordinates take

    X0=(0,0,-1/4,0), X1=(0,0,1/4,0), X2=0.

Their cubic functional matches all eight actual admissible cubics exactly. Their quartic cost is kappa²D(A+B), and the entire remaining budget is the identity

    f-E-2<|G|⁴>
      = (A+B-8D)²/16 + 2D² + 5(A-B)²/16
        + (1-kappa²)D(A+B) >= 0.

This retains the actual ROC quadratic through the positive Hessian identity. The new safe family has active P0 correlation: its unit-amplitude triad has r=-4/7, so vanishing third moments do not explain the result.

The overlapping block was reconstructed by exact Fourier convolution, including both fourth-order interference terms. Four original covariance rays and finite rational backgrounds match both cubic targets simultaneously. Its phase-independent budget lower bound is 1570767021/29796352; its fourth gradient moment is at most 57043/2048, which proves the stated 3/2 factor. The complete literal matrices and coefficients are in overlap_exact.txt.

For separated blocks, the decisive F0-specific fact is stronger than a numerical cross bound: on every pair of rank-one matrices, the F0 cross-Hessian dominates the cross-Hessian of |A|⁴. In normalized angular variables their difference is

    6(s+t)² + 8(1-s²) >= 0.

This and exact frequency separation give the uniform constant c for arbitrarily many blocks. Unrestricted overlapping networks remain outside the proof.

`PROOF.md` contains the complete argument, including all-mean matching, source credits and precise quantifiers. Exact replays:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 receive.py
PYTHONDONTWRITEBYTECODE=1 python3 overlap.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_identity.py
```

All passed. The last receiver independently reconstructs an actual rational-phase periodic gradient's P0 energy at a nonzero rational mean and verifies exact equality to the positive quartic budget plus three nonnegative rank-one Hessian evaluations. This is implementation validation; the continuum statements follow from the exact symbolic identities. `construct.py` and `full_face.py` retain the minimum-cost constructions and rational formulas. A nonnegative-coefficient shortcut for an optimized rational cost is unnecessary: the explicit three-square identity above supplies the global amplitude certificate.

The abstract quadrature identity, overlap pattern and separated-block strategy are credited to the two authorized Ultra proofs. Their F*, twelve modes, rays and numerical certificates were not assumed valid for F0. The actual exceptional cubic space and P0 ROC admission retain their checkpoint credit. This new work is confined to this transfer directory and leaves the frozen trial outcome unchanged.

The unresolved frontier is still global QC of P0, arbitrary compatible resonance networks, and the full exceptional face. No negative-energy compatible field was obtained. No finite collection of passing fields is being promoted to global QC.
