# Receiving review: finite event-memory transport and load response

30 October 2026. Existing physical-mechanism role. Root's file was not edited. No new helper or numerical fixture was used.

## Actual input and disposition

Reviewed `EVENT_MEMORY_AND_BALANCED_TRANSPORT.md`, SHA256
`e9ef100fa72a8c4ffeb2ac73d2ddd281ce70a1603f38e52270f5fddbebf5b0aa`.
An exact snapshot and input metadata are preserved alongside this review.

**Accepted at its stated finite-system interface.** I found no required correction in the balance/martingale theorem, equilibrium variance, supplied-load stationary law, two-state current/activity cell, or several-independent-bits extension. In particular, the file already contains the two critical scope restrictions requested for this review: unknown *selected* kinetics are not granted, and suppression of equilibrium current variance is accompanied by suppression of response to the stated circulating force.

This is not acceptance of an apparatus, a finite-latency implementation, a stationary initializer, a hidden-rate acquisition theorem, a full spatial action, unchanged density relaxation, or a physical covariance rotation obtained by merely relabeling outputs.

## 1. Exact balance and the conditional current identities

Vertex balance implies sum_e c_e(eta_x-eta_y)=0 for every occupancy configuration. This statement is algebraic and remains true along arbitrary unselected dynamics. On active selected edges, delta_e is plus or minus one. Expanding

\[
c_e(1+\alpha u\delta_e)(\delta_e-\alpha u)
=c_e(1-\alpha^2)\delta_e
\]

and summing proves zero conditional drift. Expanding the squared increment gives

\[
\sum_e c_e(1+\alpha u\delta_e)(\delta_e-\alpha u)^2
=(1-\alpha^2)\sum_e c_e\delta_e^2.
\]

Thus M is genuinely the raw sum of corrected increments; a compensator has not been omitted. The selected intensity is bounded on the finite graph, so square integrability follows even if the unselected hidden state space is large, provided the declared full process is nonexplosive.

Every counted selected event reverses u and every uncounted event leaves u unchanged. Therefore
\(\sum_{\rm selected}u_{v-}=(u_0-u_t)/2\), proving the current identity pathwise. Null attempts cannot be counted as bit-changing events; the text explicitly excludes them.

At alpha=1, the support condition itself implies delta_e=u_pre whenever a selected event has positive rate. The corrected increment vanishes. The bound |J|<=1 is therefore insensitive to arbitrary positive reweightings of permitted transitions, including nonstationary or hidden-dependent rates. It does not follow that such reweightings preserve equilibrium or density transport. The source makes exactly this distinction.

## 2. Reversibility and what hidden kinetics may remain unknown

For a selected joint transition, simultaneous reversal of occupancy and bit sends (u,delta_e) to (-u,-delta_e). Their product is unchanged. The stated equality nu(eta,z)=nu(eta^e,z) consequently gives detailed balance in nu times the fair bit. Each unselected channel is separately reversible in nu at every fixed bit and hence preserves the same product law. Irreducibility is unnecessary for this stationarity assertion.

The broad hidden-kinetics claim is confined to these **unselected** reversible channels. They may change correlations and holding times, and need not mix, but they do not enter the pointwise corrected-current drift. For the explicit coefficient, the selected c_e, their balance, and the actual factor 1+alpha u delta_e are warranted. Equilibrium weights alone do not supply any of them. The text explicitly excludes hidden variables that change the selected rates without a separate justification.

Uniform canonical occupancy gives each edge activity probability 2M(n-M)/[n(n-1)], proving the displayed mean A_c. Under the specified stationary law, the martingale isometry gives E M_t^2=(1-alpha^2)E A_c t. The endpoint correction is uniformly bounded, so its variance is O(1) and its covariance with M is O(sqrt(t)); division by t proves the variance growth limit. No CLT or bracket stabilization has been inferred from stationarity alone.

The mean selected event rate is A_c already pointwise, since the alpha u sum c_e delta_e term cancels. This validates the one-bit update count. It is an event count, not an energy or communication cost.

## 3. Supplied force: the stationary law is exact and its preparation matters

Under the additional rate port exp(h delta_e), the incoming flux at (eta,u) has selected aggregate coefficient

\[
A_c[\cosh h-\alpha u\sinh h]w_h(-u),
\]

while the outgoing aggregate is

\[
A_c[\cosh h+\alpha u\sinh h]w_h(u).
\]

For w_h(u)=1-alpha u tanh h, both products equal
\(A_c[\cosh^2h-\alpha^2\sinh^2h]/\cosh h\).
The unselected channels continue to preserve nu separately at each bit value, so multiplying their stationary weights by w_h(u) does not change invariance. This proves the displayed mu_h without assuming detailed balance, mixing or uniqueness under the force.

The stationary bit mean is -alpha tanh h. Averaging the exact current drift A_c[sinh h+alpha u cosh h] gives

\[
\mathbb E_{\mu_h}J_t/t=(1-\alpha^2)\mathbb E_\nu A_c\sinh h.
\]

Thus the response derivative with respect to h is the equilibrium variance growth coefficient. With the full dimensionless affinity F=2h, it is half that coefficient, as expected for the conventional current diffusion constant. There is no claim of suppressed fluctuations at unchanged response to this supplied force.

The exact equality for every t is a statement about execution **initialized at mu_h**. It is not a transient response theorem after switching on the force from a fixed mu_0 start. Nor does reducible dynamics prepare mu_h by waiting. These limitations are already explicit in the source. The stated total-variation distance alpha|tanh h|/2 is correct, and the file does not use that vanishing distance to transfer speed-N rare probabilities.

## 4. The two-state spectral cell is a current/activity identity

On v(u), the selected tilted generator has diagonal entries -cosh h minus or plus alpha sinh h and positive off-diagonal entries cosh(h+k) plus or minus alpha sinh(h+k). Vertex balance is what removes every remaining signed-edge sum. The discriminant is

\[
\alpha^2\sinh^2h+\cosh^2(h+k)-\alpha^2\sinh^2(h+k)
=\alpha^2\cosh^2h+(1-\alpha^2)\cosh^2(h+k),
\]

which verifies the Perron eigenvalue. The off-diagonal entries remain strictly positive even at alpha=1 for finite h,k, so a positive two-component eigenvector exists. If A_c happens to vanish at some occupancy, both sides of the local eigenvector identity vanish there; reducibility introduces no exception.

The tilted eigenvector identity is pointwise in the full state. Applying the jump compensator to exp(kJ)v(u) gives the claimed exponential martingale with integrated random A_c. Selected jump intensities are bounded, A_c is bounded, and v has a finite positive maximum/minimum, so the local martingale is mean one on every finite horizon. Unselected transitions act trivially on v and on the recorded selected current.

The symmetry k -> -2h-k and the second-order expansion follow directly from the eigenvalue formula. At alpha=0 the cell reduces to the ordinary current compensator cosh(h+k)-cosh h; at alpha=1 the eigenvalue is zero, consistent with the bounded physical current.

Crucially, this is not generally a scalar SCGF equal to b_alpha times E A_c. For negative b_alpha, low-activity histories may dominate; even a small stationary variance of A_c does not supply the needed exponential occupation estimate. The warning in the source is mathematically necessary and correctly retained.

## 5. Several labeled channels and covariance scope

Each channel's corrected current is a martingale with the stated bracket. Distinct channel events do not occur simultaneously, and each event contributes to only its own corrected-current sum, so the cross predictable bracket vanishes. Martingale orthogonality gives zero cross second moment. Bounded bit endpoints contribute only O(sqrt(t)) cross terms, hence the stated long-time diagonal covariance after division by t.

With separate force parameters, the product of the biased bit weights preserves each channel generator separately: all other bit factors are constants during that channel's event. The visible/hidden marginal stays nu, so mean activities do not acquire hidden cross-dependence on the other h parameters. The resulting stationary response is diagonal as written.

The labeled event identities, separate physical bit updates, and common reference-law invariance must actually exist even if channels share a geometric edge. The final matrix congruence for linear combinations of recorded currents is only a readout transformation. The file says so. A subsequently supplied shared-bit two-cycle construction is a different physical operation and is not accepted by this review before its own actual equations are read.

## 6. Physical comparison and final status

The event-updated bit is an additional selective gate, requiring an atomic joint swap/bit transition and coupling of all selected ports to that same degree of freedom. It need not compute parity from the entire visible configuration, but it does not eliminate the physical task of transmitting and acting on the bit. Delayed sensing and broadcast change the generator; no finite-latency limit follows from the finite theorem alone.

The ordinary time-change construction saved in this role gives a useful contrast. At unchanged mean speed, autonomous positive global activity fluctuations cannot suppress the circulation coefficient and only broaden rare tails. Ordinary threshold-and-hold feedback can suppress terminal circulation with extra sensing/hold ports, but freezes the whole density after triggering. The event-memory theorem has a different interface and does not by itself prove its desired full-density advantage.

Pair-current conservation and finite-state current corrections have established predecessors. The present receiving acceptance concerns the written finite balanced-network identities and their exact conditional kinetics/force scope. Historical priority, apparatus feasibility and the separate full spatial receiver remain outside this review.
