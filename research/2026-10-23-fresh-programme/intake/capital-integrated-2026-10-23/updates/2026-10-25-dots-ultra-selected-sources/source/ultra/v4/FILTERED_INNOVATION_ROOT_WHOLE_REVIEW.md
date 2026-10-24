# Root whole review: local initial-state Gaussian comparison

25 October 2026. Internally verified/accepted at the following mathematical
scope and versions, after root read the complete owner arguments and
independently reconstructed their load-bearing steps:

- LOCAL_GAUSSIAN_ENVELOPE.md, SHA256
  e32666266c1dc660dcd32cdcd4c63242bdfbcd4862a384c4b27b32f9d3a8af55.
- SOFT_JOINT_ENERGY.md, SHA256
  4f441b2edefd2b06597ae25941620a788887ed57ac28fcf4464d134a100a9d22.
- ROOT_EXACT_WAVEPACKET_REFERENCE.md, SHA256
  2c23c95ab917520a43fc10fcb1898f0167e065dd1ea213b72f67f6aef18ca926;
  owner independently checked root's full reference construction.

The exact mixed finite difference A_F cancels paths missing any mark.
Selection includes every bath cluster able to act at a marked location.
Only genuinely outside contacts enter the arbitrary enlarged-system
background; all selected unmarked contacts remain in Wick expansion.
Norm-bounded dressed system factors preserve the Gaussian skeleton estimate
uniformly in the enlarged input state. Root checked the numerical skeleton
sum against Ng--Preskill's governing equations (9), (27), (44)--(45),
(59)--(67), and its mixed-Gaussian input discussion:
https://preskill.caltech.edu/pubs/preskill-2009-gaussian.pdf .

Positive comparison of the SAME A_F^dagger A_F then yields
epsilon_NG^2<=C^nu 2eE. The hard-support rank lemma is valid for arbitrary
initial correlations. Its optimal displayed thermal comparison constant
and the special vacuum case check. The angular-frequency normalization
was repaired before accepting the listed version.

The soft extension is also valid. Weighted block Cauchy, followed by
rho_nn<=exp(-beta E_n)Omega, proves rho<=Z exp(-beta K/2) tensor Omega.
Normalizing gives C=MZ^2 with a T-dependent tilted outside state. Root's
earlier infinite-Schmidt counterexample excludes keeping the original
outside marginal; it does NOT exclude this tilted state. The supplement
correctly preserves that distinction. Product Poisson COUNT laws survive
arbitrary initial number-diagonal phase unitaries, so the stated entangled
non-Gaussian class has the required all-selected-set moments. Marginal
moments alone do not supply them.

The wavepacket example is exact: positive-frequency f(omega) is normalized,
K(t)=(1+i omega_c t)^(-2), its modulus is integrable, and the nonstationary
Gaussian covariance yields E_contact<=pi g^2 t0(1+n_ref)/omega_c. The
interaction form condition is finite although a dressed-ground-state norm
condition diverges; no dressed ground state is claimed or needed. Fixed
Ohmic strength must not be confused with fixed normalized g when changing
the cutoff.

Acceptance is of an all-set INITIAL-state transfer theorem under the
displayed independent quadratic-cluster, linear-contact, unitary-domain,
integrable covariance and conventional QEC-receiver assumptions. These
are actual hypotheses. It establishes neither a finite-energy-only theorem
nor arbitrary nonlinear bath dynamics, continual non-Gaussian replenishment,
or an acquired preparation/coupling/QEC apparatus. Those are separate open
scientific operations, not reasons to withhold acceptance of this theorem.

## Continued classical-source construction

Root whole-read FILTERED_INNOVATION_FT.md, SHA256
afb23474eef080faa7f23bd31abb935e5efaa5aa6a266d05b960f59b2f29154c.
It is internally verified/accepted for its defined fixed-slot exogenous
classical-source circuit, as a separate result from the quantum initial-state
comparison above.

The exact marked-path product retains all unmarked noisy unitaries. Its
L2 norm after classical purification is bounded by the joint product angle
moment for arbitrary logical/reference input. Root independently recovered
the Gaussian-auxiliary determinant bound, its trace/norm relaxation, and the
choice t=1/[2(R+V)], giving epsilon_cl^2=2(R+V)/sqrt(e). The V=0 endpoint,
stable-filter convolution/Fatou argument and AR(1) constants check. The
quartic innovation density has the stated Gaussian absolute-value stochastic
domination and hence joint sub-Gaussian input proxy. The local deterministic
implementation-error addition follows by Minkowski and an all-subset binomial
expansion, with its uniform locality/source-law conditions retained.

Root read HKZ's Theorem1/Remark2/proof,
https://arxiv.org/html/1110.2842 , and SchWARMA's source law/Eqs.(5),(9),
https://arxiv.org/pdf/2010.04580 . These support the stated conventional
concentration and correlated-circuit architecture ancestry. The present
composition does not establish a new noise architecture or a priority claim.

Acceptance is not a theorem for quantum backaction, noncommuting innovations,
adaptive source sampling, or general nonunitary SchWARMA dynamics. The source
law is a premise; finite records/PSD fits, a PRNG, or the one-sample thermal
density do not acquire it. Actual refresh, entropy, calibration and full QEC
apparatus remain independent physical operations. The next quantum-injection
question is not solved by renaming this classical purification a quantum bath.
