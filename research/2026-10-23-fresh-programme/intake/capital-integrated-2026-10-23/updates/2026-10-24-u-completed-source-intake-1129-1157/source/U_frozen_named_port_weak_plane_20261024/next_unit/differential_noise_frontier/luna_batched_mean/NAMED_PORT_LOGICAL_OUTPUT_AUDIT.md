# Named-port operation: logical/output audit

Scope: the projected signal and added-control contributions in
`../NAMED_PORT_WEAK_PLANE_OPERATION.txt`, under its stated moving-frame
identities and actual sample-plus-meter trace/reset. This is a bounded
operator-order check, not a verification of the population comparison
barriers, the physical port implementation, or the completed-operation
theorem.

## Projected logical signal

With syndrome basis `(C,D)`, the projected Hamiltonian `P V P` is diagonal in
logical `X`. For its two logical eigenvalues `s=+1,-1`, the syndrome matrix is

```text
s * [[ 2 A E/n^2,                  A E (1-2z)/(n^2 sigma) ],
     [ A E (1-2z)/(n^2 sigma),    -2 z(1-z) A E/(n^2 sigma^2) ]].
```

The extra named-port control has `K_PP=0` and `K C=0`, so it adds no direct
logical Hamiltonian in the transported plane and does not alter the
first-order `C`-branch phase. Since the reset acts on sample and meter only,
the reduced logical output is invariant under that trace-preserving reset;
orthogonal `C,D` coherences are traced, not coherently identified. Thus the
`C,D` off-diagonal signal term is not a first-order logical rotation. It
produces an off-syndrome amplitude, whose squared contribution is of higher
order after the trace. This conclusion uses the actual syndrome-trace
instrument; it would fail for a hypothetical coherent map that erased the
syndrome label.

For `beta=h^4`, `a0=h^8`, `e0=h^9`, `delta=d0 h^2`, and the fixed
nonnegative bump `f`,

```text
z = -h^8 f^2 + O(h^16),
sigma = h^4 f (1+O(h^8)),
M_CC = 2 h^17 f^4 + O(h^25).
```

The first-order relative phase over a cycle is therefore
`4 g d0 h^19 integral_0^1 f^4 ds + O(h^27)`. It is nonzero for a
nonzero nonnegative bump. The projected signal remains order `h^19`.

## Added-control output terms

The exact identities `N C=0`, `N D` orthogonal to both `C,D`, and
`C^dag N D=D^dag N D=0` imply `K C=0` and `K_PP=0` in the broad mathematical
frame. The only first-order trace contribution from `K` is consequently from
its off-plane coupling to the `D` direction, plus its `Q-Q` block. Using the
lead's stated bounds,

```text
v0 integral_0^delta ||Y_Qb(t)||_1 dt
 <= C [a0 v0 beta delta^(5/2) + v0^2 beta^2 delta^3].
```

At the proposed scales `v0=e0/(beta delta)=O(h^3)`, both terms are `O(h^20)`:
their powers are respectively `3+8+4+5=20` and `6+8+6=20`. The `Q-Q`
contribution is smaller under the stated `q(t)` barrier: `v0 integral q(t)dt`
has order `h^25`. There is no `K` contribution involving `C`, because `K C`
vanishes exactly. Hence this added-control trace term does not cancel the
`h^19` signal or introduce an order below the claimed `h^20` remainder.

The first-error signal coupling also remains consistent with the bound: its
integrated `C-D` amplitude is `O(h^15)`, and the named-port `D-Q` control can
convert it to an `O(h^20)` off-plane amplitude over a cycle. The actual
syndrome trace removes its linear interference with the code branch. This
check does not establish the uniform trace-norm estimates in the lead file;
it only verifies their displayed powers and identifies where the syndrome
trace is used.

## Finding and open gates

I found no additional lower-order logical phase or g-independent logical
noise term from the named-port correction, conditional on the exact frame
identities, the displayed `Y_Qb`/`q` bounds, and the sample-plus-meter
trace/reset. The newly introduced logical-output contribution is order
`h^20`, matching the proposed per-cycle remainder, while the projected
useful phase is order `h^19`.

Still needed for the full claim: independently establish the endpoint
quotient/control bounds and the simultaneous population and cross-block
barriers; verify finite-rate cleanup/reset and charge its errors; and bound
all remainders uniformly over the allowed coupling interval. No acquisition
advantage or hardware implementation is established here.
