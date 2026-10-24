# Positive-edge whitening filter: exact normalization audit

This checks the proposed no-phase edge-state operation only. The graph is
`Gamma_st~Bernoulli(q)` on `N=kM` strings per side, `E=|Gamma|>0` is the
realized edge count, and

`|Omega> = E^(-1/2) sum_(s,t) Gamma_st |s>_A |t>_B`.

For `s=s(x,i)`, `t=t(y,j)`, define `v_(x,i)^y[j]=Gamma_(s,t)` and
`F_i^x=(k M q)^(-1) sum_y |v_(x,i)^y><v_(x,i)^y|`, `F_x=sum_i F_i^x`.
Measuring Alice's old `(x,i)` and tracing Bob's old `y` gives the exact
unnormalized residual state

`rho_(x,i)=(1/E)sum_y |v_(x,i)^y><v_(x,i)^y| = alpha F_i^x`,

where `alpha=k M q/E = 1/sum_x Tr(F_x)`. Thus
`Pr(oldX=x)=alpha Tr(F_x)` and the conditional fine assemblage is exactly
`F_i^x/Tr(F_x)`. The random edge count must remain in `alpha`; replacing
`E` by `N^2 q` is not exact. The normalization identity
`sum_x Tr(F_x)=E/(k M q)` holds for each realized graph.

## The deterministic filter

For fixed `x`, independent Bernoulli edges yield

`E_Gamma F_x=(1-q)I+qJ=:F_0`,

because a diagonal entry is a sum of `kM` Bernoulli variables with mean
`kMq`, while an off-diagonal entry is a sum of `kM` products of distinct
edges with mean `kMq^2`. `F_0` has eigenvalue `1-q` on the orthogonal
complement of the all-ones vector and eigenvalue `1-q+qM` on that vector.
Let `C_0=F_0^(-1/2)` and `K=sqrt(1-q) C_0`. Its eigenvalues are `1` on the
orthogonal complement and
`sqrt((1-q)/(1-q+qM))` on the uniform vector, so `0<=K<=I` for `q<1`.
It is a genuine Bob-local success filter, completed by failure effect
`I-K^2`; it depends only on `q,M`, not on the realized graph.

After tracing old `y`, apply `K` to the residual `j` system. Put
`A_i^x=C_0 F_i^x C_0` and `A_x=sum_i A_i^x=C_0 F_x C_0`. The exact
post-filter substate for old `(x,i)` is

`rho_(x,i)^succ = alpha(1-q) A_i^x`.

Hence the old-x-conditional success probability and success-conditioned
fine assemblage are, respectively,

`p_succ|x=(1-q)Tr(A_x)/Tr(F_x)`,
`sigma_i^(x,succ)=A_i^x/Tr(A_x)`.

The first ratio is near `1-q` when `A_x` is near `I`; it is not exactly
`1-q` at finite error. More globally, if `||A_x-I||<=eps<1` for every x,
then `F_x=C_0^(-1)A_x C_0^(-1)` and `Tr(F_0)=M` imply
`Tr(F_x)/M, Tr(A_x)/M in [1-eps,1+eps]`. Consequently

`p_succ=alpha(1-q)sum_x Tr(A_x)`
`          =(1-q) (sum_x Tr(A_x))/(sum_x Tr(F_x))`,

so
`(1-q)(1-eps)/(1+eps) <= p_succ <= (1-q)(1+eps)/(1-eps)`.
In particular it is `(1-q)(1+O(eps))` and the success-conditioned old-x
law is `Tr(A_x)/sum_z Tr(A_z)`, within total variation
`eps/(1-eps)` of uniform.

## Fresh maximally entangled reference and retained records

On `|Phi_M>=M^(-1/2)sum_j|j,j>`, Alice can use one all-input POVM family

`E_i^x=(A_x^(-1/2) A_i^x A_x^(-1/2))^T`.

The transpose is in the Schmidt `j` basis. These effects sum to `I` when
`A_x` is invertible, and Bob's conditional substate is
`A_x^(-1/2)A_i^x A_x^(-1/2)/M`. It approximates
`A_i^x/Tr(A_x)`: for `eps<=1/2`, the block trace-distance bound is at most
`3.1 eps` by the same positive-operator estimate as for `F_x` in the
companion note. Any same Bob POVM on the retained `j`-system contracts this
error. Relative to uniform fresh `x`, the normalized accepted fine table is
therefore within `3.1 eps+eps/(1-eps)<=5.1 eps` in total variation.

The original edge source retains Alice's fine `i`; the Bob side has first
discarded old `y`, then applies the success/failure filter on `j`. On
success the residual `j` register is retained for Bob's later readout. The
fresh-reference implementation can match that averaged-over-old-`y` table
approximately, including any fixed graph-aware Bob POVM on `j`. It does not
retain or reproduce a record resolved by old `y`, and it does not prove that
a fresh input `y` can select the corresponding old-y component. A Bob
measurement that has access to the discarded old-y environment is outside
this comparison.

The reference requires `log_2 M` ebits. The source state itself is a
graph-supported coherent state in local dimension `N=kM`; preparing it
requires graph-aware coherent access or a separately supplied state. The
filter is simple, but the `A_i^x`-dependent Alice POVMs still require the
realized graph. This calculation alone supplies neither an efficient
implementation nor the desired uniform payoff bound against all
Gamma-aware Bob POVMs.
