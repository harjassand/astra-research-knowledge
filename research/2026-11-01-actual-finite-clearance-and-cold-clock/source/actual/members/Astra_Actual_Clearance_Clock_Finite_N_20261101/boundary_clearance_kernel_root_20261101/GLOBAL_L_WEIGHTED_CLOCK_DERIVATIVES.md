# L-weighted clock derivatives on a padded one-sided cone

Status: root deterministic construction awaiting independent review. No stochastic admission, finite-N timing, or normal-approximation error is supplied.

Use the received remaining-time function b(l,e). For l>0,e>=0, write the inverse flow in increment coordinate w=v-e:

 L'(w)=1/(2L(w)^2)+(3/2)(e+w), L(0)=l,
 J(w)=exp[-integral_0^w L(z)^-3 dz], J_inf=lim J(w).

Then b_l=J_inf-1. Since L(w)>=l+3w²/4,

 |b_l|<=min(1, [sqrt(3)pi/8]l^-5/2)<=min(1,l^-5/2),
 b_ll=3J_inf integral_0^infinity J(w)L(w)^-4 dw
       <=[5sqrt(3)pi/16]l^-7/2 <=(5/2)l^-7/2.

The coarse rational constants use only pi<4 and sqrt(3)<2. They hold without any lower or upper e/l ratio.

## Uniform bounds through the small-l startup

For all l>0,e>=0,

 J_inf<=min(1,10(1+e)l²).

To prove this, set h=1/[2sqrt(1+e)]. If l>=h, the bound is immediate. Otherwise let w_h be the first L=h. Since L'>=1/(2L²), w_h<=2h³/3. The exact logarithmic identity gives

 J(w_h)=(l/h)² exp[integral_0^w_h 3(e+w)/L(w) dw]
        <=4(1+e)l² exp(3e h²+2h^5)
        <=4(1+e)l² exp(13/16)<10(1+e)l².

The final exponential inequality follows directly from a rational Taylor sum with a geometric remainder. Also

 b_ll<=3J_inf(1-J_inf)/l.

Combining it with the two bounds J_inf<=10(1+e)l² and J_inf(1-J_inf)<=1/4 gives

 0<b_ll<=5sqrt(1+e).

The inequalities are compatible with the received smooth boundary extension; no literal inverse division at l=0 is used.

## Mixed derivative sign and a fixed padded cone

Let Y=partial L/partial e at fixed l in the increment representation. It obeys

 Y'=-L^-3Y+3/2, Y(0)=0,
 0<=Y(w)<=3w/2.

Therefore

 b_le=3J_inf integral_0^infinity L(w)^-4 Y(w)dw>=0.

The received exact identity also gives

 b_le=J_inf/l³-alpha b_ll<=1/l³,
 alpha=3e/2+1/(2l²),
 b_ee=-(3/2)b_l-alpha b_le.

Now restrict only to e²<=3l. For l<=1/2 this implies e<5/4. Use the fixed intermediate level L=1/2. The logarithmic argument above gives J_inf<12l². Before that level, Y<=L³-l³ and dw/dL<=2L², so the integral of L^-4Y is at most1/4. After it, Y<=1/8+(3/2)z and L>=1/2+3z²/4. The two tail integrals are less than5/4 and equal8/3 respectively, using elementary beta integrals. Their total, with the startup term, is less than25/6. Hence

 b_le<13, and b_le<=150l² for l<=1/2.

For l>=1/2 use b_le<=l^-3<=8. The remaining exact derivative formulas and cooperative monotonicity b_e<=0 yield the following global bounds on the padded cone e²<=3l:

 |b_l|<=1, |b_e|<=6,
 0<=b_ll<=9, 0<=b_le<=13, |b_ee|<=148.

For l>=1 in that same cone, stronger tails are available:

 |b_l|<=l^-5/2, |b_e|<=1/(2l²),
 b_ll<=(5/2)l^-7/2, b_le<=l^-3, |b_ee|<=5l^-5/2.

For example the small-l b_ee bound follows from
3/2+[15/8+1/(2l²)]150l²<148. At l>=1/2 its direct bound is smaller. For l>=1, e<=sqrt(3l)<2sqrt(l) gives the stated tail. These are analytic ceilings, not fitted numerical derivative bounds.

## Receiving significance and limits

The weight psi(l)=min(1,l^-5) bounds b_l² and has integral0^infinity psi=5/4. Thus later source-time/bracket calculations need not replace the sensitivity by a constant over a growing compact region. A bounded primitive of this weight is available as an ordinary auxiliary test function; its actual finite-jump drift and martingale still require proof.

Every Taylor segment, not just its starting state, must satisfy the padded cone. The function e²/l is convex for l>0, so checking both segment endpoints is sufficient for that particular geometric condition. Actual L/E jump padding and all exceptional exits remain stochastic receiving obligations. No lower-ratio gate is introduced by these derivative bounds, and no practical clearance claim follows yet.
