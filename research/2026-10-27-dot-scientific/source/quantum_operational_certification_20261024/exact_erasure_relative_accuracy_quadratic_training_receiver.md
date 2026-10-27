# A relative-accuracy exact-erasure receiver with quadratic inverse-signal training

2026-10-27. New explicit construction, pending independent receipt. This uses only the ordinary discarded-label T/omega training access, controlled output-register SWAPs, known qutrit gates, and the same memoryless-source/data-independence promises as the received programmed decoder. It does not require the unknown code projector as an operation. All training is consumed anew per data attempt.

## Theorem

Let E(rho)=p V rho V*+q Tr(rho)tau with V:C3->B isometric, p+q=1, p>=p0>0, and tau V=0. Thus the source has EXACT zero original entropy deficit. The finite output register is accessible, but V, tau, p and the code are otherwise unknown. For every relative-error request0<eps<=1, the construction below has complete UNHALVED diamond distance at most eps p from

 (p id, q erasure).

It uses the original identity throughput p per DATA invocation, includes all rejected runs, and consumes

 N_train <=1024 S^2/xi +18 L r m                         (1)

training channel calls plus one data call, where

 xi=eps/2,
 L=max(1,ceil(log_16[144/(p0 xi)])),
 eta=(xi/(100 L))^2,
 M=2^m is the smallest power of two with M>=144/p0,
 r=ceil(log_2(1/eta)),
 S=9 L r pi(M-1).

For fixed relative eps, the inverse-signal dependence is p0^-2 times polylogarithms in1/p0. This matches the received worst-case p^-2 lower exponent for meaningful complete recovery, up to logarithmic factors. It is NOT an optimal joint error/signal theorem, a practical resource claim, an unassisted quantum capacity, or a reusable decoder. Gates and memory width still depend on the output register size.

## 1. Source sectors and the nine ideal Bell projectors

Use a local qutrit C and the received output B. Put

 Q=I_C tensor VV*,
 P_j=(U_j tensor I)|Phi_V><Phi_V|(U_j* tensor I), j=1,...,9,
 A_j=p P_j-(p/9)Q,

where U_j are the known qutrit Weyls. The P_j are orthogonal rank-one projectors and sum to Q. The nine A_j commute, with common sectors P_1,...,P_9 and I-Q. The exact-erasure training states T and omega are block diagonal for Q, each having code-sector weight Tr(Q T)=Tr(Q omega)=p. As before, A=4(T-omega), and known C-only conjugations implement the A_j versions.

Prepare the known Bell pair on logical output O and local C. Ideal measurement of all P_j, followed by the known U_j^T correction on O and erasure if no P_j occurs, implements accepted map V*(.)V. Thus on the original source its complete channel is exactly(p id,q erasure). The code projector Q is only an object in the proof, not a gate supplied to the receiver.

## 2. Actual repeated spectral classifier

For EACH j, run L independent nondestructive spectral classifiers for A_j. Keep C,B after every outcome. Use the finite QPE classifier from `source_unknown_qpe_training_cost_improvement.md`: M grid points for exp[i pi(A_j+I/9)], r repetitions and majority classification. All r QPE repetitions and all L classifier instances use fresh independent training states.

Each ideal-evolution classifier has false-pass and false-fail probability at most eta on EVERY relevant eigenstate, using the received wrap-safe threshold. Its controlled A-times are t_a=pi 2^a, a=0,...,m-1, repeated r times. Scalar phases are known local operations.

Run ALL9L classifiers, retaining every classical result. A label j qualifies only if ALL its L classifiers accept. If exactly one label qualifies, accept and apply its known transpose correction. If zero or more than one qualifies, erase. No intermediate rejection discards C,B, and no merely erased-failure instrument is used as a black box.

For every controlled time t allocate

 N_t=ceil(512 t S/xi)

signed T/omega collision rounds, with one fresh T and one fresh omega per round and respective collision angles +4t/N_t and -4t/N_t. Their conjugated versions have the same sector weight p. Total controlled A-time is S. The received elementary diamond simulation bound256t^2/N_t implies

 total simulation error <=xi/2,
 simulation error for ONE classifier <=xi/(18L).         (2)

The count2sum N_t gives(1). Moreover the sum over ALL elementary collision angles h_l satisfies the additional exact budget

 sum_l sin^2(h_l) <=sum_l h_l^2
 =sum_controlled_times 32t^2/N_t <=xi/16.               (3)

This source-sector budget, not an unproved improvement of the uniform diamond simulator, is the new ingredient.

## 3. Code-input quantum instrument error

For exact controlled evolutions, every classifier Kraus operator is diagonal and scalar on each P_j. On sector P_j, the chance that j fails to qualify is at most L eta. Each other label qualifies with probability at most eta^L. The independence is conditional on the common eigenstate sector, on which nondestructive ideal QPE leaves the data state unchanged. Consequently correct label j has probability at least1-L eta-8eta^L.

On the code complement Q-P_j, the probability of label j is at most eta^L. This is a uniform operator bound, since the ideal measurement is diagonal in the shared orthogonal sectors. For the accepted j Stinespring map, the complement restriction has norm at most eta^(L/2). Decomposing an arbitrary reference-assisted input into P_j and Q-P_j blocks bounds the diamond error of that accepted CP branch by

 L eta +9eta^L+2eta^(L/2).

Here the diagonal P_j block costs at most L eta+8eta^L, the complement block costs at most eta^L, and the two cross blocks cost at most2eta^(L/2). Summing nine branches and adding erased failure gives complete code-restricted instrument error at most

 18 L eta+162eta^L+36eta^(L/2)
 <=180L eta+36sqrt(eta)
 <=.378 xi <xi/2.                                     (4)

This is a quantum CP/diamond argument, not an inference from classification probability alone. Known Bell contraction, corrections and discarding registers do not increase the distance. Adding(2), the ACTUAL receiver on arbitrary code input, including an untouched reference, differs from the ideal deterministic inverse by at most xi.

## 4. Controlled-collision sector invariance and first code import

Let rho be one fresh program, commuting with Q and with Tr Qrho=p. Write a joint data/control state in control blocks Omega_ab. Suppose every Omega_ab commutes with Q. A controlled partial-SWAP with angle h, followed by discarding its program, maps the diagonal control blocks as

 Omega_00 -> Omega_00,
 Omega_11 -> cos^2(h)Omega_11+sin^2(h)Tr(Omega_11)rho
             +i sin(h)cos(h)[rho,Omega_11],

up to the immaterial common sign convention. Off-diagonal blocks are cos(h)Omega_01 minus i sin(h)Omega_01 rho, and its adjoint counterpart. Thus EVERY resulting block still commutes with Q. The same reasoning holds with arbitrary auxiliary/reference registers: partial traces replace scalar traces, and the Q-commutation conclusion is unchanged.

The total code population changes by exactly

 sin^2(h)[p Tr(Omega_11)-Tr(Q Omega_11)],

because the commutator has zero Q trace. In particular, conditioned on the data still being outside Q, the probability of entering Q at this collision is at most p sin^2(h). Control gates, phase gates, classifier-record processing and C-only Weyl conjugations preserve Q; none imports code weight.

Starting with an outside input, the data and all retained ancillas remain jointly block diagonal between Q and I-Q after each consumed-program collision. Therefore inserting mathematical Q/(I-Q) sector measurements at those points leaves the actual circuit unchanged. These are VIRTUAL measurements for analysis only, not a protocol step. They define a legitimate classical first-import history. By(3), the total probability of EVER importing code is bounded by

 Pr(any code import) <=p sum_l sin^2(h_l) <=p xi/16.    (5)

This carefully distinguishes code import, which is suppressed by p, from code leakage to reset, which need not be suppressed by p.

## 5. False acceptance without code import

On an arbitrary outside-sector input, including arbitrary ancillary correlations, an ideal single classifier accepts with probability at most eta, since A_j=0 on the entire outside space. Its actual complete nondestructive implementation differs by at most xi/(18L) in diamond norm by(2). Thus its acceptance probability is at most

 beta=eta+xi/(18L) <1/16.                             (6)

Restricting to the CP histories which do NOT import code can only decrease this unnormalized probability. Between classifiers the retained normalized state on each such history is still outside Q, so the same bound applies again, whatever earlier classifier records occurred. For a fixed label j, the probability of all L required accepts with no import is at most beta^L. Intervening classifiers cannot increase trace mass. Therefore

 Pr(final accept and no import) <=9beta^L
 <=9(1/16)^L <=p0 xi/16 <=p xi/16.                    (7)

Combining(5) and(7), a reset datum is accepted with probability b<=p xi/8. This argument explicitly pays errors that import code and would fool every later repeated test; such errors are NOT assumed to disappear on repetition.

## 6. Complete original-channel receiving

The source data input is a mixture of its code branch of weight p and its independent reset branch of weight q. On the code branch the complete receiver error is at most xi by(4)+(2). On the reset branch the ideal output is erased, and the actual known output flag is classical. Its complete trace/diamond deviation from erasure is exactly2b. Consequently

 ||receiver composed with E - (p id,q erasure)||_diamond
 <=p xi+2q b <=p xi+p xi/4 =5p xi/4
 =5 eps p/8 <=eps p.                                  (8)

The surplus numerical margin is intentional. The channel is stationary and memoryless conditional on its fixed source; programs are independent of the data/reference. This is not a statement about unrestricted hidden-memory channels, unknown exact-erasure validity, or near-erasure sources with a small nonzero deficit. The existing model-free holdout machinery may independently test a fixed implementation, but every per-total-use rate must charge(1) plus its data and validation calls.
