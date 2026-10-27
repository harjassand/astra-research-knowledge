# Robust relative-accuracy recovery without an extra inverse-p training factor

2026-10-27. New analytic extension, pending independent receipt. The exact-erasure construction remains frozen separately in `exact_erasure_relative_accuracy_quadratic_training_receiver.md`.

## Theorem

Use EXACTLY the same receiver, finite parameter choices, and consumed-training count as that construction, with requested0<eps<=1 and xi=eps/2. Now allow an arbitrary finite-dimensional replacement density operator tau, including coherence between the unknown code and its complement:

 E(rho)=p V rho V*+q Tr(rho)tau, p>=p0>0, p+q=1.

Let P=VV* and beta=q Tr(P tau). The complete unhalved diamond error from the original-rate ideal(p id,q erasure) is at most

 (5/8)eps p+4beta.                                    (1)

In particular, with the received source entropy quantity
 epsilon_ent=sqrt[5(p+3q)Delta],

 beta<=3epsilon_ent/p

implies the complete operational guarantee

 error <=min{2, (5/8)eps p+12epsilon_ent/p}.             (2)

The sample count retains p0^-2 times polylogarithms at fixed relative accuracy. The algorithm requires neither P nor beta nor Delta. These quantities enter the guarantee, not the controls. This is a statement for the fixed isometry-plus-replacer memoryless family, not model verification or an unrestricted hidden-bath channel.

The main issue is that small beta DOES NOT justify exact code-sector block diagonality of the actual programs. The proof below removes this obstacle by paired reset cancellation and a global sign symmetry; it does not insert unknown physical code measurements.

## 1. A valid interpolation through coherent reset states

Write

 tau_d=P tau P+(I-P)tau(I-P),
 tau_o=P tau(I-P)+(I-P)tau P,
 tau(z)=tau_d+z tau_o, -1<=z<=1.

Every tau(z) is a density operator: with S_B=I-2P,
 tau(z)=[(1+z)tau+(1-z)S_B tau S_B]/2.

The success isometry and p are fixed. In the discarded-label program model the two program derivatives are IDENTICAL:

 T'(z)=omega'(z)=delta=q(I3/3) tensor tau_o,
 d=||delta||_1=q||tau_o||_1.

The common reset part therefore cancels from the signed Hamiltonian at every z. Positivity and the Schatten Cauchy-Schwarz inequality give

 ||P tau(I-P)||_1<=sqrt[t(1-t)], t=Tr(P tau),
 d^2<=4q^2 t(1-t)<=4beta.                             (3)

These estimates include singular and noncommuting replacement states.

## 2. A derivative bound for one signed controlled-collision pair

Let C_(sigma,h) be the controlled partial-SWAP collision channel with fresh mixed program sigma, followed by discarding that program. It is linear in sigma. For a traceless Hermitian perturbation delta, denote its derivative by D_h(delta). Controlled unitary differentiation at h=0 gives

 D_h(delta)=h L_delta+R_h,
 L_delta(X)=i[Pi_1 tensor delta,X],
 ||L_delta||_diamond<=2d,
 ||R_h||_diamond<=2h^2 d.                              (4)

To justify the last bound without a small-angle asymptotic: write the collision unitary as exp(i h G), G=Pi_1 tensor SWAP, ||G||=1. The map appending delta has diamond norm d; each commutator with G costs at most2. The integral second-order Taylor remainder therefore costs at most2h^2d after partial trace. Tr delta=0 makes the zero-order derivative vanish. Also

 ||D_h(delta)||_diamond<=2|h|d,
 ||C_(sigma,h)-Id||_diamond<=2|h|                     (5)

by the corresponding first-order integral bound. All estimates allow untouched auxiliaries and references.

For one actual signed round define

 K(z)=C_(omega(z),-h) composed with C_(T(z),h).

At fixed z both factors are CPTP. Their shared derivative and opposite angle give cancellation of the entire first-order common-reset term. More explicitly, substituting(4) into K' and writing each CPTP factor as Id plus its difference from Id gives

 ||K'(z)||_diamond<=12h^2 d.                           (6)

The two first-order terms contribute at most8h^2d using(5), and the two remainders contribute at most4h^2d. Because individual collision channels are linear in their program,

 K''(z)=2 D_(-h)(delta) composed with D_h(delta),
 ||K''(z)||_diamond<=8h^2 d^2.                        (7)

There are no uncharged source-dependent gates between the two signed collisions of a round. Known qutrit conjugations may surround a controlled evolution and preserve all these estimates.

## 3. The complete logical receiver is an even function

Let F(z) be the entire original-source logical channel: prepare its training programs from E_(tau(z)), receive one independent E_(tau(z)) datum, run the fixed receiver, correct the successful Bell outcome, and erase otherwise. This is a CPTP channel for every z in[-1,1].

The sign S_B=I-2P fixes the isometry CHANNEL, because S_B V=-V, and conjugates tau(z) to tau(-z). Thus E_(-z)=Ad_(S_B) composed with E_z, and every corresponding program is conjugated by I3 tensor S_B. Simultaneous conjugation of the datum and all program receiver registers passes through every full-register SWAP, its controlled version, all control/phase processing, and every local qutrit gate. It disappears when the received C,B registers are discarded. The known logical output corrections and acceptance record are unchanged. Consequently, as complete logical channels including any untouched reference,

 F(-z)=F(z), and hence F'(0)=0.                       (8)

This is a mathematical covariance identity, not an available operation requiring knowledge of P.

Let H=sum_rounds h^2. The finite allocation of the exact-erasure receiver gives H<=xi/32. The derivative of the initial data channel has diamond norm d; its second derivative vanishes. Differentiate the circuit product, treating all known operations as diamond-norm-one CPTP maps. Equations(6)-(7) imply uniformly in z

 ||F''(z)||_diamond
 <=8H d^2 +(12H d)^2 +2(12H d)d
 =(32H+144H^2)d^2.                                  (9)

The three terms respectively charge one twice-differentiated round, two distinct once-differentiated rounds, and one differentiated round together with the differentiated data channel. The factor for distinct pairs is bounded by the square of the sum; all source-dependent factors remain CPTP on this real interpolation interval.

Using(8), the integral Taylor remainder, (3), and H<=xi/32 now give

 ||F(1)-F(0)||_diamond
 <=(16H+72H^2)d^2
 <=[2xi+(9/32)xi^2]beta.                             (10)

Thus neither a square-root-beta loss nor a factor equal to the number of training samples is incurred. The paired cancellation and global parity are both essential.

## 4. Receiving the pinched source, which need not be exact erasure

At z=0, all training programs commute with the code projector Q=I3 tensor P and have code-sector weight

 w=p+beta.

Their signed contrast and its ideal Bell projectors are unchanged: the replacement still cancels exactly. Thus the exact construction's code-restricted instrument error remains at most xi. Its virtual first-code-import calculation now has w instead of p, so a normalized outside datum is finally accepted with probability at most

 w xi/16 +p0 xi/16 <=(2p+beta)xi/16.

The source datum at z=0 has three positive branches: genuine encoded data of mass p, replacement inside the code of mass beta, and replacement outside the code of mass q-beta. The first costs at most p xi in complete channel error; the second costs at most2beta against erasure; and the third costs at most twice the preceding false-acceptance probability. Hence

 ||F(0)-(p id,q erasure)||_diamond
 <=(5/4)p xi+(2+xi/8)beta.                           (11)

No assumption that the pinched source itself has zero deficit is made.

Combine(10)-(11):

 ||F(1)-(p id,q erasure)||_diamond
 <=(5/4)p xi+[2+(17/8)xi+(9/32)xi^2]beta.

Since xi=eps/2<=1/2, the bracket is less than4. This proves(1), and the separately received entropy trace bound gives(2).

## Consequence and limits

For entropy defect small enough that epsilon_ent is a sufficiently small constant times p^2, this supplies a genuinely relative-accuracy recovery operation with the same p0^-2 polylogarithmic training dependence as the exact-erasure construction. Its worst-case inverse-signal exponent is constrained by the exact-erasure adaptive-query lower bound, since exact erasure is a subfamily.

This does not verify the source promise, eliminate the need for quantum memory and controlled SWAP access, give a practical constant, or resolve the optimal joint dependence on entropy defect and accuracy. Data/program independence is conditional on one fixed memoryless source. The guarantee is for the average over discarded training randomness, not every retained public training transcript.
