# A finite-aperture bounded readout for the prepared inertial response

25 October 2026. This closes the infinite spatial-profile assumption of the
bounded-meter option in FINITE_WAVE_PACKET_RESPONSE.md atcce43afab. It does
not claim that finite coupling norm equals field-generator production
energy. The proposed apparatus still needs a real calibrated bounded
profile over its finite active region, its derivative and time-control
boxes, and a physical frame. All predecessor proofs remain unchanged.

## 1. The reference packet gives a uniform aperture, not a false actual variance

Let k=P_*/hbar. For the explicit reference packet, initially

    Var(Y)=pi^2/(4k^2),
    Var(P)=P_*^2(1/3-2/pi^2), Cov_sym(Y,P)=0.

At the response hold t_*=2pi B hbar/P_*^2 its variance is exactly

    Var_ref(Y)=[19pi^2/12-8]/k^2 <8/k^2.              (1)

Both compared reference packets therefore obey
Pr_ref(|Y|>L)<=8/(k^2 L^2). The actual FULL state is within trace distance
e_model of that reference, so its same tail probability is at most the
reference tail plus e_model. No second moment of the actual state is
inferred from trace distance. In the following it is simpler to transfer
the common bounded measurement by contractivity and use ONLY reference
tails for the aperture error.

## 2. A compactly supported C^2 profile with explicit derivatives

Define eta(r)=1 for|r|<=1, eta=0 for|r|>=2. Between these regions put
z=|r|-1 and

    eta(r)=1-10z^3+15z^4-6z^5.

This is C^2,0<=eta<=1, |eta'|<=15/8 and |eta''|<=15. Set

    h_L(Y)=eta(Y/L)cos(kY).

It vanishes EXACTLY outside |Y|<=2L, agrees with the desired cosine on
|Y|<=L, and obeys

    ||h_L||<=1,
    H_1:=||h_L'||<=k+15/(8L),
    H_2:=||h_L''||<=k^2+15k/(4L)+15/L^2.              (2)

Use the explicit bounded qubit coupling

    H_m(t)=(hbar g_m(t)/2)h_L(Y)tau_z,
    int g_m=A=1/4, g_m>=0.

Its own tau_z Hamiltonian is retained in the readout frame. A frozen-kick
reference gives the final tau_y mean sin[A h_L(Y)]. Since
|sin[A h_L]-sin[Acos(kY)]|<=A 1_(|Y|>L), the aperture changes EACH
reference mean by at most8A/(k^2L^2). Thus the two means' difference loses
at most16A/(k^2L^2).

Choose L=40/k, independent of geometric gain. The loss is at most1/400.
The prior all-line bounded-profile gap was strictly greater than1/25;
the finite-aperture reference gap is consequently greater than3/80.
This is a finite active extent at fixed response accuracy, not a profile
postulated over the whole line.

## 3. A finite pulse remains controlled for this NONCOMMUTING profile

There is no need to pretend a scalar Lipschitz inequality automatically
holds on a quantum state. For a bounded C^2 function h, the native
canonical Hamiltonian gives on its finite-energy domain

    d h(Y_H(s))/ds=(p_Y h'+h'p_Y)_H/(2B_0).

Using p_Y h'=h'p_Y-i hbar h'' and the actual native force bound F_* gives

    ||[h(Y_H(s))-h(Y)]xi||
      <=s[H_1||p_Y xi||+hbar H_2/2]/B_0
                                      +H_1F_*s^2/(2B_0).          (3)

The analysis-only partial reference meter kick exp[-ia h_L(Y)tau_z/2]
shifts p_Y by at most hbar A H_1/2. Therefore interaction-picture Duhamel
gives the ACTUAL finite-pulse state error bound

    e_apmeter<=A/(2B_0){t_m[H_1(p_*+hbar A H_1/2)+hbar H_2/2]
                                             +(H_1 F_*/2)t_m^2}.  (4)

The exact native input-energy bound supplies p_* as in the predecessor.
All populated rotor bands are included; a small leakage probability is
not used to control an unbounded moment. For every finite design a
positive finite t_m satisfies a desired fixed error allocation. The real
amplitude/slew and bandwidth boxes must fit that choice.

For example if e_model+e_apmeter<=1/800 per geometry, the pair's mean
error is at most4/800=1/200. With the aperture gap above, the remaining
mean gap is still greater than1/40. Constant nonzero probe/detector
contrast scales that gap; its coarse uncertainty and offset drift must
be included before using bounded binary concentration. No near-perfect
measurement, arbitrarily fine analog record or g-dependent aperture is
needed for this fixed response discrimination.

## 4. What is physically closed, and what is not

A triangular pulse has peak2A/t_m, slew4A/t_m^2, and coupling-work bound
2hbar A/t_m. Its force is bounded by hbar|g_m|H_1/2. These are interaction
and source bounds within the declared finite component model. They do
NOT determine the energy, mass, waste heat or initialization of the
apparatus generating the spatial profile. A finite co-moving/relative
frame, the active length4L, profile error, qubit stock, readout and source
implementation still require their actual acquisition.

An implemented h_L with independently certified C^2/profile errors can
be compared to this model with the appropriate bounded-Duhamel/record
allowance. Arbitrary forces or geometry-dependent detector changes outside
the declared box cannot be dismissed merely because the reference packet
has small tails. The mathematical operation is finite aperture with exact
bounded coupling, not an assertion of a measured electromagnetic or
mechanical field generator.

Preparation, hold and readout can now be stated as one finite response
operation on explicitly supplied fresh stocks with counted controls. It
remains ISOLATED response. No coupled Gibbs variance, heat-blocking record,
material feasibility or practical advantage is inferred from the aperture
construction.
