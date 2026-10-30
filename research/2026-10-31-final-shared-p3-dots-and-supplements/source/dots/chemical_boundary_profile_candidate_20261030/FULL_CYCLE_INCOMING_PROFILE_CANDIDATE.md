# Incoming A-reserve transport through a whole boundary cycle
Status: personal construction, not independently reviewed. This is the hard kernel step proposed in BOUNDARY_RETURN_NEUMANN_PRINCIPLE_V1.md, rather than an assumed reset envelope.

## Contract and scales
Use the multi-seed graph contract with 2<=a0<m, v=m-a0>0: every degree-m fast complex contains at least a0 A; mA and a0 A+(m-a0)X_i are sources; each latter source has an A-producing edge. The graph is strongly connected; coefficients are fixed positive. The connector is unchanged, q>m. Work at large residual r=N-H(B), with active pointwise section S={B=q,A>=a0}. Define p0(r)=Cr^-v, and K(r)=r^gamma with 0<gamma<v/m and also gamma<v/(v+1). Constants may depend on every fixed exponent and graph parameter.

The incoming-moment lemma supplies f_s(A)=(1+A)^-s and, for every fixed s>0, the FIRST-connector kernel bound

    E[f_s(A_after); any connector event]<=C_s f_s(A_in). (M)

For clearing, this follows from F_s=C1 f_s+C2N^-s as previously derived. Immigration and activation increase A; adding their terminal rewards to the killed-generator inequality costs no more than their killing terms already subtract. Thus (M) is a joint first-event inequality, not a conditional output assertion.

The local mean can be sharpened to T<=C N^-v A^(1-a0): Q A^(1-a0)<=-cN^v near the low-A face; killing of this positive function divided by N^v dominates in the interior. It follows that p0 controls the worst active mean and the clearing-output inverse-m-th moment. The clearing compensator and Holder give uniform activation-before-clearing probability epsilon(r)->0. Immigration-before-clearing is O(p0).

For the activation subkernel, (M) with exponent2s and Cauchy-Schwarz give

    E[f_s(A_after); activation first]
       <=C_s sqrt(epsilon(r)) f_s(A_in).                (Mrare)

The same statement holds uniformly in B>=q, after catalyst restoration. It is crucial that rare extra activations are small in the INCOMING-PROFILE norm, not merely in total mass.

## 1. Counting connector stages before a fixed number of immigrations
Start with B bounded by a fixed constant (q or2q-1 or a bounded low phase). Distinguish LOW-phase activations, which are not rare, from FAST activations at B>=q, which obey (Mrare). Counting all activations as rare would be an error.

Stop at the m-th noncompulsory low-phase immigration or any fast immigration. Group a visit to B=0, its compulsory immigration, and its subsequent low-phase run into one launch. A zero-length run activates directly to section B=q and terminates. Thus every nonterminal B=0 launch consumes at least one counted noncompulsory immigration. Before the stop there are at most m compulsory B=0 immigrations, so the TOTAL immigration count is bounded by2m plus an initial constant.

Use the explicit nonnegative phase height

    J(B)=B-(q-1)1_{B>=q}.

A low-phase activation leaves J unchanged. A fast activation increases J by q-1. Every clearing decreases J by at least1 (by q if its target remains high). Immigration increases J by at most1; the low-to-high threshold crossing actually decreases it. Consequently the clearing count is <=J(B_initial)+I+(q-1)T_fast. Every nonterminal low activation must be followed by a clearing before another low activation, so its count is at most the clearing count plus1. Therefore the total connector-stage count is <=C_{m,q}+C_q T_fast.

For each specified path of T_fast rare activations, ordinary clearing profile kernels cost at most C_s per event, while each FAST activation costs C_s sqrt(epsilon) by (Mrare). Low activation increases A and has profile norm at most1. The number of event-type strings grows only exponentially in T_fast. Thus summing these positive-kernel products is geometric once r0 is large. This earns bounded full-processor profile norms for every fixed s, retaining the actual input A. No finite cap or independent-reset law is used.

## 2. Spending inverse powers on low-phase immigration races
At positive low B, the probability of immigration before activation is <=C/(1+A). Moreover immigration increases A. Thus the operator for one such race maps f_s to at most C f_(s+1); activation increases A and can only decrease these profiles. Fast processing transports the remaining f_s according to section1.

Stop the cycle upon section return, the m-th noncompulsory immigration, a fast immigration, or an inactive high-B clearing output. A high-B inactive output has A_after<a0, so its probability is <=C E f_m(A_after); (M) bounds it by C f_m(A_in). A fast immigration probability is <=C f_m(A_in) by the incoming-dependent killed-time bound from the preceding lemma (common B catalyst only helps).

Before either designated bad event or the m-th counted immigration, sum event-type strings as above. Every path reaching m counted immigrations has spent m inverse powers; every designated bad fast branch itself charges f_m at its entrance. Consequently, from a FIRST clearing-output law nu with total mass<=1 and int f_m dnu=t,

    P(designated bad or m-th counted immigration
      before return to S)<=C t.                        (E)

This improves the scalar-envelope cross-term estimate. It does not multiply unconditional marginal moments: the f_s functions are transported through the actual positive kernels, and each race changes the exponent before the next kernel composition.

## 3. Actual continuation of designated branches
A high-B inactive state has A<a0. Immigration increases A by1; activation, whenever A>=1, increases it by m-1 and directly makes it active. Therefore at most a0 actual immigrations, or an earlier activation, seed activity. Each waiting interval has a positive immigration-rate floor; the expected total seeding time is bounded. Its upward residual displacement is at most a0 h. This continuation is not instantaneous and may reverse a previous downward residual jump.

After a designated branch, use actual repair to S. For exponential weights w_theta(r), the active/fresh-low repair kernel has a downward factor exp(-theta h)<1, while fresh-low upward and bad factors tend to0 with p0^(1/m). Group neutral fast-to-low motion inside a round. Inactive clearing outputs have mass O(p0), and their finite seed displacement has a fixed exponential multiplier. Thus the positive round norm is exp(-theta h)+o(1)<1 after increasing r0. It earns finite real repair cost and a bounded expected terminal w_theta, uniformly in hidden composition. Arbitrary initial low/inactive inputs pay only a fixed exponential multiplier, because their initial number of upward seed/race steps is bounded.

This needs the exact coefficient-one downward bound: a fresh reset followed by no noncompulsory immigration has nonincreasing r; its terminal weight is at most the current weight. Rare immigrations/inactive outputs are charged separately. Replacing this by an unspecified C exp(-theta h) would be insufficient for small theta.

Therefore (E) survives actual continuation with weighted terminal and running-cost bounds C_theta t w_theta(r). Before the designated stop, r can rise only a bounded number of times, so exponential factors are bounded as well. The same is true for fixed polynomial enlargements of w_theta after choosing r0 so those enlarged weights are increasing.

## 4. Weighted bad-entry estimate remembers the FIRST law
Let B_bad={A<=K(r)} on S. On paths returning to S before the designated stop, section1 transports f_m through all connector stages and low races (dropping race factors when unnecessary). Since r_next can increase only a bounded amount, K(r_next)<=C K(r). Thus

    E[w_theta(r_next)1_B_bad; first clearing branch]
       <=C_theta K(r)^m t w_theta(r).

The designated continuations cost C_theta t w_theta(r), which fit the same bound. Here t is the first clearing sublaw's moment, bounded by C T for the actual incoming section state, NOT by p0 unless taking a uniform supremum.

The first immigration branch has mass k_I T and bounded weighted continuation. The first activation branch has mass proportional to U; its first clearing is downward, and its fresh reset moment is bounded by Cp0. Applying the same argument from that reset bounds its bad-entry contribution by C_theta K(r)^m p0 U w_theta(r).

Consequently the actual whole-cycle kernel satisfies

    P[w_theta(r_next)1_B_bad]/w_theta(r)
       <=C_theta K(r)^m [T+p0 U].                      (Bentry)

For the weight g(r)w_theta(r), g=r^-v, the same argument gives the additional factor Cg(r): before a designated stop r increases only a bounded amount, and g(r)w_theta(r) is increasing; after it use the corresponding enlarged-weight repair bound. Uniformly T<=Cp0 and U=o(1), so the bad-to-bad norm in weight gw is O(K^m p0)->0.

### Unbounded first-clearing phase after extra high activations
An activation-first section branch can undergo arbitrarily many extra high activations before its first clearing; the resulting B is not bounded pointwise. Do not apply a bounded-initial-phase estimate to that law without accounting for its history. Instead start the stage enumeration at the original B=2q-1. Each preceding high activation adds only q-1 to the phase height and carries its small kernel norm. The continuation profile constant grows at most exponentially in that count, while the rare-activation norm decays geometrically. Summing the count preserves a finite constant. The first clearing moment bound Cp0 holds at each actual pre-clearing input relative to its clearing mass; disintegrate there, multiply by the geometrically summable preceding-history weights, then continue. This earns the asserted Cp0 contribution without assuming that the first-clearing B is bounded.

## 5. Good-region occupation gap is graph-derived
For A between K and M=N^eta, choose gamma<eta<v/(v+1). Over time c/[A^(a0-1)N^v], bounded-jump counting gives a fixed positive probability of staying in[A/2,2A]. The clearing hazard on this interval is O(A^(v+1)/N^v)=o(1), and competing hazards also give o(1). Thus U>=c A^(2-a0)N^-v. Together with T<=C A^(1-a0)N^-v this gives T/U<=C/A<=C/K.

For A>M, stop at killing or first entrance below M. Before that entrance U_pre>=M T_pre; the bounded-jump landing has the same ratio bound C/M. Strong Markov extends T/U<=C/K to all good inputs. This does not claim any vanishing ratio for A=O(1), which was analytically falsified.

## 6. Closing the composition-dependent section potential
The uncorrected section weight has drift <=[-c_theta U+C_theta T]w, because activation-first produces a downward clearing and coefficient-one continuation, while (E) bounds the clearing-first dangerous branches by CT. On bad inputs this is at most Cp0 w. On good inputs T/U<=C/K->0.

Use the actual bad-return Neumann construction in BOUNDARY_RETURN_NEUMANN_PRINCIPLE_V1.md with g=p0. Its norm is O(K^m p0)->0 by (Bentry). The good-side leakage of the resulting correction is at most

    C p0 K^m [T+p0 U]w
       <=C[p0 K^(m-1)+p0^2 K^m]U w=o(Uw).

Hence the personally derived section profile w+H has negative drift on BOTH bad and good incoming compositions, although the scalar pointwise time/occupation gap is false on the bad region. Actual running costs are paid by a polynomial enlargement, as in the operator theorem. This is a candidate completed mechanism, not an independent review or a general WR result. The full-processor path enumeration, weighted designated-branch repair, and first-law bad-entry bound are the precise new audit obligations.
