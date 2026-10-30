# Infinite-phase first-residual-exit contraction

Status: child adversarial review passed; see INDEPENDENT_INFINITE_PHASE_FIRST_EXIT_AUDIT.md. This is an infinite-B elimination result for a controlled projected model. It is not full physical recurrence or a claim that the physical comparability cone is invariant.

## Residual and controlled projected rates
Let n=N=A+C and B>=0. Define

    h_0=0,h_1=1,h_2=2,h_3=3;
    h_4=3,h_5=4,h_6=5;
    h_(b+3)=h_b+2 for b>=4,
    r=n−h_B.

Connector jumps are immigration (n,B)→(n+1,B+1), activation→(n+2,B+3), clearing→(n−3,B−4). Their residual increments are respectively0 or+1, exactly0 for enabled activation, and0 or−1. Up exits are immigration from B=3 or B>=6 divisible by3. Down exits are clearing from B>=7 congruent1 modulo3.

During a neutral excursion r is constant and n=r+h_B. Allow arbitrary nonanticipative coefficient choices in fixed positive compact intervals, with rates

    lambda_I in [c_I,C_I],
    lambda_T in [c_T,C_T] n B,
    lambda_D in [c_D,C_D] (n)_3 (B)_4.

Choose r sufficiently large. The actual hard network satisfies these bounds locally on A>=epsilon N, but the controlled auxiliary model is defined independently and does not assume that physical cone is invariant.

## Exact finite-head certificate
Take head B=0,...,12. Stop on the first nonzero residual increment or the first neutral exit to B>12. Kill at all those exits. The finite graph has positive rates of degrees0,1,3 in r. Exact rate-form positive Schur elimination gives, uniformly over head starting phases,

    P(first exit is UP) <= C_1/r,
    P(first exit is a NEUTRAL tail exit) <= C_2/r^2,
    E(head stopping time) <= C_3 r^D

for some fixed finite D. The degree calculation is recorded by check_first_residual_all_exit_degrees.py and FIRST_RESIDUAL_ALL_EXIT_DEGREES.json (use the K=12 record). It computes absorption probabilities by adjoining source probes of rate1 and eliminating all transient states with positive Schur arithmetic. Each up-probability exponent is at most−1 and each neutral-tail probability exponent is at most−2.

These exponents depend only on positive rate supports/orders, not on leading coefficient values. Uniform compact coefficient bounds therefore give uniform constants. Arbitrarily changing row controls are covered by the finite affine policy-improvement lemma: maximize the sum of (-Q_pi)^(-1)b_pi over endpoint policies, where b_pi is the selected exit intensity. The maximizing vector is a common supersolution for every row choice. Expected-time bounds use b=1. All endpoint-policy matrices are transient because enabled immigration eventually exits the finite head.

This is a finite exact subcalculation inside an infinite-phase theorem, not extrapolation from several growing cutoffs.

## Tail estimate independent of the size of B
Start at B>=13. Stop on the first immigration, a down residual exit, or head entry. In the absence of immigration, activation adds3 to B and leaves its residue modulo3 unchanged; clearing subtracts4 and cycles the residue. Thus within at most THREE clearings there is a down exit or head entry, no matter how many activations intervene.

While outside the head, clearing intensity is at least c r^3 (B)_4>=c' r^3. Therefore the expected time to this stopped event is at most C r^(−3), by the compensator/hazard bound for at most three clearings. Immigration intensity is bounded above, so the probability immigration occurs first is at most C r^(−3).

A neutral immigration can restart a tail attempt. Its probability is O(r^−3), giving a geometric bound on the number of attempts. Hence the actual time to head entry or a nonzero residual exit has expectation O(r^−3), and

    P_tail(UP before eventual residual exit) <= C r^−3 + H(r),

where H(r) is the worst corresponding up probability from the finite head, over all controls.

No hidden tail explosion is used: for fixed r, activation intensity grows at most C(r+B)B, whereas clearing grows at least c(r+B)^3(B)_4. The linear function B has an upper bounded drift outside a finite set for the neutral killed process, giving nonexplosion by stopped localization. Equivalently, infinitely many activations before the required finite number of clearings have probability zero because the successive activation/clearing rate ratios decay at least as a fixed power of B.

## Close the actual head–tail renewal inequality
Let T(r) be the worst up probability from any tail phase. Strong Markov/dynamic control conditioning gives

    H(r) <= C_1/r + (C_2/r^2) T(r),
    T(r) <= C_4/r^3 + H(r).

For sufficiently large r these imply

    sup_(all B, all controls) P( first nonzero residual exit is UP ) <= C/r.

The same renewal equations for holding times, using the finite-head polynomial bound and tail O(r^−3) bound, show the first nonzero residual exit time tau is finite with

    sup_(all B, all controls) E tau <= C r^D.

The tail feedback was actually bounded and absorbed; it was not discarded or frozen.

## Factorial trace contraction
At tau the residual is exactly r+1 or r−1. For any fixed d and any 0<alpha<1 put

    phi(r)=exp(−d r) Gamma(r+1)^alpha.

Then uniformly over B and allowed controls,

    E[phi(r_tau)]/phi(r)
       <= C exp(−d) r^(alpha−1) + exp(d) r^(−alpha) (1+o(1))
       →0.

In particular this ratio is at most1/2 for sufficiently large r. Together with the polynomial excursion-time bound, this controls the expected time of repeated residual excursions until r reaches a fixed finite threshold. That threshold set is NOT compact in (n,B), so this is not yet recurrence.

## Remaining physical/global obligations
- Actual coefficients can leave the positive comparability intervals when A/N becomes small; no cone invariance is assumed.
- The set r below a fixed threshold still contains arbitrarily large B and n.
- A pointwise normlike global physical Foster function and the coupling to the independently earned endpoint certificate are not asserted.

The result supplies a real infinite-phase, infinite-background trace contraction where the earlier finite-halo mechanism stopped. Its finite-head algebra, controlled-rate extension, and tail estimates require review before use as established capital.

## Sharp failure if the physical lower-rate premise is dropped
In the actual network, start at A=0, C=N, B=3 with N large. Activation has rate AB=0, clearing is disabled, and all fast conversion reactions are disabled because B<4. Immigration is the ONLY enabled reaction. It changes (A,C,B) to (1,N,4), so the residual changes from N−3 to N−2: the first nonzero residual exit is UP with probability1.

Thus the O(1/r) first-up bound is FALSE for the unrestricted physical network. The positive rate-comparability premise cannot be removed by changing constants or thresholds. A composition-boundary correction must actually be coupled to the infinite-phase trace before a global physical conclusion is possible. The previously earned entropy-sum corner construction addresses that boundary only at fixed finite B width; it is not silently being imported as an infinite-width closure.
