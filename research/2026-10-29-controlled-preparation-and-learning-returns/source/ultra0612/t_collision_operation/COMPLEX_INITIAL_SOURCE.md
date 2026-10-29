# Covariance-scale terminal information without a covariance-mixture oracle

This compatible INPUT operation consumes root's direct-complex construction
in root_complex_collision. Root owns the improved dual/full sampler. The
ACQUISITION and RESOLVED_ACQUISITION runs use the older polarization rule;
no improved performance is inferred from them.

## 1. Exact physical-moment transport

Let mu_0 be centrally symmetric. Supply kappa>0 and an actual routine for
`F_q^0(z)=E(z.V_0)^(2q)/[(2q-1)!! kappa^q]` on complex unit z, returning
the exact value or an unbiased complex sample of modulus<=1. Its work is
charged; a formal moment bound alone is not this acquired routine.

The RAW gain coefficient identity
`binom(2q,2j) d_j d_(q-j)/d_q=binom(q,j)`, d_q=(2q-1)!!,
shows that these normalized actual velocity moments obey precisely the
complex covariance-power hierarchy. Odd terms vanish by central symmetry.
Root's Haar/binomial marked rule is therefore valid, including its
uniform separating probability and singleton covariance compression.
For q=1 the exact continuation is
`exp(-t/2)F_1^0(z)+(1-exp(-t/2))tr(C_0) z^Tz/(3kappa)`.

For declared Gaussian variance s>kappa, the root contour receiver samples
`mu_t*G_s`, equivalently the Maxwell solution from `mu_0*G_s`, with
`beta=s-kappa`, `g=s+kappa`, `C=(g/beta)^(3/2)`.
The conserved energy E_0=tr C_0 and Jensen give
`ell(v)=exp(-E_0/(2s))(g/s)^(3/2)exp[-|v|^2(1/s-1/g)/2]` and
`I=exp(E_0/(2s))[s^2/(g(2s-g))]^(3/2)`.
Thus exact ideal factory work is <=19 C^2 I queries, and 2s-g=beta>0.
Gaussian resolution is part of the target, not free added error.

Bounded symmetric velocities |V_0|<=R supply this interface with kappa=R^2
by the terminal sample `(z.V_0)^(2q)/(d_q R^(2q))`. Consequently root's
operation lowers RESOLVED_INITIAL_DATA's old s>4R^2 requirement to s>R^2.

## 2. A concrete covariance-scale source

Supply real vectors v_1,...,v_J and the generative initial law
`V_0=sum_l epsilon_l v_l`, independent symmetric signs. Acquire
`C_0=sum_l v_l v_l^T` and a warranted C_0<=kappa I bound in O(J) input
work plus a3-by-3 PSD check. This is a supplied model, not a fit theorem.

For complex a_l an elementary even-moment Gaussian comparison gives
`E|sum epsilon_l a_l|^(2q)<=d_q(sum|a_l|^2)^q`.
Proof: expand `|c+a x|^(2q)` as
`(|c|^2+2Re(conj(c)a)x+|a|^2x^2)^q`. After symmetric averaging all
surviving coefficients are nonnegative. Replacing one sign by a standard
real Gaussian increases every even power; repeat for all signs. The
resulting complex Gaussian is a real2D Gaussian. Diagonalize its covariance
and apply convexity of x^q at fixed eigenvalue sum to bound its moment by
d_q times that sum to power q. This proves the stated comparison.

Therefore `|F_q^0(z)|<=(z^*C_0 z/kappa)^q<=1`.
This is ordinary even-integer Khintchine/Gaussian comparison, not a new
Khintchine theorem; established primary prior includes
https://doi.org/10.4064/sm-70-3-231-283 . The elementary proof suffices.

An ACTUAL terminal routine truncates `prod_l cosh(t z.v_l)` at degree2q,
using arrays of length q+1 in t^2, and returns
`(2^q q!/kappa^q)[t^(2q)]prod_l cosh(t z.v_l)`.
Cost is O(Jq^2) complex arithmetic, O(q) memory, and reads all J vectors.
Terminal degrees sum to q, so their total cost within one marked query is
O(Jq^2). All Poisson degree moments under the tilted receiver Gaussian are
finite; expected full-law work is therefore finite uniformly in t. Exact
random/output bits and certified arithmetic remain separately unacquired.

## 3. Discriminating size/control test

The consumer uses64 distinct odd primes p_l above1024 and
`v_l=(floor(p_l/8)/p_l,0,0)`. All2^64 sign velocities are distinct:
multiply an equality by prod p_l and reduce modulo each p_l. A nonzero
sign difference is+/-2; neither2, floor(p_l/8), nor the other primes vanish
modulo p_l, a contradiction. The terminal routine still uses64 vectors.

Here kappa=sum|v_l|^2 is exact and the tight support radius is R=sum|v_l|.
R^2/kappa is near64. The new sufficient resolution s>kappa stays at
covariance scale, whereas the old s>4R^2 gate requires about256 times the
variance. The exact active-direction fourth cumulant is
`-2sum|v_l|^4<0`, unchanged by adding G_s, excluding centered Gaussian
covariance mixtures.

No exponential cost is ascribed to an equally informed ordinary method:
it already samples the factored initial law in O(J), evaluates its
characteristic function in O(J), and may use the same moment polynomial.
The constructed link is compatibility with the bounded all-time nonlinear
collision receiver, not invention of initial-state compression or proof of
practical solver dominance.
