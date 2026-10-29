# Receiving review: selective physical family, finite acquisition and integrated response

29 October 2026. Independent mathematical review by the existing
record-geometry role. No new agent or tests were added. Root files were
not edited. This review includes the updated context-dependent SSEP
receiver and the further relative-response result.

## Actual reviewed versions

    SELECTIVE_KINETIC_ANNEALING.md
    SHA256 53b1a25cc73ba0802085ab82bca8e7560a0854dd71184b4be33b1cab1eb39350

    FINITE_ACQUISITION_AND_RESPONSE.md
    SHA256 91711b60d4488a1b147ef3bf98dc1225ff89efc7d1a57888b2893441c2915afb

    RELATIVE_COLLECTIVE_RESPONSE.md
    SHA256 03df6fe085c502bd27e2e425fc5a9ea17633b33d5a5cefd6e7732e83b490bd79

All three are under new_science/continuation5_20261029. Exact snapshots
with the SHA prefix in each filename are saved in this review directory.
The governing compressed theorem remains the previously accepted
GAP_FREE_SELECTIVE_AVERAGING.md at SHA256
9df1e444eefdf5223a97e48cbbe5145339d4b00ae6521bd7f9208482e7b5eeae.

## Verdict

**Accepted at the stated interfaces.** I found no required mathematical
correction in these actual versions. The arbitrary frozen parameter,
context-dependent modulation, independent phase-fiber bath, continuous-
rate intervals, joint terminal-law confidence budget and relative
integrated-response bounds are consistent with the governing theorem.

This is not acceptance of the forthcoming separate deterministic mirror
comparison or an apparatus implementation. It does not establish
historical novelty or a favorable resource cost.

## 1. Context-dependent rates and the local projection identity

The class-constant mobility multiplication commutes with E_i and A_i.
For a visible u, the conditional covariance expression for ||bu||^2 is
valid pointwise in the visible configuration, even when pi has strong
many-body correlations. Under the stated covariance bound it is at most

    M sum_i E_pi[m_i |A_i u|^2].

Because m_i commutes with the orthogonal projection A_i,

    <A_i u,m_i A_i u>=<u,m_i A_i^2 u>=<u,m_i A_i u>.

Thus equation (4) has the correct constant. Independence of visible
sites was not used. The warning that a general reversible endpoint
kernel supplies only A_i^2<=2A_i is necessary and is correctly retained.

## 2. Arbitrary frozen Z and the phase-fiber inequality

For fixed Z, each centered mobility is s_i alpha_i cos(theta_i).
Its conditional phase mean is zero. Different i cross terms vanish
under the independent uniform phase coordinates, even when Z is shared
by all sites and every alpha_i depends arbitrarily on Z. Its variance
is s_i^2 alpha_i^2/2, giving M<=smax a0^2/2.

The phase-averaging projection R leaves every function of (Y,Z)
unchanged. Since Rbu=0, only (I-R)v pairs with bu. The tensorized circle
Poincare inequality on each fixed (Y,Z) fiber gives

    ||(I-R)v||^2<=<v,Hv>.

This proves the required relative bath-energy condition. It does not
assert a full hidden gap. The average s_i being independent of Z is
essential: otherwise bu can acquire a component in ker(H), exactly as
the document's frozen-mean counterexample states.

One may apply the circle theorem separately at every fixed Z and
integrate the uniform bound over any law of Z. This also justifies the
receiver for arbitrary measurable frozen amplitudes without requiring
a Fourier approximation in the Z coordinate. The declared equilibrium
has visible law pi in each sector. Other conditional visible starting
laws use their actual density contract in the acquisition document.

The sign-reversal alternative has mean-zero fair signs, mobility
variance at most s_i^2 a0^2, and sign-bath gap 2gamma. Its bound
smax a0^2/(2gamma) is therefore correctly normalized. It genuinely
requires a phase-reversal actuator and private fresh sign randomization;
those are not consequences of phase diffusion alone.

## 3. SSEP eigenvalue, context dependence and the physical scaling clock

On a bond, the fair 10/01 refresh gives
A_i Y_i=(Y_i-Y_(i+1))/2. Summing the two incident bonds therefore
yields the discrete Laplacian with coefficient s/2. For q=2pi m/N,

    a F_q=s(1-cos q) F_q.

The swap rate and eigenvalue in the document agree. In a fixed occupancy
sector with 0<Mpart<N, the unnormalized nonzero Fourier mode has
squared L2 norm Mpart(N-Mpart)/(N-1)>0, so its stated normalization
is legitimate. The reference correlation is then exp(-omega_q t).

The added outside-bond occupation factor can destroy the actual
linear-density invariant subspace while remaining constant within its
own refresh class. The mean generator stays SSEP because the phase
mean of that factor's modulation is zero. None of the energy argument
or the Fourier receiving calculation requires the actual density
observable to have closed dynamics. The assertion is that closure
need not hold, not that it fails in every small or one-particle sector.

On t=N^2 tau, the rate is
c_N=N^2 s(1-cos(2pi m/N))=2pi^2 s m^2+O(N^-2) for fixed m!=0.
The bound |exp(-c tau)-exp(-d tau)|<=|c-d|/[e min(c,d)]
is valid uniformly in tau>=0. Hence the reference scaling error
vanishes uniformly, and any kappa_N tending to infinity removes the
additional memory error under a uniform local amplitude/rate envelope.
No N^2 bath-strength requirement has appeared. The document correctly
keeps the result at the density-mode correlation level and charges
the array's actuator number, power and preparation.

## 4. Native resolvent moments and confidence intervals

The two successive pulses are repeated applications of the actual
resolvent kernel, each with fresh independent clock/native randomness.
With the hidden state and surrounding context held fixed, their flip
scores have conditional means g and g^2, where
g=lambda/(alpha+lambda). They do not directly give exact lambda moments;
the bounded inverse inequalities in Section4 correctly supply intervals.

On the simultaneous score event, gL<=E g<=gU and
Var(g)<=qU-gL^2<=vU. Since

    alpha E g<=m<= (alpha+Lambda)E g,
    Var(lambda)<=[(alpha+Lambda)^4/alpha^2]Var(g),

the stated [L,U] and variance bounds follow. Dividing by m>=alpha gL
gives the second term in J_i. The first follows from
Var(lambda)/m<=Lambda-m<=Lambda-L. Taking their minimum is valid;
the L=0 fallback avoids division by zero. As previously reviewed, the
harmonic mean minimizes |mhat/m-1| relative to the true rate and is
therefore the correct center for the relative-form receiver.

For the phase and telegraph families, the serial concentration statement
is applied **conditional on fixed Z**. There is no contraction assertion
on all hidden functions including Z. Conditional phase/sign moments can
depend on Z; the confidence estimates cover those conditional moments
uniformly, while the native mean m=s remains Z-independent. The
simultaneous union bound need not assume independence across families.
Its stated sample counts and bath spacings are fixed declared protocols;
optional stopping or unaccounted data-adaptive sampling would need an
appropriate confidence argument.

## 5. Paid bath-only preparation and the joint record formula

The circle heat kernel relative to uniform has Fourier expansion
1+2 sum_(n>=1) exp(-kappa n^2 t) cos(n(theta-theta0)). Its TV distance
is at most the displayed sum, which is bounded by
exp(-kappa t)/(1-exp(-kappa t))<=2exp(-kappa t)
when kappa t>=log 2. The product transition kernel and a union coupling
give 2d_phase exp(-kappa t), uniformly over the initial phase vector.

For kappa>0 and an error budget 0<zeta<=1, the stated warm-up duration
therefore works. Uniformity in the initial phase row means it also
works after conditioning on arbitrary old (D,Y,Z), retaining exactly
that marginal. Independent bath innovations are needed. The explicit
requirement to turn off native Y motion during the hold is load-bearing:
a bath term which leaves Y fixed is not itself a protected hold while
the visible generator continues running. The text makes this distinction.

To check the full formula, let rho_tilde have the same actual (D,Z)
marginal and the declared conditional visible density times fresh
stationary phases. The initial TV difference from the actual law is
at most zeta, and propagating the same selected physical program costs
at most zeta by data processing. On the simultaneous good calibration
event, condition on (D,Z) and apply the two operator bounds to the
centered density. This costs at most

    (K/2)(delta_mem+delta_cal).

The bad event has the same (D,Z)-measurable probability in both laws
and costs at most beta. Thus zeta+beta+the displayed term is correct;
there is no additional old-record cardinality factor. This is a joint
frequentist result, not a per-realized-record posterior guarantee.

The warm-up does not provide K or a fresh visible Gibbs preparation.
Keeping the entire calibration record can make the conditional visible
density costly. The document expressly retains that limitation.

## 6. Relative resolvent theorem and infinite-time response

For z>0, solving the omitted equation with (z+C)^(-1) gives the
compressed resolvent [z+a-K_z]^(-1). K_z is positive. Its variational
formula and the relative energy premise yield

    0<=K_z<=r a,

because dropping -z||v||^2 only enlarges the supremum. Inverse order
then gives the entire sandwich in equation (1). For the circle
extension, the omitted block is self-adjoint on the stated form
domain, its z-resolvent is bounded, and b is bounded, so this Schur
elimination remains legitimate.

The spectral measure of a reversible autocorrelation is nonnegative.
Letting z decrease to zero therefore gives equation (5) by monotone
convergence. The condition f perpendicular to ker(a) and finite
reference inverse energy is sufficient; the upper bound also rules
out an otherwise divergent actual conserved component. Removing only
one global mean would not suffice for arbitrary reducible systems,
and the text correctly says so.

Increasing kappa raises A_kappa in form order, hence lowers its
resolvent. This supports monotonicity of integrated/Laplace response,
not pointwise monotonicity of every transient correlation. The stated
distinction is correct.

## 7. Collective relaxation coefficient and fitted response

For the normalized SSEP mode, the reference inverse energy is exactly
1/omega_q. Thus the bounds on tau_q and
s_resp(q)=1/[(1-cos q)tau_q] follow directly. The latter is monotone
in kappa because tau_q decreases. It is a specifically defined finite-
volume response coefficient; no unrelated macroscopic diffusion
convention or process limit is being inferred.

The condition kappa>=M(1+epsilon)/epsilon makes
r/(1-r)<=epsilon and is independent of the visible mode's gap.
The time itself remains of order N^2. This is a relative response
certificate, not a claim that the relaxation becomes microscopic.

Finally, (1-eps)a<=ahat<=(1+eps)a implies

    (1-eps)(z+ahat)^(-1)<=(z+a)^(-1)
       <=(1+eps)(z+ahat)^(-1).

Combining with the memory sandwich proves the fitted bounds (11),
including their conservative uniform-z constants. Off the common
conserved space the z=0 limit is justified when the reference inverse
energy is finite.

The response document correctly refuses to integrate a constant
terminal-TV error over infinite time. Its infinite-time claims concern
the exact declared equilibrium/operator response on the simultaneous
confidence event. A finite-TV warm-up alone does not supply an
infinite-horizon experimental-estimator tail bound.

## Acceptance boundary

The three reviewed files form a consistent mathematical physical-
supplier/acquisition/response chain under their declared resources.
Exact common Gibbs ratios, actual selective phase control, full local
context access, stationary conditional hidden calibration, visible
isolation for warm-up and the deployment density contract remain real
premises. They are not outputs of the finite visible measurements.
