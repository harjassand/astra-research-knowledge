# The heavy-Schmidt zero-population scalar envelope is positive

2026-10-25. Exact scalar theorem; physical receiving constraints are supplied by wh3_aligned_zero_population_balanced_face.md. The logarithmic constants below are certified by exact rational arithmetic, not an optimizer.

## Statement

Let 1/2<=a<1, b,c>=0, b+c=t=1-a, and a<=x<=1. Define

f_l(z)=l log(z/3)-(1-l)log[(1-2l+lz)/(2(1-l))],
F(l)=f_l(l),
h(l)=log(1-l)-[l/(1-l)]log l.

Use continuous endpoint values. Then the exact heavy envelope from the source receipt satisfies

L=F(b)+F(c)+f_a(x)+(a/t)(x-a) min(h(b),h(c)) >3/1000. (1)

The limiting case a=1 has value log(4/3), hence is safe too. This closes the heavy-spectrum part of the all-zero-population aligned source face when combined with its source-derived envelope. It is not a proof for arbitrary nonzero populations or nonaligned marginal interfaces.

## 1. A lower entropy payment

For 0<=l<=1/2,

h(l)>=l(1-2l).                                       (2)

Indeed multiply the difference by 1-l and set

k(l)=(1-l)log(1-l)-l log l-l(1-l)(1-2l).

Both endpoint values are0 and

k'(l)=-log(l(1-l))-3+6l(1-l).

For z=l(1-l) increasing from0 to1/4, G(z)=-log z-3+6z decreases up to1/6, then increases; G(1/4)=log4-3/2<0. Hence k' has exactly one change from positive to negative, proving k>=0.

Assume without loss c<=b. Since b+c<=1/2,

b(1-2b)-c(1-2c)=(b-c)(1-2t)>=0.

Therefore min(h(b),h(c))>=c(1-2c).

## 2. Pay the unbalanced light spectrum by strong symmetric convexity

Let z=x-a in [0,t], d=t/2-c in [0,t/2], and k=az/t<=a. On [0,1/2],

F''(l)=1/l-1/(1-l)

is convex. Thus the symmetric function F(t/2-d)+F(t/2+d) has second derivative at least 2F''(t/2), giving

F(b)+F(c)>=2F(t/2)+m d^2,
m=F''(t/2)=4a/[t(1+a)].

Also

c(1-2c)=at/2-(2a-1)d-2d^2.

Completing the square yields

F(b)+F(c)+k c(1-2c)
 >=2F(t/2)+kat/2-k^2(2a-1)^2/[4(m-2k)].

The denominator is positive since

m-2k>=m-2a=2a(1+a^2)/[t(1+a)]>0.

Using z<=t, this gives

F(b)+F(c)+k c(1-2c)
 >=2F(t/2)+K(a)z,
K(a)=a^2/2-a(2a-1)^2(1+a)/[8(1+a^2)]
 >=3a^2/8.                                          (3)

The last difference is exactly

a(1-a)(3a^2+3a-1)/[8(1+a^2)]>=0.

## 3. Pay the decrease in the heavy coordinate

For a>=1/2, f_a'(1)=0 and f_a'''(x)<=0 on [a,1]. Indeed, writing D=1-2a+ax, one has D<=tx and

f_a'''(x)=2a/x^3-2a^3t/D^3<=0.

Consequently f_a''(x)>=f_a''(1)=M=a(2a-1)/t, and

f_a(x)>=f_a(1)+(M/2)(1-x)^2.

Combine this with (2)-(3), put K=3a^2/8 and use Kz>=Kz^2/t. Minimizing the resulting two nonnegative quadratic terms over z gives

L>=2F(t/2)+f_a(1)+M K t^2/(Mt+2K)
  =B(a)+R(a),                                       (4)

where

B(a)=(1-a)log(1-a)-(1+a)log(1+a)+(1+a)log4-log3,
R(a)=3a^2(2a-1)(1-a)/[2(11a-4)].

Formula(4) is continuous at a=1/2, where M=0.

## 4. A global one-variable lower bound

First,

B'(a)=log[4/(1-a^2)]-2,
B''(a)=2a/(1-a^2)>=4/3.

At a0=2/3 the exact rational log certificate gives

B(a0)>-571/100000, |B'(a0)|<26/1000.

Strong convexity and minimization of the supporting quadratic imply globally

B(a)>=B(a0)-(3/8)B'(a0)^2
 >-571/100000-(3/8)(26/1000)^2 >-6/1000.              (5)

On [11/20,4/5], R has its minimum at an endpoint. To see this, R' has the sign opposite to

C(a)=66a^3-98a^2+47a-8.

Here C''>0 on [1/2,1], C'(1/2)=-3/2, C(1/2)=-3/4 and C(1)=7. Thus C first decreases then increases and has exactly one zero in this interval. Therefore R increases then decreases, so has no interior minimum. Its exact endpoint values are

R(11/20)=3267/328000>9/1000,
R(4/5)=3/125>9/1000.

Together with (5), this proves B+R>3/1000 on [11/20,4/5].

Outside that interval, the certificate gives

B(11/20)>1/100, B'(11/20)<0,
B(4/5)>1/100, B'(4/5)>0.

Since B' is increasing, B>1/100 on [1/2,11/20] and [4/5,1). As R>=0 throughout, (1) follows everywhere.

## 5. Exact numerical constants and endpoints

heavy_zero_population_scalar_certificate.py checks every logarithmic comparison above using Fraction arithmetic and160 terms of

log q=2 sum_(j>=0) ((q-1)/(q+1))^(2j+1)/(2j+1).

The omitted absolute tail is bounded by

2|z|^321/[321(1-z^2)], z=(q-1)/(q+1).

The resulting .json records every exact comparison as true. Floating diagnostics are not premises. Cases with b=0 or c=0 follow by continuity; all preceding convexity estimates extend by limits. At a->1, t->0 and x->1, the original envelope tends log(4/3)>3/1000.
