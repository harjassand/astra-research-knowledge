# Average-output thermal domination as a write/hold interface

Root construction, 2026-11-02. Exact conditional consumer and an ideal Petz-map example, not a physical noisy writer or a novelty claim about Petz recovery.

## 1. A nonstationary basin from an average channel output

Let rho_LG be stationary under the actual hold Hamiltonian H. Let Q_j be the fixed decoded Pauli algebra, P a bad projector, and assume

 [H,Q_j](I-P)=0,  ||[H,Q_j]||<=c_j,  p=Tr(rho P).

Because i[H,Q_j] is Hermitian, it is supported on P on BOTH sides. Let W map an incoming qubit A to LG. Suppose its uniform-input average obeys the operator inequality

 W(I_A/2) <= kappa rho.

This is an explicit, strong channel-state condition; local stochastic noise or small mean excess energy does not imply it. Let the initially decoded write channel be within epsilon_write of the identity in diamond norm.

Then for arbitrary input/reference xi_AR, the memory marginal after writing satisfies

 sigma_LG(0)=W(xi_A)<=2 W(I/2)<=2 kappa rho,

and hence sigma_LG(t)<=2 kappa rho at all hold times, by stationarity. Therefore Tr(P sigma(t))<=2 kappa p.

Write the decoded joint state in its Pauli expansion on L. Its time derivative has three coefficients Tr_LG(i[H,Q_j] sigma_LGR). Each coefficient is Hermitian, and trace-norm duality against any reference observable M with ||M||<=1 gives

 ||Tr_LG(i[H,Q_j] sigma_LGR)||_1 <= c_j Tr(P sigma_LG).

The identity coefficient is constant. Since ||Q_j/2||_1=1, integrating gives

 ||storage_T-id||_diamond
   <= min(2, epsilon_write+2 kappa p T sum_j c_j).

If c_j<=2 v_dyn n, the added hold error is <=12 kappa v_dyn n p T. This is linear in p. It does not require each written state to be close in trace norm to rho, or itself stationary. Reference safety uses only the memory marginal domination and operator duality; no unjustified factorization with the reference is assumed.

## 2. Composition exposes the physical service required

If a terminal physical noise channel N has N(rho)<=kappa_N rho, then the averaged-output condition survives with kappa replaced by kappa*kappa_N. In particular an EXACT Gibbs-preserving channel has kappa_N=1. Its logical write error must still be bounded separately; preserving equilibrium alone does not preserve encoded information.

Arbitrary local stochastic faults do not automatically meet this inequality with volume-independent kappa. An extensive athermal startup can have max-relative entropy O(n), which destroys a stretched-exponential rare-event advantage. An average-energy estimate alone cannot replace this operator condition.

Energy-conserving operations with thermal auxiliaries motivate a physical route to Gibbs-preserving services, but controller coherence, switching work, ancilla resets, finite response and generic imperfections must all be included. Calling the ideal channel a thermal operation does not implement it.

## 3. Explicit ideal Petz encoder

Let r=Tr_G rho, assumed full rank (automatic for finite-temperature full-rank rho). Define

 W_rho(X)=rho^(1/2) (r^(-1/2) X r^(-1/2) tensor I_G) rho^(1/2).

This is completely positive. Taking the trace gives Tr W_rho(X)=Tr X, so it is a channel. It obeys W_rho(r)=rho and

 W_rho(I/2)<= [1/(2 lambda_min(r))] rho.

Thus kappa=1/(2 lambda_min(r)) is explicit. This is the familiar Petz/transpose embedding applied to the decoded factor, not a claimed new recovery construction.

Let tau=Tr_L rho, rho0=I_L/2 tensor tau, and delta=||rho-rho0||_1<1. Then lambda_min(r)>=(1-delta)/2 and kappa<=1/(1-delta). A conservative reference-safe write-error estimate follows from canonical Kraus/Stinespring operators and the square-root inequality:

 epsilon_write <= min(2, 2[ sqrt(2delta/(1-delta))
                            +(1-delta)^(-1/2)-1 ]).

Indeed canonical Kraus operators are K_g=rho^(1/2)(r^(-1/2) tensor |g>), while the ideal product-write operators are I_L tensor tau^(1/2)|g>. Their stacked isometries differ in norm by at most

 ||r^(-1/2)|| sqrt(||rho-rho0||_1)
                 +||r^(-1/2)/sqrt(2)-I||,

using ||sqrt(rho)-sqrt(rho0)||_2²<=||rho-rho0||_1. Trace-norm contraction gives the displayed channel bound. This estimate is deliberately conservative and requires independent verification before use.

The existing finite-temperature logical-twirl correlation estimate can supply delta in its admitted model; the beta-free stationary-overwrite theorem did not need that estimate, but this different Petz write-fidelity bound does. At very low temperature with logical polarization, kappa and write fidelity may deteriorate; no beta-uniform claim is made.

## 4. Scientific consequence and unresolved implementation

This identifies a concrete alternative to demanding an arbitrary noisy loader produce the ideal overwritten Gibbs gauge state: construct a logically accurate writer whose UNIFORM input output is Gibbs-subpreserving with polynomial or constant kappa. That condition immediately provides a time-uniform nonstationary basin and preserves rare-bad protection through hold.

The ideal Petz map is not such a noisy physical construction by itself. Implementing it requires actual thermal information/coherences and may be highly nonlocal. Existing ideal filtered preparations do not automatically supply it for native clocks, and fault-tolerant reset/control resources cannot be omitted. This note is therefore an earned conditional interface plus a precise ideal benchmark, not the missing device operation.
