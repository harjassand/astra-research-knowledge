# A fractional-factorial moment envelope for target-following episodes

This strengthens the new reward operation in `EPISODE_TAIL_LIFT.md`. It builds on Kriebel's August 2026 v1.2.4 marked-target identity, path episodes, and binary single-linkage availability proof, all explicitly attributed there. This is an author-derived extension, not an independent audit or a historical-priority determination.

## Whole consequence at the earned scope

For EVERY finite weakly reversible ONE-LINKAGE BIMolecular mass-action list, every fixed positive rate vector, and every actual infinite communicating class, there exists beta>0 such that its stationary law obeys

    E_pi product_i (X_i!)^beta < infinity.                         (A)

Moreover the actual CTMC has a state with a finite exponential moment of its positive physical return time. Every initial state has a finite exponential moment of the physical hitting time of a finite classwise head. Finite classes and absorbing classes are elementary separate cases. The argument does not give an acquired universal head radius, moment value or useful mixing-time bound, and no spectral-gap assertion is made here.

This is a completed consequence of the primary source's proved availability lemma plus the envelope below. It covers arbitrary species count and mutually changing inventories, with no controller, phase pinning, stationary fiber or homogenization. It does NOT establish general multiple-linkage or higher-order recurrence.

## 1. An exact multiplicative recursion

Use the notation of `EPISODE_TAIL_LIFT.md`: m complexes, a_y total outgoing constant, R=a_max/a_min, C0=log(mR), V(x,t)=sum_i log((x_i−t_i)!), and one fixed directed target-following path of length k<=m−1 from t to terminal c. Let q_j>0 be the fraction of outgoing rate constant assigned to its designated edge, and p_j the ACTUAL probability that the next source is its carried target. Set

    q_* = min_(designated edges) q_j > 0.

The source's path library and q_* are finite and acquired directly from the raw graph. For 0<alpha<1 the ordinary one-jump identity gives

    E exp(alpha Delta V) <= B p_j^alpha,   B=exp(alpha C0).

Let M_j be the exponential moment of the TOTAL remaining episode reward. Since a designated continuation has exactly zero reward,

    M_j = E exp(alpha Delta V) + q_j p_j (M_(j+1)−1).              (1)

All reaction channels, physical states and output inventories remain actual. No path likelihood is replaced by a rate-modified comparator.

## 2. A uniform alpha exists and can be selected explicitly

Suppose M_(j+1)<=1−c. Then (1) implies

    M_j <= sup_(0<=p<=1) {B p^alpha − q_* c p}.                   (2)

The unrestricted supremum over p>=0, a valid upper bound, equals

    (1−alpha) exp{[alpha C0+alpha log(alpha/(q_* c))]/(1−alpha)}.  (3)

This is just a concave scalar maximization. It has no unproved probabilistic interface.

Here is one deliberately inefficient but explicit choice. Put L_0=1 and recursively

    L_(j+1)=q_*^(−1) exp(C0+2L_j),   j=0,...,m−2,
    alpha=1/(4 L_(m−1)).                                        (4)

Then alpha L_j<=1/4. If c>=alpha L_(j+1), the upper bound in (3) is at most

    (1−alpha) exp[−2alpha L_j/(1−alpha)]
       <= exp(−2alpha L_j)
       <= 1−alpha L_j.                                         (5)

The last inequality holds for 0<=alpha L_j<=1/4. A terminal bound M_k<=1/2 supplies c>=alpha L_k for every k<=m−1. Applying (5) backward therefore yields M_0<=1−alpha.

The tower in (4) establishes mathematical existence; its size is a defect of this envelope, not a lower bound on the network's real relaxation. The accompanying code instead searches rational alpha=2^(−K) and CERTIFIES the scalar inequalities with exact rational logarithm enclosures. This acquires a finite alpha certificate for the displayed diagnostics. It is not an acquisition of the classwise head.

## 3. The terminal bound is actually earned in the governing class

It suffices that the terminal actual source probability obey

    p_(z+c)(c) <= p_* := (mR)^(−1) 2^(−1/alpha),                 (6)

because then B p_*^alpha=1/2. Kriebel's binary one-linkage top-complex lemma proves that along EVERY escaping marked sequence in a fixed class there is, after subselection, a fixed terminal c for which p_(z+c)(c)->0. Consequently the states where no terminal satisfies the FIXED threshold (6) form a finite head. This is the same analytic compactness operation used in the source, at a specified stronger threshold.

Choose the terminal with the LEAST actual p_(z+c)(c) inside the carried linkage, before the episode starts. No test of membership in the finite head, and no numerical evaluation of the extremely small threshold (6), is needed to operate this selector. For rational rates every compared probability is an exact rational number. Outside the proved finite head the selected terminal automatically qualifies. Therefore

    E W(Z_tau) <= (1−eta)W(x,t),
    W(x,t)=exp(alpha V(x,t))=product_i ((x_i−t_i)!)^alpha,         (7)

where eta>0 is supplied by (4), or by the acquired rational envelope certificate. Formula (7) is global on the whole actual class under the source's binary single-linkage hypotheses. It is not a bulk-only result.

## 4. Physical return times

Let rho=1−eta<1 and sample successive selected episodes until a landing in the finite head H. Since W>=1, the stopped nonnegative supermartingale rho^(−n) W(Y_n) proves

    E rho^(−sigma_H) <= W(x,t).

There are at most m genuine jumps per episode, so the original embedded chain has an exponential moment of its hitting jump count of H. A first ordinary jump from H has finitely many successors. Thus every head return excursion has an exponential jump-count moment, uniformly over the FINITE head.

To obtain a return to one particular marked state, use the original finite irreducible trace on H. From every trace state a fixed finite trace path hits the chosen state with a common positive probability within a fixed finite number of trace steps. The maximum head-excursion moment-generating function tends to one as its argument decreases to zero, by domination at the already proved positive argument and finiteness of H. For a sufficiently small argument, the weighted probability of failing one such trace block is strictly less than one. Summing those blocks gives a finite exponential moment of the full original jump-count return. This argument retains any dependence between an excursion duration and its terminal trace state.

Every nonabsorbing physical state has q(x)>=kappa_min>0. Conditional on the embedded path, the ACTUAL holding-time moment at s<kappa_min is

    E exp(s H_x)=q(x)/(q(x)−s) <= kappa_min/(kappa_min−s).

Choose s small enough that the right side, raised to the jump count, is integrable by the preceding jump-return bound. The physical return therefore has a finite exponential moment. Infinite repeat visits have independent positive holding times at the fixed return state, so their sum diverges: the same construction proves nonexplosion rather than presuming it.

## 5. Physical factorial rewards and (A)

At EVERY preterminal point of a selected episode the marked residual is the SAME z, so W is exactly the same value W(x,t). The total embedded W-reward in an episode is at most mW(x,t). The geometric drift (7) pays this reward after multiplication by m/eta. Stopping, taking the finite head's first jump, and closing its finite trace therefore proves a finite expected sum of W over an entire marked regenerative cycle. Actual holding means are at most 1/kappa_min, so the same cycle has finite physical occupation reward integral W dt.

For any 0<beta<alpha,

    sum_i log(X_i!) <= V(X,t)+D log(|z|_1+D+1),

and the extra logarithmic term is absorbed by (alpha−beta)V outside a finite set. Thus product_i (X_i!)^beta <= C W(X,t), uniformly over the finite target set. The physical regenerative occupation formula proves (A). For example beta=alpha/2 is an acquired positive choice once alpha is selected.

Because sum_i log(x_i!)>=n log(n/d)−n for n=|x|_1, (A) implies all prescribed stationary exponential count moments and a factorial-order qualitative tail. The finite prefactor in that tail is not numerically acquired here.

## 6. What this changes and what it does not

The primary preprint proves recurrence and explicitly leaves moments and convergence estimates as further questions. The new multiplicative scalar envelope upgrades its episode mechanism to a global fractional-factorial reward and exponential physical return operation. The baseline target augmentation and its availability proof remain prior work. General Markov-chain sampled drift and finite trace closure are established tools; the acquired part here is the multiplicative envelope and the compatible reward/clock chain.

The actual scientific obstruction for general weak reversibility remains terminal rarity, or a replacement for target-following episodes. `ORDERED_COMPLEX_OBSTRUCTION.md` gives a fully coupled THREE-species, one-linkage degree-seven raw network in one fixed class where every such episode is nonnegative along an unbounded ray. Thus neither (7) nor a general recurrence claim is being extended by assumption. A new actual activation-cycle operation is needed there and across linkages.

The exact accepted Astra extension is in `N1567_TAIL_TRANSFER.md`: the same proof applies to EVERY successful terminal-gap cone certificate in that source, without a one-linkage or bimolecularity requirement. `mgf_selector.py` actually acquires raw graph/path data, a scalar certificate and the least-probability rule under its narrower CHECKED binary common-span admission. Unsupported stable inputs return UNKNOWN. The common-span example's acquired alpha is 2^(−4096); its numerical finite head and moment value are not acquired.
