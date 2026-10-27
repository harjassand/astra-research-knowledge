# Local detuning destroys the embedded pair through an eighth-order channel

## Target and choice

The target is a quantitative response of the supplied interacting, symmetry-protected two-memory pair to a local fabrication error. This could determine whether its ideal conditional phase survives realistic memory-frequency mismatch. The actual available machinery is the local ladder, its complete one-body endpoint spectral measures, the even-sector pair eigenvector, and hard-core resolvent compression. The missing link is coupling to the previously forbidden odd continuum.

A materially different opening is N750's exact conditional integration of oscillatory resonant blocks. Its consequential goal is affordable sign-problem computation; the remaining global phase/variance bound is not supplied by its local regularization. Optimized contours, transfer methods, and constructive interpolation remain strong alternatives there. I chose the ladder because its missing channel can be constructed explicitly from a definite local perturbation. Conventional dispersive interactions and ordinary gapped photonic couplers remain relevant physical alternatives; this episode establishes no practical advantage over them.

## Hamiltonian and scope

Use exactly the producer's local two-rail Hamiltonian, in units hbar = B = 1. The two hard-core memories have energy 3; bath parity bands are [4,6] and [0,2], and memory-to-parity-endpoint couplings are sqrt(2) g and g. In rail coordinates these are the supplied positive direct/crossed first-rung hoppings. Add only

\[
 H_{g,\delta}=H_{g,0}+\delta V,\qquad V=n_L-n_R.
\]

Thus memory frequencies become 3+delta and 3-delta. This is a local relative-frequency error, not a wrong-band source. It preserves excitation number and breaks rail-exchange parity. In the physical two-particle Hilbert space, ||V||=1 and V|LR>=0.

The strongest result is the exact finite-g continuum spectral response below and its nonzero weak-g coefficient. A local second-sheet continuation gives a resonance pole for fixed sufficiently small g and sufficiently small delta. No explicit uniform remainder, finite experimental gate fidelity, or device realization is supplied.

## Exact constrained response

Let h_+, h_- be the two one-body Jacobi operators and mu_+, mu_- their COMPLETE memory spectral measures. In particular their in-gap bound atoms must remain. Write

\[
 G_\sigma(z)=\int\frac{d\mu_\sigma(x)}{z-x},\qquad
 L_\sigma(z)=\iint\frac{d\mu_\sigma(x)d\mu_\sigma(y)}{x+y-z}.
\]

Let lambda = E_p(g) solve L_+(lambda)+L_-(lambda)=0, as in the source. Define

\[
 N_g=\sqrt{\frac{2}{L_+'(\lambda)+L_-'(\lambda)}},\qquad
 J_\sigma(x)=\int\frac{d\mu_\sigma(u)}{x+u-\lambda}
             =-G_\sigma(\lambda-x).
\]

All J values used on their own measure's support are real: the even-sector continuum avoids lambda.

In harmonic two-boson coordinates the forbidden even and odd double-memory states are

\[
 q_e=(|++\rangle+|--\rangle)/\sqrt2,\qquad q_o=|+-\rangle.
\]

The normalized physical even pair is

\[
 \psi_p=\frac{N_g}{\sqrt2}
 \big[(h_+\otimes1+1\otimes h_+-\lambda)^{-1}|++\rangle
    +(h_-\otimes1+1\otimes h_--\lambda)^{-1}|--\rangle\big].
\]

Its q_e overlap vanishes by the root equation. Since V q_o=2 q_e, the odd vector eta=V psi_p is automatically orthogonal to q_o. In the product spectral representation L2(mu_+ x mu_-), it is exactly

\[
 \boxed{\eta(x,y)=N_g[J_+(x)+J_-(y)].}\tag{1}
\]

The odd *physical* Hamiltonian is the compression of h_+ tensor 1 + 1 tensor h_- away from q_o. It is not the unconstrained product Hamiltonian. Put, for Im z>0,

\[
 K(z)=\iint\frac{d\mu_+(x)d\mu_-(y)}{x+y-z},\quad
 C(z)=\iint\frac{\eta(x,y)d\mu_+(x)d\mu_-(y)}{x+y-z},
\]
\[
 D(z)=\iint\frac{\eta(x,y)^2d\mu_+(x)d\mu_-(y)}{x+y-z}.
\]

The rank-one compression identity gives the exact full response

\[
 \boxed{\langle\eta,(H_{g,\mathrm{odd}}-z)^{-1}\eta\rangle
             =D(z)-C(z)^2/K(z).}\tag{2}
\]

There is no complex conjugate on C squared in this analytic resolvent identity. At z=lambda+i0 the only open channel is upper-continuum plus lower-continuum. If rho_sigma is the continuous part of mu_sigma and alpha=C/K at that boundary, Stone's formula becomes the manifestly positive expression

\[
 \boxed{S_g(\lambda)=\int_{\max(4,\lambda-2)}^{\min(6,\lambda)}
 \rho_+(x)\rho_-(\lambda-x)
 |\eta(x,\lambda-x)-\alpha|^2\,dx.}\tag{3}
\]

To verify the positivity identity directly, write Im K=pi integral rho_+ rho_-, Im C=pi integral eta rho_+ rho_-, and Im D=pi integral eta^2 rho_+ rho_-. Substitution into Im(D-C^2/K) yields pi times (3). The source's pair must be scattered against the *constrained* odd states, which contribute the subtraction alpha.

The second-order pole width is therefore

\[
 \boxed{\Gamma_{\rm pole}(g,\delta)
     =2\pi\delta^2S_g(\lambda)+O_g(\delta^4).}\tag{4}
\]

Here Gamma=-2 Im z_pole, a probability-linewidth convention. The amplitude linewidth is half this value. Equation (3) is an exact spectral coefficient; assigning a time-domain exponential over a specified gate duration needs a separate remainder estimate.

## Local resonance construction

For fixed sufficiently small g>0, lambda=6-a g^2+O(g^6) lies strictly in (4,6), away from the mixed two-band sum thresholds 4,6,8, the bound-plus-band thresholds, and the harmonic bound-pair poles. The memory one-body resolvent with detuning is an explicit 2x2 inverse with the two half-line Weyl functions as self-energies. Its bound atoms and band densities depend analytically on delta near zero.

The forbidden two-double-memory Green matrix M(z,delta) is the symmetric tensor convolution of these complete one-body matrix measures. Its continuous densities are real analytic near lambda. For example, for E in (4,6) the mixed-band integral has x in [4,E]. Substitution x=4+(E-4)t turns its endpoint square roots into sqrt(t(1-t)) times a function analytic in E in a neighborhood of lambda. Remaining endpoint factors stay nonzero there. Rational/algebraic one-body denominators are nonzero on the open bands at the admitted small coupling. Thus the Cauchy transforms have a local continuation through this open interval, with the ordinary spectral jump. This is a local second sheet; no continuation through the threshold E=6 is asserted.

At delta=0, M is diagonal in q_e,q_o with entries (L_++L_-)/2 and K. The first entry vanishes simply: its z derivative is (L_+'+L_-')/2>0. K has positive imaginary part because the mixed-band density is strictly positive. Hence the continued determinant has a simple zero, and the analytic implicit function theorem gives a unique continued zero z_pole(delta) near lambda. The physical pair resolvent has nonzero residue there at delta=0, so this zero remains a physical resolvent pole. Parity takes delta to -delta, making its Taylor series even. Second-order Feshbach expansion gives Im z_pole=-pi delta^2 S_g(lambda)+O_g(delta^4), establishing (4).

This construction gives existence for fixed g and sufficiently small delta. It provides neither an explicit admissible delta(g) nor a bound uniform as g tends to zero. The local continuation's distance from the E=6 threshold itself shrinks like g^2; silently exchanging these limits would be invalid.

## Nonzero eighth-order coefficient

Set

\[
 a=4-2\sqrt3,\qquad b=4/\sqrt3-2=a/\sqrt3.
\]

The source's one-body Schur equations and connected shift give

\[
 E_+=3-2ag^2+4abg^4+O(g^6),\qquad
 E_-=3+ag^2-abg^4+O(g^6),
\]
\[
 Z_+=1-2bg^2+O(g^4),\quad Z_-=1-bg^2+O(g^4),\quad
 \lambda=6-ag^2+O(g^6),\quad N_g=3ag^2+O(g^4).
\]

Evaluate (1) on the mixed bound-bound atom. The order g^-2 terms in J_+(E_+)+J_-(E_-) cancel, leaving

\[
 J_+(E_+)+J_-(E_-)=-b/(3a)+O(g^2),\qquad
 \eta_{bb}=-bg^2+O(g^4).
\]

The pole at E_++E_- differs from lambda by -chi=3abg^4+O(g^6). It dominates K and C, whereas their remaining bound-continuum terms are O(g^2). Consequently

\[
 \alpha=\eta_{bb}+O(g^6)=-bg^2+O(g^4).
\]

On the open shell, G_+(6-x)+G_-(x) cancels at g=0, so eta(x,lambda-x)=O(g^4). Thus it is the hard-core scattering correction, rather than the bare eta shell amplitude, that supplies the leading response:

\[
 \eta(x,\lambda-x)-\alpha=bg^2+O(g^4).
\]

The continuous measures obey

\[
 \rho_+(x)=\frac{2g^2\rho_{5}(x)}{(x-3)^2}+O(g^4),\qquad
 \rho_-(6-x)=\frac{g^2\rho_{5}(x)}{(x-3)^2}+O(g^4),
\]

where rho_5(x)=(2/pi)sqrt(1-(x-5)^2) on [4,6]. Dominated convergence applies after scaling out g^8. The remaining elementary integral is

\[
 I=\int_4^6\frac{\rho_5(x)^2}{(x-3)^4}\,dx
  =\frac4{\pi^2}\int_1^3(-u^{-2}+4u^{-3}-3u^{-4})\,du
  =\frac{16}{27\pi^2}.
\]

Therefore the exact finite-g spectral coefficient has the asymptotic

\[
 \boxed{2\pi S_g(\lambda)
    =\frac{64b^2}{27\pi}g^8+o(g^8)
    =0.0722287299930597\ldots\,g^8+o(g^8).}\tag{5}
\]

In particular S_g(lambda)>0 for all sufficiently small nonzero g. A sufficiently small nonzero local relative detuning converts this protected eigenvalue into a resonance. Its leading probability linewidth is quadratic in the fabrication error and eighth order in the memory-bath coupling. The limits here are delta to zero at fixed g, then g to zero for the coefficient.

## Executed checks and retained failed shortcut

`local_detuning_response.py` evaluates the infinite-chain Weyl functions, both bound atoms, the pair root and normalization, and the positive convolution (3). It uses NumPy 2.5.3 with standard-library Python, no source script with legacy output paths. Split cosine quadrature removes the square-root endpoint behavior.

| g | Gamma_pole / delta^2 | Gamma_pole / (delta^2 g^8) |
|---:|---:|---:|
| 0.40 | 1.27579535e-5 | 0.0194670921 |
| 0.20 | 1.33675190e-7 | 0.0522168710 |
| 0.10 | 6.66175248e-10 | 0.0666175248 |
| 0.05 | 2.76504757e-12 | 0.0707852177 |
| 0.035 | 1.61049949e-13 | 0.0715181441 |
| g -> 0 | asymptotic | 0.0722287300 |

At g=.2, 80/160/320 quadrature nodes give scaled coefficients 0.0522168709685924, 0.0522168709685923 and 0.0522168709685904. The two independent imaginary-part shell identities agree to about 1e-19 and 1e-21 at 160 nodes. These are floating-point quadrature checks, not interval certificates.

`finite_fock_audit.py` separately builds the full physical two-particle Fock Hamiltonian with 6,10,14 sites in each bath band, diagonalizes it, forms the perturbation times psi_p directly, and compares its complex resolvent with (2) at three nonreal spectral arguments. It checks both the memory error and the first-rung error constructed below, for eighteen comparisons. Vector norms and the forbidden overlap also agree. A finite chain does not have a continuum linewidth; this check validates the response identity, not a lifetime.

The failed shortcut is retained numerically: omitting the odd hard-core compression gives a false g^12 leading response. At g=.2 its on-shell density is about 1.4262e-11, while the correct constrained value is 2.1275e-8, about 1492 times larger. The cancellation V|LR>=0 alone does not protect the dressed pair.

## A constructed local counterterm with a strict residual

There is a second microscopically local control: shift just the first rail rung's oscillator frequencies by opposite amounts,

\[
 W=n_{A_0}-n_{B_0}=b_{+,0}^\dagger b_{-,0}+b_{-,0}^\dagger b_{+,0},\qquad
 H=H_{g,0}+\delta V+\epsilon W.
\]

This is an actual site-frequency perturbation of the connected ladder. It does not insert a spectral source by hand. In the memory spectral representations, the endpoint bath vectors have coordinates

\[
 f_+(x)=(x-3)/(\sqrt2g),\qquad f_-(y)=(y-3)/g,
\]

because the memory row of the one-body eigenvalue equation gives c_sigma times bath endpoint amplitude = (E-3) times memory amplitude. Define

\[
 H_\sigma(s)=\int\frac{f_\sigma(u)d\mu_\sigma(u)}{s-u}
       =\frac{(s-3)G_\sigma(s)-1}{c_\sigma}.
\]

The exact first-rung response vector is

\[
 \eta_W(x,y)=-N_g[f_-(y)H_+(\lambda-x)+f_+(x)H_-(\lambda-y)].
\]

Its C value is the same one-dimensional formula as the memory response with G replaced by H:

\[
 C_W=N_g\left[\int H_+(\lambda-x)H_-(\lambda+i0-x)d\mu_+(x)
              +\int H_-(\lambda-y)H_+(\lambda+i0-y)d\mu_-(y)\right].
\]

K is unchanged. Thus (3) applies to the exact linear combination delta*(eta_V-alpha_V)+epsilon*(eta_W-alpha_W). No cross-channel rate is guessed or added incoherently.

At small g, alpha_W=O(g^4), while on the open shell

\[
 \eta_W-\alpha_W=\frac{3a}{\sqrt2}m_1(x)g^2+O(g^4),\qquad
 m_1(x)=2[(x-1)-\sqrt{(x-1)^2-1}].
\]

The leading terms on the mixed bound atom cancel for this perturbation, giving alpha_W=O(g^4). Combining with the memory result yields the acquired positive quadratic form

\[
 \boxed{\Gamma_{\rm pole}\sim4\pi g^8\int_4^6
 \frac{\rho_5(x)^2}{(x-3)^4}
 \left[b\delta+\frac{3a}{\sqrt2}m_1(x)\epsilon\right]^2 dx.}\tag{6}
\]

The meaning is the quadratic coefficient in the joint small-error expansion, followed by g to zero. Its Gram matrix, in order (delta,epsilon), is numerically

\[
 M=\begin{pmatrix}
 0.0722287299931&0.0764655091748\\
 0.0764655091748&0.0818535681928
 \end{pmatrix}.
\]

This also supplies a constructive local compensation, rather than merely observing fragility:

\[
 \epsilon_*=-\frac{M_{12}}{M_{22}}\delta
            =-0.934174414911\ldots\,\delta.
\]

Its residual coefficient is

\[
 \boxed{\Gamma_{\rm pole}\sim0.000796607698822\ldots\,\delta^2g^8.}\tag{7}
\]

This is 0.011029 of the uncompensated memory-error coefficient, a reduction of about 90.7 in this leading coefficient. It does not vanish: the two Gram functions 1 and m_1(x) are not proportional on an interval of positive weight, so strict Cauchy-Schwarz proves M positive definite. No nonzero choice of these two local errors restores a zero leading width. If epsilon=epsilon_*+Delta epsilon, the leading coefficient becomes (M11-M12^2/M22)*delta^2+M22*(Delta epsilon)^2; the calibration error is explicit.

`local_compensation.py` computes the integral matrix and the complete finite-g second-order matrix from (3). At g=.2 its optimum is epsilon/delta=-0.87110445 and its remaining fraction is 0.0153891; the asymptotic ratio should not be used unchanged at finite coupling. The compensated finite-g coefficient divided by g^8 is 0.00080357036 at g=.2 and 0.00079696516 at g=.025. Both individual response vectors are checked against physical Fock matrices by `finite_fock_audit.py`.

This control requires an estimate of delta and an independently adjustable antisymmetric first-rung frequency. Neither is acquired experimentally. Directly retuning the two memory frequencies, when available, removes delta itself and is the stronger ordinary control. The constructed counterterm is relevant to an interface where the first-rung frequency is accessible but memory retuning is constrained; no such hardware advantage is established here.

The local counterterm retains an explicit stability regime. After eliminating both rail tails at zero energy, the first-rung bath Schur matrix is

\[
 K_0=\begin{pmatrix}5/2+\sqrt6&\epsilon\\\epsilon&1/2\end{pmatrix}.
\]

For |epsilon|<=.1 its least eigenvalue is at least .4. The memory block has least eigenvalue at least 2.9 for |delta|<=.1, and the endpoint coupling matrix has norm squared at most 2g^2<=.32. Its Schur complement is therefore at least 2.9-.32/.4=2.1. The one-body Hamiltonian stays nonnegative in this explicit regime; second quantization and hard-core compression retain nonnegativity in every particle sector. This is stability, not a lifetime or occupancy-capacity claim.

## Gate implication and ordinary loss

Using the source's chi=-3abg^4+O(g^6), a CZ plateau has total hold time pi/|chi| across the two echo halves. The formal leading radiative loss exponent from this error alone would be

\[
 \Gamma_{\rm pole}\,\pi/|\chi|
 \sim \frac{64}{81\sqrt3}\delta^2g^4.
\]

This is a pole/plateau consequence, not an inclusive gate error bound. It does not include loading, unloading, relative one-body calibration, or echo errors.

The same computation retains the actual bath population. Exactly,

\[
 \|V\psi_p\|^2=P(\text{one memory occupied}),\qquad
 \langle N_{\rm bath}\rangle=2-2|\langle LR|\psi_p\rangle|^2-\|V\psi_p\|^2.
\]

Both quantities are 3b g^2+O(g^4). If every bath oscillator has ordinary Markov loss rate kappa, the initial jump rate is kappa times this population. Its formal pair-plateau exponent is pi*kappa/(a*g^2), increasing when g decreases. Thus suppression of this one detuning channel does not establish a useful gate in a lossy ladder. The required noise/actuator interface has not been acquired.

## Exact residual obligation and next attack

The unresolved obligation is a quantitative time-domain error estimate, uniform in a stated joint regime of g, delta, ramp duration and bath loss, for the actual two-cycle code isometry. The local continued pole supplies no explicit O_g(delta^4) constant and does not by itself bound a long gate's background, initial slip, or ramp-created radiation. The limits cannot be exchanged without this work.

The next attack is to use (2) to bound the odd-sector spectral kernel over an explicit energy window, combine it with the source's even-sector gap for the complement, and optimize finite ramps against leakage. The exact fixed-time second-order loss is

\[
 \delta^2\int\frac{4\sin^2((E-\lambda)T/2)}{(E-\lambda)^2}
 \,d\mu_{\eta}^{\mathrm{odd,hc}}(E),
\]

with the constrained measure determined by (2). This specifies the missing kernel rather than inserting a lifetime oracle. Controlling its remainder over T of order g^-4 is still required. A circuit/Maxwell realization, full control costs, measured noise, historical novelty and practical comparator advantage remain unestablished.

## Sources and credit

- Supplied `ASTRA_SYMMETRY_FILTERED_EMBEDDED_PAIR_20261027.md`, SHA-256 b465b21250366e67b0e341951b5d2a0ae64df18be495e831b81e7b8b35f19730: governing local Hamiltonian, protected pair, chi, stability and qualitative CZ. These existing results are credited, not rediscovered. The new calculation is the local n_L-n_R response, its constrained kernel, and coefficient (5).
- Supplied `astra_symmetry_filtered_embedded_pair.py` and local-ladder audit: governing spectral conventions and Hamiltonian parameters. Their legacy /mnt/data output paths were never executed or written.
- Astra corpus navigation read at frozen revision `c1b8ac1516457a88b383a6350680e3be865fbffd`; its task-first and scope requirements were retained. No changing HEAD, shared build or source mutation was used.
- Supplied `N750_governing_source.txt`: materially different opportunity and its global phase-control gap. The generic N1077 compiler is already complete at its promised class and was not treated as an unsolved contraction theorem.
- [Soffer and Weinstein, Time Dependent Resonance Theory, arXiv:chao-dyn/9804033v1](https://arxiv.org/abs/chao-dyn/9804033v1): established distinction between a nonzero golden rule and the local-decay hypotheses needed for a time-dependent resonance theorem.
- [Lee and Zworski, A Fermi golden rule for quantum graphs, arXiv:1602.04866v1](https://arxiv.org/abs/1602.04866v1): perturbing embedded graph eigenvalues is established machinery, not a new principle claimed here.
- [Yue Chang, Two-Photon Bound States in the Continuum: A No-Go Theorem and Long-Lived Quasi-Bound States, arXiv:2608.16527v1](https://arxiv.org/html/2608.16527v1): its single-nonlinear-mode no-go uses positive spectral convolutions. Our two hard-core memories and separated parity bands have a different interface; this reference does not invalidate the supplied protected construction or establish our priority.

Firecrawl retrieval failed once because its account had insufficient credits. No retry or paid expansion was made; the primary public pages above were read through ordinary web retrieval. Priority of the model-specific coefficient has not been established.
