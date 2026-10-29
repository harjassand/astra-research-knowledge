# Direct complex receiver for resolved symmetric velocity data

## The acquired model-side operation

Supply an independent initial velocity sampler for a centrally symmetric
law mu_0 in3D with |V_0|<=R, and a declared Gaussian variance s>R^2.
For the same normalized unit-rate homogeneous isotropic Maxwell model,
the operation generates an ideal-law sample from `mu_t*G_s` at ANY finite
elapsed t. Equivalently it samples the Maxwell solution initialized by
`mu_0*G_s`; common Gaussian convolution commutes with the collision gain.
The output is not the unsmoothed mu_t law, a particle path or a gas experiment.

This version consumes root's direct-complex idea, whole-reviewed separately
in ROOT_COMPLEX_REVIEW. It replaces the older polarization receiver in
RESOLVED_INITIAL_DATA for this input class. The old programs/results remain.

## Exact physical even-moment transport

Set kappa=R^2 and d_q=(2q-1)!!. For complex Hermitian-unit z define
`F_q(z,t)=E(z.V_t)^(2q)/(d_q kappa^q)`; the inner product here is BILINEAR.
The initial terminal sample `(z.V_0/R)^(2q)/d_q` has modulus<=1.

At a collision Haar R_3 let A=(I+R_3)/2,B=(I-R_3)/2. Central symmetry
makes every odd moment vanish. The raw coefficient, BEFORE any angular
integration, is exactly
`binom(2q,2j)d_j d_(q-j)/d_q=binom(q,j)`.
With U=||A^Tz||^2 and1-U=||B^Tz||^2, draw J~Binomial(q,U), normalize
occupied child vectors and continue them independently. This produces the
correct moment gain. The two norm squares add to1, even for complex z.

For q>=2 each collision separates with conditional probability>=1/3:
write z=u+iw, and apply convexity of U^q+(1-U)^q to the real/imaginary
norm-weighted mixture of two marginal Uniform[0,1] variables. Their
correlation is allowed. Thus the expected number of collisions before
separation/time termination is<=3. At most q-1 separations occur.

For q1, use the ordinary covariance evolution. Draw ONE initial V_0 and
return `(z.V_0/R)^2` with probability exp(-t/2); otherwise return
`|V_0|^2 z^Tz/(3R^2)`. Both values are bounded, with exactly the right mean.
This is raw covariance/trace compression, not a Gaussian-mixture assumption.
Conditioning on first collisions and induction prove that the product H_q
is bounded by1 and unbiased for F_q. Finite initial support ensures all
finite-time moments exist; the bounded dual then gives all-time Gaussian
normalized moment bounds. The resulting characteristic series is entire.

Expected collision/initial work is O(q), in ideal standard-random/arithmetic
units. There are<=2q-1 conceptual genealogical blocks. The program separately
counts raw iterations (including nonsplit continuations), whose expectation
is<=4q-3, and actual source draws. Worst-case work is unbounded.

## Full-law contour and factory

The even moment expansion is
`hat mu_t(k)=sum_q (-kappa/2)^q |k|^(2q) F_q(k/|k|,t)/q!`.
For the Gaussian-resolved density shift the Fourier contour to
`xi-i v/g`, where `g=s+kappa`, and use frequency precision
`beta=s-kappa>0`. Draw xi~N(0,beta^-1 I), z=xi-i v/g,
K~Poisson(kappa||z||^2/2), and define

`W(v)=C Re[(-1)^K exp(i(s/g-1)xi.v) H_K(z/||z||,t)]`,
`C=(g/beta)^(3/2)`.

Then |W|<=C and E W=f_t(v)/G_g(v). The Poisson factor broadens frequency
precision from s to beta; its velocity term cancels the contour prefactor
because g-s=kappa. Absolute Gaussian domination uses beta>0. No4^K
polarization or radial closure remains.

Let E_0=E|V_0|^2, acquired from the supplied table or conservatively replaced
by R^2. Energy conservation, zero mean and Jensen give
`f_t(v)>=G_s(v) exp(-E_0/(2s))`. Therefore the ratio lower envelope is
`ell(v)=exp(-E_0/(2s))(g/s)^(3/2) exp[-|v|^2(1/s-1/g)/2]`.

Huber's credited multiplier2 factory turns W into an acceptance coin of
mean f_t(v)/(C G_g(v)). Independent G_g proposals return EXACT f_t in the
ideal model. Every rejected attempt is charged. Put

`I=exp(E_0/(2s))[s^2/(g beta)]^(3/2)`.

Then expected signed queries/output<=19 C^2 I and expected total degree
is at most that times `(3kappa/2)[1/beta+s/(g beta)]`. This integrates all
outcome-correlated source/degree work using the requested-query and proposal
renewal identities. Finite time-input encoding and fair-bit computation are
separate, not zero-cost claims.

## Executed discriminating source and ordinary comparator

The fixed source is equal mass at the six +/-coordinate unit vectors,
R=1, with DECLARED s=2. It has negative directional fourth cumulant -2/9
after Gaussian convolution; hence it is outside EVERY centered Gaussian
covariance-mixture model. The old sufficient receiver required s>4; this
new source/output uses s=2>1 and is not a variance relabeling of old runs.

The predeclared consumer uses exact rational gain/initial identities,
independent direct physical-moment ODE controls at complex directions,
known initial Gaussian-location-mixture density,1000 full outputs at
t=0/3/1000000, and1000 ordinary exact Wild outputs at t=0/3 under EXACTLY
the same initial/source/resolution contract. It retains every discrepancy.
No small sample is asserted to resolve the negative fourth cumulant; the
source separation is exact algebra. The ordinary moment hierarchy is also
charged and credited for its far cheaper moment output.

The generic terminal callback additionally accepts the acquired
ProductSignSource from COMPLEX_INITIAL_SOURCE. Its O(Jq^2) DP work is
counted separately from actual initial velocity draws. That source adapter
is implemented but is not promoted to a full-run performance result unless
the corresponding consumer is actually executed.

All executable distributions/ODEs are FLOATING diagnostics. Declared blur,
support/symmetry validation, exact random/finite-output bits, material
cross-section validity and practical superiority remain distinct interfaces.
