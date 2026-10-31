# An explicit passive-network binding of the source contract

1 November 2026. This is a declared ideal circuit construction, not a report of
fabrication or measurement. Kirchhoff/Dirichlet reduction is ordinary network
theory. It supplies an interpretable physical class for the acquired response
law, without assuming arbitrary Gram matrices are realizable by arbitrary
devices.

Let a finite resistor network have two clamped terminals with potentials 1 and
0, internal voltage vector v, and fixed nonnegative baseline conductances.
Assume each internal connected component touches a clamped terminal, making the
grounded baseline quadratic form H positive definite. Let v0 minimize baseline
power. Completing its quadratic energy gives

    P0(v)=c0+(v-v0)^T H(v-v0).

Actuator i adds conductance u_i>=0 across a specified pair of graph vertices.
The voltage difference across that edge is a_i^T v+h_i, with a_i its internal
incidence vector and h_i the contribution of clamped endpoints. Put

    g_i=a_i^T v0+h_i,
    b_i=H^(-1/2)a_i,
    y=H^(1/2)(v-v0).

The minimum total power is therefore

    J(u)=c0+min_y [||y||²+sum_i u_i(g_i+b_i^T y)²].

At unit voltage the terminal current equals total dissipated power, so one
external current measurement returns J(u). The Woodbury identity gives the
source form

    J(u)=c0+g^T P(I+P B P)^(-1)Pg,
    B_ij=b_i^T b_j,
    P=diag(sqrt(u)).

The maximum principle keeps every baseline voltage in [0,1], so |g_i|<=1:
G=1 is warranted by this ideal passive model. Dark g_i=0 and singular B are
allowed. The hidden interior can be arbitrarily large; the acquiring program
does not receive H,v0,g or B.

## A direct way to warrant the interaction scale

Suppose baseline hardware includes a known parallel conductance at least a>0
across each controllable edge. Its contribution to H implies

    H >= a a_i a_i^T,
    a_i^T H^(-1) a_i <= 1/a.

The second inequality follows by applying the first to H^(-1)a_i, or by the
rank-one Rayleigh quotient. For a_i=0 it is trivial. Hence B_ii<=1/a and
q=delta/a is a valid effective-dose upper bound. This bound does not require
measurement or reconstruction of every hidden baseline resistance. Adding
these baseline elements is a physical design choice; their power, wiring,
size, and altered baseline response are costs, not free qualification.

## Stronger control curvature for this subclass

The maximum principle also holds after any nonnegative conductance additions.
The envelope derivative partial J/partial u_i is the square of the actual
voltage difference across actuator i, hence lies in [0,1]. Consequently the
normalized source f(x)=[J(delta x)-c0]/delta has Hessian entries bounded in
absolute value by 2q, and its whole-simplex directional curvature can be taken
as 8q. This improves the generic Gram-source constant
8q(1+sqrt(q))² used in the separate consumer proof, but only for the declared
passive circuit subclass.

## Information and comparison boundary

The protocol assumes scalar terminal-current observations and commanded
conductance additions. It does not acquire internal voltages, every terminal
response, or arbitrary forcing measurements. If those are cheaply available,
ordinary multiport network identification can be a stronger and cheaper route.
Conversely, the presence of controllable internal elements does not logically
supply those measurements at zero cost. The correct comparator must receive the
same sensing and actuation interface.

This construction earns the ideal model contract. It does not demonstrate that
the generic worst-case acquisition budget is practical, that an existing circuit
cannot be directly solved, or that thermodynamic/engineering performance beats
an equally informed conventional design procedure.
