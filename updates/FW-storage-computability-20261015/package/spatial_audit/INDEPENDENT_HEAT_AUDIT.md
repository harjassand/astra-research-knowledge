# Independent audit of the padded-heat storage solver

15 October 2026. Internal analytic review, not external validation.

## Verdict

No fundamental counterexample was found to the proposed route for a fixed, effectively smooth endpoint and a finite incoming horizon. The global heat certificate is stronger than quasiconvexity and supplies exactly the missing one-sided approximation estimate. Arbitrary concentration of incoming gradients is not an obstruction to this construction. This does NOT yield uniform finite-Fourier observation of endpoints on a critical Sobolev ball.

A search horizon larger than the incoming horizon is sufficient for computing the unrestricted storage. Compressing back to the original horizon is unnecessary. The construction below deliberately avoids that extra obligation.

## A precise repaired construction

First fix a smooth endpoint U, an incoming horizon N, and a near-optimal gradient budget E. Initial zero padding makes the original path have exact duration N without changing action. Let its gradient fourth-power integral be at most E. For the fixed-endpoint variant, means may move arbitrarily inside the path; no mean-fixed hypothesis is used.

Choose a padding width δ>0. Put the unknown incoming path on [δ,N+δ], with stationary zero and U profiles on the adjacent pads of width δ. Attach a known smooth return from U to zero of duration one, flat in x at its ends. This gives a periodic W^(1,4) loop Ψ on a rectangle of x-length L=N+2δ+1. Choose a smooth periodic reference R equal to Ψ on both pads and the entire return, interpolating smoothly from zero to U within [δ,N+δ]. The difference F=Ψ−R is supported in that closed unknown interval.

The gradient budget is explicit:

K^4 = E + δ ||U_y||_4^4 + ||D(return)||_4^4.

Also ||Ψ||_4 <= L K because Ψ starts at zero. Thus ||F||_4 is bounded by L K+||R||_4, uniformly over all incoming paths in the budget. Neither intermediate means nor concentration can invalidate this estimate.

Cut the heated loop on I=[δ/2,N+3δ/2]. Its length is N+δ. Every point of the exterior O is at periodic x-distance at least δ/2 from supp F. On O and at both cut profiles, heat applied to F is quantitatively small in every fixed derivative norm. For multi-index α one may use the fully explicit bound

sup_O |D^α H_t F| <= ||F||_4 sup_(z in O) ||1_(supp F) D^α K_t(z−.)||_(4/3).

Here K_t is the anisotropic periodic Gaussian kernel with the source rational diffusion constants. Its displayed tail norm is computable by Gaussian sums and integration, and tends to zero exponentially in δ²/t, times a fixed negative power of t. A crude bound can instead use its pointwise Gaussian-derivative tail times the finite domain volume. All periodic image terms must be included. In particular a time of order δ² with a fixed proportionality constant does not guarantee arbitrarily small error; t must be selected using the tail estimate.

For the smooth known reference, ||D^α(H_t R−R)||_infinity <= t ||D^α (d1 R_xx+d2 R_yy)||_infinity. Consequently one obtains computable q(t)→0 controlling the gradient change on O and the value and y-derivative errors at both cuts. Derivatives of the unknown interior are never estimated pointwise.

## Signed exterior subtraction: required and valid

Write J for the adjusted density f_B. The source global periodic heat monotonicity gives J_all(H_t Ψ)<=J_all(Ψ). Therefore

J_I(H_t Ψ) <= J_I(Ψ) + J_O(Ψ)−J_O(H_t Ψ).

No sign for the exterior action is presumed. Since Ψ=R on O, the last difference is uniformly small by the preceding gradient estimate. For example, with b=|B|, r=||DR||_infinity and gradient error q, its absolute value is at most

180 |O| q [b²(r+q)+b(r+q)²+(r+q)³].

The original interior action is J_original plus δ/2 times the stationary endpoint action integral_y f_B(0|U_y). Pay the absolute value of this padding term. Stationary nonzero profiles do not have free action.

The monotonicity extends from smooth loops to W^(1,4) loops by strong density and quartic polynomial continuity. This is a legitimate use of the supplied heat certificate, not an inference from ordinary quasiconvexity alone.

## Exact endpoint repair

Let a,b be the cut locations, s=(x−a)/(b−a), and v=H_t Ψ restricted to I. Define

T(v)=v−(1−s)v(a,.)−s v(b,.)+s U.

This has exactly the required initial and terminal profiles. Boundary value and y-derivative errors control the W^(1,4) norm e of the correction by an explicit function of q and |I|; its x derivative costs 1/|I|. If A is the old gradient with ||A||_4<=K, the action change is at most

180 e [b² |I|^(1/2)(K+e)+b |I|^(1/4)(K+e)²+(K+e)³].

Thus padding can first be made cheap and heat time then made small, yielding a feasible smooth path of known duration N+δ with action at most the original action plus any prescribed error. The bound is uniform over the incoming near-optimal budget, even though no uniform strong approximation rate for those unsmoothed gradients exists.

## Fourier truncation and a genuinely finite search

For fixed t>0, the full periodic heat field has a uniform Fourier tail in C1: its coefficients are those of Ψ times exp(−t[d1(2πk/L)²+d2 l²]). The coefficients of Ψ are uniformly bounded by its L4 budget and finite volume. Summing the explicit exponential derivative tail supplies a computable cutoff. Apply T to the truncated field. T is bounded on C1, so the cutoff error remains controlled and the endpoints remain exact.

For a finite-Fourier U, these corrected fields form an explicitly finite-dimensional affine family. Bound every real sine/cosine coefficient by the above uniform coefficient bound and round coefficients on a finite rectangular grid. Every grid point is feasible because T enforces the endpoints identically. A finite-dimensional derivative bound for T and the polynomial growth estimate supplies an explicit mesh ensuring the additional action error is small. Integration and action evaluation must be certified to a chosen tolerance; point samples without a certified quadrature remainder do not suffice. For rational/computable input data these finite-mode integrals are computable.

If m is the exact minimum over this finite feasible grid and η is the total horizon, endpoint, padding, smoothing, truncation and rounding allowance, the correct direction is

p_B(U) <= m <= p_B(U)+η.

Consequently [m−η,m] encloses the value. If only certified evaluations yield m in [m_low,m_high], use [m_low−η,m_high]. A feasible sampled minimum alone is only an upper bound. The lower bound comes from the uniform near-minimizer approximation, never from the sampled values alone or presumed minimizer attainment.

## Free terminal means and endpoint representation

For the quotient horizon q_B^N, the known finite-horizon near-minimal bound |d|<=N^(3/4) E^(1/4) is essential before constructing a uniformly bounded return/reference family. Include d as two bounded real grid variables, use U+d in T, and keep the adjusted density throughout. Rounding d remains feasible for the quotient problem. Never optimize the physical affine correction DG(B):(actual_mean|0) over this artificial d.

For rough critical endpoints the algorithm needs a finite-Fourier approximation with a certified strong W^(3/4,4) error, or equivalent effective approximation data. The source bounded-ball Lipschitz estimate transfers that error to storage. A mere bound on the endpoint's critical norm, a black-box finite Fourier observation, or uncertified strong density does not supply this input. The source high-frequency endpoint counterexamples explicitly exclude that stronger oracle claim.

## Conditions still needed in a final theorem

1. State the computational input representation of B, U, endpoint norm/extension budget, and tail certificate.
2. Publish computable majorants for the periodic Gaussian tails, reference derivatives, Fourier tails and coefficient-rounding action errors. They may be extremely inefficient.
3. Specify the feasible finite-dimensional family and include all necessary real coefficients and, if used, terminal-mean variables.
4. Carry numerical integration/evaluation errors in the final interval.
5. Claim an unrestricted-storage algorithm, not a fixed-horizon algorithm, unless separately proving compression or a fixed-horizon boundary treatment.

No minimum-attainment, convexity of G, weak compactness of minimizing traces, or uniform endpoint finite-observation principle is required or justified.


Integration evidence status: `source_derived_unreviewed`. Audit verdicts and primary-source reading statements above are attributed to the supplied research, not new external review. This intake replays only its three own exact verification scripts. The conclusion applies to the particular certified Heat18 quartic G, not the full quartic cone, PR97’s newly exposed ROC ray, or general Morrey questions.
