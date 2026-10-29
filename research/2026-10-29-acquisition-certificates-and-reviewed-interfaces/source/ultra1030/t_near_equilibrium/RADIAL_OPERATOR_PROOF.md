# A globally qualified radial operator escapes the relative-Maxwellian barrier

29 October2026. Actual normalized hard-sphere model, not Maxwell rates.
This is a positive operator/cost interface for a bounded SIGNED perturbation
query. It does not by itself provide a normalized continuous velocity sample.
The subsequent finite-observation positivity consumer is treated separately.

## 1. Representation and exact angular integration

Use beta=3/4, h=(f-M)/M^beta, and restrict to rotationally invariant sources
and solutions. This restriction is explicit, preserved by the model and
available to the ordinary isotropic deterministic/particle comparator.
Here beta denotes a REFERENCE-DENSITY POWER. The collision rate exponent
remains exactly1: |v-w|. It is not the paper's VHS exponent also named beta.
Mass and energy matching imply int M^beta h=0 and int |w|^2 M^beta h=0.
The linearized gain kernel may therefore subtract a(V)+c(V)s^2, where V=|v|,
s=|w|. Its coefficient functions can depend on V, but its tested moment
space remains only the conserved radial mass/energy space.

Integrate the native kernel over the incoming direction BEFORE taking an
absolute value. With m=min(V,s), z=max(V,s), define

    F(x)=int_0^1 exp[x(1-u^2)/2]du
        =sum_(n>=0) x^n/(2n+1)!!,
    A(m)=4F(m^2)-m^2/3,
    k(V,s)=A(m)/z-z.                                   (R1)

At V=0 this is4/s-s. For m>0,
F(m^2)=sqrt(pi/2) exp(m^2/2)erf(m/sqrt2)/m.
The series shows A>=4 and A is increasing: its coefficients are4,1 and
4/(2n+1)!! for n>=2. Consequently k is increasing in m and decreasing
in z, an important enclosure fact.

To derive (R1), integrate4exp(v_perp^2/2)/|v-w| over uniform cosine.
Set r=|v-w|, D=V^2-s^2. Its integral is2/(Vs) times

    exp[(V^2+s^2)/4] int_(|V-s|)^(V+s)
             exp[-r^2/8-D^2/(8r^2)]dr.

The primitive is sqrt(pi/2) times the sum of
exp(-|D|/4)erf((r-|D|/r)/(2sqrt2)) and
exp(|D|/4)erf((r+|D|/r)/(2sqrt2)). The second term cancels at the two
endpoints; the first gives2sqrt(pi/2)exp(-|D|/4)erf(m/sqrt2).
Thus the averaged gain is4F(m^2)/z. The averaged loss is z+m^2/(3z).
This pays angular cancellation analytically, without a free conditional
average or an independent value for each direction.

## 2. Weighted row and actual finite certificate

Let rho_beta(s) be the normalized chi3 density of a Gaussian of variance
1/beta, and nu(V)=E_(W~M)|v-W|. The complete controlled row is

    J(V)=D(V)/nu(V) int rho_beta(s)|k(V,s)-a(V)-c(V)s^2|ds,
    D(V)=beta^(-3/2)exp[-(1-beta)V^2/2].                 (R2)

The result ACQUIRED by certify_radial_rows.py/RADIAL_ROW_CERTIFICATE.json is

    J(V)<=99/100 for EVERY V>=0.                       (R3)

The head0<=V<=8 is covered by51 closed intervals with exact dyadic controls.
The intervals form a complete dyadic bisection cover. The optimizer only
proposes coefficients; arbitrary proposed coefficients would be valid if
the subsequent outward bounds passed. No optimizer accuracy is a theorem
premise. The largest admitted actual interval bound is below0.98375.

The radial integral is bounded by512 intervals of width1/32 over[0,16],
plus analytic first-cell/tail bounds. There is no source/target velocity
cutoff. On [Vlo,Vhi]x[slo,shi], excluding the origin cell,

    k_low=A(min(Vlo,slo))/max(Vhi,shi)-max(Vhi,shi),
    k_high=A(min(Vhi,shi))/max(Vlo,slo)-max(Vlo,slo).

These follow from the monotonicity just proved. Combining with the exact
quadratic-control range gives a uniform absolute-integrand upper. Each bin
is multiplied by an outward upper for its Gaussian probability, obtained
from erf(s sqrt(beta/2))-s sqrt(2beta/pi)exp(-beta s^2/2).

For the first interval[0,d], bound the gain by A(d)/s and integrate1/s
against rho_beta exactly. The remaining loss/control part is bounded by
Vhi+4d/3+|a|+|c|d^2. For s>=S=16>=Vhi, bound the absolute kernel/control
by A(Vhi)/s+s+|a|+|c|s^2. All four truncated chi moments are evaluated by
their explicit erfc/exponential formulas in the code. D(V)/nu(V) is
decreasing; nu is radial convex and nondecreasing, so the factor at Vlo
is an upper. Every scalar bound is outward Arb at128bits; exact upper
dyadics are retained in the JSON. This is a continuum enclosure, not a
claim based on the earlier four-anchor preview.

## 3. Analytic native speed tail

For V>=8 set a=c=0. Since F(s^2)<=sqrt(pi/2)exp(s^2/2)/s, splitting the
positive gain at s=V and integrating its two Gaussian envelopes gives

    gain_row/nu <=4/[beta(1-beta)V^2].

The absolute loss has bound

    beta^(-3/2)exp[-(1-beta)V^2/2]
                [1+2sqrt(2/(pi beta))/V],

using nu(V)>=V and triangle inequality. Both bounds decrease with V.
At V=8 their sum is below0.333969, as outward-certified separately.
Hence (R3) holds on the entire unbounded speed tail.

## 4. Why this does not contradict the earlier obstruction

In relative-M variables, the positive gain mass2nu escapes every fixed
velocity ball. A fixed finite moment correction is tight and cannot remove
it; that theorem remains valid. Here M^beta, beta<1, changes the tail norm,
and the resulting raw row tends to ZERO relative to nu. This is a real
representation change, not adding more fixed moments to the refuted norm.
Angular integration is valid only for the declared invariant radial class.

The quartic relative-M preview is preserved: it narrowly failed its origin
row and, more fundamentally, its nonlinear product doubles polynomial degree.
The beta Gaussian weight instead obeys the exact collision identity
M^beta(p)M^beta(q)=M^beta(v)M^beta(w). This pays the nonlinear partner
Gaussian integral used in the next construction.

## 5. Cost and scope

The executed full-domain certificate evaluated101 adaptive head intervals
and completed in0.71602seconds after imports, with no kinetic sampling.
It is an operator admission result, not exact nonlinear sampling or data
acquisition. The sources are explicit, the exact dyadic control table is
finite input to the consumer, and its construction/precision are charged.
Weighted linearized semigroups, moment controls and radial integration are
established mechanisms; historical priority of this specific admission and
its subsequent consumer is UNKNOWN. Strong equally informed ordinary
isotropic spectral/deviational methods retain the same source and symmetry.
