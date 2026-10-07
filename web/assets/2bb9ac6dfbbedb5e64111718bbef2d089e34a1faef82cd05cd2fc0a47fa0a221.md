# Quantitative finite-ensemble broadcasting implies classical reconstruction

Status: complete finite-dimensional candidate proof; the measurement, posterior, prefix, tree, arbitrary-prior and minimax interfaces passed independent adversarial checks by an agent and child, and the minimax contract was checked by broadcast_quantitative. The finite-label extraction uses established information-theoretic mechanisms, credited below. External correctness and historical priority remain open.

## Theorem

Let E={rho_1,...,rho_m}, m>=2, be any supplied finite ensemble on a finite-dimensional Hilbert space H. Suppose one CPTP channel B:H -> H tensor H reconstructs every input state in both output marginals with trace error at most epsilon. No actual unknown-label prior is supplied or used: design distributions below are auxiliary choices in an existence/minimax construction.

For every integer L>=0, there exists an EB reconstruction channel Lambda_L on H whose worst-label trace-distance error is at most

e_L <= L epsilon + sqrt(m ln(m)/(2*2^L)).

In particular, for 0<epsilon<=1, choose

L=max(0,ceil(log_2(m ln(m)/(2 epsilon^2)))).

For 0<epsilon<=1/2 the logarithm is positive, and

e(E) <= epsilon [ 2 log_2(1/epsilon) + log_2(m)
                         + log_2(ln(m)/2) + 2 ].

The right side can be capped at one, and m=1 is reconstructed exactly by constant preparation. At epsilon=0, the displayed infimum over L gives e(E)=0. This proof supplies a dimension-independent effective finite-label modulus without the ultraproduct machinery.

The binary proof in ../broadcast_quantitative/EXPLICIT_PAIR_BOUND.md is sharper: its special posterior identity gives e_pair<=L epsilon+sqrt(ln(2)/(2*2^L)), with no m prefactor. The present extension is conservative and does not claim optimal label dependence.

## 1. Iteration and adaptive information extraction

Iterate B as a binary tree of depth L, giving a legal CPTP channel C_L:H -> H^(tensor K), K=2^L. Each leaf marginal is a composition of L one-step marginal channels. Contractivity and the original per-state one-step guarantee telescope to

T(C_L(rho_x)_j,rho_x)<=L epsilon

for every label x and every leaf j. This argument does not require the intermediate perturbed states to belong to E.

Set Omega_x=C_L(rho_x). Give X any fixed design prior pi in the m-label simplex. We construct an adaptive sequence of two-outcome measurements on leaves Q_1,...,Q_K. At stage j, for each previous record h, let p_h be its unconditional probability, p_x(h)=P(X=x|h) its posterior, sigma_x^h the conditional state of Q_j, and

tau_h=sum_x p_x(h) sigma_x^h.

For a zero-probability record or label choose an arbitrary conditional state. Write d_x(h)=T(sigma_x^h,tau_h). Choose a label x_h attaining max_x p_x(h) d_x(h)^2, and measure the two-outcome spectral sign projector of sigma_(x_h)^h-tau_h. This measurement is computed from the known ensemble/channel and h; it has no dependence on the actual unknown label.

Let r_x^h be its output distribution conditional on label x, and r^h=sum_x p_x(h) r_x^h. Since r^h is the measurement distribution of tau_h, the selected measurement satisfies TV(r_(x_h)^h,r^h)=d_(x_h)(h). Classical Pinsker, using natural logarithms, gives conditional information gain

I_h(X:Y_j)=sum_x p_x(h) D(r_x^h||r^h)
          >=2 p_(x_h)(h) d_(x_h)(h)^2
          >=(2/m) sum_x p_x(h) d_x(h)^2
          >=(2/m) [sum_x p_x(h) d_x(h)]^2.

The last step is Jensen for the posterior probabilities. Let g_j=I(X:Y_j|H_(j-1)). The classical chain rule gives

sum_(j=1)^K g_j=I(X:Y_1,...,Y_K)<=H(pi)<=ln(m).

Choose one index j with g_j<=H(pi)/K. The entire adaptive sequence was used only to prove and select such an index; the actual reconstruction channel performs the prefix stages 1,...,j-1.

## 2. Legal prefix measurement and conditional-state preparation

Measure that prefix and, after outcome h, prepare tau_h on the selected leaf's output Hilbert space H. Let Lambda'_j be this measure-and-prepare channel on the joint output. Nonselective measurement of the other leaves leaves the original Q_j marginal unchanged. Thus for each label x, convexity of trace distance gives

T(Lambda'_j(Omega_x),Omega_(x,j))
 <= sum_h P(h|x) T(sigma_x^h,tau_h).

Averaging labels with the design prior and then using the conditional information inequality gives

sum_x pi_x T(Lambda'_j(Omega_x),Omega_(x,j))
 <= sum_h p_h sum_x p_x(h) d_x(h)
 <= sqrt( (m/2) sum_h p_h I_h(X:Y_j) )
= sqrt(m g_j/2) <= sqrt(m H(pi)/(2K)).

Composing the prefix instrument with C_L induces a genuine POVM on the original input H. The prepared tau_h are fixed from the known ensemble, design prior, channel and measured record, so Lambda_(L,pi)=Lambda'_j composed with C_L is one legal EB channel. Triangle inequality gives, for every pi, a channel satisfying

sum_x pi_x T(Lambda_(L,pi)(rho_x),rho_x)
 <=L epsilon+sqrt(m H(pi)/(2K))
 <=L epsilon+sqrt(m ln(m)/(2K)).

For the fixed finite input/output dimension, the set of EB channels is compact and convex (its normalized Choi states are separable). The loss

f(Lambda,pi)=sum_x pi_x T(Lambda(rho_x),rho_x)

is continuous and convex in Lambda and linear in pi. Sion's minimax theorem therefore gives

inf_(Lambda EB) max_x T(Lambda(rho_x),rho_x)
 =inf_Lambda sup_pi f(Lambda,pi)
 =sup_pi inf_Lambda f(Lambda,pi)
 <=L epsilon+sqrt(m ln(m)/(2K)).

The attained minimizer is one common channel for all labels, proving the worst-case statement. Unlike the uniform-prior direct channel, this sharper channel is supplied by minimax; its efficient acquisition is not proved. A direct uniform-prior construction would instead give the looser sqrt(m^3 ln(m)/(2K)) term.

A finite alphabet bound survives this step without introducing Hilbert dimension. Each prior-designed prefix decoder has at most N=2^(K-1) outcomes. The set of N-outcome EB channels is compact in the fixed finite input/output dimension, because its POVM effects and prepared states vary over compact sets. Their loss vectors form a compact set V in [0,1]^m. The same finite minimax argument gives a vector v in conv(V) with every coordinate at most the stated bound. Caratheodory's theorem represents v using at most m+1 vectors from V. Mixing those at most m+1 decoders produces an EB channel whose trace-distance losses are no larger than the corresponding averaged loss vector, by convexity, and whose alphabet has at most (m+1) 2^(K-1) outcomes. This huge but dimension-independent bound makes the apparatus interface explicit. The random choice of decoder may be made before the common C_L preprocessing, so the number of calls to B need not be multiplied by m+1.

## 3. A quantitative growing-entropy theorem

For an arbitrary family E_n, let b_n be its optimal two-broadcast worst marginal error and N_n(a) the cardinality of a trace-distance a-net selected from E_n. Apply the finite-ensemble theorem to such a net and extend by channel contraction. For every L>=0 and a>0 with m=N_n(a)>=2,

e_n <= 2a + L b_n + sqrt(m ln(m)/(2*2^L)).

An arbitrarily small channel slack suffices if the optimum is not attained. For b_n>0, the explicit choice above gives

e_n <= 2a + b_n [ 2 log_2(1/b_n) + log_2(m)
                             + log_2(ln(m)/2) + 2 ].

Therefore if b_n->0 and there is a_n->0 with

b_n log N_n(a_n)->0,

then e_n->0. This permits diverging covering entropy. It quantitatively weakens uniform total boundedness for the implication two-broadcast->EB. It does not replace the separate root-gap->EB mixture argument with an effective intrinsic-gap rate.

Once EB reconstruction holds, a single classical record broadcasts to any prescribed number K_n of receivers with the same marginal error bound, as in GENERAL_CRITERION.md. The joint outputs may be correlated.

## Costs and scope

The prior-average extraction is constructive given exact full joint output matrices and spectral/conditional-state operations; the sharper worst-case version adds an existence/minimax step. It does not establish efficient acquisition or implementation. Each C_L uses 2^L-1 calls to B and has 2^L output systems; the explicit sharper choice is of order m ln(m)/epsilon^2. The adaptive prefix has at most 2^(j-1) records and can be enormous. Computing the small-gain index, all posteriors and preparations may require exponentially large joint data. The minimax channel may require combining or acquiring channels for many design priors. These costs are explicit resources rather than hidden access to the unknown input label.

The proof preserves marginal states on the supplied finite ensemble; it does not preserve arbitrary external entanglement, approximate B in diamond norm, recover every state in an unpromised Hilbert space, or create independent copies. The logarithmic rate and m extraction prefactor are not asserted optimal.

Source provenance: classical Pinsker, Shannon chain rule, binary Helstrom measurements, Sion minimax and Caratheodory are established. The adaptive low-information measured-conditioning mechanism is explicitly prior art: Brandao, Piani and Horodecki, Generic emergence of classical features in quantum Darwinism, https://arxiv.org/pdf/1310.8640v1 , p10 Eqs28-30 (v2 AppendixA pp17-18 Eqs32-34); Li and Smith, Quantum de Finetti theorem under fully-one-way adaptive measurements, https://arxiv.org/pdf/1408.6829 , Lemma3; Qi and Ranard, Emergent classicality in general multipartite states and channels, https://arxiv.org/pdf/2001.01507 , Proposition1. The binary constant in ../broadcast_quantitative/EXPLICIT_PAIR_BOUND.md is a direct finite-label specialization of those contracts, composed with a broadcasting tree. This explicit proof is an operational corollary of known conditioning machinery, not a new information-extraction principle. The present selected-label/minimax bookkeeping gives the displayed general-m bound; its optimization is not a priority claim. The direct source collision and exact specialization are audited in ../broadcast_prior_art/FINITE_ENTROPY_ADDENDUM.md. Exact broadcasting/classical-sufficiency and the root-gap statistic are prior art listed in ../broadcast_prior_art/AUDIT.md. The full intrinsic-gap experiment equivalence and all historical priority claims require external review.
