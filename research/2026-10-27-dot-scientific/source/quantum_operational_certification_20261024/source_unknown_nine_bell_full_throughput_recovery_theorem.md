# Nine learned Bell outcomes recover the original identity throughput

Status: separate new construction, pending independent receipt. This strengthens the per-DATA throughput, not automatically the rate per TOTAL channel use. It uses the ordinary classically labelled-training access model, not joint Choi programs at the receiver.

Assume the IID channel and trusted access promises of `source_unknown_classically_labelled_training_recovery_corollary.md`, p>=p0>0. Training randomness is discarded and independent of the data/reference. Let epsilon=sqrt[5(p+3q)Delta]. For every0<zeta<=1 an explicit finite programmed instrument has complete joint diamond distance at most

 zeta+6epsilon/p                                          (1)

from the ORIGINAL-rate ideal(p id,q erasure). All training states are consumed, and their count is below. No channel-model verification, reusable classical decoder, hidden-branch measurement, unassisted-capacity or practical-rate claim is made.

## 1. Actual orthogonal Bell family and teleportation correction

Let U_j, j=1,...,9 be the known qutrit Weyl unitaries. On the local qutrit C and received output B define
 P_j=(U_j tensor I)|Phi_V><Phi_V|(U_j* tensor I),
 Qcode=I3 tensor VV*.
Then P_j are pairwise orthogonal rank-one projectors and sum_j P_j=Qcode. The reset-cancelling Hamiltonians
 A_j=(U_j tensor I)A(U_j* tensor I)
    =pP_j-(p/9)Qcode
COMMUTE. Their common sectors are the nine one-dimensional P_j spaces and the outside sector I-Qcode. All A_j simulations can be obtained by known qutrit conjugations of the same sample-simulated A=4(T-omega); no additional unknown oracle is supplied.

Prepare a known local Bell pair |Phi3>_OC. An ideal P_j outcome on C,B contracts to
 bar(U_j)V*/3
on the retained logical O register. Correct by the known U_j^T, since U_j^T bar(U_j)=I. Each of the nine corrected outcomes therefore contributes V*(.)V/9. Summing all outcomes gives the exact ideal received-system accepted map
 Racc(X)=V* X V,
with rejected probability Tr[(I-VV*)X]. The factor9 gain comes from accepting all nine ACTUAL outcomes, not silently rescaling one postselection branch.

## 2. Nondestructive nine-classifier acquisition

Run a spectral classifier for EACH A_j while retaining C,B after every intermediate rejection. Do NOT use the erased-failure instrument from the one-projector theorem as a black box: intermediate tests here are their underlying nondestructive controlled-evolution/ancilla-measurement circuits. Decide only at the end: if exactly one classifier accepts, output that label and perform its transpose correction; otherwise erase.

For ideal controlled evolutions, every measurement operator is diagonal in the SAME common sectors above. If each classifier has spectral false-pass and false-fail probabilities at most eta, a true P_j sector is correctly labelled with probability at least1-9eta. On every sector orthogonal to P_j, the probability of the unique-j label is at most eta, since it requires classifier j to falsely accept. On the outside sector any incorrect label has total probability at most9eta.

This classical statement alone is not the quantum guarantee. For label j, its accepted Stinespring map restricted to the orthogonal complement of P_j has norm at most sqrt(eta), while its P_j acceptance coefficient lies in[1-9eta,1]. Because P_j is rank one, the full CP branch differs from P_j(.)P_j in diamond norm by at most
 10eta+2sqrt(eta)
(the P_j block costs9eta, the complementary block eta, and the two cross blocks2sqrt eta). Summing the nine labelled successful branches and then adding erased failure gives the conservative COMPLETE bound
 180eta+36sqrt(eta).                                    (2)
Known teleportation corrections, discarding C,B and forgetting the successful label cannot increase this distance. This proof includes arbitrary untouched reference systems; it does not assume that intermediate failures preserve all unknown coherences.

## 3. One explicit ordinary-labelled training budget

Choose eta=(zeta/100)^2 and k=ceil[162 p0^-2 log(1/eta)]. For each of nine classifiers use k Hadamard Y-tests as in the received theorem. There are H=9k controlled exp(i pi A_j) operations. Simulate each using
 N=ceil[512pi² H/zeta]
signed T/omega collision rounds. Its diamond error is at most256pi²/N; the H simulations together cost at most zeta/2. Formula(2) is at most(.36+.018 zeta)zeta<=zeta/2. Thus the entire learned Bell measurement/decoder differs from its ideal complete Bell counterpart by at most zeta.

The actual number of training calls is
 n_train=2 H N=18kN,
plus ONE data call per attempt. Every sample T and omega consumes one original channel use and T uses a known finite classical preparation label. Compared with the single-outcome construction, the larger number of classifiers also increases the required per-simulation accuracy: one must use this actual count, not claim a ninefold total-use rate gain.

A separately acquired coherent-phase implementation can instead replace the classifier tests with its explicit error and total-time allocation; no such optimization is a premise of this theorem.

## 4. Original source error and entropy charge

On the original channel the ideal full-Bell accepted map is
 p rho+q Tr(rho)V*tau V.
Its identity contribution is EXACTLY p id. The diverted reset mass is beta=qTr(V*tau V)=3Tr(PY), with Y=q tau/3. The received scalar-anchor trace bound gives Tr(PY)<=epsilon/p. Thus beta<=3epsilon/p. Relative to(p id,q erasure), the accepted extra replacer and missing erased reset contribute exactly2beta<=6epsilon/p. Adding the learned-measurement error zeta proves(1).

For Delta=0 the ideal full-Bell receiver is precisely the original erasure instrument, and this finite training construction approximates it arbitrarily well at the original per-DATA identity throughput p. Its per-TOTAL-use rate still pays n_train+1 channel calls per attempt. For general Delta the actual approximate acceptance need not be input independent; no normalized nonlinear operation is called a channel. The model-free low-dimensional holdout certificate applies to this fixed decoder with its new n_train, but any claimed certified rate must use that count.
