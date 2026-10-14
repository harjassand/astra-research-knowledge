# Proof notes and exact countermodels

## 1. Exact identity behind the shared-tree acquisition

For a cycle `E`, write the positive rational source weights as

`W(S) = r^|S| t^(n-b(S))`,

where `b(S)` is the number of cycle edges crossing from `S` to `V\\S`, `t>1`, and `r>0` is a uniform field factor. For `i notin S`, let `m_i(S)` be the number of cycle neighbors of `i` in `S`. Adding `i` changes the boundary by

`b(S+i)-b(S) = (2-m_i(S))-m_i(S) = 2-2m_i(S)`.

Therefore

`R_i(S) = W(S+i) W(empty) / [W(S) W(i)] = t^(2m_i(S)) = q^m_i(S)`, `q=t^2`.

For the root calibration, `S=V\\{0}` contains both neighbors of site 0, so `R_0(S)=q^2=t^4`; hence `q=sqrt(R_0(S))`. The cache seed is `{empty,V,{i}: i∈V,V\\{0}}`, containing `n+3` unique weights for `n>2`.

At a tree node `T` with known count `k=m_i(T)`, select a child `A` not containing `i`. If `i` is in one half this is the other half; if `i` is outside `T`, choose the left half. Query `R_i(A)` and classify its exponent `a∈{0,1,2}`. The other child's count is exactly `k-a`. Recurse only into positive-count children. At each positive leaf, the coordinate is one of the two neighbors. The exact replay independently evaluated `W` from the planted cycle formula and confirmed recovery for 101 deterministic n=24 labelings.

### Deterministic unique-energy bound for n=24

Let `h=ceil(log2 n)=5`. A full binary split tree with `n` leaves has `2n-1=47` node masks; this covers every `W(A)` query, all singleton seeds, and `W(V)`. Each vertex's two neighbors lie on at most two root-to-leaf paths, so there are at most `2h` queried positive internal nodes per vertex and at most `2nh=240` fresh `W(A+i)` masks. The bootstrap adds only `W(empty)` and `W(V\\{0})` outside the tree. Thus there are at most `47+240+2=289` unique energy masks, strictly below the 301 pairwise scheme. This counts cache reuse globally and treats every `A+i` as fresh, so overlap can only lower the count.

The simulation counts actual unique masks, not arithmetic operations or bits. It does not include state preparation, repeated noisy measurements for precision, uncertainty calibration, or costs of obtaining the energy oracle. Finite observations still cannot establish the global pairwise promise.

### Deterministic finite-error bound

Let every queried dimensionless energy have deterministic absolute error at most `delta`. The contrast `D=E(S)+E(i)-E(S+i)-E(empty)` has error at most `4 delta`. The root computes `log q=D/2`, so its error is at most `2 delta`. For a true child count `k≤2`, let `a=log q=2 log t`. Then

`|Dhat/ahat-k| ≤ (4 delta+2k delta)/(a-2 delta) ≤ 8 delta/(2 log t-2 delta)`.

Nearest-integer classification is correct if this is `<1/2`; it suffices that `delta < log(t_min)/9`. The proposed stricter `delta < log(t_min)/10` gives a worst-case bound `4/9`. This assumes `t≥t_min>1`; it is deterministic interval robustness, not a stochastic measurement confidence result.

## 2. Acquisition-only extension to nonuniform positive pairwise graphs

For `W(x)=r^|x| ∏_{(u,v)∈E} t_uv^[x_u=x_v]` with every `t_uv>1`, the same calculation gives

`log R_i(S) = Σ_{j∈N(i)∩S} 2 log t_ij`.

All terms are positive. Starting from `R_i(V\\{i})`, a split query on one child returns its positive edge-weight sum; subtracting from the known parent sum gives the other child. A child has a neighbor exactly when its sum is nonzero, so positive branches can be recursively split. The leaf mass is the individual edge coefficient. This recovers support and weights for arbitrary simple graphs under a globally pairwise, sign-definite ferromagnetic premise.

For a balanced tree of maximum depth `h`, there are at most `2mh` positive internal nodes summed over vertices, because each incident edge contributes one leaf path at each endpoint. Root-mass acquisition takes `n` additional `V\\{i}` masks. A conservative unique-weight bound is `3n+2mh` (tree node masks, root masks, and at most one fresh `A+i` per contrast). This is an acquisition lemma only: mixed-sign interactions can cancel in a sum, and the FH source's explicit slow/complement spectral bound remains specific to the homogeneous ring. No broader lifetime certificate is claimed.

## 3. Collective slow space, full complement bound, and source residual

For the zero-field ferromagnetic ring and specified heat-bath law, set

`eta=(t²-1)/(t²+1)`,
`q_i(sigma)=nu/2 [1-eta sigma_i(sigma_{i-1}+sigma_{i+1})/2]`,
`L=-Q`, and `m(sigma)=n^{-1} sum_i sigma_i`.

Direct local algebra gives `L 1=0` and `L m=lambda m`, with `lambda=nu(1-eta)`. For the spin monomial `chi_S=prod_{i∈S} sigma_i`,

`L chi_S = nu |S| chi_S - (nu eta/2) sum_{i∈S} sum_{j=i±1} chi_{(S\\{i}) symmetric_difference {j}}`.

The monomial filtration is triangular: terms either preserve degree or reduce it by two when a neighboring coordinate is already in `S`. On the degree-p quotient, the preserved-degree block is `p nu(1-eta)` plus the Dirichlet operator of p nearest-neighbor walkers, each jumping at rate `nu eta/2`, killed when walkers collide. For `p≥2`, retain the Dirichlet energy of any two walkers and discard the other nonnegative terms. Their separation walk is killed at the endpoints of `{1,...,n-1}` and has lowest energy `2 nu eta [1-cos(pi/n)]`. Therefore every p≥2 block has lower spectral edge at least

`p nu(1-eta)+2 nu eta [1-cos(pi/n)]`
`≥ 2 nu(1-eta)+4 nu eta/n²`,

using `1-cos(pi/n)≥2/n²`. The degree-one Fourier modes have eigenvalues `nu[1-eta cos(2 pi j/n)]`. The uniform mode is `m`; every nonuniform degree-one mode is at least `nu[(1-eta)+8eta/n²]`. Thus with

`gamma=nu[(1-eta)+4eta/n²]`,

the full operator obeys

`L ≥ lambda P_m + gamma(I-P_1-P_m)`.

Here `P_m` is the orthogonal projection in the Gibbs `L²(pi)` space onto the span of `m`, while `P_1` is the constant projection. Reversibility makes the orthogonal complement invariant. This is a full-complement theorem for the declared homogeneous zero-field ring, not a fitted-mode estimate. The source derives the all-n inequality; this audit independently checked exact small matrices at n=4 and n=5 but did not externally verify the all-n proof.

For `K=L+kappa 1_{x_0=1}`, define

`C=lambda P_m + gamma(I-P_1-P_m) + kappa 1_{x_0=1}`.

Then `0<C≤K`, hence `K^{-1}≤C^{-1}`. For any trial vector `v`, let `r=1-Kv`. The exact symmetric-operator identity is

`tau_eq=<1,K^{-1}1>=2<1,v>-<v,Kv>+<r,K^{-1}r>`.

It yields the rigorous interval

`2<1,v>-<v,Kv> ≤ tau_eq ≤ 2<1,v>-<v,Kv>+<r,C^{-1}r>`.

The useful computation is a rank-two Woodbury inverse, not a new residual principle. With `B=[1,m]`, `G=diag(1,s)`, `s=<m²>`, `D=gamma+kappa 1_{x_0=1}`, and `J=diag(-gamma,(lambda-gamma)/s)`, one has `C=D+BJB*`; the inverse needs only `H=B*D^{-1}B`, a 2×2 matrix. Since `D^{-1}=a+b sigma_0`, where `a=(1/gamma+1/(gamma+kappa))/2` and `b=(1/(gamma+kappa)-1/gamma)/2`, all contractions are exact rational combinations of the acquired Gibbs moments when model parameters are rational.

The trial support is the zero- or two-domain-wall set, with `2+n(n-1)` states. Because `K` is single-spin local, `Kv` vanishes outside the support and its one-flip neighborhood, so the exact residual is `r=1` on every remaining configuration. The full-source contractions retain that omitted source through exact Gibbs expectations; the omitted residual is not set to zero. At n=24, the trial has 554 states and the residual neighborhood has 10,178 states, versus `2^24` total states.

## 4. Exact finite generator checks

The independent checker constructs the complete finite generator and Gibbs weights, forms `K=L+k`, and verifies `C=L_minorant+k` by exact rational matrix arithmetic. It independently computes the full exact lifetime and `C^{-1}` residual form. Results are saved in `replay/independent_checks.json`:

- `n=4,t=2`: `gamma=11/20`, `lambda=2/5`, exact lifetime `7297276071/2062098280`; the exact minorant is PSD and the full lifetime lies inside `[284/205, 151685628/34310645]`.
- `n=5,t=10`: `gamma=446/2525`, `lambda=2/101`, exact lifetime is the stored 49-digit fraction; the exact minorant is PSD and the full lifetime lies inside the stored exact lower/upper interval.

For both, the residual equals exactly one outside the one-flip neighborhood, and the independently assembled full-matrix `C^{-1}` contraction agrees with the source's compact formula. These finite checks are implementation checks, not a proof of the all-n spectral theorem.

## 5. Exact failure of finite-probe class inference

For `n=6,t=2`, alter only the weight of mask `14` (coordinates 1,2,3 excited) by a factor 1000. The source's 22 empty/singleton/pair probes are unchanged, so its learner returns the same `t=2`, `r=1`, and six cycle edges. The independently executed richer shared-tree transcript also leaves mask 14 unqueried: all 28 unique masks and every adaptive contrast remain identical, and it returns the same cycle and coupling. The hidden model is still reversible after deriving the corresponding rates from the modified energy, but it is no longer the homogeneous pairwise Ising law. The exact killed means differ by a factor `121.542793...`; the hidden mean exceeds the baseline certificate upper endpoint by `64.982747...` times. Exact fractions and both query-equality checks are in `replay/independent_checks.json`.

This counterexample directly blocks any statement that those probes certify absence of higher-order interactions.

## 6. Exact failure of energy-to-clock inference

Keep the baseline `n=6,t=2` energy and equilibrium law. Change only the target coordinate's heat-bath attempt prefactor from `nu_0=1` to `nu_0=1/1000`, leaving other coordinates at `1`. This preserves detailed balance and every energy query. The equilibrium probability of target-closed states is exactly `1/2`; from any such state, the target opening hazard is at most `1/1000`, so expected first-opening time is at least `1000`. Consequently the equilibrium mean is at least `500`, versus the uniform-clock certificate upper endpoint of approximately `6.486`. The proof and exact setup are in the checker output.

Thus the heat-bath attempt law and uniform mobility are real supplied premises; energy observations do not acquire them.

## 7. Preparation conversion and coupled uncertainty

For binary killing `k=kappa 1_A`, the source's equilibrium conditioning identity is

`tau_{pi|A}=1/[kappa pi(A)]`,
`tau_{pi|A^c}=[tau_eq-1/kappa]/[1-pi(A)]`.

Here `A={x_0=1}` and zero-field spin reversal gives `pi(A)=1/2`, so the open-conditioned mean is exactly `2/kappa`; the closed-conditioned interval follows by the displayed affine transform of the equilibrium interval. At `n=24,t=1000,nu=kappa=1`, it is `[289754.54605,313699.31479]` up to the source's displayed rounding. It is not the same preparation as the point mass on the all-closed configuration.

For that point preparation, define the normalized load `b2=1_{all-closed}/pi(all-closed)`. The preparation code proposes two rational witnesses for loads `1` and `b2`, constructs their full residual cross-form matrix `Gamma`, and verifies `Gamma` PSD exactly. The bilinear residual term obeys

`E12 ∈ [(Gamma12-sqrt(Gamma11 Gamma22))/2, (Gamma12+sqrt(Gamma11 Gamma22))/2]`,

with an outward rational square-root enclosure. The fresh n=24,t=1000 point-prepared interval is `[289799.3453074289,313745.3363051288]`, ratio `1.082629555192049`; its equilibrium endpoints reproduce the separate equilibrium certificate to displayed precision. This is a source-aware two-load certificate for one exact preparation, not a theorem for arbitrary experimental ensembles.

For coupled energy/mobility/reaction uncertainty, the source assumes a common mass perturbation `m0≤m≤R m0` after removing irrelevant scalar normalization and clock multipliers in `[a,b]`. Under its heat-bath conductance form it derives

`tau0/(b R^2) ≤ tau ≤ R^2 tau0/a`.

For the uniform family, assumed dimensionless energy errors `|δ log t|≤eJ` and `|δ field|≤eh` imply `log R≤n(eJ+eh)`. If every energy reading has deterministic error at most `delta`, the analytic bounds are `eJ≤2delta` and `eh≤6delta`, conditional on correct edge/nonedge separation and the model class. The source's prototype uses exact rational weights; a general noisy graph-fit implementation is not present.

With `delta=10^-5` and independent `nu,kappa` relative uncertainty `0.002`, the n=24,t=1000 equilibrium interval widens to `[144034.9373754090,157769.6611491243]`. At t=1200, the corresponding interval is `[207439.1314356965,221924.2263705704]`, while the exact-input interval is `[208653.7035252942,220631.5241090090]`; these assumed uncertainties still imply `B/A>1.31482` for the two equilibrium-conditioned models. This is a distinguishable model decision under declared uncertainty, not evidence that those uncertainty ranges are physically calibrated.
