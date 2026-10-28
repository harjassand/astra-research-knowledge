# Ordinary row-kernel validation and an honest fast-route fallback

28 October 2026. New candidate, independent receiving pending. The new construction replaces an untested exact row-rank promise by a PAID one-sided validation of the actual task approximation. It is not a generic k^2 worst-case theorem. The supplied physical receiver basis, stationary resets and four-real-coordinate encoder remain. The fast route is useful when a balanced nearly rank-one row representation exists; otherwise a received generic learner can be used after rejection.

## 1. The actual source, without a rank-one model assumption

Let T_x be the ordinary six-state loss density on the known physical d=2k dimensional B/A basis. Retain the full-CPTP objective ell(x,C)=(3/2)Tr(C^T T_x), with 0<=C<=2I. The actual linear encoder and the fixed physical source give ONE common purification linear in real x:

    Psi_x=sum_i |i> G_i x,
    T_x=Tr_E |Psi_x><Psi_x|,
    B_i=Re(G_i^*G_i), sum_i B_i=I_4.                 (1)

For example, take a fixed Kraus representation of the source and put the six ordinary probe labels, source Kraus index, and the unused purification degrees of freedom in E. The column for selector coordinate s is the actual six-state preparation with V_s in place of V_x. Thus (1) is a mathematical purification of the ACTUAL family, not a fitted positive Choi completion, and does not require physically coherent selector inputs. In particular each B_i is a real PSD matrix with Tr B_i possibly arbitrarily small. Its rank can be any value up to four.

After any finite ordinary pilot, let the learner freeze:

- a retained coordinate set I;
- rational real unit vectors v_i for i in I;
- a rational unit encoder x_0 such that |v_i^T x_0|^2>=9kappa/16 for all i in I, where 0<kappa<=1/4 is an algorithm parameter.

If no such candidate is returned, proceed directly to the generic fallback. The correctness of the validation below does NOT assume that the pilot accurately estimated B_i or their eigenvectors. Every pilot record is allowed.

Define the two nonnegative actual residuals

    Lambda=sum_{i not in I}Tr B_i,
    S=sum_{i in I}Tr[B_i(I_4-v_i v_i^T)].             (2)

These are properties of the selected approximation to the actual source. They are not asserted to equal the sum of spectral tails, and their acquisition is described explicitly below.

## 2. Actual probes measure both residuals with nonnegative outcomes

**Discarded-mass bank.** Draw the received finite fourth-design selector x, prepare one actual ordinary T_x, measure its output coordinate, and record one if it is outside I. Each fresh binary outcome has conditional mean

    p_D=Lambda/4.                                   (3)

The selector second moment I_4/4 suffices for this identity.

**Retained row-kernel bank.** Draw i uniformly from all d coordinates. If i is not retained, consume a declared ordinary call and record zero. If i is retained, draw one of three known orthonormal real directions z_{i,1},z_{i,2},z_{i,3} spanning v_i^perp, prepare that ordinary encoder, and record one exactly when the measured loss-state coordinate is i. The conditional mean is

    p_S=(1/(3d))sum_{i in I}sum_{a=1}^3 z_{i,a}^T B_i z_{i,a}
       =S/(3d).                                    (4)

This is a direct observable Bernoulli experiment, not a signed difference of empirical eigenvalues. It has variance at most its own mean, including at exact rank one.

All selector directions can be exactly rational unit vectors. For a rational unit v, choose s=1 if v_1>=0 and s=-1 otherwise, w=e_1+s v, and

    H=I_4-2ww^T/(w^T w).

Here w^T w=2(1+|v_1|)>=2. The last three columns of the rational orthogonal H form the required basis. There is no small denominator or source gap in this control construction. The at most 3d such chosen settings are actual paid calibration controls; this is not a claim of a constant number of validation settings.

Both banks are fresh after the entire candidate record is frozen. Conditional on that record, their outcomes are iid Bernoulli with the displayed means. The physical stationary source is fixed; conditioning does not average different source channels into a fictitious iid product. Exact rational samplers can be implemented with bounded bits and a paid whole-process approximation, as in the received base receipt.

## 3. Finite one-sided tests and deterministic caps

For 0<gamma,epsilon<=1 set

    Lambda_max=gamma epsilon/2^20,
    S_max=kappa gamma epsilon/2^24,
    u_D=Lambda_max/4, u_S=S_max/(3d),
    beta_0=epsilon/2048.

For either u=u_D or u_S, take exactly

    n(u)=ceil[(64/u)log(1/beta_0)]                   (5)

fresh calls. Accept that test if its empirical binary mean is at most u/2. The threshold comparison uses actual integer counts and rational parameters; no estimated stopping time is used.

The following elementary Bernoulli test facts apply uniformly over the frozen pilot record:

    Pr(accept and p>u)<=beta_0,
    p<=u/4 implies Pr(reject)<=beta_0.               (6)

For the first, monotonicity reduces to p=u, and the multiplicative lower tail is at most exp(-nu/8). For the second, monotonicity reduces to p=u/4, and the upper tail at twice the mean is at most exp(-nu/12). Equation (5) has ample slack. Integer threshold rounding is harmless: the two events are contained in the same real-threshold events.

Accept the fast route only if BOTH tests accept. Regardless of the pilot's quality or the source's row ranks,

    Pr(fast acceptance with Lambda>Lambda_max or S>S_max)
       <=2beta_0.                                  (7)

This is an unconditional false-acceptance-mass statement. It does not assert the same failure probability after conditioning on an arbitrarily rare acceptance record. The fixed validation source bill is

    n_D+n_S=O_tilde(d/(kappa gamma epsilon)).         (8)

## 4. Why the certified residual controls all coherent decoders

Put P=sum_{i in I}|i><i| and define the physical row projection only as a mathematical approximation:

    Phi_x=sum_{i in I}|i> G_i v_i(v_i^T x),
    Rhat_x=diag_i[(v_i^T x)/(v_i^T x_0)] on I,

with zeros outside I. Then Phi_x=Rhat_x Phi_x0 and ||Rhat_x||<=2/sqrt(kappa). The same actual purification in (1) gives, uniformly for every unit x,

    ||Psi_x-P Psi_x||^2<=Lambda,
    ||P Psi_x-Phi_x||^2<=S.

Consequently

    ||P Psi_x-Rhat_x P Psi_x0||
       <=(1+2/sqrt(kappa))sqrt(S)<=3sqrt(S/kappa).    (9)

No payload is measured or pinched in deriving this inequality. In particular every lost cross-coordinate coherence is paid by the norm of the same purification, rather than removed from the comparator. Equation (9) holds for arbitrary B_i ranks and for arbitrary learned directions.

On fast acceptance acquire a FRESH actual T_x0 Bures bank, conditional on the frozen pilot and validation record. Use

    m=kappa gamma epsilon/2^24, beta_q=epsilon/512,
    D_0=nextpow2(dr),
    n_0=ceil[(80D_0/m)log(12D_0/beta_q)],             (10)

where r is the supplied actual loss-state rank bound. Its physical density estimate tau satisfies root fidelity 1-f(T_x0,tau)<=m except beta_q. Form the positive quadratic predictor T_hat_x=Rhat_x tau Rhat_x. It need not be normalized or a TP source model.

A single Uhlmann alignment with the actual anchor, (9), and the full-decoder loss-operator norm at most 3 imply

    sup_{x,C CPTP}|sqrt(ell(x,C))-sqrt(ell_hat(x,C))|
       <=sqrt(3Lambda)+sqrt(27S/kappa)+sqrt(24m/kappa)
       =:delta.                                    (11)

On the validated event,

    delta^2<=9Lambda_max+81S_max/kappa+72m/kappa
       =(297/2^24)gamma epsilon
       <gamma epsilon/32768.                       (12)

This is a simultaneous guarantee for the actual encoder family and every full coherent decoder. It is not a uniform matrix/Bures completion assertion.

## 5. Optimization, acceptance accounting, and generic fallback

Use the received finite known-coefficient full-CPTP SDP and rational encoder-net construction, with objective coefficient bound b=6/kappa and total surrogate optimization debit

    nu_opt<=gamma epsilon/131072.

All decoded policies are physical on every record, including failures. Exactly as in the received root-risk transfer, on a correct fast acceptance and a good fresh bank,

    ell_fast<=(1+gamma/2)ell_star+27epsilon/32768
       <(1+gamma/2)ell_star+epsilon/1024.             (13)

If a policy is required also on rejection, run the received generic Sylvester-clipped ordinary learner on completely FRESH calls, at local parameters (gamma/2,epsilon/512). Its ideal expected Bell loss is at most (1+gamma/2)ell_star+epsilon/512 conditional on any rejected pilot/validation record. This is the identity-known-frame specialization of that received learner, not a new use of random output rotation in the row model. Its actual coefficient dimension is the known output k; no k=O(R) inference is required.

The rejection decision is made before the fallback data. Therefore one may multiply its uniform conditional guarantee by the rejection probability. For accepted histories use (13), debit the false-acceptance mass 2beta_0 once, and debit the fresh-bank failure mass at most beta_q once. Summing the two branches yields, for EVERY source with the declared actual known interface, without a rank-one or balance promise,

    E ell_selected
       <=(1+gamma/2)ell_star+epsilon/512+2beta_0+beta_q
       <=(1+gamma/2)ell_star+5epsilon/1024.           (14)

This argument does not divide by the acceptance probability or substitute a conditional product law for a mixture. A public record-dependent guarantee has not been obtained. Private-framed one-payload deployment plus one whole-process implementation discrepancy at most epsilon/2 gives the usual actual unhalved target (1+gamma)Delta_star+epsilon, capped at 2.

Without the generic fallback, (7) and (13) provide only a selective fast-route statement, not an unconditional relative learner on arbitrary sources. This distinction is essential.

## 6. Fast completion on the balanced exact-row subclass

One concrete candidate generator is the count pilot and rational acquired-anchor search of `ACQUIRED_BALANCED_ROW_ANCHOR_EXTENSION.md`, with the same count threshold T=ceil(2^18 L/kappa), beta_t=epsilon/512, and the slightly larger pilot cap

    N_pilot=ceil[2^44 dL/(kappa gamma epsilon)],
    L>=max{1,log(64d/beta_t)}.                        (15)

The correctness of Sections 1-5 does not import that candidate's pending theorem. For the subclass speed claim only, repeat its elementary argument: exact rows B_i=lambda_i u_i u_i^T have conditional gap 1/3, realized weighted direction error at most 4096dL/N_pilot, and discarded mass at most 2^22dL/(kappa N_pilot). If there exists a kappa-balanced anchor, the rational grid search succeeds on the pilot good event and returns the required estimated overlaps. On that event,

    Lambda<=gamma epsilon/2^22=Lambda_max/4,
    S=sum_{i in I}lambda_i sin^2 angle(u_i,v_i)
       <=4096dL/N_pilot<=S_max/256.                  (16)

Both validation tests then accept except probability 2beta_0. Thus this subclass completes along the fast route with probability at least 1-beta_t-2beta_0, using

    N_pilot+n_D+n_S+n_0+1
       =O_tilde((d+dr)/(kappa gamma epsilon))+1.     (17)

The same conclusion holds for any source/pilot law that produces the two stronger residual inequalities in (16) with the stated probability, without an exact-rank promise. No claim is made that every near-rank-one source or arbitrary unknown output basis does so automatically.

The deterministic worst-case cap reserves the fast acquisition costs PLUS the generic fallback's O_tilde(k^4/(gamma epsilon)) calls and one payload. Hence this is not a universal k^2 source theorem. The fast subclass statement is a high-probability actual-call bound, not a hidden expected stopping time or a claim that every bad pilot avoids the fallback. All output memory, classical searches, full-CPTP synthesis, sampler bits, learned kernel-direction controls and implementation errors are charged over the predetermined worst-case horizon. The source budget may stop early after fast acceptance, but the allowed maximum is fixed before data.

## 7. Governing accepted imports and scope

The unchanged received balanced-row source/receipt supply the finite count concentration, safe rational vector processing, Bures bank and decoder-control conventions. Its main source SHA is `421f3fdabfaff88e924346795f7d7aa63014549cb335db4b1c884abfdfe97083`; independent JSON receipt SHA is `66be88a3cedd8f54154a4173731b575d3c132ca6df418a7a1819b5cae34a6a27`.

The generic fallback source is `../ordinary_generic_matrix_gls_sylvester_clipping_20261028.md`, SHA `9454b204df34d302bf315bfe20afddc6ea5f109a8205bbd20f61b4de22c22c21`, with its received independent JSON receipt SHA `ff4f074e6b30ec8353dee6bf900d997f60ced914a2a5d2e57d7818b582ae12ef`. Its accepted local estimator and control dependencies are imports, not re-proved or physically executed here. The fixed known physical output basis allows the identity frame. The exact scalar local contract, rather than a theorem about a different postselection or public transcript, is used in (14).

The substantive new acquisition is (4): row-dependent, ordinary positive kernel probes make the learned approximation residual observable at a fast Bernoulli rate. The final decoder remains fully coherent. This neither grants coherent selector inputs nor measures the unknown payload in the pilot basis. Identically informed conventional learners can use the same procedure. No hardware practicality, generic spectral certification, quantum-over-classical advantage, or new generic k^2 rate is claimed.
