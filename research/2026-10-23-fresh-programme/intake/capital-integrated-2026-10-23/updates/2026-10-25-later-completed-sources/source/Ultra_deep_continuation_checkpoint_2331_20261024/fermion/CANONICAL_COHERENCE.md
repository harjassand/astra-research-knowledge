# Canonical equivalence and stable pair ODLRO in the controlled block family

24 October 2026. Owned theorem candidate, continuing the supplied-state
contraction construction. This note adds a state property that does not follow
merely from having an observable evaluator. It does not assert a physical
preparation, a Hamiltonian ground state, stiffness, a material phase, or novelty.
The zero-bridge reference already has pair ODLRO. The result below is a uniform
weak-bridge persistence statement, including exact particle number, rather than
a mechanism that creates order from an initially unpaired state.

The dependencies are the exact graded block/edge representation, the signed KP
and marked-sector bounds in `BLOCK_CANONICAL_OBSERVABLES.md`, and the internally
reconstructed hard scalar-charge negative-root theorem in
`CANONICAL_CONTRACTION.md`. The latter was independently reconstructed in the
whole Sol review; a finite numerical root test is not its proof. The additional
localization, finite local-CLT calculation, canonical equivalence and pair-matrix
bound are given here explicitly.

## 1. An actual native state family and a uniform two-block certificate

There are `M` four-site blocks, hence `4M` physical sites. On each block labelled
`0,1,2,3`, set the symmetric internal matrix entries

```
F_01=F_23=F_02=F_13=1,
```

with all other internal entries zero. Let `E` be any symmetric complex-rational
cross-block matrix. Its actual physical degree is at most the fixed `Delta`,
and its block graph has degree at most fixed `D`. A verified rational envelope
bounds every cross entry by `lambda`. Use the supplied matrix itself; a general
diagonal congruence is not a free finite-hole state gauge. The partition can be
acquired by the earlier threshold-component search when `lambda<1/2`: the unit
internal edges form precisely these connected four-site blocks.

The state is the hard no-double-occupancy, exactly `2M`-electron state

```
|Psi_M> proportional to P_(N=2M) P_G
       exp(sum_ij F_ij c†_(i,up)c†_(j,down)) |vac>.
```

Thus its pair number is `k=M` and its electron filling is one half. No energy
or ground-state promise is part of this input. Graphs can be nonbipartite and
have growing width. Bounded degree and block size, rather than bounded
treewidth, are the contraction premises.

Use the following deliberately conservative uniform constants:

```
nu=1/4,       s0=1/8,       r0=1/2,
b_*=8,       d_*=4,         D_*=max(1,2D),
t=2^(-d_*-5)=1/512,
v >= 2 sqrt(2) lambda,       v<=1,
h=2^(d_*+2) 2^(b_* Delta) v,
x=4 D_* 3^5 h,
S=x²/[4D_*(1-x)].
```

For instance `v=3lambda` is a rational choice. Verify

```
x<=1/4,
S<=min(nu s0/128, t/4096, 1/64),
S+(D_*+1)h 3^d_*<=nu/16.                                      (C)
```

These tests use explicit matrix data and rational arithmetic. They hold for a
nonempty size-independent interval of actual bridge strengths at fixed
`D,Delta`. Their constants can be extremely small; no practical coupling range
is claimed. A failed certificate gives no conclusion about the state.

The constants dominate the unmerged model and EVERY partition obtained by
merging two nonadjacent blocks. For such a pair, there is no cross edge internal
to the merged union. Its reference polynomial is the product of the two native
block polynomials. The new size is at most eight, degree at most `2D`, physical
cross degree at most `Delta`, and ALL block charge degrees are at most four.
Consequently the same `h,S` bound the unfiltered and both marked models for
every such pair, independently of their separation and of `M`. All fermionic
permutation signs are retained when the two blocks are placed together.

The previous paid tilt search gives a positive rational `r in [1/4,1]` with
full-state tilted mean `|mu(r)-M|<=1/4`, for all sufficiently large `M`. Its
inputs are the exact finite block polynomials and differentiated truncated
clusters, not supplied Bernoulli factors or a mean oracle. Finite exceptions
can be enumerated as in the previous theorem. The coherence theorem concerns
the large-size range stated explicitly below.

## 2. Normalized pair mode and the reference benchmark

For a selected internal bond `(i,j)` define

```
B_ij† = c†_(i,up)c†_(j,down)-c†_(i,down)c†_(j,up),
b_ij = P_G B_ij P_G / sqrt(2).
```

The normalized singlet `B_ij†|vac>/sqrt(2)` is taken to `|vac>` by `b_ij`.
On the hard Hilbert space `b_ij` is a norm-one partial isometry. Select the
same bond `(0,1)` in every block and call its mode `b_a`. Distinct block modes
have disjoint physical supports. For `a!=b` set

```
T_ab=b_a† b_b,
O_ab=T_ab+T_ab†=(B_a† B_b+B_b† B_a)/2   on the hard space.
```

`T_ab²=0` and its initial and final subspaces are orthogonal; it exchanges
empty-a/singlet-b with singlet-a/empty-b, with spectator modes unchanged.
Therefore `||O_ab||=1`. It is charge conserving and even. This fixes all factors
of two in the marked filter and the pair-density matrix.

An isolated block has exactly

```
B(z)=1+8z+4z²,
mu_B(1/2)=1,       V_B(1/2)=1/3.
```

If `Omega_q` denotes its unnormalized `q`-pair sector, direct fermion algebra
gives

```
<Omega_0|b_01|Omega_1>=sqrt(2),
<Omega_1|b_01|Omega_2>=sqrt(2).
```

In the second matrix element the two resonating coverings contribute
`2sqrt(2)` and `-sqrt(2)`; their interference sign is not discarded. Thus the
auxiliary positive-fugacity block mean is

```
gamma(r)=<b_01>_ref,r=sqrt(2r)(1+r)/(1+8r+4r²).                  (1)
```

At `r=1/2` it is `1/4`. Uniformly for `r in [1/4,1]`,

```
gamma(r)² >= 25/5408 > 1/256.                                  (2)
```

This follows by bounding `2r>=1/2`, `1+r>=5/4`, and `B(r)<=13`.
The product-block reference has `<O_ab>_ref,r=2gamma(r)²`.

For comparison, its exact canonical correlation, without ANY bridge, is

```
<T_ab>_(M,k),E=0
 = [z^k]{2z(1+z)² B(z)^(M-2)} / [z^k]B(z)^M.                   (3)
```

At `M=k=3` this is `42/704=21/352`. At `k=M` it tends to `1/16`.
The zero-bridge operation is ordinary polynomial coefficient DP, not a new
hard-contraction result. Exact global number projection kills `<b_a>` but
retains the neutral pair-transfer correlations in (3).

## 3. Localize the marked ratio before taking a thermodynamic limit

Fix ANY nonadjacent `a,b`, merge their blocks, and use the SAME merged partition
for the unfiltered base and the two mathematical norm filters
`A_+=I+tO_ab`, `A_-=I-tO_ab`. The inserted filter matrices remain AFTER the
cross-edge operators in each activity. They are not commuted through creation.
Let `Z,Z_+,Z_-` be the corresponding analytic norm polynomials and set

```
R_+(z)=Z_+(z)/Z(z),  R_-(z)=Z_-(z)/Z(z),
R_O(z)=(R_+(z)-R_-(z))/(4t)=Z_O(z)/Z(z).
```

Here `Z_O(z)=sum_q <psi_q|O_ab|psi_q> z^q`. On the positive ray `R_O(r)` is the
grand-canonical expectation and has magnitude at most one. The filtered
polynomials need NOT be real-rooted.

Write `Q_j=log[Z_j/product_B B_(B,j)]` for each of the three signed gases.
Only the merged marked reference factor and activities containing that block
change. Every log cluster missing it is IDENTICAL and cancels exactly. The KP
rooted-cluster bound gives

```
|Q_+-Q_0|<=2S,       |Q_--Q_0|<=2S.                            (4)
```

For clarity, a log cluster touching the mark contains at least one polymer
containing the mark. Mark one such occurrence, overcount if necessary, and use
the usual fixed-polymer rooted bound. The total absolute sum is at most
`sum_(C contains mark)|w(C)|exp(|C|)`, which is at most `S` by the same connected
support count used in the certificate. Apply it separately to the two models.
There is no factor of `M` in (4). This is where using the same partition matters.

On the larger logarithmic domain of radius `s0` around the inner arc, the native
merged polynomial has charge degree four and

```
|B_mark,±/B_mark,0-1| <= (2t+t²)2^4 < 1/8.
```

The branch of its log near one therefore has magnitude at most `1/7`. Together
with (4) and (C), this gives `|log R_±|<1/2`, hence `|R_±|<2`, uniformly in
`M,a,b`. A disk of radius `s0` about every inner-arc log-fugacity lies in this
larger domain. Cauchy's estimate then gives

```
|d R_±/d log z|<=16,
|R_O(r exp(i theta))-R_O(r)| <= (8/t)|theta|,
                         |theta|<=pi/2.                       (5)
```

All these ratios are evaluated in a zero-free sector, never through a negative
reference zero.

Because `a,b` are nonadjacent, their native merged reference is still the
product reference at `E=0`. On the positive ray its filtered ratio is at most
`(1+t)²<2`. Equation (4), `|exp u-1|<=2|u|` for `|u|<=1/2`, and polarization
therefore imply the uniform grand-canonical perturbation bound

```
|R_O(r;E)-2gamma(r)²| <= 4S/t.                                 (6)
```

This controls an extensive wavefunction perturbation by LOCAL cluster weights;
it is not a fixed-finite-volume continuity argument applied at growing `M`.

## 4. A finite Poisson-binomial local-CLT bound

The unfiltered scalar norm polynomial has only negative real roots, by the
previous reconstructed chiral-derivative argument. Thus for each positive `r`
its tilted charge law is a sum of independent Bernoulli variables, as a
mathematical representation. No roots or Bernoulli sample oracle are needed by
the contraction algorithm. Let its mean be `mu` and variance be `sigma²>0`.
There are at most `2M` factors.

For a Bernoulli parameter `p`, put `q=1-p` and `f(theta)=q+p exp(i theta)`.
For `|theta|<=1/2`, choose the log branch from `f(0)=1`. Direct differentiation
gives

```
(log f)''' = -i p q exp(i theta)(q-p exp(i theta))/f(theta)^3.
```

The numerator magnitude is at most `pq`, while
`|f(theta)|>=cos(1/4)>31/32`. Hence its third derivative is at most `2pq`.
After summing factors and removing the mean,

```
phi_c(theta)=exp[-sigma²theta²/2+R(theta)],
|R(theta)|<=sigma²|theta|³/3,        |theta|<=1/2.                (7)
```

Consequently

```
|phi_c(theta)-exp(-sigma²theta²/2)|
 <= (sigma²|theta|³/3) exp(-sigma²theta²/3)
```

on that interval. Its full-line integral, including the `1/(2pi)` inversion
factor, is `3/(2pi sigma²)<1/sigma²`. Deterministic Bernoulli factors only shift
the mean and do not affect this calculation.

Globally,

```
|phi_c(theta)| <= exp[-2sigma² sin²(theta/2)],   |theta|<=pi.     (8)
```

The actual Fourier tail `1/2<=|theta|<=pi`, with inversion normalization, is at
most `exp(-sigma²/9)<=4/sigma²`. Use `sin(1/4)>6/25` and maximize
`u exp(-u/9)` to check these constants. The comparison Gaussian's full-line
tail outside this interval is at most
`2 exp(-sigma²/8)/(pi sigma²)<1/sigma²` by a one-step Mills bound. Thus the
following deliberately looser estimate is proved, uniformly in every integer
`k`, for `sigma>=1`:

```
|Pr(K=k) - exp[-(k-mu)²/(2sigma²)]/(sqrt(2pi)sigma)|
 <= 20/sigma².                                                (9)
```

The oscillatory factor `exp[-i(k-mu)theta]` has unit modulus in each error
integral. In particular, if `|mu-k|<=1/4` and `sigma>=160`, the Gaussian term
is at least `1/(4sigma)` and (9) gives

```
Pr(K=k)>=1/(8sigma).                                          (10)
```

These are finite estimates with actual cutoffs, not an asymptotic CLT invoked
without hypotheses.

In the present block family, throughout the acquired factor-two tilt bracket
the reference variance is at least `nu M/2`. Cauchy's estimate for the SAME
unfiltered cluster log gives `|Q_0''|<=2MS/s0²`. Condition (C) therefore yields

```
3nu M/8 <= sigma² <= M/2.                                     (11)
```

The upper bound is the general Poisson-binomial variance bound. The lower one
is a verified susceptibility, not an assumed extensive variance of the unknown
full state.

## 5. Canonical/grand-canonical equivalence for the two-block observable

At the paid full-state tilt `r`, let `p_k=Pr_r(K=k)` and `k=M`. Fourier inversion
gives the difference of expectations as the integral of

```
[Z_O(r exp(i theta))-R_O(r)Z(r exp(i theta))]/Z(r),
```

divided by `2pi p_k`, with the factor `exp(-ik theta)`. On the inner arc, use
(5) and (8). Since `sin(theta/2)>=|theta|/4` for `|theta|<=pi`,

```
(1/(2pi)) integral |theta| |Z(r exp(i theta))/Z(r)| dtheta
 <= 2/sigma².
```

The resulting inner contribution, after (10), is at most `128/(t sigma)`.

On the outer arc do NOT use the ratio `R_O`, which could be undefined there.
There are `M'=M-1` coarse blocks and `M-2` unmarked native references. Each
unmarked reference has variance at least `1/6` at this tilt; hence for `M>=3`

```
V_u(r)>=(M-2)/6 >= nu(M-1)/4.
```

The explicit marked forest bound and (C) give, for either sign,

```
|Z_±(r exp(i theta))|/Z_±(r) <= exp[-3nu(M-1)/16],
                                           |theta|>=pi/2.     (12)
```

This uses only native UNMARKED negative roots and positive coefficients of the
marked reference. No filtered stability is assumed. Also
`Z_±(r)<=(1+t)²Z(r)`. Together with (8),(11), `M-1>=M/2`, and `t<sqrt(2)-1`,
the absolute outer numerator is at most
`(2/t)Z(r)exp(-3nu M/32)`. Dividing by (10) gives the explicit finite bound

```
|<O_ab>_(canonical k=M)-<O_ab>_(grand r)|
 <= 128/(t sigma) + (16sigma/t)exp(-3nu M/32),
                         sigma>=160, |mu-M|<=1/4.             (13)
```

The constants are uniform in the positions of the two nonadjacent blocks.
The first term tends to zero as `M^(-1/2)` by (11); the second is exponentially
small. This closes the exact-number transfer that an evaluator or a pointwise
real-fugacity expansion alone would not supply.

## 6. Uniform pair coherence and a macroscopic two-particle eigenvalue

Combining (2),(6),(13) and `O_ab=2 Re T_ab` gives, for every nonadjacent pair,

```
Re <b_a† b_b>_(canonical)
 >= 1/256 - 2S/t - 64/(t sigma)
                   - (8sigma/t) exp(-3nu M/32).                (14)
```

For an explicit large-size statement, choose a fixed `M0>=3` so that

```
sqrt(3nu M0/8) >= max(160, 2^17/t),
M0 >= 16/(3nu),
(8/t)sqrt(M0/2) exp(-3nu M0/32) <= 1/2048.
```

Such an integer exists and can be acquired by doubling. The last test can use
the rational upper envelope
`(8/t)ceil(sqrt(M0/2))2^(-floor(3nu M0/32))`; square roots use integer squared
comparisons. The actual function `sqrt(M)exp(-3nu M/32)` is decreasing beyond
the displayed cutoff, so a successful test controls every `M>=M0`. These
constants are intentionally very loose and can make `M0` enormous; no useful
finite experimental size is inferred. They are fixed-parameter proof costs.

Using (C), each of the three subtracted terms in (14) is at most `1/2048`.
For all `M>=M0`, therefore,

```
Re <b_a† b_b> >= 1/512,       for every nonadjacent pair a,b.    (15)
```

Let `P_ab=<b_a†b_b>` be the `M by M` pair-mode matrix. It is positive
semidefinite: `u*Pu=||sum_a u_a b_a Psi||²>=0`. Its diagonal lies in `[0,1]`
and every entry has magnitude at most one. At most `DM` ordered pairs of
distinct blocks are adjacent. The all-ones Rayleigh quotient, subtracting
those possibly adverse terms rather than assuming them positive, gives

```
lambda_max(P) >= (1/512)(M-1-D)-D = Omega(M).                   (16)
```

The chosen singlet pair modes are orthonormal two-fermion vectors on disjoint
physical blocks. On a hard input, pair annihilation cannot create double
occupancy; any double-occupancy component created by its adjoint is orthogonal
to the hard bra. Thus the projectors in `b_a†b_b` do not change its matrix
element, and `P` is a compression of the ordinary fermionic two-particle RDM
with the convention whose trace is `choose(N,2)`. Since `N=2M`, (16) is a
macroscopic charge-two pair eigenvalue, or pair ODLRO of the specified states.
Exact number conservation still gives `<b_a>=0`.

This is uniform in graph width and separation at fixed degree, and permits
complex signed bridges. It is not just a positive-weight dimer model. It also
does not imply a gap, a condensate preparation, transport stiffness or a ground
state of a natural Hamiltonian. In particular the unbridged reference already
has (3); adding weak bridges is not the source of its ODLRO.

## 7. Computation, equally informed comparators, and actual exposure

The existing signed-block algorithm supplies relative canonical norms and
additive bounded neutral observables at fixed block size, degree, variance and
certificate margin. The merging overhead is constant even at distant endpoints.
For an explicit list of `O(M²)` pair entries, the number of evaluator calls is
polynomial; (16) instead follows from one uniform analytic bound without
evaluating them individually. The proof does not supply a sampler. Threshold
search, exact block tensors, bridge envelopes, tilt estimation, filter matrices,
graded routing, truncation, arithmetic precision and the exact-enumeration
fallback remain charged as in the preceding notes. The matrix is supplied;
neither its experimental acquisition nor a preparation/reset protocol is hidden
inside a contraction call.

The conventional zero-bridge coefficient DP is exact and is the strongest
baseline on that limit. An equally informed polymer implementation may use all
the same block, parity, scalar-root and canonical coefficient structure; no new
ownership of KP or the generic truncation algorithm is claimed. The reviewed
[Mann--Minko framework](https://arxiv.org/html/2306.08974v2) already supplies
the abstract signed-polymer algorithmic layer. The added interface here is the
native projected-fermion representation and its uniform exact-charge/marked
control, with the very small sufficient bridge regime made explicit.

Pair ODLRO and number projection are older phenomena. I read Yang's
[1989 eta-pairing paper](https://doi.org/10.1103/PhysRevLett.63.2144), sections
1--3, including its exact pair correlation and its distinction between an
eigenstate and a ground state. That construction supplies Hamiltonian
eigenstates, a stronger physical connection than is acquired here; its onsite
doublon pairs, however, are removed by the present hard projector. The primary
paper was read from its four-page Westlake-hosted scan. The
[1962 ODLRO paper](https://doi.org/10.1103/RevModPhys.34.694) was located only
as a publisher record, with full content requiring authorization; no full-read
claim is made for it.

For the actual projected-BCS comparison, I read the fixed-number definition and
pair-correlator treatment in
[Paramekanti--Randeria--Trivedi](https://arxiv.org/html/cond-mat/0101121).
They already study no-double fixed-number d-wave states by VMC and find ODLRO
in a physically motivated optimized regime. The present proof does not discover
that mechanism or establish superiority on those instances. The
[Edegger et al. analysis](https://arxiv.org/html/cond-mat/0506120) addresses
canonical versus grand-canonical projected BCS via fugacity and Gutzwiller
approximation. Our step is an explicit controlled signed-norm/local-CLT proof
for the stated family, not a replacement for their physical modelling.
Projected d-wave
[fPEPS contraction](https://arxiv.org/html/2208.04566v2) is another informed
baseline reaching relevant parameter regions not shown to satisfy (C).
The Sager--Mazziotti 2022 quantum-device pairing paper was read only at the
publisher abstract; it is further ancestry for finite-device pair-RDM witnesses,
not support for this theorem. No novelty-clearance inference follows from the
sources checked.

Development provenance: the owner developed the localized-ratio and canonical
equivalence route before this note, shared it inline with root, and retained the
exact cutoff proof here. Root supplied independent normalization, outer-bound
and Rayleigh challenges and reviewed the preceding proofs. The same four
exposed Luna supports checked bounded algebra, tails, sources and physical
meaning; their conclusions were rederived by the owner. This is cumulative,
reviewed research rather than a blind independent-discovery claim. Earlier
DIMER/gauge/phase-estimator failures and frozen scientific files are preserved.
