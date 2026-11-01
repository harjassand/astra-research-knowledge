# Conditional weighted derivatives for the deterministic clock

Status: separate deterministic addendum, pending independent receipt. It concerns the remaining clock b(l,e) defined in REMAINING_CLOCK_OBSERVABLE.md. It makes no claim that an actual count path stays in this cone.

Fix 0<g<=3/4 and suppose l>=g e², e>0. Along the inverse flow from(l,e),

 L(v)=u(v)+3v²/4>=l+3(v²-e²)/4>=g v², v>=e.

With J(v)=exp[-integral_e^v L^-3], differentiation of the actual scalar flow gives

 |b_l|=1-J_infinity<=1/(5g³e^5),
 b_ll=3J_infinity integral_e^infinity J(v)L(v)^-4 dv,
 0<b_ll<=3/(7g^4e^7).

These estimates do not assume the state lies on the single orbit from(0,0). They require the displayed cone; without it the e^-5 sensitivity assertion is false.

For l>0, cooperative comparison of the original vector field gives b_e<=0. The transport identity and b_l<=0 then yield

 |b_e|<=1/(2l²)<=1/(2g²e^4).

To acquire the remaining C² segment weights, put alpha=3e/2+1/(2l²). Exact differentiation gives

 b_le=J_infinity/l³-alpha b_ll,
 b_ee=-(3/2)b_l-alpha b_le.

For e>=1 define

 K_le(g)=g^-3+9/(14g^4)+3/(14g^6),
 K_ee(g)=3/(10g³)+(3/2+1/(2g²))K_le(g).

The preceding inequalities imply

 |b_le|<=K_le(g)e^-6,
 |b_ee|<=K_ee(g)e^-5.

In the convenient padded cone l>=e²/2, e>=1, the explicit bounds are

 |b_l|<=8/(5e^5), |b_e|<=2/e^4,
 0<b_ll<=48/(7e^7), |b_le|<=32/e^6, |b_ee|<=572/(5e^5).

All constants are direct deterministic analytic ceilings. There is no numerical ODE oracle in these derivative bounds.

For a finite-jump Taylor remainder, the ENTIRE actual jump segment must satisfy the admitted cone and lower e threshold, or a separate startup bound must be used. A statement about the current state alone does not license these derivative weights at all successors. An actual-cone admission probability, all exceptional exits, and global passage through the boundary/clearance region remain separate stochastic operations. These bounds may reduce a task-specific clock error while a full-path norm remains stiff; that potential computational advantage has not yet been demonstrated.
