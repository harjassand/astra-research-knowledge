# Structural failure of frozen finite-phase elimination: unbounded conservative composition

Status: new internal derivation, awaiting audit. This is NOT a recurrence counterexample.

## Fixed rank-three single-linkage network
Use unbounded species A,C and boundary species B. Include the connector cycle

    0 --1--> A+B --1--> 3A+4B --1-->0.

At B stoichiometric count4, include the reversible chain

    3C+4B <--> A+2C+4B <-->2A+C+4B <-->3A+4B.

In the direction increasing A, the three rates are6,1,7. In the direction decreasing A, they are12,1,1 respectively. All constants are positive. The full complex graph is strongly connected and its stoichiometric rank is3.

The fast chain conserves A+C and B. With r=A/C, its leading A-increase/decrease rates divided by C³(B)_4 are

    b(r)=6+r+7r²,
    d(r)=12r+r²+r³,
    b(r)−d(r)=−(r−1)(r−2)(r−3).

## Every fixed fugacity fractional-factorial tilt fails somewhere
Allow an arbitrary fixed positive fugacity multiplier in A,C, and a fixed0<alpha<1. Its leading tilt on a fast A-increase/C-decrease step has the form

    t(r)=k r^alpha,

where k>0 is arbitrary (the inverse fugacity ratio, according to convention). The fast frozen-count diagonal contribution is

    H(r)=b(r)(t(r)−1)+d(r)(t(r)^(−1)−1).

Since H=(t−1)(b−d/t), H≤0 holds exactly when t lies between1 and d/b. In particular it requires t≤1 where b>d and t≥1 where b<d. The sign of b−d alternates across1,2,3. No strictly increasing t(r)=k r^alpha can satisfy these inequalities for all r: it would have to be≥1 on(1,2) and≤1 on(2,3), forcing t(2)=1 and contradicting strict monotonicity on either interval. Hence for EVERY k>0 and every alpha∈(0,1), H(r)>0 somewhere.

Also H(r)→−6 as r→0 (because alpha<1). By continuity one can choose r with

    0<H(r)<r³.

Fix such r and send C=n,A~r n.

## Positive eigenvalue of the actual proposed frozen-phase matrix
Truncate B to{0,...,K}, for ANY fixed K≥4. Build the ideal factorial-tilted phase matrix M_alpha(A,C), including all ordinary outgoing losses and retaining internal phase gains. This is precisely the matrix required by the proposed finite-phase resolvent construction. Consider its principal submatrix on phases{0,1,4}; deleting other phases can only lower the spectral abscissa of a Metzler matrix.

At phase0 the outgoing connector rate is1. At phase1 the connector to phase4 has rate A, and an additional immigration exits the principal block at rate1. At phase4 the connector to phase0 has rate24(A)_3; other connector losses are4A+1. The same-phase fast composition chain contributes

    24 C³ H(r)+o(C³)

to its tilted diagonal. The product of the three tilted connector gains is asymptotic to24 A⁴: all fugacity and factorial-tilt powers cancel around the connector cycle, whose net A,C displacement is0.

The characteristic equation for this3x3 Metzler block therefore has a bounded real eigenvalue satisfying

    (lambda+1)(lambda+1+A)
      [lambda+1+4A+24A³−24C³ H(r)+o(C³)]
       =24 A⁴[1+o(1)].

After division by24 A⁴ this converges to

    (lambda+1)[1−H(r)/r³]=1.

The limiting root is

    lambda_* = H(r)/(r³−H(r)) >0.

It is simple, so a positive real eigenvalue persists for all sufficiently large n. Therefore M_alpha is not Hurwitz. Increasing the strip K does not help: the same principal block remains present, with the same outgoing losses, for every K≥4.

Thus NO fixed alpha∈(0,1), no fixed fugacity choice, no farther-out count threshold, and no larger finite B strip can make this frozen-count factorial resolvent method work globally for this network.

## The escaping boundary states belong to one actual class
All(A,C,4) with A≥1,C≥0 are reachable from0. Put N=A+C. Fire0→A+B exactly4N times; convert A to C exactlyC times using3A+4B→2A+C+4B; fire A+B→3A+4B exactly12 times; finally fire3A+4B→0 exactlyN+8 times. Every firing is enabled, and the final state is(A,C,4). Weak reversibility supplies an enabled return path for every fired reaction, so all these states communicate with0. The counterexample is not an artifact of rays outside the physical class.

## Interpretation and scope
The strip's PHYSICAL frozen phase chain can reach its exit, but it contains a closed lifted complex layer carrying conservative composition dynamics in the two unbounded populations. Freezing that composition turns a bounded-population redistribution process into an exponentially tilted growth mechanism. It is exactly the stronger 'every lifted complex reaches killing' hypothesis of the proved leaky-strip theorem that fails.

A composition-dependent correction can in principle handle the fast conservative chain; indeed its within-shell stationary profile is the relevant object. But that profile lives on a shell whose size grows with A+C. Therefore the general boundary problem contains a genuine infinite-background component and cannot be reduced to a fixed phase alphabet by this freezing step. No claim about nonrecurrence or explosion of the original WR process is made.
