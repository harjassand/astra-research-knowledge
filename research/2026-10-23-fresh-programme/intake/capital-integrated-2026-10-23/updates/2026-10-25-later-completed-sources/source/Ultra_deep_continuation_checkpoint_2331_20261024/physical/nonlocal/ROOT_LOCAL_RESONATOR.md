# A counted conventional local resonator

24 October 2026. Root construction supplied to the physical owner as a stronger
incumbent. The numerical integral below is exploratory, not an interval proof
or a physical device result. It must not be excluded by a one-node topology
restriction unless an actual physical requirement supplies that restriction.

Let each cell contain a backbone point mass m_b and a pendant point mass m_s.
The backbone rods have length a, speed c and static stiffness K. An internal
pendant rod has length ell and stiffness k, with the same material speed.
Their fully counted masses per cell are K(a/c)^2 and k(ell/c)^2. Thus

    M_total = m_b + m_s + K(a/c)^2 + k(ell/c)^2.

There is one outgoing backbone rod per cell and one pendant rod, so no factor
of two is needed. Static relaxation translates the pendant with the backbone;
the relaxed long-wave stiffness remains K. Distributed inertia enters the
acoustic mass through all four counted masses.

For frequency omega, alpha=omega*a/c and s=omega*ell/c, the internal rod has
dynamic stiffness matrix [[A,-B],[-B,A]], where

    A=k*s*cot(s), B=k*s*csc(s).

Eliminating the pendant point at a nonpole gives the backbone onsite load

    Z_eff=-m_b*omega^2 + A - B^2/(A-m_s*omega^2).

The exact distributed-backbone secular equation is consequently

    cos(q)=cos(alpha)+sin(alpha)*Z_eff/(2*K*alpha).

This includes internal modes of BOTH rod types. Away from the discrete
elimination poles, the side field and rod fields are uniquely determined by
the backbone amplitude. There is one right-moving channel exactly when the
real expression on the right lies strictly between -1 and 1, at regular
frequencies. At a pole the full uneliminated system must be used; isolated
frequencies do not affect the Landauer integral. There is at most one channel
almost everywhere, providing a one-channel Bose tail bound.

The comparison proposed to the owner uses K=M_total=theta=1,
a/c=1/sqrt(101), ell/a=1/10, m_b=1/1000 and k=2/5. The backbone rod mass is
1/101, the pendant rod mass is 1/25250, and
m_s=1-1/1000-1/101-1/25250 is positive. Identical total mass, stiffness and
material speed/cell length can therefore be compared with the N=4 Fejer rod
graph. Material area, junction routing and maximum actual relative motion
still require equal treatment; no cap on those was acquired here.

Using g(omega)=[(omega/2)/sinh(omega/2)]^2, a vectorized midpoint integral on
omega in [0,30] gave J=0.72404281294 at 150001 points and 0.72395493220 at
300001 points. No claim of quadrature certification follows from refinement.
The same exploration at k=.3 gave approximately .74284 and k=.5 approximately
.73690; this is a small diagnostic sweep, not a globally optimized incumbent.

If certified, this can beat the N=4 kernel while using ordinary local resonance.
The positive finite-rod Fejer theorem versus an unadorned local rod remains a
valid narrower construction; it would not establish advantage over this
equally informed conventional alternative. Transverse/torsional modes,
finite contacts, damping, minimum rod area and hardware realization are outside
both longitudinal metric-graph calculations.

## Total quantum endpoint motion without resolving narrow real bands

The oscillator identity

    hbar/(2 omega) coth[omega/(2 theta)]
      = k_B T [1/omega^2 + 2 sum_(j>=1) 1/(omega^2+nu_j^2)],
    nu_j=2 pi j theta,

follows from the partial-fraction expansion of coth. Positive spectral
calculus therefore gives a Matsubara formula for any translation-annihilating
endpoint force f, with static compliance C_0 and imaginary-frequency compliance
C(nu):

    Var(f.x)=k_B T [C_0+2 sum_(j>=1) C(nu_j)].

This is the TOTAL Gibbs variance including zero-point motion. Eliminating the
distributed fields at imaginary frequency preserves the full resolvent; it
does not discard their modes. Since the elastic operator is nonnegative,
C(nu)<=f^T M_point^(-1) f/nu^2 for forces only on positive endpoint point masses.
The tail after L terms is consequently at most

    k_B T (f^T M_point^(-1) f)/(2 pi^2 theta^2 L).

For the local resonator, let eta=nu*a/c and zeta=nu*ell/c, and define

    P=k*zeta*coth(zeta), C=k*zeta*csch(zeta),
    D=m_s*nu^2+P,
    A=m_b*nu^2+2*K*eta*coth(eta)+P-C^2/D,
    B=2*K*eta*csch(eta), Delta=sqrt(A^2-B^2).

Its exact Bloch-averaged pendant-relative and adjacent-backbone compliances are

    C_pendant(nu)=1/D+(1-C/D)^2/Delta,
    C_adjacent(nu)=2/Delta*[1-B/(A+Delta)].

These follow by a two-by-two Schur complement and the positive integral
average_q 1/(A-B*cos q)=1/sqrt(A^2-B^2). The static limits are C_pendant(0)=1/k
and C_adjacent(0)=1/K. At high nu, evaluate coth/csch with exp(-eta) to avoid
overflow. A small main point mass can increase actual zero-point extension;
an inferior upper bound is not a proof of infeasibility.

For the Fejer rod graph at imaginary frequency the scalar endpoint inverse is

    G(q,nu)=[m*nu^2+2 sum_l kappa_l*eta_l*
              (coth(eta_l)-cos(lq)*csch(eta_l))]^(-1),
    eta_l=nu*l*a/c.

The l-cell endpoint-extension compliance is the Bloch average of
2[1-cos(lq)]G(q,nu). Its static term uses the positive spring graph rather
than replacing all rods by one effective spring. This permits an equal total
quantum endpoint-range comparison with a controlled positive Matsubara tail.
Quadrature error in any remaining q integral must also be controlled.
These endpoint formulas do not supply bounds on continuum local strain,
cracks, transverse modes or atomic-scale fluctuations.
