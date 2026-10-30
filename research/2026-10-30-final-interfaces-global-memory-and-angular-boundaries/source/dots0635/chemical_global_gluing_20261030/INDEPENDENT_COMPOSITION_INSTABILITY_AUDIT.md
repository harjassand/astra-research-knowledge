# Independent audit: frozen boundary composition instability

Reviewer: finite_phase_drift_challenge, 2026-10-30. Internal mathematical audit, not external novelty certification.

## Verdict

The stated counterexample passes the full audit. It refutes the specified fixed-alpha, fixed-fugacity frozen-count finite-phase resolvent extension, for every finite B strip containing phases 0,1,4. It does not refute recurrence of the original network, nor every possible finite-dimensional correction representation.

## 1. Graph, drift, and unavoidable positive tilt

The connector joins zero, A+B, and 3A+4B in a directed cycle; the reversible fast chain joins all its other complexes to 3A+4B. Thus the complex graph is strongly connected. In species order (A,B,C), the vectors (1,1,0), (3,4,0), and (-1,0,1) are linearly independent (determinant 1), so the stoichiometric rank is exactly three.

The increasing-A fast rates, divided by (B)_4 C^3, approach 6+r+7r². The decreasing rates approach 12r+r²+r³. Their difference is exactly -(r-1)(r-2)(r-3).

For t>0,

    H=b(t−1)+d(t^−1−1)=(t−1)(b−d/t),

so its nonpositive interval is precisely the interval between 1 and d/b. On (1,2), b<d and nonpositivity requires t≥1; on (2,3), b>d and it requires t≤1. A strictly increasing t=k r^alpha cannot satisfy both conditions for every r. Therefore every fixed k>0 and alpha in (0,1) gives H>0 somewhere. Furthermore t→0 and d/t=O(r^(1−alpha))→0 as r↓0, so H→−6. A positive component of the open set {H>0} has a finite left boundary r0>0 with H(r0)=0. Taking r in that component sufficiently close to r0 yields 0<H(r)<r³. This selection is rigorous even if H has multiple components.

## 2. Exact principal block and characteristic asymptotics

Let c_A>0 be the fixed A fugacity. The positive connector entries in the ideal matrix on phases (0,1,4) are exactly

    g01=c_A^−1 A^alpha,
    g14=c_A^−2 A^(1−alpha) (A)_3^alpha,
    g40=24 c_A^3 (A)_3^(1−alpha).

Their product is exactly 24 A(A)_3, independently of alpha and fugacity. A fixed fugacity in B merely adds phase-similarity factors and also cancels around the cycle; C has no connector displacement. The fast chain is same-phase in this frozen construction, so it changes only the phase-4 diagonal.

At phase 0 the diagonal is -1; at phase 1 it is -(A+1). At phase 4 it is

    -(24(A)_3+4A+1)+24 C³ H(A/C)+o(C³),

with the last error uniform for A/C in a fixed compact positive neighborhood. These are all the diagonal losses: phase-4 immigration contributes 1, its A+B connector contributes 4A, and its clear reaction contributes 24(A)_3. Gains leaving the principal block do not remove their outgoing losses.

Hence the exact characteristic polynomial has the three diagonal factors minus g01*g14*g40. Along C=n and A=floor(rn) (or any integer rounding with A/C→r), division by 24 A^4 converges uniformly for bounded real lambda to

    (lambda+1)(1−H(r)/r³)−1.

The limiting root lambda*=H(r)/(r³−H(r)) is strictly positive and simple. Uniform convergence and opposite signs on either side of this root give a positive real root of the finite-n characteristic polynomial for all sufficiently large n. A principal submatrix's spectral abscissa is bounded above by that of the full Metzler matrix. Consequently the full strip matrix is not Hurwitz. The same principal block and its outgoing losses persist for every fixed K≥4.

This also directly rules out a positive pointwise vector v with M^T v strictly negative at these counts: such a vector for a Metzler matrix would imply Hurwitz stability. It does not rule out spatially varying corrections whose actual count-shift terms cannot be discarded in the frozen operator.

## 3. Physical-class path: all firings enabled

For a target (A,C,4) with A≥1, put N=A+C≥1. After 4N immigration firings the state is (A_count,B_count,C_count)=(4N,4N,0). After C fast conversions 3A+4B→2A+C+4B it is (4N−C,4N,C). During these conversions A_count remains at least 4N−C≥3N+1≥4, and B_count≥4, so each is enabled.

After twelve A+B→3A+4B firings the state is (4N−C+24,4N+36,C). During N+8 clear firings it ends at

    (4N−C+24−3(N+8), 4N+36−4(N+8), C)
      =(A,4,C).

Before the last clear firing the counts are A+3≥4 and B=8, hence all earlier clear firings are enabled too. Connector firings clearly have sufficient A and B throughout. Weak reversibility gives an enabled reaction-graph return path for each individual firing: if the forward step leaves residual z, the return path carries the same nonnegative residual z. Reversing the list in this way proves communication with zero. Thus all asymptotic states used really belong to one closed communicating class of the weakly reversible state graph.

## 4. Exact distinction from the accepted leaky-strip lemma

The lifted vertices (B=0,a=0), (B=1,a=A), and (B=4,a=3A), together with the fast B=4 composition complexes, form a closed lifted complex component. Its connector cycle closes inside the strip and the fast reactions remain within it. Additional immigration and connector exits at these same phases have DIFFERENT unbounded source complexes; they do not create outgoing graph edges from the closed lifted vertices. Thus the condition “every lifted complex reaches killing” genuinely fails, although the physical frozen phase process can reach the strip exit by repeated immigration.

The obstruction is therefore structural, not a failure to take the count threshold or the fixed strip width large enough. The conservative A+C shell grows without bound and supports a nontrivial composition profile. Treating this profile by a fixed constant fugacity and a fixed fractional-factorial exponent cannot make the frozen resolvent stable. Other composition-dependent or nonfrozen methods remain possible; no recurrence or explosion conclusion is inferred.

Reviewed source SHA-256: `e5a3f282d015fd0ba1c006673c88e6826283b1cce6f6b238060498e451cc4c44`.
