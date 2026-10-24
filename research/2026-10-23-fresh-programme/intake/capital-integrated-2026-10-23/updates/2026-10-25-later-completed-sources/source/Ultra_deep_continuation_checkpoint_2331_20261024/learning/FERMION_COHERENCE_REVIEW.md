# Whole review: canonical equivalence and weak-bridge pair coherence

24 October 2026. Review by the existing learning Sol owner. The constructor
provided the path directly. I read all 470 lines of
`fermion/CANONICAL_COHERENCE.md`, SHA-256
`9bf0a44029e10f22c3285f86cb68d091bb77ed602fa7636d6d58480c3d9a446e`,
and checked its dependencies against the preceding whole evaluator review.
No constructor files, old proofs, or recorded source observations were changed.

## Finding

**PASS for the stated native four-site-block family and uniform certificate
(C).** I found no missing volume factor, filtered-stability assumption, CLT
conditioning oracle, or invalid distant-pair summation in this proof. The new
argument supplies a weak-bridge persistence result that the evaluator alone
did not prove. It keeps the reference's already established coherence separate
from the perturbation and exact-number transfer.

The result is at fixed degree, fixed local structure and an extremely small
verified bridge envelope, with an explicitly enormous finite-size threshold.
It remains a property of the supplied wavefunctions, not a preparation,
Hamiltonian ground-state, stiffness or material theorem. The construction's
comparison and priority qualifications remain unchanged.

## 1. The localized log ratio really has no volume factor

For a selected nonadjacent pair, the base and both filtered models use exactly
the same merged partition and fermionic mode order. There is no native edge
between the two merged blocks, so its unfiltered reference is the product of
their original references. All reference factors outside the merged mark and
all activities whose supports miss it are identical in the three gases.
Consequently every log cluster avoiding the mark cancels term by term.

The tilted KP theorem bounds the absolute cluster sum touching one vertex by
the same per-vertex `S` used in (C). It can be obtained with the zero-weight
singleton test or by overcounting a cluster through an occurrence of a polymer
containing that vertex. Applying this bound separately to the two models gives
`|Q_pm-Q_0|<=2S`, rather than `O(MS)`. Repeated polymers and clusters touching
the mark multiple times are harmless: marking occurrences only overcounts.

The filter reference perturbation is bounded by
`(2t+t^2)2^4<1/8` throughout the larger inner logarithmic domain. The branch
of its logarithm near one is therefore at most `1/7`. Combining with `2S`
gives `|log R_pm|<1/2`; no inconsistent branch is introduced because the
ratios are the same nonzero analytic functions given by the convergent gases.
Thus `|R_pm|<2`. Cauchy on a radius-`1/8` log-fugacity disk yields

```
|R_pm'|<=16,
|R_O(re^(i theta))-R_O(r)| <= 8|theta|/t.
```

The derivative estimate holds uniformly along the complete inner arc. Its
constant depends on the fixed two-block filter, not on the pair separation or
the total system size.

At positive radius the native marked reference ratio is at most
`(1+t)^2<2`. Since `|exp u-1|<=2|u|` for `|u|<=1/2`, each filtered ratio
changes from its reference value by at most `8S`. Polarization then gives

```
|R_O(r;E)-2 gamma(r)^2| <= 4S/t.
```

This is the required uniform local perturbation estimate. A finite-volume
wavefunction-continuity estimate growing with `M` would not suffice, and is
not what the note uses. The global degree cap `d_*=4` explicitly covers all
references after any two-block merge, including the unmarked ones; the earlier
degree-notation clarification is therefore already resolved here.

## 2. Full unfiltered Bernoulli local CLT and finite mass

The preceding scalar negative-root theorem applies to the **full unfiltered**
norm, with arbitrary complex bridges. It supplies a mathematical
Poisson-binomial factorization with at most `2M` factors. The roots and the
individual Bernoulli parameters are not computational inputs. No such
factorization is asserted for a filtered norm.

For one factor `f=q+p exp(i theta)`, direct differentiation gives the stated
third derivative. Its numerator is at most `pq` because
`|q-p exp(i theta)|<=1`; on `|theta|<=1/2`,
`|f|>=cos(1/4)>31/32`. Thus the derivative is at most `2pq`. Taylor's theorem,
after centering and summing all factors, gives

```
log phi_c = -sigma^2 theta^2/2 + R,
|R|<=sigma^2 |theta|^3/3.
```

This bound is uniform for nonidentical parameters approaching zero or one.
Deterministic factors merely shift the mean. The exponential difference is
bounded on this interval by
`(sigma^2 |theta|^3/3) exp(-sigma^2 theta^2/3)`. Its full-line normalized
integral is exactly `3/(2pi sigma^2)`, below `1/sigma^2`.

For the remaining Fourier arc,
`|phi_c|<=exp[-2sigma^2 sin^2(theta/2)]` follows by multiplying the exact
one-Bernoulli modulus. On `1/2<=|theta|<=pi`, this is at most
`exp(-sigma^2/9)`. The normalized arc has length below one, and
`u exp(-u/9)<=9/e<4`, giving the stated `4/sigma^2` tail bound. The comparison
Gaussian's full-line tail is below
`2 exp(-sigma^2/8)/(pi sigma^2)<1/sigma^2`. Hence the total error is actually
below `6/sigma^2`; `20/sigma^2` is conservative.

The oscillatory phase for any integer `k` has modulus one, so this proves the
uniform local estimate, not only a distribution-function CLT. If
`|mu-k|<=1/4` and `sigma>=160`, the Gaussian term is at least `1/(4sigma)`
and `20/sigma^2<=1/(8sigma)`. Therefore `p_k>=1/(8sigma)` with the advertised
finite cutoff.

The variance is also derived rather than supplied. Throughout the tilt
bracket the reference variance is at least `nu M/2`; Cauchy gives

```
|Q_0''| <= 2MS/s0^2 <= nu M/8,
3nu M/8 <= sigma^2 <= M/2.
```

The lower inequality uses the actual certificate
`S<=nu s0/128` and `s0=1/8`; the upper uses at most `2M` Bernoulli factors.
All conditioning quantities in the later bounds can thus be replaced by
explicit functions of `M,nu`, without a variance oracle.

## 3. Canonical transfer and the outer marked numerator

Fourier inversion of the numerator and denominator gives exactly the
canonical/grand difference written in section 5. On the inner arc its numerator
is `Z(z)[R_O(z)-R_O(r)]`. The localized derivative and global unfiltered
modulus imply

```
(1/(2pi)) integral |theta| |Z(re^(i theta))/Z(r)| dtheta
 <= 2/sigma^2.
```

For example, `sin(theta/2)>=|theta|/4` bounds the full-line integral by
`4/(pi sigma^2)<2/sigma^2`. Multiplying by `8/t` and dividing by
`p_k>=1/(8sigma)` yields the claimed `128/(t sigma)`.

The proof correctly switches representations on the outer arc. It bounds
`Z_O=(Z_+-Z_-)/(4t)` directly. It never divides there by `Z(z)` or a vanishing
reference factor. Each unmarked native block has variance at least `1/6` in
the stated factor-two tilt bracket, and for `M>=3`,

```
V_u >= (M-2)/6 >= nu(M-1)/4.
```

The marked forest estimate consequently gives the exponent
`-3nu(M-1)/16` for each filtered polynomial. The filtered real normalizers
are at most `(1+t)^2 Z(r)`. The subtracted base term has
`|R_O(r)|<=1` and faster full-law decay. With `M-1>=M/2` and
`(1+t)^2<2`, their combined coefficient is bounded by

```
(1+t)^2/(2t)+1 <= 2/t.
```

Outer integration and the same mass lower bound give
`16sigma exp(-3nu M/32)/t`. Thus equation (13) follows with no stability or
CLT assumption for either filtered model. A completely explicit version is

```
error <= 128/[t sqrt(3nu M/8)]
       + (16/t)sqrt(M/2) exp(-3nu M/32).
```

It tends to zero uniformly over all nonadjacent endpoint choices. This is the
new exact-charge step; the earlier polynomially small mass bound alone would
not have given this vanishing error by the same absolute-value argument.

## 4. Normalization, uniform pair bound and macroscopic eigenvalue

The hard-space singlet annihilator `b=B/sqrt(2)` is a norm-one partial
isometry. On disjoint selected bonds, `T=b_a^dagger b_b` maps orthogonal
initial/final subspaces, so `O=T+T^dagger` has norm one. The factor of two in
`<O>=2 Re<T>` is consistently retained throughout the filters and final bounds.

The isolated reference's formula gives
`gamma(r)^2>=25/5408>1/256` on the entire tilt bracket. Consequently the
grand perturbation and canonical transfer give exactly (14). At the specified
`M0`, each of its three error terms is at most `1/2048`. The remaining lower
bound is `5/2048`, so the stated `1/512` is safely smaller. The condition
`M0>=16/(3nu)` makes `sqrt(M) exp(-3nu M/32)` decrease for all later sizes.
The rational power-of-two/exact squared-comparison test at `M0` is a valid
upper enclosure. Its doubling acquisition is finite; the very large threshold
is not presented as a useful experimental size.

For the pair matrix, positivity follows from its Gram representation. Each
diagonal is nonnegative and each entry has magnitude at most one. There are
at most `DM` ordered adjacent off-diagonal pairs. The all-ones Rayleigh quotient
therefore gives

```
lambda_max(P) >= (M-1-D)/512-D.
```

This subtracts all potentially adverse adjacent terms; it assumes neither
their positivity nor independence of different pair entries. Uniformity over
nonadjacent pairs is essential, because there are order `M^2` such terms.
For a fully explicit positive linear statement, take additionally
`M>=2+1026D`; then the bound is at least `M/1024`. This is just an explicit
threshold version of the note's fixed-`D` `Omega(M)` conclusion.

Finally, the hard projectors do not alter these pair-RDM matrix elements.
Annihilation cannot create double occupancy, and double-occupancy components
created by the adjoint are orthogonal to the hard bra. Thus

```
<b_a^dagger b_b> = <B_a^dagger B_b>/2
```

on this state. The selected normalized singlet two-fermion vectors have
disjoint supports and are orthonormal. `P` is therefore a genuine compression
of the ordinary two-particle RDM with trace `choose(N,2)`. Its positive linear
eigenvalue lower bound transfers to the full RDM. Since `N=2M`, this proves
the claimed macroscopic pair eigenvalue. It does not prove stiffness or a
Hamiltonian ground-state property.

## 5. Checks and boundaries of this review

In a bytecode-disabled exact rational calculation with no output files I independently
recomputed the four-site reference coefficients `[1,8,4]`, both unnormalized
`B_01` sector transition elements `2,2` (hence normalized `sqrt(2),sqrt(2)`),
and the reference `M=k=3` transfer ratio `21/352`. This was finite algebra,
not an additional source observation or a test of a large lattice.

Only two of the owner's existing Luna supports were reactivated: one for the
new finite CLT/variance calculation, one for localized cancellation and outer
numerator handling. Their inline bounded checks corroborate the independent
derivations above; no new worker or support report was created. The reviewed
coherence source retained its quoted hash after the read and algebra check.

I found no substantive repair required in this note. All conclusions remain
conditional on the explicit native family and certificate (C), the exact
graded representation and the already reviewed scalar stability/KP results.
The zero-bridge ODLRO benchmark is not the new result; the new proved content
is uniform weak-bridge persistence through exact-number projection. Neither
this review nor finite reference algebra certifies novelty, physical operation
or a practical advantage over equally informed conventional methods.

## Literal review assignment, retained once

> Your evaluator whole review is accepted and constructor applied d_* clarification without code changes. Once constructor saves its separate canonical-equivalence/pair-ODLRO note, use this same Sol slot for adversarial whole review of the localized cluster cancellation, full unfiltered Bernoulli local CLT, outer marked numerator handling, and uniform distant-pair to Omega(M) Rayleigh step. Do not infer coherence from the existing evaluator alone; zero-bridge coherence is an established reference property and weak bridges need a uniform error proof. Constructor is writing it now; coordinate the note path directly. Existing four supports only if a new bounded question genuinely helps; no new workers or source observations.
