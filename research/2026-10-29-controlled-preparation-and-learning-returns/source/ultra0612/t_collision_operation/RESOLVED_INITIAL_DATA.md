# Removing the covariance-mixture input oracle at declared resolution

## 1. Stronger changed output contract

Let the initial velocity law mu_0 be ANY supplied centrally symmetric law
supported in the ball `|v|<=R`. Independent initial draws are supplied;
there is no covariance-mixture representation assumption. Let mu_t be its
solution of the SAME normalized isotropic-cutoff homogeneous Maxwell model.
For a DECLARED Gaussian variance `s>4R^2`, this construction samples

`f_t = mu_t * N(0,sI)`

exactly in the ideal-real/random model with expected work uniform over t.
Equivalently it samples the unblurred Maxwell solution with initial law
`mu_0 * N(0,sI)`. Those are two interpretations of the same mathematical
law, not permission to add noise to a requested unsmoothed target silently.
Warm counterstreaming Gaussian-location mixtures are included. Spatial,
hard-sphere, asymmetric-input and path outputs are not included.

This removes a latent covariance-mixture acquisition requirement. It pays
instead an initial support/symmetry promise and a substantial output
resolution (or common initial thermal variance). It is not a general
high-resolution Boltzmann sampler or a measured-gas fitting theorem.

## 2. The positive even-moment dual

Let `d_q=(2q-1)!!`, `d_0=1`, and define

`a_q(n,t)=E(n.V_t)^(2q)/(d_q R^(2q))`.

Central symmetry is preserved by the collision gain, so all odd moments
vanish exactly. Expand the even directional collision moment. Its interior
term j has raw coefficient

`binom(2q,2j) integral_0^1 u^j(1-u)^(q-j) du`.

After Gaussian moment normalization the coefficient becomes exactly

`binom(2q,2j) Beta(j+1,q-j+1) d_j d_(q-j)/d_q = 1/(q+1)`.

Thus a_q obeys precisely the rotating marked hierarchy of PROOF Sections
2--4, with the SAME nonsplit angular kernel and separating rates. The only
changed terminal sample is

`[(n.V_0)/R]^(2q)/d_q`,

which lies in `[0,1]`. Singleton propagation remains hold/uniform with
weight `exp(-t/2)` because the covariance equation is the same. Therefore
the sampled H lies in `[0,1]`, has mean a_q, and costs O(q) expected initial
draws/rotations uniformly in t. In particular `0<=a_q<=1` is proved by the
positive dual; it is not inferred by comparing Taylor coefficients of an
mgf inequality.

The moment expansion is

`hat mu_t(k)=sum_q (-R^2/2)^q |k|^(2q) a_q(k/|k|,t)/q!`.

For real k the moment series is justified by uniform sub-Gaussian tails:
the positive moment bound gives `E exp(a|V_t|)<infinity` for every finite a
by summing its even series and Cauchy--Schwarz for odd absolute moments.
For complex k the same normalized homogeneous polynomial extension and
polarization apply. This is a distributional moment construction, not an
assumption that mu_t is a covariance mixture.

## 3. Full-law receiver and exact energy lower envelope

The collision map commutes with isotropic Gaussian convolution: with
`A=(I+R)/2`, `B=(I-R)/2`, the independent common Gaussian parts have
conditional covariance `s(AA^T+BB^T)=sI`, independent of the collision
rotation and core velocities. Uniqueness of the integral equation proves
`S_t(mu_0*G_s)=S_t(mu_0)*G_s`.

Use the PROOF contour/polarization rule with

`c=s`, `h=R^2`, `beta=s-4R^2`, `g=s+4R^2`, `C=(g/beta)^(3/2)`.

The normalized polynomial is now a_q, rather than covariance powers. The
same Poisson expansion proves `E W(v)=f_t(v)/G_g(v)` and `|W|<=C`.

Let `E_0=E|V_0|^2<=R^2`, which may be replaced by the known support bound.
Energy is conserved and the mean is zero. Jensen's inequality gives

`f_t(v)=G_s(v) E exp[v.V_t/s-|V_t|^2/(2s)]
       >=G_s(v) exp[-E_0/(2s)]`.

Hence a strictly positive lower density-ratio envelope is

`ell(v)=exp[-E_0/(2s)] (g/s)^(3/2)
        exp[-|v|^2(1/s-1/g)/2]`.

The same credited Huber/rejection operation is exact in the ideal model.
It charges every rejected proposal and every signed query. Its constants are

`I=exp[E_0/(2s)] [s^2/(g(2s-g))]^(3/2)`,

`E queries <=19 C^2 I`,

`E total degree <=19 C^2 I *6R^2[1/beta+s/(g(2s-g))]`.

The condition `s>4R^2` makes BOTH beta and `2s-g` positive, so all these
costs are finite and time-uniform. Reading t, exact random primitives,
finite output bits, and initial-law acquisition remain charged separately.

## 4. A discriminator against silently staying in the old family

Take equal mass on the six velocities `+/-e_1,+/-e_2,+/-e_3`, R=1, and
s=8. For `n=(1,1,1)/sqrt(3)`, the initial smoothed projection has variance
`25/3` and fourth moment `1873/9`. Thus its fourth cumulant is `-2/9`.
Any centered Gaussian covariance mixture has nonnegative fourth cumulant
in EVERY real direction, by variance-mixture Jensen. This exact source is
therefore outside both N787's radial family and the covariance-mixture
extension in PROOF, not another covariance parameterization.

It is also a strong cost warning: the sufficient resolution standard
deviation exceeds twice the largest core speed, so this theorem alone
does not acquire accurate sharp velocity tails. A model-aware moment or
equilibrium approximation can remain much cheaper for its own declared
task. No practical superiority follows from the new ideal-law receiver.
