# Independent check of root's exact thermodynamic frontier

29 October 2026, Brisbane. Root supplied the candidate central theorem after
the complementary four-state construction. This note reconstructs its proof,
checks the hidden-dimension obligation, and gives a robustness extension.
It is an internal ordinary proof review, not external acceptance or priority.

## Claim checked

The supplied exact record is

    S=[[1,-1],[-1,1]], w_B=(1,1), v_R=v_L=(1,1), c=2.

Hidden departure rates are at most 1, and both port rates are at most ell.
The stationary weights total W=4, of which hidden mass V=2. All states are
even under the stipulated physical reversal. Entropy below is unnormalized
E=sum phi_xy log(phi_xy/phi_yx); physical normalized rate is E/4.

For 1<ell<3/2, let A=2(ell-1) and d=sqrt(1-A). Then the minimum over ALL
finite hidden dimensions is

    E_min = 4 d log[(1+d)/(1-d)].

At ell=1 every positive realization has infinite E. For ell>=3/2 zero E
is attainable. This is a resource frontier for a fixed consequence record,
not recovery of the original source's dissipation or a mean-evaluation speedup.

## 1. Rigidity does not assume the unknown hidden topology

Uniformize every hidden process at rate 1 and let N be its number of ticks
in a native port-to-port excursion, including virtual ticks. The intensity
measure includes N=0 direct jumps. The identities are

    integral N = V=2,
    integral N(N+1)=2c=4.

Therefore integral N(N-1)=0. Since this is nonnegative at every integer,
N is in {0,1} almost surely under the excursion intensity measure.

Every hidden state has positive weight and is reachable from a port without
an intervening port: take any path from a port to that state and its last
port. If its native rate were strictly less than 1, uniformization would have
a positive virtual self-step there, producing an excursion with at least two
ticks. If any hidden-hidden edge were positive, a reachable path using it
would likewise give at least two ticks. Both contradict the equality above.

Consequently EVERY compatible realization consists of direct port jumps
and hidden stars of rate exactly 1, each entered from and exited to a port.
This conclusion covers arbitrary finite hidden cycles and arbitrarily many
positive-weight hidden states; they are excluded by equality rather than
by an assumed canonical representation.

## 2. Star parameterization and entropy

For hidden state x of weight w_x, stationarity and its rate 1 make incoming
and outgoing total flux each w_x. Write its two incoming fractions as
alpha_x=(p_x,1-p_x), and its outgoing fractions as beta_x=(q_x,1-q_x).
Its boundary-edge entropy is

    w_x J(alpha_x,beta_x),

where J is Jeffreys divergence. The total hidden weight is 2. The total
self-return excursion flux is

    R=sum_x w_x r_x,  r_x=p_x q_x+(1-p_x)(1-q_x).

Each native port clock equals its fixed trace departure 1 plus its self-return
flux, so R<=A. Direct port edges have nonnegative entropy. In fact they are
symmetric for this record because equal incoming/outgoing margins imply
equal hidden off-diagonal trace contributions, but this extra fact is not
needed for the lower bound.

## 3. Binary inequality, constants and equality

Define

    g(r)=4 sqrt(1-2r) atanh(sqrt(1-2r)) for 0<r<1/2,
    g(r)=0 for r>=1/2, and g(0)=infinity.

Then J(alpha,beta)>=g(r). To prove this for r<1/2, interchange labels if
needed and write x=2p-1>0, y=1-2q>0. One has xy=1-2r and

    J=(x+y)(atanh(x)+atanh(y)).

Arithmetic-geometric mean gives x+y>=2sqrt(xy); convexity and monotonicity
of atanh on (0,1) give atanh(x)+atanh(y)>=2atanh(sqrt(xy)). Multiplication
gives the claimed constant. Equality holds when x=y, equivalently q=1-p.
For r>=1/2, nonnegativity of Jeffreys suffices.

Set z=sqrt(1-2r). On 0<r<1/2,

    g'(r)=-4[atanh(z)/z+1/(1-z^2)],
    g''(r)=4[(z/(1-z^2)-atanh(z))/z^3+2/(1-z^2)^2]>=0.

The last inequality follows by integrating 1/(1-t^2), which is at most
1/(1-z^2) on 0<=t<=z. The left derivative at r=1/2 is -8; the extension
by zero has right derivative 0. Thus the full g is convex and decreasing.
Jensen and R<=A give

    E>=sum_x w_x g(r_x)>=2g(R/2)>=2g(A/2)
      =4sqrt(1-A)log[(1+sqrt(1-A))/(1-sqrt(1-A))].

For attainment choose two hidden states of weight 1, with mirror entrance
fractions (p,1-p),(1-p,p), exit fractions reversed, and p=(1+d)/2. Add
symmetric direct port flow A/2. This is precisely the four-cycle family
in THERMODYNAMIC_COMPLETION.md. It matches both individual port caps and
all record entries; hidden clocks are 1.

At ell=1, A=0 requires every star r=0, giving disjoint incoming/outgoing
support and infinite entropy. At ell=3/2, a single hidden state of weight 2,
entrance=exit=(1/2,1/2), and symmetric direct flow 1/2 suffices for zero E.
For larger ceilings use this same construction. No limiting infinite state
family improves the lower bound, since it holds for every finite realization
with no dimension-dependent constant.

## 4. A robust entropy bound when exact clock rigidity is relaxed

The exact formula uses c=V/Lambda. It is therefore useful to retain a bound
that survives c>V/Lambda. Let h be native hidden-entry flux. Uniformization
gives for every integer k>=1,

    N(N+1)>=(2k+2)N-k(k+1)  for integer N>=1.

Integrating only positive-duration excursions yields

    h >= H_clock := max_{k>=1}
           [2(k+1)Lambda V-2Lambda^2 c]/[k(k+1)].

In particular h>=2Lambda V-Lambda^2 c. The ordinary Cauchy floor
V^2/(2c) is also valid. These are scalar necessary inequalities; they do
not assert that a complete network simultaneously attains all constraints.

The proof of Proposition 2 in THERMODYNAMIC_COMPLETION.md may use ANY
positive lower bound H on h. Thus use max(H_clock,V^2/(2c)) there. For
V=2,Lambda=1,c=2, H_clock=2 and the bound becomes E>=4log(1/A), matching
the exact frontier's leading divergence coefficient. For c=2+eta with
0<=eta<2, H_clock>=2-eta. Logarithmic divergence as A tends to zero persists
despite this positive moment slack and the loss of star rigidity.

An upper hidden-rate ceiling is not a lower rate or a tail bound. Statistical
certification of c, positive coefficients, reciprocal support and a physical
reversal remains separate. Finite coefficient precision also restricts how
close a realized affinity can approach the singular boundary.
