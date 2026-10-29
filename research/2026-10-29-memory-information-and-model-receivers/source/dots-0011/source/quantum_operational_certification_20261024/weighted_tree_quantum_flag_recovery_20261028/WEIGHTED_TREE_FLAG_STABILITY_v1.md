# Probability-weighted tree acquisition with noncommuting root flags

28 October2026. New derivation, independent review pending. The weighted-row idea was contributed by the independent tree-certificate reviewer; this source requires a different receiving reviewer for that new lemma. It is a second acquisition route to the exact finite-feature quantum recovery reduction, distinct from label-observed training. No numerical/hardware advantage is claimed.

## 1. Source and target

The full n-qubit channel is N(rho)=sum_x p(x) P_x rho P_x tensor tau_(x_r), with a supplied rooted tree, unknown tree-Markov Pauli distribution p, and arbitrary unknown qubit root-flag states tau_a, a=I,X,Y,Z. Zero marginal/transition probabilities and rank-deficient noncommuting flags are allowed. The Pauli frame, tree structure, root-feature dependence and source reset/stationarity are promises, not inferred from local records. All n logical payloads are retained; no redundant encoder is introduced.

As proved in the separate label-observed manuscript by Kraus/Pauli orthogonality, every full CPTP recovery is equivalent at global Bell fidelity to a gauge POVM followed by a Pauli correction. For each root feature a, only a maximum-probability word x*_a needs be returned. The global oracle is discrimination of the four unnormalized states m_a tau_a, m_a=max_(x:x_r=a) p(x). The present aim is APPROXIMATE oracle recovery without any marginal floor or exact-mode gap, not exact identification of x*_a.

## 2. Acquire unnormalized local objects

Ordinary independent product Pauli eigenstate inputs and matching data readouts provide the estimators Z_i(a)=[1+3 chi_(axis_i)(a) input_sign_i output_sign_i]/4 from the tree-certificate source. Their products give the edge marginals J_ij(a,b)=p_ij(a,b). Independently choose a flag-Pauli axis k and outcome c, and define the usual single-qubit shadow G=(I+3c sigma_k)/2. Then

    E[Z_r(a) G]=sigma_a=p_r(a) tau_a.

Logical-root and gauge measurements commute, and their random axes are independent. The learner uses actual preparation/readout records, not error labels or a supplied state. Finite concentration can bound each Hermitian raw matrix estimate sigmahat_a and each raw edge table Jhat_ij. No conditional flag state is divided by p_r(a).

Set A_a=(sigmahat_a)_+ by positive spectral clipping, and B_ij(a,b)=max(0,Jhat_ij(a,b)). These are known mathematical fitting objects. They are not asserted to be mutually consistent true marginals.

## 3. Normalize only after weighting: no supplied floor

Let sigma_a>=0 and trace sum_a sigma_a=1. Write epsilon_root=sum_a ||A_a-sigma_a||_1 and Z=sum_a Tr A_a. If Z>0 define the approximate ROOT CQ STATE as sum_a |a><a| tensor A_a/Z. Then

    || sum_a |a><a| tensor sigma_a - sum_a |a><a| tensor A_a/Z ||_1
      <= sum_a ||sigma_a-A_a||_1 + |1-Z|
      <= 2 epsilon_root.

If Z=0, use any fixed normalized root CQ fallback. Then epsilon_root=1 and the same bound2 remains valid. Individual zero feature weights require no special division. Write q_r(a)=Tr A_a/Z and tauhat_a=A_a/Tr A_a only as a conceptual description when that trace is positive; zero-weight flags may be arbitrary.

For an edge i->j let its true row be J_a=p_i(a)T_j(.|a), and let B_a>=0 be the fitted row. Normalize it to That_j(.|a)=B_a/s_a when s_a=sum B_a>0; choose any fixed probability row when s_a=0. For EVERY row,

    p_i(a) ||T_j(.|a)-That_j(.|a)||_1
      <= ||J_a-B_a||_1 + |p_i(a)-s_a|
      <= 2 ||J_a-B_a||_1.

For s_a=0 this follows directly from the upper bound2p_i(a). Therefore no rare-parent division enters the GLOBAL error bound, despite a division used to synthesize a probability row. A row with almost zero mass can be poorly estimated without receiving unearned large importance.

## 4. Global quantum/classical assembly

Use the fitted root CQ state and fitted conditional rows to generate

    Gammahat=sum_x q(x) |x><x| tensor tauhat_(x_r).

The actual state is Gamma=sum_x p(x)|x><x| tensor tau_(x_r). Replace the conditional edges in reverse topological order, leaves toward root. When changing a given edge, every upstream edge is still the true one, so its parent marginal is exactly p_i. Previously changed descendant maps are stochastic CPTP postprocessings and cannot enlarge trace distance. The flag may be noncommuting but is only carried along; each branch's flag trace is its classical probability. Summing edge changes and replacing the root CQ state last proves

    (1/2)||Gamma-Gammahat||_1
       <= epsilon_root + sum_edges ||J_ij-B_ij||_1.        (A)

This is a trace-distance statement about the whole classical error record AND quantum flag, not a comparison of unrelated local marginals.

A fixed controlled-Pauli construction maps Gamma to N, so its channel half-diamond distance from Nhat is at most the left side of(A). In fact equality holds: a complete logical Bell input tags every Pauli error by an orthogonal Bell vector, retaining the same quantum-flag block trace norms. Thus the finite sufficient cq representation, not the microscopic environment, controls the full source channel at this promised scope.

Let Rhat be an eta-optimal physically implemented recovery for Nhat. Bell fidelity changes by at most source half-diamond distance under any fixed CPTP recovery. Consequently

    max_R F_e(R N)-F_e(Rhat N)
       <= 2 epsilon_root + 2 sum_edges ||J_ij-B_ij||_1 + eta.  (B)

No exact-mode separation, minimum marginal probability or gauge eigenvalue is required for approximate performance. A loose right side can of course be vacuous.

## 5. Efficient actual fitted decoder

The fitted distribution is a tree by construction. For each root value a, ordinary max-product dynamic programming finds the conditional most-likely word and its probability w_a under the fitted transition rows. The four discrimination coefficients are

    C_a=w_a A_a/Z,

with C_a=0 for zero A_a. This formula does not divide by a rare root probability. The known four-outcome qubit-POVM SDP maximizes sum_a Tr(M_a C_a), M_a>=0,sum M_a=I. A finite primal/dual certificate and a paid physical POVM compilation give eta. Return the conditional MAP Pauli word selected by the flag outcome. Classical tree inference is O(n*4^2); gauge optimization has fixed matrix dimension. Generic finite POVM synthesis, precision, readout, conditional gates and control error remain paid operations, not an unknown-source recovery oracle.

## 6. From raw errors to honest cost

PSD clipping is NOT silently trace-norm contractive for noncommuting matrices. For Hermitian sigmahat and true sigma>=0,

    ||(sigmahat)_+-sigma||_1 <=2||sigmahat-sigma||_1,

because Tr(sigmahat)_-<=||sigmahat-sigma||_1 and the triangle inequality applies. Elementwise clipping of a nonnegative classical table does not enlarge its entrywise error. Thus if four raw root matrices have trace errors at most e and every edge entry has error at most delta,

    regret <=16e +32(n-1)delta +eta.

Joint ordinary data can make these errors O(sqrt(log(n/beta)/N)) at fixed local/gauge dimension, giving a finite polynomial N=O(n^2 epsilon^-2 log(n/beta)) sufficient for additive epsilon regret. Constants can be large. This is not a uniform constant-fidelity/noisy-hardware advantage or a claim that tree structure is acquired.

This mechanism explicitly resolves a weakness of the earlier exact polynomial mode certificate: that certificate may abstain near zero marginal probabilities, whereas approximate recovery only charges their probability-weighted contribution. The exact certificate and this approximate theorem have different conclusions and neither supersedes the other's actual scope.

## 7. Conventional comparison and limitations

Known Markov-field Pauli learning, ordinary tree inference and quantum state discrimination are the conventional ingredients. The new local synthesis is the complete weighted root-CQ/edge error composition and its physical recovery consumer with noncommuting flags. Strong conventional methods can use the identical information and construction. No historical-priority or complexity separation claim follows.

The exact pair-indistinguishability counterexample in the collective-tree package still defeats any attempt to infer the global tree promise from local records. Nor does this theorem handle flags depending on the entire error word through unknown quantum correlations, arbitrary returning bath memory, unknown coherent noise, or an unacquired Pauli frame.
