# Inverse stability with a bounded cumulative residual

**Separate deterministic addendum; the scalar numerical freeze is unchanged.**
This lemma improves the total-variation perturbation interface in `PROOF.md`.
It changes none of the numerical certificate, startup, quadrature, or tail.

Let `f(v,x)=1/[2(x+3v²/4)²]`. Work on a common finite interval `[a,E]`
in a domain where all displayed denominators are positive. Let `s` solve
`s'=f(v,s)`, and suppose a measurable path `ŝ` satisfies the **exact** identity

    ŝ(v)=ŝ(a)+∫_a^v f(u,ŝ(u))du+R(v),
    R(a)=0,  sup_[a,E] |R| <= epsilon,

with an integrable drift. No differentiability or finite variation of `R` is
required. In particular, the deterministic assertion permits a càdlàg
martingale sample path, if the stated equation and bound have actually been
proved on that path.

Put `delta0=ŝ(a)−s(a)` and `q(v)=ŝ(v)−s(v)−R(v)`. Then `q` is absolutely
continuous and

    q'=f(v,ŝ(v))−f(v,s(v))       almost everywhere.

Since `f` decreases in its second argument, on `{q>epsilon}` we have
`ŝ−s=q+R>0`, hence `q'<=0`. On `{q<−epsilon}` the reverse inequality gives
`q'>=0`. Apply the absolutely-continuous positive-part chain rule at the
barriers `max(delta0,epsilon)` and `min(delta0,−epsilon)` to obtain

    min(delta0,−epsilon) <= q(v) <= max(delta0,epsilon).

Therefore the uniform endpoint bound is

    sup_[a,E] |ŝ−s| <= max(|delta0|,epsilon)+epsilon
                       <= |delta0|+2epsilon.                 (A)

There is no positive Gronwall exponential and no total-variation charge.
The coefficient two is not an independence assertion: the same residual
enters the integral feedback and the displayed path value.

More precisely, if `r_minus<=R<=r_plus` with `r_minus<=0<=r_plus`, then

    min(delta0,−r_plus)+r_minus <= ŝ−s
        <= max(delta0,−r_minus)+r_plus.                       (B)

For matched initial data, (B) gives an error at most the residual oscillation
`r_plus−r_minus`. A symmetric bound `|R|<=epsilon` recovers `2epsilon`.

## The stochastic operation still owed

This is a deterministic stability lemma, not a finite-N clearance theorem.
The count `E` is not monotone. An actual-chain argument must construct a valid
inverse coordinate (or another representation that really has the equation
above), bound its domain and entry error, identify and charge every residual
and jump term, and prove a simultaneous residual-supremum event. Ordinary
martingale inequalities could then be used **on that earned residual** in (A),
without converting a martingale supremum into total variation.

After a finite level, the remaining deterministic tail and the stochastic
continuation to macroscopic service must still be charged. The frozen scalar
certificate provides the deterministic target but not those interfaces.
