# A paid source-conditioned switch, without an entrance-profile or gap

Author construction for the signed-receiver continuation. This earns the
actual two-stage activation bound needed at the peer/corner interface.
The proof uses finite birth/death Green identities, not a stationary
entrance law, rapid equilibration, a neighboring-profile premise or a
uniform spectral gap.

## 1. Actual operation and the uniform conclusion

Start at anchors A=D=1, with B=0,E=q>=0 and

    C=B+s1, F=E+s2, s1,s2>=n>0.                         (1)

Both conservative directions are live at their true raw rates. Until the
first block reaction, the only block hazards are

    h1=alpha1*B, h2=beta1*E, B0=alpha0+beta0.

If this first block event is source1 of port i, retain its ACTUAL shift:
that anchor becomes2 and that port's C-coordinate increases by1. Run the
actual conservative background until the next block event. The event
that the OTHER port's source1 occurs before the newly available own
source2 has probability, including the probability of the first source,
bounded by

    P_i <= 3*alpha_i1/[2*alpha_i2*n].                    (2)

Other actual block hazards only reduce the event. The bound is uniform
in q, in both majority gaps and their ratio, and in all positive core
constants. In particular q may be arbitrarily large; no q/n premise is
needed. Summing (2) bounds the probability of TWO phase1 source1 events
before either source2 exits the low-low corner.

## 2. Real initial Green density is monotone

Index the finite physical core component by B=b_j=2j, j=0..J, with
E=q-b_j, C=b_j+s1,F=q-b_j+s2. (The parity of E is inherited from q.)
Let Q be its genuine pre-source core generator. Positive constants on
both directions make it a finite reversible birth/death chain; its
reference weights mu are ACQUIRED by

    mu_0=1, mu_(j+1)=mu_j*Q(j,j+1)/Q(j+1,j).

This is not an incoming law. Put H=h1+h2+B0 and let

    nu=delta_0*(-Q+diag H)^(-1), f_j=nu_j/mu_j.           (3)

Thus nu is the ACTUAL physical occupation measure from the empty endpoint.
Writing c_j=mu_j Q(j,j+1), the exact killed current balance gives

    c_(l-1)*(f_(l-1)-f_l)=sum_(j>=l) nu_j H_j >=0.       (4)

Hence f is nonincreasing, with no mixing argument. Also nu H=1.

For every bounded u, reversible summation by parts gives

    E_Q(f,u):=sum_j c_j(f_j-f_(j+1))(u_j-u_(j+1))
              =u_0-sum_j nu_j H_j u_j.                 (5)

If 0<=u<=1, then |E_Q(f,u)|<=1.

## 3. The actual source shift acquires the receiving conductances

Suppose port i's source1 occurs first. Let C_i denote its pre-source
landing-coordinate count (C or F). On the SAME physical minority index,
the post-source core generator Q_i has both anchor catalysts multiplied
by2, and C_i replaced by C_i+1. Its reference is exactly

    mu_i=mu/(C_i+1).                                   (6)

One checks this at each real edge by falling-factorial cancellation.
The post-source edge conductance is

    c_j^i=2 c_j/(min_edge C_i+1) <=(2/n)c_j.             (7)

This is the needed acquired neighboring-background relation. It follows
from the RAW source shift and conductance formula; it is not supplied as
a transport inequality. Normalizing mu_i is unnecessary.

Own source2 now has its actual hazard

    l_i=2 alpha_i2 B_i(C_i+1).

Write k_i=B0+h_other. Temporarily OMIT the additional own source1 hazard
at anchor2; this increases the probability of the other source winning,
so it is a legitimate upper comparison. Let

    u_i=(-Q_i+diag(l_i+k_i))^(-1) k_i.                  (8)

This is an actual finite competing-kill probability, not a chosen output
profile. As a function of the own minority count, l_i is increasing and
k_i is decreasing. Ordered coupling of finite nearest-neighbour chains
(run independently until meeting, then together) and common kill clocks
therefore proves that u_i is nonincreasing in its own minority count.
In the common B index, u_1 decreases and u_2 increases.

Consequently every edge product in E_Q(f,u_i) has the SAME sign. Combining
(5),(7), without any gap or cancellation estimate,

    |E_(Q_i)(f,u_i)| <=(2/n)|E_Q(f,u_i)| <=2/n.          (9)

## 4. Complete source-weighted receiving identity

Multiply the equation for (8) by f*mu_i and sum. Formula (6) cancels the
entire newly created C_i+1 factor in l_i. Exactly

    P_i:=sum_j nu_j alpha_i1 B_i u_i
       = alpha_i1/(2 alpha_i2) *
         [sum_j nu_j k_i(1-u_i)/(C_i+1)
                            - E_(Q_i)(f,u_i)].         (10)

The first term is at most 1/n, because nu k_i<=nu H=1. Equation (9)
then proves (2). All source competitions and the REAL post-source
coordinate C_i+1 are retained in this identity. The occupation measure
is (3) from the actual point input, not mu.

The finite component q can grow without bound, and the physical mixing
gap can vanish. Neither enters (10). Conservative residence is included
through its actual Green operators. This lemma bounds an actual source
output probability; the larger corner construction separately pays the
physical time and noncore reward.

## 5. Scope and wider reusable operation

The boundary input B=0 is used to earn monotonicity (4). Arbitrary
interior inputs need not have that Green-density monotonicity, so the
bound is not silently asserted there. A general finite background would
need its own sign or energy control of the bilinear term in (10).

The same calculation works with pre-anchor a>=1 and fixed peer anchor d,
with core time factor (a+1)/a and source prefactor
alpha_i1/[alpha_i2*(a+1)]; the other nonzero channels may be stopped as
competing exits. The a=1 version above is the one used in the fully live
corner. It supplies a concrete missing operation beyond bounded rate
distortion: the REAL source-weighted post hazard cancels its shifted
reference factor, and a monotone actual Green density controls the
receiving Dirichlet term.

Finite Green inverses, current balance, reversible summation by parts
and ordered birth/death coupling are ordinary methods. The raw retag
identity and their use to pay this source-conditioned switch are the
author construction, not an independent novelty certification.

check_source_conditioned_switch.py verifies (4)--(10) by exact rational
two-stage kernels, including q=100 and majority gaps up to10^12. These
finite checks support but do not replace the uniform proof.
