# A summed-current refinement (same operation)

This is an analytic refinement of PROOF Section 3, not another source or fitted case.
It strengthens the admitted contrast and independent-component range.

Keep the notation there, with k_f=u in [1,q] and all other conductances fixed.
The exact transfer-current identity, including an optional fixed PSD grounding term,
implies

    sum_(e!=f) R_ef(u)^2 <= R_ff(u)-u R_ff(u)^2.

Let s=R_ff(1) in [0,1]. Sherman--Morrison gives

    R_ff(u)=s/[1+(u-1)s].

Therefore

    integral_1^q sum_(e!=f) R_ef(u)^2 du
      <= (q-1)s(1-s)/[1+(q-1)s]
      <= (q-1)/(sqrt(q)+1)^2.

The last scalar maximum is attained at s=1/(sqrt(q)+1). Combining with the
already proved derivative bound (r(q-1)q/8)R_ef^2 gives

    c_sharp = r q(sqrt(q)-1)^2/8.                        (S1)

Thus c_sharp<1 is also a sufficient finite-graph CFTP condition. It is strictly
stronger than the initial rational c=r q(q-1)^2/8. For example, q=4,r=1 has
c_sharp=1/2, while the initial c would be 9/2 and would admit nothing. At q=2,
r=3 gives c_sharp=9/4-(3/2)sqrt(2)<13/100 rather than the initial 3/4.

The original code/window and executions deliberately retain the initial rational
constant unless an explicitly declared stronger rational qualifier is supplied.
This extension changes no existing sample bytes. Any rational c_bar satisfying
c_sharp<=c_bar<1 can be consumed without an irrational runtime decision.

This is still a finite global sampler. The calculation does NOT exchange a sum
with an entrywise supremum, prove infinite-volume uniqueness, remove the cost of
resolvent evaluation, or handle a linear force / nonzero-tilt Gibbs measure.
