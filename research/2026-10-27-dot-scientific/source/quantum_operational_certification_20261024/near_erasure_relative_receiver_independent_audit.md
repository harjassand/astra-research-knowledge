# Independent receipt: coherent-reset robustness at quadratic training cost

27 October 2026, 02:55 UTC. PASS for near_erasure_relative_accuracy_quadratic_training_receiver.md.

This audit checks the extension beyond exact sector invariance. It does not apply the exact-erasure first-import proof directly to coherent programs.

## Valid source path and common derivative

The interpolation tau(z)=tau_d+z tau_o is the displayed convex mixture of tau and its code-sign conjugate for realz in[-1,1], so every source/channel/program along the path is positive and normalized. Both T and omega have the SAME derivative delta=q(I3/3) tensor tau_o. Its trace norm isd=q||tau_o||_1 and its trace is zero. Positivity gives||P tau(I-P)||_1<=sqrt(t(1-t)), so d^2<=4beta. No full-rank or commuting assumption is needed.

## Controlled-round differential estimates

The program-perturbation map appends delta, with diamond normd. The controlled full-register SWAP generator has norm1. Differentiating its unitary conjugation gives first-commutator bound2d and second-commutator bound4d. Integrating gives||D_h||<=2|h|d and the remainder bound2h^2d exactly, for arbitrary h and with auxiliary references. The zero-order derivative vanishes becauseTr delta=0; its first-order term is the commutator withPi_1 tensor delta.

For K=C_omega,-h composed withC_T,h, write the CPTP factors as identity plus their differences. The shared first-order terms cancel. The two first-order cross differences cost at most8h^2d and the remainders at most4h^2d, proving12h^2d. Linearity in each program givesK''=2D_-h composed withD_h and norm at most8h^2d^2. These statements require the paired collisions use the same control and have no intervening source-dependent gate; the actual receiver satisfies this. Known local qutrit conjugations preserve the common derivative.

## Exact parity of the COMPLETE channel

S_B=I-2P sendsV to-V and therefore preserves its isometry channel, while swapping tau(z) andtau(-z). Simultaneously conjugating the received datum and every fresh program by this SAME S_B passes through controlled and uncontrolled full-register SWAPs. Local qutrit gates and control/phase/record processing commute with that conjugation. Consumed programs are traced out, and the final received registers are also discarded. Logical output corrections and classical accept/reject records are unaffected. Thus the complete logical channel, with any external reference, obeysF(-z)=F(z).

This provesF'(0)=0 without physically performing an unknown-code operation. The identity would not follow from pinching only the datum while leaving training programs fixed; the proof correctly transforms both.

## Whole-circuit Taylor ledger

Group the actual paired collisions into rounds and putH=sum h^2. The circuit contains the data channel, whose first derivative has normd and whose second derivative vanishes. All intervening real-z channels are CPTP with diamond norm1. Single twice-differentiated rounds contribute8Hd^2; distinct once-differentiated round pairs contribute at most144H^2d^2; round/data cross derivatives contribute24Hd^2. Thus the full bound(32H+144H^2)d^2 is correct, and includes program copies' shared parameter dependence.

Evenness halves this bound in the integral Taylor remainder. WithH<=xi/32 andd^2<=4beta, it becomes[2xi+(9/32)xi^2]beta. There is no multiplier equal to the raw sample count and no square-root-beta term.

## Pinched source and final error

Only atz=0 is the exact code/exterior sector argument reused. Both programs have code massp+beta, while their signed Hamiltonian remainspP_j-pQ/9 because reset cancels. Code-input instrument error is still at mostxi. The outside-datum first-import bound usesp+beta, and the no-import repeated-test bound uses the unchangedp0. Its acceptance is at most(2p+beta)xi/16.

The data source has three positive branches: genuine code massp, replacement-code massbeta, and replacement-exterior massq-beta. Charging respectivelyp xi,2beta, and twice the exterior acceptance gives(5/4)p xi+(2+xi/8)beta. Together with the coherence Taylor term, the beta coefficient is2+(17/8)xi+(9/32)xi^2. On0<xi<=1/2 its maximum is401/128=3.1328125, below4. Therefore the claimed complete error5eps p/8+4beta is valid.

The earlier scalar-anchor trace receipt suppliesbeta<=3epsilon_ent/p with epsilon_ent=sqrt(5(p+3q)Delta), giving the stated entropy-controlled guarantee and optional universal cap2. That inference does not validate the source family or measure Delta; both remain promise/guarantee parameters.

The result preserves the exact receiver's p0^-2 polylogarithmic consumed-training bound and original ideal throughputp per data call. It covers arbitrary coherent/noncommuting reset within the fixed memoryless isometry-plus-replacer family, not unrestricted hidden memory, transcriptwise guarantees, free validation, reusable programs or generic Hamiltonian-simulation error improvement.
