# Fixed-support reciprocal relations over prime extensions

## Result

For each fixed support size `w >= 3`, the large-prime-extension question has a
sharp geometric reduction. A degree-two inverse-graph relation of weight `w`
over `F_(2^ell)` for unbounded prime `ell` exists **if and only if** some
binary self-dual length-`w` code has an `F_2`-defined, positive-dimensional,
geometrically irreducible locally closed stratum in its all-nonzero,
pairwise-distinct reciprocal locus. In that case Lang--Weil gives such
relations for every sufficiently large `ell`, hence for every sufficiently
large prime `ell`. If no such stratum exists, all sufficiently large prime
extensions are excluded at that fixed `w`.

This gives a precise target for the unresolved girth gate. It does not show
that the tensor identity forces a proper constant field, and it does not
produce an `F_2`-varying reciprocal configuration.

## Tensor identity behind the code locus

Write `u_i` and `u_i^(-1)` in an `F_2` basis of `F_(2^ell)`, with binary
coordinate columns `x_i,y_i`. Vanishing of the full degree-two lift sum
implies

```text
sum_i 1 = 0,   sum_i x_i = sum_i y_i = 0,
sum_i x_i tensor x_i = sum_i y_i tensor y_i
                    = sum_i x_i tensor y_i = 0.
```

Applying the `F_2`-linear Frobenius maps in each tensor factor gives, for all
`a,b mod ell`,

```text
sum_i u_i^(2^a + 2^b) = 0,
sum_i u_i^(-2^a - 2^b) = 0,
sum_i u_i^(2^a - 2^b) = 0.
```

The last family is the cross-tensor identity. The tensor equations mean the
binary row span of the two coordinate arrays and the constant row is
self-orthogonal; extending it to a self-dual code `C` gives the exact
finite-type locus

```text
X_C = { [z] in P(C tensor Fbar_2) : z_i != 0,
        z_i != z_j (i != j), and (1/z_i)_i in C tensor Fbar_2 }.
```

It is defined over `F_2`: on the coordinate torus, reciprocal membership is
given by clearing denominators in the linear equations for `C`. There are
only finitely many such codes for fixed `w`.

## Prime-degree argument

Stratify each `X_C` into finitely many geometrically irreducible locally
closed strata over `Fbar_2`, with Frobenius permuting the strata. Since there
are finitely many codes and strata at this fixed `w`, their Frobenius orbit
lengths have a finite maximum `B_w` (no useful explicit bound is needed for
this implication).

Let `ell > B_w` be prime and let `p in X_C(F_(2^ell))`. The unique stratum
containing `p` is carried to itself by `Frob^ell`, because `p` is fixed by
that Frobenius power. If its Frobenius orbit has length `d`, then `d | ell`.
Since `d <= B_w < ell` and `ell` is prime, `d=1`. Thus the stratum itself is
defined over `F_2`.

It cannot be zero-dimensional: a Frobenius-stable geometrically irreducible
zero-dimensional stratum is an `F_2` point, whose nonzero projective
coordinates are all equal, contrary to pairwise distinctness for `w >= 2`.
So any relation for a prime `ell > B_w` lies on an `F_2`-defined
positive-dimensional geometrically irreducible stratum.

Conversely, an `F_2`-defined positive-dimensional geometrically irreducible
locally closed stratum inside `X_C` has `F_(2^ell)` points for all sufficiently
large `ell` by Lang--Weil. Those points remain nonzero and pairwise distinct,
so they are genuine inverse-graph relations. Pigeonholing over the finitely
many codes and strata establishes the stated iff for unbounded prime `ell`.

## What remains to prove

The exact missing implication is now geometric, not a generic
subfield/Kneser claim: for each fixed `w`, either rule out every
`F_2`-defined positive-dimensional geometrically irreducible stratum of every
`X_C`, or exhibit one. The known `F_128` curve does not settle this: a
positive-dimensional component defined only over `F_128` has Frobenius orbit
length dividing `7`, and its points need not descend to prime degrees other
than `7`. Conversely, the tensor identities alone have not been shown to
exclude an `F_2`-defined component.
