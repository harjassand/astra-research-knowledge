# Actual positive shared-waveform ambiguity beyond three stages

19 October 2026. Kinetic-frontier worker, with independent endpoint-rank and proof audits by the kinetic_realization and collision_audit workers and the arbitrary-finite-duration extension supplied by root.

**Internal mathematical result. Historical priority UNKNOWN. No physical assay, practical advantage, or mission achievement is claimed.** This is an exact existence theorem for actual positive waveforms, not an independently specified pair of ramp matrices and not a successful numerical optimizer.

## Result and scope

The three-stage two-speed identification theorem does not extend to four stages under its stated distinct-spectrum and unequal-adjacent-response hypotheses. There are two different four-stage orders, all four response ratios pairwise unequal, and an actual bounded strictly positive normalized waveform for each order, such that the same waveform at durations d and 2d gives identical **complete** mixed endpoint surfaces. Pure-level endpoint laws also agree.

More strongly, for **any preselected finite menu of distinct positive ramp durations**, root's generic gap choice and the argument below give a counterexample. If the interface also supplies a repeatable return waveform, each model can have a bounded strictly positive outward waveform and a bounded strictly positive return waveform, each shared over the duration menu, such that **every finite legal A/B hold/ramp word** has the same terminal law in the two models. Holds may have arbitrary nonnegative durations; ramps must use the preselected finite menu. Consequently repeated loops and extra endpoint precision cannot distinguish that pair.

Quantifiers matter. The models and waveforms may depend on the finite menu. This does not construct one pair agreeing at every continuously variable ramp duration, does not rule out an adaptive strategy with unrestricted new durations, and does not contradict the reciprocal-volume theorem's generic weighted-product nonresonance condition. The construction is in its resonant set.

## Model and the old open obligation

The transient column generator of a mandatory irreversible serial four-stage chain is

    Q(k) = (J-I) diag(k),

where J has ones immediately below the diagonal; the fourth stage exits to an absorbing completed state. Preparation is e1 and noncompletion readout is c=1^T. Pure A and B rate vectors have distinct positive entries. During each finite ramp the four rates are bounded strictly positive functions of normalized time. A single waveform is stretched to each selected duration within a model. Competing models may have different unknown waveforms, exactly as in the earlier identification contract.

The earlier m4 target satisfied augmented total nonnegativity and every adjacent-pair joint-waveform test, but its coupled realization remained UNKNOWN. The proof here does not settle that specific epsilon L target. Instead it constructs a different, locally obtainable collision through a regular constant positive seed, thereby closing the existence question without assuming any global waveform-realizability characterization.

## Equal-sum quadratic blocks give an exact nonclock collision branch

Choose four distinct labels

    lambda = (a,b,S-b,S-a),       0<a<b<S/2.

Group alpha=(1,4) and beta=(2,3). Their A rate sums both equal S. Write

    P_alpha = a(S-a),       P_beta = b(S-b).

The two stage orders are

    sigma = (1,4,2,3),       tau = (2,3,1,4).

Define B rates near the A rates using the roots of two quadratics:

    mu_1,mu_4 are the continuation of a,S-a in x^2-Sx+t P_alpha=0,
    mu_2,mu_3 are the continuation of b,S-b in x^2-Sx+t P_beta=0.

Thus mu=lambda at t=1; for t sufficiently near 1 all rates remain positive and distinct. Both B block sums are S, and both block products are multiplied by the same t.

For a serial order omega, the matched diagonal residue coefficient is

    C_i^omega = product_(j before i) lambda_j/(lambda_j-lambda_i)
                product_(j after i) mu_j/(mu_j-mu_i).

These coefficients are identical for sigma and tau. To verify this, consider i in alpha. Moving beta from after i to before i changes its cross-block factor from

    P_beta,B / (P_beta,B-P_alpha,B)

to

    P_beta,A / (P_beta,A-P_alpha,A).

The two are equal because both products scale by t. The identity for i in beta is the same with the blocks exchanged. Factors within each block are unchanged. This proves all four C equalities for the whole branch, not only to first order.

All four response ratios are pairwise unequal whenever t != 1. Indeed each paired lambda_i,mu_i satisfies

    mu_i(S-mu_i) = t lambda_i(S-lambda_i).

Put r_i=mu_i/lambda_i. Then

    lambda_i r_i^2-S r_i+t(S-lambda_i)=0.

If two distinct labels have r_i=r_j=r, subtraction gives r^2=t; substitution gives r=t. Positivity forces r=t=1. Thus any nontrivial branch point has every response ratio different. This is stronger than the old adjacent-inequality premise.

## Exact target matrices, including the diagonal covariance

For a distinct ordered rate vector k, let V(k) be the unit lower triangular eigenvector matrix of Q(k), so

    Q(k)=V(k) diag(-k) V(k)^(-1),
    V_rj = product_(l=j)^(r-1) k_l / product_(l=j+1)^r (k_l-k_j), r>j.

For each order omega in {sigma,tau}, and each selected duration multiplier D, define

    F_D^omega(t) = V(mu^omega(t)) diag(exp(-D L lambda^omega)) V(lambda^omega)^(-1).

Here L>0 fixes a baseline ramp time. These matrices are lower triangular, and their physical diagonals are exp(-D L lambda^omega). Therefore all duration diagonal identities hold exactly, including F_2,ii=F_1,ii^2.

The full mixed noncompletion surface is

    q_D(z,s)/(zs) = sum_i C_i(t) exp(-D L lambda_i)
                           /[(z+lambda_i)(s+mu_i(t))].

This follows by inserting the eigenvector factorization into

    c(sI-Q_B)^(-1) F_D (zI-Q_A)^(-1)e1.

All off-diagonal rate-labelled residues vanish. Since the C_i are identical for the two orders, the entire surfaces agree for every positive pair of clocks z,s, not just a finite grid. Pure A and B completion laws depend only on the unordered rate multisets and also agree.

At t=1, the targets are genuine constant positive ramp flows:

    F_D^omega(1)=exp(D L Q(lambda^omega)).

The remaining step is to prove that nearby target tuples are still realized by one shared positive waveform per model. This is precisely what local endpoint submersion supplies.

## Positive shared-waveform realization by local openness

For k selected durations D_1,...,D_k, consider the endpoint map from a bounded positive normalized waveform to its k lower triangular transient matrices. Its image lies in the manifold M where, for each physical diagonal i, all duration diagonals have one common integrated hazard:

    log R_Dl,ii / D_l is independent of l.

The dimension of M is 4+6k. At a constant positive waveform Q(lambda), its linearized response in the eigenbasis has four tied diagonal directions and strict-lower coordinate functions proportional to

    D_l exp(D_l Delta_pq u),       Delta_pq=lambda_q-lambda_p, p>q.

Each root coordinate is affected by at least one rate control. One explicit coefficient is

    (V^(-1) B_p V)_pq = -V_pq != 0,

where B_p is the generator derivative with respect to rate p. If all 6k numbers D_l Delta_pq are distinct, exponential linear independence separates every strict-lower output coordinate. The four diagonal rate controls are independent. Thus the endpoint derivative is onto the tangent space of M.

This infinite-dimensional statement has a finite piecewise-constant version. Use 6k+1 equal intervals and vary all four stage rates independently on each interval. If an output covector annihilates the resulting derivative, its integral over each interval is zero for each input. Those integrals form a Vandermonde system in the distinct positive nodes exp(D_l Delta_pq h), together with node 1. Hence every coefficient vanishes, giving rank 4+6k. The ordinary finite-dimensional submersion/implicit-function theorem gives a local right inverse.

All baseline rates are strictly positive. Consequently the right-inverse waveforms remain bounded and strictly positive for sufficiently small |t-1|. The target tuples above lie in M and approach the constant seed, so they have actual shared-waveform preimages in both orders. These are not independent waveforms for each duration.

For the concrete two-speed choice

    lambda=(1,3,8,10), sigma=(1,4,2,3), tau=(2,3,1,4), D=(1,2),

the signed strict-lower gaps for the true order (1,10,3,8) are

    {-9,-2,7,-7,2,-5},

and their doubles are {-18,-4,14,-14,4,-10}. All twelve are distinct. The alternative order has the same gap set. The independent worker kinetic_realization provides an exact rational rank certificate using only five intervals of length log 2, with total L=5 log 2. General regularity also holds at any chosen L>0 using the interval argument, so the theorem does not require a long damping ramp.

For an arbitrary fixed finite duration menu, choose a,b,S generically. With x=b-a>0 and y=S-a-b>x, the six signed gaps are

    {-(x+y),-x,+y,-y,+x,-(y-x)}.

Every collision D_l Delta_p=D_r Delta_q excludes a proper linear condition on x,y, apart from the identical-root/identical-duration case. There are only finitely many such conditions. Positive x,y with y>x avoiding them exist, and a>0 can then be chosen freely. This is root's extension from two speeds to every preselected finite menu.

## A concrete rational branch point and certified waveform box

The exact script [exact_collision_certificate.py](exact_collision_certificate.py), using the independent [fixed_hazard_jacobian.py](../kinetic_realization/fixed_hazard_jacobian.py), makes the two-speed existence result quantitative. Put

    eta=2^(-128), u=108/25+eta,
    w=(50u-216)/(12-5u^2),
    mu=(1-w/2, 3-u w/2, 8+u w/2, 10+w/2).

Every mu is rational. With x=9+w and y=5+u w, the identity 12x^2-5y^2=847 implies that the two B block sums equal 11 and their products are 10t and 24t for the same rational t. Also t!=1 and all four response ratios are different. This is one explicit branch point, rather than an unspecified sufficiently small perturbation.

For each order, divide the baseline ramp into five chronological intervals of length log 2. For each of the first three stages i and intervals j=0,...,3, add the free rate parameter v_ij in interval j and subtract it in interval 4. Keep stage 4 constant. These twelve parameters preserve every integrated stage hazard exactly. The output map is the twelve raw physical strict-lower entries at durations d=5 log 2 and 2d. Its center Jacobian J is rational and invertible. The helper computes J and its inverse exactly for both orders.

Let alpha be the larger infinity norm of the two exact inverses. It is approximately 2.492331716e28. Use the rational parameter radius

    r = 1/(4 alpha * 9216) = approximately 1.08840793290e-33.

The completed five-state propagators are stochastic. Duhamel differentiation and contraction in induced column 1-norm show that the first derivative of a complete flow in any compensated interval direction has norm at most 4D log 2 < 8 for D<=2. Every scalar Hessian entry is therefore bounded by 64. Consequently

    ||J(v)-J(0)||_infinity <= 12^2 * 64 * ||v||_infinity
                           = 9216 ||v||_infinity.

This bound uses the raw physical output coordinates; no uncharged eigenvector conditioning is hidden in it.

For each of the four targets (two orders, outward and return), let F(v) be the twelve-component endpoint discrepancy and set A=J(0)^(-1). The fixed point map is

    N(v)=v-A F(v).

The exact rational script verifies

    beta=||A F(0)||_infinity <= 0.00035429158 r,
    sup_(||v||<=r) ||I-A J(v)||_infinity <= 1/4.

Thus N is a contraction mapping the closed radius-r box strictly into itself. Banach's theorem defines a unique exact rate-parameter vector there, obtainable as the limit of the specified Newton-preconditioned iteration. The resulting five-piece rate waveform is a single common waveform for d and 2d. It is an actual positive flow realization: all rates are between 3/4 and 11, and all four integrated-hazard identities are exact. This proof requires no numerical optimizer and no promotion of total nonnegativity to common-waveform realization.

The JSON receipt records each rational beta/r and contraction bound, all targets, the branch parameters, exact endpoint-preserving gauge identities, and 64 finite word replays. The proof, not those finite replays, establishes universal word equivalence. The explicit contrast eta=2^(-128) is chosen to make a conservative local certificate simple; it is extremely small and supplies no practical finite-data advantage.

## Smooth ramps matching the actual endpoints

Root observes that the existence theorem can require C-infinity positive waveforms that equal lambda at the outward start and mu at the outward finish, and the reverse at return. Here is the justification.

At the common-clock seed, approximate the full-rank piecewise-constant control variations by smooth bumps supported strictly inside the ramp interval. The endpoint derivative depends continuously on the variations. Full rank is open, so a sufficiently close smooth bump family retains full rank. Let chi be a smooth transition from zero to one that is flat at both endpoints. For the outward base use

    k_base(s,t)=lambda+(mu(t)-lambda) chi(s),

and for return interchange the endpoints. Add the finite smooth bump family. At t=1 this is the same regular constant positive seed. The finite-dimensional implicit-function theorem gives nearby bump coefficients realizing the same exact target tuples. Bumps vanish near both ends, so the ramps match the pure levels and glue smoothly to constant holds; positivity survives by continuity.

This strengthens the model-validity counterexample without supplying a monotone rate ramp, an endpoint rate envelope, a calibrated rate-control law, or waveform time reversal. Those additional restrictions are outside the theorem. The explicit rational Banach box above certifies the five-piece waveform version; the endpoint-matching smooth version is a separate local-existence corollary.

## Return controls and exact equality for every word

Define return targets using the same spectral damping factors:

    G_D^omega(t) = V(lambda^omega) diag(exp(-D L lambda^omega)) V(mu^omega(t))^(-1).

They also approach constant positive seed flows and satisfy all diagonal duration relations. The same local-openness proof gives a separately repeatable bounded positive return waveform shared over the selected duration menu. No claim that it is the time reversal or inverse of the outward physical waveform is needed.

In the spectral representation every pure hold and every outward/return target is diagonal between the corresponding mode bases. Consequently all products telescope through those bases. A word starting and ending at A has scalar spectral coefficients

    (c V_A)_i (V_A^(-1)e1)_i,

which are static serial residues and independent of order. A word starting at A and ending at B has the C_i above, identical in the two orders. Reverse coefficients are also equal: interchange A and B in the equal-sum/product-ratio argument, or observe that forward C equality makes the endpoint-preserving A and B gauge scalings coincide label by label. The same argument handles words starting at B.

The exponential diagonal factors depend only on each matched pair and the chosen total A holds, B holds, and ramp duration multipliers. Thus the two physical models agree for every legal finite word in the fixed duration-menu interface, including repetitions and loops. These are readouts after complete operations; sub-ramp completion times or intermediate readouts are not included. The return remains a contracting positive physical flow. It is not the inverse of F.

## What this closes and what it does not

This closes the unresolved **existence** of a genuine four-stage positive shared-waveform ambiguity with unequal adjacent responses. It also defeats any uniform extension that merely adds a fixed finite list of stretched ramp durations, even with fixed return loops at those durations. It does not realize the old 2^-40 L target, prove historical novelty, recover literal chemistry, or provide a consequential physical experiment.

The construction is local near equal response and can have arbitrarily small identifying margins. The proof establishes exact nonidentifiability, not a useful estimation protocol or a finite-data lower bound. It does not contradict the known arbitrary-stage instantaneous-switch result: zero-duration switching lies outside the fixed positive-duration menu, and the two candidate targets cannot both extend to I at D=0 unless the mode gauges agree. It does not contradict reciprocal-volume generic nonresonance: the two blocks have equal products of response ratios, putting the swapped orders at the same W.

The initially attempted random and warm-start pulse optimizers failed. Their scripts/receipts are preserved as bounded negative evidence and are not used in this proof. The proof uses the exact residue branch and the independently checked local endpoint rank.
