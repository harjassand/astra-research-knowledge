# What collective common-frame programmes do, and do not, add

30 October 2026. Mathematical constructions and access-class lower bounds.
No quantum source, controller, optimizer, or new model instance is executed.
All traces and Choi states below are normalized unless stated otherwise.

The native memoryless source is

    N_U(x)=U(x tensor I_r/r)U*,  U:C^k tensor C^r -> C^D,
    U*U=I,  k>=2, D>=kr.                                      (1)

The target is a deterministic decoder for an independently supplied native
payload, including an arbitrary reference. Its error e is HALF diamond
distance from the logical identity, after composition with (1). Programme
acquisition in the classes treated here is independent of that payload.
The decoder can process the entire programme jointly with the payload.
This qualification is essential: payload-correlated future source queries
are not reduced to a calibration programme by the arguments below.

## 1. The whole reflection bank is an iid-Choi output

Let J_U=(id tensor N_U)(Phi_k). It has rank r. The random-purification
channel of Yoshida et al., arXiv:2512.21260v2 Theorem 2, gives the exact
CPTP transformation

    J_U^tensor Q -> E_V [ |Psi_V><Psi_V|^tensor Q ],
    |Psi_V>=(I tensor V)|Phi_k>,                              (2)

where V:C^k->C^r tensor C^D is ONE Haar-random Stinespring frame of N_U.
There is no frame label. To verify the state/channel normalization, every
purification of J_U has reference marginal I_k/k. Reshaping it as the
normalized Choi vector of V therefore gives V*V=I. The Haar distributions
in (2) agree with the primary definitions (23)--(24).

Fix a PUBLIC isometry V0 into the same output. The pure-state conditional
sample channel used in the primary Lemma 6 maps, pointwise in V,

    |Psi_V><Psi_V|^tensor Q
       -> E_theta [ |Psi_(Ftheta)><Psi_(Ftheta)|^tensor Q ],
    Ftheta=(exp(i theta)|0>V0+|1>V)/sqrt(2).                  (3)

The SAME V and SAME theta occur in all Q factors. One direct finite
realization of (3) is useful. Draw w~Bin(Q,1/2), using Q fair bits; keep
w unknown samples, add Q-w copies of the known sample, and coherently
shuffle the flagged samples uniformly into all subsets of size w. A
uniform-subset state is a known Dicke state. Controlled permutations and
uncomputation of the subset index using the output flags produce

    binom(Q,w)^(-1/2) sum_(|S|=w)
       (|1>Psi_V)_S (|0>Psi_V0)_(S^c).

Its mixture with weights binom(Q,w)/2^Q is precisely (3): integrating
theta removes cross terms only between different w. No continuous phase
oracle is required. The known subset preparation/permutations have
polynomial(Q, log(k r D)) gate cost at a declared accuracy; only the
primary random-purification channel remains as an imported primitive.

Finally trace all Q logical Choi references. This proves the exact channel

    J_U^tensor Q -> B_Q(U):=E_(V,theta)[(P_(V,theta)/k)^tensor Q],
    P_(V,theta)=Ftheta Ftheta*.                             (4)

It uses EXACTLY Q iid Choi copies. In particular it does not replace the
joint bank by a product of separately averaged programmes. It reveals
neither V nor theta. It is a deterministic state-channel conversion,
not a postselected retrieval of an open unknown channel.

This conversion itself holds for ANY CPTP source with a known Kraus-rank
bound r: its Choi reference marginal is still I_k/k. Flatness is used by
the lower bound below, not by the bank-conversion channel.

**Consequence.** Every joint processor of the specified bank (4) and an
independent native payload, with NO further original-source calls, has
an iid-Choi implementation with Q copies
and the identical input/output channel. No restriction to independent
reflection synthesis, DME, a particular amplitude-amplification circuit,
or a product measurement is involved. Section 4 gives the required
fixed-k iid-Choi lower bound, including k=2.

This closes a real possible shortcut: changing only the downstream use
of (4) cannot remove its quadratic-rank copy obstruction. It does not
exclude stronger *open* RDS inputs or payload-dependent source histories.

## 2. Retaining public factory workspace is not automatically extra access

Here is an exact general extension lemma. Suppose a known parallel-query
preprocessor prepares omega_(A,E), independent of U and of the incoming
payload, with A=(C^k)^tensor Q and

    omega_A=I_A/d,  d=k^Q.

There exists a KNOWN CPTP map L:R->E such that

    omega_(A,E)=(id_A tensor L)(Phi_d).                    (5)

Indeed d omega is the unnormalized Choi matrix of L (with the reference
ordering fixed by Phi_d); positivity and the displayed marginal are
exactly complete positivity and trace preservation. Applying N_U^tensor Q
to A in (5) proves that the WHOLE post-query state, including E and any
public measurement records retained later, is a CPTP output of J_U^tensor Q.
All known postprocessing can be appended. A copy lower bound permits
unrestricted known processing; it does not require an efficient classical
description of L for this inference.

This covers the literal RDS Theorem 3 / Fig. 2(a) factory with maximally
mixed external logical input, including the choice retaining its known
Bell purification. The only source-input operation before N^tensor Q is
the controlled permutation transpose

    sum_sigma |sigma><sigma| tensor pi(sigma)^T.

Tracing its control gives a permutation average of I/d, hence I/d. The
figure was visually read in the primary page 7 image already acquired in
ROOT25; the source queries really precede QFT, the lambda measurement and
the inverse small Schur transform. Retaining that measurement record or
the controlled-permutation workspace does not evade (5).

This paragraph is a statement about that literal source preprocessor,
not a claim that *every* conditionalisation factory's discarded workspace
has been characterized. Equation (4) independently covers its specified
output bank without any workspace assumption.

A uniform query marginal by itself is NOT enough if its extension is
unknown and correlated with the U-dependent payload or earlier source
outputs. Then (5) need not have a U-independent known L. The preceding
lemma explicitly supplies the entire prestate as known and independent
of U and the incoming payload; it is not an adaptive-query reduction.

More generally let rho_A be the actual known query-input marginal of an
arbitrary offline parallel calibration strategy and put

    chi=d ||rho_A||_op,  1<=chi<=d.                       (6)

Purify the known prestate as sum_a |a>_A |v_a>_E and define T|a>=|v_a>.
Then ||T||^2=||rho_A||. Applying T/sqrt(||rho_A||) to the reference of
Phi_d succeeds with probability 1/chi and produces that known prestate.
The same filter on the reference of J_U^tensor Q produces its whole
post-query state with that same U-independent probability. Tracing any
purifying workspace handles mixed prestates. Repeating on disjoint Q-copy
blocks, or using a finite cap, therefore costs at most

    Q ceil(chi/delta) iid Choi copies                     (7)

for programme error at most delta. This is a COPY-count reduction with
arbitrary known filters allowed, not a polynomial gate claim for an
arbitrarily succinctly specified probe. On failure output a fixed state.
The exact marginal chi=1 case has success one and needs only Q copies.

Combining (7) with Section 4 yields a necessary *spectral concentration*
of the actual source-query input for any subquadratic-rank offline
parallel calibration: Q chi must be Omega(r^2), for fixed useful error
and fixed delta. Thus a state-space reduction or coherent common frame
alone does not pay the missing input resource.

## 3. A common-frame simulation for bounded entangled input blocks

There is a stronger reduction for a different large class. Consider the
open joint RDS resource E_V[Ad(V)^tensor Q] (or its conditional Ftheta
version), fed a product of KNOWN pure probes

    tensor_(i=1)^s |psi_i>_(R_i,A_i),
    A_i=(C^k)^tensor m_i, sum_i m_i=Q, m_i<=b.             (8)

Retained references belong to their respective blocks. Arbitrary known
joint processing of all output blocks is permitted. Shared classical
randomisation is also permitted by conditioning on its known label.
Entanglement between retained references in different blocks, an unknown
payload used to prepare the probes, and adaptive open RDS slots are NOT
assumptions of (8).

### 3.1 A gate-paid construction using only the known probe preparations

Acquire M iid J_U copies and apply (2) ONCE. If needed apply (3) ONCE
with M in place of Q. Conditional on the unknown common frame W=V or
Ftheta, the resource is |Psi_W>^tensor M.

For a block of size m put d_i=k^m. Prepare a fresh copy of the supplied
known |psi_i>_(R_i,A_i), and project A_i together with the references of
m fresh common-frame Choi samples onto Phi_(d_i). Elementary normalized
teleportation gives the exact successful vector

    (1/d_i) (id_(R_i) tensor W^tensor m)|psi_i>.          (9)

Success probability is p_i=d_i^(-2), INDEPENDENT of W. No correction by
an unknown W, adjoint W*, controlled W, or external amplitude oracle is
used. Bell projection has O(m log k) known gates/measurements. Every failed
trial discards its m samples and its prepared probe; it does not collapse
or consume a previously accepted block. Every trial's known probe
preparation, temporary reference space, routing and measurement is paid.

Retry blocks using a common queue of fresh samples. Given W, trial
successes are independent with these fixed probabilities. In particular
neither the binary failure record nor the stopping count changes the
posterior distribution of W. For the ideal unlimited queue, let G_i be
the geometric number of trials for block i. The total sample use T has

    E T=sum_i m_i d_i^2 <= Q k^(2b)=:S_Bell.             (10)

Choose M=ceil(S_Bell/delta). Abort to a fixed known output if the queue
cannot finish. Coupling to the unlimited queue and Markov give

    Pr[abort]<=Pr[T>M]<=S_Bell/M<=delta.                 (11)

The abort event is frame-independent. Conditioned on completion, the
accepted programme is EXACTLY the required common-frame joint output of
(8). All failed trials are discarded. Thus the implemented output has
half trace distance at most delta from it, including all retained probe
references. Appending a fixed joint decoder and arbitrary native payload
turns this into at most delta HALF diamond error.

This is a finite capped physical state-channel construction; an expected
runtime with a hypothetical infinite common-frame reservoir is not being
silently executed. All M source calls and the one M-copy purification
occur in advance. The subsequent queue is known postprocessing.

### 3.2 A stronger copy-count bound if arbitrary known matrix filters are allowed

Write |psi_i>=sum_a |a>_(A_i)|v_a>_(R_i) and set
T_i|a>=|v_a>. Its Frobenius norm is one, so ||T_i||<=1.
The success operator T_i applied directly to the Choi reference produces

    d_i^(-1/2)(id tensor W^tensor m_i)|psi_i>,           (12)

with probability 1/d_i, again frame-independent. Consequently the same
queue proof has

    S_matrix=sum_i m_i d_i<=Q k^b,
    M=ceil(S_matrix/delta).                             (13)

No inverse singular-value promise is needed to define T_i. It is a
contraction of a known finite matrix. Its generic unitary dilation exists
and can be approximated; acquiring its entire matrix from an arbitrary
succinct circuit may be expensive. That known computation is NOT free in
the gate-paid port (9), which needs only the original probe preparation.
For a copy LOWER bound it is legitimate to allow arbitrary known gates,
as the imported iid-Choi lower bound already allows them. With explicit
probe coefficients and a bounded/compressed reference register one may
also pay ordinary generic known-matrix synthesis, polynomial in the
explicit matrix dimension and inverse accuracy. These are distinct cost
contracts.

One can state the copy-only refinement more intrinsically. Set
chi_i=d_i ||rho_(A_i)|| and scale T_i by ||T_i||. The success probability
then becomes 1/chi_i. The same queue has expected sample consumption
sum_i m_i chi_i, which replaces S_matrix in (13). Every chi_i is between
1 and d_i. If all chi_i=1 the filters succeed deterministically and
EXACTLY Q copies suffice, with no truncation delta. This refinement is
not charged as an efficient matrix-spectrum oracle in the gate-paid port.

### 3.3 Complete-error and block-width consequences

If a processor using (8) has complete error e uniformly in U, (10)--(11)
give an iid-Choi processor with error at most e+delta and the same joint
payload contract. A further known-controller simulation error zeta adds
to that total. Section 4 therefore implies

    ceil(Q k^b/delta)
       >= r^2 [log k-h(e+delta)-(e+delta)log(k-1)]/(16k^2) (14)

when e+delta<1-1/k, with arbitrary known matrices allowed. The explicitly
gate-paid version replaces k^b by k^(2b). For fixed useful e, delta and
fixed k,b, either version is Omega(r^2) in Q. No logarithm in the number
of blocks is needed: the finite queue uses a total-cost Markov bound,
not a separate high-probability cap for every block.

In particular, a family with Q=O(r^(2-zeta_0)) and fixed useful accuracy
cannot lie in this bounded-block class with b<zeta_0 log_k r-O(1).
This is a necessary condition within (8), not a claim that logarithmic
block width is sufficient, a general entanglement-depth theorem for mixed
query marginals, or a bound on active payload-dependent strategies.

## 4. The actual iid-Choi lower bound for every fixed k, including qubits

The inherited N1104 proof states k=3. Here is its literal dimension port;
the three-label Fano statement is not reused unchanged. This argument
uses the SAME already accepted SU(d) concentration input as that proof.

It suffices to take D=d=kr and U Haar on U(d); a larger ambient can contain
this known d-dimensional family. Write J_U=P_U/r, where P_U has rank r
and Tr_logical P_U=I_d/k. Define the consistent exchangeable states

    R_m=E_U J_U^tensor m, R_0=1,
    F_m=m log(kd)-S(R_m), a_m=F_m-F_(m-1).

The one-copy mean is I_(kd)/(kd). Strong subadditivity and exchangeability
make a_m nondecreasing, so for n>=1,

    a_(n+1)<=F_(2n)/n.                                  (15)

Let g(U)=k^2 r Tr(J_I J_U)=(k^2/r)Tr(P_I P_U). Then Eg=1,
g>=0, and invariance plus Renyi-2 entropy gives

    F_m<=log E g^m<=log E exp[m(g-1)].                   (16)

For any Hermitian generator H of Hilbert--Schmidt norm one,

    |d Tr(P_I P_(exp(itH)U))/dt|_(t=0)
       <=2 ||P_I||_2 ||(I_k tensor H)P_U||_2
       =2 sqrt(r/k).

Thus g is L_g-Lipschitz with L_g=2 k^(3/2)/sqrt(r). The accepted primary
SU(d) log-Sobolev inequality is Ent(f^2)<=(4/d)E||grad f||^2 with the
Hilbert--Schmidt Riemannian metric (Meckes--Meckes1210.2681). Global-phase
invariance identifies its averages with the U(d) ones here. Applying it
to exp(tg/2) and integrating Herbst's differential inequality gives

    log E exp[t(g-1)] <= L_g^2 t^2/d =4k^2 t^2/r^2.

All functions are bounded on the compact group; no limiting MGF or
singular density is assumed. Hence

    F_m<=4k^2 m^2/r^2,
    a_(n+1)<=16k^2 n/r^2.                               (17)

Let A,B be the last Choi reference and output in R_(n+1). Since
Tr_A J_U=I_d/d for EVERY U,

    I(A: J-programmes,B)=a_(n+1).                        (18)

Measuring A in the logical basis gives the equiprobable k-label ensemble
E_U[J_U^tensor n tensor N_U(|a><a|)]. A decoder of HALF-diamond error e
makes a label error at most e, uniformly in U. Data processing and Fano
therefore imply, for 0<=e<1-1/k,

    log k-h(e)-e log(k-1) <=16k^2 n/r^2,
    n>=r^2[log k-h(e)-e log(k-1)]/(16k^2).                (19)

For k=2 this is r^2[log2-h(e)]/64. For k=3 the coefficient 1/144 and the
log3-h(e)-e log2 bracket reproduce the inherited statement with its
unhalved error zeta=2e. Zero programme copies cannot achieve e<1-1/k,
as the averaged datum is label-independent, so the n>=1 step loses no
case. All logarithms are natural. This is not an optimal epsilon-law.

The processor in (19) may have arbitrary ancillas, arbitrary joint gates,
all-reference payloads and unrestricted known computation. It has NO
additional original N calls after receiving its n Choi copies. This last
qualification is why (19) does not become an adaptive physical-query
lower bound.

## 5. The unexcluded input resource, and the real remaining question

The preceding theorems leave a specific operation, rather than an
unspecified reflection-precision allocation. A collective parallel probe
may have a nontrivial globally entangled logical input, and an active
strategy may prepare future inputs correlated with the UNKNOWN payload.
Neither is an iid Choi bank nor necessarily (8).
Offline sequential calibration with U-dependent quantum query states is
also outside the known parallel-input hypotheses here.

For example a qubit query marginal invariant under collective U(2) and
query permutations has a Schur profile

    rho_A=directsum_j p_j I_((2j+1) f_j)/[(2j+1) f_j],
    f_j=binom(Q,Q/2-j)-binom(Q,Q/2-j-1),
    chi=2^Q max_j p_j/[(2j+1) f_j].                     (20)

The iid-Choi profile has p_j=(2j+1)f_j/2^Q and chi=1. A probe confined
to the symmetric j=Q/2 sector has chi=2^Q/(Q+1), so it escapes the small-
chi reduction. That does NOT make it sufficient: C's frozen ROOT28 exact
single-sector analysis already bounds that particular programme by
Fe<=1/4+(Q+1)/(8r sqrt(Q)); a fixed useful gain still needs Omega(r^2).
The formula is a granted stronger comparator, not another run here.

A full input profile with coherence preserved in its purification is a
genuinely different resource from (4). Replacing it by separately chosen
one-irrep programmes, by independent averages of the common frame, or by
a free inverse frame would change the task. No acquisition of an optimal
full-profile decoder, efficient Kronecker multiplicity oracle, general
parallel lower bound, or subquadratic active inverse is claimed here.

## 6. Strong ordinary operations remain available

The previously paid flat inverse uses O(k^2 r^2/epsilon) original source
calls, offline if desired, plus a consumed quantum programme, all its
storage and online controlled-collision/controller latency. Its ideal
amplification takes O(r) exact reflections; its ACTUAL programme is (4).
The present theorem explains why that bank cannot be made a subquadratic
rank recovery resource merely by a better collective use of it. It does
not prove its 1/epsilon law optimal or identify DME as the best processor.

Yoshida--Murao2607.29054v1 Corollary11/(140) is also admitted at full
strength: a REAL deterministic approximate conjugate k->D channel costs
at most k(rD-k)/epsilon parallel native calls, with the stated known CG
controller cost polynomial in rD and 1/epsilon. At D=kr this is
k^2(r^2-1)/epsilon. Its type is k->D, not the D->k arbitrary-payload
inverse. Appending a transpose, a restoring failure, or coherent V* is
not a free reduction. Its varying-r optimality is not supplied by the
paper's constant-r general-channel corollary. Its actual globally
coherent input service is not silently put inside class (8).

Pure-isometry/unitary inversion, optimized PBT/storage-retrieval and the
specified off-code covariant converter remain as paid in ROOT28. None
has been withdrawn to manufacture the present lower bound. The primary
random-purification and conditional-sample operations already underlie
the exact bank conversion; no generic novelty is claimed for them.
Historical priority of these access-class compositions remains UNKNOWN.

## 7. Precision, storage and execution boundary

Equations (2)--(4) and (9)--(13) are ideal finite-dimensional CPTP
constructions. For actual finite known controls, divide a declared zeta
over their finite gate list; a channel hybrid adds zeta to programme and
complete decoding error. In particular one compares the WHOLE capped
queue instruments, including both Bell outcomes and every fallback.
One does not divide a rounded conditional-state error by a rare success
probability and then treat that normalized branch as free. At most M
trials allow a literal per-trial full-instrument budget zeta/O(M).
The growing-rank random-purification port may
use the already paid highest-weight/small-Schur/ONE common finite-Haar
twirl construction. Its conservative bound is polynomial in M,r and
inverse accuracy, with physical-carrier storage at least M log(k r D)
qubits plus reference/control workspace. No large-irrep enumeration,
real-Haar oracle, fixed-rank-only polynomial or polylog(r) claim is used.
The fair-bit law approximates the AVERAGED quantum channel; it is not
close in classical TV to continuous Haar. Its seed is discarded.

The Bell queue in (9) needs at most M source samples, at most M trials,
the supplied probe preparations/inverses only as known controls, and
their measured Bell outcomes. Accepted blocks have total Q output
carriers plus their stated references. Generic coefficient filters in
(12) or (7) have no efficient succinct-description theorem here; their
copy-count use deliberately allows unrestricted known processing.

This work performs source reading, exact symbolic derivation and access
accounting only. No new quantum/source experiment, random source tape,
reflection simulation, numerical optimum or many-body fixture supports
the theorems. The complete all-k entropy argument is analytic; it is not
an extrapolation of a finite label table.
