# Independent receipt: positive finite-patch source corrector

2026-11-01. **PASS as a conditional mathematical compiler; microscopic service and the complete memory join remain separate premises.** No practical, novelty, or hardware-realization conclusion.

Audited root: `ROOT_FINITE_PATCH_SOURCE_CORRECTOR.md`, SHA256 `06edec14885e1c284786fe01192d36dd9c1060fa455b7676db1629f54702e1c8`.
Read stage-completion note SHA256 `aeba76b86eed67f55a49622a000bdf483c3286279ae762dcaf423f23a88c5528`; its stage bound is not substituted for final cache service.

## 1. Precise locality contract

Write G for the **time-independent Heisenberg** source generator on a finite tensor-product graph, G=sum_i ell_i. Every ell_i is itself a Hamiltonian or GKSL generator with support X_i, and has induced operator norm, including spectator identities, at most lambda. A sufficient bound is 2||h_i||+2 sum_j||L_ij||^2. Every site has dimension at most d, each support has at most s sites, and the interaction-overlap graph (i adjacent j iff their supports intersect, including self) has degree at most Z>=1. The number of terms incident at a site is bounded by iota. These constants are uniform in the global size. Bounded-degree finite-range geometry with bounded local term multiplicity supplies this contract; graph degree alone without bounded multiplicity/strength does not.

Let 0<=e<=I have support Y, and let m be the number of terms touching Y. For integer R>=1, take P_R to contain Y and all supports X_i at overlap-graph distance <R from the m seed terms touching Y. Define G_R by retaining exactly those whole original terms whose support lies inside P_R. No artificial boundary reset is added. In particular, G_R generates a unital CP contraction, regardless of whether it has any service property.

Assume actual GLOBAL service exp(TG)e<=epsilon I for fixed finite T. A sector-restricted version is stated below.

## 2. Primary source and independent path specialization

Primary locality source: Barthel and Kliesch, *Quasi-locality and efficient simulation of Markovian quantum dynamics*, [arXiv:1111.4210v2](https://arxiv.org/abs/1111.4210), Theorem 1 and Section V, equations (21)–(25). Its local-generator recursion is the input used here. Its Theorem 2 additionally assumes polynomial shell growth and is **not** invoked for an expander. The following summed-path specialization instead counts branching directly.

Set E_R(t)=exp(tG_R)e. For any generator K_X supported on X, split G_R into terms disjoint from X and terms touching X. K_X commutes with the disjoint generator, whose propagator is contractive. Variation of constants therefore gives

 ||K_X E_R(t)|| <= ||K_X e||
   + ||K_X|| sum_{j retained: X_j intersects X} integral_0^t ||ell_j E_R(u)|| du.

Normalize by ||K_X|| and iterate. The terminal value vanishes unless the last support meets Y. Each n-fold time integral contributes t^n/n!. This is an ordinary finite-volume iteration; its remainder vanishes by the exponential-series bound, so no infinite-volume exchange is needed.

Now sum over omitted terms i. Terms disjoint from the patch annihilate E_R(t), so the actual sum is finite and supported near its boundary. For an omitted term to connect through n retained terms to Y, n>=R: otherwise its support would have been included in the chosen patch. Reverse each such path. Its terminal term has at most m choices and its n subsequent steps each at most Z choices. Including the initial omitted generator norm, the product of n+1 norms is at most lambda^(n+1). Thus

 B_R(t):=||(G-G_R)E_R(t)||
 <= lambda m sum_{n>=R} (lambda Z t)^n/n!
 <= lambda m exp(lambda Z exp(mu)t-mu R),   mu>0.                 (1)

The last inequality follows by multiplying each summand by exp(mu(n-R))>=1 and summing the full exponential series. Branch growth is already included in Z; no separate polynomial-growth hypothesis or unjustified expander corollary is used. If m=0, all dynamics leaves e fixed and the residual is identically zero.

## 3. Both required errors and the corrector

Define H_R=integral_0^T E_R(t)dt. Positivity/unitality give 0<=H_R<=T I. Its support is contained in P_R. Exactly,

 G H_R=-e+E_R(T)+(G-G_R)H_R.                                  (2)

Duhamel and contraction of the GLOBAL CP propagator give

 ||exp(TG)e-E_R(T)||
 <= integral_0^T ||(G-G_R)E_R(t)||dt.

Separately, linearity and the triangle inequality give

 ||(G-G_R)H_R|| <= integral_0^T ||(G-G_R)E_R(t)||dt.

Combining these bounds with actual global service proves

 G H_R <= -e+(epsilon+delta_R)I,
 delta_R = 2 lambda m exp(-mu R)
                [exp(v_mu T)-1]/v_mu,
 v_mu=lambda Z exp(mu).                                       (3)

The continuous zero-rate interpretation applies. A simpler safe choice is
 delta_R<=2 lambda m T exp(v_mu T-mu R).

For desired locality error delta>0, it suffices to choose an integer R>=1 with
 mu R >= v_mu T + log(2 lambda m T/delta).
Choose mu=1 if desired. T and R may be extremely large but are independent of total memory size. No statement that a truncated patch refreshes its cache is used. Equation (3) is a fixed generator inequality; there is no storage-duration approximation error delta*T_storage appended to it. The error delta is instead a persistent Foster floor that must fit the later barrier budget.

## 4. Sector and protected-label restrictions

If service is known only as S exp(TG)e S<=epsilon S for an admitted projector S, the conclusion is ONLY

 S G H_R S <= -S e S+(epsilon+delta_R)S.

The norm estimates above remain full-space estimates. They do not promote sector service to all states. If the eventual consumer requires full-space drift, that stronger service must be proved.

For protected labels, require each retained local semigroup to map their joint commutant into itself, and e to belong to that commutant. A sufficient condition is that every individual Hamiltonian and jump commutes with every relevant label. Then E_R(t), H_R commute with all labels, hence with any component projector that is a function of those labels. Scalar conservation of W alone is insufficient. Individual-term preservation matters: cancellation in the complete generator need not survive truncation. Cache-block diagonality required by Boolean consumers is a separate invariant-algebra check, not implied by positivity or locality.

The fixed identity (2) is for autonomous G. Arbitrary time-dependent source terms do not automatically yield a single time-independent H_R satisfying it. A time-dependent corrector would require its additional time derivative and separate admission.

## 5. Explicit finite computation and its real cost

A coarse patch bound is

 N_R:=|P_R| <= |Y|+s m sum_{j=0}^{R-1} Z^j,
 D_R:=dim H_(P_R) <= d^(N_R).

There are at most iota N_R retained terms. A full dense Heisenberg supermatrix has D_R^4 entries; dense observable storage already has D_R^2 entries. This is finite and size-independent, not practical and not polynomial in T or target precision under the above radius estimate.

With supplied computable local coefficients and certified precision access, H_R can be approximated without a spectral gap or inversion. Let K be a certified upper bound on ||G_R||, e.g. lambda iota N_R. The polynomial

 H_N=sum_{j=0}^N T^(j+1) G_R^j(e)/(j+1)!

has operator-norm remainder at most

 T exp(KT) (KT)^(N+1)/(N+2)!.

Choose N and arithmetic precision to make total Hermitian approximation error <=q. Then H_hat+q I is positive and <=(T+2q)I. Since G(I)=0, its drift differs from G H_R by at most lambda M_near q, where M_near<=iota N_R counts all full-generator terms meeting the patch. This finite additional floor must be charged. Iterative matrix application gives an elementary finite algorithm; even storing the full supermatrix and using dense matrix arithmetic is a conservative implementation. Arbitrary unencoded real coefficients do not supply a finite algorithm or bit-cost theorem. Symmetry-respecting arithmetic is needed if the implemented certificate must retain exact label commutation; the exact mathematical H_R already does.

## 6. Scope and pending gates

Accepted: conditional positive finite-patch compiler on general bounded-overlap finite-dimensional graphs, including exponentially growing graphs, with both evolution and boundary-generator errors explicitly bounded.

Not accepted from this lemma alone: uniform small final mismatch after arbitrary coherent initialization; small duty/activity service; protected-label preservation of the actual apparatus; cache/Boolean commutation; a positive total memory barrier margin after pricing all correctors and noisy actuators; collective-decay hardware realization. Stage-completion observability alone is not final-cache service. No physical experiment or full receiver was executed for this receipt.
