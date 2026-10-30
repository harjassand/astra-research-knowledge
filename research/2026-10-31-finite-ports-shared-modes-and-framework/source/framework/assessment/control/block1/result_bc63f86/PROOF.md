# A quantitative barrier for repeated weak native words

This is a restricted-family obstruction, **not** an impossibility theorem
for every program in `CONTROL_NEXT_SCOPE.md`. It identifies a failure of
transferring the older high-degree flat-word construction to arbitrary
time-dependent first-motion baths. All trace errors here are full trace
norms, without a factor of one half.

## 1. Statement

Let a fixed finite native word have normalized duration `D`, piecewise
constant real controls `f_A,f_B,f_C`, at most one nonzero at any time,
and `|f_j|<=1`. Its physical duration is `D delta`. Suppose:

1. Every handle is used on positive measure and has zero signed integral.
2. At zero drift its first and second Taylor coefficients vanish, for
   every gain triple in `[1,2]^3` and the allowed global native sign
   variants. In particular this holds for flat commutator words whose
   leading pure-control degree is any `k>=3`.

There are constants `gamma>0` and `delta_0>0`, depending only on the fixed
word, with the following property. For every `0<delta<=delta_0` and every
finite integer `N`, an admitted **fixed, private-coin-independent** bath
and an initial state exist such that repeating the word `N` times has
reduced-data trace-norm error at least

\[
\boxed{1-\exp(-\gamma N\delta^4)}
\tag{1}
\]

relative to `E=exp(-i pi Z_1 X_2/4)`. The controller may use arbitrary
private choices of global native polarities in different repetitions;
the estimate is uniform in those choices and survives averaging them.
It is also uniform in the static gain box.

The same lower bound holds if the repeated block is surrounded by any
native prefix and suffix, with the adversarial bath set to zero outside
the block. No later native control can recover the lost information.

In particular, a leading degree-`k` primitive repeated
`N=Theta(delta^-k)` to obtain a nonzero gate angle fails for every fixed
`k>=5`: the lower bound tends to one. The known degree-three construction
has `N delta^4=O(delta)` and is consistent with this theorem.

The fixed-shape assumption matters. This does not exclude schedules whose
entire shape changes with accuracy, other synthesis methods, or the full
unknown-gain target.

## 2. Six admissible drift profiles

Write the three mediator axes as `x,y,z`, and the data factors as

\[
P_A=X_1,\qquad P_B=X_2,\qquad P_C=Y_1.
\]

Define primitives `F_j(x)=integral_0^x f_j(y)dy` on `[0,D]`. They vanish
at both endpoints. Choose a target handle `j` and a different mediator
axis `k`. Of the remaining handles, exactly one, denoted `l`, also fails
to commute with `sigma_k`.

There is a bounded real profile `h_{jk}` such that

\[
\int h_{jk}=0,\quad\int h_{jk}F_l=0,\quad
\mu_{jk}:=\int h_{jk}F_j>0,\quad \|h_{jk}\|_\infty\leq1/2.
\tag{2}
\]

Here all integrals are on `[0,D]`. One construction is to take the
`L^2` residual `r=F_j-Proj_span{1,F_l} F_j` and put
`h=r/(2||r||_infinity)`. The residual is nonzero: otherwise differentiating
would give `f_j=constant*f_l` almost everywhere, impossible because their
supports are disjoint and `f_j` is nonzero. Orthogonality gives (2), with
`mu=||r||_2^2/(2||r||_infinity)>0`. These profiles are finite piecewise
affine functions. For equal-segment words, projection on the averages
of the primitives in half-segment cells instead gives exact rational
piecewise-constant profiles; the code uses that equivalent construction.

Use all six ordered choices `j,k`, `j!=k`. In a cycle labeled by `(j,k,b)`
with `b=+1/-1`, the bath on the mediator is

\[
H_{jk,b}(t)=b h_{jk}(t/\delta)\sigma_k.
\tag{3}
\]

It has norm at most `1/2` and every local Pauli commutator has norm at most
one. Its free evolution over the cycle is exactly the identity, since its
axis is fixed and its integral is zero. Its time dependence has scale
`delta`, which is allowed by the first-motion promise.

## 3. The second-order error of one realization

Fix the controller's global signs `s_j`. The complete first-order integral
of the controlled Hamiltonian plus (3) is zero. At second order, the
control-control term vanishes by hypothesis, and the bath-bath term
vanishes because its axis is fixed and its integral is zero.

The mixed Magnus coefficient for handle `j` is

\[
s_j b g_j[P_j\otimes\sigma_j,\sigma_k]
                   \int h_{jk}(x)F_j(x)\,dx.
\tag{4}
\]

For example, the time-ordered scalar integral is

\[
\int_{x>y}(f_j(x)h(y)-h(x)f_j(y))\,dy\,dx
 =-2\int hF_j,
\]

where endpoint terms vanish. The other affected handle contributes zero
by (2), while the handle along `k` commutes with the drift. Therefore

\[
U_{s,jk,b}(\delta)=I+\delta^2 b L_{s,jk}+O(\delta^3),
\quad
L_{s,jk}=\pm2i s_jg_j\mu_{jk}Q_{jk}.
\tag{5}
\]

The six Hermitian Pauli operators `Q` are

\[
X_1\sigma_y,\quad X_1\sigma_z,\quad
X_2\sigma_x,\quad X_2\sigma_z,\quad
Y_1\sigma_x,\quad Y_1\sigma_y.
\tag{6}
\]

Their exact signs in (5) are irrelevant to the following norm estimate.
Their data factors are nontrivial: this is actual data decoherence after
the independent bath label is ignored.

## 4. A dimension-eight contraction estimate

For the moment average the twelve labels `(j,k,b)` independently and
uniformly, retaining the data and mediator. For fixed controller signs,
let `T_s` be this random-unitary channel on their eight-dimensional joint
space. It fixes both `I` and `X_2` exactly, since every native Hamiltonian
and bath Hamiltonian commutes with `X_2`.

Work in Hilbert-Schmidt operator space and let

\[
\mathcal C=\operatorname{span}\{I,X_2\}^{\perp}.
\]

This subspace is invariant under the channel and its adjoint. The only
operators commuting with all six Paulis in (6) are `span{I,X_2}`. Indeed,
products of the A-noise pair and the B-noise pair generate all mediator
Paulis, forcing a commuting operator to have mediator identity; the
remaining conditions force data factor `I_1` and second-qubit factor
`I_2` or `X_2`.

Pauli orthogonality makes the following quantitative form immediate:

\[
\sum_{j\ne k}\|[Q_{jk},X]\|_2^2\geq4\|X\|_2^2,
\qquad X\in\mathcal C.
\tag{7}
\]

Each Pauli basis vector outside the common commutant anticommutes with
at least one `Q`, contributing `4` times its squared norm.

For `delta<=1/(5D)`, the full Hamiltonian has norm at most `2.5`; its
commutator generator on Hilbert-Schmidt space has norm at most `5`.
The Dyson remainder after second order is bounded by

\[
C_3\delta^3,\qquad C_3=e(5D)^3/6.
\]

Thus (5) gives, in induced Hilbert-Schmidt norm,

\[
\operatorname{Ad}_{U_{s,jk,b}}
 =I+\delta^2 b\mathcal A_{s,jk}+R_{s,jk,b},
\quad\|R_{s,jk,b}\|_{2\to2}\leq C_3\delta^3,
\]

where `A(X)=[L,X]`. Put `mu_min=min mu_{jk}` and
`beta=(8/3) mu_min^2`. Gains are at least one, so (7) implies

\[
\mathbb E_{jk,b}\|\mathcal A_{s,jk}X\|_2^2
\geq\beta\|X\|_2^2,\qquad X\in\mathcal C.
\tag{8}
\]

For `Y=Ad_U X`, the exact Hilbert-space variance identity says

\[
\|T_sX\|_2^2=\|X\|_2^2-\mathbb E\|Y-\mathbb EY\|_2^2.
\]

The mean of the order-two term is zero because `b` is fair. The inequality
`||a+b||^2 >= ||a||^2/2-||b||^2` and the remainder bound yield

\[
\mathbb E\|Y-\mathbb EY\|_2^2
\geq(\tfrac12\beta\delta^4-4C_3^2\delta^6)\|X\|_2^2.
\]

Choose, explicitly,

\[
\delta_0=\min\left\{\frac1{5D},\frac{\sqrt\beta}{4C_3},
                              (4/\beta)^{1/4}\right\},
\qquad\gamma=\beta/8=\mu_{\min}^2/3.
\]

Then for every controller sign variant,

\[
\boxed{\|T_s|_{\mathcal C}\|_{2\to2}
\leq \sqrt{1-\beta\delta^4/4}
\leq e^{-\gamma\delta^4}.}
\tag{9}
\]

This argument does not assume that the averaged unitary is the averaged
channel. Its contraction is precisely the variance of unitary channels.
Nor does it need to cancel or even identify higher coherent error terms.

## 5. Realizing independent bath labels within the original contract

The label average above is one legal deterministic bath with a legal
initial state, not a new noise oracle. Give the spectator `N` registers,
each with twelve orthogonal basis states. Initially place them in the
product uniform classical mixture. During cycle `i`, use the fixed
block-diagonal Hamiltonian

\[
H_M(t)=\sum_{j\ne k,b}|j,k,b\rangle\langle j,k,b|_{L_i}
               \otimes b h_{jk}((t-t_i)/\delta)\sigma_k.
\tag{10}
\]

Every other label register is untouched during that cycle; past registers
are never used again. This finite-dimensional Hamiltonian has norm at most
`1/2` and satisfies all three local-motion bounds. It is completely fixed
from the public word and does not use the private controller signs or
initial data. The label mixture is independent of those signs and data.
Its spectator dimension is `12^N`, finite for each finite program.

Discarding a retired label produces `T_s`; independence of the initial
label registers gives chronological composition of these maps. For any
fixed complete private-sign history, (9) composes to contraction
`exp(-gamma N delta^4)` on `C`. Averaging over histories cannot enlarge
that norm. No memory reset, measurement, or physical bath-randomness
assumption was supplied to the controller.

## 6. A reduced-data error witness and irreversibility

Let `F=Z_1X_2 tensor I_mediator`, and take initial data and mediator state

\[
\rho_{Dm}=(I+F)/8.
\]

Its data state is the normalized projector onto the `+1` eigenspace of
`Z_1X_2`; the mediator is maximally mixed. The target gate preserves that
state and its expectation of `F_D` is one.

The actual output expectation is at most

\[
\frac1{8}\|F\|_2\|T(F)\|_2
\leq e^{-\gamma N\delta^4}.
\]

Duality with the norm-one data observable `F_D` proves (1). No reference
is needed for this witness; failure on this input already rules out the
required diamond guarantee for this schedule family.

A native prefix or suffix also fixes `I,X_2` and contracts
Hilbert-Schmidt norm. Set the bath to zero there, so it acts only on data
and mediator and cannot revisit retired labels. The same argument bounds
the final `F` expectation regardless of those surrounding operations.
Thus later polynomial-compensation factors cannot undo a contraction
already incurred inside a high-degree primitive block.

## 7. Application and exact remaining scope

The predecessor supplement constructs pure-control monomials such as
`c*g_A^2 F` at degree five and `c^3 F` at degree nine, then compensates
unknown positive chirality by an odd polynomial. Its stronger regularity
hypotheses permit the required high-order flat-word remainders.

For a fixed such word, gaining a finite coefficient requires
`N delta^k` bounded below. Under (10), its unavoidable contraction exposure
is then `N delta^4`, which diverges for `k>=5`. This defeats the direct
repeated weak-word transfer even with private global sign projection,
known gain orientation, and arbitrarily small native segments.

The theorem does not establish that every possible gain-compensating
program must contain such a block. It supplies no general lower bound
for accuracy-dependent word shapes, correlated internal sign designs,
nonperturbative protocols, or any other unrestricted native schedule.
The full unknown-static-gain first-motion question remains unresolved.
