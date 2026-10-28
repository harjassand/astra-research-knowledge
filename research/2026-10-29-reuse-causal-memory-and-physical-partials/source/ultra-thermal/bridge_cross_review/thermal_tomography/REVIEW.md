# Whole review: finite-temperature diagonal-quartic tomography

**ACCEPTED at the stated mathematical, known-model computational and
conditional statistical scopes.** I whole-read the final PROOF.txt,
qualify_frame.py / FRAME.json / SOURCES.json, compose_global.py /
GLOBAL_INVERSE.json and compile_forward.py / FORWARD.json. I
independently derived the finite-temperature constants, chain rank,
whole-box Jacobian and inexact-iteration estimates and finite Wick
forward error. No producer, resolvent, Wick-state, frame, model,
sampling or parameter-grid execution was repeated.

The positive construction is stronger than an affine rank result:
at a qualified positive temperature the ACTUAL variance map is
globally injective on the entire coefficient box, and its forward
interface has been acquired by a finite Gaussian-moment compiler.
Actual variance data and inverse iterations have not been executed.
Known physical K, uniform shifts, mechanical bath/metric, preparation,
exposure and calibration remain explicit admission inputs.

## 1. Finite-temperature affine bound

After x=sqrt(theta) z, the Gaussian covariance is R=(K+lambda I)^-1
and W=sum_i alpha_i z_i^4/4>=0. With F=z_p^2,

    C=Cov_0(F,W)=3 sum_i alpha_i R_ii R_pi^2,
    mu<=3nA/(4kappa^2),
    m2<=105 A^2 n^2/(16kappa^4),
    mF2<=945 A^2 n^2/(16kappa^5).                       (1)

The last two inequalities follow directly from Gaussian Holder at
degrees 8 and 10, so they hold even when covariance entries have
different signs. Wick's covariance is nonnegative because its
cross-port entry is squared. C<=4b mu is correct.

For Z=1-theta mu+rZ and N=b-theta E_0(FW)+rN, the identity

    N-(b-theta C)Z
       =rN-theta^2 C mu-(b-theta C)rZ                   (2)

has the correct signs. Under theta mu<=1/2, dividing by Z>=1/2
and using |b-theta C|<=3b gives the stated bound
theta^2[mF2+3b m2+8b mu^2]. Its coefficient is
(945+315+72)/16=333/4. Multiplying by theta to return to the physical
variance and dividing by 3theta^2 gives exactly

    B(theta)=(111/4) A^2 n^2 theta/kappa^5.              (3)

The condition theta<=2kappa^2/(3nA) pays the normalizer uniformly for
ALL alpha in [0,A]^n. A=0 is trivial. This uses a finite remainder
for a negative exponential, not an infinite quartic perturbation
series or an observation of a temperature derivative.

## 2. Rank and what the count means

For a known irreducible tridiagonal chain measured at an endpoint,
the continuant inverse formulas are correct. In zero-based index i,
the numerator of f_i=R_ii R_pi^2 is

    (product_(j<i)b_j^2) L_i T_(i+1)^3,

of degree i+3(n-i-1)=3n-3-2i and nonzero leading coefficient. The
distinct degrees make the n numerator polynomials independent.
D(lambda)>0 at positive shifts. Thus a combination vanishing at
3n-2 distinct positive shifts would have too many roots unless it
were zero, proving the rank theorem without a genericity assumption.

The 3n-2 shifts are CANDIDATES computed from known K. Select n
independent rows before physical measurement. The actual scalar
summary count is n finite-temperature variances at these selected
shifts, with many reads per summary. The theorem does not require
physically measuring all candidate shifts, and it does not claim
arbitrary n chosen shifts suffice.

This is not a theorem for every cyclic SPD matrix. The retained
n4 star is not treated as a chain: its 10-row frame is separately
qualified exactly, and the first four rows are invertible. General
known-SPD inputs need their own rank and conditioning qualification.

## 3. Whole-box exact Jacobian and global inverse

For the actual variance transformation y=(theta b-v)/(3theta^2),

    partial y_j/partial alpha_i
       =Cov_(j,alpha)(z_p^2,z_i^4)/12.                  (4)

The theta factors cancel as written. One-sided boundary derivatives
are sufficient; integrating along any segment inside the box never
requires a Gibbs law with negative quartic coefficients.

For nonnegative H, Z>=1/2 yields

    |E_alpha H-E_0 H|
       <=2theta[E_0(HW)+E_0 H*mu].                     (5)

Applying Gaussian Holder to H=F z_i^4, F and z_i^4 gives respectively
495, 9 and 57 times A n theta / kappa^(5,3,4). The product-of-means
difference adds 9*6+57=111 in units A n theta/kappa^5. Total covariance
error is therefore 606 A n theta/kappa^5; dividing by 12 gives 101/2.
Summing over the n derivative columns AFTER multiplication by L
gives exactly root's infinity-operator bound q.

Consequently G=L y obeys, globally on the convex box,

    ||G(a)-G(b)-(a-b)||infinity<=q||a-b||infinity.       (6)

If q<1 this proves exact finite-temperature injectivity and inverse
Lipschitz constant 1/(1-q) in transformed-data units. It is not
merely an inverse-function argument at alpha=0.

There is a useful general consistency check. Put
M=max_i sum_j |L_ij|/kappa_j^5. The affine bias coefficient is
beta=(111/4) A^2 n^2 M. If theta<=delta/(2beta), as in the saved
frame, then automatically

    q<=(101/111)*(delta/A).                            (7)

For the actual selected temperature the value is exactly 202/8325,
matching GLOBAL_INVERSE.json. Thus the legacy conservative bias
temperature also supplies a nonvacuous global-injectivity margin.

Clipping is nonexpansive in infinity norm. The exact noisy map
T(a)=clip[a-G(a)+L yhat] contracts by q on the box and has a unique
fixed point. If the transformed measurement error is at most s and
the implemented forward error is uniformly at most e, finite iterates
obey the valid conservative bound

    ||a_k-alpha_true||infinity
       <=A q^k+(s+e)/(1-q).                            (8)

An approximate forward map need not itself be q-contractive solely
from a uniform error bound. That stronger claim is unnecessary:
comparison to the exact map proves (8) and a limsup-radius bound.
No convergence/unique fixed point of the approximate map is inferred.

## 4. Forward interface is actually paid

compile_forward.py implements the exact Gaussian integration-by-parts
recursion: remove one occurrence of variable i and pair it with each
remaining j with multiplicity e_j R_ij. Total degree drops by two,
so the recursion is finite. Repeated i=j=p indices are accumulated
correctly. It compiles mu,n1,m2,n2 for EVERY candidate alpha, not a
truth-alpha table. Symmetry checks and the Gaussian covariance identity
connect the linear coefficients to the qualified frame.

The compiled moments have degree at most 10. The analytic remainder
also uses the bounded 12th and 14th Gaussian moments, with constants
11!!=10395 and 13!!=135135; those are bounds, not memoized coefficient
moments. The distinction in FORWARD's degree field is appropriate.

The finite alternating Taylor bounds give
0<=Z2-Z<=theta^3 m3/6 and 0<=N2-N<=theta^3 n3/6. Both denominators
are at least 1/2. Writing the ratio error with N2 in its second term,

    |N2/Z2-N/Z|<=2|N2-N|+4Nmax|Z2-Z|,

and dividing by 3theta proves exactly

    |y2-y|<=theta^2[n3+2Nmax*m3]/9.                    (9)

Nmax is valid because the omitted -theta n1 is nonpositive.
Nonnegativity of N2 follows from 1-t+t^2/2>=e^-t>=0. There is no
positive quartic mgf, global high-dimensional cubature or uncomputed
normalizer in this receiver. The evaluator is a finite rational
expression of acquired coefficient polynomials. Actual future
arithmetic must be exact or outward qualified, as stated; the model
remainder does not automatically cover arbitrary floating evaluation.

The saved coefficient acquisition uses four additional known-K
resolvents, 348 memoized Wick states and .0033635 s after imports.
Its uniform transformed error 9.9712517e-11 is below the required
.0048787 tolerance. With the existing statistical allowance, (8)
after two ideal/qualified inexact steps gives radius .0213804851,
below the requested .04. The steps were NOT executed on observed
data. GLOBAL_INVERSE's earlier forward-integral remaining-field is
historical; the subsequent FORWARD packet closes that computational
input at this source and tolerance.

## 5. Code, stationary-read budget and full cost

I checked qualify_frame.py line by line. It uses the recovered K
field, the explicit box A=3/2 and stated accuracy/risk. The source
JSON also contains alpha metadata, but no alpha value enters any
calculation or selection. Thus the scientifically relevant claim is
NO truth-alpha use, not a literal byte-level file-content separation.

The symmetric Gershgorin floor is 1 at this K, giving floors
2,3,4,5 at the four selected shifts. The matrix transpose-rref pivots
are row indices of the original frame. The exact inverse identity,
row norm, weighted bias norm, temperature, noise allowance and error
assembly all have the correct orientations. This is an actual n4
known-K qualifier, not a software API for all SPD matrices; another
SPD matrix can require a sharper acquired curvature floor.

The variance error e=3theta^2*delta/(2||L||infinity) is about
1.35413e-27. The selected theta is about 6.24546e-10. Taking the
average score (Y+eta)^2-sigma^2 is valid because the stipulated
unforced Gibbs law and zero-mean detector are symmetric.
Z>=1/2 gives EY^4<=6theta^2 b^2 and EY^2<=2theta b. Expanding the
detector fourth moment and using the reversible gap proves exactly
root's 6S0^2+12theta^2b^2/(exp(kappa tau)-1) bound. At tau=1/kappa,
18S0^2/Q is safe. The code's factor n/zeta and union bound deliver
all n variance intervals simultaneously with failure at most .05.
Independence between different shifts is not needed for this union
bound; stationarity at each shifted model IS needed.

The sufficient point-read budget is of order 1.3e37 in both displayed
detector plans. It is a CONDITIONAL stationary plan, not reads already
taken, a lower bound, a demonstration of impossibility, an optimal
design or a full-likelihood cost comparison. Settling/preparation,
exposure, detector offsets/variance, temperature, stiffness-shift and
K calibration, bath validity at this theta and native physical time
mapping remain unpaid physical inputs.

The frame qualifier costs .00641475 s, scalar global composition
.000369125 s and forward compiler .0033635 s after imports. The frame
and forward stages perform 10+4 known-K resolvent calculations, not
10 total. All upstream decoded-K acquisition/qualification and source,
proof, import and calibration costs remain separate; .01015 s of new
measured code is not an end-to-end physical tomography cost.

## 6. Useful conditional query and the practical admission gap

If actual justified variance intervals are acquired and the stated
receiver is evaluated, its parameter radius r immediately certifies

    |V_hat(x)-V_true(x)|<=r*sum_i x_i^4/4,
    ||grad V_hat(x)-grad V_true(x)||2<=r*||x||6^3.        (10)

On a Euclidean state ball of radius B these are at most r B^4/4 and
r B^3. This is a usable potential/force query certificate over a whole
state region, conditional on the SAME known K and measured variances;
it is not another actual measurement or a finite-bath mean-field
approximation. With no variance observations, no numerical physical
coefficient/potential certificate has yet been issued.

The small statistical interval exposes a precise calibration debt.
With F, theta and q kept qualified, an additional uniform additive
variance bias e_cal contributes at most
||L||infinity e_cal/[3theta^2(1-q)] to (8). The remaining radius
headroom therefore supplies an explicit admission budget of order
1e-27 in variance units. This is a sufficient budget of this receiver,
not a physical lower bound: common-reference cancellation, warmer
nonlinear fitting or another access might do better. Changes in K,
theta or shifts also change F/q and require their own propagation,
not merely this additive-error substitution.

## 7. Prior and scope boundary

Gaussian Wick moments, finite Taylor remainder, continuants,
interpolation, global near-identity/contraction bounds, FDT and LP
membership inference are ordinary operations. The same-bath active
susceptibility measures v/theta, and a full-data nonlinear likelihood
method receives the same warranted inputs. No comparison against that
stronger statistical method has been executed here.

I read SOURCES.json and the primary
[Imaging with Thermal Noise Induced Currents](https://epubs.siam.org/doi/full/10.1137/23M1571630)
model/introduction. It uses selectively heated electrical noise to
recover conductivity-related power information, with its actual
electrical FDT covariance. That is controlling thermal-imaging prior,
not this uniform mechanical-bath/all-quartic inverse. It cannot
warrant RC noise or the present bath/metric automatically. N1037's
labeled internal-shunt input is also distinct; this is not a new
audit or strengthening of that supplied theorem.

The source pin 2bdc6a88e7ce0966ba259728267c3d318f70e009 is point-in-time
current in root's recorded receipt; this review does not infer its
continuing freshness or a historical absence result. No new fixture,
model/producer run, scalar variance, inverse iteration or physical
action was performed by this review. The finite-temperature global
operation and paid forward polynomial are accepted. Historical
novelty, practical advantage and a physically economical tomography
capability remain unacquired.
