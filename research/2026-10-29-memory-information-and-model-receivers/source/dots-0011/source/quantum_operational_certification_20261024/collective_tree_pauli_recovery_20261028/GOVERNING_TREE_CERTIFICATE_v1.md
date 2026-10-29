# Acquired collective recovery certificate for a promised tree Pauli source

28 October2026. New scoped bridge and exploratory simulated fixture, independent review pending. This is NOT a new graphical-model learning algorithm or a generic correlated-noise theorem. It replaces the unacquired global identity-dominance premise by an executable local-data certificate within a supplied tree-Markov Pauli family. Original local-oracle counterexamples remain valid.

## 1. Source and full-CPTP comparator

Let n qubits undergo N_p(rho)=sum_x p(x) P_x rho P_x, x in {I,X,Y,Z}^n. The Pauli frame and a rooted tree are supplied. The actual error distribution is promised to factor as p(x)=p_r(x_r) product_(i->j) T_j(x_j|x_i). Zero conditional probabilities are allowed. The source is fixed and full calls reset independently. Trusted ordinary single-qubit Pauli preparation/readout is available. This does not acquire the tree promise or a quantum environment model.

For ANY CPTP recovery R, Pauli conjugation twirling preserves F_e(R N_p): N_p is Pauli covariant and Bell fidelity is invariant under identical input/output conjugations. The twirled R is a Pauli channel with some probability q(y), and F_e(R_twirl N_p)=sum_y q(y)p(y). Therefore

    max_R CPTP F_e(R N_p) = max_x p(x).

An optimum is the actual product-Pauli correction P_x. This is the conventional maximum-likelihood Pauli correction and a FULL collective n-qubit Bell objective, not the product of marginal fidelities. No code redundancy or high fidelity is automatically implied.

## 2. Actual ordinary measurements

Each full call independently chooses a_i uniformly from X,Y,Z and an input eigenvalue s_i uniformly from {-1,+1}; prepare the corresponding product state. Measure the same axis at output, giving b_i. Write y_i=s_i b_i. For a Pauli error e_i, y_i=chi_(a_i)(e_i), where chi is the usual four-symbol Pauli character table. The learner sees only (a,s,b), not e.

For every symbol e define Z_i(e)=[1+3 chi_(a_i)(e)y_i]/4. Then

    E Z_i(e)=p_i(e),   E[Z_i(e) Z_j(f)]=p_ij(e,f).

Each Z_i is 1 or -1/2. Its product with Z_j is 1,-1/2 or1/4. Thus both estimators lie in[-1/2,1]. Estimate all4n one-site and16(n-1) tree-edge probabilities from ONE common bank of N full calls. Correlations across estimates within a call are harmless. Hoeffding and a union bound give simultaneous additive error delta with failure at most

    2M exp[-2N delta^2/(9/4)],  M=4n+16(n-1).

Intersect each interval with[0,1]. The supplied process promise is not statistically established by this event. Drift/memory producing only averaged marginals is not silently a fixed tree distribution.

## 3. A genuinely division-free global score

Put c_i=number of children of node i. Define the common nonnegative factor

    D=product_i product_a p_i(a)^c_i,

and, for each word x, the polynomial score

    Q(x)=p_r(x_r) product_(i->j) p_ij(x_i,x_j)
                     product_i product_(a != x_i) p_i(a)^c_i.

For a strictly positive tree source, substitution of p_ij=p_i T_j gives Q(x)=D p(x). This remains true for EVERY tree source with zero probabilities by continuity: perturb root and each transition independently toward strictly positive distributions, and take the limit. Consequently sum_x Q(x)=D even at the boundary.

Use lower endpoints in every factor to form L(x), upper endpoints to form U(x). All factors are nonnegative, so on the simultaneous event L(x)<=Q(x)<=U(x) for every word. Generate ANY data-selected candidate xhat. Accept only when

    L(xhat) > max_(x != xhat) U(x).

This is sound without a supplied marginal/conditional probability floor. Indeed acceptance implies Q(xhat)>Q(x) for every alternative. Since L(xhat)>U(x)>=0, Q(xhat)>0, hence D=sum_x Q(x)>0. Dividing in the PROOF now establishes p(xhat)>p(x); the computation never divides by an unknown probability. Zero or tiny internal marginals may force abstention. This removes an input floor, NOT the statistical conditioning cost.

The score has known tree factors. Standard max-product dynamic programming computes its maximum and its maximum excluding xhat in O(n*4^2) arithmetic operations. Carry a Boolean state indicating whether any coordinate differs from xhat. Tree branches combine this flag by OR. Rational data and rational delta allow exact comparisons; products have bit length polynomial in n and log N. The delivered executable is a chain specialization. No exponential4^n enumeration or global witness oracle is used by its acquisition/guard.

The candidate proposal in the executable uses empirical positive ratios. This is not the certificate: any proposal would be valid, and only the division-free acceptance supports its floor-free conclusion. An additional ratio guard uses acquired positive one-site lower endpoints and may give sharper explicit probability bounds. Its positive-denominator prerequisite is checked, not supplied.

## 4. Executed correlated fixture and costs

The physical channel samples a four-state spatial Markov chain with root(7/10,1/10,1/10,1/10) and transition397/400 on the same symbol,1/400 on each other symbol. It then applies that Pauli word. This is strongly correlated and not a tensor-product channel. The retained state needed to generate the chain is four classical states; no such hidden state is supplied to the learner. Calls are reset independently.

Version3 uses n=8, N=2^22 full calls. The generator samples the exact rational source through uniform integer draws; no floating Born/CDF approximation is used. The learner uses only ordinary preparation/measurement records and saves their integer sufficient sums. The simulated PRNG run is exploratory, not laboratory acquisition or external preregistration.

With delta=1/400 the simultaneous Hoeffding failure upper is below2.186e-8, checked by an exact rational lower bound on the exponential series. The division-free candidate/competitor score ratio is2.3854756>1; the chosen correction is I^8. The separate acquired-ratio guard gives F_e>=.6290511. The source-informed diagnostic is .6640666. The same pipeline costs33,554,432 native qubit exposures, preparations and readouts, plus classical statistics and at most8 physical Pauli corrections per deployment. The nominal1,048,576-call version2 ratio guard passed but its division-free guard FAILED (ratio .80147); preserved rather than hidden. Version1 used floating categorical generation and is superseded by exact-integer versions2/3 for distribution fidelity.

There is no asserted asymptotic sample advantage. Near-tied modes or small internal marginal probabilities can demand arbitrarily many observations. Constant global fidelity in this fixture avoids presenting an exponentially tiny global fidelity as useful preservation. The optimum itself is still far from a high-fidelity memory.

## 5. Exact structure boundary

`exact_structure_boundary.py` constructs two strictly positive three-qubit Pauli distributions with IDENTICAL every one- and two-site marginal. The first is product, with one-site distributions

    (.46,.39,.08,.07), (.45,.40,.08,.07), (.44,.41,.08,.07).

The second subtracts(1/100)(-1)^(number of X symbols) on the {I,X}^3 cube and changes nothing elsewhere. All proper marginals are unchanged because the perturbation sums to zero on each coordinate. All one-qubit Bloch contractions are strictly positive. Yet the product source has unique global oracle III; the second has unique oracle IIX, with fidelity9487/100000 versus identity2027/25000 (gap1379/100000).

Therefore pairwise marginal acquisition cannot certify that the global source is tree-Markov. The second source violates the promise and defeats any inference that simply assumes the pairwise tree reconstruction is physically complete. In particular strict local positive-block oracles plus all pair data still do not imply a collective oracle without the structural assumption. Higher-order parity perturbations give the same obstruction to any fixed-order local-only data interface.

## 6. Relation to strongest conventional method and unresolved extension

Flammia and Wallman, *Efficient estimation of Pauli channels*, arXiv1907.12976v3, full primary HTML read28October2026, §I.1 and §VII: https://arxiv.org/html/1907.12976 . They already give polynomial-measurement reconstruction for known bounded-degree Markov fields with positive marginals and benchmarking noise assumptions. Standard graphical inference plus that learning is the strong comparator. The present direct trusted-SPAM, exact acceptance implementation is a qualified bridge to Astra's collective oracle obligation, not a replacement for or superiority claim over those methods.

The consequential missing extension is a realizable NON-Pauli or noncommuting-gauge family whose global recovery witness is locally acquirable, or an acquired global structure test that rules out hidden high-order correlations at an honest cost. This file does not solve either. The normal-cone machinery still needs global information unless its source family supplies a validated factorization.

Dependencies inspected: local_oracles_do_not_compose_collectively_20261028.md; qubit_extractor_oracle_normal_cone_20261028.md; Astra N1144 capsule at revision d6672151ce8e86d4af3e74b3b880abcdc82ae304 (source-transport correction noted; no scientific correction inferred). No received source changed.
