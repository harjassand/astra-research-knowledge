# Independent audit: complete-map convex compiler

5 November 2026. The accepted mixed-block, inverse-channel and classical
history-erasure results are inputs. This checks the proposed new compiler and
overlapping-interval schedule; it does not certify an arbitrary apparatus.

## Convex hull

Use normalized Choi matrices on input/output dimension d:

    K_d = {J >= 0 : Tr_out J = I_d/d}.

Its affine translation space is V_d={X=X†:Tr_out X=0}. If J_*>=a I, the
relative Hilbert-Schmidt ball of radius a about J_* lies in K_d, since
||X||op<=||X||HS. Let {J_j} be an r-net of K_d in Hilbert-Schmidt norm, and
let actual CPTP vertices satisfy ||J_j-Jtilde_j||HS<=e. For every unit u in V_d,

    h_conv(actual)(u) >= h_K(u)-(r+e)
                     >= <u,J_*> + a-r-e.

When r+e<a, separation proves J_* belongs to the convex hull of actual
vertices. There is no perfect final selector: every actual vertex must already
include the entire noisy word selection, execution, reset, and output map.

For R_sigma with sigma>=eta I/(2d), normalized Choi is sigma tensor I/d,
with floor eta/(2d²). For k qubits, D_gamma^tensor k has normalized Choi floor
gamma^k/d², using D_gamma=(1-gamma)Id+gamma Depol. For k<=B a uniform safe
radius is a=min(eta/2,gamma^B)/4^B. Norm conversions must be retained if the
net or physical estimates use diamond or trace norm instead.

## Schedule

Enumerate intervals of length ell=1,...,B and color their starts modulo ell.
Each color is disjoint. At most T=B(B+1)/2 rounds suffice, independent of N.
For candidate I, the desired map is R_sigma_I when I is a sampled block, and
D_gamma^tensor |I| otherwise. Both have interior Choi matrices.

Conditional on the partition, active blocks are disjoint and each site is
replaced once. Later active maps cannot touch an already prepared block.
Every later inactive desired map acts as a product of one-site depolarizing
channels, including across intended block boundaries. Therefore the later
channel restricted to any active block is a product channel. The accepted
full-rank leaf inverse supplies sigma_I for sufficiently small gamma.

This reasoning requires equality of complete channels on arbitrary external
references. Equality only on a special initialized input would fail. Actual
palette branches may couple all qubits of I even when I crosses intended
block boundaries: their exact mixture equals the inactive product channel.
This is the real composition improvement over a state-only factory.

## Implementation premises that must be closed

1. **Fixed support.** Every library word must act on the same predetermined
   input/output interval. Wrong selectors may select wrong maps but cannot
   silently address distant cells. Fixed wiring or a bounded local mux can
   enforce this. All wrong-address behavior within the support stays in the
   actual map.
2. **No old-record dependence.** An apparatus conditional on un-erased
   controller history has no single Choi map. Use the accepted uniform
   history-erasure coupling and pay its discrepancy across the campaign.
   Include the fresh noisy reference word law in each actual map.
3. **Finite physical library.** Every net channel has a finite Stinespring
   circuit using constant workspace for fixed B and radius. Compile to a
   finite native alphabet and bound maximal circuit length L. In the inherited
   independent Pauli model, fault-free coupling bounds map error by O(Lp).
   Selector, reset, padding, storage and delivery locations count toward L.
4. **Acquisition.** Unknown-SPAM process tomography does not identify an
   absolute laboratory channel without additional assumptions. The inherited
   homogeneous acquired Pauli model avoids this: acquire primitive parameters
   with the earned templates and compute every bounded circuit channel
   classically. Do not call an arbitrary unknown complete map calibrated
   without earning its observation model.
5. **Physical noise locality.** Parallel disjoint calls require the joint
   channel law supplied by the inherited independent location model.
   Cross-partition errors inside a scheduled interval are now allowed.
   Arbitrary long-range or context-dependent crosstalk is not eliminated by
   convex geometry. A larger fixed error support requires an explicitly
   enlarged cell/schedule analysis.
6. **Timing and coherent lifetime.** Complete classical sampling/control
   preparation before data reset. Pad every circuit to L. Run T fixed rounds.
   Raw program storage over this constant schedule has a further bounded
   acquired noise law. The synchronous native-circuit contract is explicit;
   this is not a proof of perfect timing or arbitrary continuous-time control.
7. **Records.** Palette choices correlated with the data give a different
   state-record extension. Erase them at paid cost when claiming a record-free
   Gibbs output, or retain and report the actual extension.

## Precision and resources

The convex decomposition is a fixed-dimensional linear feasibility problem
with strict margin. Finite-precision channels and coefficients are sufficient.
The vertices/dimension are constants only after B, eta, gamma are fixed.
Classical bit precision and control redundancy grow with requested global
accuracy. Per-call diamond error delta contributes at most O(NB delta) by
channel telescoping. Initial sampler and leaf-computation errors are separate.

The inactive Choi floor contains gamma^B. Conservatively the component rate
must satisfy p approximately below gamma^B/(4^B L), before other factors.
Gamma itself is constrained by block inversion, and L depends on a net at
that tiny radius. Thus this removes growth in coherent quantum resources; it
does not establish an accessible hardware threshold, favorable total spacetime,
or an advantage over ordinary quantum fault tolerance.

## Conclusion

No mathematical counterexample appears in the convex-hull or schedule logic
once these complete physical maps are earned. The strongest justified
implementation uses the inherited acquired stationary Pauli apparatus,
predetermined bounded support, and paid protected classical history erasure.
The operation directly addresses noisy random-mask composition while keeping
its locality, stationarity, timing, acquisition and enormous-constant limits.
