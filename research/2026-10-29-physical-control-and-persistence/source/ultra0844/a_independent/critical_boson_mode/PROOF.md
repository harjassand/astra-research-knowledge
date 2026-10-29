# A native critical occupation that no normalizable fugacity makes cheap

29 October 2026. New all-occupation construction; root has independently whole-read and accepted the stated analytic scopes. No finite Fock-space fixture is used as a theorem. This attacks the critical-number interface left open by the normal-fluid and bounded-cut samplers. It is a scoped obstruction to grand-to-canonical filtering and fixed-slice critical-mode replacement, NOT a general sampling or fixed-density hardness result.

## 1. A fixed, stable, genuinely frustrated source

There are three sites and two bosonic flavors. In physical units choose

```
T = [ 3  1 -4
      1  3 -4
     -4 -4  8 ],
H = b†Tb+c†Tc+sum_(i=1)^3 (nb_i-nc_i)^2.
```

T has eigenvalues 0,2,12 and normalized zero vector `u=(1,1,1)/sqrt(3)`. For example it is `v1 v1^T+2 v2 v2^T`, v1=(1,-1,0), v2=(1,1,-2). The hopping triangle product is `1*(-4)*(-4)=16>0`, invariant under site phases. Three negative stoquastic hopping entries would have negative product. Thus this is a frustrated hopping input; all diagonal one-body terms are retained.

The Hamiltonian is positive, number conserving, and noncommuting. Define it by its finite particle-number blocks and their nonnegative direct sum. The potential is EXACTLY q_i^2, q_i=nb_i-nc_i. Expanding it into normal-ordered quartics includes its linear number term; that term is not discarded or hidden in the chemical potential. Couplings do not grow with occupation.

At fixed n_b,n_c, let N=n_b+n_c. Write b0,c0 for the u modes and define total depletion

`D=N-b0†b0-c0†c0 >=0`.

The spectral data give the operator inequalities

`2D <= H_hop <=12D`.                                  (1)

## 2. Coercivity from an exact relative-number uncertainty relation

Put f=diag(1,-1,0), `v=(1,-1,0)/sqrt(2)`, and `s=<v,fu>=sqrt(2/3)`. Define

`Q=(nb_1-nb_2)-(nc_1-nc_2)`,

`J_b=i(b0†bv-bv†b0)`, `J_c=i(c0†cv-cv†c0)`, `J=J_b-J_c`.

The local potential obeys `Q^2<=2sum_i q_i^2`. On the one-particle space, j=i(|u><v|-|v><u|) has norm one, and `C=i[f,j]` has norm at most two and `<u,Cu>=2s`. Hence

`i[Q,J]=dGamma_b(C)+dGamma_c(C)`.

For N>=1 and a normalized state with expected depletion d, its summed one-particle density gamma has trace N and `<u,gamma u>=N-d`. The N=0 vacuum obeys the final bound directly. Purification/fidelity (or direct block Cauchy--Schwarz) gives

`||gamma-N|u><u|||1<=2sqrt(Nd)`.

Therefore

`<i[Q,J]>=Tr gamma C >=2sN-4sqrt(Nd)`.

If `d<=N/24=s^2 N/16`, the right side is at least sN.

For either flavor, let A=b0†bv. The exact two-mode algebra gives

`J_b^2<=(2)(A†A+AA†)`

`=4 n0 nv+2(n0+nv)<=4 n_b nv+2 n_b`.

Consequently `J^2<=2(J_b^2+J_c^2)<=4N(2D+1)`. Robertson and the bounds above imply, in the small-depletion case,

`<sum_i q_i^2> >= N/[48(2d+1)]`.

Together with (1),

`<H>>=2d+N/[48(2d+1)]`.

Set x=2d+1 and use scalar AM--GM to obtain `<H>>=sqrt(N/12)-1`. In the complementary case d>N/24, (1) gives `<H>>=N/12`, which is an even stronger bound. Thus for EVERY particle sector,

`H_(n_b,n_c) >=[sqrt((n_b+n_c)/12)-1] I`.              (2)

No gap estimate or large-spin approximation has replaced this uncertainty argument.

## 3. The exact critical grand trace is finite

For all beta>0, the dimension of the entire N-particle sector of six modes is `binom(N+5,5)`. Equation (2) gives

`Tr exp(-beta H) <=exp(beta) sum_(N>=0) binom(N+5,5) exp[-beta sqrt(N/12)] <infinity`.       (3)

In particular the balanced grand trace at common fugacity r=1, chemical potential zero, is normalizable. It also has every finite particle-number moment. This is a stable interacting critical source, not an attractive unbounded Hamiltonian or a finite-occupation regularization.

For balanced count K,K, `D_K=binom(K+2,2)` and

`Z_K<=D_K^2 exp[beta-beta sqrt(K/6)]`.                 (4)

## 4. A constructive sublinear-energy number-squeezed trial

To determine the other side of the fugacity domain, a lower energy bound is insufficient. The following explicit normalized trial construction pays it.

Let `Omega_K=|u^K>_b |u^K>_c`, and choose `a=K^(1/3)>=1`. Put `X=sum_i q_i^2`,

`F=exp[-X/(2a^2)]`, `p=<Omega_K,F^2 Omega_K>`,

`psi_K=F Omega_K/sqrt(p)`.

Occupation measurements in Omega_K are two independent Multinomial(K;1/3,1/3,1/3) vectors. A vector lies in the box `|n_i-K/3|<=2sqrt(K)` with probability at least5/6, by the three exact variances 2K/9 and Chebyshev. Partition its first two coordinates into cells of integer side floor(a). At most `196K/a^2` cells intersect the box. Cauchy--Schwarz shows that two independent occupation vectors lie in the SAME such cell with probability at least `(5/6)^2 a^2/(196K)`. On that event, their first two differences have modulus at most a, the third at most2a, and X<=6a^2. Hence

`p>=c0 a^2/K`, `c0=25/[7056*4^6]>0`,                 (5)

using exp(-6)>4^-6. This is a paid normalization lower bound, not a supplied squeezed-state oracle.

The function F(q)=exp[-|q|^2/(2a^2)] has global Euclidean Lipschitz constant at most1/a. For example

`(b_i-b_j)F Omega_K`

`=sqrt(K/3)[F(q+e_i)-F(q+e_j)] Omega_(K-1,K)`.

Its squared norm is at most `2K/(3a^2)`. The identity

`D_b=(1/3)sum_(i<j)(b_i-b_j)†(b_i-b_j)`

and the analogous c identity give

`<psi_K,D psi_K> <=4K/(3a^2 p)`.

The tilted classical occupation distribution has relative entropy `-<X>_psi/a^2-ln p>=0`, so `<X>_psi<=a^2 ln(1/p)`. Combining this with (1) and (5) yields

`<psi_K,H psi_K>`

`<=K^(2/3)[16/c0+ln(1/c0)+(1/3)ln K] =:E_trial(K)=o(K)`.   (6)

The constants are deliberately poor. The important point is the actual all-K normalized trial and sublinear energy, not a useful numerical estimate at moderate K. It also has depleted fraction `O(K^(-1/3))`, while keeping the relative-number correlations absent from the unsqueezed product condensate.

For every r>1, Jensen and this trial give

`r^(2K) Z_K >=r^(2K) exp[-beta E_trial(K)] ->infinity`.

Thus NO common fugacity r>1 has a finite balanced grand trace. Together with (3), its normalizable positive range is exactly `0<r<=1`. Allowing unequal positive flavor fugacities does not help: their product on K,K is r_eff^(2K), and a product above one already diverges on the same balanced subsequence.

## 5. Even a PERFECT grand sampler cannot make the large critical count cheap

Grant an equally informed algorithm exact sampling of the physical balanced grand Gibbs state at ANY normalizable r, plus a free exact particle-number readout. Its probability of count K is

`p_K(r)=r^(2K)Z_K/[sum_n r^(2n)Z_n]`.

The vacuum denominator is at least one and r<=1. Therefore (4) implies the uniform bound

`sup_(normalizable r) p_K(r) <=D_K^2 exp[beta-beta sqrt(K/6)]`.    (7)

Every grand-to-canonical POSTSELECTION receiver at this temperature needs at least

`exp[beta sqrt(K/6)-beta]/D_K^2`

grand samples in expectation. This is stretched-exponential in condensate occupation, even if all mixing, determinant evaluation, free-mode conditioning and normalizer acquisition are granted. Chemical-potential tuning cannot remove it; moving above the endpoint makes the physical grand trace diverge.

The bound is uniform over K-dependent or adaptively chosen normalizable fugacities. Any positive mixture of those equilibrium grand proposals has the same count upper bound, by averaging. This does not cover non-Gibbs importance proposals or changes of temperature followed by paid reweighting.

Equation (7) is NOT a lower bound on arbitrary canonical samplers, importance estimators, Bogoliubov methods, tensor methods, or the original globally fixed-density problem. There are only three sites here; K grows. This is the actual high-occupation obligation of an interacting critical-mode interface, not a thermodynamic many-site hardness theorem.

## 6. A fixed imaginary-time mesh has the WRONG critical tail

Now keep an arbitrary positive integer L FIXED and let delta=beta/L. On the finite K,K sector define the symmetric transfer

`C_K=exp(-delta V/2) exp(-delta H_hop) exp(-delta V/2)`.

Its power trace is the same finite-slice canonical object used by the accepted HS receiver. Since the one-body hopping has a zero mode u,

`exp(-delta T)>=|u><u|`.

They commute in their common eigenbasis, so the K-fold symmetric power is at least the rank-one projector onto |u^K>. For a paired occupation vector alpha=(n,n), V_alpha=0 and

`(C_K)_alpha,alpha >=p_K(n)^2`,

where `p_K(n)=K!/(3^K product_i n_i!)` is the multinomial probability. Scalar spectral Jensen gives

`Z_(L,K)=Tr C_K^L >=sum_n p_K(n)^(2L)`.

The same Chebyshev box has probability at least5/6 and contains at most25K possible first-two-coordinate pairs for K>=1. Power-mean/Hölder therefore yields

`Z_(L,K)>=(5/6)^(2L)/(25K)^(2L-1)`.                  (8)

In particular `Z_(1,K)>=1/(36K)`. The finite-L1 balanced grand trace at r=1 diverges harmonically, although the EXACT physical trace (3) is finite. The positive balanced field envelope also has this divergence: its definition is the nonnegative sum `sum_K |h_K(B)|^2`, so Tonelli applies without a signed interchange. No post-continuum finite-part statement is being used.

More generally (4) and (8) give

`ln Z_(L,K)-ln Z_K`

`>=beta sqrt(K/6)-beta-2ln D_K+2L ln(5/6)-(2L-1)ln(25K)`.   (9)

At every fixed L this tends to positive infinity at order sqrt(K), up to logarithms. For a declared absolute log-partition error epsilon, a necessary condition is

`L >=max(0,[beta sqrt(K/6)-beta-2ln D_K-epsilon+ln(25K)]/[2ln(30K)])`.   (10)

Thus an occupation-uniform critical prediction cannot inherit a fixed slice count; at least an Omega(sqrt(K)/ln K) growth is forced by this native source. This is not a sufficient mesh theorem or a runtime lower bound for continuous-time algorithms. The accepted polynomial sufficient finite-sector mesh remains valid, and exact many-body exponentiation can bypass slicing in a fixed-mode model.

The source counter is distinct from the earlier post-continuum Casimir finite-part counter. Here the Hamiltonian is the SAME density-difference native class, exact critical Gibbs is stable, and the issue is a finite-slice/critical-occupation limit. It does not contradict a strict negative-chemical-potential contraction theorem: that theorem's r<1 hypothesis excludes precisely this endpoint.

## 7. What exact free-mode separation does and does not acquire

Grant the exact one-particle zero mode, its complete Gaussian thermal conditioning, and every ordinary fixed-rank determinant identity. They do not change (7) or (9).

Projection of the two-flavor K,K state to the product zero mode alone gives Omega_K. Its hopping energy is zero, but its potential expectation is exactly `4K/3`. In contrast, (6) is sublinear in K with a vanishing depleted fraction. Thus a small depleted fraction by itself does not pay a relative Gibbs-weight approximation: the missing relative-number squeezing changes the leading energy. Number-conserving Bogoliubov and nonlinear squeezed-state corrections are strong established comparators and must be allowed to retain those correlations.

Indeed the condensate-only projected Hamiltonian would give `Z_projected,K=exp(-4beta K/3)`, falsely permitting common fugacities up to exp(2beta/3)>1. It is not the interacting critical number law even though its one-particle zero mode is exact.

For THIS fixed three-mode input, the fully informed ordinary canonical route is already polynomial: each flavor has D_K=Theta(K^2) states, the joint matrix has Theta(K^4) dimension, and direct sparse/dense canonical diagonalization or exponentiation avoids grand postselection. No claim that this example defeats that method is made. It supplies a decisive failure of the grand-count and fixed-mesh INTERFACES, not a new practical superiority result.

The higher-leverage missing operation is direct acquisition of an interacting critical sector coupled to an extensive bath or an extensive critical-mode manifold, retaining its number/coherence correlations with a paid cost. An arbitrary many-body critical weight, spectral gap, mixing time, or small effective rank is not supplied by this proof. Generic hardness and generic tractability both remain unproved.

## 8. Prior and evidence boundary

The ordinary ingredients are Schwinger boson mode algebra, Robertson, a Gaussian number-squeezed trial, entropy of a classical tilt, multinomial concentration, scalar spectral Jensen, and canonical sector diagonalization. Number-conserving condensate/depletion treatments are established, for example Gardiner quant-ph/9703005, Castin--Dum PRA57 3008, and Gardiner--Morgan cond-mat/0610623. No claim of inventing those methods or of ruling them out is made.

Rigorous Trotter theory distinguishes strong convergence from trace/occupation-uniform error. Tim Möbus, ["On Strong Bounds for Trotter and Zeno Product Formulas with Bosonic Applications," Quantum 8, 1424 (2024)](https://doi.org/10.22331/q-2024-07-25-1424), is a relevant ordinary alternative; an applicable error route must be acquired, not dismissed because a fixed L fails. The publisher author/title metadata and abstract were read, not an applicable occupation-uniform theorem imported. Historical priority of the explicit native construction is UNKNOWN.

The proof is all-K and analytic. The companion exact-data consumer checks only its fixed one-particle algebra, rational constants and displayed bound evaluations. Such a replay is not the proof, a physical experiment, an independent scientific review, or a many-body fixture establishing the asymptotics.
