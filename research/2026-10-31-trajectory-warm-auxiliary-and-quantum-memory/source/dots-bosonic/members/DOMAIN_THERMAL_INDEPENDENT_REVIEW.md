# Independent domain and thermal-receiving review
31 October 2026. Reviewer: independent mathematical review.

## 1. Source binding and scoped verdict

PASS for the canonical infinite-Fock controlled process, its quantitative vacuum-cutoff bound, product-dynamics identification, and exact finite-mode thermal-to-vacuum receiving. This is not acceptance of a complete efficient bosonic compiler.

I read the following complete bodies in damped_bosonic_reservoir_opening_20261031, then the specified final additions, and verified their hashes:

- VACUUM_LIMIT_AND_THERMAL_RECEIVING_CANDIDATE.md, 9,332 bytes, SHA-256 e0134c48d6d099ba53bfc7ddf4a5a308f2d7bc36fdd35f474ce3b34b0cab4a7b.
- INFINITE_FOCK_CONTROLLED_LIMIT.md, final 11,414 bytes, SHA-256 a250c6ff320d19e86f28406d432c698c54f4ff71c9cab5dfaa0b2681f04501a2. I read the complete 10,728-byte version 470dbafd676ade6b5a558ca1f1a265b84a84a3bb37d3ba703b859f360f962242 and the final accumulated-interaction-time addition.
- THERMAL_VACUUM_CONTROLLED_REDUCTION.md, final 13,363 bytes, SHA-256 61085d944aa7d27aaea552582fb13eb02f26b50d42f847e31bd34296373c2403. I read the complete 11,920-byte version 0b5c3aaf23aecfa79d5aa9b6e05f22e70c7e58814c734d5724065734ab6f93fa and the final graph-domain and comparator corrections.

The earlier opening and its local receipt remain separate: FIRST_CONSTRUCTION_UNREVIEWED.md SHA-256 3b9a31235983ca4207a73922b2df52503afe0f06169889a9038259cf034cb2a4, and OPENING_INDEPENDENT_REVIEW.md SHA-256 9d323c243f11e441651afdc88ca8f9469622a2e660ad85d9896e458e670901b1. Their source bytes are unchanged.

The present pass requires the final author's more explicit domain/splitting arguments, not merely the root opening's suggested interchange. No arbitrary uniqueness theorem for all unbounded formal GKSL extensions is asserted.

## 2. Non-Hermitian coupling square and sharp cutoff

Use the author's convention
H=H0+sum omega_i n_i+sum(F_i a_i^dagger+F_i^dagger a_i),
J_i=sqrt(2kappa_i)a_i,
with bounded, not necessarily Hermitian F_i. Put C=sum ||F_i||^2/(2kappa_i), Gamma=4C and F2=sum ||F_i||^2.

For V=z^N the conjugated adjoint contribution is
-d_i a_i^dagger a_i+i c_z(F_i^dagger a_i-F_i a_i^dagger),
where d_i=2kappa_i(1-1/z), c_z=sqrt(z)-1/sqrt(z). It equals
-B_i^dagger B_i+(c_z^2/d_i)F_i^dagger F_i
for B_i=sqrt(d_i)a_i+i c_z F_i/sqrt(d_i). No commutation between F_i and F_i^dagger is assumed. Their commutation with reservoir operators is sufficient.

This proves the stated finite-cutoff number moment. With the jump tilt and z=2e^theta-1 it gives the stated emission MGF. Both are valid at finite local cutoffs because a_L^dagger a_L=n_L and the number-shift identities remain exact. The false cutoff CCR is never needed.

The outward raising block has orthogonal ranges for different modes and square
B_L^dagger B_L=(L+1)sum F_i^dagger F_i tensor Pi_{n_i=L}.
Finite Duhamel, trace-class Cauchy-Schwarz and contraction then prove the source's sharp finite-to-finite estimate, uniformly in reference and retained instrument records:
2T sqrt((L+1)F2) sqrt(M_z) exp[CT(z-1)/2] z^(-L/2).
For virtual vacuum and z=2 this is exactly the earlier exp(Gamma T/8) cutoff bound. There is no extra factor p: the control-free integrals sum to physical time T.

All quantitative count claims are unconditional. System instruments preserve the reservoir weight after their outcomes are retained and summed, not necessarily after normalizing a rare branch.

## 3. The infinite process is actually constructed

The cutoff input map that projects into the cube and resets only its rejected reservoir component to vacuum is a mathematical CPTP approximation to the identity, with system/reference data retained. It converges in trace norm on every trace-class input. This is not a reservoir reset inserted into the target physical dynamics.

On fixed finite-particle inputs, the preceding comparison gives Cauchy convergence uniformly on compact time intervals. Contractivity extends convergence from that dense class to all trace-class inputs. The resulting maps are normal CPTP, including after finite ancillary extensions. Composition passes through the strong limit by contraction, and the uniform compact-time convergence gives strong continuity.

On finite-Fock-supported trace-class tests, the finite generators stabilize beyond the support plus the required bandwidth. Dividing the cutoff comparison by small time gives a residual error coefficient tending to zero with cutoff. This identifies the constructed generator with the formal expression on the specified test class. It does not claim that mere equality on a dense test domain proves uniqueness of every conceivable unbounded extension.

Counter-augmented finite constructions can be treated with a finite count cap first. The same cutoff comparison is uniform in that cap because the Hamiltonian boundary source acts trivially on the counter. Bounded count tests and monotone cap limits then receive the emission MGF. It is not inferred from occupation alone.

Thus there is a conservative normal process, not just a list of finite-time reduced density approximations. The quantitative vacuum-input controlled-channel bound remains stronger than the pointwise extension statement for general initial states.

## 4. Uniform splitting and interaction-unitary existence

The stronger decreasing-weight proof closes the interchange explicitly. For accumulated interaction time u<=U, set
z(u)=1+2/(1+u/U).
Then z starts at 3, ends at 2, and (z-1)^2/(-z')=2U. The derivative of the weight contributes a negative number term, against which the linear interaction is squared without relying on damping. For a uniform bound F2 on the active interaction coefficients,
E[z(u)^N]<=M3 exp(2Uu F2).

Vacuum damping decreases this increasing number weight, number rotations preserve it, and system-only CPTP controls preserve it unconditionally. The estimate is therefore uniform in the number and ordering of splitting steps with total interaction-piece duration at most U. The resulting cutoff error is
2U sqrt((L+1)F2) sqrt(M3) exp(U^2 F2) 2^(-L/2).

The final qualification is essential: if separate mode or real/imaginary interaction pieces each run for a physical step length, their accumulated duration can exceed physical T. One must use that actual U and a valid uniform coefficient bound, not keep T by notation. For fixed finite splitting architecture U remains finite and independent of mesh size.

At each fixed Fock cutoff, bounded-generator Lie splitting is ordinary. Uniform-in-mesh cutoff comparison then justifies exchanging the product and cutoff limits. This identifies the canonical process with the full Gaussian damping/rotation channels alternated with actual interaction unitaries.

This coarse estimate may have exp(constant times lambda) dependence through F2. That is acceptable only because it proves existence/identification at fixed physical parameters. It MUST NOT replace the sharper continuously damped cutoff bound in a claimed stiffness-efficient compiler.

The interaction unitary is also earned. Finite-particle vectors have an analytic-vector bound from the fact that the linear-plus-number Hamiltonian raises total number by at most one and has norm O(n+1) on number<=n. Alternatively, the positive/negative-time cutoff unitary limits are inverse by contraction/strong convergence. Neither argument supplies a cheap simulation oracle; algorithmic implementation remains separate.

## 5. Thermal Weyl algebra and exact product experiments

For one thermal mode let u=sqrt(nbar+1), v=sqrt(nbar) and b=u a+v c^dagger. The complementary canonical mode d=u c+v a^dagger commutes with b. A finite-mode Bogoliubov transformation implements this representation as a normal factor embedding; it is not an assertion about infinite baths or infinite squeezing.

With W_b(z)=exp(z b^dagger-z* b),
W_b(z)=W_a(uz)W_c(-v z*).
The minus-conjugate argument is correct. The virtual vacuum characteristic function is exp[-(nbar+1/2)|z|^2], exactly the physical thermal restriction.

Vacuum damping of a and c with opposite frequencies maps this embedded Weyl observable to
exp[-(nbar+1/2)(1-e^(-2kappa t))|z|^2]
W_b(z e^{(-kappa+iomega)t}).
This is the full physical thermal attenuator, including drift and noise covariance. Weyl operators span an ultraweakly dense algebra; normality extends the equality to the generated physical factor.

The interaction maps to
u(S a^dagger+S^dagger a)+v(S c+S^dagger c^dagger).
In particular its second virtual creation coefficient is v S^dagger, not v S. This distinction is load-bearing for general non-Hermitian S. The embedded interaction unitaries and system-only instruments preserve the same factor. Hence every finite free/interaction/control product experiment agrees, including outcome records and retained references.

The full virtual process is the strong product limit established above. Its adjoint limit preserves the ultraweakly closed physical factor, so restriction defines the canonical thermal interacting process. This proves a complete controlled receiving route, not merely matching two moments of an otherwise unspecified environment.

## 6. Thermal domain qualification checked in the final version

Two shortcuts would have been invalid and are explicitly excluded:

1. Heating jumps in a finite PHYSICAL thermal cutoff raise occupation and do not agree with larger-cutoff damping on the smaller cube.
2. A physical thermal state need not have a finite moment Tr(3^N rho).

The actual cutoff/splitting proof is applied to doubled VIRTUAL vacuum, with M3=1. The thermal physical side uses the FULL known Gaussian attenuator in its product experiments, not a presumed vacuum-like heated-cutoff comparison.

A physical finite-particle test is also not finite-support in virtual coordinates. The final graph-domain completion handles this correctly. Tensor that test with complementary vacuum and apply finite squeezing. The resulting vectors are polynomial excitations of a squeezed vacuum, with an exponential virtual number tail for some z>1; no claim that z=3 works is needed. Their cutoff projections converge in the graph norm of N. Consequently H u, a_i u and the rank-one jump terms converge in their required Hilbert/trace norms. Closedness of the constructed virtual generator extends its established finite-particle action to these transformed tests. Complementary partial trace and the Gaussian restriction identify the physical thermal GKSL sum on the physical test class.

This supplies a specified domain identification. It still does not make an unrestricted uniqueness claim for arbitrary unbounded formal generators or arbitrary infinite-energy initial preparations.

## 7. Backaction, temperature cost and which jumps are bounded

The virtual interaction drifts are
da/dt=-(kappa+iomega)a-i u S,
d(c^dagger)/dt=-(kappa+iomega)c^dagger+i v S.
Combining them gives db/dt=-(kappa+iomega)b-iS because u^2-v^2=1. The thermal enhancement does not incorrectly multiply the coherent backaction.

The two virtual coupling norm squares sum to (2nbar+1)||S||^2. Therefore the stated occupation and count constants and the corresponding paid temperature strength are correct. Finite temperature is not a free preparation or a free simulation scale. Negative-frequency auxiliary rotations are a digital representation, not a thermodynamic hardware resource.

A binding interpretation: the rate-independent count bound is for emissions in the DOUBLED VIRTUAL vacuum representation. It is not the physical thermal emission-plus-absorption count. For S=0 the virtual modes remain dark, while the uncoupled stationary thermal mode has total physical jump rate 4kappa nbar(nbar+1). Thus the receiving theorem does not identify bath detector records, heat-transfer statistics or reservoir trajectories. Those records are excluded from the accessible consumer interface.

## 8. Classical-Hamiltonian-noise obstruction

The Jaynes-Cummings example is decisive within its stated scope. With vacuum and S=g sigma_minus, the ground/vacuum state is dark. From the excited/vacuum state the dynamics stays in the zero/one-excitation sector and gives a reduced amplitude-damping channel. For positive damping its short-time loss is p(t)=g^2 t^2+o(t^2), positive for sufficiently small nonzero t. The zero-damping sin^2(gt) expression is only an illustrative limit, not needed to establish the positive-damping case.

Any average of system unitaries generated by a classical Hermitian Hamiltonian source is unital when no controls are inserted. It sends I/2 to I/2, whereas amplitude damping sends it to a state with population imbalance p(t). The trace-norm discrepancy is p(t), or p(t)/2 under half-trace-norm convention. Therefore this quantum reservoir cannot generally be replaced by classical colored Hamiltonian noise.

This is not an obstruction to ordinary quantum pseudomodes, influence-functional methods, or retained quantum ancillas. Nor does it say that no special Hermitian zero-frequency coupling has a classical OU representation; that special interface remains valid.

## 9. Prior-method credit and remaining compiler boundary

Thermofield doubling is established machinery. The primary de Vega–Bañuls abstract explicitly describes exact mapping of a thermal environment to two vacuum environments. [Thermofield-based chain mapping approach](https://arxiv.org/abs/1504.07228).
Tamascelli et al. give nonperturbative temperature-dependent vacuum representations. [Efficient simulation of finite-temperature open quantum systems](https://arxiv.org/abs/1811.12418).
Gaussian multitime equivalence is also prior, including system maps and sequential measurement statistics. [Smirne et al.](https://arxiv.org/html/2209.00293).

I checked the final comparator correction against the primary ancilla-train text. Its abstract advertises time-dependent applicability, but its proved Trotter error/resource analysis explicitly assumes time-independent system H and leaves the general time-dependent analysis for future work. It is fair to credit its multiple-environment/arbitrary-coupling representation and polynomial inverse-accuracy result without silently strengthening that theorem. [Ancilla-train algorithm](https://arxiv.org/html/2509.12717).

This receiving pass earns the infinite process and thermal physical interpretation. It does not earn the immigration-death coherent bridge compiler, factorized first-event preparation, large-frequency timing ledger, OAA precision, total gate complexity or physical parameter acquisition. Those require their own exact bodies and review. No generic novelty, practical advantage, hardware noise suppression or thermodynamic equivalence beyond the stated observable interface is claimed.
