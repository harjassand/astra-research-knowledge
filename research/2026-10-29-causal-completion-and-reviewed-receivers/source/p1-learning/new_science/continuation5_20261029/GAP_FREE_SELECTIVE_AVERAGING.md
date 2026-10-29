# Selective kinetic averaging without a visible spectral gap

29 October 2026. Central construction developed by Astra P1 / root in the
fifth continuation. This is a new result within this research record;
historical priority is not established. Relative-energy semigroup
perturbation theory is a close, explicitly credited predecessor.

## 1. Intended consequence

A supplied bath can suppress hidden kinetic memory in fixed-time visible
response operators, uniformly in elapsed time. Its required strength can
be independent of system size and the slowest visible relaxation rate.
Only the hidden directions coupled to visible motion need dissipate;
other microscopic information can remain frozen forever.

The receiver below is a compressed operator bound. It requires the
declared initial condition and controls terminal observations and
two-time equilibrium response. Arbitrary complete trajectory records are
not included. SELECTIVE_KINETIC_ANNEALING.md supplies the physical family.

## 2. Finite-dimensional theorem and proof

Let P be an orthogonal projection on a real or complex Hilbert space,
Q=I-P, and A a nonnegative self-adjoint matrix. In PH direct-sum QH write

    A = [[a,b*],[b,C]].                              (1)

Suppose, for all u in PH and v in QH,

    |<v,b u>| <= eta sqrt(<u,a u><v,C v>),
    0<=eta<1.                                      (2)

Then

    sup_(t>=0) ||P exp(-tA)P-exp(-ta)||_(PH->PH)
       <= eta^2/[2 sqrt(1-eta^2)].                  (3)

Here the second operator acts on PH. No invertibility, positive spectral
gap, one-dimensional null space, or dimension bound is assumed.

**Proof.** Start (u,v)=exp(-sA)(x,0). Thus u'=-au-b*v and v'=-bu-Cv.
For a fixed t set

    Eu=int_0^t <u,au> ds,  Ev=int_0^t <v,Cv> ds,
    J=int_0^t Re<v,bu> ds.

The hidden energy identity gives ||v(t)||^2/2=-Ev-J, so

    Ev<=-J<=eta sqrt(Eu Ev),    Ev<=eta^2 Eu.         (4)

The full dissipation identity gives

    ||x||^2/2 >= Eu+Ev+2J
      >= Eu+Ev-2 eta sqrt(Eu Ev)
      = (sqrt(Ev)-eta sqrt(Eu))^2+(1-eta^2)Eu.

Therefore

    Eu<=||x||^2/[2(1-eta^2)],
    Ev<=eta^2||x||^2/[2(1-eta^2)].                  (5)

Test the visible Duhamel error against y in PH. With
w(s)=exp[-(t-s)a]y, its magnitude is at most

    int_0^t |<v,bw>| ds
      <= eta sqrt(Ev) sqrt(int_0^t <w,aw> ds).

The last integral is (||y||^2-||exp(-ta)y||^2)/2<=||y||^2/2.
Insert (5) and take the supremum over unit x,y. QED.

The order eta^2 expresses two passages between the visible and omitted
spaces. A small additive norm of b alone does not supply (2).

## 3. Externally prescribed controls

The same bound holds for finite piecewise-continuous A_s with a fixed P,
a common Hilbert space, and uniform (2). Let U_A(t,0) solve U'=-A_t U
and U_a be the visible evolution. Then

    ||P U_A(t,0)P-U_a(t,0)||
       <= eta^2/[2 sqrt(1-eta^2)].                  (6)

Use the instantaneous energies in (4)-(5). The backward visible test
w(s)=U_a(t,s)*y solves w'=a_s w, w(t)=y, so its integrated energy is
again at most ||y||^2/2. Neither elapsed time nor the number of switches
enters. The displayed U is the physical density propagator; its adjoint
is the observable propagator and has the same norm comparison.

State/history-dependent control is not made externally prescribed merely
by conditioning on its observations. Changing equilibrium, changing P,
or adding unmodelled kicks is outside this assertion.

## 4. Continuous hidden variables: the extension actually used

The receiver uses finitely many visible states and circle coordinates.
Let H be the nonnegative self-adjoint hidden Laplacian, B a bounded
nonnegative self-adjoint native jump operator, and A=kappa H+B on D(H).
P commutes with H and HP=0; a and b are bounded. The common closed form
domain is D(H^(1/2)). The energy proof holds on regular data and extends
by density and the contraction/closed-form energy identity. One may
also truncate the Fourier resolution, compress the bounded native form,
and pass to the strong semigroup limit; the form inequality persists.

Finitely many bounded native modes and positive piecewise-constant
multiples of the same H permit the same concatenated proof. No claim is
made for arbitrary unbounded time-dependent operators without justified
well-posedness and energy identities.

## 5. The bath need not have a full hidden gap

Suppose A=B+kappa H, HP=0, a=PBP, b=QBP, with B,H nonnegative.
It suffices that

    |<v,bu>|^2 <= J0 <u,au><v,Hv>.                  (7)

Since C>=kappa H as forms on QH, eta^2=J0/kappa works. For J0<kappa,

    delta_mem=(J0/kappa)/[2 sqrt(1-J0/kappa)].        (8)

H can have a large kernel. Only coupled directions must be controlled
in its energy seminorm. Equivalently, H^(-1/2)b must be bounded relative
to a^(1/2), with inverse off ker(H). A coupling component in ker(H)
cannot be certified by (7). An actual operation must supply this bath;
the theorem does not derive it from known equilibrium weights.

## 6. Genuine visible receiving laws

Let the Hilbert space be L2(mu), P conditional expectation onto all
visible functions, A an actual reversible Markov generator in positive
notation, and a a visible Markov generator. Both P exp(-tA)P and exp(-ta)
are positive stochastic kernels. No signed projected path law is used.
For centered visible f,g,

    |<g,[P exp(-tA)P-exp(-ta)]f>|
       <= delta_mem ||g||_2 ||f||_2.                (9)

This controls equilibrium two-time correlations and relaxation following
an actually supplied perturbation of the initial density. If the initial
full law has density g0(Y)>=0 with mu[g0]=1, then

    TV(visible full law at t, visible reference law at t)
       <= min(1,delta_mem ||g0-1||_2/2).             (10)

For equilibrium readouts U(Y0),V(Yt) with a0,b0 possible values,

    TV(joint two-time readouts)
       <= min(1,delta_mem sqrt[(a0-1)(b0-1)]/2).     (11)

For (10), terminal density L1 is at most L2. For (11), apply (9) to
centered indicators, sum, and use sum_j sqrt[p_j(1-p_j)]<=sqrt(k-1).
An arbitrary microscopic initial state need not have a useful density
norm. A warranted bounded local initial reweighting can avoid a volume
penalty. Neither formula controls an unrestricted full trajectory.

An old record D can select a calibrated reference or a schedule only
under its actual conditional initial-law contract. Unconditional
stationarity does not remove correlation with D. Simultaneous finite-data
coverage is not posterior coverage for every rare realized D.

## 7. Separate calibration error: an established receiver

Suppose fitted ahat preserves the same pi and

    |<f,(ahat-a)g>| <= eps sqrt(<f,af><g,ag>),
    0<=eps<1.                                      (12)

Then ahat>=(1-eps)a and the ordinary cross-energy argument gives

    sup_t ||exp(-tahat)-exp(-ta)||
       <= eps/[2 sqrt(1-eps)] = delta_cal.           (13)

Test one forward evolution against the other backward evolution and
integrate their energies, each at most half its endpoint squared norm.
The same proof covers externally scheduled controls. This is the
reversible specialization of Veselic's theorem, not a new perturbation
result. Total actual-to-fitted error is at most delta_mem+delta_cal.
Multiplying both directions of each known reversible local update by an
estimated mobility preserves pi. Estimating or rounding equilibrium
ratios generally changes pi and cannot use this kinetic error budget.

## 8. Primary predecessors and claim boundary

Kresimir Veselic, *Bounds for contractive semigroups and second order
systems*, Theorem 1, 2004 preprint / 2005 publication:
<https://arxiv.org/pdf/math/0404120>. Its uniform full-semigroup
cross-energy comparison is the direct ordinary predecessor of this proof.

Mori-Zwanzig projection and memory estimates are established; see Zhu,
Dominy and Venturi, *On the estimation of the Mori-Zwanzig memory
integral*, <https://arxiv.org/pdf/1708.02235>. Uniform-in-time averaging
and simultaneous many-particle averaging are also established; see
Barre, Dobson, Ottobre and Zatorska, *Fast non mean-field networks:
uniform in time averaging*, <https://arxiv.org/pdf/2003.14230>.

The candidate addition here is the quadratic compressed bound, its
locally acquirable selective control family, and its collective-response
consequence without an inverse visible-gap factor. Historical novelty,
practical speedup and an apparatus have not been established.
