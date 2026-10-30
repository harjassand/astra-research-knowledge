# A covariant causal receiver and an exact parallel-query boundary

30October2026. Root personally constructed the comb model, exact one-query
receiver and rational two-query parallel dual. C independently constructed
the coherent relative-SWAP/Pauli feedback receiver. This is a mathematical
operation/certificate, not a quantum/source experiment or a linear-r theorem.
Pure-isometry endpoints match established inversion results; historical
priority of the mixed-source specialization is UNKNOWN.

## 1. Input and consequence being investigated

For known integers k>=2,r>=1,D>=kr, the SAME unknown memoryless source is

    N_U(X)=U(X tensor I_r/r)U*,  U*:U=I_(kr).

Only ordinary forward uses are supplied. Input registers can be entangled
with retained memory, and later calls may depend coherently on that memory.
No controlled unknown source, adjoint/dilation inverse, environmental flag,
junk intervention or quantum switch is assumed. Known gates, clean ancillas,
measurements and quantum storage are separately paid operations. One already
encoded arbitrary payload must produce a logical output at full throughput.

The target is the native-query gap between explicit quadratic-r recovery and
the physical-query linear lower bound, not a presumed quadratic impossibility.
The early ordinary construction in a_ordinary/FLAT_RDS_RECOVERY.md supplies
O(k^2 r^2/epsilon) offline calls with no online source query, but a consumed
large quantum programme and online gates. Its ideal reflection count is only
O(r); the expensive source-to-reflection supplier is the actual bottleneck.

## 2. Choi and causal conventions

Use UNNORMALIZED channel Choi matrices J_N, Tr_B J_N=I_A. A Q-slot receiver
has a positive comb W on logical output A0, query inputs A1...AQ, query
outputs B1...BQ and encoded payload B0. Full-throughput deterministic causal
trace identities are

    Tr_A0 W = I_BQ tensor W_Q,
    Tr_Aj W_j = I_B(j-1) tensor W_(j-1)  (j=Q,...,2),
    Tr_A1 W_1=I_B0.

For a FULLY PARALLEL query block the single trace identity is

    Tr_A0 W=I_(B1...BQ) tensor W_pre,
    Tr_(A1...AQ) W_pre=I_B0.

It allows arbitrary entangled source inputs, memory and payload preprocessing;
it is NOT restricted to independent normalized Choi programmes. Source queries
and the target payload encounter the same N_U. Direct Kraus-index contraction
gives average entanglement fidelity Tr(W Omega), where

    Omega=( E_U[J_N^(tensor(Q+1))] )^T/k^2.                    (1)

The transpose is on all displayed tensor indices and the ordering pairs Ai
with Bi. These k^2 factors are for the ONE logical Bell test, not one factor
per queried channel. No Haar sampling is used in the computations below.

## 3. Haar covariance gives a finite complete operator model

Average U over Haar Stiefel measure. Physical simultaneous U(D) rotations on
all B carriers and logical simultaneous U(k) rotations on all A carriers
preserve the objective and causal identities. Every averaged optimum can
therefore be written

    W=sum_(sigma,tau in S_(Q+1)) c_(sigma,tau)
          P_sigma^A tensor P_tau^B.                       (2)

This is the COMPLETE commutant, including inter-irrep/multiplicity coherence
allowed by causality, not a fixed-spin ansatz. Null permutation relations at
k<Q+1 are retained: coefficient trace equalities are imposed only modulo the
logical Gram kernel. PSD is imposed on every logical Young irrep with at most
k rows and every physical one with at most D rows. Their Specht-block sizes
are small for Q<=3. The code verifies all representation multiplications.

Tracing a tensor factor of a permutation removes it from its cycle; a fixed
point contributes the tensor dimension. Thus all causal constraints are
explicit finite linear coefficient/Gram relations. The objective is simply

    Tr(W Omega)=k^-2 sum_(sigma,tau) c_(sigma,tau)
             k^(cycles(sigma tau^-1)) r^(cycles(tau)-Q-1). (3)

To verify(3), the physical twirl Gram is G_(sigma,tau)=D^(cycles(sigma^-1tau)).
For J0=|Omega_k><Omega_k| tensor I_r/r, the physical permutation moment is

    Tr_B[P_tau* J0^(tensor l)]=r^(cycles(tau)-l) P_tau^A,
    l=Q+1.

Twirl via G^-1, then contract with(2); the physical Gram cancels. Simultaneous
inversion of both permutations leaves the coefficients unchanged, so the
transpose in(1) does not change this real operator. Equation(3) does not make
all aspects of decoding independent of D: wire widths, known gates and allowed
Young diagrams still carry D. All model reductions are mathematical.

## 4. An exact one-query theorem and its literal receiver

For Q=1 the complete averaged comb is

    W=alpha I+beta S_A+gamma S_B+delta S_A S_B.

The causal identities force beta=1/k-k alpha, delta=-k gamma. Writing
x_+=alpha+gamma and x_-=alpha-gamma, positivity of all four swap sectors is
EXACTLY

    1/[k(k+1)] <= x_+,x_- <= 1/[k(k-1)].                    (4)

The objective is

    F=1/k^2+(k^2-1)(x_--x_+)/(2kr),

so its maximum is

    F_one=(1+1/r)/k^2.                                    (5)

Here is a constant-performance receiver attaining it for EVERY U, establishing
the minimax result rather than merely an average upper bound. Query N once on
half a k-dimensional Bell pair and store reference R plus physical programme
B1. On incoming B0, measure their known SWAP sector t=+/- and apply to R the
known CPTP channel

    Gamma_+(X)=(Tr(X)I+X^T)/(k+1),
    Gamma_-(X)=(Tr(X)I-X^T)/(k-1).                         (6)

These maps are PHYSICAL: their Choi matrices are (I+/-SWAP)/(k+/-1), positive
and trace preserving. Symmetric/antisymmetric matrix-unit bases provide
explicit Kraus operators. For k=2, Gamma_- is the known Pauli-Y unitary.
After a physical swap result, the unnormalized R state is

    omega_R^+/-=(I+/-rho^T/r)/(2k).

Equations(6) yield the actual decoded channel

    Lambda(rho)=rho/[r(k^2-1)]
                +(1-1/[r(k^2-1)])I/k.                    (7)

Its fidelity is(5). The known swap test uses O(logD) controlled swaps with a
single known ancilla; programme storage is O(logD+logk) qubits and is consumed.
There is zero online N call, but the payload must survive these known gates.
No branch is an exact mixed-source inverse when r>1. In particular, the
antisymmetric branch's qbit output is [(r-1)I+rho]/(4r): a useful fidelity
signal cannot be declared a heralded success or safely repeated on the same
payload. This constructive failure is not an asymptotic query lower bound.

## 5. Numerical construction of the next causal mechanism

`covariant_inverse.py` solves the FULL fixed-order model for Q=1,2,3 and an
equally informed PARALLEL entangled-input model. It is a discovery tool; solver
statuses/residuals are retained, including CLARABEL failures and SCS recovery.
No source/Haar/quantum run was performed. Pure Q=1,2,3 endpoints match actual
2401.10137v3 Table2 and2109.08202v3 Theorem5: e.g. Q2 parallel
cos^2(pi/5)=(3+sqrt5)/8 and the established sequential0.7500 result. These
pure endpoints are ordinary controls, not inventions of this wave.

For mixed r=2, the proposals are Q2 adaptive0.450250928 versus
parallel0.432940681, and Q3 adaptive0.510393080 versus parallel0.484627079.
Those decimals ALONE prove no advantage. They identified the two-query
coherent feedback operation constructed separately by C and the small
parallel dual that is now exactly certified below. They do not establish
linear-r high-fidelity recovery or an asymptotic rate for adaptive strategies.

## 6. A complete exact two-query PARALLEL dual

Now k=2,r=2,D=4,Q=2. By physical covariance, W_pre of any averaged parallel
strategy is rho_(A1A2) tensor I_B0, with Tr rho=1: twirling B0 in the parallel
trace identity gives this form even if the original preprocessing used the
payload. Logical covariance allows rho to be averaged too. No restriction to
iid or classically known source inputs has been made.

Choose an invariant Hermitian Y on A1,A2,B0,B1,B2. If

    I_A0 tensor Y >= Omega,
    Z=Tr_(B0B1B2)Y <= lambda I_(A1A2),                    (8)

then every such parallel W obeys

    Tr(W Omega)<=Tr[Y Tr_A0 W]=Tr(rho Z)<=lambda.          (9)

We use all twelve coefficients

    Y=sum_(a in S2,t in S3) y_(a,t) P_a^(A1A2) tensor P_t^B.

For Omega, compute the6x6 physical Gram G exactly and set

    omega_(s,t)=G^-1_(t,s) r^(cycles(s)-3)/k^2.

The first condition in(8) is checked on logical S3 irreps trivial/standard
and physical S3 irreps trivial/standard/sign, so SIX blocks of size at most4.
For the standard representation use rational basis(e0-e2,e1-e2), whose metric
is H=[[2,1],[1,2]]. A block M is positive as an operator exactly when
(H_A tensor H_B)M is positive as an ordinary symmetric rational matrix. This
avoids relying on floating square roots or a nonorthogonal PSD convention.
The second condition in(8) has the two exact scalar sector values

    z_+/-=sum_t D^(cycles(t))( y_(I,t)+/-y_(SWAP,t) ).

`parallel_dual_certificate.py` uses numerics only to PROPOSE y, rounds them
to rationals, symmetrizes inverse-paired coefficients, and adds a positive
identity shift. It then accepts only after exact rational LDL factorization
with strictly positive pivots for ALL six blocks and exact z_+/-<=lambda.
The shift is1/549755813888. The accepted result is

    F_parallel <= 29751457437/68719476736
                =0.4329406865435885... .                  (10)

All coefficients, six matrices, positive LDL pivots and normalization values
are saved in PARALLEL_DUAL_CERTIFICATE.json. This is a rigorous upper bound
once(1),(8) are consumed, not a claim that the noisy numerical optimum is
exact. No hardcoded approximate feasible-point residual is called a proof.

## 7. Consequence for C's positive feedback receiver

C's separately constructed FULL-THROUGHPUT, two-query native circuit has
one online query after payload arrival. Its exact positive/trace-preserving
receiver is certified in c_active_inverse/C_COHERENT_FEEDBACK.md and its
owned exact consumer. Root's final acceptance of that whole construction
is recorded separately; it is not supplied by this dual alone.

Its proposed exact fidelity is

    F_adaptive=55716029295809/123760695281664
              =0.4501916312687661... > (10).               (11)

The circuit retains coherent relative-SWAP information and uses different
known Pauli-Stinespring amplitudes in its two sectors before QUERYING the
retained unknown logical memory. Its actual all-U invariance also permits
a physical logical-Pauli twirl via known pre-Paulis on EACH source query
and a known decoded post-Pauli, with no operation on the already encoded
payload. If the positive receiver/that twirl are accepted, its all-input
half-diamond error is exactly1-F_adaptive, whereas any parallel receiver
has worst-case half-diamond error at least1-(10), by its Bell test.

Thus the intended consequence is a strict, physically supplied adaptive
versus parallel arbitrary-payload decoding gap for a mixed reversible source,
not a measurement-only virtual inverse. A SOURCE CALL still means the full
unknown N cycle, and the online payload must remain coherent through it.
No actual device, native readout/gate admission or practical advantage has
been acquired. No novel general adaptive gap is claimed without the strongest
mixed-source prior comparison; the pure adaptive gap was known already.
