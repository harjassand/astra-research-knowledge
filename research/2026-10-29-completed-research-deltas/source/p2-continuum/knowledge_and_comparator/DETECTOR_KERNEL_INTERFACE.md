# Coupling and detector kernels: the missing observable interface

28 October 2026. New derivation by the knowledge/comparator contributor. This is a conditional mathematical interface, not a model of the P2 hardware detector. The underlying ingredients are coherent-state overlap, bosonic second quantization, positive-kernel realization, and a passive dilation. No priority claim is made.

## 1. A scalar bath density does not specify a physical detector

The local phase density fixes the coupling Gram function

`G(t,s)=<f_t,f_s> = integral rho(omega) exp[i omega(t-s)] domega`

(with the sign adapted to the chosen field convention). It determines the source's coupling to a canonical vacuum bath. It does not specify which outgoing modes a particular detector collects. Take one coupled oscillator b and an unused vacuum oscillator c. A passive beamsplitter after the source sends b to detector port 1 with amplitude cos(theta) and port 2 with amplitude sin(theta). It leaves the preceding source dynamics and its phase density unchanged. For a coherent outgoing amplitude alpha, the port-1 click probability is `1-exp[-eta cos(theta)^2 |alpha|^2]`, which varies from zero to `1-exp[-eta|alpha|^2]`. Thus no function of the scalar local phase density alone can determine that record probability.

This does not invalidate an unmeasured full-bath channel certificate. It identifies an extra observer input. For a physical multiport instrument one needs a specified output isometry/transfer and detector efficiencies/time windows, or the equivalent detector kernels below. The represented dressed bath modes are not automatically freely propagating detector modes.

## 2. Minimal additional data on the dynamically visited subspace

Let `h` be the bath one-particle Hilbert space and let the vertices use vectors `f_x`, with x collecting source-port labels and times. Let `h_vis` be their closed linear span. For detector r, supply a positive contraction effect `E_r` on this one-particle space with

`E_r >= 0`, `sum_r E_r <= I`.

The necessary data are the ordinary and detector Gram kernels

`G(x,y)=<f_x,f_y>`, `D_r(x,y)=<f_x,E_r f_y>`.

For every finite list x_1,...,x_n, they must obey

`D_r >= 0`, `sum_r D_r <= G`

as matrix inequalities. These conditions also suffice, provided the kernels are consistent on all finite lists. Construct the Hilbert space completion of formal finite combinations modulo the null space of G. The inequality bounds each sesquilinear form D_r by the G norm, ensures that it vanishes on the null space, and gives by the bounded-form representation theorem a unique `0<=E_r<=I` on the completion. Summing the forms proves `sum E_r<=I`. Any unvisited orthogonal complement may be supplied with zero effects.

Consequently, for coherent packets whose amplitudes are finite linear combinations `alpha_a=sum_j c_aj f_xj`, the unmeasured and all detector-weighted overlaps can be computed entirely from these two families of kernels. No arbitrary discretization of a reservoir Hilbert space is logically required. Numerical evaluation of the kernel integrals, of course, has its own cost and error.

## 3. Exact passive multiport threshold effects

Set `E_0=I-sum_r E_r` and define the one-particle isometry

`L u = (sqrt(E_0)u, sqrt(E_1)u,...,sqrt(E_m)u)`.

Second quantization sends a coherent state to the product of coherent states with these amplitudes. At each detector port use an ideal on/off detector; efficiencies and passive losses are already included in E_r. The no-click effect for a subset S of detectors, pulled back to the original bath Fock space, is

`Pi_no(S) = Gamma(I-sum_(r in S) E_r)`.

For normalized coherent states,

`<beta|Pi_no(S)|alpha>`

`= exp[-(||beta||^2+||alpha||^2)/2 + <beta,(I-sum_(r in S)E_r)alpha>]`.

For a complete binary record with no-click set N and click set C, inclusion-exclusion gives

`<beta|Pi_(N,C)|alpha> = sum_(L subset C) (-1)^|L| <beta|Pi_no(N union L)|alpha>`.

This remains correct when the pulled-back E_r do not commute. The detector projectors commute in the dilated output ports. One must not replace the joint no-click operator by `product_r Gamma(I-E_r)` on the input bath. That multiplication does not represent the same passive detector experiment.

An arbitrary coherent superposition may have correlated port records even though each individual coherent packet produces a product of Poisson counting distributions. Keeping the off-diagonal packet kernels is therefore essential.

## 4. A complete reference-compatible instrument

Let a candidate source-to-source-and-bath map be

`V = sum_a B_a tensor |alpha_a>`,

where every B_a maps the complete specified input code into the retained source Hilbert space. For record z, after discarding the bath,

`I_z(rho)=sum_(a,b) <alpha_b|Pi_z|alpha_a> B_a rho B_b^dagger`.

The kernel matrix is positive because Pi_z is positive. Thus each record map is completely positive. Summing records gives the bath-traced V channel. If `V^dagger V=I`, the total instrument is trace preserving; otherwise the endpoint normalization defect must be charged or corrected and cannot be hidden by normalizing each input state separately. The expression retains all source coherences and is valid with an arbitrary reference.

Postprocessing an exactly defined source-plus-bath channel by this detector instrument contracts its diamond-distance error. If the instrument itself is uncertain, that error is a separate physical/model term. A small scalar representation error does not calibrate detector efficiency, dark counts, mode collection, dead time or reset.

## 5. Numerical obligations that can change the decision

The supplied G and D_r must be mutually compatible, not separate plausible fits. Shared-line crosstalk, finite collection windows and port filtering alter D_r and can introduce correlations. Matrix positivity may be spoiled by quadrature or roundoff; clipping negative eigenvalues without charging the change is not a certificate. Close coherent packets make Gram matrices ill-conditioned. Any compression, thresholding, cancellation or linear solve must be checked in the physical Gram norm, and the retained off-diagonal channel coefficients must be controlled.

The useful bridge is therefore a physically specified kernel pair `(G,{D_r})` plus a full-input residual/endpoint certificate. It can evaluate candidate control/readout mechanisms before assuming independent two-port statistics. It still provides no generic bound on packet count, no arbitrary-device observer model, and no proof that the present P2 workload is feasible.
