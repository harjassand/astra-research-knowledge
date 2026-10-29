# A fixed-coupling nonlinear impurity receiver in an eta-defect frame

29 October 2026. This source is independent of the frozen
`c_resonant_fibers/` construction. It does not improve its extreme
volume-dependent weak-coupling limit. It changes the admitted initial
state and perturbation, and never projects onto energy resonances.

The positive output is a qualified nonlinear local-density response of a
strongly interacting Hubbard model at fixed density and fixed couplings.
The computational engine is an exact known symmetry plus ordinary
bounded-source Dyson/particle-sector truncation. No new generic simulation
algorithm, world priority, generic finite-density closure, or physical
state preparation is claimed. The strongest symmetry-aware ordinary
method reproduces this operation. See `PRIOR_AND_DECISION.md`.

## 1. Exact physical input and symmetry rotation

Let G be any finite bipartite graph with L sites, real spin-independent
nearest-edge hopping, and staggered sign s_i=+1 on one sublattice, -1 on
the other. All CAR are literal fermionic CAR. Set

    Hc = -J sum_(ij),sigma (c†_(i,sigma)c_(j,sigma)+h.c.)
         + U sum_i n_(i,up)n_(i,down) - (U/2) N.

The vacuum has energy zero. Define

    d_i† = c_i,up† c_i,down†,
    eta_i+ = s_i d_i†, eta_i- = (eta_i+)†,
    eta_iz = (n_i,up+n_i,down-1)/2,
    eta_iy = (eta_i+ - eta_i-)/(2i).

The global eta operators commute with Hc. Locally the empty and doubly
occupied states have the same centered interaction energy; the hopping
commutator cancels on each edge because s_i+s_j=0. Thus this holds on an
open graph too, not just a periodic lattice. This is Yang's established
eta symmetry, not a new identity.

Let R(theta)=exp(i theta sum_i eta_iy). The admitted initial ray is

    Psi_eta(theta)=R(theta)|vac>
       = product_i [cos(theta/2)+s_i sin(theta/2)d_i†]|vac>.

Its mean density is 2 sin²(theta/2), independent of L. This is the
established eta-coherent family, not a generic Hubbard equilibrium state
and not a fixed-particle-number eta-Dicke ray.

At site 0 with s_0=+1 apply the physical NUMBER-CONSERVING quench

    Hphys=Hc + epsilon(n_0,up+n_0,down-1).

Since R† eta_z R=cos(theta) eta_z+sin(theta) eta_x, its exact rotated
Hamiltonian, after an irrelevant scalar, is

    H'=Hc + epsilon cos(theta)n_0
             + epsilon sin(theta)(d_0†+d_0).

At theta=pi/2 the transformed state starts at vacuum and

    H'=Hc+epsilon X,   X=d_0†+d_0,   ||X||=1.                  (1)

Hc is kept fully interacting. U/J need not be small. There is no
Gaussianity assumption after evolution, no dephasing, no mixing,
no time averaging, and no gap or energy-level resolution in (1).

The physical density excess at the source rotates to X:

    <n_0(t)-1>_physical = <d_0†+d_0>_(H',vac).                 (2)

Eta_y at the source is unchanged by R, and has norm 1/2. It is a
secondary diagnostic requiring a phase convention. Equation (2) is
number conserving in the physical frame and is the primary output.

There is an exact superselection-compatible extension for this output.
Hphys and n_0 commute with N. Averaging the initial ray over its global
U(1) phase leaves (2) unchanged. The same density result therefore holds
for the mixed eta ensemble with binomial eta-Dicke weights
2^-L binom(L,q), q pairs. This is not a theorem for an individually
fixed q; it neither acquires that ensemble nor makes its preparation
free. Adding (U/2)N back to Hphys also leaves density predictions
unchanged, although it changes anomalous phase observables.

## 2. General graded input contract and projected DYNAMICS error

Let Hilbert space be a direct sum of nonnegative grades P_q. Assume

    [Hc,P_q]=0,
    P_q V P_r=0 if |q-r|>1,
    V=V†, ||V||<=1,
    psi_0=P_0 psi_0, ||psi_0||=1.

In (1), q=N_up=N_down, and V=X. Put P=P_0+...+P_K,
H_K=P(Hc+epsilon V)P, and phi_K(t)=exp(-itH_K)psi_0. All
spaces may be finite dimensional; the present proof makes no unbounded
Hamiltonian domain claim. Let z=|epsilon| |t| and

    R_m(z)=sum_(r=m)^infinity z^r/r!.

In the Hc interaction picture each V(t) still has norm <=1 and grade
bandwidth one. A Dyson term of order r has norm <=z^r/r! and cannot
reach grade >r. The same is true inside P. In particular

    ||P_K phi_K(s)|| <= R_K(|epsilon|s).                       (3)

There is NO factor two in the following state bound. The exact residual
of the embedded projected trajectory is

    (i d/dt-H)phi_K = -epsilon (I-P)V P_K phi_K.

Only grade K can leave P. Duhamel with the FULL unitary propagator and
(3) gives

    ||psi(t)-phi_K(t)||
       <= |epsilon| integral_0^|t| R_K(|epsilon|s) ds
       = R_(K+1)(z).                                         (4)

Thus (4) controls the error of projected dynamics, including excursions
that return from outside. A bound only on the final discarded
population would not prove (4). A difference of two unrestricted Dyson
tails would give a weaker factor-two argument and is not used here.

This is a bounded-source specialization of established quantum-number
truncation principles. Its source norm is the GLOBAL norm one, rather
than the weaker generic pair-creation estimate O(sqrt(q+1)).

## 3. Observable-sensitive return agreement

Suppose O has norm <=M and grade bandwidth b. Let O_K=POP. In the
interaction picture relative to Hc, O(t) has the same grade bandwidth
and norm. Expand the expectation as a double Dyson series, with r
insertions on the ket and s on the bra. Each term has norm at most

    M z^(r+s)/(r! s!).

Insert grade projectors between every operator. A surviving grade path
starts at 0, passes the O insertion, and returns to 0. If it visits
grade K+1 at any point, its V edges have total count at least

    m=2(K+1)-b.                                               (5)

Indeed, take a path from 0 to its first maximal grade and back: its
total grade variation is at least 2(K+1). V edges contribute at most
one each and the single O edge at most b. Therefore every term of
total order r+s<m agrees EXACTLY between full and projected dynamics.
For higher orders bound the difference by 2M, and use
sum_(r+s=n)1/(r!s!)=2^n/n!. Hence, for positive m,

    |<psi(t),O psi(t)> - <phi_K(t),O_K phi_K(t)>|
          <= 2M R_m(2z).                                     (6)

This is a selection-rule cancellation on closed observable paths. It
does not cancel phases statistically or require oscillatory integrals
to be bounded. The ordinary Dyson/particle-sector comparator has the
same access to it. No novelty of this generic argument is established.

For density excess in (2), M=b=1, so the error is
2 R_(2K+1)(2z). For eta_y it is half that. Diagonal number observables
have b=0 and start one order later. The connected Wick number printed
in the receipt is only a numerical diagnostic: no sufficient combined
error bound for a non-Gaussianity claim is acquired.

## 4. Exact native sparse compiler

Order all up orbitals before all down orbitals. The raw grade-q basis
has q occupied sites of each spin. Its dimension is binom(L,q)^2.
Hc in this basis is

    T_q tensor I + I tensor T_q
      + diag[U popcount(u & d)-U q].

Here T_q is the exact fermionic one-spin hopping matrix. A hop i<j
has sign (-1)^popcount(mask strictly between i and j).
The on-site source at site zero has raw sign (-1)^q. Rephase each
grade by beta_q=(-1)^(q(q-1)/2). The source coupling is then +1
between all admissible configurations. The Hamiltonian is still real
symmetric; no Jordan-Wigner boundary convention is omitted.

`check_native.py` constructs annihilation operators from the full literal
CAR, independently of the compiler's mask hopping formula. On the
2x2 graph it checks all 64 mixed CAR relations, the integer eta
commutator/algebra, and EVERY entry of the rephased source+Hamiltonian.
Its comparison of original and rotated exponentials is a binary64
diagnostic, not the proof of the rotation. The exact commutators and
Section 1 prove the general identity.

The finite-data receiver is `native.py`. At epsilon=1/20 all entries
of B=20(H_K+shift I) are integers represented exactly as binary64.
No numerical eigensolver, spectral window or small denominator enters.

For degree bound Delta_G and cutoff K, memory is O(D_K K Delta_G),
where D_K=sum_(q=0)^K binom(L,q)^2. Scalar propagation costs the
same factor times the number of polynomial matvecs. This is polynomial
in L for fixed K, with a potentially large exponent 2K. It is not an
efficient fixed-time thermodynamic-limit construction without also
paying spatial truncation; that interface is not acquired here.

## 5. Arithmetic error contract of the executed propagation

The numerical result is qualified in the standard binary64
round-to-nearest model, with no overflow. It is not a formal proof of
the installed SciPy or hardware. The compiler's integer values and
sparsity are exact. Sparse dot products are bounded by the standard
gamma_(2d) rowwise model, where d is maximal nonzeros per row; the
additional eight-operation margin covers scaling/division/sign work.
Subnormal absolute errors are covered by an added 10^-280 per step,
vastly larger than the number of underflow roundings times the smallest
binary64 subnormal in the executed finite problem.

Write gamma_n=nu/(1-nu), u=2^-53. Here B=B^T is real. Its absolute
matrix has row sum at most R, so ||B||_2 and || |B| ||_2 <=R. A step
with h=t/S uses a=hR/20 and Taylor degree p. Its exact polynomial
operator differs from the exact unitary by at most

    tau=exp(a) a^(p+1)/(p+1)!.

Let rho=gamma_(2d+8). Each computed Taylor recurrence term has norm
and error bounded using multiplication norm a(1+rho)/r. Relative to
the exact term, its error is bounded by
a^r[(1+rho)^r-1]/r! times the input norm. Summing and adding the
p+1-term summation error gives the local operator-action error

    delta <= tau + exp(a(1+rho)) [a rho+gamma_(p+1)] +10^-280.

This bound is homogeneous in the current vector norm, with the displayed
absolute underflow floor. The exact step is unitary. Telescoping S
computed steps therefore gives

    e_state <= S delta exp(S delta).

The harmless scalar shift contributes only a global phase. A final
norm-one observable reduction is bounded by

    e_num <= 2 e_state(1+e_state)
             + gamma_(16D_K+100)(1+e_state)^2.

The second term is a conservative sequential-double reduction bound
for the retained pair-map dot products and real extraction. All scalar
exponentials used to certify these bounds are enclosed by POSITIVE
exact Fraction series with a geometric remainder. JSON
`upper_fraction` fields, rounded upward to 45 decimal places, are
authoritative; `upper_float` is a convenience display.

## 6. Actual finite source and useful nonlinear distinction

The executed main source is the open 4x4 square Hubbard graph:

    L=16, J=1, U=8, epsilon=1/20, theta=pi/2, t=10, K=3.

These parameters do not shrink with volume in the theorem. This is
mean physical density one and strong interaction U/J=8. The reference
state is a highly special eta state, not an ordinary thermal half-filled
state. Mathematical state specification is supplied; its preparation,
model validation and physical units are unacquired.

The retained sector sizes are 1,256,14400,313600, total 328257. The
exact same balanced-spin full space would have 601080390 amplitudes;
that number is a storage comparison, NOT a performance comparison
against all tensor-network or symmetry-aware methods.

`PREDICTION.json` records 5405735 sparse entries, compiler time .1472s,
2160 matvecs, propagation 10.7656s, peak host RSS 654999552 bytes.
The 4x2 preview took .0831s of propagation; it was a cost/sign preview,
not withheld additional source data. The 2x2 exact-algebra consumer took
.0254s. No classical/quantum trajectory samples were used.

The main density prediction, rounded safely beyond all displayed
arithmetic errors, is

    -0.287100 < <n_0(10)-1> < -0.286193.                       (7)

The unrounded center is -0.28664650110600487, the norm-qualified
numerical error <1.923e-9, and the return-path error <.000452546.
The combined rational bound is <.000452548. These are finite-model
bounds, with the stated numerical arithmetic contract.

The strongest available LINEAR-response reduction is given exactly
the SAME Hubbard parameters, eta state and observable. Keep the full
two-particle Hc, and solve the unilateral triangular vacuum-to-pair
source. This is the exact first derivative in epsilon, with all U,J,t
dependence retained; no gap division is needed. `compare_linear.py`
computes this 257-amplitude problem in .0105s. Its density prediction
is -0.2955294195287588, numerical error <3e-11. The nonlinear and
linear predictions differ by more than .0084303 after qualification.
Thus the extra nonlinear sectors change this actual output, rather
than merely refining the established two-particle linear reduction.

The triangular generator is not Hermitian. Its anti-Hermitian source
part has logarithmic norm |epsilon|/2. The comparator charges the
propagator/input norms by exp(z/2), and a further conservative factor
for its final nonnormalised vector reduction. Its bound remains below
3e-11. `receive_result.py` takes a still safer 1e-9 comparator error
and performs all final interval subtraction in exact Fractions.

This is NOT evidence of superiority over a symmetry-aware nonlinear
particle-sector solver: that ordinary method is precisely the present
engine. Linear response is a limited target comparator, not the
strongest ordinary same-task algorithm.

## 7. Exact boundary: extensive sources and generic states

The LOCAL-source norm in Section 2 is essential. For the spatially
uniform physical quench epsilon(N-L), the rotated source is
epsilon sum_i s_i(d_i†+d_i)=2 epsilon eta_x. It commutes with Hc.
Starting at vacuum its defect number is EXACTLY

    q ~ Binomial(L, sin²(epsilon t)).                          (8)

At any fixed nonzero epsilon t not a multiple of pi, a fixed K
retains vanishing probability as L grows. The exact expression is
sum_(q=0)^K binom(L,q)p^q(1-p)^(L-q), which tends to zero for
0<p<1 (each term is polynomial times an exponentially small factor).
At p=1 the defect grade is exactly L, so fixed K<L retains zero mass.
Thus the fixed-defect representation does NOT solve spatially extensive
perturbations just because the input is eta coherent. This is a
representation failure, not a hardness argument: the uniform example
itself is a trivial exactly soluble global pseudospin rotation.

Likewise, generic finite-density initial states do not rotate to a
low-q seed. Arbitrary fixed-density eta-Dicke rays are not covered
individually by the vacuum rotation. No collision closure, Gaussian
closure, thermalisation or model learning is inferred from (7).

The surviving improved question is concrete: identify physically
qualified finite-density backgrounds with an exact/controlled
low-defect frame and a SUBEXTENSIVE symmetry-breaking source. Here
one such ideal mathematical interface is constructed and evaluated.
Whether it adds practical predictive capability over established
symmetry-aware methods remains NOT_ESTABLISHED.
