# Multiplicative backward test for bounded collective disturbances
30 October 2026. Root construction candidate; independent review pending. This removes the variance loss in the earlier fixed-population deterministic-time forcing bound. It does not import a global chemical theorem or a seed/extinction repair.

## 1. Contract
There are n PERSISTENT labels with ranks r_i in {0,...,L}, L>=1, and target rank0. The full process may contain arbitrary retained environment/history. Its conditional generator includes:

- for each nonzero-rank label, a progress transfer at rate at least q>0 reducing its rank by at least1;
- any additional safe transitions which do not increase ANY label's rank;
- adverse events changing at most k labels each, with the sum of their conditional participation intensities at any one label at most b.

The progress subrate q is an actual positive rate splitting. Its destination may depend on the current state. No independence of realized paths or adverse histories is assumed. All other evolution acts only on retained variables. The process and the following bounded test admit Dynkin/localization; in a finite-population finite-rate module this is automatic. Arbitrarily fast safe transitions are allowed if the actual process remains well-defined.

## 2. Exact product witness
Choose a in (0,1), and set beta=b(1-a)^(-(k-1)). For u>=0 define

 phi_r(u)=exp(-beta u) Pr(Pois(q u)>=r),
 f_r(u)=1-a phi_r(u).

Thus 1-a<=f_r<=1, phi_r decreases as rank increases, and

 d phi_r/du=q(phi_(r-1)-phi_r)-beta phi_r,

where phi_(-1)=phi_0 for r=0. Fix a horizon T and use

 F(t)=product_(i=1)^n f_(r_i(t))(T-t), 0<=t<=T.

For exactly one-step progress at rate q, the time derivative cancels its generator contribution and leaves

 (partial_t+L_progress)F
 =-beta F sum_i a phi_(r_i)/f_(r_i).                   (PF1)

A progress jump skipping more ranks only decreases F further. Safe events likewise contribute nonpositively. No variance estimate is needed for either of these contributions.

For an adverse event touching A with |A|<=k, its new factors are at most1. Put z_i=a phi_(r_i)/f_(r_i), so 1/f_i=1+z_i. Its relative increase is bounded by

 F_after/F_before-1 <=product_(i in A)(1+z_i)-1
 <=(1-a)^(-(k-1)) sum_(i in A) z_i.                   (PF2)

The last inequality follows by telescoping the product; every partial product of at most k-1 reciprocal f-factors is <=(1-a)^(-(k-1)). Summing actual event intensities and using the PER-LABEL participation bound b makes PF2 cancel PF1. Hence F is a nonnegative supermartingale:

 E F(T)<=F(0).

At T, f_0(0)=1-a and f_r(0)=1 for r>0. If A_T is the actual number of target labels,

 E(1-a)^(A_T)
 <=product_i[1-a phi_(r_i(0))(T)]
 <=[1-a phi_L(T)]^n
 <=exp[-a n phi_L(T)].                              (PF3)

This is a product OBSERVABLE proof, not a claim that the factors or physical labels are independent. Adapted cross-label events and arbitrary common environmental history are retained throughout.

## 3. Deterministic-time lower tail
For a=1/2, beta=2^(k-1)b. Write

 p(T)=exp(-2^(k-1)b T) Pr(Pois(qT)>=L).

PF3 and Markov give, conservatively,

 Pr(A_T<=n p(T)/4)<=exp[-n p(T)/4].                  (PF4)

The slightly stronger coefficient is 1/2-(log2)/4. For 0<T<=1,

 p(T)>=exp[-(2^(k-1)b+q)] q^L T^L/L!,

so PF4 has exponent c n T^L and threshold c' n T^L. This restores the same small-time power as independent-label forcing without assuming independent realized label paths. The earlier exp(-c n T^(2L-1)) bound remains correct within its own contract but is weaker when L>1 and T is small.

The constant k must be paid. If k grows, one may instead choose a of order1/k to keep beta of order b, at an exponent cost of order1/k. No fixed-strength bound for an event affecting the entire population is silently obtained.

## 4. Exact uses and limits
This strengthens the deterministic-time persistent-cohort input to the separately reviewed collective killed-Green calculation. Any updated stopped exponents must be explicitly recalculated and reviewed; PF4 alone is not a hitting-time moment theorem.

If physical seed events remove labels, one can sometimes extend each removed original label as an auxiliary ghost and subtract the number removed when comparing actual target occupation to the virtual cohort. Such an extension proves only a deterministic-time containment on the event of sufficiently few removals, assuming the virtual rank process itself meets this generator contract. It DOES NOT prove finite killed time or a global Green bound. The retained SEED_EXTENSION_OBSTRUCTION.md shows why: a geometrically rare complete extinction can leave infinite waiting time. Actual replenishment/finite-head return and clocks remain indispensable.

The result also does not derive a bounded per-label adverse intensity from a mere mean face holding-time bound. The actual reward-weighted entrance/exchange construction, or another genuine rate bound, must supply that interface. It is a mathematical robust-forcing lemma, not a measured physical model or a solution of general weak reversibility.
