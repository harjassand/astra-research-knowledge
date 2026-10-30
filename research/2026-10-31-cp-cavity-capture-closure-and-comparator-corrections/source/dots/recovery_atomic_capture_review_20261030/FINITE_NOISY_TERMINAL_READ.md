# Actual finite noisy terminal copy-out from physical record ports
30 October 2026. Optional classical read consumer. This uses the physical-port theorem, not a quantum-computation receiver. Local working result awaiting review.

The main theorem supplies simultaneous port-error projectors relative to the genuine historical outcome m, with parameter p. A mathematical measurement of those projectors is already a well-defined positive law, but it need not be mistaken for a free physical output. Here is an actual finite copy-out operation, including dirty targets and gate exposure.

## 1. Reset physical output targets
Attach one output two-level target per requested port, arbitrarily dirty and correlated. Run actual onsite zero resets for fixed duration tau_r, while record retention continues. Include that interval in its declared horizon H. The same reset subset-moment lemma supplies target-error law

 Tr(product_(j in S)T_j rho)<=r^|S|,

where r includes finite reset residual and the actual incident noise. The physical-port law still holds on this SAME joint state, since it is uniform in its arbitrary retained bath and extra target noise. No independence between targets, ports or bath is asserted.

The port projectors E_j and target projectors T_j commute. For any disjoint sets A,B of records, positive-state Cauchy--Schwarz gives

 Tr(E_A T_B rho)<=sqrt(Tr E_A rho Tr T_B rho)
                 <=p^(|A|/2) r^(|B|/2).

For the ideal CNOT output-error projector B_j=E_j XOR T_j, use B_j<=E_j+T_j and expand products. Consequently

 Tr(product_(j in S)B_j rho)<=q_w^|S|,
 q_w=sqrt(p)+sqrt(r).                                  (R1)

This conservative square-root loss is real in this proof. It is not labeled independent read noise or silently replaced by p+r.

## 2. Actual bounded-strength copy gate
For this TERMINAL read, pause classical-majority service during a fixed-duration parallel layer of actual port-to-output CNOTs. A finite Hamiltonian on each control-target pair implements the ideal gate; the physical root is a control. Gate strength, duration and per-site incidence are fixed. The pause is explicit, not treated as continued protection. No further retention guarantee after this terminal operation is asserted here.

In the ideal partial-gate interaction picture, the output B_j are commuting bounded-cone defect projectors. The initial warm exponential moment from (R1) is

 Tr exp(theta sum_(j in S)B_j)rho
 <=[1+q_w(e^theta-1)]^|S|.

The accepted positive subset-moment source calculation, with the finite gate's actual lightcone/incident-norm inflation, gives during its duration tau_c

 (d/dt) moment <= C eta e^(a theta)|S| moment,

where a,C are fixed by the bounded system-leg model and gate layer. All other record/bath systems remain part of the retained bath. The paused nominal classical generator contributes nothing; arbitrary bath-only evolution annihilates these tests. There is no total-storage-volume cost.

Exponential Markov gives the ACTUAL physical output-target law

 Pr(all output targets in S are wrong)
 <=[ e^(-theta)(1+q_w(e^theta-1))
                         exp(C eta tau_c e^(a theta)) ]^|S|.   (R2)

For (a C eta tau_c)^(1/a)<=1, choosing e^(-theta)=(a C eta tau_c)^(1/a) yields the convenient bound

 p_out <= e^(1/a)[sqrt(p)+sqrt(r)+(a C eta tau_c)^(1/a)].    (R3)

The eta=0 case follows by theta tending to infinity. Cap any displayed parameter at1 if necessary. Reset duration and noise threshold can be chosen so p_out is a desired small fixed constant. This does not inherit an independence-in-time claim.

## 3. Scope of physical reading
The output consists of actual physical qubits whose joint Z-error distribution is bounded by (R2), after finite noisy reset/copy operations. A supplied final Z measurement instrument preserves these probabilities if ideal; any detector imperfections need their own declared finite local instrument/noise contract, which can be added to the final source layer when its positive-subset-moment hypotheses apply. This note does not build a macroscopic detector from first principles or claim error-free external classical software.

One can instead use roots directly as Z-diagonal controls, as the main classical theorem allows. Correct quantum DATA under those time-correlated controls requires the separate quantum-consumer proof. Repeated nonterminal output operations, autonomous scheduling and native two-site compilation of the storage majority remain separate. The present finite copy-out gates themselves are ordinary two-site gates, but that does not change the storage hardware's bounded-body resource setting.
