# Finite composition receiver for up to five qutrit Weyl-Bell states

## Scope and conventions

Let A and R be qutrits. All logarithms are natural. Put
`W(Z)=(Tr(Z) I-Z^T)/2`, `N=W_A tensor id_R`,
`E(X)=I_A/3 tensor Tr_A(X)`, and
`Delta(X)=Tr X log X+Tr EX log EX-2 Tr NX log NX`.
Let omega be a primitive cube root of unity and
`Phi_ab=3^(-1/2) sum_j omega^(bj)|j,j+a>` (indices modulo three).
For any probability vector p supported on at most five of these nine
orthogonal Bell states, the acquired conclusion is

**Delta(sum_ab p_ab |Phi_ab><Phi_ab|)>=(1-sum_ab p_ab^2)/128.**

For a point mass, Delta is exactly zero. The theorem covers arbitrary real
weights and all choices of at most five labels. It is not a theorem for
all nine-state mixtures or general Choi states. Historical novelty is
not established. The two entropy/purity extremum bounds below are prior.

## Exact channel reduction

Use the permutation `|u,d> -> |u+d,u+2d>`. In this basis

`N(rho_p) = I_3/3 tensor M_p`,
`M_p = sum_ab p_ab S_ab`,
`S_ab = |s_ab><s_ab|`,
`s_ab=(|a+1>-omega^(-b)|a+2>)/sqrt(2)`.

These are the Hesse SIC projectors: `Tr S_i S_j=1/4` for distinct
indices, `S_i^2=S_i`, `Tr S_i=1`, and `sum_i S_i=3I`.
Consequently, writing `s=sum_i p_i^2`,

`Tr M_p^2=(1+3s)/4`,
`Delta(rho_p)=2 S(M_p)-H(p)`.

This is a linear channel identity, not an entropy fit. The exact replay
in `replay_sic_exact.py` works over Q[omega]/(omega^2+omega+1). It checks
all 729 entries for the nine basis projectors, so linearity proves the
identity for every p. It also checks all 81 SIC and 81 Bell overlaps.

For a direct symbolic derivation, partial transposition gives the entries
`[delta_ik delta_jl-delta_(j,k+a)delta_(l,i+a)omega^(b(k-i))]/6`.
Under `i=u+d,j=u+2d,k=v+e,l=v+2e`, the two deltas in the second term
are equivalent to `u=v` and `e=-d-a`. The entry becomes
`delta_uv[delta_de-delta_(e,-d-a)omega^(b(e-d))]/6`, precisely
`delta_uv S_ab[d,e]/3`. The reflection fixes d=a and exchanges a+1,a+2,
giving the displayed rank-one vector for S_ab.

## Prior entropy envelopes and the one-dimensional receiver

For `1/5<=s<=1`, define

`z=(1+sqrt(4(5s-1)))/5`,
`U5(s)=h2(z)+(1-z)log(4)`.

For `1/3<=q<=1`, define

`L3(q)=H(a,a,1-2a)`, `a=(2+sqrt(6q-2))/6`, if `q<=1/2`;
`L3(q)=h2((1+sqrt(2q-1))/2)` if `q>=1/2`.

The sharp classical bounds are `H(p)<=U5(s)` (pad with zeros if needed)
and `S(M)>=L3(Tr M^2)`. These are the finite-alphabet upper arc and
lower cascade in Harremoes and Topsoe, *Inequalities between Entropy and
Index of Coincidence derived from Information Diagrams*, IEEE IT 47(7),
2944--2960 (2001), Theorem 2.5, equations (16)--(17), following Theorem
2.1. [Author-uploaded primary full text](https://www.researchgate.net/publication/3080552_Inequalities_between_entropy_and_index_of_coincidence_derived_from_information_diagrams),
[DOI](https://doi.org/10.1109/18.959272).
The input weights here are preparation weights; a SIC measurement-output
entropy theorem would concern a different probability distribution.

Therefore `Delta(rho_p)>=G(s)=2L3((1+3s)/4)-U5(s)`.
Both L3 and U5 decrease with their arguments, as follows directly by
differentiating their displayed parametrizations. On a rational interval
`[l,h]`, a valid uniform lower bound is

`G(s)>=2 L3((1+3h)/4)-U5(l)`.

The exact certificate covers `[1/5,63/64]` with 39 contiguous rational
intervals and verifies a rational lower bound at least `(1-l)/128` on
each interval `[l,h]`. Since `1-s<=1-l`, this proves the displayed
quantitative claim on the whole interior portion.
There are no omitted points or floating comparison premises. The smallest
recorded cell lower bound exceeds 0.001919 nats. Endpoint 63/64 is covered.

## Analytic tail, including arbitrarily small nonzero admixture

For `63/64<=s<1`, put `u=1-s`, `eta=1-z`, and `c=256/507`.
Then `u=2eta-5eta^2/4`; first `eta<=u`, then `eta<=cu` follow.
For the small output eigenvalue `nu`, `nu(1-nu)=3u/8`, so
`3u/8<=nu<=3u/4<1/3`. Monotonicity of `x log(1/x)` in this range gives
`2h2(nu)>=(3u/4)log(8/(3u))`.
The elementary bound `h2(eta)<=eta(log(1/eta)+1)` and monotonicity give
`U5(s)<=cu[log(4/(cu))+1]`. Hence
`G(s)/u >= (3/4-c)log(1/u)+(3/4)log(8/3)-c log(4/c)-c`.

Use `log(1/u)>=log64>=4`, `log(8/3)>=8/9`, and
`log(4/c)=log(507/64)<log8<=25/12`. These follow from
`2/3<=log2<=25/36` and `1<=log3<=10/9`, each obtained from the first
term and geometric remainder of the positive atanh series. We obtain
`G(s)>=[11/3-(85/12)(256/507)]u=(137/1521)(1-s)>=(1-s)/128`.
At s=1, p is a point mass and M is pure, so Delta is exactly zero.
Together with the contiguous interval certificate this proves the claim.

## Arithmetic trust boundary and replay

`certify_sic_sparse.py` uses only Python integers and Fraction. For each
nonnegative rational square root it brackets at denominator 2^60 by an
integer square root. Logs are range-reduced to `[1,2]`, and use
`log y=2 sum_(j>=0) z^(2j+1)/(2j+1)`, `z=(y-1)/(y+1)`.
The first 16 terms are a rational lower bound; the omitted tail is at most
`2z^33/[33(1-z^2)]`. Interval products account for every endpoint sign.
The special interval touching probability zero uses monotonicity of
`-x log x` on `[0,1/4]`. The square-root and log precisions were fixed
before the adaptive cover. Every final interval and its rational lower
bound are saved in `outputs/SIC_SPARSE_INTERVAL_CERTIFICATE.json`.

Replay with the existing solver-runtime Python, first
`replay_sic_exact.py`, then `certify_sic_sparse.py`.
The recorded runs took approximately 0.130 and 0.064 seconds, excluding
interpreter start. The cover examined 77 intervals, accepted 39, reached
depth eight, and used at most 7,866 numerator/denominator bits. These are
local acquisition costs, not an advantage over an equally informed route.
