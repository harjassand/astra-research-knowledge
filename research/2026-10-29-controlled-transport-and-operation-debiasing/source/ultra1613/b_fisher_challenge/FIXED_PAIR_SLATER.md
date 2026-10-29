# An explicit strict starting point for a fixed positive release

30 October2026. B's constructive strengthening of the independently reviewed
Fisher-unit-ball operation. This is derived separately from C's joint-design
theorem and uses the accepted conditional-Umegaki/free-form equivalence.
It is ordinary rational linear algebra plus an explicit CP construction,
not a claim of historical novelty or a new generic free Farkas theorem.

## 1. Input, output, and exact finiteness gate

Let `L` be ANY rational nonnegative column-stochastic `ell by n` channel,
after deleting identically zero output rows. Let the FIXED rational
column-stochastic `m by n` channel `K` be strictly entrywise positive.
Set `k=min_(y,i) K_yi>0`. Both channels share the same supplied raw
classical input boundary. The information quantity is the conditional
`J_A=D((A tensor id)rho||(A tensor id)sigma)-D(rho_R||sigma_R)`, only for
defined finite differences, not an uncentered contraction of reference
information.

**Proposition.** Its complete conditional comparison coefficient is finite
if and only if `K ker L=0`. When that gate holds there is an explicit
rational strictly feasible Choi/residual/c point for the FIXED-K SDP at a
computable finite `c0`. All dimensions and bit lengths are polynomial in
the channel matrix dimensions and rational input bit lengths. Consequently
the coefficient can be weakly optimized to additive rational precision
in polynomial Turing time using the ordinary weak-SDP machinery. Exact
boundary comparison and favorable numerical/physical conditioning are
not asserted.

Necessity is elementary and constructive. If `h in ker L` but `Kh!=0`,
column stochasticity gives `sum_i h_i=0`. Use scalar `Q_i=1/n` and `u_i=h_i`.
Then `F_L=0` and `F_K>0`. A rational `h` is acquired by exact linear algebra
when this gate fails. This is a kernel violation, not a finite ratio.
It also gives ordinary rational CLASSICAL hypotheses immediately: take
`p_i=1/n`, `q_i=p_i+t h_i`, with rational
`t=1/[2n max_i |h_i|]`. Then q is faithful, Lq=Lp and Kq!=Kp, so its
reference-free J_L=0<J_K. No reference-state search or logarithm evaluation
is needed to establish that strict divergence separation.

For sufficiency solve the consistent rational linear system

`K=D L`

for a possibly SIGNED `m by ell` matrix `D`. Such a solution exists exactly
when the kernel gate holds. No stochastic postprocessor is inferred and
no inverse of an arbitrary rectangular matrix is assumed. Gaussian
elimination on the actual input pays this factorization and its bit size.

## 2. A rational CP certificate without matrix square roots

Use C's source pencil with coefficient order `e=n+ell+1` and target order
`f=m+1`:

`A=diag(Q_i) direct_sum [[diag(LQ),LU],[(LU)*,I]]`,
`B_c=[[diag(KQ),KU],[(KU)*,cI]]`,

where `sum Q_i=I,sum U_i=0`; the `U_i` may be arbitrary complex operators.
Put

`S_yi=sum_z D_yz^2 L_zi`, `Smax=max_(y,i) S_yi`,
`a=k/[2(1+Smax)]`, `delta=k/4`, `c0=m/a+1`.

These are positive rational numbers. Each fill coefficient

`r_yi=K_yi-a S_yi-delta >= k/4`

is positive. Define CP maps by the following Kraus matrices `V:e by f`.
For each release output `y`, the arrow matrix `V_y` has

`(V_y)_(n+z,y)=sqrt(a) D_yz`,
`(V_y)_(e-1,f-1)=1/sqrt(a)`,

and all other entries zero. It contributes to `V_y* A V_y` the top entry
`a sum_z D_yz^2 (LQ)_z`, the off-diagonal `(D LU)_y=(KU)_y`, and bottom
entry `I/a`. Separately, for every `(y,i)` use `sqrt(r_yi) E_(i,y)` in the
first Q-block. It contributes `r_yi Q_i` only to target diagonal position y.

Summing these maps gives a CP map `Phi0` with the exact PENCIL identity

`B_c0 = Phi0(A)+diag(delta I_m,I)`.

This is a polynomial coefficient identity on arbitrary complex Q/U, not
only a pointwise scalar identity. It therefore includes the imaginary/skew
Z equations.

The square roots are used solely to prove positivity. They need not be
computed or supplied. With the convention
`C_(a,p),(b,q)=Phi(E_ab)_(p,q)`, each arrow Choi block is the rational
outer-product pattern

`[[a D_y D_y^T, D_y],[D_y^T,1/a]]`

on its sparse index set; the direct-Q terms add nonnegative rational
diagonal entries `r_yi`. Thus the full Choi matrix `C0` is explicitly
rational and PSD.

## 3. Full strictness and a fixed-K optimization box

Every source nonconstant coefficient has trace zero and its constant has
trace3. Therefore the CP map with Choi matrix `eta I_(ef)` adds only the
constant `3 eta I_f` to the pencil identity. Choose

`eta=delta/6`,
`C_start=C0+eta I_(ef)`,
`R_start=diag(delta I_m,I)-3 eta I_f`.

Then `C_start>=eta I>0` and
`R_start=diag((delta/2) I_m,1-delta/2)>0`. Since stochasticity implies
`k<=1`, no extra bound is needed for its final entry. The coefficient
equalities hold for the given FIXED K and `c=c0`.

Optimize c in the supplied box `[0,cmax]`, where `cmax=c0+1`. Its scalar
slacks at the starting point are also strict. Source definiteness gives

`a0=min{1/n,min_z (sum_i L_zi)/n,1}>0`,
`Tr C <=(1+cmax)/a0`, `Tr R<=1+cmax`.

After embedding the PSD blocks and c-slacks as block diagonal variables,
`eta/2` is a valid rational inner Frobenius radius IN the affine equality
space. The trace and scalar bounds give an explicit rational outer radius
about this displayed starting point. This uses the same geometric contract
as de Klerk--Vallentin Theorem1.1, rather than assuming a generic Slater
point exists or is known.

One literal outer radius is `2 B`, with
`B=(1+cmax)/a0+(1+cmax)+cmax`: the block variable consists of C, R,
and the scalar slacks c,cmax-c; its Frobenius norm is at most its trace,
which is at most B. The center obeys the same bound. The scalar/slack
minimum is at least eta, so `eta/2` is a valid inner radius. This avoids
an implicit Euclidean-coordinate condition number.

All rational output sizes are polynomial. Exact Gaussian elimination
produces D with polynomial bit length; squaring/summing at most ell entries,
taking a maximum, and performing the displayed positive rational divisions
preserve polynomial bit length. The numerical VALUES of cmax or the inverse
margin may be large, but their logarithms and the complete input/output
lengths are paid. This is not a strongly polynomial claim.

The weak-SDP algorithm then returns a feasible `c_hat` with
`C_cond<=c_hat<=C_cond+epsilon`; equivalently it supplies an additive
epsilon enclosure. No such new fixed-pair optimization is claimed executed
in this review. The explicit starting-point compiler is a separate finite
algebraic construction, not a fresh source/solver case.

## 4. Necessary boundaries

Strict positivity of the GIVEN K is load-bearing for this certificate's
fill and strictness. With zero entries, the exact inclusion SDP remains
valid, but this particular fixed-pair Slater construction is not supplied;
forced faces and infinite coefficients may occur. C's JOINT synthesis
still has its positive constant-release baseline even when its allowed
entry floor is zero. Do not conflate these different statements.

The finite kernel test is not a physical support/zero-certification method.
L/K and their rational coefficients are supplied, not estimated from a
sample. The signed factor D and the CP map between pencil coefficient
algebras are not physical degraders. One-use conditional-information and
raw-input access restrictions are retained. No correlated-block,
guessing/privacy, laboratory or practical-speed advantage follows.
