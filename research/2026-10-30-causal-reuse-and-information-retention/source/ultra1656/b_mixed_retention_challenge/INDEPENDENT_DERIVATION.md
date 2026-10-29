# Independent mixed-retention reconstruction

Derived from the supplied claim before the producer's full proof existed on
disk. This is an analytic reconstruction, not yet a whole-file intake.

## Exact mathematical claim

Take `n>=2` density matrices `tau_i` on a finite output space. Restrict the
output to `S=supp(sum_i tau_i)`. Within S define

`P_i=projector ker(sum_(j!=i) tau_j)`, `r_i=Tr tau_i P_i`, `r=min_i r_i`.

The proposed complete conditional minimum retention is r. In particular,
for every finite reference and every cq state pair with the relevant
relative entropies finite,

`D(T rho||T sigma)-D(rho_R||sigma_R)
 >= r [D(rho||sigma)-D(rho_R||sigma_R)]`.               (A)

For r>0 its reverse coefficient is exactly1/r; for r=0 no finite reverse
coefficient works. The same r is the minimum retention without subtraction
and on the equal-reference restriction. Sharpness needs no reference.

The requirement n>=2 is necessary for the sharp *conditional* coefficient
statement: at n=1 both conditional quantities vanish identically. This
does not affect ordinary all-D retention, where the singleton channel is
the identity on the reference and has coefficient1.

## 1. The Hilbert--Schmidt extraction is exact but is not a POVM

For r_i>0 set `E_i=P_i/r_i` and define the linear map from output HS space
to C^n by `(T X)_i=Tr E_i X`. With the complex Hilbert--Schmidt product,

`T* z=sum_i z_i E_i`, `T(tau_j)=e_j`.

There is no extra conjugate in the first formula: E_i is Hermitian and
the inner product is conjugate-linear in its first argument. If k!=j,
both `E_k tau_j=0` and `tau_j E_k=0`. Hence

`(T L_tau_j T*)_(kl)=Tr E_k tau_j E_l
                   =delta_kj delta_lj/r_j`,
`(T R_tau_j T*)_(kl)=Tr E_k E_l tau_j
                   =delta_kj delta_lj/r_j`.           (B)

For k=l=j the equality uses P_j^2=P_j and cyclicity, not commutativity
of P_j with tau_j. For every other pair, one of the annihilation
identities kills the term. Thus all complex cross terms are paid.

For arbitrary positive reference-HS operators Q_i^L,Q_i^R, let

`W=sum_i [L_tau_i tensor Q_i^L + R_tau_i tensor Q_i^R]`,
`Q_i=Q_i^L+Q_i^R`, `y=sum_i tau_i tensor u_i`.

Then (B) implies

`(T tensor I) W(T* tensor I)=diag(Q_i/r_i)`,
`(T tensor I)y=(u_i)_i`.

For W>0, the elementary inverse-form projection inequality gives

`<y,W^-1 y> >= sum_i r_i <u_i,Q_i^-1 u_i>`.            (C)

One self-contained proof is to subtract the right side: it equals
`||W^-1/2 y-W^1/2 T*(TWT*)^-1 Ty||^2`.
The same statement on finite inverse-form domains follows by adding a
positive regulator. For physical faithful blocks below, W is already
positive on the restricted S output, so no boundary inverse is needed.

The extraction is not asserted to be trace-preserving or even a
measurement: the E_i need not sum below identity. Thus (C) is an
information inequality, not a simultaneous label-recovery probability.

## 2. Full unequal-reference modular gauge

Let the faithful cq baseline be `diag(A_i)` with A_i>0, and let H_i be
Hermitian tangent blocks. For each v in[0,1], on the reference HS space put

`Q_i=(1-v)L_Ai+v R_Ai`, `Q=sum_i Q_i`,
`h=sum_i H_i`, `z=Q^-1 h`, `u_i=H_i-Q_i z`.

Then `sum_i u_i=0`, and completing the square gives EXACTLY

`sum_i <H_i,Q_i^-1 H_i>-<h,Q^-1 h>
    =sum_i <u_i,Q_i^-1 u_i>`.                         (D)

On output HS tensor reference HS use

`W=(1-v)L_(sum tau_i tensor A_i)+v R_(sum tau_i tensor A_i)`,
`Y=sum_i tau_i tensor H_i`, `U=sum_i tau_i tensor u_i`.

Here `W(I_S tensor z)=sum_i tau_i tensor Q_i z`. The cross term in
the output completion vanishes because Tr tau_i=1 and sum_i u_i=0.
The constant term is <h,Q^-1 h>, again exactly. Therefore

`<Y,W^-1Y>-<h,Q^-1h>=<U,W^-1U>`.

Applying (C), then r_i>=r, proves the conditional inequality at every
modular parameter v. Integration of

`Dlog(A)=integral_0^1 [(1-v)L_A+vR_A]^-1 dv`

proves the conditional BKM inequality. Integrate that Hessian along the
state line sigma+t(rho-sigma), with weight1-t, to obtain (A). The
reference entropy is the Hessian of the SAME reference state line, so
this argument never imports an equal-reference/classical-output theorem.

All these HS spaces are complex. The normalizing z may be non-Hermitian
at v!=1/2; it is used only inside a complex positive quadratic form.
There is no requirement that the intermediate u_i represent a physical
Hermitian tangent. The actual H_i do represent that tangent; C permits
arbitrary complex u_i, which is exactly what closes the gauge.

Finite defined boundary differences follow by common faithful
regularization. Each finite D converges individually by joint convexity
and lower semicontinuity. Undefined infinity-minus-infinity is excluded.

## 3. Endpoint sharpness, including noncommuting mixed outputs

Fix label i. Let `B=sum_(j!=i) w_j tau_j`, where all w_j>0 and sum w_j=1,
and take the scalar input hypotheses `p=e_i`,
`q_e=e e_i+(1-e)sum_(j!=i)w_j e_j`. The input divergence is log(1/e).
The output second state is `B_e=(1-e)B+e tau_i`.

In the restricted total output S, split off ker B. Let
`a=lambda_min(B+tau_i)>0` and let b>0 be the least positive eigenvalue
of B. For e<=1/2, `B_e>=e(B+tau_i)>=e a I`. On ker B, its Rayleigh
quotient is at most `e||tau_i||<=e`. The min--max principle thus traps
each of the dim(ker B) small eigenvalues between e a and e; the other
eigenvalues stay at least b/2. Separated spectral perturbation gives
`||P_small(e)-P_i||=O(e/b)`. Therefore:

* all small nonzero eigenvalues of B_e are e times fixed positive
  quantities, bounded above and below by constants times e;
* their joint spectral projector converges to P_i with error O(e);
* the other eigenvalues stay bounded below.

Thus

`D(tau_i||B_e)=r_i log(1/e)+O(1)`                     (E)

(an O(e log(1/e)) projector correction is bounded). If r_i=0, tau_i is
supported inside supp B and the output divergence stays finite. Hence
the minimum retained fraction is at most every r_i, and is exactly r by
(A). All e>0 divergences here are finite. Perturbing p into the strict
simplex interior at each fixed e preserves the same limiting supremum.

## 4. Exact acquisition versus fragile physical admission

For exactly supplied rational complex Hermitian preparations, each P_i
and r_i is rational and can be computed without eigenvalue/logarithm
oracles. Obtain a rational full-column-rank basis Z_i of the kernel of
`sum_(j!=i)tau_j` by Gaussian elimination, then

`P_i=Z_i(Z_i*Z_i)^-1 Z_i*`, `r_i=Tr tau_i P_i`.

All Gaussian elimination, inversion and exact comparison steps have
polynomial rational bit cost in the explicit matrix input size. Zero
kernel gives P_i=0 and r_i=0. A producer routine must check Hermiticity,
normalization and positive semidefiniteness or declare those as input
promises; it cannot infer them from decimal tolerances.

This is not a robust finite-precision physical inverse. For n>=2, replace
each preparation by `(1-delta)tau_i+delta I/d` for ANY delta>0. Every
preparation is faithful, so P_i=0 for all i and the universal reverse
coefficient is infinite. Arbitrarily small unrestricted channel error
therefore changes a finite coefficient to infinity. Exact support
structure is a real admission gate. Bounded-away-from-boundary priors
would be a different problem, not the theorem being challenged.

When all r_i>0, one can choose a vector from each private functional
space that separates its label. This implies n<=d; in fact
rank(tau_i)<=d-n+1. Consequently the finite-coefficient case has
substantial rank-deficient geometry, already familiar from unambiguous
discrimination. It is not a generic full-rank cq channel property.

## 5. Optional structural consequence: product sources

For product preparations indexed by(i,j), the span of all OTHER labels is

`[span_(k!=i)supp(tau_k)] tensor S_B
 +S_A tensor [span_(l!=j)supp(omega_l)]`.

Its orthogonal complement is the tensor product of the two private
subspaces. Hence `r_(i,j)=r_i r_j` and the minimum retention is exactly
multiplicative for product cq sources. This uses no new matrix/source
execution. It also warns against treating a constant one-copy retention
as a size-independent retention over a full exponentially growing
product alphabet.

## 6. Literal finite Choi operation, with no optimizer

The projection proof can be exported as an explicit pencil certificate.
Write the two-family source pencil as

`A_tau=diag(Q_i^L,Q_i^R) direct_sum [[W_tau,b_tau(U)],[b_tau(U)*,I]]`

and the identity-target pencil as

`B_id,c=[[diag(Q_i^L+Q_i^R),U],[U*,cI]]`.

Its source order is e=2n+d^2+1, target order f=n+1. Let c=1/r and put
the constant e-by-f arrow Z into the source's lower block: its
HS-to-target-label block is T*, its source-bottom to target-bottom
entry is c, and all other entries are zero. The CP congruence
`Z* A_tau Z/c` contributes

`[[diag(Q_i/(c r_i)),U],[U*,cI]]`.

For each i and BOTH source effect families, add a rank-one Kraus fill
from that source-effect row to target coordinate i, with squared
coefficient `1-1/(c r_i)>=0`. The sum is EXACTLY B_id,c, without a PSD
remainder. Although a Kraus display uses square roots, its Choi matrix
is a rational PSD sum. Under source-first indices(a,p) with
`C_(a,p),(b,q)=[Phi(E_ab)]_(p,q)`, it is

`vec(conjugate Z)vec(conjugate Z)*/c
 +sum_i,family (1-1/(c r_i)) v_i v_i*`.

Here vectorization means the stated source-first ordering, and the fill
vectors are the relevant real coordinate vectors. The conjugate is
necessary: Phi(A)=Z* A Z/c gives Choi entries
`conjugate(Z_ap) Z_bq/c`. Writing ZZ* as if the arrow Z were already a
Choi vector has the wrong dimension; omitting conjugation would silently
rely on real data. This correction was sent to both producers before
whole-package acceptance.

All its entries are rational complex numbers when the input tau_i are;
this is a literal finite algebraic output of kernel elimination. The
CP map here acts on pencil coefficient matrices, not on the original
physical output states. It is not required to preserve trace, so it
does not contradict the POVM/UDM comparison.
