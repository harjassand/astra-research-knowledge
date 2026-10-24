# What a floating-pair continuity test actually requires

W75, 24 October 2026. Conditional circuit derivations. No measured switch,
current spectrum, settling time, or physical advantage. This qualifies the
already proposed ideal-open comparator; it is not a new assignment.

## 1. Exact DC leakage law

Consider two equal stars with d leaves each, leaf conductance a>0, and an
optional hub edge a. Select one leaf in each star. Their external drivers
are A and0 through identical series resistance r_s. Set

    p=a/(1+a r_s),  k=d-1.

Every unselected terminal, INCLUDING each hub, instead has off-conductance
g>=0 to a grounded environment. It has no other DC burden. Eliminating an
unselected leaf adds a g/(a+g) to the hub's ground conductance. Thus the
total unselected shunt on each hub is

    H=g+k a g/(a+g).

After eliminating the two selected leaves as well, the hub equations are

    (p+H+a)u-a v=p A,
    -a u+(p+H+a)v=0.

The receiver current magnitude, present only when the hub edge exists, is
therefore EXACTLY

    J_g = a p^2 A / [(p+H)(p+H+2a)].                 (L1)

For no edge, the receiving star has no driven source, so its DC mean is0.
For g=0, J_0=a p A/(p+2a), a degree-independent positive constant.
For fixed a,p,A and fixed g>0, J_g=Theta(d^-2). To keep J_g/J_0 bounded
below independently of d, H=O(a), equivalently d g=O(a) in the small-leakage
regime g/a->0. This is an aggregate leakage condition, not a claim that
each real switch has a conductance-valued or temperature-independent leak.
Fixed leakage-current offsets require a separate offset/calibration model.

If the selected ports are the TWO HUBS, replace p by their source
conductance g_s and replace H by d a g/(a+g) in the same two-hub equations.
Consequently opening the leaves but retaining fixed per-leaf DC leakage
does not by itself grant constant contrast to fixed ordinary hub sources.
An ideal floating leaf (g=0) does remove its DC shunt completely.

This is an exact mean-signal law. Thermal/correlated noise, observed
leakage fluctuations and alternate commands can contain additional
information; (L1) is not an all-data or all-protocol lower bound.

## 2. Exact capacitive transient from an acquired reset state

Take g=0 and give each of the k unselected LEAVES per star an identical
capacitance C>0 to the environment. Give the hubs zero capacitance in this
explicit model. Selected-port capacitances and switch charge injection
are omitted. Prepare every capacitor at0, then apply the above constant
selected-pair commands at t=0. The selected branch conductance is p.

Write w_U,w_V for the common voltages of the unselected leaves in the two
stars, s=w_U+w_V and z=w_U-w_V. Exact elimination of the hubs gives

    u+v=[p A+k a s]/[p+k a],
    u-v=[p A+k a z]/[p+(k+2)a],
    C ds/dt=a[(u+v)-s],
    C dz/dt=a[(u-v)-z].

The resulting time constants are

    tau_c=C(p+k a)/(a p),
    tau_d=C[p+(k+2)a]/[a(p+2a)].                    (C1)

Both grow linearly with d at fixed positive a,p,C. With the edge present,
the EXACT received mean is

    J(t)=(p A/2)[c0+b_c exp(-t/tau_c)
                         +b_d exp(-t/tau_d)],      (C2)
    c0=2a/(p+2a),
    b_c=-k a/(p+k a),
    b_d=p k a/{(p+2a)[p+(k+2)a]}.

J(infinity)=J_0 and J(0)=a p^2 A/{(p+k a)[p+(k+2)a]}.
With no edge, the receiving mean is0 at every time for this reset state.
This exhibits a slow physical mode even though the graph path uses only
three resistors. It does NOT show that discrimination must wait a full
settling time.

For example, in a SEPARATE stipulated fixed white receiver-noise model
E[eta(t)eta(t')]=S delta(t-t'), the mean-only continuous-record KL is

    D_mean(T)=1/(2S) integral_0^T J(t)^2 dt.         (C3)

The integral is an explicit sum of six exponential integrals. For large
d and 1<<T<<d (with dimensional constants held fixed),

    J(t) ~ a p^2 A t^2/(2 C^2 d^2),
    D_mean(T) ~ a^2 p^4 A^2 T^5/(40 S C^4 d^4).

Thus this fixed-step, zero-reset-state test can reach constant mean KL at
T=Theta(d^(4/5)), earlier than Theta(d) settling. This is a conditional
asymptotic for that waveform and receiver; it is not a universal optimal
time bound. Early transient observation, other initial preparations,
distributed ordinary drives, thermal covariance information and other
schedules must remain available to a fair comparator. The ideal-open
DC action count alone establishes neither constant duration nor an
adaptive wall-clock advantage.

Reset/preparation is physical: charging O(d) capacitances to O(A) stores
O(d C A^2) energy. Parallel grounding through all ordinary ports can
shorten reset time while using all those ports and aggregate current.
Two selected ports alone can inherit the same slow common mode. Exact
reset tolerance and switching transients must be specified and measured.

## 3. Interpretation for the incumbent comparison

With ideal opening, no off-load, settled independent fixed-noise readings,
and all pairs precommitted, W73's random-pair continuity comparator is a
legitimate strong nonadaptive benchmark. Its circuit operation is already
ordinary two-terminal resistance measurement through a switch matrix.
The conditional acquisition advantage on the original permanently
terminated interface cannot be transferred to this expanded interface.

Real opening must characterize aggregate off-leakage, off-capacitance,
sensor input burden, switch feedthrough and both source/receiver noise.
The equations above show explicit changes that those premises can make;
they do not certify the survival or failure of an advantage after all
physical resources and competing schedules are optimized.

Primary engineering context: Keithley's *Switching Handbook*, sixth
edition, section4.4, distinguishes relay motion from circuit settling and
includes cabling/fixture leakage in measurement uncertainty. TI's
*Selecting the Correct Texas Instruments Signal Switch*, revisionE,
defines the distinct off-leakage and capacitance parameters. The numerical
scalings above are derived for the stated circuit, not taken from a
manufacturer or measured component.

https://download.tek.com/document/SwitchingHandbook.pdf
https://www.ti.com/lit/an/szza030e/szza030e.pdf

Status: local analytic derivation; finite replay in replay_instrument.py.
Fresh proof review UNKNOWN; physical validation NOT_ACQUIRED; practical
advantage UNKNOWN; novelty UNKNOWN; mission NOT_ACHIEVED.
