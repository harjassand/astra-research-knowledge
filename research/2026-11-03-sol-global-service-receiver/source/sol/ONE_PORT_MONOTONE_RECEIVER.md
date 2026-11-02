# A raw-derived monotone large-anchor receiver

Author construction in the live boundary stage. No full six-species recurrence
claim follows yet. This replaces the unproved monotonicity of an unknown
anchor-zero value by an explicit receiver.

For an autonomous C3 block with positive rates (k0,k1,k2,k3), put

    t=min(b,c), h=|b-c|+3t/2+(t mod 2)/2, g=(a-h)_+.

Here h is integer, h(b+2,c+2)=h(b,c)+3. Let ell be 3 at (0,0), 2
when exactly one hidden coordinate is zero, 1 when min(b,c)=1, and 0
when min(b,c)>=2. Acquire

    K=max(1,4 k3/k2), L=4+4K k1/k2, C=L+5.

Define the finite profile d by

    d(0,0)=3;
    d(b,0)=2 if b=1, and L+1 if b>=2;
    d(0,c)=2 if c>=1;
    d(b,1)=L if b>=2;
    d(1,c)=1 if c>=1;
    d(b,c)=0 if min(b,c)>=2.

Put f=C ell+d and

    F0(a,b,c)=K g^2+C a+f(b,c),    F=16 F0.

The formula may be used also at small anchors; only its large-anchor
generator inequality is asserted. Let fmax=3C+L+3 (a convenient upper bound).

## Exact properties

F is nonnegative, F>=16Ca and F<=16(Ka^2+Ca+fmax), uniformly in b,c.
Incoming packets obey F(a,b+2,c+2)<=F(a,b,c): h increases by3 and every
nonready profile lands in the ready class f=0. At a ready source, removing
one packet has cost at most

    F(a,b-2,c-2)-F(a,b,c)<=96Ka+16 fmax.             (1)

This follows from g_out<=min(a,g+3) and the finite profile bound. These are
pointwise receiving statements, not stationary or averaged profiles.

## Uniform generator inequality

There is an acquired finite N, from the following rational inequalities in
a alone, such that for all a>=N and ALL b,c>=0,

    L_block F0<=-q_block/4, hence L_block F<=-4q_block.  (2)

The source propensities are q0=k0, q1=k1 ab, q2=k2 a(a-1)bc,
q3=k3 a(a-1)(a-2)b(b-1)c(c-1). All nonzero rate ratios used below are
exact falling-factorial ratios. For any birth, g increases by at most1.
At a terminal jump a->a-3, (b,c)->(b-2,c-2), g is EXACTLY unchanged.

* b=c=0: the only source is0; h increases1, f decreases C+1 and a
  increases1. Thus its F0 increment is exactly -1.
* b=0,c>=1: again only source0; the new profile is C+1 and h increases1,
  so the increment is exactly -1.
* b>=1,c=0: source1 has increment -1. At b=1 source0 has increment
  C+L-1, and at b>=2 it has increment C. Its ratio q0/q1<=k0/(k1 a).
* b=c=1: source2 has increment -1. Source0 and source1 have respective
  increments C+L-1 and C. Their ratios to q2 are bounded by
  k0/[k2 a(a-1)] and k1/[k2(a-1)].
* c=1,b>=2: source2 has increment -L; source0 has increment C; source1
  has increment at most K(2a+1)-L. Its ratio q1/q2=k1/[k2(a-1)].
  For a>=4, (2a+1)/(a-1)<=3, so the choice of L leaves a fixed negative
  margin. Source0/q2<=k0/[2k2 a(a-1)].
* b=1,c>=2: source2 has increment -1; source1 has increment C;
  source0 has increment <=K(2a+1)-1. The ratios are at most
  k1/[2k2(a-1)] and k0/[2k2 a(a-1)].

Choose N in these four nontrivial unready classes so the positive terms
are <=q_max/2 and q_block<=2q_max. Then LF0<=-q_block/4 there.

In the ready class min(b,c)>=2, every birth has positive increment at
most K(2a+1)+C, and source2 at most C. At a terminal jump, unless
(b,c)=(2,2), the new ell<=2 and new d<=L+1, so its increment is
<=-C+L+1=-4. Uniformly, the ratios of q0,q1,q2 to q3 are bounded by

    k0/[4k3 a(a-1)(a-2)],
    k1/[2k3(a-1)(a-2)], k2/[k3(a-2)].

The total positive increment divided by q3 tends to0 uniformly. Choose N
so it is <=2 and q_block<=2q3. This proves the required inequality.

At (b,c)=(2,2), the terminal increment is exactly3; source0/source1
increments are C; source2's increment is C-K(2a-7) for a>=5. Thus

 LF0/q3 = 3+[C-K(2a-7)]k2/[k3(a-2)]
             +C{k1/[2k3(a-1)(a-2)]
                 +k0/[4k3a(a-1)(a-2)]}.

Its limit is 3-2Kk2/k3<=-5. Acquire N so the display is <=-2 and
q_block<=2q3. All conditions are rational one-variable inequalities
with the stated strict limits, so an integer N can be found by bounding
the displayed denominators or eventual-sign polynomial root bounds. A
theorem need not numerically materialize N. This is not a hidden
unbounded-state oracle.

The generator classification exhausts every physical b,c, including
unpaired and highly unequal inventories. It pays the genuine source
count, not merely physical time.

## Scope and next interface

For the autonomous process stopped upon a<N, (2), nonnegative F, and
localization pay the full physical clock and genuine event count. For
the coupled process, (1) and packet monotonicity supply actual core
receiving costs. The next file develops that operation; matching its
outgoing values to the existing high-region trace remains a separate
global obligation.
