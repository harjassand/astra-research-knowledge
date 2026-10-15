# Independent analytic audit of the slow-fast and target-logspiral exclusions

15 October 2026. Same-team model-assisted review, not external correctness
review or formal verification. Historical novelty remains **UNKNOWN**.

**Decision:** the two new analytic exclusions have a sound proof under the
same inherited sharp-negative heat certificate and rank-one Bregman lemma
used by N876. I found no missing large-frequency cancellation, derivative
normalization loss, radial heat flux, or full-affine Schur term. They may
be retained as internally supported, narrowly quantified deductions.
They do **not** prove the uniform all-affine fourth-power margin.

The reviewed producer report is
`workers/fy_margin_counterconstruction/REPORT.md` in the current research
directory. The pinned read-only W revision is
`b32943eeb62d0d79929a9e572a344219a785ebf9`.
Only this new `fy_logspiral_audit` directory was written. The completed
cone/gluing packet and the producer report were left unchanged. No
candidate grid, numerical minimization, or producer scientific script was
rerun. Sixteen targeted exact algebra checks are saved separately.

## 1. Fixed-r hypotheses and the inherited inputs

Throughout fix a real parameter r<-2 and put

    alpha=3r/[8(r+2)]>0, beta=r(r-1)/6>0, C=r(r+2)/3>0,
    J(A)=alpha*((a-d)^2+(b+c)^2)^2+beta*(a^2+c^2)^2
         +(ad-bc)^2+r*(a^2+c^2)*(ad-bc).

The used inherited statements are:

- J is rank-one convex and has the sharp-negative corrected scalar heat
  identity with fixed positive diffusion d1 partial_xx+d2 partial_yy.
- Its nonnegative corrected density has the eight outer-product kernel
  implications from N876, evaluated on the full gradient.
- Those implications give zero-density rigidity for positive-time analytic
  heat fields with sublinear growth.
- On every real rank-one line,
  J(B+R)-J(B)-DJ(B):R >= J(R)/3 >= alpha |R|^4/3.

I read the old N876 `PROOFS.md`, its full additive clarification, and the
previous analytic audit. The target-logspiral extension does not alter
the universal certificate or pretend to verify that inherited analytic
input anew. It uses the same exact density identity for a different
class of compatible initial maps.

## 2. Slow-fast compatibility and the complete affine optimization

For a fixed nontrivial real smooth doubly periodic f(X,y) with zero y
mean, the displayed phi has exactly the gradient

    q_epsilon=[[epsilon P,S],[epsilon^2 Q,-(r+1)epsilon P]],
    P=f_X, S=f_y, Q=-(r+1) partial_XX partial_y^(-1)f.

The zero y mean makes the inverse derivative periodic and unambiguous
after choosing zero mean. Integration by parts gives

    <SQ>=-(r+1)<P^2>,

so the determinant has zero period average, as compatibility requires.
No arbitrary matrix-valued probability law is substituted for this field.

For q=[[p,b],[w,z]] and e=(r+1)p+z, the exact quadratic and cubic Taylor
coefficients at I are respectively

    e^2+C w^2+(r+2)det q,
    2p e^2+[-2bw-(r+2)p^2+r w^2]e-C p(p^2+w^2).

These identities, including the absence of a p b^2 term and the coefficient
-(r+2) of p^2 e, were independently regenerated. Averaging q_epsilon gives
M(I,I)=C epsilon^4<Q^2> and the stated cubic coefficient L(I).

Write B=tI+V with V perpendicular to I. The limiting quadratic on V is

    M_0(B,B)=<S^2>[2alpha(a-d)^2+6alpha(b+c)^2+c^2],

which is positive definite on V because alpha>0 and <S^2>>0. The last
inequality holds for every nontrivial zero-y-mean profile. The limiting
diagonal/off-diagonal split is block diagonal. Smooth polynomial dependence
in epsilon therefore gives a uniformly invertible V block for this fixed f.

The full mixed orders in the report are correct. In particular the exact
averaged cross terms are

    M(I,diag(1,-1))=-r epsilon^2<P^2>
                       +r(r-1)epsilon^4<Q^2>/3,
    M(I,e12)=0,
    M(I,e21)=-C epsilon^3<PQ>.

The diagonal component of M_VV^(-1)L_V is O(epsilon), and the off-diagonal
component is O(1). Hence the residual linear coefficient after optimizing
V remains O(epsilon^3), rather than O(epsilon^2) or O(epsilon).

### The potentially delicate Schur lower bound is valid

If P is nonzero, fixed f has a nonzero Fourier coefficient f_(k,l) with
k!=0. Zero y mean forces l!=0. Its gradient amplitude is a common complex
scalar times the real rank-one matrix

    eta_epsilon tensor xi_epsilon,
    eta_epsilon=(1,-(r+1)epsilon k/l),
    xi_epsilon=(epsilon k,l).

Parseval expresses M as a sum of PSD background acoustic matrices. One
such fixed mode is already enough. Target normalization is an orthogonal
change of the background variables, and contributes the positive factor
|eta_epsilon|^8 to the determinant. The independently checked normalized
acoustic determinant is

    det M_r(p,q)=9 p^4 q^4 r^4/16.

Consequently that mode has determinant bounded below by a fixed positive
multiple of epsilon^4 and bounded trace. For four nonnegative eigenvalues,
lambda_min >= det/(trace)^3. The complete M therefore dominates a fixed
positive multiple of epsilon^4 times the identity. Minimizing its quadratic
over V with the I coefficient fixed gives the same epsilon^4 lower bound
for the I Schur complement. Thus no unexamined higher-order cancellation
of that Schur complement remains.

The final I optimization subtracts O(epsilon^6)/Omega(epsilon^4), which is
O(epsilon^2). It cannot affect the leading fourth-power ratio. At epsilon=0,
the remaining linear term is 4alpha<S^3>(b+c). Optimizing the positive
limiting V quadratic gives c=0, a-d=0,
b+c=-<S^3>/(3<S^2>), and hence exactly

    lim_(epsilon->0) inf_B Gap_B/<|q_epsilon|^4>
      =alpha[1-2<S^3>^2/(3<S^2><S^4>)] >=alpha/3.

This includes optimization over an unbounded affine matrix. If P=0, the
gradient is rank-one valued and the inherited pointwise lemma gives the
same positive lower exclusion directly.

The fixed-profile qualifier is indispensable. A changing f_epsilon may
have its selected Fourier weight and Schur constant collapse. Neither this
argument nor the recorded finite diagnostics gives uniform control over
changing-profile slow-fast sequences.

## 3. Critical target-logspiral heat strictness

For any fixed real omega and smooth periodic h, let

    phi(rho,theta)=rho^(1/2) R_(omega log rho) h(theta),
    A_(h,omega)=[(.5I+omega J0)h | h']R_theta^T.

The polar gradient formula is exact. It has the target rotation in front:
Dphi=rho^(-1/2)R_(omega log rho)A_(h,omega). Left target invariance of J
removes this rotation from its energy. The norm identity is

    |A_(h,omega)|^2=(1/4+omega^2)|h|^2+|h'|^2.

Scalar constant-coefficient heat commutes with every constant target
rotation. Combining heat dilation with the twisted homogeneity gives

    psi_t(x)=t^(1/4)R_((omega/2)log t)psi_1(x/sqrt t).

There is no omitted rotation derivative in the energy: J is left invariant,
so the exact truncated identity is still E_R(t)=E_(R/sqrt t)(1).

For each fixed smooth h and fixed omega, all m-th initial derivatives on
far annuli are O_(h,omega)(R^(1/2-m)). The Gaussian near-field expansion,
with its vanishing first moment and exponentially small far tail, gives

    Dpsi_1(R e_r)=R^(-1/2)R_(omega log R)
                     [A_(h,omega)+O_(h,omega)(R^-2)],
    D^2psi_1=O_(h,omega)(R^-3/2).

Angular/radial derivatives of the logarithmic target rotation introduce
only fixed-omega constants and the expected powers of R^-1. The heat flux
is bounded by |Dpsi|^3 |D^2psi|=O(R^-3). The inherited cubic primitive
pullback has the same bound. Their circle integrals are O(R^-2), tending
to zero. The nonnegative bulk density is O(R^-4), integrable at infinity,
and smooth at the origin at positive time. Therefore

    I_omega(h)=2t integral D_r(Dpsi_t,D^2psi_t).

The sign and factor 2t follow from differentiating the truncated scaling;
the full fourth-order energy is never claimed finite. A zero angular
energy forces analytic zero-density rigidity. The heat field has
O(1+|x|^(1/2)) growth, hence zero gradient. Local Fourier inversion for the
nonvanishing Gaussian multiplier gives zero initial gradient. Twisted
degree-half homogeneity then forces phi=0 and h=0.

For rough W1,4 angular profiles, strong angular approximation gives a
common sublinear growth bound and positive-time heat convergence on
compact sets. Fatou gives the needed one-sided density inequality, exactly
as in N876. An unjustified equality for rough data is unnecessary.

## 4. Bounded frequencies and derivative-norm loss

On |omega|<=Omega0, normalization N_omega(h)=1 bounds h in W1,4 uniformly.
For a hypothetical zero-energy sequence, pass to omega_n->omega, uniform
h_n->h, and weak L4 convergence of h_n'. The first column then converges
uniformly as well. Rank-one convexity makes the integrand convex in its
second column, so weak lower semicontinuity yields I_omega(h)<=0.
The strictness argument above gives h=0.

Uniform h_n->0 is not by itself enough: the derivative norm could be lost.
The rank-one Bregman bound closes precisely that gap. With first-column
base B_n and second-column increment R_n,

    I_(omega_n)(h_n) >= (alpha/3) integral |h_n'|^4
                        -C_(r,Omega0)||h_n||_infinity^3 integral |h_n'|.

The base is rank one and has nonnegative J, and its derivative is bounded
by a cubic norm. The error tends to zero, forcing strong derivative
convergence to zero and contradicting normalization. Thus each bounded
frequency interval has a positive margin. No minimizer or computable
lower enclosure is claimed.

## 5. High absolute frequency: the calibration and all constants

Set Omega=|omega|, sigma=sign omega, y=Omega theta and
g(y)=Omega h(y/Omega). Then g_y=h'(theta), exactly. The leading field is

    A0=[sigma J0 g | g_y]R_theta^T,

and the perturbation in the first column is g/(2Omega). Both integrals
acquire the same factor 1/Omega under this change of variable. The new
period is 2pi Omega; no integer-frequency assumption is needed.

At fixed theta the rank-one-column energy is

    P_theta(nu)=alpha(1+nu^2)^2
                  +beta(cos theta-nu sin theta)^4.

Its second derivative is at least 4alpha, so its unique minimizer is smooth.
Put q=cos theta-nu sin theta. At g=a e1, make the radial second-column
variation v=a(t e1+sigma nu e2). Its determinant is -sigma a^2 t, and
d/dt of its energy at zero is precisely

    a^4 mu_sigma,  mu_sigma=sigma[4alpha(1+nu^2)-r q^2].

The parallel variation vanishes by P minimization. Left target invariance
then identifies the full second-column derivative at arbitrary g with
mu_sigma |g|^2 g. Applying the inherited rank-one Bregman bound in that
column proves the claimed calibration pointwise for every g,v.

For v=g_y, its apparently dangerous term has the exact integral

    integral mu_sigma(theta)|g|^2 g.g_y dy
       =-(1/(4Omega)) integral mu_sigma'(theta)|g|^4 dy.

The endpoint term vanishes on the actual period 2pi Omega. This identity
also holds for W1,4 profiles by the one-dimensional chain rule; no smooth
profile or frequency cutoff is hidden.

The stated derivative bounds check. Comparing the minimizer to nu=0 gives
|nu|<=Lnu. Implicit differentiation has denominator

    alpha(1+3nu^2)+3beta sin^2(theta) q^2 >=alpha

and numerator

    beta q^2[cos^2(theta)-3sin^2(theta)-4nu sin(theta)cos(theta)].

The last bracket has absolute value at most 3+2Lnu, proving exactly the
reported Vnu bound. Differentiating mu gives the reported M1. Therefore
the calibrated lower bound with coefficients alpha/2 and alpha/3 is valid
once Omega>=M1/(2alpha).

Writing w=g_y-nu sigma J0 g gives the stated norm comparison

    |A0|^4 <=(2+16Lnu^4)|g|^4+16|w|^4,

and hence integral J(A0)>=gamma0 integral |A0|^4. Separately,

    |DJ(A)| <=(16alpha+4beta+1+2|r|)|A|^3=Cgrad|A|^3.

The four contributions are bounded respectively by 16alpha, 4beta, 1,
and 2|r| times |A|^3. For Omega>=1 the first-column perturbation is at
most |A0|/(2Omega). The mean-value theorem gives precisely the loss
27Cgrad/(16Omega) times integral |A0|^4. The reported frequency threshold
makes this at most gamma0/2. Finally
|A_actual|^4<=(3/2)^4|A0|^4 yields the claimed positive ratio 8gamma0/81.

Thus the high-frequency estimate is uniform over all angular profiles.
Together with the compact-frequency argument it proves the stated
positive all-omega margin for each fixed r<-2. The compact-frequency
portion remains nonexplicit, and no uniformity in r is established.

## 6. Annular normalization and the exact boundary of the result

A cutoff chi(log rho) adds to the leading polar matrix only
chi_s h in its radial column. The same norm identity bounds
|h|^4<=16|A_(h,omega)|^4, uniformly in omega. Fixed logarithmic-width inner
and outer transitions therefore cost O_r(N_omega(h)), uniformly in omega,
h, and annulus length T. This verifies the normalized annular consequence
even when omega and h vary together with T.

For fixed B and N_omega(h)=1, Holder on the circle and radial integrability
of rho^(-1/2) in powers 2 and 3 give uniform L2/L3 gradient integrals.
The linear affine term integrates to zero for the cutoff map. Quadratic
and cubic cross terms are O_(r,B)(1), while the quartic norm is T+O(1).
This validates the fixed-B normalized extension. Shrinking amplitudes
replace B by B/a_T; growing effective backgrounds remain outside its scope.

The still-uncontrolled classes include changing-profile slow-fast sequences,
general log-radial changes of angular shape, nonconstant target rotation
rates, interacting multiscale concentration, and increasing-depth laminates.
The fixed-depth rank-one martingale estimate deteriorates as n^-3 and
does not supply a depth-independent margin. No sharp-J storage transfer or
uniform all-affine coercivity conclusion follows from this audit.

`verify_targeted.py` reports 16 exact algebra groups PASS, covering the
contact Taylor coefficients, averaged slow-fast blocks and limiting
objective, full acoustic determinant, both calibration signs, and the
implicit minimizer derivative. These checks support the analytic reasoning;
they do not mechanically prove the heat identity, compactness, boundary
limits, or historical priority.
