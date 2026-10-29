# The positive consumer covers arbitrary finite velocity resolution, with overflow

The three radial cells are an execution case, not the full admitted output
class. This construction supplies the Gaussian masses/conditional access in
UNIFORM_QUERY_PROOF Section7 for ANY finite Cartesian grid in[-4,4]^3, plus
ONE overflow label. No additional kinetic model or stochastic sweep is used.

## 1. Positivity for every resolution

Let N>=1 be a supplied integer and split each axis[-4,4] into N equal bins.
There are N^3 interior cells plus overflow. The source/model remains radial;
the observed cells need not be radial because the density query depends on
the sampled point only through its radius.

On the cube, |v|^2<=48 and

    M(v)/M(v)^beta >=(2pi)^(-3/8)exp(-6)>D=1/3200.

Thus EVERY positive-volume subcell satisfies A_i>D B_i independently of its
width. This is not a grid finite-test argument. The overflow masses are

    A_out=1-erf(4/sqrt2)^3,
    B_out=Z_beta[1-erf(4sqrt(beta/2))^3].

Their strict A_out>D B_out is independently outward-certified. Hence the
exact positive completion applies at arbitrary FINITE N. It does not assign
the same claim to an unbounded countable grid or to continuous coordinates.

## 2. No N^3 table or target-probability oracle

Sample a proposal point Y from the KNOWN mixture density

    q(Y)=[M(Y)+D M(Y)^beta]/[1+D Z_beta],

and map it to the grid/overflow label i. That label automatically has
proposal weight (A_i+D B_i)/(1+D Z_beta). Compute only its Gaussian masses:
for an interior box, each A_i is a product of three ordinary normal-CDF
differences, and B_i is Z_beta times the corresponding beta-Gaussian product.
Their inputs are the supplied grid endpoints. Overflow uses the two displayed
constants. No dynamic f_t cell probability is supplied or estimated in a table.

Independently draw W from M^beta conditional on i; query H_t(|W|), then
accept i with the rule in UNIFORM_QUERY_PROOF. Y itself is NOT a physical
velocity output: its conditional distribution is the proposal, not f_t.
Only the label/declared quantized observation is exact.

## 3. Conditional sampling and complete resolution cost

Inside a box, sample each coordinate by uniform proposal on its interval
and accept exp[-beta(x^2-m^2)/2], where m is the interval point of smallest
absolute value. The target is the exact truncated beta Gaussian. Every
acceptance is at least exp(-6), since |x|<=4. Thus expected coordinate
proposals are at most exp(6), independently of N. Three coordinates cost
at most3exp(6) such proposals; this conservative bound is not a practical
timing estimate.

For overflow, reject ordinary beta Gaussians until outside the cube. This
is charged, not assumed constant conditionally. Let p_beta denote that tail
probability. The colder M has tail probability A_out<=p_beta. Weighted by
the proposal chance of overflow, its expected Gaussian draws are

    (A_out+D Z_beta p_beta)/[(1+D Z_beta)p_beta] <=1.

Thus total average conditional sampling has a finite resolution-independent
ideal-primitive bound, without enumerating the cells. The query's uniform
time bound and expected1+D Z_beta proposals remain in force.

Resolution is NOT free: grid encoding/index/output use O(log N) bits, endpoint
arithmetic and small Gaussian-CDF differences require the requested precision,
and actual fair-bit/validated arithmetic implementation is unacquired here.
There is no claim of constant BIT cost in N. Likewise detector calibration,
source identification and physical symmetry/moment qualification remain
separate. This is an ideal-real exact finite-observation operation, not a
new apparatus or a continuous full-law sampler.
