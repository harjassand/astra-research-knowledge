# Composition of symmetry-protected embedded pairs: a cooperative radiation channel

27 October 2026. Independent derivation from the supplied `ASTRA_SYMMETRY_FILTERED_EMBEDDED_PAIR_20261027(3).md`. Units are B = hbar = 1. The exact single-unit assumptions and its fourth-order connected interaction are retained. The spectral obstruction below is exact. The outgoing transition coefficient is perturbative; a resonance theorem and a finite-time remainder are not proved here.

## 1. Coupling two protected units while preserving both symmetries

Take two independent copies A and B of the supplied ladder with its two hard-core memories. In each copy fix two total excitations and even rail-exchange parity. Let

\[
M_i=n_{L_i}+n_{R_i},\qquad
H_0=H_{A,2}\otimes I+I\otimes H_{B,2}.
\]

The pair-product eigenstate is \(\Psi_p=\psi_p\otimes\psi_p\), at energy \(2E_p\). Add the bounded, ordinary density interaction

\[
V=\lambda M_A M_B
=\lambda\sum_{u\in\{L_A,R_A\}}\sum_{v\in\{L_B,R_B\}}n_u n_v.
\]

This preserves both individual rail parities and both individual total excitation numbers. No mirror breaking, wrong-band source, or extra environment has been introduced.

At g = 0, the local even two-excitation continuum is \([0,5]\cup[7,12]\), with the isolated memory pair at 6. The product sector therefore contains

\[
[3,5]+[7,9]=[10,14],
\]

which contains the pair-product energy 12. One unit contains a minus-parity bound memory and a lower-band photon; the other contains a plus-parity bound memory and an upper-band photon. Both local total parities remain even. For small g the corresponding continuum is

\[
(E_-+[0,2])+(E_++[4,6]),
\]

and still contains \(2E_p\) in its interior. Escaping photon wavepackets with the localized one-excitation states give Weyl sequences. Thus the exact uncoupled product is protected by factorization, but has no spectral gap in the product of the original symmetry sectors. An isolated-eigenvalue argument cannot justify arbitrary symmetry-preserving interunit coupling.

## 2. On-shell amplitude with fixed density coupling

Treat lambda as fixed and expand in g. At g = 0, the initially doubly occupied memories in both units have energy

\[
E_i=12+4\lambda.
\]

After emission of one photon of energy omega by A, the memory occupancies are (1,2), and the intermediate energy is \(9+2\lambda+\omega\). After emission of one photon by each unit, the occupancies are (1,1), with outgoing energy \(6+\lambda+\omega+\nu\). Hence the outgoing shell is

\[
\omega+\nu=6+3\lambda.
\]

The two orderings give, apart from the normalized endpoint mode factors and an irrelevant parity sign,

\[
\begin{aligned}
\mathcal T_{\sigma\tau}
&=g^2\alpha_\sigma\alpha_\tau
\left(\frac1{3+2\lambda-\omega}
+\frac1{3+2\lambda-\nu}\right)\\
&=\boxed{\frac{\lambda g^2\alpha_\sigma\alpha_\tau}
{(3+2\lambda-\omega)(3+2\lambda-\nu)}}.
\end{aligned}
\]

Here \(\alpha_+=\sqrt2\), \(\alpha_-=1\), and the second equality is on shell. At lambda = 0 the two time orderings cancel exactly, as required by factorization. The interaction shifts the initial, intermediate, and outgoing configurations differently, removing that cancellation.

For \(|\lambda|<1/2\), every individual first emission remains off shell, with intermediate detuning at least \(1-2|\lambda|\). A lower-band and upper-band photon nevertheless have a joint shell for \(|\lambda|<2/3\). Thus \(0<|\lambda|<1/2\) gives simultaneous emission while the separate emissions remain forbidden.

The bath endpoint densities are

\[
\rho_-(\omega)=\frac2\pi\sqrt{1-(\omega-1)^2}\,1_{[0,2]}(\omega),
\quad
\rho_+(\nu)=\frac2\pi\sqrt{1-(\nu-5)^2}\,1_{[4,6]}(\nu).
\]

Define

\[
J(\lambda)=\int
\frac{\rho_-(\omega)\rho_+(6+3\lambda-\omega)}
{(3+2\lambda-\omega)^2(3+\lambda-\omega)^2}\,d\omega.
\]

The integration interval is \([0,2]\cap[3\lambda,2+3\lambda]\). For \(0<|\lambda|<1/2\), its interior has positive length, and the integrand is strictly positive there. The two orientations (lower photon emitted by A or by B), together with \(\alpha_-^2\alpha_+^2=2\), give the formal leading population-decay expression

\[
\boxed{\Gamma(g,\lambda)=8\pi\lambda^2g^4J(\lambda)+o(g^4).}
\]

The proved calculation is the positive on-shell transition coefficient. A fourth-order resonance theorem is not supplied. At nonzero g the remaining one-memory-per-unit states can also radiate; this is an inclusive leading exit channel, not a guarantee of permanent bound remnants. The amplitude-linewidth convention is Gamma/2.

Exchanging the lower-photon emitter gives \(J(-\lambda)=J(\lambda)\). At zero,

\[
\begin{aligned}
J(0)&=\int_0^2\frac{\rho_-(\omega)^2}{(3-\omega)^4}\,d\omega\\
&=\frac4{\pi^2}\int_1^3
(-u^{-2}+4u^{-3}-3u^{-4})\,du
=\frac{16}{27\pi^2}.
\end{aligned}
\]

The successive weak-lambda and weak-g coefficient is therefore

\[
\boxed{\Gamma\sim\frac{128}{27\pi}\lambda^2g^4
=1.5090246456\ldots\lambda^2g^4.}
\]

This is a symmetry-preserving composition channel, distinct from the supplied wrong-band leakage perturbation. Its leading dependence on g is fourth order, rather than eighth order.

## 3. Independent fixed-g, weak-lambda derivation

Let \(\mu_{M,g}\) be the spectral measure of \(M\psi_p\) for the exact single-unit even two-particle Hamiltonian, and write \(\rho_{M,g}\) for its continuum density. Its pair atom has weight \(\langle\psi_p,M\psi_p\rangle^2\).

The first-order dressed pair contains a component
\(g\eta_\sigma\alpha_\sigma/(3-\omega)\)
on the state with one memory of parity sigma and one photon of the same parity, where \(\eta_+=1\), \(\eta_-=-1\). Orthogonalizing the scattering state against the dressed pair is essential. Since M equals 2 on the bare pair and 1 on a one-memory state, the transition matrix element is

\[
\langle\omega,\sigma;g|M|\psi_p\rangle
=-\frac{g\eta_\sigma\alpha_\sigma}{3-\omega}+O(g^2).
\]

Consequently,

\[
\rho_{M,g}(3+\omega)
=g^2\alpha_\sigma^2\frac{\rho_\sigma(\omega)}{(3-\omega)^2}
+o(g^2).
\]

The exact second-order-in-lambda shell coefficient at fixed g is

\[
C(g)=\int\rho_{M,g}(E)\rho_{M,g}(2E_p-E)\,dE.
\]

The pair atom cannot combine with a local continuum on this shell because of the local sector gap. The continuum-continuum contribution gives

\[
C(g)=\left(\frac{64}{27\pi^2}+o(1)\right)g^4.
\]

Multiplication by \(2\pi\lambda^2\) reproduces the preceding coefficient.

The executed `cooperative_radiation.py` builds the connected rail ladder and complete two-excitation Fock Hamiltonian with actual hard-core memories, then restricts to even parity. It measures the spectral weights of \(M\psi_p\). With twelve bath sites per rail, the lower and upper weights divided by g squared approach respectively

\[
b=4/\sqrt3-2=.3094010768\ldots,
\qquad 2b=.6188021535\ldots.
\]

At g = .025, the values are .3094195146 and .6188201515. Their sum agrees with the variance of M within \(2.5\times10^{-15}\). Independent continuum quadrature yields \(J(0)=.06004218289916314\), matching the exact expression. The finite-chain regularized convolution in the JSON is a diagnostic only; it is not an infinite-volume linewidth estimate.

## 4. Implication on the original gate timescale

The unit interaction has \(|\chi|\sim c_\chi g^4\), with \(c_\chi=28\sqrt3-48=.4974226119\ldots\). A plateau accumulating connected phase pi takes \(T_\pi\sim\pi/(c_\chi g^4)\). Therefore

\[
\Gamma T_\pi\sim\frac{128}{27c_\chi}\lambda^2
=9.5306096407\ldots\lambda^2.
\]

Restoring units replaces lambda squared here by \((\lambda/B)^2\). Decreasing g alone does not improve this ratio. This is a leading scaling observation, not a certified numerical gate error or a universal bound for other interunit interactions.

## 5. An exact repair for this channel: sequential activation

For the declared density coupler, set each inactive module's memory-bath coupling exactly to zero. Every spectator \(M_j\) then commutes with the full Hamiltonian, and its initially empty ladder remains empty. Conditional on spectator occupations \(m_j\in\{0,1,2\}\), the active module only experiences

\[
\varepsilon_i\mapsto\varepsilon_i+\sum_{j\ne i}\lambda_{ij}m_j.
\]

There is no second emitter for the cooperative lower/upper photon pair. With one spectator and \(|\lambda|<1/2\), the shifts 0, lambda, and twice lambda keep the sufficiently weakly coupled active unit inside its local even-sector gap. In general the total shift must keep that gap open.

The cost is explicit: only one module's bath coupling is active at a time. Spectator superpositions cause conditional frequency shifts and phases, which the control protocol must account for. Imperfect switch-off, intermodule excitation exchange, and non-density interactions are outside this result. This is not a claim of protected arbitrary parallel computation.

This repair can also be useful beyond number conservation: an exactly disconnected spectator memory can still have conserved occupation. But the shifted active-unit gap must then be rechecked in the full microscopic Hamiltonian; the rotating-wave thresholds cannot simply be reused.

## 6. A parallel spectral repair and its frequency cost

In the number-conserving, fixed-two-excitations-per-unit model, scale unit j's complete Hamiltonian by \(B_j>0\). At g = 0, its spectrum relative to the target pair lies in

\[
\{0\}\cup[-6B_j,-B_j]\cup[B_j,6B_j].
\]

For two units, \(B_2>6B_1\) prevents compensation between any nonzero local deviations. The product pair is then isolated in its product symmetry sector. A strict margin survives sufficiently small local couplings and bounded interunit perturbations.

More generally, suppose

\[
\sigma(H_j-E_j)\subseteq\{0\}\cup[-D_j,-d_j]\cup[d_j,D_j],
\qquad d_j>0,
\]

with one-dimensional target eigenspaces. If

\[
d_j>\sum_{i<j}D_i\quad\text{for all }j,
\]

then the product eigenvalue has gap at least

\[
\min_j\left(d_j-\sum_{i<j}D_i\right)>0.
\]

Proof: in every nonzero spectral sum, the largest-index nonzero deviation dominates the sum of all previous possible deviations. The spectral theorem gives the gap. A sufficiently small bounded perturbation preserves the rank-one isolated branch.

Here the sufficient condition is \(B_j>6\sum_{i<j}B_i\). A geometric ratio greater than 7 suffices for arbitrarily many units. This is an exponential frequency-span cost, not a free scalability result, and the sufficient condition need not be optimal.

The argument uses exact local excitation conservation and bounded spectra within those sectors. A non-number-conserving oscillator parity sector has unbounded upper spectrum; its additional many-photon thresholds need a separate analysis.

## 7. Why fixed-scale replication eventually loses sector isolation

Suppose an invariant sector contains an isolated target E and continuum intervals \([a,b]\) and \([c,d]\), with \(a<b<E<c<d\). For sufficiently many identical copies, the target product energy mE lies inside the continuum in the product of those same individual symmetry sectors.

Let \(\ell=(a+b)/2\), \(u=(c+d)/2\), and \(w=\min((b-a)/2,(d-c)/2)>0\). Choose k nearest to \(m(u-E)/(u-\ell)\). The center of

\[
k[a,b]+(m-k)[c,d]
\]

differs from mE by at most \((u-\ell)/2\), while its half-width is at least mw. For sufficiently large m, \(1\le k\le m-1\) and \(mw>(u-\ell)/2\), proving interior inclusion. Products of escaping wavepackets prove essential spectrum.

A finer symmetry label cannot forbid continua that already have the target's own local symmetry. The uncoupled product remains an exact eigenstate, but protection against general symmetry-preserving energy-exchange perturbations requires an additional resource: interaction restrictions, temporal isolation, spectral separation, or different logical states.

## Scope

The original single-unit embedded pair and ideal adiabatic gate are unchanged. The new spectral failure concerns composed active units under one explicit density coupling. The positive outgoing coefficient has two independent derivations and an executed Fock-weight audit. A rigorous resonance-width theorem, finite-time error bounds, optimal scale separation, and experimental acquisition remain open.

## 8. A sharp uniform tensor-sum gap criterion

The replication obstruction admits a precise converse, provided the stability requirement is stated correctly.

Let H be self-adjoint on a chosen invariant symmetry sector K. Let E be a simple isolated eigenvalue, with normalized eigenvector psi and projection P. Put h = H - E, Q = I - P, and

\[
S=\sigma(h|_{QK}),\qquad
\delta=\operatorname{dist}(0,S)>0.
\]

For N identical copies, define

\[
K_N=\sum_{i=1}^N h_i,\quad
P_N=P^{\otimes N},\quad Q_N=I-P_N,
\quad
\Delta_N=\operatorname{dist}(0,\sigma(K_N|_{Q_N})).
\]

The value Delta_N is zero if an additional exact eigenstate or continuous spectrum occurs at the target energy. This definition distinguishes a robust rank-one target from an energy value surrounded by a lattice gap but possessing a growing degeneracy.

**Theorem.** Assuming QK is nonzero, the following are equivalent:

1. The target product has a strictly positive spectral gap uniformly for all N: \(\inf_N\Delta_N>0\).
2. The non-target spectrum is one-sided: either \(S\subseteq[\delta,\infty)\) or \(S\subseteq(-\infty,-\delta]\).

In the one-sided case, \(\Delta_N=\delta\) for every N. If S has points of both signs, \(\Delta_N\to0\). If S contains intervals of positive width on both sides, \(\Delta_N=0\) for all sufficiently large N, with the target in essential spectrum.

**Proof.** The decomposition K = PK direct-sum QK gives an orthogonal decomposition of the tensor product according to which factors are in QK. Therefore

\[
\sigma(K_N|_{Q_N})
=\overline{\bigcup_{k=1}^N
\underbrace{(S+\cdots+S)}_{k\text{ terms}}}.
\]

If S is positive, every nonempty sum is at least delta, while placing one factor in Q and the others in P realizes the original lower spectral edge. The negative case is the same with signs reversed.

If \(a<0<b\) belong to S, let \(r=b/|a|\). If r is rational, positive integers n,m give \(n a+m b=0\). This point belongs to the complement spectrum for N = n+m, so Delta_N = 0. If r is irrational, Dirichlet approximation gives positive integers n,m with \(|mr-n|\) arbitrarily small. Hence \(|n a+m b|\) is arbitrarily small. Spectral vectors in sufficiently narrow intervals around a and b give the same conclusion even if neither point is an eigenvalue. Since adding a target-state spectator preserves every previous complementary spectral value, Delta_N is nonincreasing, and thus tends to zero. For continuum intervals, the mixed-interval proof in Section 7 gives interior essential-spectrum overlap at a finite N; adding target spectators gives it at every larger N. This proves the theorem.

An explicit continuum bound is available. For relative-energy intervals centered at \(\ell<0<u\), let w be the smaller half-width. Every integer N with \(Nw>(u-\ell)/2\) admits a mixed interval containing zero in its interior. The nearest-integer construction automatically uses at least one factor of each sign because each interval lies strictly on its own side of zero. This bound is sufficient, not generally sharp; the present ladder already fails at N = 2.

**Stronger finite-size corollary.** A continuum interval on only one side, together with any spectral point on the opposite side, already suffices for essential-spectrum overlap at some finite copy number. For example, suppose a < 0 belongs to S and S contains [u-w,u+w] with u > w > 0. Choose n such that n w > |a|/2 and k nearest to n u/|a|. Then the interval \(k a+n[u-w,u+w]\) contains zero in its interior, because its center differs from zero by at most |a|/2. Therefore zero lies in the complementary essential spectrum at N = n+k and at every larger N. This includes an excited state whose own symmetry sector also contains a lower discrete vacuum and a higher continuum: a lower continuum is not required for eventual replication failure. It is relevant when excitation-number conservation is replaced by parity conservation in a non-RWA model. Again, it establishes spectral overlap, not a nonzero radiation matrix element.

### What "accessible" means

For arbitrary bounded interactions preserving the declared symmetries, K is the whole corresponding joint symmetry sector. All its spectrum must be included. If interactions are restricted to a smaller operator algebra, the theorem can instead be applied to a genuinely common reducing subspace containing psi and invariant under H and every allowed interaction. A spectral density computed from one convenient source vector does not by itself establish that smaller invariant space. The one-sided criterion is not necessary for stability against specially chosen interactions that preserve additional local energies or annihilate the target.

### Uniform stability under an arbitrary bounded perturbation

In the positive one-sided case, let W_N be any self-adjoint operator on the product sector with \(\|W_N\|\le v<\delta/2\), independently of N. The target continues to a unique rank-one isolated eigenprojection. Its eigenvalue lies in [-v,v], its gap is at least \(\delta-2v\), and the projection displacement tends uniformly to zero with v/delta. The same conclusion holds at the upper edge in the negative case. This follows directly from the gap, the bounded spectral shift, and the Riesz projection along the homotopy t W_N.

Conversely, two-sided spectrum rules out such a uniform guarantee for the class of **all bounded symmetry-preserving perturbations**. Given an arbitrarily small epsilon, choose N and a unit vector \(\phi\in Q_N\) with \(\|K_N\phi\|<\epsilon\), using a narrow spectral interval around a complementary spectral point near zero. Write \(w=K_N\phi\), \(\alpha=\langle\phi,w\rangle\), and define

\[
W_N=-|w\rangle\langle\phi|-|\phi\rangle\langle w|
+\alpha|\phi\rangle\langle\phi|.
\]

Then W_N is self-adjoint, has norm at most 3 epsilon, annihilates the original target, and satisfies \((K_N+W_N)\phi=0\). Thus an arbitrarily small allowed perturbation produces a second eigenvector at the target energy. The operator can be extended by zero on other symmetry sectors, preserving all the declared symmetries. Adding an arbitrarily small coupling between phi and the target also shows the absence of uniform eigenvector stability.

This construction is generally an N-body, nonlocal bounded operator. It proves necessity for the stated unrestricted perturbation class, not a theorem that every two-body or nearest-neighbor coupler causes loss. Section 2 supplies an explicit ordinary density coupler that opens a channel for the particular ladder. Neither spectral overlap nor the abstract perturbation construction alone proves irreversible decay.

## 9. The perturbation norm and bounded spectators matter

The uniform statement controls the **total operator norm** of W_N. A bound on every individual pair term is insufficient when the number of terms touching a unit can grow.

A simple counterexample uses local two-level Hamiltonians \(h_i=\delta|1\rangle\langle1|_i\), with target all zeros. Define

\[
W_N=-\eta\sum_{j=2}^N
|1\rangle\langle1|_1\otimes|0\rangle\langle0|_j.
\]

Each spectator term has norm eta and preserves every diagonal local symmetry. The state with only unit 1 excited has energy \(\delta-\eta(N-1)\). Choosing \(\eta=\delta/(N-1)\) closes the gap even though every individual coupling tends to zero as N grows. This is a gap counterexample, not a decay claim. Uniform bounds at fixed interaction strength per edge require further assumptions such as bounded coordination and an applicable many-body stability theorem; neither is established here.

A scalar spectator shift \(c_N I\) leaves the gap unchanged. A general additional spectator operator of total norm d changes the elementary guaranteed gap by at most 2d and must be counted in the same perturbation budget. Merely calling each spectator contribution bounded does not provide an N-independent budget.

## 10. An ordinary one-sided comparator with a nonzero interaction

There is a conventional comparator that meets the uniform-gap criterion without an embedded pair. Use two hard-core memories of energy epsilon coupled to a common bosonic bath with

\[
\sigma(h_b)\subseteq[\Omega,\infty),\qquad \Omega>\varepsilon,
\]

and square-integrable coupling vector f. A concrete finite-band choice is a semi-infinite chain centered at 5 with nearest-neighbor hopping -1/2, memories at epsilon = 3, and equal endpoint coupling g from both memories. The bath band is [4,6].

The number-conserving Hamiltonian is

\[
H=\varepsilon(n_L+n_R)+d\Gamma(h_b)
+g\big[(\sigma_L^++\sigma_R^+)a(f)
+a^\dagger(f)(\sigma_L^-+\sigma_R^-)\big].
\]

At g = 0, in the **full physical two-excitation sector**, the bare state LR is the unique ground state at \(2\varepsilon\). Every other configuration contains at least one bath excitation and has energy at least \(\varepsilon+\Omega\). Thus the gap is \(\Delta=\Omega-\varepsilon\), without needing rail parity. In this fixed sector the coupling is bounded; for example the conservative estimate \(\|gV\|\le4|g|\|f\|\) follows from the truncated creation/annihilation norms. If \(2\|gV\|<\Delta\), the unique pair branch remains the ground state, with gap at least \(\Delta-2\|gV\|\). Sharper constants are possible but unnecessary for the conclusion.

All accessible complementary spectrum now lies above the pair eigenvalue. Tensor products of these pair branches in fixed-two-excitations-per-unit sectors have a gap bounded below by the local gap, independently of the number of units. Any interunit couplers preserving those sectors and satisfying an N-independent total norm budget below half that gap preserve a rank-one isolated branch. Parity preservation is not additionally required for this gap argument.

The comparator is still nonlinear. Let

\[
m(z)=\langle f,(z-h_b)^{-1}f\rangle.
\]

Below the bath, \(m(\varepsilon)<0\) and \(m'(\varepsilon)<0\). The symmetric one-particle memory channel has self-energy \(2g^2m(z)\), while the antisymmetric channel is dark. The same hard-core rank-two resolvent expansion used in the supplied proof gives

\[
\boxed{\chi(g)=-4m(\varepsilon)m'(\varepsilon)g^4+O(g^6)\ne0.}
\]

For epsilon = 3 and bath band [4,6],

\[
m(3)=-(4-2\sqrt3)=-a,\qquad
m'(3)=-(4/\sqrt3-2)=-b,
\]

so \(\chi=-4abg^4+O(g^6)\), compared with \(-3abg^4\) in the supplied embedded-pair ladder. This coefficient does not establish a speed advantage after comparing physical coupling, control, and mode resources.

The executed `one_sided_comparator.py` checks the exact finite-Fock Hamiltonian with 24 bath sites. For g = .2, .1, .05, .025 it obtains chi/g^4 = -.62329772, -.65280829, -.66059559, -.66256967, approaching the analytic value -.6632301492. The full physical two-excitation finite-chain gap remains about 1.008 over this sweep. The associated JSON preserves the energies, overlap weights, and scope. These checks support the coefficient; the infinite-system and uniform-product gap claims follow from the preceding spectral argument, not from finite-size numerical gaps.

This is a conventional below-band dispersive construction, presented as an equally informed comparator, not as a novel device. It replaces symmetry-selected embedding by a genuine accessible spectral cutoff. Acquiring that cutoff, excluding extra electromagnetic channels, switching couplings, and controlling losses remain physical costs. The argument is number conserving and fixed at two excitations per unit; it does not prove a uniform gap for the complete many-qubit logical space containing all zero-, one-, and two-excitation code branches, nor for a non-RWA oscillator parity sector.

The precise design consequence is limited but useful: a one-sided **accessible** spectrum provides a uniform gap for tensor composition of the chosen branch; two-sided accessible continua require an additional resource for arbitrary-size gap-based protection. An embedded state could still satisfy the one-sided condition within its own true invariant sector while lying in another sector's global continuum, but the supplied two-band pair has continua on both sides within its own sector and therefore does not.
