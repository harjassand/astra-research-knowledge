# An isolated, finite-clock response operation for the compact amplifier

25 October 2026. This follows COMPACT_INERTIAL_AMPLIFIER.md and
NORMAL_BAND_PREPARATION.md without modifying either. The advance is from
ground-band curvature to an actual finite-time packet and bounded readout
construction. It uses the COMPLETE isolated periodic canonical Hamiltonian,
not an assumed quadratic reduced mass. It still does not prove the live-
lead thermal contact has that response or bounded Gibbs motion.

Write R=B/B_0, f_b=I_0(2b)^-2, q(P)=gIP/(hbar B), and epsilon_b(q) for
the exact normal rotor ground energy. The normal state at zero flux is
psi_b proportional to exp(b cos psi). All preceding masses, pitch,
barrier, material cutoff, initialization and switching costs are retained.

## 1. The WHOLE lowest dispersion has an exact quadratic bracket

Let chi be the periodic real phase corrector used in the stiffness proof:

    chi'=1-[2pi/(int psi_b^-2)]psi_b^-2.

For ANY real q, psi_b exp(iq chi) is a periodic trial state. Its energy
is EXACTLY epsilon_b(0)+E_R f_b q^2, not a Taylor approximation. The
diamagnetic inequality gives the matching lower bound epsilon_b(q)>=
epsilon_b(0). Therefore the complete lowest helical dispersion satisfies

    P^2/(2B)<=E_0(P)-E_R b
                         <=[1+(R-1)f_b]P^2/(2B).      (1)

This holds across a finite momentum window without differentiating a tiny
numerical band width. Thus on that band a free hold of duration t has
unitary error, relative to the inertial evolution P^2/(2B), at most

    e_hold<=t P_*^2(R-1)f_b/(2hbar B)                  (2)

on |P|<=P_*. This compares the full ground-band phase, not merely its
second derivative at zero. With b=(1/4+epsilon)log R and t proportional
to B, (2) tends to zero.

## 2. The finite normal ramp can also preserve the known packet phase

The earlier normal preparation gave leakage amplitude a_*=hbar C_ad/T
uniformly at EVERY time during the ramp and every allowed momentum. Let
the instantaneous normalized ground vector be in parallel-transport gauge.
Writing the exact phase-removed vector as A(s)|0_s>+eta_s gives

    A'(s)=<partial_s 0_s|eta_s>,
    ||eta_s||<=a_*, ||partial_s 0_s||<=D_1/G.

Consequently the full vector differs from its adiabatic ground-band
transport, including phase, by at most a_*(1+D_1/G). Choose

    T>=hbar C_ad(1+D_1/G)/e_coh.                       (3)

All normal H_b(q) matrices are real in the Fourier basis (their cosine
couplings are real). Their rank-one eigenvectors can be chosen real and
continuous in the permitted (b,q) rectangle, so their b-Berry connection
is zero. There is no hidden phase oracle in that assertion.

For the ramp b(s)=s b, subtract its momentum-independent energy phase.
Equation(1), with f<=1, bounds the remaining phase by

    e_ramp_phase<=T P_*^2/(2hbar B_0).                 (4)

The final ground vector's change with q, in the same real Fourier gauge,
is bounded by the earlier derivative/gap estimate:

    ||psi_b,q-psi_b,0||
         <=2pi^2 sqrt(b+q_*^2)|q|,
    e_embed<=2pi^2 sqrt(b+q_*^2)q_*.                   (5)

For fixed B_0,I,P_* and g increasing, q_*=O(1/g), while the allowed
flux window is only logarithmically shrinking. Thus (5) tends to zero.
The coherent time in(3) has order hbar b^6/(E_R e_coh). For example take
e_coh=1/b; then T=O(hbar b^7/E_R), (4) tends to zero, and the full-state
ramp range bound still has added terms tending to zero (the coarse force
term is O(b^16/g)). Initial/control errors remain separate actual inputs.

## 3. An explicit packet and a nonvanishing bounded response signal

Use exactly the normalized initial momentum stock from the preparation
note,

    F(P)=P_*^-1/2 cos(pi P/(2P_*)), |P|<=P_*.

It has finite position and momentum moments and no sharp-edge infinite
position variance. The actual initial rotor is N=0. Apply the finite
isolated ramp, then hold the unchanged full periodic Hamiltonian for

    t_*=2pi B hbar/P_*^2.                              (6)

Up to a global phase, the resulting FULL pure state is within

    e_model=e_coh+e_ramp_phase+e_hold+e_embed            (7)

in vector norm of the explicit physical-coordinate state

    Phi_t(Y,phi)=F_t(Y)psi_b(phi-gY),
    F_t=exp[-it P^2/(2B hbar)]F.

To see this, first compare the coherent ramp to the exact ground-band
packet, then compare its full time-independent band evolution using(1),
and finally replace the normal eigenvector at each P by psi_b,0 using(5).
Unitarity transports the preparation error without amplification. There
is no physical postselection on a ground-band event. Equation(7) bounds
trace distance and hence ANY common final measurement's record-TV error.
It does not by itself bound unbounded position moments.

The explicit reference's Y marginal is exactly |F_t(Y)|^2 because the
normal state stays normalized under the shift phi-gY. Put k=P_*/hbar.
A direct one-dimensional overlap integral gives

    <cos(kY)>_(t=0)=1/pi,
    <cos(kY)>_(t=t_*)=1/(3pi),
    response_gap=2/(3pi)>7/33.                         (8)

For example on the momentum overlap write x=(P+P_*)/P_* in[0,1]. The
product is sin(pi x)/2. The hold phase is exp[-i2pi(x-1/2)], so integrating
that positive sine weight yields the second value. This is a FIXED
bounded response contrast on a time proportional to B, while the exact
nonlinear rotor, rather than its local harmonic expansion, is evolving.

For b=(1/4+epsilon)log R, fixed P_* and e_coh=1/b, all four errors in(7)
tend to zero. This is an actual isolated response-law construction. It
requires the growing drive/material resources already calculated, not
one fixed instrument that was assumed to have them.

## 4. A finite binary-qubit readout, with no instantaneous meter granted

The bounded cosine effect can itself be approximated by an explicit finite
probe operation. Supply a fresh independent qubit in |+x>, couple

    H_meter(t)=(hbar g_m(t)/2)Y tau_z,
    int_0^t_m g_m(t)dt=k, g_m>=0,

and read tau_x. Its own polarizing Hamiltonian proportional to tau_z
COMMUTES with the interaction; retain its known free rotation in the final
readout axis. For an instantaneous kick the exact result is cos(kY).
To control a genuinely finite pulse, use the full native Hamiltonian in
its interaction picture. The force bound and momentum norm give

    ||[Y_H(s)-Y]xi||
      <=s/B_0 ||p_Y xi||+F_* s^2/(2B_0).

The analysis-only partial reference kick shifts p_Y by at most hbar k/2.
Duhamel therefore bounds the actual finite-meter state error by

    e_meter<=(k/2)[t_m(p_*+hbar k/2)/B_0
                                      +F_* t_m^2/(2B_0)].          (9)

Here a fully controlled actual p_* is available. Since V_b>=0 and the
isolated hold conserves energy, the finite preparation-work bound gives

    p_*^2<=P_*^2+2B_0 E_R(b^2+2b).

The state/domain calculation uses these actual finite moments; the
unbounded Y coupling is not treated as a bounded operator. Each spin
branch is a finite-duration Stark force plus the bounded periodic lock,
with the ordinary self-adjoint finite-force propagator. No equilibrium
ground state during the measurement pulse is assumed.

Choose a positive finite t_m making(9) fit its error allocation. A triangle
pulse has finite peak2k/t_m and slew4k/t_m^2; the real instrument must
supply them. Known probe free rotation, initial coherence, finite detector
contrast and clock/storage error have their own acquired boxes. No
near-perfect detector or arbitrarily fine analog reading is required:
a fixed nonzero binary contrast suffices for the fixed gap(8).

All actual readout/source work is finite by the same force/moment bounds.
For instance ||Y(s)||_2<=||Y_start||_2+s p_*/B_0+F_*s^2/(2B_0), with
the additional bounded meter impulse included. This is a finite-per-design
bound, not a claim of a uniform operating Y variance over arbitrarily long
free holds.

## 5. Statistical operation and true boundaries

Compare fresh prepared copies with hold0 and hold t_*, using the same
declared readout law and a coarse positive contrast lower bound. With
model/meter/calibration errors sufficiently below the constant gap(8),
bounded Bernoulli concentration uses O(contrast^-2 log(1/delta)) copies
at fixed confidence. Each copy pays its actual stock, normal ramp,
isolation, hold and meter. Independent repeats of one unknown bath history
have NOT been substituted for fresh quantum packets. No empirical confidence
is inferred solely from this model-relative bound.

This realizes finite response on a clock of order B and explains what
ground-band inertance would mean operationally. It does NOT prove uniform
TOTAL Y variance through the full free hold from a small leakage bound;
only a finite moment bound per design is claimed. It also does not join
the live Rubin leads or establish the desired heat deficit. Those separate
equilibrium/finite-contact questions require their actual coupling, all
material modes and preparation error to remain inside the argument.

The initial canonical packet, rotor stock, two harmonic potential controls,
isolation switch and Y-qubit meter are real added capabilities, with the
finite amplitude/slew/phase resources specified above. If any required
box cannot be acquired, this proposed operation is UNKNOWN on that apparatus.
Its consequence is a proved response construction and a visible resource
cost, not a manufactured device or practical advantage.


## 6. A fully BOUNDED spatial-profile meter is another literal option

The linear-Y pulse above is a legitimate finite Stark-force model, but
assigning it to a finite-range instrument requires its actual range box.
There is a stronger bounded interaction alternative. Supply an independent
qubit with known coarse positive transverse polarization, and use

    H_m(t)=(hbar g_m(t)/2)cos(kY)tau_z,
    int g_m=A, g_m>=0, A=1/4.

This is an explicitly ADDED bounded spatial-profile coupling, not an
operation already supplied by the passive rotor. Its potential has norm
hbar|g_m|/2 and its Y-force is bounded by hbar|g_m|k/2 over the WHOLE real
line. It need not assume a finite hard coordinate range. Creating the
cosine profile and its calibrated strength/wavelength is a real interface.

For a frozen-kick reference, the final rotating tau_y mean is
sin[A cos(kY)] (multiplied by the probe polarization). Uniformly for
|z|<=1, |sin(Az)-Az|<=A^3/6. Therefore the two reference packets of(8)
have a qubit mean gap at least

    A*2/(3pi)-A^3/3 >7/132-1/192 >1/25.               (10)

A genuinely finite pulse needs no frozen-coordinate assertion. Use

    exp(ikY_H)-exp(ikY)
      =i int_0^k exp[i(k-u)Y_H](Y_H-Y)exp(iuY)du.

The right Fourier shift changes p_Y by at most hbar k; the partial
reference meter kick changes it by at most hbar A k/2. Thus the same
state-induced Duhamel argument gives the explicit finite-pulse bound

    e_bmeter<=(A k/2)[t_m(p_*+hbar k(1+A/2))/B_0
                                       +F_*t_m^2/(2B_0)].          (11)

This treats the NONCOMMUTING native Y evolution by the Fourier identity,
not by a false statewise ordering of coordinate projectors. Every term
is already bounded by actual finite input energy and the native locking
force. Choose finite t_m so that(11) fits a fixed allocation. A triangle
pulse needs peak2A/t_m and slew4A/t_m^2; its absolute source-work bound is
2hbar A/t_m. The qubit's own tau_z Hamiltonian commutes with the coupling;
retain its known free phase in the readout. No initial pure qubit or
perfect detector is needed if their combined contrast has an acquired
positive constant lower bound.

For example in the unit-contrast reference, if e_model+e_bmeter<=1/400
per geometry, the actual mean gap is still greater than1/40. Coarse
contrast/offset and readout-error boxes can be included before choosing
that constant allocation. There is no accuracy requirement shrinking
with a rare Delta^2 signal here. Fresh independent prepared copies and
bounded binary concentration then acquire the finite response at a
constant-in-g sample count for fixed confidence and contrast. Its long
hold, stock production, huge locking resources and finite probe control
are still paid. This remains an isolated mechanical response experiment,
not a thermal-contact validation or proof of uniform operating variance.
