# Shared-bath design contrasts: exact obstruction and a thermal refinement

Integration-derived mathematics, 2026-10-13. Capital pin
`4025c5252f1ca992d3eae6ed422d6338ebe6c5a4`.
These are restricted internal deductions, not external correctness or priority
clearance. The source's finite-bath moment and causal Green arguments are the
explicit dependencies. Standard variational, Gibbs, CAR, Pinsker and Duhamel
tools are credited rather than claimed as new primitives.

## 1. Contract

Use the source's finite quadratic fermionic bath and grand-canonical impurity
energy/potential. Both designs have the **same impurity modes, coupling and bare
bath**, and differ only in their supplied even number-conserving impurity
Hamiltonians `H_A,0,H_A,1`. Write `Delta(Gamma)=F_1(Gamma)-F_0(Gamma)` at fixed
inverse temperature beta; the bare bath subtraction cancels. The zero-temperature
version uses the bath-subtracted ground energies. The bath spectral measure is
symmetric, and its acquired squared-energy moments give physical envelopes
`Gamma_l<=Gamma<=Gamma_h` in the source's Loewner sense. No canonical sector,
interacting-substrate reduction or physical spectral acquisition is inferred.

## 2. Individually extremal baths need not extremize the contrast

Take two uncoupled impurity channels, one absolute-energy band `[0,1]`, and
matrix moment data

    W=I_2, S=I_2/4.

In each channel the lower hybridization/upper-energy bath L has poles `+/-1/2`
with pair-total weight one. The upper hybridization/lower-energy bath H has a
zero pole of weight `3/4` and poles `+/-1` with pair-total weight `1/4`. Thus the
single-channel measures in `s=epsilon^2` are

    nu_L=delta_(1/4),
    nu_H=(3/4)delta_0+(1/4)delta_1.

Both have mass one and first s-moment `1/4`. The common-bath information class
also permits L in one channel and H in the other. This mixed bath does not
change the matrix moments, which remain exactly the displayed scalar matrices.

Choose designs

    H_A,0=10 n_1,  H_A,1=10 n_0.

Both all-L and all-H baths give `Delta=0`, since interchanging channels maps
the two full Hamiltonians unitarily. Denote by `e_x(B)` the normalized
single-channel ground impurity energy at impurity level x with bath B. For the
mixed bath `(H,L)`, the exact contrast is

    Delta(H,L)=e_10(H)+e_0(L)-e_0(H)-e_10(L)=R_0-R_10,
    R_x=e_x(L)-e_x(H)>=0.

For the free resonant level, elementary one-particle diagonalization gives

    e_0(L)=(1-sqrt(5))/2,
    e_0(H)=1-sqrt(2+sqrt(3)),
    R_0=sqrt(2+sqrt(3))-(1+sqrt(5))/2 > 11/40.

The last strict rational inequality follows from `sqrt(3)>17/10`, hence
`sqrt(2+sqrt(3))>19/10`, and `sqrt(5)<9/4`.

For either bath and any positive impurity level M, completing the square yields

    M d^dagger d+d^dagger Vc+c^dagger V^dagger d
      = M(d+Vc/M)^dagger(d+Vc/M)-c^dagger V^dagger Vc/M
      >= -Tr(V^dagger V) I/M = -I/M.

The normalized uncoupled bath Hamiltonian is positive, while the trial state
with the impurity empty and the bath in its reference ground state gives
`e_M<=0`. Therefore `-1/M<=e_M<=0`. Source monotonicity gives
`0<=R_10<=1/10`, and consequently

    Delta(H,L)>7/40>0.

Swapping the two bath channels gives `Delta(L,H)<-7/40`. The two source extremal
baths both give a tie although two other compatible **shared** baths give
opposite, strictly separated decisions. This refutes the named transfer
"evaluate the design difference at the single-design mean and endpoint baths
to obtain its extrema." It does not refute either source energy theorem or its
valid propagated comparison interval. In particular the source already
disclaims joint sharpness.

## 3. The universal one-radius contrast allowance is unavoidable

For one fixed impurity Hamiltonian the source gives
`F_ref,j-R<=F_j<=F_ref,j` with the same acquired bath envelopes. Thus

    |Delta(Gamma)-Delta(Gamma_l)|<=R_beta.

The allowance cannot be made uniformly smaller solely because the bare bath
is shared. Take one design to be the free resonant impurity, which attains
the source width, and let the other have all impurity levels M tending to
positive infinity. For finite bath dimension at zero temperature the square
bound above gives a width tending to zero. At fixed finite beta the same
conclusion follows from the one-particle block matrix `[[M I,V],[V^dagger,h]]`.
For bounded z its Schur determinant is

    det(z-M I) det[z-h-V^dagger V/(z-M)],

so its bounded eigenvalues converge, counting multiplicity, to those of h;
the remaining impurity eigenvalues tend to positive infinity. The continuous
single-level free-potential function `-beta^(-1)log(1+exp(-beta e))` then makes
the bath-subtracted free potential tend to zero. The design
contrast error therefore approaches the full resonant width. This is a
worst-case sharpness statement across design Hamiltonians, not a claim that
every fixed pair attains that radius.

Scalar shifts in either design do not change this uncertainty. More elementary
pair-specific information can already help: if

    delta=min_c ||H_A,1-H_A,0-cI||_op,

then variational/Loewner bounds give `|Delta(Gamma)-Delta(Gamma_l)|<=2delta`.
The minimum is half the spectral diameter of the supplied design difference.
Both this bound and the source radius can be used, taking their minimum.

## 4. A contrast-sensitive finite-temperature bound without a correlated solve

Assume `0<beta<infinity`. Set `X=H_A,1-H_A,0-cI` and acquire any certified
`delta>=||X||_op`. Define fermionic Matsubara frequencies and positive matrices

    omega_n=(2n+1)pi/beta,
    A_l(omega)=omega I+Gamma_l(omega),
    A_h(omega)=omega I+Gamma_h(omega),
    L(omega)=log det A_h(omega)-log det A_l(omega)>=0,
    xi(omega)=min{1,
       delta(2beta+4/omega)(1+||Gamma_h(omega)||_op/omega)}.

Then every compatible shared quadratic bath obeys

    |Delta(Gamma)-Delta(Gamma_l)| <= C_beta,
    C_beta=(2/beta) sum_(n>=0) xi(omega_n)L(omega_n)
            <= R_beta.                                      (1)

One may take the minimum of `C_beta` and `2delta`. All quantities in (1)
involve the supplied local design difference and one-particle envelope matrices;
no correlated state, self-energy or Green-function evaluation is an input.
The reference **value** Delta(Gamma_l) still needs an appropriate certified
correlated calculation, exactly as in the source.

### Gibbs trace-distance lemma

For any finite H and `||X||<=delta`, let rho_0,rho_1 be the Gibbs states of
H and H+X at the same beta. Writing `r=||rho_1-rho_0||_1`, the Gibbs identity is

    D(rho_1||rho_0)+D(rho_0||rho_1)
      = beta Tr[X(rho_0-rho_1)] <= beta delta r.

Quantum Pinsker gives each relative entropy at least `r^2/2`; hence
`r<=beta delta` (the zero-r case is immediate). For reference, Pinsker follows
by applying relative-entropy data processing to the Helstrom two-outcome
measurement and classical binary Pinsker. The latter follows by integrating
the binary divergence's second derivative `1/[p(1-p)]>=4` around its minimum.
This is standard entropy mathematics, not a new information primitive.

### Green-function difference lemma

Let `G_j(iomega)` be the exact impurity retarded analytic Green matrix in these
Gibbs states, and `M_j=-Im G_j`. For every normalized field `a=u^dagger d`,
the CAR gives `||a||=1`. The retarded Laplace formula is

    u^dagger G_j(iomega)u
      = -i integral_0^infinity exp(-omega t)
             Tr[rho_j {a_j(t),a^dagger}] dt.

Changing the state contributes at most `2r` to the integrand. Duhamel's formula
and `||X||<=delta` give
`||a_1(t)-a_0(t)||<=2delta t`; its anticommutator contributes at most
`4delta t`. Integrating and using the Gibbs lemma proves the Hermitian bound

    ||M_1(iomega)-M_0(iomega)||_op
       <= q(omega)=delta(2beta/omega+4/omega^2).              (2)

The source causal bound gives `0<=M_j<=A^(-1)`, where
`A=omega I+Gamma`. Therefore, with `D=M_1-M_0`,

    -A^(-1)<=D<=A^(-1),
    ||A^(1/2) D A^(1/2)||<=min{1,q(omega)||A||}.

When `Gamma<=Gamma_h`, the final quantity is at most the displayed xi.

### Integrating the shared-bath contrast

Interpolate a true compatible bath with the reference by
`Gamma_t=Gamma_l+tK`, `K=Gamma-Gamma_l>=0`. A common physical direct-sum bath
realizes this path for **both** designs. Their full Hamiltonian difference
remains exactly X plus its scalar part throughout. The source derivative
identity gives

    dDelta/dt=-(2/beta) sum_n Tr[K(omega_n)(M_1,t-M_0,t)].

For any PSD K the preceding normalized Hermitian inequality implies

    |Tr(KD)|<=xi Tr(K A_t^(-1)).

Integrating t turns the last trace into
`log det(omega I+Gamma)-log det A_l`, which is at most L(omega).
Summing proves (1). Positive beta and finite baths justify absolute convergence;
the envelope domination also supplies the source controlled continuum limit
when that limit exists under its bounded-bandwidth, finite-weight contract.

### An explicit improvement regime and a computable tail

If `W_total` is total pair coupling weight, then
`||Gamma_h(omega)||<=||W_total||/omega`. Thus

    xi(omega_n)<=min{1,
      beta delta(2+4/pi)(1+beta^2||W_total||/pi^2)}.

When the second expression is below one, (1) uniformly improves R_beta by
that factor. The guarantee is most useful at high temperature and for a small
design difference. It makes no useful uniform zero-temperature claim: beta
diverges, and the proof reverts to the source radius.

For exact source-style equal-moment bins `[a_b^2,b_b^2]`, normalize by the
factor L_b. The scalar chord gap is exactly

    ((B-a_b^2 I)(b_b^2 I-B)) /
    ((omega^2+a_b^2)(omega^2+b_b^2)(omega^2 I+B)).

It follows that `L(omega)<=C/omega^6`, with
`C=sum_b Tr(W_b)(b_b^2-a_b^2)^2/4`. Consequently the tail from n=N>=1 is
bounded by

    (2/beta) C (beta/(2pi))^6 / [5(N-1/2)^5].

The same bound applies to C_beta because xi<=1. General acquisition envelopes
with different total masses instead need their own slower asymptotic tail
budget; the equal-moment tail must not be imported there. Matrix square roots,
logarithms, spectral norms, summation and pi must be evaluated with outward
precision if a machine-rigorous numerical certificate is claimed.

## 5. Relationship to current capital and remaining gates

N775's task-operator cancellation motivates asking for the actual design
contrast rather than a full-system error norm; it does not supply the Green
bound above. The finite-temperature Gibbs identity is compatible with N779,
but (1) has a genuinely quadratic spectral input contract instead of an
arbitrary common K and local UCP witness. Neither theorem acquires the other's
inputs. N778's fixed-charge repair remains relevant as an explicit warning:
number conservation does not turn these grand-canonical results into fixed-N
reaction energies.

The exact shared-bath falsifier identifies a new obstruction to blindly reusing
single-design extremizers. The thermal refinement partially repairs it in a
precise regime with a computable local contract. Neither establishes practical
chemical superiority. Required gates remain: external proof review and priority
search; acquired Hamiltonian and matrix spectral moments; non-Gaussian/model
error bounds; certified reference solvers; physically relevant temperature and
design margins; and matched strongest-method total-cost comparisons.
