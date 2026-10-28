# Low observable-rank quantum-port quotients without a CP section

28 October 2026. **Separate theorem candidate; independent receiving pending.** The received full-core `COMPLETE_PORT_PHYSICAL_RESIDUAL_SIMULATOR.md` (SHA `d2564c18b184b92fdd471e9d73720c693389c7f2f07f82432885663189da7a92`, receipt `304928cf39604187dc89ba8242d6a3e7608824ac80a27a77007fd4ade96fb563`) is unchanged. This extension removes its full r=d^2 saturation premise only by supplying an HONEST exact observable-rank upper bound over the full IC port alphabet, plus a matching exact rank certificate for the actual fitted physical candidate. A smaller nonsingular noisy minor by itself is insufficient.

The new obligation is proved explicitly: the scalar unobservable kernel remains invisible under arbitrary finite coherent port/caller contractions with all terminal records retained. No completely positive quotient section or physical equality of chosen memory representatives is assumed. The parent signed/Dyson route is not rederived here; a complete segment-norm lemma is stated as a reusable consequence.

## 1. Exact rank and physical interface

Retain the received stationary finite native quantum-port interface: finite accessible input/output dimensions, ordinary known IC input density matrices rho_(a,u), output POVM effects E_(a,v), and actual CP maps V_(a,o):M A_a -> M B_a with TP native-outcome sums. Native outcome o and action labels are classical. The caller may retain quantum references, recycle outputs coherently, measure and adapt actions from classical records. Distinct native labels are not coherently superposed. Source memory is inaccessible and starts in its declared reset state product with arbitrary caller input/reference. All starts, settings, finite caller memory and implementation errors remain paid.

In this first theorem the source memory is finite-dimensional. Its dimension need not equal the candidate's or sqrt(r). The ordinary causal-break alphabet consists of z=(a,u,o,v) with

    Phi_z(X)=Tr_B[(I tensor E_(a,v)) V_(a,o)(X tensor rho_(a,u))].

Let R be the COMPLEX linear span of all raw finite branch-prefix states Phi_w(rho_0), including the empty word. Define

    N={X in R : Tr Phi_w(X)=0 for EVERY finite future word w}.

The actual observable rank is dim_C(R/N), equivalently the rank of the infinite raw Hankel matrix. Supply an exact upper bound r on this rank for the ENTIRE declared IC alphabet. The true bound must come from an architectural promise or another sound certificate, not a thresholded singular value or absence of observed long-word discrepancies. A full confidence-certified r by r core then proves the rank is exactly r on the good event. If actual rank is smaller, this particular r-core test can return UNKNOWN indefinitely.

Choose r raw prefixes p_j and future words f_i with empty prefix/test first. Let tau_j=Phi_(p_j)(rho_0), F_i=Phi_(f_i)^*(I), so tau_j>=0, Tr tau_j<=1 and 0<=F_i<=I. Set

    H_ij=Tr(F_i tau_j), H_z,ij=Tr[F_i Phi_z(tau_j)],
    m_j=Tr tau_j, C_z=H^-1 H_z.

All tables are raw JOINT probabilities, without conditional normalization. Assume H is certified nonsingular by the same simultaneous interval inverse test as the received source. It follows that the classes [tau_j] form a basis of R/N and the selected tests form its full dual basis.

Supply a candidate initial density and actual FULL CP/TP quantum ports on a declared finite memory dimension d_f, with the same accessible spaces, outcomes and legal core procedures. Its raw states sigma_j, tables H^f,H^f_z and mass row m^f are computed from that physical model. Require H^f nonsingular and candidate observable rank <=r over its complete IC branch alphabet. Therefore its rank also equals r. Define C^f_z=(H^f)^-1 H^f_z. A family of separately CP scalar causal-break maps is not a full candidate: the transpose failure control in the received theorem still applies.

## 2. Algebraic quotient identities, with their exact domain

The reachable space R is invariant under every Phi_z. The space N is invariant as well: for X in N, every Tr Phi_w Phi_z(X) is another defining zero. Also Tr N=0 because the empty future is included. Both spaces are closed under adjoint, since they are generated/detected by Hermitian physical states/effects.

Define the extraction and chosen physical section by

    Pi_j(X)=sum_i (H^-1)_(j,i) Tr(F_i X),
    Lambda(c)=sum_j tau_j c_j.

Then

    Pi Lambda=id,
    X-Lambda Pi(X) in N            for X in R,
    Pi Phi_z(X)=C_z Pi(X)          for X in R,
    Tr X=m Pi(X)                  for X in R.              (1)

Proof: nonsingular H gives the first identity. The selected tests separate R/N, so the difference in the second has zero quotient class. Invariance of N gives the third, using Pi Phi_z Lambda=H^-1 H_z; the fourth follows from Tr N=0. The same identities hold for the candidate's R_f,N_f,Pi_f,Lambda_f.

In general Phi_z Lambda(c) is NOT Lambda(C_z c) as a physical memory operator. Their difference lies in N. Likewise Lambda Pi need not be positive, CP or TP on the ambient memory algebra. We use exactly (1), not a full-space inverse identity.

## 3. Why the invisible kernel survives coherent quantum callers

This is the load-bearing upgrade beyond a scalar Hankel argument. Let D_(a,u) and B_(a,v) be known Hermitian IC duals:

    X_A=sum_u rho_(a,u) Tr(D_(a,u)X_A),
    Y_B=sum_v B_(a,v) Tr(E_(a,v)Y_B).

For an operator X on M A R, first form

    X_u=Tr_A[(I_M tensor D_(a,u) tensor I_R)X] on M R.

Expanding input and output in those dual frames yields the exact full operator identity

    (V_(a,o) tensor id_R)(X)
      =sum_(u,v) insert_B { (Phi_(a,u,o,v) tensor id_R)(X_u), B_(a,v) }. (2)

Here insert_B places B between the memory and the remaining caller register; on a simple tensor Y_M tensor Z_R it means Y_M tensor B tensor Z_R, extended linearly. Equation (2) is an identity of every memory/output/reference matrix element, not an inference from distances between classical distributions.

Consequently, for every finite caller/reference dimension,

    V_(a,o)[R tensor L(A R)] subset R tensor L(B R),
    V_(a,o)[N tensor L(A R)] subset N tensor L(B R).         (3)

Indeed partial input functionals preserve the memory-factor subspace; each Phi_z preserves it; and the finite dual-frame sum preserves it. Caller-only linear operations preserve the same subspaces. This includes each measurement branch, record-controlled operation, classical selection of native action, private randomization and coherently recycled input. By induction the memory entries of every finite true joint history lie in R. An insertion in N stays in N through EVERY such complete continuation, branch by branch. Finally Tr_M annihilates it because Tr N=0.

Therefore the complete accessible endpoint OPERATOR from any signed X in N tensor L(caller) is zero, with all native/controller records and reference registers retained. There is no normalization of a rare history and no scalar-only terminal restriction. The conclusion is not a claim that the hidden memory insertion vanishes physically. The identical statement holds for the candidate kernel N_f.

Applying Pi entrywise to (2) gives the exact quantum quotient transfer on operator-valued coordinates:

    [C_a(x)]_(i,o)=sum_(j,u,v) C_(a,u,o,v)[i,j]
           B_(a,v) tensor Tr_A[(D_(a,u) tensor I_R)x_j].     (4)

For every reachable joint X, Pi V_a(X)=C_a Pi(X). Moreover a candidate physical continuation from Lambda_f(x) has exactly the complete accessible endpoint predicted by its quotient transfers and terminal row m^f: any deviations from the chosen section lie in N_f and vanish by (3). This operational suffix identity replaces physical section intertwining. No CP map on an abstract quotient cone has been constructed or assumed.

## 4. Complete norm and empirical residual certificate

For a positive true reachable joint prefix Omega, including an entangled caller,

    x_j=Pi_j(Omega)=sum_i (H^-1)_(j,i) Tr_M[(F_i tensor I)Omega].

Every partial effect functional is CP and trace-nonincreasing because 0<=F_i<=I. Hence, uniformly over caller dimension,

    ||x||_Sigma:=sum_j||x_j||_1 <=K Tr Omega,
    ||Lambda_f(x)||_1 <=||x||_Sigma,
    K>=sum_(j,i)|(H^-1)_(j,i)|.                            (5)

The fitted lift bound uses only sigma_j>=0 and Tr sigma_j<=1, not a positive quotient section. On arbitrary Hermitian joint X the same functional argument gives ||Pi(X)||_Sigma<=K||X||_1. We do not import the scalar cube-vertex sharpening.

For completeness the acquired quantities are

    U=Hhat^-1, A=|U|D_H, ||A||_infinity<1,
    M=(I-A)^-1|U|, K=max(1,sum M_ji),
    E_z=M[D_z+D_H|C^f_z|+|Hhat C^f_z-Hhat_z|],
    epsilon=max_a max_j sum_(i,o,u,v)
                  ||D_(a,u)||op ||B_(a,v)||_1 E_(a,u,o,v)[i,j],
    delta_m=max_j {D_H,(1,j)+|Hhat_(1,j)-m^f_j|}.            (6)

Certified upper bounds for the dual norms suffice. On the common confidence event |C_z-C^f_z|<=E_z. The exact partial-functional norm inequality and (4) give ||C_a-C^f_a||_(Sigma,complete)<=epsilon_a. These are the received interval/dual calculations; they do not require full memory rank. All branch outcomes are included, and actual input/output conditioning is paid.

**Low-rank complete CP-suffix theorem.** For every allowed finite controller with at most H native calls, the complete accessible source/candidate endpoint distance obeys

    D_H<=min(1,(K/2)(H epsilon+delta_m)).                   (7)

For a specified bounded-call controller, H epsilon can be replaced by epsilon E_true[L]. The controller may be selected after reading the simultaneous calibration record. Initial coordinates are e_1 because the empty prefix is first; both source and candidate initial memories remain product with the caller.

**Proof.** Telescope in coordinates with true prefixes, fitted suffixes, and the terminal (m-m^f) term, exactly as Eq. (13) of the received full-core source. At each true positive prefix of mass p, (5) gives coordinate norm <=Kp; the local complete residual gives <=epsilon Kp. Lift that signed insertion with Lambda_f and apply the actual candidate physical continuation. Its trace norm contracts. Equation (3), NOT physical section invariance, proves that this continuation has exactly the required quotient endpoint operator. Sum true active-prefix masses to get E_true[L]. The terminal row term is bounded by K delta_m using the true terminal positive state and (5). Divide by two. Both endpoints are physical, yielding the cap. QED.

Thus the fixed-service full-CPTP decoder regret, finite decoder SDP/synthesis mechanism, raw-mass accounting, confidence failure/abstention debits and record-averaged implementation distinctions of the received full-core theorem carry over with this eta. The extension gives no hidden-memory distance, normalized rare-history guarantee, free source samples or automatic finite-model fit.

## 5. Shared complete segment primitive, not another signed predictor

For any complete finite physical source/controller segment P, retaining the physical memory at its endpoint, its exact quotient-coordinate action is

    T_segment=Pi P Lambda,
    ||T_segment||_(Sigma,complete)<=K.                    (8)

To verify composition, replacing a representative by Lambda Pi changes it only by N; Eq. (3) keeps that change in N and Pi kills it. Thus the quotient action is independent of representatives even through coherent controls. The norm follows from ||Lambda||<=1, physical CPTP contraction, and ||Pi||<=K. A zero-length identity has norm one. The tuple input may be signed Hermitian; no intermediate positivity is required.

Equation (8) supplies a genuine low-rank complete primitive potentially usable by the separate root signed/Dyson method under these additional honest rank premises. This source does not independently receive or rederive that method, its projection bounds or its implementation costs.

## 6. Short raw acquisition and exact candidate rank certification

On the r-dimensional quotient, the reachable chain from [rho_0] stabilizes by length r-1, and the dual future chain from trace does too. If a stage fails to grow it is invariant under every quotient branch map; a growing chain starts at dimension one. Thus when the actual rank is exactly r, prefixes and future words of lengths <=r-1 contain a nonsingular r-core, including empty prefix and trace by basis extension. Shifted words have depth <=2r-1. This relies on the EXACT supplied rank upper bound; it is not a way to discover absence of later modes from finite counts.

For s IC branch symbols and q=sum_(l=0)^(r-1)s^l, the pool contains at most (1+s)q^2 raw core/shifted events before deduplication. The pool, settings, all attempted/failed-prefix calls, independent starts, local IC frames and finite matrix computations are paid. Shared-setting multinomial outcomes can share shots. Simultaneous Hoeffding intervals, finite core enumeration and summable sequential-round budgets work as in the received raw-core source. Near-singular cores can require arbitrarily many starts; r and this word pool can themselves be large.

The fitted candidate's rank upper bound must be exactly checked. For declared finite d_f, one option forms reachable/future words through length d_f^2-1 and forces all (r+1) minors of the resulting complete IC Hankel matrix to vanish. A more compact sufficient-and-complete existential witness uses columns G=[sigma_j] in memory Liouville coordinates and at most d_f^2-r kernel columns W, with

    trace W=0,        Phi^f_z W=W A_z,
    Phi^f_z G=G C^f_z+W B_z,    sigma_0=G e_1,
    H^f C^f_z=H^f_z,           H^f invertible.              (9)

Every z in the FULL IC alphabet is included. The kernel columns need not be independent for soundness. Their span is invariant, trace zero, and by (2)-(3) invisible to complete quantum continuations. These polynomial identities certify candidate observable rank<=r, while H^f gives the matching lower bound. Conversely an actual rank-r candidate supplies W as a basis of its reachable invisible kernel, of dimension <=d_f^2-r, so a finite enumeration of allowed column counts is complete.

With rational/real-algebraic ideal frame/control coefficients, exact physical CP/TP constraints, raw probabilities in rational bands and (9) give a finite semialgebraic search. It can be very expensive. A local optimizer is only a proposal; its rank tolerance is not an exact certificate. Conditional eventual feasibility additionally needs a supplied finite physical dimension bound sufficient to contain an actual rank-r source realization. Finite observable rank ALONE does not supply that physical realization or a dimension bound. If the actual source dimension d is supplied, searching d_f=d is a finite but generally prohibitive fallback on a good confidence event. Resource-capped UNKNOWN/ABSTAIN costs its own mass in any unconditional recovery risk claim.

## 7. Concrete non-full-rank mechanism and evidence scope

A qubit memory with native controlled-Z port U=|0><0| tensor I+|1><1| tensor Z provides a useful boundary case. Start the source memory in |+><+|. The ordinary full IC branch-prefix span can be all four memory coordinates, but all future effects are diagonal. The invisible kernel is span{X,Y}, so observable rank is TWO. Arbitrary coherent callers cannot reveal the hidden off-diagonal entries: the port preserves the pointer labels, all memory off-diagonal operators remain off-diagonal, and the final memory trace removes them. This remains true with recycled entangled inputs and all classical records retained.

With six-state Pauli inputs and output POVM rho_(P,s)/3, choose the empty prefix and the branch “input +X, output +X.” The second raw memory state is |0><0|/6. Choose the same future test and empty trace; then

    H=[[1,1/6],[1/6,1/18]],    m=(1,1/6),    sum|H^-1|=50.

The chosen section is NOT physically invariant: a branch with input +X and output -X produces |1><1|/6, while its selected representative differs by an off-diagonal invisible operator. A finite full-memory-core theorem would correctly refuse this rank-two observable process; the present theorem accepts it only with the supplied/certified rank-two structure.

A physical fitted initial state with populations (51/100,49/100) and nonzero imaginary coherence has the same full ports. Every quotient native C_z is independent of the initial pointer weights; source and fit have identical C_z, but m^f=(1,17/100), so delta_m=1/300. Exact zero-width bands and this checked candidate give epsilon=0 and eta=1/12. The actual complete endpoint distance is at most |1/2-51/100|=1/100 for every finite controller; a single Bell probe already attains that value because the two pointer-conditioned outputs are orthogonal. This is a classical hidden-pointer mixture implemented quantum mechanically, not a quantum computational advantage. Its hidden coherences, noninvariant sections and coherent output test specifically exercise the quotient obligation.

`low_rank_complete_quotient_check.py/.json` is a completed PASS exact author fixture, not independent receiving, real data acquisition, generic physical-model search, a decoder optimizer or compiler. It verifies source AND candidate reachable dimension four, invisible dimension two and observable rank two; all 36 quotient maps agree; both chosen physical sections have nonzero invisible errors. Eight full input-matrix checks verify kernel invariance, and six amplified quotient checks retain a qutrit reference. A two-call outcome-dependent stopping controller retains both records and has E_true[L]=91/50; its endpoint difference is exactly the mass-row term, with certified half-trace upper bound 243/15625<1/12. The one-call Bell distance is exactly 1/100. Rank is certified by exact architectural algebra, not estimated from samples. All source calls, episode starts, RNG and hardware counts are zero; no floating-point inference is used.

## 8. Comparator, prior art and boundaries

Direct tomography of the SAME fixed H-call small accessible service remains the strongest equally informed baseline, as quantified in `DIRECT_SERVICE_TOMOGRAPHY_COMPARATOR.md`. It needs no hidden rank/dimension promise or physical hidden model, and already avoids environment tomography. The possible distinction here is acquisition depth <=2r-1 and reuse across later coherent/adaptive services, not mere existence of fixed-service recovery. The conservative K, IC weights, physical rank search and required widths can make this method much worse. No cost advantage is established.

The ordinary reachable/observable quotient and spectral identification ingredients are established and retained from the received classical sources; full IC quantum process reconstruction is established in [White et al., PRX Quantum 3, 020344 (2022)](https://journals.aps.org/prxquantum/abstract/10.1103/PRXQuantum.3.020344). The finite CP realization obstruction is not removed: [Monras and Winter, TQC 2014](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.TQC.2014.99) studies precisely the completely positive realization problem for finite-dimensional stochastic descriptions. This theorem assumes/checks an actual physical candidate and only proves complete operational invisibility of an already supplied quotient kernel. The earlier Singer/equivalence and correlated-noise decoder credits remain unchanged. No broad novelty claim is made.

No statement about an infinite-dimensional true memory is inferred merely from this finite-memory presentation. Such a version requires an explicit trace-class/normal-map formulation and retention of the finite-candidate existence limitation. No unbounded-controller/stopping limit, nonstationary extrapolation, free rank discovery, or CP section on an abstract quotient is asserted.
