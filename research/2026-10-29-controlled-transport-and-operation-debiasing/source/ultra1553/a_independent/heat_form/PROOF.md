# Rational-angular compensation proves quasiconvexity of the original Hopf quartic

30 October 2026. This is a new mathematical construction in this private
programme, with exact arithmetic below. Independent review is in progress;
world priority, physical realization and practical material advantage are
not claimed. The strictly rank-one-convex/non-polyconvex source theorem is
the previously accepted `work/sol9_frontier_20261028/hopf/PROOF.md`, §§1–3,
with its independent review in `selector_opening/independent_hopf_review/`.
Those old sources are unchanged. The new result supplies the previously
unpaid quasiconvexity of that **same** literal energy.

## 1. Statement and target binding

For A=[[a,b],[c,d]], set

    T=a²+b²+c²+d², q=ad−bc, x=a²+c²−b²−d²,
    F(A)=T²+(252/25)q²+(99/25)qx.                  (1)

**Theorem.** For every bounded Lipschitz Ω⊂R², every A0∈R^(2×2), and
every φ∈W^(1,4)_0(Ω;R²),

    ∫Ω [F(A0+Dφ)−F(A0)] ≥ (1/900000)∫Ω |Dφ|⁴.    (2)

In particular F is quasiconvex on all real planar matrices. The accepted
source theorem proves F>0 away from0, strict rank-one convexity, and
failure of unrestricted polyconvexity at A0=diag(36,35). Thus (2) is a
quasiconvexity result for a smooth, positive, objective but anisotropic,
non-polyconvex quartic. It does not assert a negative compatible gap or
resolve unrestricted Morrey2×2. Rank-one convexity was an input of the
search, not a hidden premise needed for the new implication proof.

## 2. Compatible jets and the acquired exact identity

Use row-major coordinates A=(a,b,c,d). For six arbitrary real numbers h,
let

    B1=[[h0,h1],[h3,h4]], B2=[[h1,h2],[h4,h5]].    (3)

These are exactly the compatible derivatives ∂1Dv,∂2Dv of a map v. Let
J=[[0,−1],[1,0]] act on the output, so JB in row-major order is
(-B21,-B22,B11,B12). Put

    ν=102669769/1000000000000,  |ν|<1/1000,
    DνF=F''(A)[B1,B1]+F''(A)[B2,B2]
          +ν{F''(A)[B1,JB2]+F''(A)[B2,JB1]}.      (4)

The certificate supplies four homogeneous degree5 polynomials P_s(A)
and defines a one-form on A≠0 by

    α=Σ_(s=0)^3 [P_s(A)/T(A)] dA_s.              (5)

Every coefficient is a literal rational in
`RATIONAL_EXACT_CERTIFICATE.json`. Its `primitives` entries (s,e) and
matching `alpha` values specify P_s=Σ_e alpha_(s,e) A^e. No expression
evaluation, optimizer, or coefficient-conditioning oracle is required to
read them. All224 degree5 monomial one-forms were admitted in acquisition.

Let z be the120-vector of all A^e h_j, |e|=3, 0≤j<6, in the certificate's
literal `z` exponent order. The exact rational symmetric120×120 matrix Q
in the same certificate satisfies the universal polynomial identity

    zᵀQz = T² DνF + [T dP − dT∧P](B1,B2).       (6)

Here P=ΣP_s dA_s, so on A≠0 the bracket is T²(dα)(B1,B2).
This is an identity in all4+6 independent real variables. Restricting it
to the compatible jets (3) therefore imposes no extra unacquired field
equation or background assumption.

`qualify_rational.py` reconstructs the literal F, differentiates its sparse
polynomial dictionary, constructs both mixed terms in(4), and independently
differentiates the four P_s by their exponent lists. It checks every
coefficient of(6) exactly. It imports neither the symbolic map generator,
CVXPY, nor the optimizer's floating equality map. A small rational Gram
correction enforces the actual identity before positivity is checked.
The correction l1 is71659/12500000000000; this is implementation cost,
not a mathematical tolerance in(6).

## 3. Exact PSD qualification and coercivity

The verifier does not accept a floating eigenvalue. A rounded Cholesky
factor is only a proposal for a rational matrix L. Its integer entries
and denominator10^10 are included. Exact integer multiplication proves

    Q = (1/1000)I + LLᵀ + E,
    max_i Σ_j |Eij|
      =123436226613/10000000000000000000 <1/2000.  (7)

For symmetric E, its absolute row-sum bounds its operator norm (or use
2|v_iv_j|≤v_i²+v_j²). Hence

    Q ≥ (1/2000)I.                               (8)

No invertibility or rounding premise on L is needed for LLᵀ≥0. The exact
row sum, literal numerator identity and rational input binding can be
verified with standard-library integer/Fraction arithmetic.

The multinomial theorem has coefficients at most6 at degree3, so

    T³ ≤6 Σ_(|e|=3) (A^e)².

Dividing(6) by T² and using(8), for A≠0,

    DνF+(dα)(B1,B2) ≥ T|h|²/12000.               (9)

Also |B1|²+|B2|²=h0²+2h1²+h2²+h3²+2h4²+h5²≤2|h|².

## 4. Origin regularity and Stokes

Although α is rational, it is not singular as a real one-form at0.
Each coefficient P_s/T is homogeneous degree3 and smooth on the unit
sphere. For j=0,1,2 its jth derivatives away from0 are bounded by
C_j|A|^(3−j). Extending α(0)=0 gives a C² form, with derivatives through
order2 at0 equal0; differentiability follows recursively from those
bounds. Consequently ω=dα is C¹ on all of R4 and homogeneous degree2.
It vanishes at0. Inequality(9) extends there continuously.

For a smooth periodic map v(x)=A0x+φ(x), the map A=Dv is periodic. The
pullback A*α is a periodic C¹ one-form, and

    A*ω=d(A*α),  ∫_Q ω_A(∂1A,∂2A)=0.           (10)

Thus (9) gives a positive integrated dissipation. This is a genuine
globally exact angular correction; multiplying a variable scalar into
an ordinary null Lagrangian was never assumed to integrate away.

## 5. The actual smoothing flow and signs

Evolve only the periodic perturbation by

    ∂tφ=Δφ+2νJ∂12φ,  φ(0)=φ0.                  (11)

For a Fourier frequency ξ its symbol is
−|ξ|²I−2νξ1ξ2J. Since J is skew, every Fourier coefficient is a rotation
times e^(−t|ξ|²). The flow is a real, globally smooth, constant-coefficient
parabolic evolution. It preserves periodicity and the mean, and every
nonconstant derivative mode tends smoothly to0. It is an auxiliary proof
flow; no material dynamics, controller, or positive heat kernel is granted.

Write A_t=A0+Dφ_t and

    E_F(t)=∫_Q [F(A_t)−F(A0)].

For t>0 integration by parts gives

    E_F'(t)=−∫_Q DνF(A_t;∂1A_t,∂2A_t).          (12)

In particular the mixed term is not discarded: integrating the original
2νJ∂12 term in x1 gives2ν∫F''[B1,JB2], and integration in x2 gives
2ν∫F''[B2,JB1]. These two integrals agree. Their average is precisely
ν times the symmetric bracket in(4). Equation(10) then proves from(9)

    −E_F'(t) ≥ (1/12000)∫_Q T|h|².              (13)

Smooth convergence makes E_F(t)→0 as t→∞, so integrating already proves
the unquantified Jensen inequality. No long-time nonlinear closure is
required: the evolution is the explicitly solved linear flow(11).

## 6. Quantitative Jensen margin and full domain

Put G(A)=|A|⁴. Its Hessian has operator norm≤12|A|², hence for(3)

    |DνG|≤12(1+|ν|)T(|B1|²+|B2|²)
          ≤24(1+|ν|)T|h|².                      (14)

With κ=1/300000, equations(9),(14) and |ν|<1/1000 give
Dν(F−κG)+ω≥0 pointwise. The same flow and Stokes argument therefore
prove quasiconvexity of F−κG. The elementary uniform convexity estimate

    |A+X|⁴−|A|⁴−4|A|²A:X ≥ |X|⁴/3             (15)

follows by expanding its difference as
2[|A|²|X|²−(A:X)²]+6[A:X+|X|²/3]²≥0. Since the periodic mean gradient
vanishes, (15) gives(2) for smooth periodic perturbations.

For compactly supported smooth φ on Ω, extend it by0 into a periodic
box; its initial integrand vanishes outside Ω. This proves(2) without
any dynamical preservation of compact support. Approximate general
W^(1,4)_0 perturbations by compactly supported smooth ones. The quartic
difference bound C(|A|+|B|)³|A−B| and Hölder imply energy continuity,
so(2) passes to the claimed full class. There is no orientation,
invertibility, determinant sign, Fourier cutoff, or amplitude restriction.

## 7. Ordinary route, scientific increment and boundaries

The closest constructive predecessor is Bruno–Pasqualotto2608.06367v1,
§§2–3: heat-flow energy monotonicity with a globally exact matrix-space
two-form. Current pinned N794/N797 already use that method to prove
anisotropic quartic slices, including a strict9-coefficient QC/non-PC
neighborhood. N740 explicitly distinguishes pointwise algebraic
completion from globally closed selection; N794's later scalar-flow
separator excludes a related polynomial-correction/SOS class. None is
rebranded as an unresolved theorem or a newly invented general strategy.

The new construction admits the rational angular primitive(5). Polynomial
primitives, polynomial multipliers of a fixed cubic primitive, ordinary
constant-SPD flow proposals, output-skew polynomial proposals and finite
multi-flow decompositions did not provide a certificate for(1). These
floating failures are retained as failed acquisitions, not exact
nonexistence theorems. The rational primitive's **positive** exact identity
is what proves the new target. It supplies one complete operation in the
remaining compatibility problem, not arbitrary rank-one-convex quartic
inclusion or completeness of this rational ansatz for quasiconvexity.

The nearby passing control T²+12q²+(159/40)qx is deliberately not used as
evidence for(1). An equally informed ordinary polynomial minor-support
construction proves it actually polyconvex with stronger Jensen margin
1/400; `ORDINARY_PC_EXACT.json` records the exact26×26 certificate. That
ordinary route defeats the earlier possible advantage claim for the
control. The literal(1), by contrast, imports its accepted actual non-PC
certificate. No weak-source comparison or PC inference from failed search
is used.

The exact coefficient acquisition costs are reported separately from
verification: the rational SDP is a candidate generator, whereas its
verification is deterministic rational arithmetic. No experimental
material, device, physical stabilization or historical priority is
established. The original civilisation-level manufacturing/prediction
goal remains open; the acquired result is a mathematical stability
inequality beyond this input's polyconvex escape.
