# Non-small dormant block: same-exponent weighted Green with incoming profiles
Status: personal derivation, unreviewed. This closes the isolated D=0 block, not yet its full feedback with the positive-D boundary cycle.

## Exact killed reference process and target norm
On D=0, C is frozen. The actual connector0->A+B->mA+qB->0 runs until the fast seed mA+qB->(m-1)A+D+qB fires. Here m=a0+2, q>m. Its rate k_seed(A)_m(B)_q is proportional to connector clearing. The killed PRE-jump path is exactly the ordinary connector with enhanced clearing rate k_D+k_seed, stopped at the first independently seed-marked clearing. The actual seed terminal reward uses A_seed=A-1, D_seed=1, B unchanged, C unchanged; it is not the reference clearing's post-state.

For fixed theta>0, s>=0, use the exact residual r=C+A-H(B) and

    W(A,B;C)=exp(theta r)(1+A)^-s.

Claim: uniformly in all A,B,C,

    E[int_0^tau_seed W(X_t)dt+W(actual seed output)]<=C_theta,s W(A,B;C). (G)

The same bound holds when adding W rewards at each section visit B=q, or at the discrete blocks below. This is the incoming-profile/same-exponent norm required by a non-small block. It is stronger than pointwise finiteness or a separate list of all moments.

## 1. Pointwise finiteness is earned by an ordinary comparator
The enhanced three-complex connector is weakly reversible, deficiency-zero and rank2 (q>m). Its complex-balanced parameters satisfy ab=k_I/k_T and a^m b^q=k_I/(k_D+k_seed). Its conditional product-Poisson invariant laws have every polynomial-exponential moment. Nonexplosion follows independently from the linear-total Lyapunov estimate. Regeneration plus a fixed positive seed-marking probability earns finite pre-seed occupation and seed-output moments from every fixed finite input state.

Indeed W<=exp(theta C)exp(theta A), and event/visit rewards are bounded by a polynomial propensity times such an exponential. The actual seed reward has the same bound. For any finite set of (A,B) inputs, these constants are uniform; frozen C contributes only exp(theta C). This will supply ACTUAL boundary values on a finite corner, not a recurrence assumption for the full chemical network.

## 2. High A: a seed chance contracts the actual weighted continuation
Choose A0>>m. When A>A0 and B>=q, the first fast/connector event is seed or clearing with probability1-O(A^(1-m)); conditional on this pair, seed probability is the fixed p=k_seed/(k_seed+k_D)>0. The first immigration probability is O(A^-m B^-q), and activation probability O(A^(1-m)B^(1-q)).

Clearing never increases r; it changes the inverse-A factor by1+O_s(1/A). Activation is r-neutral and increases A. Immigration can raise r only by fixed h=q-m and increases A. Consequently the NONSEED first-event continuation has expected W ratio <=1-p+O_theta,s(1/A).

If clearing lands at B<q, compose the next low-phase approach before declaring the block complete. Low-phase A only increases. Before B>=q there are at most q immigrations or one activation. Its mean duration is bounded by q/k_I. An upward r-wrap requires an immigration to beat activation at positive B, with probability O(1/A); hence its expected terminal W ratio is <=1+O_theta,s(1/A), while its running cost is <=C_theta W. Neutral fast-to-low motion is inside this block, not called rare.

Choose A0 so the composite nonseed continuation norm is <=rho<1, uniformly in B. Stop additionally upon A<=A0, where the terminal value is supplied by the head/corner construction. Actual seed rewards and running/visit costs within a block are <=C_theta,s W. This gives a high-A normalized Green bound of the form

    G_high<=C1+C2 H_head,                              (H)

with constants independent of C and B, once the head value is bounded. Starting B<q is handled by its initial low approach.

## 3. B-large finite-A head: invert the true non-small leading kernel
Take A<=A0 and B>=B0, with B0 large. Use the following collapsed physical step:

- A>=m: wait for seed or clearing; a competing birth is an error.
- 1<=A<m: prescribe activation before immigration, then seed or clearing; a contrary birth is an error.
- A=0: take its compulsory immigration, then prescribe activation and seed/clearing; extra immigrations or fast births are errors.

Each step contains at most three actual events and has bounded expected running cost in W. Intermediate A after a prescribed activation is allowed to exceed A0; it remains INSIDE the collapsed step until seed/clearing/error. It must not be mistaken for an uncontrolled head exit.

In the limiting error-free kernel, seed occurs with probability p. Otherwise the endpoints are

    (A,B)->(A-m,B-q)       if A>=m,
    (A,B)->(A-1,B-1)       if 1<=A<m,
    (0,B)->(0,B)           if A=0.

The first two endpoints never increase r; the last has exactly unchanged r. A strictly decreases until reaching0. The inverse-A factor telescopes over this finite descent and grows by at most(1+A0)^s. Therefore the n-step weighted nonseed kernel P0 satisfies

    ||P0^n||_W <=(1+A0)^s(1-p)^n.

This earns a finite positive Green operator even though a one-step weighted row sum need not be <1. Equivalently, the only recurrent leading phase is the A=0 loop with survival probability1-p; the other bounded-A phases are transient. B residue information is retained through the exact r shifts, not averaged away.

Actual errors have probability O(1/B), uniformly over this finite A alphabet, and bounded weight multipliers depending only on theta,s,A0,m,q. They feed either the head or high-A region with bounded overshoot. If B falls below B0 after a prescribed step, it enters a fixed finite (A,B) corner and is assigned its actual comparator Green value from section1. Thus positive-kernel perturbation of the earned P0 Green gives

    H_head<=C3+eta G_high,                              (B)

where eta can be made arbitrarily small by choosing B0 large. The finite-corner boundary constant may grow with B0, but it is finite and does not affect the small coupling coefficient eta.

Combining (H)-(B), choose eta C2<1/2. The resulting two-type Neumann construction proves finite uniform normalized Green values. This is an actual coupled head/high process; no invariant finite cap is imposed.

## 4. Rewards, physical time and stopping conventions
The proof may be performed first with finitely many blocks and actual corner values, then passed monotonically. Reference-chain nonexplosion and marked killing independently ensure the actual stopping interpretation. Within every collapsed head step, r shifts by a bounded amount and A remains in a fixed enlarged finite alphabet; within a high/low block the fixed-shift profile estimates above apply. Hence time-integrated W and one W reward per block are both paid.

Section B=q visits can be charged to block endpoints/interiors with a fixed multiplicity. On the finite corner their expected weighted count is finite by the reference jump-intensity occupation formula; outside it the same block construction pays them. The actual seed terminal weight has unchanged r and A decreased by1, so it also has a bounded within-block multiplier. This proves all variants of (G).

## What is still not proved
This is a local Green estimate for the EXACT D=0 killed subsystem. Positive-D excursions can change the frozen reservoir C before returning to D=0. Their phase-dependent incoming forcing must still be composed with this Green; a mere small unweighted return probability is insufficient. The separate dormant-return inverse-power gain is relevant, but the complete coefficient-one global section drift has not yet been written or reviewed. No full recurrence upgrade is claimed by (G).
