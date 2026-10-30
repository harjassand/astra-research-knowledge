# Ordinary scheduled Tanner memory with noisy local classical processing
2026-10-30. Constructive adaptation of existing single-shot decoding and circuit analysis; no novelty or priority claim. This removes an unnecessarily strong comparator assumption, not the autonomous timing problem.

## Result first
The reliable-classical-processing assumption of arXiv:2610.03684 is not needed for its fixed-iteration MEMORY cycles if the classical decoder is implemented as the bounded-degree local circuit actually described by the Tanner parallel algorithm. Add its noisy gates, record cells, communication and correction controls to the same local-stochastic fault-path model, apply corrections physically, and reset all round scratch. A classical fault has only a constant-sized forward light cone. It therefore changes only O(1) physical correction bits, and the ordinary contraction/error-span proof survives with worse constants.

The implementation uses O(N) classical cells and O(N) classical gates/communications per fixed-duration round, in addition to O(N) quantum resources. It does not require exponentially reliable individual classical gates, a growing concatenated classical code, or a persistent global Pauli frame. It STILL requires an externally scheduled circuit, bounded physical communication times along the decoder graph, and enough parallel hardware. Global clock failure or one faulty unbounded-fanout bus is not a local fault in this model.

## 1. Primary algorithms and the exact dependency graph
Gu et al., arXiv:2306.12470, Section 4.1 and Algorithms 3–4, give the actual local dependency structure; Theorem 4.20 gives the contraction. The local code length w=Delta^2 is a fixed constant.

1. At each local-check vertex v, a finite lookup maps that vertex's O(w) syndrome bits to a local minimum-weight mask epsilon_v. This is an exhaustive fixed-size table, not a global decoder.
2. The initial mismatch bit at a square q is the XOR of its TWO incident relevant local masks. The four correction-accumulator vectors initially contain zero.
3. Each parallel iteration has FOUR sequential vertex-color substeps V_00,V_01,V_10,V_11. At a vertex, a finite lookup reads the mismatch on Q(v), selects a local codeword and its row/column decomposition, and updates mismatch and accumulators on Q(v). Within a fixed color, the views Q(v) partition the square set, so there is no unbounded concurrent fan-in at a square. Different colors are serialized.
4. The final correction bit is an XOR of the local initial guess and two local accumulated bits. It is not a global parity or broadcast.

For a fixed iteration count j, synthesize every fixed table into a fixed bounded-fanin Boolean circuit. A large but fixed fanout can be replaced by a fixed tree of copying gates. Send a square's value only to its bounded number of neighboring vertex processors. Hence there are constants D_c,F_c,q_c, independent of N, such that classical depth is at most D_c, fanout at most F_c, gate arity at most q_c, and total live bits/gates O(N). A conservative per-location correction-output light-cone bound is q_c max(1,F_c)^(D_c+1). Constants may be enormous in the fixed local code degree and chosen j; no numerical threshold claim follows.

This claim concerns a FIXED number of parallel iterations. The complete O(log N)-iteration final decoder has growing dependency cones and is not covered by the same constant-spread argument.

## 2. Actual classical gates rather than a coherent shared bus
A nominal classical gate with input x and output f(x) is the CPTP map

    Gamma_f(rho)=sum_x <x|rho|x> |f(x)><f(x)|.

For retained inputs, replace f(x) by (x,f(x)); copying acts only on classical basis information. A wire, fresh record initialization, and bounded fanout copy are included as circuit locations. A classical send across laboratories measures its source in the message basis and prepares that basis value at its destination; it is not a coherent quantum wire. A correction-control gate first reads its basis bit and applies the designated local Pauli. These maps can be physically realized by local measurements, local computation/reset and classical communication. Exact ideal locations are a scheduled-circuit specification, not a promise that the actual gates never fail.

A faulty location may be an arbitrary CPTP operation on its bounded operands and a retained bath. Record faults may introduce quantum coherence; the next nominal basis-reading gate dephases it. More generally, expand the local faulty operator in matrix units and retain the bath coefficients. The resulting coefficients follow ordinary classical paths through every fault-free compute gate. Nothing in the support argument requires the internal fault to be a stochastic bit flip.

## 3. Deterministic decoder-output fault bound
Fix one actual fault-location set F in a round, and let K=|F|. Select any compatible coefficient history from the local operator expansion, with an actual observed syndrome y. Compare the actual correction mask f_tilde with the output f(y) of the fault-free classical circuit on THAT same y.

Outside the union of forward classical cones of faulty classical locations, every wire has the same value in the two computations. This follows by induction on circuit depth; an ideal deterministic gate with unchanged inputs has unchanged outputs, regardless of nonlinearity. Therefore

    |f_tilde+f(y)| <= c_c K.                         (1)

The bound uses one common cone union determined by F, not a separate probabilistic bit-error model. Faults in quantum syndrome extraction give y=sigma(e)+m with |m|<=c_s K and a bounded data increment. Faults while computing, sending, waiting or applying the final mask give an additional data Pauli of reduced weight <=c_l K. All cells are discarded/reset at the next round, so no old corrupted bit secretly fans out across indefinitely many rounds.

Apply the decoder's reduced-weight contraction to f(y), then add (1). If r is the sum of the reduced weights of the two CSS error components, there are constants A,B,C,beta,c_d,c_s,c_l,c_c such that

    A(r+c_d K)+B c_s K <= C N

implies

    r_out <= alpha r + H K,
    H=alpha c_d+beta c_s+c_l+c_c.                    (2)

The same argument works for the relative error of the bilateral Bell buffer. Physical mask application is essential to this simple formulation: merely accumulating a long-lived, unprotected software Pauli-frame register would reintroduce a classical memory obligation.

## 4. Fault-path probability and coherent recovery
Choose j so alpha<1, then choose a small fraction eta>0 and rho=H eta/(1-alpha) so that

    2 rho N < d_N,
    A(rho+c_d eta)+B c_s eta < C.

Every round with at most eta N faults leaves r<=rho N, by induction from the exact encoded state or a comparably small initial residual. A round contains at most c_0 N locations counting BOTH quantum and classical gates, local communication, reset, and waits. For an input-independent local-stochastic location set of strength p,

    Pr(K>eta N) <= binom(c_0 N, floor(eta N)+1)
                        p^(floor(eta N)+1)
                   <= C_1 exp(-c_1 N)

at sufficiently small fixed p. No independence between rounds is required. Over S rounds the bad-event probability is <=C_1 S exp(-c_1 N).

For every good fixed fault path, keep all environment/Kraus coefficients and actual measurement records. Equation (2) holds coefficientwise, so all error operators are in the same stabilizer-reduced correctable span E(rho N). The usual distance/Knill–Laflamme argument gives one fixed ideal recovery for the ENTIRE span, retaining all interference and logical/reference entanglement. Averaging over actual good/bad fault paths gives

    ||R P Enc - id||_diamond <= 2 C_1 S exp(-c_1 N).   (3)

For the bilateral known-Bell resource replace this arbitrary-logical identity recovery by the relative-syndrome recovery and matched signed-sector decoder; the logical Bell target factors from its gauge/reference. It is not a theorem protecting arbitrary inputs in the enlarged two-party target space.

This adaptation tolerates arbitrary coherent local operations CONDITIONED ON classical faulty locations. It does not cover small coherent deviations at every location unless a separate positive fault-record representation is supplied. Nor does it autonomously generate the circuit schedule.

## 5. What this changes in the comparison
Bharti et al., arXiv:2610.03684, explicitly assume reliable classical processing and records in Section 2.1 and give the coherent common-span/fault-count proof in Sections 3.2–3.5. The above adaptation changes their classical implementation and enlarges their counted location set; it does not improve the asymptotic O(N) hardware/work per constant-time round or O(SN) total spacetime cost. Its natural interpretation is that the ideal-classical assumption is removable for these LOCAL FIXED-ITERATION memory rounds under a comparable local-stochastic hardware model.

Therefore a fair ordinary comparator should be granted a noisy scheduled local classical circuit, not artificially forced to rely on perfect classical gates. The interesting difference of the autonomous construction remains its internally generated timing/service and its precisely reviewed continuous-noise or native noisy-controller scope, not a generic claimed inability of scheduled single-shot recovery to tolerate classical gate faults.

What is not removed: long-range connectivity costs; finite propagation time; a robust global schedule; arbitrary unknown-state initialization; physical bare-output error floors; final O(log N)-depth classical decoding reliability; selective logical addressing; magic states; general universal computation. Those remain separate interfaces or resource assumptions.

Primary texts inspected:
- https://arxiv.org/html/2306.12470 , Section 4.1, Algorithms 3–4, Theorem 4.20.
- https://arxiv.org/html/2610.03684 , Sections 2.1–2.3 and 3.1–3.5.
