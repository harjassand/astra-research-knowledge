# Independent review: pure stationary completion and rate-independent activity
31 October 2026. Independent mathematical review (internal).

## 1. Source binding and verdict

I read the complete local source general_markov_noise_completion_20261031/PURE_STATIONARY_COMPLETION_AND_ACTIVITY_BOUND.md, 6,417 bytes, SHA-256 e5bd50e302be281314e030c61a1cba8463223a2f8c71125e4fd7192fc3e716bf. The source labels itself unreviewed; this receipt is separate and does not alter those bytes.

Verdict: PASS as a finite-dimensional structural representation and source-conditioned jump-activity theorem, with the explicit notation correction below. This is not a general efficient simulator, a recovered source, an implementation, or an originality certificate.

Binding correction: the displayed C_xx=2 lambda sum_y q_xy in Section 2 must mean 2 lambda sum_{y != x}q_xy. The unrestricted row sum of Q is zero. The proof and all subsequent conclusions use the exit-rate sum, not that unrestricted sum.

Assumptions retained: finite irreducible row generator Q; positive known stationary probability pi; lambda>0; finite bounded Hermitian system couplings through real diagonal source functions; initial reservoir exactly psi=sum sqrt(pi_x)|x>, independent of the system and its reference; system-only controls, with private reservoir and its jump records not revealed. Uniform activity bounds are unconditional and retain consumer outcome registers. Source preparation, stationary-law acquisition and a usable gap certificate are not free.

## 2. Exact completion, including the nonreversible sign

Write r_xy=sqrt(pi_x/pi_y). Each edge jump is sqrt(lambda q_xy)|y>(<x|-r_xy<y|), so it annihilates psi exactly.

For x != z, a_xz=q_zx sqrt(pi_z/pi_x), b_xz=q_xz sqrt(pi_x/pi_z). Interchanging x and z swaps a and b, so H_xz=i lambda(a_xz-b_xz)/2 is Hermitian. Its x component on psi is
(i lambda/2)[(sum_{z != x}q_zx pi_z)/sqrt(pi_x) - sqrt(pi_x)sum_{z != x}q_xz]=0
by stationarity. Thus H psi=0, not merely an unspecified eigenvalue.

For diagonal F, direct edgewise multiplication gives C_xz=-lambda(a+b) and
(D^dagger F)_xz=lambda(b-a)(f_x-f_z)/2.
Meanwhile i[H,F]_xz=lambda(a-b)(f_x-f_z)/2, which cancels it. Diagonal entries are lambda sum_{y != x}q_xy(f_y-f_x). Incoming stationary flow supplies the second exit-rate contribution to C_xx. Hence the claimed diagonal restriction is exact even without detailed balance. No approximation in lambda or reversibility was introduced.

The pure state P=|psi><psi| is stationary by the ordinary dark-state criterion. A nonreversible H_env is essential for this particular formula; dropping it would generally leave off-diagonal observable terms.

## 3. Full controlled process, not just one-time marginal agreement

The joint Heisenberg algebra consists of sum_x O_x tensor |x><x|, including arbitrary operators on retained reference and control registers. The environmental generator maps it by the classical row generator; the diagonal coupling contributes i[A(x),O_x] in each block. H0 acts within every block. This is precisely the finite classical Markov-noise backward generator.

The initial pure reservoir functional on this algebra equals sum_x pi_x O_x. Equality of these generators and initial functionals therefore gives equality for every finite controlled experiment obtained by interleaving the evolutions with system/reference-only instrument maps. Each branch map preserves the algebra; summing branches while retaining their classical labels establishes the unconditional process identity. The reservoir need not be measured, diagonal in its own density matrix, or reset at controls.

This does not identify the displayed Lindblad jump record with the classical Q-chain jumps. Indeed the activity reduction concerns a different, unobserved unraveling. Nor does it license revealing that record, interacting directly with the reservoir, or normalizing a rare consumer postselection while retaining the same error/count guarantee.

## 4. Gap and source costs

The exact quadratic form is
<v,C0 v>=sum_{x -> y}q_xy |v_x-sqrt(pi_x/pi_y)v_y|^2.
Its kernel is span(psi): irreducibility forces v_x/sqrt(pi_x) to be constant along the connected directed graph. In finite dimension this gives a strictly positive smallest eigenvalue on psi-perpendicular.

More specifically, with D_pi=diag(pi) and S=D_pi^(-1/2) Q^T D_pi^(1/2), the no-jump reservoir generator is lambda S and C0=-(S+S^dagger). Thus the relevant c is an additive-reversibilization/Dirichlet-form gap. It must not be replaced without proof by the real-part eigenvalue gap of a nonnormal Q. A certified lower bound on c, rather than an unpriced spectral oracle, is part of the input-cost ledger. Both c^-1 and pi_min^-1 may be large.

An optional mathematical consequence, not needed for the activity bound, is uniqueness of the uncoupled reservoir stationary state: L_env^dagger P=R>=pi_min C, so any stationary density has zero C expectation and is supported on psi. This does not supply efficient state preparation.

## 5. Tilted inequality and count constants

For kappa=e^theta-1 and a_theta=e^theta pi_min-kappa>0 choose delta=2 kappa/a_theta, V=I+delta Pperp. Since every jump lands in |y>,
R=sum L^dagger P L=sum pi_y L^dagger L>=pi_min C.
The tilted dissipator is exactly
D_theta^dagger V=kappa(1+delta)C-e^theta delta R.
Its scalar upper coefficient is kappa-delta a_theta=-kappa. Hence it is at most -lambda kappa c Pperp.

The environmental and system-only Hamiltonians commute with V. Only sqrt(lambda)K contributes off-diagonal ground/excited blocks, of norm at most delta sqrt(lambda)B0. For vectors (u,v) in those blocks, the cross term is bounded by
2 delta sqrt(lambda)B0 ||u|| ||v|| -lambda kappa c ||v||^2
<=delta^2 B0^2/(kappa c) ||u||^2.
Consequently the full tilted adjoint is at most [4 kappa B0^2/(c a_theta^2)]P, and in particular at most the stated constant times V. No commuting system-operator assumption is used.

The positive tilted evolution gives E exp(theta N_T)<=exp[4 T kappa B0^2/(c a_theta^2)], because V>=I and the initial V expectation is one. Finite dimension ensures finite-time count exponential moments for fixed lambda; alternatively positive truncation yields the same argument. Dividing the bound minus one by theta and taking theta down to zero proves the mean bound without differentiating an uncontrolled estimate.

At theta=pi_min/4, kappa<=pi_min/3 and a_theta>=2 pi_min/3. Chernoff therefore gives the written tail with threshold 12 B0^2 T/(c pi_min^2) and slope pi_min/4. The constants are conservative but valid.

For noncentered A(x), B0^2 is the norm of sum pi_x A(x)^2 - (sum pi_x A(x))^2, equivalently sum pi_x(A(x)-mean A)^2, also for noncommuting A(x). The deterministic mean term can be moved into H0 but may then scale as sqrt(lambda); its simulation cost is not removed by the activity bound.

System-only CPTP controls fix I_system tensor V in the adjoint, including adaptive controlled maps on retained records. Thus the same Gronwall bound survives such controls. Neither a pointwise intensity bound nor a Poisson-thinning construction follows.

## 6. What remains genuinely open computationally

Small observed jump count does not bound the cost of the no-jump maps or their coherent Kraus-time preparation. Although lambda S is a positive similarity transform of Q^T before coupling, its virtual classical paths may still make order lambda T transitions. General source matrices do not have the independent two-state tensor factorization used in the earlier telegraph compiler. The added diagonal, operator-valued system coupling is noncommuting across source states. No efficient bridge, normalization, complete-instrument block encoding, or finite-bit general-source construction is established here.

This theorem also does not solve the cost of learning pi, preparing psi, estimating c, or describing an exponentially large source state space. It therefore does not fast-forward an arbitrary unknown Markov chain. Its useful exact delta is a representation with a source-conditioned, lambda-independent activity estimate, not a whole simulation-complexity theorem.

## 7. Primary-source comparison and originality boundary

Invariant commutative-algebra restrictions and quantum extensions of classical dynamics are established frameworks. Bardet's quantum-extension paper explicitly treats subclassical maps, discrete-state extensions and continuous-time constructions under stated hypotheses. I inspected its extension and invariant-algebra sections; they are relevant ordinary comparators, not a proof that the present exact edge formula or activity inequality has already appeared. [Bardet, Quantum extensions of dynamical systems and of Markov semigroups](https://arxiv.org/html/1509.04849).

Dark-state characterization is likewise established: Kraus and collaborators characterize pure stationary states and their dark-state representation. I read the corresponding theorem and criterion. The step “all jumps annihilate psi and H psi=0 implies stationary” should be credited as standard, not a new result. [Kraus et al., Preparation of Entangled States by Quantum Markov Processes](https://arxiv.org/html/0803.1463).

The combination of a classical-semigroup extension with a pure invariant quantum state also predates this candidate. Fagnola, Kumar and Srivastava construct a quantum Laguerre extension with a unique pure invariant state and convergence results. I inspected the publisher's accessible primary PDF introduction and statement of scope. This is a different continuous-state model, but rules out presenting that conceptual combination as unprecedented. [A quantum Laguerre semigroup, 2021](https://insa.nic.in/writereaddata/UpLoadedFiles/IJPAM/Vol52_2021_4_ART21.pdf).

The carré-du-champ quadratic form, stationary similarity transform, additive reversibilization, tilted-generator exponential moment technique and completing-square estimate are ordinary ingredients. The inspected sources did not establish the exact arbitrary finite nonreversible formula together with the particular controlled activity bound written here. This limited search is not a priority certificate or an exhaustive novelty finding. Existing denied full-text restrictions were respected; no alternate-copy bypass, outreach or external transfer was used.

## 8. Final scope

Accepted, source-bound and with the exit-rate notation correction: exact finite Markov-source completion, pure stationary reservoir, controlled noncommuting system-process equivalence, and the stated source-conditioned activity bounds. Not accepted by implication: a general-source efficient compiler, cheap preparation/gap acquisition, polynomial source-condition dependence in arbitrary succinct models, arbitrary postselected guarantees, or a novelty claim. The earlier many-mode telegraph theorem and its source bytes are unchanged.
