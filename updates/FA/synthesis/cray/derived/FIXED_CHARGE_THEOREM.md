# Fixed-charge environment-uniform ground-energy comparison

Integration-derived research, 2026-10-13. This proof is an internal reconstruction,
not external review, formal verification, a priority claim, or a consequential
electronic-structure calculation. It extends the supplied CRAY comparison
argument to an explicitly stated Abelian charge contract. Standard CP-channel,
superselection, purification and SDP machinery is credited below.

## 1. Contract

Let finite-dimensional A and C carry nonnegative integer charge operators N_A
and N_C. Let h_0,h_1 be supplied Hermitian matrices on A tensor C satisfying

    [h_j, N_A tensor I + I tensor N_C] = 0.

Fix an integer Q >= 0. Define the admissible local space

    V_Q = direct_sum_{t<=Q} ker(N_A+N_C-t),
    D_Q = dim V_Q > 0.

The environment ranges over every finite Hilbert space R with a supplied-for-
that-instance nonnegative integer operator N_R, with arbitrary charge
multiplicities. We do not require negative charges. In particular, the universal
class allows a newly constructed R having any finitely many charge values
Q-t needed in the proof. K is any Hermitian matrix on C tensor R commuting with
N_C+N_R. Its norm, locality, signs and realistic material realization are
unrestricted. The total-Q sector must be nonempty.

Set

    H_j(K) = h_j tensor I_R + I_A tensor K,
    E_j^Q(K) = lambda_min(H_j(K) restricted to total charge Q),
    Delta_Q(K) = E_1^Q(K)-E_0^Q(K).

Changing the R charge-spectrum promise or fixing one particular R instead of
allowing all such R changes the converse problem. This theorem is not asserted
for an arbitrary preassigned R, a bounded-norm or geometrically local K class,
non-Abelian total-spin sectors, approximate charge conservation, or fermionic
locality without an independently justified finite tensor-product encoding.

## 2. The operation

Let M_N be the compact convex set of Heisenberg UCP maps Phi on B(A) with a
Schrodinger adjoint of the form

    Lambda(rho) = sum_alpha K_alpha rho K_alpha^dagger,
    sum_alpha K_alpha^dagger K_alpha = I,
    [K_alpha,N_A] = 0 for every alpha.

Equivalently Phi fixes every spectral projector P_q of N_A. The latter fact
follows in one direction from the Kraus expression; in the other direction,
the multiplicative-domain property of a fixed projector forces the map to
preserve each input/output charge block. This is stronger than covariance
under exp(i theta N_A); a covariant channel can exchange charge with its
discarded dilation environment.

Define

    L_Q(h_0,h_1) = max_{Phi in M_N}
        lambda_min_{V_Q}[h_1-(Phi tensor id_C)(h_0)].

Then

    inf_{R,N_R,K} Delta_Q(K) = L_Q(h_0,h_1),
    sup_{R,N_R,K} Delta_Q(K) = -L_Q(h_1,h_0).

The left endpoints are closure extrema. An R of dimension at most D_Q suffices
to approximate either endpoint to any positive accuracy. No environment state
or optimal comparison map is supplied to the operation.

## 3. Sufficiency

Every Kraus operator preserves the total-Q sector, and Phi tensor id fixes
I_A tensor K. On that sector the restricted map is UCP. Thus a residual bound

    h_1-Phi(h_0) >= c I on V_Q

implies H_1(K) >= Phi(H_0(K))+c I >= (E_0^Q(K)+c) I on the total-Q sector.
The residual restriction to V_Q suffices because nonnegative N_R implies local
charge at most Q. This proves Delta_Q(K)>=c.

Ordinary covariance is insufficient for this step: it preserves charge modes
on average but need not preserve a particular total-charge sector of a state.

## 4. Minimax and charge-compatible purification

Compact convex minimax gives

    L_Q = min_{rho supported on V_Q}
        { Tr(rho h_1) - min_{Phi in M_N} Tr[rho Phi(h_0)] }.

For every admissible Phi, both local operators in the objective commute with
N_A+N_C. Twirling rho by that charge leaves every objective unchanged. Choose
a minimizing rho commuting with N_A+N_C, and diagonalize it within local-charge
blocks:

    rho = sum_{t,k} p_{t,k} |v_{t,k}><v_{t,k}|,
    (N_A+N_C)|v_{t,k}> = t |v_{t,k}>.

Choose R with orthonormal vectors r_{t,k} having charge Q-t and put

    |psi> = sum_{t,k} sqrt(p_{t,k}) |v_{t,k}> |r_{t,k}>.

Then psi has total charge Q, purifies rho, and dim R <= D_Q. Put B=C tensor R
and sigma=Tr_A |psi><psi|. Its support S is invariant under N_B; write

    S = direct_sum_q S_{Q-q},
    sigma = direct_sum_q sigma_{Q-q}.

Its block ranks satisfy rank sigma_{Q-q} <= dim A_q. This block rank condition
is a consequence of the constructed pure state, not a supplied promise.

## 5. The grouped fixed-marginal reachability lemma

Every state omega on A tensor B with marginal sigma and supported in total
charge Q is obtained from psi by a channel with Kraus operators commuting with
N_A.

Proof. Purify omega as phi on A tensor B tensor E, assigning every basis vector
of the auxiliary E charge zero. Schmidt-decompose psi and phi against B using
the same charge-block eigenbasis of sigma. The Schmidt vectors of psi on A in
the sigma_{Q-q} block lie in A_q. The corresponding Schmidt vectors of phi lie
in A_q tensor E. The isometry between the Schmidt supports consequently
preserves every q. Extend it within each charge block to an isometry

    W = direct_sum_q W_q : A -> A tensor E.

Enlarge a neutral E if necessary. Its Kraus operators <e|W commute with N_A;
tracing E gives the required omega. Conversely every such channel preserves
the marginal and total-Q support. QED.

Therefore the inner minimization equals

    g_0(sigma) = min { Tr[(h_0 tensor I_R) omega] :
        omega >= 0, Tr_A omega=sigma, omega supported in total charge Q }.

This is the decisive distinction from merely asserting that an unrestricted
purification lemma remains valid after adding a superselection rule.

## 6. Conditional dual and a finite charge-conserving counterenvironment

Let V:S->B be inclusion. The relevant support of the conditional primal is

    W_Q = direct_sum_q A_q tensor S_{Q-q}.

Compress h_0 tensor I_R to W_Q, obtaining htilde_0. A strictly positive feasible
primal is the block-diagonal matrix

    omega_* = direct_sum_q (I_{A_q}/dim A_q) tensor sigma_{Q-q}.

The trace on A of each block equals sigma_{Q-q}. Unlike the ungraded product
I_A/d tensor sigma, this matrix lies in the required total-charge sector and
is positive definite on W_Q.

The conditional dual is

    g_0(sigma) = max_Z Tr(sigma Z),
    htilde_0 >= (I_A tensor Z) restricted to W_Q,
    Z = direct_sum_q Z_{Q-q} Hermitian on S.

Off-charge blocks of Z vanish under this compression and do not affect the
objective, so restricting to charge-preserving Z loses nothing. A sufficiently
negative scalar is strictly feasible. Finite-dimensional strict feasibility
gives equality and an attained dual optimum.

For B_0>=||h_0|| and eta>0, set

    K = -V Z V^dagger + M(I_B-VV^dagger),
    M >= B_0+B_0^2/eta.

Both terms commute with N_B. On total charge Q and support S, H_0(K)>=0. On
its orthogonal complement the diagonal block is >=M-B_0, and the off-diagonal
block has norm <=B_0. Completing the square gives E_0^Q(K)>=-eta. The total-Q
trial vector psi gives

    E_1^Q(K) <= Tr(rho h_1)-Tr(sigma Z)=L_Q.

Thus Delta_Q(K)<=L_Q+eta. Exchanging the pair proves the upper endpoint.

For a controlled finite-accuracy construction, choose nonnegative norm bounds
B_j>=||h_j|| and put S_0=B_0+B_1. If S_0=0 then both local Hamiltonians vanish,
Delta_Q(K)=0 for every compatible K, and the comparison is exact without
smoothing or a penalty construction. Otherwise, for any epsilon>0, set

    tau=min{1,epsilon/(4 S_0)},
    rho_tau=(1-tau)rho+tau I_{V_Q}/D_Q,
    eta=epsilon/2.

Every active charge block that occurs in V_Q then has its A-marginal eigenvalues
at least tau/D_Q. The nonzero spectrum of sigma is that of this A marginal.
The source dual-conditioning argument gives ||Z||<=2 B_0 D_Q/tau. Moreover,
convexity and |f|<=S_0 give f(rho_tau)<=L_Q+2 S_0 tau<=L_Q+epsilon/2.
Together with the penalty error eta this yields Delta_Q(K)<=L_Q+epsilon,
with polynomial energy scales in the local dimensions and 1/epsilon. This
establishes a finite constructive bound; the generic dual-extraction pipeline
has not been implemented here.

## 7. Explicit SDP and resource boundary

Use the source Choi convention C[(i,a),(j,b)]=Phi(|i><j|)[a,b], in an N_A
eigenbasis. In addition to C>=0 and Tr_input C=I, impose

    C=Pcal C Pcal,
    Pcal=sum_q P_q^T tensor P_q.

The residual inequality is checked only on V_Q. These are linear equalities
and two PSD constraints. If d_q=dim A_q, the Choi PSD block has dimension
m=sum_q d_q^2; the residual PSD block has dimension D_Q. Dense storage still
includes m^2 entries, plus the input matrices and image contraction.

For k spin-1/2 or occupancy variables, m=sum_q binom(k,q)^2=binom(2k,k), so
this symmetry restriction provides only a polynomial factor reduction of the
16^k Choi-entry growth. It does not establish efficient many-electron chemistry,
a small comparison radius, cheap Hamiltonian acquisition, or model accuracy.

## 8. Exact half-filled counterexample and sharp repaired interval

For the supplied four-spin motif

    h_0 = S0.S1+S0.S2+S1.S3,
    h_1 = 2 S0.S1+S0.S2+S1.S3,
    N_i=|down><down|_i,

the unrestricted theorem certifies Delta<=-0.22421. That conclusion does not
apply to minima restricted to total down-spin count Q=2.

Use no extra R and the common one-body collar Hamiltonian

    K_M = M(2 I-N_2-N_3).

It is charge conserving and local on the same two collar spins. In the Q=2
sector its zero-penalty subspace is the one-dimensional vector |up up down down>.
The compressed energies of h_0,h_1 on that vector are -1/4 and 0. Elsewhere
K_M>=M. Since ||h_1||<=3, a block bound gives

    E_1^2(K_M)>=-9/(M-3),  E_0^2(K_M)<=-1/4.

At M=100,

    Delta_2(K_100)>=1/4-9/97=61/388>0.

The independent exact script verifies the rational positive-definite shift
of the six-dimensional charge-two h_1+K matrix and the exact Rayleigh value
for h_0+K. Numerical diagonalization gives approximately +0.24997423865347;
the positive sign follows from the rational bound, not that decimal.

The charge-aware uniform interval is exactly [-3/4,+1/4] in closure for the
universal nonnegative-graded environment class at Q=2. Identity supplies these
perturbation bounds. To see optimality directly in the minimax formula:

* For the forward order, take rho=|singlet><singlet|_A tensor
  |up up><up up|_C. A charge-preserving channel stays in active charge one.
  The projected boundary term is (S0^z+S1^z)/2=0 on that block, and the minimum
  h_0 energy attainable there is -3/4. The trial h_1 energy is -3/2, so the
  minimax value is at most -3/4.
* For the reverse order, take rho=|up up down down><up up down down|. Active
  charge zero is one-dimensional, so every allowed channel fixes its state.
  The reverse objective is exactly -1/4.

These witnesses and the identity map prove L_Q(h_0,h_1)=-3/4 and
L_Q(h_1,h_0)=-1/4. The completeness theorem supplies finite approaching
environments. An explicit upper-endpoint family is K_M above. For the lower
endpoint one can add a charge-one R state, penalize C occupation and force that
R charge; the projected active charge-one singlet has energy change -3/4.

This compares different output tasks, not a nested uncertainty class: imposing
a fixed sector changes which eigenvalues define the energy. It is not evidence
that additional correct material information intrinsically worsens a bound.

## 9. Prior art and unresolved gates

Charge-preserving Kraus blocks are established strong-symmetry machinery, not
a new operation. For example, Moharramipour et al., PRX Quantum 5,040336 (2024),
arXiv:2406.08542, discusses strongly symmetric channels and sector steady
states. Cirstoiu et al., PRX 10,041035 (2020), distinguishes channel symmetry
from conservation. Alhambra et al., PRL123,190601 (2019), arXiv:1902.02357v2,
already develops local-energy CP optimization. Gour et al., Nat.Commun.9,5352
(2018), supplies channel comparison with symmetry constraints. The exact
paired-energy fixed-sector characterization and this particular counterexample
have not been priority-cleared.

Primary sources inspected for these boundaries:

* https://arxiv.org/html/1902.02357v2 : setting, Eq.(1), Theorem1 and SDP proof
  routes. This takes a state and Hamiltonian, unlike the new robust pair task.
* https://www.nature.com/articles/s41467-018-06261-7 : definition, channel
  ordering and symmetry context. No unproved import into the argument above.
* https://arxiv.org/html/1108.5930v1 : Theorem4.2.1 CP/LMI domination. Its bounded
  spectrahedron assumption does not automatically fit the unrestricted
  environment pencil. This prevents declaring an exact prior-art reduction
  without the missing assumption conversion.
* https://arxiv.org/abs/2406.08542 and
  https://doi.org/10.1103/PRXQuantum.5.040336 : strong-symmetry precedent.
* https://doi.org/10.1103/PhysRevX.10.041035 : symmetry/conservation distinction.

Next decisive gates: adversarial review of grouped reachability and conditional
dual; independent priority search in operator-algebra/quantum-comparison
literature; useful fixed-charge and realistic-environment restrictions with
affordable active dimensions; acquired model-error bounds; matched comparison
against strong bootstrap and correlated-electron methods on a supplied
scientific benchmark. The present theorem repairs an exact interface gap and
the counterexample prevents a false chemical transfer. It does not solve the
scientific capability gate.
