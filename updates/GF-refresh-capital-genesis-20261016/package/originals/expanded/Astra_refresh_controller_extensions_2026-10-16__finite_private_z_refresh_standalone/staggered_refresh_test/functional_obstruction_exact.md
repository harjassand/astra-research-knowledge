# Exact functional obstructions to the two-gap product bound

**Scope:** These are counterexamples to an abstract entire-function lemma. They are **not** counterexamples to a specified staggered-refresh Hamiltonian/history model. In particular, no admissible irreversible first-mismatch record realization is asserted.

## Proposed lemma

Suppose a vector-valued entire function F(z,w) has separate exponential types at most a and b, satisfies ||F(x,y)|| <= M on the real plane, and takes values in orthogonal output sectors E1 + E2 with

- E1 F(0,w) = 0 for every w;
- E2 F(z,0) = 0 for every z.

The proposed conclusion is

    ||F(1,1)||^2 <= M^2 [1 - cos^2(min(a,pi/2)) cos^2(min(b,pi/2))].

This is false. It remains false if the first component is odd in z and even in w, and the second is even in z and odd in w.

## 1. Strictly contractive, parity-compatible example

Put a = b = arccos(2/3), x = az, y = bw, and define

    G1(z,w) = sin(x) [1 + (1/2) cos(y)],
    G2(z,w) = sin(y) [1 + (1/2) cos(x)],
    F(z,w)  = (sqrt(20)/7) (G1(z,w), G2(z,w)).

Take E1 and E2 to be the coordinate projectors. The functions are entire with the stated types and respective-axis nullities. Their parity is exactly (odd,even) and (even,odd).

### Exact global norm

For real x,y set u = cos(x), v = cos(y). Then

    Q(u,v) = ||G||^2
           = (1-u^2)(1+v/2)^2 + (1-v^2)(1+u/2)^2.

Replacing u or v by its absolute value does not decrease Q, so a maximum occurs in [0,1]^2. Write s = u+v and p = uv. Expansion gives

    Q = 2 + s - (3/4)s^2 + (3/2-s)p - p^2/2.

If 0 <= s <= 1, then 0 <= p <= s^2/4 and

    dQ/dp = 3/2-s-p >= 1/4.

Thus the maximum at fixed s is attained at u=v=r=s/2. On this diagonal,

    Q(r,r) = 2(1-r^2)(1+r/2)^2.

Its maximum is at r=(sqrt(3)-1)/2, with value

    M_G^2 = (9+6 sqrt(3))/8.

If 1 <= s <= 2, completing the square in p instead gives

    Q <= 25/8 - s/2 - s^2/4 <= 19/8 < M_G^2.

Consequently the displayed M_G^2 is the exact global maximum. Since

    (9+6 sqrt(3))/8 < 49/20

(the inequality is equivalent to 30 sqrt(3) < 53), F is strictly contractive on the whole real plane:

    sup ||F||^2 = (20/49) M_G^2 < 1.

We may therefore use M=1 in the proposed lemma.

### Exact violation

At (z,w)=(1,1), cos(x)=cos(y)=2/3 and sin^2(x)=sin^2(y)=5/9. Therefore

    ||G(1,1)||^2 = 160/81,
    ||F(1,1)||^2 = 3200/3969.

The claimed right side with M=1 is

    1 - (2/3)^4 = 65/81 = 3185/3969.

Thus the excess is exactly

    15/3969 = 5/1323 > 0.

## 2. Stronger example with a lossless entire unitary completion

The preceding failure is not merely an inability to complete the vector to a unitary family. Put a=b=pi/3, x=az, y=bw, and define

    g(z,w)  = 2 cos^2(x/2) cos^2(y/2) - 1,
    F1(z,w) = sin(x) cos^2(y/2),
    F2(z,w) = cos(x/2) sin(y).

These are entire of separate types no greater than (a,b). Their parities are, respectively, (even,even), (odd,even), and (even,odd). The required respective-axis nullities hold.

For real x,y let

    v = (cos(x/2) cos(y/2), sin(x/2) cos(y/2), sin(y/2)).

Then v^T v=1, and the real orthogonal matrix

    U(z,w) = 2 v(z,w) v(z,w)^T - I

satisfies

    U(z,w) e0 = (g(z,w), F1(z,w), F2(z,w)).

The algebraic identity v^T v=1 holds for complex arguments as well. All entries of U are entire of separate types at most (a,b). In particular, on the real plane,

    g^2 + F1^2 + F2^2 = 1,

so sup ||F||=1. The two commuting parity matrices

    D1 = diag(1,-1,1),  D2 = diag(1,1,-1)

give the exact conjugation symmetries

    U(-z,w) = D1 U(z,w) D1,
    U(z,-w) = D2 U(z,w) D2.

At (1,1), x=y=pi/3, and

    g=1/8,  F1=3 sqrt(3)/8,  F2=3/4,
    ||F(1,1)||^2 = 63/64.

The claimed product bound is

    1 - cos^4(pi/3) = 15/16 = 60/64.

The excess is exactly 3/64.

### Exact failure of the required chronological completion

This family can be factored as a conjugated reflection using rotations of x/2 and y/2. Such a factorization revisits the x rotation around the y rotations, rather than placing all x-scaled interactions before all y-scaled interactions.

There is an exact obstruction to reinterpreting this same full first-column state as the required chronological record dilation. Write its unscaled-angle state as h(x,y)=(g,F1,F2). Then

    h(0,y)  = (cos(y), 0, sin(y)),
    h(pi,y) = (-1, 0, 0),
    <h(0,y), h(pi,y)> = -cos(y).

In contrast, any complete causal record dilation of the form

    W(x,y) = B(y) A(x),

with B(y) an isometry for real y, obeys

    W(x,y)^* W(x',y) = A(x)^* A(x'),

which is independent of y. The displayed overlap violates this necessary condition. Thus this particular full Householder completion cannot be such a chronological record dilation.

Projection onto selected final record sectors can destroy the kernel identity. Therefore this witness excludes only the proposed full completion, not every possible causal completion of its projected mismatch vector. It does not solve or refute the actual staggered schedule.

## 3. What a valid causal proof must additionally establish

One sufficient structure is a sequential first-mismatch instrument. If the first-step mismatch probability is p1 <= sin^2(a), and the mismatch probability at the second step conditional on the normalized first-survivor state is p2_given_survival <= sin^2(b), then

    p_union = p1 + (1-p1) p2_given_survival
            <= p1 + (1-p1) sin^2(b)
            <= 1 - cos^2(a) cos^2(b).

The clipping at pi/2 is immediate. The key missing hypothesis is a survivor-normalized conditional bound with the relevant chronological action budget. Uniform contractivity, entire type, axis nullity, definite parity, and even a lossless entire unitary completion do not imply that bound by themselves.

The functional counterexamples therefore rule out a proof that uses only those analytic properties. They do not decide whether additional first-mismatch causality rescues the desired result for the physical staggered-refresh model.
