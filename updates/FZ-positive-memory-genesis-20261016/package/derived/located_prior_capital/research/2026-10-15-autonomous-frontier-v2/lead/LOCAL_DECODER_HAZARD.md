# From an instantaneous component tail to a logical lifetime

Status: deterministic local stability and Poisson hazard reduction reconstructed
by the principal investigator, after Q1 proposed the route. This does not supply
the required component tail. Historical originality is not established.

Work over F2 on the side-L four-dimensional cubical torus. A sector's accumulated
error is a 2-chain E; its measured syndrome is s=boundary(E). Fix an ambient
lattice graph metric. Every physical fault or correction adds a 2-chain F whose
vertices lie within distance a of an anchor, where a is independent of L.

## Fixed decoder

Choose r=L/64 and R=L/8, with L large enough that a<r. For each connected
syndrome component of diameter less than R, lift it uniquely to a small coordinate
box, choose a deterministic filling inside that box, and project the filling
back to the torus. A lexicographic choice suffices; no efficiency is asserted.
When all components are small, D(s) is the sum of these fillings. Otherwise use
a fixed global filling of the entire boundary syndrome. Set D(0)=0. Thus D is
defined from the syndrome alone, without access to hidden trajectories.

The choice for a small component depends only on that component, so an identical
unaffected component has an identical filling before and after an event.
Graph-connected components of diameter below R<L/4 have consistent bounded
lifts: a winding path would have to visit coordinate positions separated by
L/2. Each such component is a 1-cycle and bounds inside its contractible box.

## Deterministic local stability

Suppose every pre-event component has diameter less than r. Put W equal to
the vertices of boundary(F). Components changed by toggling boundary(F) must
meet W; unaffected components and their chosen fillings cancel in

    F + D(s) + D(s + boundary(F)).

Each affected old component lies within distance a+r of the anchor. Each
affected new component is assembled only from these old components and the
local boundary(F), so its diameter is at most 2(a+r)<R. The old and new
fillings, as well as F, all fit in one injectively embedded coordinate cube
of side at most 2(a+r)<L. Their sum has zero boundary. The cube has trivial
second homology, hence this sum is a stabilizer boundary. If boundary(F)=0,
the same conclusion follows immediately from the bounded support of F.

Consequently the decoded homology class [E+D(boundary(E))] cannot change at
such an event. Starting from E=0, a first logical change requires a pre-event
syndrome component of diameter at least r. This argument tracks accumulated
membranes; it does not assume that a small current syndrome implies small E.

## Continual Poisson noise and correction attempts

Let B_L(u) be the probability that a sector has a component of diameter at
least r at deterministic time u. Count all independent vertex attempts,
including null attempts, rather than only state-dependent accepted jumps.
If the total attempt intensity is at most K L^4, the Poisson compensator gives

    P(first decoded logical change before T)
       <= K L^4 integral_0^T B_L(u) du.

The integrand is the pre-jump state. Independent constant-rate primitive
clocks justify this use of the compensator; it is not an assertion that
adaptively selected syndrome components have independent clocks.

For the exact two-sector Lindblad model from the previous campaign one may
take K=2*kappa+6*(lambda_X+lambda_Y+lambda_Z) before harmless constant
overcounting. A uniform bound B_L(u)<=C L^4 exp(-c L^beta), beta>0, would imply

    P(logical failure by T) <= C K L^8 T exp(-c L^beta).

Polynomial factors can be absorbed into a slightly smaller exponential
constant. This would yield a stretched-exponential memory lifetime from
arbitrary freshly encoded logical/reference states. Y correlations do not
invalidate the union bound over sectors.

## Quantum and physical scope

The specified syndrome-projector-conditioned Pauli jumps and independent
Pauli data faults admit a Pauli-trajectory decomposition from a code-space
input. A stabilizer residual acts trivially on every logical state, including
entanglement with a reference. With perfect final syndrome readout and the
fixed decoder, unhalved logical diamond distance is at most twice the bad
trajectory probability. There is no syndrome observer during storage.

The readout is ideal and may be computationally expensive. This does not
establish a noisy-readout threshold, robustness to arbitrary Lindblad
perturbations, a three-dimensional physical implementation, or fabricated
conditional multi-qubit dissipators. The instantaneous large-component tail
for the actual asynchronous process is the outstanding mathematical premise.
