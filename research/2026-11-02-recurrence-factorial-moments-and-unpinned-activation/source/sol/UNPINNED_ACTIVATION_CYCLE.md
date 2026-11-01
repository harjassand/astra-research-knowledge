# An actual-time activation cycle with two unpinned inventories

This is an author-derived operation on the coupled obstruction in `ORDERED_COMPLEX_OBSTRUCTION.md`. It keeps all competing reactions and the actual physical clock, including arbitrarily long excursions of A. It is not a full global recurrence proof for that network, and the network is not substituted for the programme's general destination.

The unit-rate raw cycle is

    0 -> A+B -> 2A+B+C -> 3A+2B+2C -> 0.

At (a,b,c) its four propensities are

    1,  ab,  a(a−1)bc,  a(a−1)(a−2)b(b−1)c(c−1).                (1)

Both B and C change during every attempted activation and every excursion. A is neither bounded nor frozen; its long excursions are controlled below rather than excluded.

## The stopped operation

Fix theta>0. There is an explicitly given finite K_theta such that, from EVERY actual state (0,b,c) with b,c>=K_theta+2, stop at the first subsequent A=0 or at the first B<K_theta or C<K_theta. Write tau for this PHYSICAL stopping time. The output reward is

    W_out=exp(theta(B_tau+C_tau))              if A_tau=0,
    W_out=exp(theta(A_tau+B_tau+C_tau))        otherwise.

Then

    E W_out − exp(theta(b+c))
       <= −[(1−exp(−theta))/(32c)] exp(theta(b+c)).              (2)

Moreover tau has a uniformly bounded exponential moment at some positive physical parameter (1/2 is available with the constants below). For every 0<r<=theta there is a finite explicit D_theta with

    E integral_0^tau exp(r(A_s+B_s+C_s)) ds
       <= D_theta exp(r(b+c)).                                 (3)

Equations (2)–(3) are compatible: for r<theta the inward output margin eventually pays the ENTIRE physical reward (3). They do not insert a stationary fiber, a gap, or a neighboring-profile comparison. The exit reward in (2) includes the actual unbounded A landing coordinate, so a future gluing argument receives a real tail budget.

## 1. Separate a finite ordinary cycle from a genuinely rare overrun

All first three transitions increase A by one; reaction 3 decreases A by three. Before the first visit to A=3, the process makes exactly three upward moves, with every available competitor retained. At A=1 the possible sources are 0 and A+B; at A=2 they are 0, A+B and 2A+B+C.

Call an upward transition out of A=3 an overrun. Without an overrun the next transition is reaction 3 and the process returns to A=0 in four jumps. If f_i counts the uses of reaction i in such a return, then

    f0+f1+f2=3f3,   Delta(B+C)=f2−f3.

Without an overrun f3=1 and f2<=1, so Delta(B+C)<=0 on EVERY such branch, not just on a designated path. These four-jump branches stay in B,C>=K until their A=0 endpoint when b,c>=K+2.

The specific actual word [0,1,1,3] removes one B. Its probability is at least

    (1/2) * 1/(c+3) * (1/2) >= 1/(16c).                       (4)

The factors follow respectively from (b+1)/(b+2)>=1/2 at A=1, the exact A=2 probability

    2(b+1)/[1+2(b+1)(c+2)] >= 1/(c+3),

and the death probability at A=3. The last is at least 1/2 for K>=3 by the rate ratio below. This branch has output ratio exp(−theta).

At its first A=3 state one has B>=b+1 and C>=c. Directly from (1), the sum of upward propensities divided by the downward propensity is at most 4/(bc), for b,c>=2. Consequently

    P(first overrun) <= 4/(bc).                                (5)

This first-overrun estimate remains valid under all preceding choices, because their B and C counts were actually updated and only increased.

## 2. Control the whole unbounded overrun, without freezing B or C

At ANY state with a>=3 and B,C>=K, (1) gives

    q_up/q_down
      = 1/[(a)_3(B)_2(C)_2]
        +1/[(a−1)(a−2)(B−1)C(C−1)]
        +1/[(a−2)(B−1)(C−1)]
      <= rho_K:=2/(K−1)^2.                                    (6)

Thus the conditional probability of an upward A step at a>=3 is at most rho_K, throughout the ACTUAL path until the stated stop. No frozen B,C generator appears.

After a first overrun A=4. Let T be the number of additional jumps until A=0 or strip exit, U the number of upward steps taken while A>=3, D the number of downward steps, and L the upward steps from A=1 or 2. Between downward steps at most two low-A upward steps occur; because the excursion starts at A=4, L<=2D. Nonnegative terminal A and

    A_end=4+U+L−3D

imply D<=4+U, hence

    T=U+D+L <=4U+12.                                          (7)

For each collapsed A up/down word with U=k, its probability is at most rho_K^k, even after summing all channel choices: (6) holds conditionally on every actual history. There are at most 2^(4k+13) words of length at most 4k+12. Therefore

    E exp(sT) <= 2^13 exp(12s) sum_(k>=0)[16 rho_K exp(4s)]^k
       <=2^14 exp(12s)                                       (8)

whenever 16 rho_K exp(4s)<=1/2. The bound also proves T is finite almost surely; infinite excursions would require arbitrarily many rare high-A upward steps and have probability zero. Strip exits are included as stops throughout this argument.

Before the overrun the total particle count is at most b+c+10. Every additional reaction increases that total by at most three. Thus the actual output, including a strip-exit landing with A>0, satisfies

    W_out/exp(theta(b+c)) <=exp(10theta) exp(3theta T).

Choose K so rho_K<=exp(−12theta−4)/32. Equations (5) and (8) show that the ENTIRE positive output contribution is at most

    [4 C_theta/(bc)],       C_theta=2^14 exp(46theta).           (9)

The same stronger choice permits the extra factor T needed for an integrated reward, since 4+T<=5exp(T). This is a complete tail estimate for the unbounded excursion; it is not a finite path calculation.

## 3. Reconcile the two branches and preserve physical time

The non-overrun branches have nonpositive output increment. The deletion event (4) contributes at most −(1−exp(−theta))/(16c). All positive possibilities are paid by (9). Taking

    K_theta >= max{3,
       1+sqrt(64 exp(12theta+4)),
       128 C_theta/[1−exp(−theta)]}

and rounding up proves (2).

Every state has the original constant immigration propensity 1, so its ACTUAL total rate is at least one. Conditional holding means are at most one; their exponential moments at physical parameter 1/2 are at most two. Combining this with (8), at s=log 2, gives a uniform finite E exp(tau/2), including the at most four pre-overrun jumps. A path with no overrun has just four jumps, so it is automatically included. Finite jump count before tau also proves the stopped process cannot explode.

At every pre-stop state after the overrun, total count is at most b+c+10+3T. Conditional expectation over the actual holding times therefore bounds the physical integral in (3) by

    exp(r(b+c+10)) E[(4+T) exp(3rT)].

The geometric series (8), with s=3r+1, proves (3). One may use D_theta=6*2^14 exp(46theta+12), which also covers the four-jump no-overrun branch. This bound retains all residence time and count rewards.

## 4. What new operation this earns

The negative word borrows and repays residual inventory across multiple source switches. The construction proves that its negative output probability is order 1/C while the WHOLE dangerous overrun has weighted probability order 1/(BC), with a uniformly controlled actual time and output tail. This supplies a real multi-inventory operation that the single-switch target representation cannot see.

The remaining work is not an assumed transfer: for this diagnostic, the infinite low-B and low-C faces and their feedback must still receive compatible return/output rewards to produce a global theorem. For arbitrary weakly reversible raw lists, one must construct such borrowed-inventory cycles or a different global representation without relying on this special A increment/reset pattern. The fixed-width bulk theorem does not close these other faces, and this local operation is not promoted to general recurrence.
