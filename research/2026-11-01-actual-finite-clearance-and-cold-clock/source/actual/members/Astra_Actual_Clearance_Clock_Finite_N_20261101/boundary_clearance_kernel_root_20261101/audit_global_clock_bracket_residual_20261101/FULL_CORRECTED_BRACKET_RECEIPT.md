# Independent receipt: full corrected-clock bracket and jumps

**PASS, no repair**, frozen `FULL_CORRECTED_CLOCK_BRACKET.md`, SHA256
`f64bc7cf924af8f6c4ffd1a58b236763b49c874d9c2ac5cf5be80e95a133edf4`.
The reviewer did not author this construction. Source copies and the exact
full manifest are preserved in `source_snapshot/full`. The main primitive and
shared residual/endpoint extension are separately received in this audit.

## Exact observable, coordinates, and enabled marks

For q=b(L/T,E/T^3)+AE b_l/T^6, differentiation at fixed N=T^5 gives exactly
q_A=e b_l/T^3, q_L=b_l/T+(Ae/T^4)b_ll, and
q_E=b_e/T^3+(A/T^6)(b_l+e b_le). Integration of this full gradient along the
actual straight jump segment is an exact finite-jump identity. Equivalently,
Delta q=Delta b+Delta h*g/T^6+h'*Delta g/T^6 with
Delta h=E Delta A+A Delta E+Delta A Delta E. Both h' and the simultaneous
product are retained. The independent checker verifies all twelve product
identities and a generic second-order derivative jet with independent
coefficients. No derivative sampling is substituted for the analytic proof.

Actual nonnegative endpoint species and their linear interpolation imply
A<=L along every segment. L/N<=1/5000 at the source and |Delta L|<=1 imply
the target/segment bound L'/N<=1/4000. Startup L'=0 is inside the received
small-e rectangle; after startup the full segment lies in the received padded
cone. Consequently the gradient proof is applicable also to the mark that
causes an admission failure.

## Continuous gradient ceilings

For l<=1 on the cone, the squared relative L-correction is at most243/T^4,
using A<=Tl, e^2<=3l and b_ll<=9. The startup rectangle is smaller. For
l>=1 the same squared ratio is at most(75/4)l/T^4<=75/16000. At T>=10000
both are below(7/100)^2, giving |q_L|<=107 sqrt(psi5)/(100T).

For the E correction and l<=1, the relative bound is27/T^2; for l>=1 it is
at most3sqrt(l)/T^2<=3/sqrt4000. Both are below3/10 for T>=10. With the
received |b_e| ceiling this gives |q_E|<=7sqrt(psi4)/T^3. The A derivative is
exactly bounded by e sqrt(psi5)/T^3. These arguments cover both pieces of D;
no A/L cap or positive-E entrance is silently used.

The continuous source-weight comparisons e^2 psi5<=24phi and psi4<=8phi
follow by multiplying by(1+e)^2<=2+6l and splitting at l=1. The rectangle is
smaller. Across a full jump, psi5(l')<=R_T psi5(l) and
phi(e')<=(1000/999)^2 phi(e). These are source-relative and remain valid near
e=0 and across l=0,1. Exact rational comparisons therefore yield squared
gradient coefficients23/20 for L motion,25 for A motion, and400 for E motion,
with the advertised T denominators.

## Complete bracket, source charge, and jumps

Use the exact integrated L motion as x and the integrated A/E motions as y.
The inequalities(x+y)^2<=(21/20)x^2+21y^2 and
y^2<=2(y_A^2+y_E^2) give

    Gamma(q)<=(483/400)psi5 q_LL/T^2+17850 phi q_A/T^6.

Every channel changes A by one, so q_A is the complete actual rate sum and
q_EE<=q_A. Fast AB/CD marks are paid at their actual small corrected jump
weight; no fast row is discarded or assigned a fictitious unit slow mark.
The constants are exactly(21/20)(23/20)=483/400 and42(25+400)=17850.

The received full-rate source bound gives

    integral phi q_A <=4T+(303/17)Qsrc
                       <=4T+(1212/17)T^3<72T^3.

Here303/17 exceeds21/19 and hence pays both AB and CD groups. The original
horizon4T pays immigration. The same raw-time source budget Qsrc<=4T^3 is
used by this inequality and by the source-paid primitive; there is no fresh
initial charge and no independence assertion.

With the separately received Qpsi<=3/(2T), the resulting bracket is exactly

    v=1449/(800T)+1285200/T^3.

Global gradient suprema give the complete jump cap
107/(100T)+9/T^3<=27/(25T). The compensator is continuous, so this also bounds
every Dynkin martingale jump. The endpoint correction satisfies
-2/T^2<q-b<=0 on both domains, including L'=0, as separately checked in the
residual receipt.

Exact fixtures are v=.0001824102,j=.000108 at T=10000, and
v=.0000181137852,j=.0000108 at T=100000. No fitted coefficient or growing
compact cutoff appears.

## Same-stop probability union and limits

Include the original common physical gates, source first-hit clock, primitive
first-hit clock and deadline in the stopped process. Their continuous clocks
have no overshoot. The two auxiliary failures are at most

    exp(-T^3/2500)+exp(-T/80).

The source term is counted ONCE, not separately for each use of its occupation
budget. Its state gates, the raw startup, count band and upper-ratio protection
remain externally supplied first-failure obligations. This receipt accepts the
full corrected-q costs conditional on those supplied inputs. It does not alone
prove target attainment, the final numerical window, early-clearance exclusion,
physical removal, or a finite-N distributional/CLT claim.
