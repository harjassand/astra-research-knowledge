# Independent review: deterministic certified perturbation direction
2026-10-29. Additive mathematical strengthening; actual universal-template implementation remains absent.

## Decision
Accepted: the explicit rational quartic G in the frozen input is a nonzero point of the degree6972 bad-polynomial complement. Consequently6973 predetermined small rational perturbations along G guarantee a good trial for every rational input quartic. At the already-reviewed fixed-template scope this yields deterministic termination and polynomial BIT complexity, not merely almost-sure expected complexity. It requires no random retry or grid totalization. This does not claim the generic template has been executed, that the fixed-z heuristic is complete, or that the large constants are practical.

## Independent modular witness
The characteristic-zero shape and full projective critical-point coverage were independently accepted in the Choi–Lam instance review. Here I independently parsed that exact shape and recomputed the finite-field proof using separate low-to-high polynomial convolution, division and extended Euclid, rather than importing the author's polynomial routines. The modulus1000000007 was verified prime by exhaustive trial division through its integer square root. All rational denominators used in specialization were checked nonzero modulo the prime.

The univariate shape has degree40 and is squarefree modulo the prime. The norm class `N=1+P(z)^2+Q(z)^2+z^2` has a verified inverse. The normalized objective `lambda=(partial_0 G)/(4N)` agrees with the author's stored coefficient vector. The40-column Krylov matrix1,lambda,...,lambda^39 has independently computed determinant438433815 modulo the prime, nonzero.

These are nonzero witnesses over Q, not assumptions that every modular property lifts indiscriminately. Invertibility of the norm multiplication matrix modulo the prime implies its rational determinant is nonzero. Its rational inverse therefore specializes correctly. Every Krylov entry is then the specialization of the corresponding rational algebra element; the nonzero modular determinant implies rational full rank.

The rational shape algebra is already known to be reduced of dimension40. After extension to C it is C^40, and powers of lambda can span40 dimensions only if its40 component values are distinct. Thus G has40 distinct normalized critical values, with all40 rays nonisotropic. No extra unseen critical rays exist by the exact chart and boundary coverage.

For clarity, nonvanishing of R_G does not require a hidden converse about regular tensors: if it were identically zero, every complex lambda would have a common projective root of the four restricted cubics. Each such root is one of the40 covered critical rays; since N is nonzero on each, each ray supplies just one lambda. A finite set cannot cover all lambda, contradiction. Universal degree≤40 and40 distinct roots then imply degree40 and nonzero discriminant. The independently replayed boundary-resultant witness gives B(G) nonzero. Hence Delta(G) is nonzero.

## Deterministic trial proof
The prior accepted factors are homogeneous: c40 has degree68, the resultant discriminant has degree6864, and B has degree40. Their nonzero product Delta is homogeneous of degree6972. Therefore Delta(F+tG), for arbitrary F, has leading coefficient Delta(G), which is nonzero, and at most6972 distinct zeros.

Let A be the exact positive coefficient l1 norm of G. The6973 values `t_j=j epsilon/(4A*6973)` are distinct positive rationals and each satisfies ||t_j G||coefficient,l1≤epsilon/4. At least one trial is good. Its perturbed global interval width≤epsilon/2 transfers to the original objective with width≤epsilon. This is an all-input deterministic statement, not a statistical extrapolation from one successful perturbation.

The number6973, G, and all template degrees are fixed constants. Input and accuracy bit heights grow only polynomially under these rational shifts; each of the fixed number of exact template trials has the previously proved polynomial-bit bound. Thus the theoretical construction has deterministic polynomial bit complexity. No actual6973-trial run is asserted.

## Source-clock and implementation boundary
Removing the random retry tail removes a real mathematical obstacle to deterministic finite padding. Given a supplied template implementation, an upper bound based on public horizon/input-size limits can bound every trial and the whole finite list, instead of exposing a private hard-instance stopping time. Nevertheless the constants may be astronomical; an abstract bit-operation bound is not a calibrated physical wall-clock, memory-buffer, gate-synthesis or source-isolation guarantee. The current package does not instantiate the complete four-cubic template/extractor, so this is not an implemented fast controller or a measured latency gain. Equally informed conventional optimizers can use the same construction.

The independent checker initially encountered Python's integer-string safety limit while parsing the trusted large exact shape; it was rerun with that formatting limit disabled. This was a parsing issue, not a failed mathematical witness. The preserved final checker/log/data contain the successful exact computation.
