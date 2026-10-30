# Unknown-gain first-motion continuation

The full unknown-static-gain entangler remains unresolved. This tranche
establishes two constructive barriers to extending the known-gain result,
and an action lower bound applying to all randomized native programs.
The main artifact is a fully specified admitted bath that defeats the
standard higher-order gain-polynomial refinement, including a finite
rational certificate. This is mathematical progress at the stated scopes;
it is neither an all-policy negative resolution nor a positive gate compiler.

## What is proved

1. **Commuting cubic macros cannot compensate unknown gains.** Any randomized
   composition of clean logical calls `exp(-i theta g_A g_B g_C F)` has
   worst-box diamond error at least `0.3251252956`. The proof uses just the
   admitted gain triples `(1,1,1)` and `(2,1,1)` and the unit-circle moment
   inequality `|E z^2-(E z)^2|<=1-|E z|^2`. Arbitrarily refining the supplied
   cubic implementation does not remove this error floor.

2. **Fixed higher-order words have a first-motion noise obstruction.** For
   any fixed zero-area native profile with vanishing frozen first and second
   coefficients, apply fresh even private signs per repetition. A public,
   coin-independent bath `H_M(t)=h(t/d) Z_M/2`, with `|h|<=1`, gives
   `Phi^*(Z1)=(1-2g_A^2 mu_A^2 d^4)Z1+O(d^5)`, where
   `mu_A=-integral |integral_0^t f_A|dt !=0`. Consequently a clean signal of
   degree `k>4`, repeated with `N d^k` fixed, has target trace-norm error
   tending to at least one. The bath uses only a qubit and norm at most 1/2;
   it satisfies every first local-motion bound. Its bandwidth grows under
   refinement, as allowed by the problem. A fixed finite composition of such
   higher-order macros and clean cubic macros inherits this obstruction.

3. **Every randomized program pays an action cost.** Let A be its native
   action, possibly with unbounded private support but finite almost surely.
   For any uniform gain-box error epsilon,
   `epsilon >= (1/(64 rho^4)) E exp(-C A)`, with
   `rho=3+2sqrt(2)` and `C=16e log(rho)+1`.
   Thus finite expected duration must grow at least logarithmically in
   `1/epsilon`, and exact gain-uniform implementation is impossible even for
   almost-surely finite programs with infinite expected duration. This
   extends the supplied analytic gain argument to randomized action tails;
   it does not preclude approximation with growing finite resources.

## The explicit hard test

The tested word is the standard degree-five nested-commutator construction,
followed by its chronological reverse to make a 92-segment palindrome.
It is not claimed as a new word or a new general gain-polynomial mechanism.
Its frozen leading term is

`I-32i g_A^3 g_B g_C d^5 Z1X2`.

Every handle has zero area and zero first moment. The adversarial waveform
is generated from the cumulative A profile, so it is fixed independently of
the realized private signs. It has zero net bath rotation per cycle.
Exact Gaussian-integer calculations find `mu_A=-130` and

`Phi^*(Z1)=Z1-33800d^4 Z1+(16701716/3)d^6 Z1`
`              -(1425644383/6)d^8 Z1+O(d^10)`.

This is channel variance, measured on returned data. A mean-unitary argument
would miss it. A bath that is static throughout a palindrome also misses
this leading obstruction; first-moment cancellation therefore does not
supply the missing uniform arbitrary-time guarantee.

At unit gains, `d=1/1000` and
`N=24,543,692,606,171` repetitions, rational certificates give:

| Same finite native program | Certified channel error from E |
| --- | ---: |
| Zero bath | at most `0.00001466109` in diamond norm |
| Constructed admitted moving bath | at least `0.9999778781` in trace norm on a data witness |

The program has 2,258,019,719,767,732 native segments and duration
2,258,019,719,767.732. Both bounds include all private records through the
appropriate averaged-channel or recordwise statement. The moving-bath
lower bound holds for every initial memory state with Z1=+1 data, so no
memory preparation resource is being granted to the controller. Norms here
are unhalved. These large finite resources certify a route failure, not a
useful controller.

## Evidence and boundaries

`PROOF.md` supplies the analytic derivations, explicit constants, finite
certificate remainder bounds, and exact scope restrictions. Run

`python3 check_barrier.py`

from this directory to regenerate `CHECKS.json` and print the checks.
`CHECKS.txt` records the completed execution. The exact checks use only the
standard library. Optional NumPy diagnostics are separate; their longest
matrix power has trace drift around 0.0021 and is not used in the proofs.
The finite certificates use exact rational arithmetic and unitary integral
remainder bounds, rather than those floating-point long-time powers.

The supplied predecessor already contains sign projection, gain polynomials,
and analytic uniform-gain obstructions. Those mechanisms are not promoted
as new inventions. The contribution developed here is the first-motion
adversarial variance theorem, its explicit symmetric fifth-order certificate,
the fixed-polynomial-composition corollary, and the randomized action-tail
bound at the scopes proved.

The unresolved frontier is any epsilon-dependent native program outside
these restricted compilation limits. The analysis does not exclude growing
word shapes, private random choices of whole word shapes, nonperturbative
control, or another construction. No claimed physical advantage, historical
priority, or complete independent audit follows from the local calculations.
Only the frozen packet, named checkpoint, predecessor supplement, and this
continuation's own files were read. No network, services, installations,
production contact, or nested agents were used.
