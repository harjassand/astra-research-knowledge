# Exact screening of power-transfer shortcuts

The actual channel is N=W3 tensor id, E=I3/3 tensor Tr_A. Literal algebra
gives N²=(Id+3E)/4. This identity is an established ingredient of current
N1093's accepted reduction-positive/parametric-contraction proof, not a new
operation. Source pin8d51d60762b3ee28c10aaaa56e1b92da119dc1cc.

## Entropy log-convexity across one channel step is false

Already for the ordinary classical qutrit input (1,0,0), successive N
outputs are(0,1/2,1/2) and(1/2,1/4,1/4). Relative to uniform, their
divergences are D0=log3, D1=log3-log2, D2=log3-(3/2)log2. Exactly

    D1²-D0 D2=(1/2)log2 log(4/3)>0.

Thus the proposed midpoint bound D1²<=D0D2 is FALSE, even without quantum
memory. N²'s depolarizing contraction cannot be transferred by that rule.
For the maximally entangled equality source one similarly gets
D0=2log3,D1=log3,D2=log3-(4/3)log2, again violating the midpoint bound.
These failures do not refute the desired D1<=D0/2.

## Trace-power positivity cannot hold at every p>1

Consider rho=(I9-P_Omega/3)/8. It is a positive density, with tau=I9/9.
Its N image is(5I+F_swap)/48, eigenvalues1/8 six times and1/12 three times.
Consequently the proposed Fp=Tr rho^p+Tr tau^p-2Tr(Nrho)^p has

    F6=[-4+9(8/9)^6-6(2/3)^6]/8^6
       =-1289/3869835264<0.

This is an actual physical source, not an arbitrary equal-trace pair.
Its true entropy deficit is(1/2)log(32/27)>0, and it lies in the accepted
reduction-positive region. The counterexample defeats only the stronger
ALL-p route, not Fp on1<p<=2 or the entropy conjecture.

## Bounded numerical screen, not a theorem

attack.py performed36 deterministic real-matrix optimization starts at
reference dimensions2,3,4 and p=1.05,1.25,1.5,1.75. It used548 objective/
gradient evaluations and at most39 iterations/start. Minimum was numerical
-4.44e-16, with no certified negative proposal. The correct conclusion is
UNKNOWN for the proposed1<p<=2 inequality. Five directional finite-
difference controls agreed with the analytic gradient to3.78e-11. The run
took.075s after imports; imports/startup are excluded. A final status-print
key error occurred AFTER the data file had been written, and was corrected.
No scientific result depends on that print or on the floating signs.

The Jensen p-power bound tends, as p decreases to1, to the existing
source-weighted Jensen surrogate. That surrogate can be negative on
physical isotropic sources; N1100 already records its failure. Current
N983 also supplies fixed-marginal local BKM quotients>1/2, so neither
global fixed-marginal convexity nor pinching can be silently granted.
Current N1098 already covers every3x2 source by its low-Schmidt eigenbasis
theorem; those states are not a new frontier. These source statements were
retrieved selectively to prevent repeated discovery, not independently
promoted beyond their existing review scope.
