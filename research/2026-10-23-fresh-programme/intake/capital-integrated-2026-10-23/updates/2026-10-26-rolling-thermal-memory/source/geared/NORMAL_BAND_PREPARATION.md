# A finite normal-band preparation operation for the compact amplifier

25 October 2026. This develops the exact compact-lock construction without
changing COMPACT_INERTIAL_AMPLIFIER.md. It addresses one actual preparation
obligation of that response mechanism. The operation is performed on the
ISOLATED canonical primitive. A working isolation/coupling switch and the
initial stock are added resources; this does not claim preparation of the
lead-coupled Gibbs state or a heat-transport theorem.

Use the preceding definitions B=B_0+Ig^2, E_R=hbar^2 B/(2B_0 I),
q(P)=gIP/(hbar B), and the exact positive lock

    h_b(q)=E_R(N-q)^2+V_b,
    V_b=E_R[b^2 sin^2 psi+b(1-cos psi)], N=-i partial_psi.

## 1. The normal gap has an elementary uniform lower bound

At zero flux, the ground density is
rho_b(psi)=exp(2b cos psi)/(2pi I_0(2b)), b>=0. It decreases monotonically
on[0,pi] and increases on[-pi,0]. For a periodic H^1 function u and
0<=x<=pi,

    |u(x)-u(0)|^2<=x int_0^x |u'(t)|^2 dt.

Since rho_b(x)<=rho_b(t) for0<=t<=x, multiply by rho_b(x), integrate and
exchange the order to obtain

    int_0^pi rho_b|u-u(0)|^2
          <=(pi^2/2)int_0^pi rho_b|u'|^2.

The same holds on the other half circle. Weighted variance is no larger
than the squared distance from the chosen constant u(0). Thus

    Var_(rho_b)(u)<=(pi^2/2)int rho_b|u'|^2.

The ground-state transform of h_b(0)-E_R b is exactly
E_R int rho_b|u'|^2. By minmax the FULL first normal excitation gap obeys

    gap_b(0)>=2E_R/pi^2,  ALL b>=0.                    (1)

This includes every rotor harmonic, not a local-curvature estimate.

## 2. A useful entire momentum window remains gapped

For0<a<1, the form inequality

    (N-q)^2>=(1-a)N^2-q^2(1/a-1)

and V_b>=0 imply
e_1(q)>=(1-a)e_1(0)-E_R q^2(1/a-1).
The real zero-flux ground trial gives e_0(q)<=E_R(b+q^2). Therefore

    gap_b(q)/E_R>=2(1-a)/pi^2-a b-q^2/a.

Take a=1/[8pi^2(b+1)]. If

    |q|<=1/[8pi^2 sqrt(b+1)],

then a b<=1/(8pi^2), q^2/a<=1/(8pi^2), and a<3/8. Hence

    gap_b(q)>=E_R/pi^2.                               (2)

Fix a target b_*, and choose a finite momentum window |P|<=P_*
whose q(P) satisfies this condition with b=b_*. It then satisfies(2)
along the ENTIRE ramp0<=b<=b_*.
For the compact fixed-I, large-g family and any fixed P_*, q(P_*) is
O(1/g), while the allowed window shrinks only as1/sqrt(log B). Thus a
fixed finite input wavepacket fits for every sufficiently large gain.
The alternative large-I/fixed-g route may require a different momentum
stock under this deliberately conservative window bound.

## 3. Explicit input and finite ramp

An allowed initial stock is the rotor angular-momentum state N=0 and an
independent relative wavepacket with momentum amplitude

    f(P)=P_*^-1/2 cos(pi P/(2P_*)), |P|<=P_*,
    f(P)=0 otherwise.

It has norm1, finite initial variance
Var(Y)=hbar^2 pi^2/(4P_*^2), and finite momentum second moment. Smooth
stock approximations with a separately bounded state error also work.
Preparing this packet, the pure rotor N=0 stock, common-motion stock and
fresh isolation is not granted by naming their states. In particular an
uncoupled rotor cannot be assumed cooled by the disconnected thermal leads.

During the isolated ramp b(s)=s b_*, s=t/T, helical P is conserved exactly.
Each fiber has a fixed common domain H^2(S^1), a bounded C^2 perturbation,
rank-one ground projection and the uniform gap G=E_R/pi^2. The derivative
bounds are

    D_1=2E_R b_*(b_*+1), D_2=2E_R b_*^2.

A sufficient normal-band leakage-amplitude estimate is

    leakage<=hbar C_ad/T,
    C_ad=8D_1/G^2+4D_2/G^2+56D_1^2/G^3.               (3)

Thus T>=hbar C_ad/epsilon gives outside-band probability at most epsilon^2
for ANY superposition supported in the declared momentum window. This
controls band population, not a free phase-corrected target wavepacket.

For clarity, the bounded-matrix theorem is NOT applied directly to the
unbounded rotor Hamiltonian. One route to(3) is finite Fourier Galerkin
compression. The lowest two minmax eigenvalues converge monotonically,
uniformly on the compact (b,q) rectangle (continuity plus Dini). For all
sufficiently large cutoffs their gap is at least G/2. Derivative norms
D_1,D_2 stay uniformly bounded under compression. Applying rank-one
Jansen-Ruskai-Seiler Theorem3 to those finite matrices gives(3). The
common diagonal kinetic part and bounded potentials make their propagators
converge strongly by Duhamel, while compact-resolvent eigenprojections
converge. Passing to the limit gives the same bound, uniformly in q.
Fiberwise integration then handles the wavepacket; it does not apply an
infinite-rank version of a finite-rank theorem without proof.

For fixed error epsilon, (3) has order

    T=O(hbar b_*^4/(E_R epsilon)).                     (4)

Large recoil makes this ideal sufficient time short, but its drive
amplitudes and slew are correspondingly large. Equation(4) is a controlled
model operation, not a claim that fixed apparatus can execute it.

## 4. Position motion is controlled in the FULL ramped state

Small band leakage alone would not bound an unbounded coordinate variance.
Here there is a separate exact force estimate. Throughout the ramp,

    |F_Y|<=F_*=gE_R(b_*^2+b_*),
    dot p_Y=F_Y, dot Y=p_Y/B_0.

On the full state, including all populated rotor bands, HS Minkowski gives

    ||Y(T)||_2<=||Y(0)||_2+(T/B_0)||p_Y(0)||_2
                                             +F_* T^2/(2B_0).     (5)

The initial rotor has N=0, so p_Y=P initially. This is a finite actual
second-moment bound; there is no probability-to-unbounded-variance shortcut.
For fixed B_0,I, b_*=O(log B), E_R=Theta(g^2) and the sufficient time(4),
the two added terms in(5) vanish as g->infinity (the slower one is bounded
by a constant times log^10(g)/(g epsilon^2)). Hence this mathematical
normal-band ramp can retain a UNIFORM full-Y preparation range while its
barrier/force resources diverge. They cannot be removed from the operation.

There is also a direct check on the projected coordinate. In parallel-
transport gauge the ground-vector derivative obeys

    ||partial_q psi_b,q||
          <=2E_R sqrt(b+q^2)/gap_b(q)
          <=2pi^2 sqrt(b+q^2).

The gauge-invariant quantum-metric contribution to Y^2 in a ground-band
packet is therefore at most

    4pi^4(gI/B)^2(b_*+q_*^2).                          (6)

It tends to0 in the fixed-I compact-gain family. This bounds one explicit
UV coordinate term but does not replace the full-state force bound(5) or
the as-yet unproved coupled-contact projection.

## 5. What must actually be acquired

The commanded energy coefficients are U_1=E_R b(s) and
U_2=E_R b(s)^2/2 for the positive first/second cosine harmonics. Their
maximum energy range, phase/pitch profile, slew, material cutoff and
isolation/switching error are real controls. A coefficient-slew cap L_U
requires, conservatively, T>=E_R(b_*^2+b_*)/L_U in addition to(3).
An amplitude cap must exceed E_R(b_*^2+2b_*). Feasibility is the actual
intersection of these requirements with any declared range/time budget;
if it fails this operation is UNKNOWN on that apparatus.

The source work obeys int|<partial_t V>|dt<=int||partial_s V||ds,
which is finite and of order E_R(b_*^2+b_*). This is work stored/supplied
during preparation, not heat blocked from one thermal lead. Bounds on
bounded potential/profile errors transfer by
||U_actual-U_model||<=hbar^-1 int||delta V(t)||dt.
Kinetic parameter errors are unbounded perturbations and need the actual
finite-energy/state-induced estimate, not this bounded-operator formula.
The stock, calibration and switches have their own confidence/time costs.

Most importantly, attaching the spring and live leads breaks the conserved
helical momentum used here. The operation supplies a prepared isolated
normal band with finite force/work and full-Y moment bounds. It does NOT
prove that the contact then stays in that band or has the desired thermal
deficit. Finite material elastic modes and the coupled-bath projection are
the next decisive requirements of a physical passive amplifier.

Primary: Jansen-Ruskai-Seiler, arXiv:quant-ph/0603175v3, common-domain
conditions and Theorem1 on pp3-4, Theorem3/Eq6 on pp4-5. I directly read
those portions. Its Theorem3 explicitly assumes bounded H; the Galerkin
passage above is retained to avoid silently dropping that condition.
https://arxiv.org/pdf/quant-ph/0603175 .
