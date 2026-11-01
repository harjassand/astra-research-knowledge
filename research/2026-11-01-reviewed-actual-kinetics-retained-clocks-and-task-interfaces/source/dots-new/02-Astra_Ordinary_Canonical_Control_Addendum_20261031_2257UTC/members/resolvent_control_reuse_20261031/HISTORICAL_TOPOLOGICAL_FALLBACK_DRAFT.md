# Uniform success from an acquired approximate closure certificate

NEW unreviewed strengthening of PROOF sections 3--5. It removes the exact-class
premise from the small-error success guarantee. The original exact-class route
is still a valid, less restrictive conditional result; it is not silently
promoted by this addendum. No new empirical acquisition or novelty claim.

Use all notation and the actual forward interface of PROOF.md. In particular
H=(1-gamma)(I-gamma A0)^(-1)Z is stochastic, Bhat_0=0, Bhat_a 1=0, and a received
event gives ||(A_a-A0)H-ZBhat_a||_(infinity->infinity)<=eta. No exact closure is
assumed. Let t=gamma/(1-gamma), q=t eta and

             kappa=(1-gamma)/(1+gamma).

## A. Geometry is earned from the baseline, not supplied

For every x in R^r,

 (1-gamma)||x||_infinity
  =||(I-gamma A0)Hx||_infinity
  <=(1+gamma)||Hx||_infinity.

Thus ||Hx||_infinity>=kappa||x||_infinity. This lower bound uses only stochasticity
and the disjoint indicator lift Z; no singular value of R=WH is needed.

For ANY randomized block policy pi, use its convex row selector Bhat_pi and
stochastic A_pi. Its error E_pi=(A_pi-A0)H-ZBhat_pi has norm<=eta. Consequently

 (I-gamma A_pi)Hx=(1-gamma)Z(I-tBhat_pi)x-gamma E_pi x,

and the inverse-contraction inequality
||(I-gamma A_pi)v||_infinity>=(1-gamma)||v||_infinity gives

 ||(I-tBhat_pi)x||_infinity >=(kappa-q)||x||_infinity.    (A)

This applies also to mixtures (1-theta)A0+theta A_pi, replacing q by theta q.
The selector may vary by block. The result is not a claim that Bhat is stochastic
or that the reduced fixed-point iteration contracts.

## B. A nominal root exists without planning advice

Assume q<kappa. Define f(w)=w-t max_a Bhat_a w, with the max taken by row.
For any w,z, each coordinate of the difference of maxima is a convex combination
of the corresponding action-row slopes applied to w-z (equivalently integrate
along the segment and choose its piecewise-constant maximizing action). Thus

 f(w)-f(z)=(I-tBhat_pi)(w-z)

for some randomized block selector pi, and (A) proves

 ||f(w)-f(z)||_infinity >=(kappa-q)||w-z||_infinity.       (B)

In particular f is injective and proper. For completeness, existence can be
obtained by a standard Brouwer-degree homotopy, used ONLY as an existence proof.
Set f_theta(w)=w-theta t max_a Bhat_a w. The mixed-source version of (A) gives
||f_theta(w)||>=(kappa-q)||w||, uniformly for theta in [0,1]. For any target g,
choose a cube of radius greater than ||g||/(kappa-q). No f_theta(w)-g vanishes
on its boundary. Its degree is the degree of w-g, namely 1, so f(w)=g has a
root. Together with (B) it is unique and obeys

         ||w0||_infinity <= Mbar:=1/(kappa-q)           (C)

for g in [0,1]^r. This invokes ordinary finite-dimensional topological degree,
not an efficient root oracle. The ACTUAL downstream computation below is an
explicit rational LP with checked primal/dual certificates.

Since Bhat_0=0, y0=w0-g=t max_a Bhat_a w0>=0, hence 0<=w0 and 0<=y0<=Mbar.
The posterior Bellman residual argument gives for V0=H w0

       ||V0-V*||_infinity <= d0:=q Mbar.                (D)

No assertion that V0 is exactly optimal, nor that the nominal signed model is
a stochastic MDP, is made.

## C. An ordinary robust LP acquires uniformly good policies

Set

 c=q(1+Mbar)/(1-q),   Y=Mbar+c,   M=1+Y,
 s=qM=c.

Solve the r-variable LP

 minimize hhat y,
 0<=y<=Y1,
 y_j>=t[Bhat_a(g+y)]_j+s    for every j,a.               (E)

This LP is feasible for every g in [0,1]^r: y0+c1 is in the box, the row-zero-sum
property leaves all Bhat_a(g+y0+c1) unchanged, and its constraint slack is exactly
c=s. Every feasible y is a TRUE original-process Bellman supersolution because
||g+y||<=M and s=qM covers the certified action-effect error. Thus V=H(g+y)>=V*.

If ||hhat-h||_1<=delta_h and hhat is a probability vector, compare an LP optimum
to y0+c1 to obtain

 Delta:=mu(V-V*) <= d0+c+delta_h Y.                     (F)

Here |h(y-y0)-hhat(y-y0)|<=delta_h Y, and (D) supplies the d0 term. The exact
microscopic averaging law mu=uW still has full support, even for unequal blocks.
Repeating the block-residual averaging calculation from PROOF section 4 yields

 rho<=r[(d0+c+delta_h Y)/(1-gamma)+s],

and the actual nominal-greedy table has pointwise normalized regret at most

 U=2r(d0+c+delta_h Y)/(1-gamma)+2(r+1)s.                 (G)

Unlike the earlier sufficient bound, (G) is valid for ANY actual source satisfying
the received approximate-error event. It does not assume a small exactly closed
nearby process or an unverified class equality. All quantities in (G) are acquired
or externally task-bound. Therefore U<=epsilon_req certifies success of the
checked LP for EVERY admitted bounded goal on the SAME confidence event.
An LP objective gap zeta adds 2r zeta/(1-gamma) to (G). The tighter measured
posterior bound remains valid for every candidate, even if q>=kappa or (G) is
uninformative; failed planning/receiving attempts remain costs.

## D. Structural consequence and restrictions

This constructs an acquired stability geometry and a uniform many-task consumer
from imperfect observations, with no R inverse, supplied good condition number,
exact generated algebra or assumed efficient nonlinear planner. It is still a
specialized successor-feature/robust-ALP construction, not a historical novelty
claim. The proof does NOT make the sufficient endpoint acquisition economical.

A finite source generally has a nonzero limiting closure defect; if q stays
above kappa or U above the requested tolerance, no universal-success certificate
is earned. Refining the partition and buying more data may help, and may instead
end at ambient rank n. Near gamma=1 the condition and sample bill are stringent.
The native reward language, current-state observation/preparation interface,
partition map storage, all search/refinement samples, and later solver precision
remain explicit. Strong ordinary learners can adopt exactly the same acquired
certificate and LP.

## E. Sharper primary route: an acquired LP objective margin

There is a more accurate ordinary LP consumer when one further ACQUIRED scalar
condition holds. Write d=kappa-q>0, G_pi=(I-gamma A_pi)^(-1), M_pi=I-tBhat_pi.
The exact identity, with the sign fixed by the definition of E_pi above, is

 H M_pi^(-1)=(1-gamma)G_pi Z-gamma G_pi E_pi M_pi^(-1).

Since mu=uW, mu Z=u and ||mu G_pi||_1=1/(1-gamma), while (A) implies
||M_pi^(-1)||_infinity<=1/d, we obtain componentwise

 hhat M_pi^(-1)
    >= [(1-gamma)/r-(q+delta_h)/d] 1^T.                 (H)

The first term uses G_pi>=I entrywise; the error terms are bounded in row L1
by q/d and delta_h/d respectively. This is valid for ALL randomized block
selectors, not just the unknown optimum. Define the computable margin

             z=(1-gamma)/r-(q+delta_h)/d.

If z>0, solve the NOMINAL small LP (2) with hhat, and optionally 0<=y<=Mbar1.
The nominal root w0=g+y0 exists by section B and is feasible. Choose an active
selector pi0 at w0. Any other feasible w has v=M_pi0(w-w0)>=0. Then

 hhat(w-w0)=(hhat M_pi0^(-1))v >= z ||v||_1.

It is strictly positive unless w=w0. Thus the nominal LP uniquely selects the
root, without a nonlinear root oracle or m^r policy search. This is NOT a claim
that an arbitrary piecewise-linear homeomorphism has an efficient solver: the
positive objective-row certificate (H) is the extra structure that earns it.

The root has rho=0 and ||w0||<=1/d. Its nominal-greedy block policy therefore has

             normalized pointwise regret <=2q/d.       (I)

All of d,z and (I) are computable from the retained finite-observation certificate.
If z>0 and 2q/d<=epsilon_req, every future g in [0,1]^r is admitted under the same
confidence event, with no exact closure assumption. A checked nonoptimal LP
candidate can still use the posterior (4), paying its actual residual.
The robust-bounded LP in section C remains a weaker-error-condition fallback;
its looser (G) may or may not meet the requested tolerance.

For the exact-class observation success bound eta<=6epsilon and delta_h<=gamma
epsilon, one convenient sufficient schedule for z>0 and (I)<=e_req is

 epsilon <= min{(1-gamma)^3/[28r gamma(1+gamma)],
                 e_req(1-gamma)^2/[24 gamma(1+gamma)]}.

Indeed q+delta_h<=7gamma epsilon/(1-gamma)<=kappa(1-gamma)/(4r),
which also gives q<kappa/2; hence z>=(1-gamma)/(2r)>0 and
2q/d<=4q/kappa<=24gamma epsilon(1+gamma)/(1-gamma)^2.
Use the explicit cap/root-bit/N construction in PROOF section 9 with this target.
These remain sufficient, potentially costly schedules, not necessary prices.
The actual admission test uses measured eta and may be much better or worse.
