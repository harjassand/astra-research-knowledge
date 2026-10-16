# A self-contained substitute for the required domination import

This is a direct reconstruction of the independent-thinning mechanism used in Temmel, arXiv:1105.1683v3, Proposition 18 (pp. 14-16). The conservative bound below is derived here; it does not invoke Temmel Theorem 28, LSS Theorem 1.3, Shearer's measure, or an uninspected lemma. The only probability machinery beyond the displayed induction is conditional expectation and sequential sampling on a countable binary product space.

## Statement

Let G=(V,E) be countable with maximum degree at most D<infinity. Write N[v] for the closed neighborhood. Suppose H_v are binary and

P(H_v=0 | sigma(H_w : w outside N[v])) <= delta almost surely.

For 0<epsilon<=1/2, if delta<=epsilon^(D+1), then H stochastically dominates an iid Bernoulli((1-epsilon)^2) field. Consequently B=1-H is stochastically dominated by iid Bernoulli(2epsilon-epsilon^2), and therefore by iid Bernoulli(p_*) when epsilon=p_*/2, 0<p_*<1.

This bound is uniform over all graphs of the given degree bound and all fields satisfying the conditional premise. No translation invariance, finite volume, or independence between neighboring H bits is required.

## Proof

Put r=alpha=1-epsilon. Let X_v be iid Bernoulli(r), independent of the entire H field, and set Z_v=H_v X_v. We prove by induction on |W| that, for every v outside finite W and every positive-probability event Z_W=s,

P(H_v=1 | Z_W=s) >= alpha.                         (1)

For W empty, the weak premise gives P(H_v=0)<=delta<=epsilon.

For the step, partition W into M=W outside N(v), N0={w in W intersect N(v):s_w=0}, and N1={w in W intersect N(v):s_w=1}. Let l=|N0|, m=|N1|; l+m<=D.

The weak premise also gives P(H_v=0 | Z_M=s_M)<=delta: conditional on H_M, the additional independent X_M randomness cannot increase this conditional expectation. This holds even though H_v need not be independent of H_M.

If l+m=0 this already proves (1). Otherwise cancel the independent probability r^m of X_N1=1 in the numerator and denominator for the conditional probability P(H_v=0 | Z_W=s). Dropping H_N1=1 and Z_N0=0 from the numerator, and retaining only the sufficient event X_N0=0 in the denominator, gives

P(H_v=0 | Z_W=s)
 <= P(H_v=0, Z_M=s_M)
    / [(1-r)^l P(H_N1=1, Z_M=s_M)]
 <= delta / [(1-r)^l P(H_N1=1 | Z_M=s_M)].         (2)

Factor the last probability in an arbitrary order w1,...,wm. Each factor is

P(H_wj=1 | H_w1=...=H_w(j-1)=1, Z_M=s_M).

It equals the corresponding probability conditioned on Z_w1=...=Z_w(j-1)=1 instead: those extra X bits are independent of H and X_M, and conditioning them to one adds no information. The conditioning set M union {w1,...,w(j-1)} has strictly fewer than |W| vertices. The inductive hypothesis thus bounds every factor below by alpha. These positive lower bounds also ensure that every sequential conditional event needed here has positive probability. Therefore

P(H_v=0 | Z_W=s)
 <= delta / [(1-r)^l alpha^m]
 <= delta / epsilon^D
 <= epsilon,

because alpha>=epsilon, l+m<=D and 0<epsilon<=1. This establishes (1).

X_v is independent of H and Z_W for v outside W. Hence

P(Z_v=1 | Z_W=s) = r P(H_v=1 | Z_W=s) >= r alpha.

Enumerate V and sample each Z coordinate using its conditional probability given earlier sampled coordinates and an independent uniform variable U_v. The bits Y_v=1{U_v<=r alpha} are iid Bernoulli(r alpha), and Y_v<=Z_v at every coordinate. Since Z<=H in the thinning construction, H stochastically dominates Y. If an explicit joint coupling is wanted, sample H conditional on Z from that thinning law; countable binary product spaces admit this conditional law. Complementing bits proves the claimed bad-field upper domination. For a larger desired bad density, add independent marks.

## Application to the pinned memory flags

Take q=R+3 and D=(4q+1)^4-1, with edges joining coarse cells at infinity distance <=2q in each fixed slab. The canonical primitive packet construction supplies the lemma's conditional premise by independence from the entire distant-packet union. A sufficient fixed bad-flag tolerance is simply

delta_*=(p_*/2)^(D+1).

Choose C,R and the HT-allowed iid death p_* first, then this delta_*, then b and the allowed sigma/kappa as in the canonical proof. All constants remain independent of L and T. Independent slab couplings produce iid deaths across the full space-time history.

## Finite periodic torus: separate application and exact boundary

The canonical proof actually applies domination on the infinite lattice in Section 3. Section 4 then keeps the native torus field and uses a fixed-patch stopped-witness replay; it expressly does not rely on torus product domination or a stationary torus cluster tail. The replacement above can be used at that same infinite-lattice step without changing this adapter.

If domination of the finite torus bad flags is desired separately, apply this lemma directly to V=(Z/MZ)^4. Join distinct cells whenever their wrapped infinity distance is at most 2q. Each vertex has degree at most D=(4q+1)^4-1; periodic identifications can only reduce this count. Use one independent primitive packet per actual torus cell and slab. The radius-q packet guards are disjoint from the union of guards centered at wrapped distance greater than 2q, so the same weak conditional premise holds. For the source's sufficiently large M, each primitive guard lifts injectively, preserving its stated marginal estimate. The finite graph is already covered by the lemma and requires no new assumption.

One must NOT periodically repeat a finite torus sample on Z^4 and treat the repeated packets or flags as independent. Such a periodic infinite cover has long-range exact identifications and does not satisfy the displayed bounded-range dependency premise. Independent auxiliary domination marks on the finite torus, extended across fresh slabs, are iid over actual torus sites and times only; their periodic lift is not iid on the infinite cover.

This finite-graph clarification does not transfer the infinite-volume HT cluster theorem to a stationary torus process. The stopped fixed-patch replay, whole-slab inclusion and accumulated-homology arguments remain separate obligations.

## Scope

This supplies the exact qualitative domination step needed by the source with an explicit, very poor constant. It removes dependence of that step on acquiring or trusting the original LSS theorem pages. It does not establish the remaining envelope, eroder, HT, replay, topology, quantum-channel, or physical claims. Original LSS source acquisition remains a bibliographic verification task, not an outstanding hypothesis of this replacement argument.


