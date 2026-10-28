# A source-local amplitude certificate and a coarse true cold-purity bracket

An actual inequality changes the acquisition contract: **one thermal amplitude
can certify normalized purity without an extensive energy-norm prefactor or
a separately assumed approximation at twice the temperature.** A concrete
entangled-block implementation and its finite-ring readout were executed.
Its small-collar residual fails the required tolerance, so none of the15
remaining bootstrap inputs is acquired at the required precision.

For A(0)=I define E(s)=(A'(s)+H A(s)/2)A(s)^-1 and nu=integral||E||. The
proved all-Schatten bound is

    ||A(beta)-exp(-beta H/2)||_p
        <=(exp(nu)-1)||exp(-beta H/2)||_p,   every1<=p<=infinity.

With eta=exp(nu)-1<1, the computed amplitude purity P_A satisfies

    |log P_A-log T_H(beta)|<=4log((1+eta)/(1-eta)).

The first rung needs nu below9.300594805589878e-8. This is an acquired
certificate theorem, not an acquired small residual. Root completed an
independent analytic/source review at this scope in
`../../cold_residual_review/REVIEW.md`.

The implemented amplitude places exact collar expansionals between entangled
open Gibbs blocks. Its multiplicative residual is a sum of finite source
operators [W,C]C^-1/2; the inside terms cancel exactly. A bounded QBP factor
was also constructed and its temperature derivative included. That repair
reduces raw factor growth but does not provide the needed small residual.
Those local ODE/norm values retain numerical-discovery status.

For the actual block4/collar1 amplitude, an exact one-magnon calculation
proves

    integral||E_total|| >=(n/4)[sinh(2beta)/4-beta/2].

At beta3/4 this exceeds10.06847 on ring256 and20.13694 on ring512. Thus this
particular all-Schatten certificate fails decisively. This is not a lower
bound on its true purity error or a no-go for other entangled amplitudes,
larger blocks, thermal MPO/BS-CMI methods, or the spin-two gap.

The declared ansatz's normalized purity is nevertheless read accurately.
Closed transfers of dimensions25 and625 give exactly Tr(AA*) andTr[(AA*)^2].
The latter retains crossed central block indices; it does not square a
traced-out one-copy marginal. Positive Taylor series, rational tails,
explicit binary64 multiplication/addition counts and charged clipped-entry
tails enclose the complete traces. All physical sectors and every transfer
mode are included. These accurate values remain **ansatz purities**.

A separate ordinary ALT/Golden--Thompson argument does produce coarse bounds
for the **true uniform-chain Gibbs state**, using only the already accepted
warm logZ inputs at beta1/2 and3/4:

| ring | lower log T(3/4) | upper log T(3/4) |
| ---: | ---: | ---: |
| 256 | -186.543892386 | -73.667364671 |
| 512 | -373.087784772 | -147.334729342 |

Every local exponential factor and binary scale is restored for these absolute
partition bounds. The actual ALT2 upper is stronger than the retained GT1
comparator. Their widths are about112.88 and225.75, against a required log
accuracy near7.44e-7. Thus these are true but coarse cold-rung brackets;
neither is a completed dyadic-lift input.

The local/source computations are modest, but widening the dense collar is
expensive: squared-density transfer dimension is5^(4ell), so ell2 alone would
require about1.22TB of dense binary64 storage. That allocation was not
attempted. Any claimed wider-collar acquisition must include a structured
contraction/error operation and the actual local residual, rather than
assuming either.

The current BS-CMI purity-factorization and MED/free-energy methods are the
strong ordinary comparators, at their actual marginal, boundary, temperature
and numerical-constant scope. They are discussed in
`SOURCES_AND_COMPARISON.md`. This construction establishes no practical
advantage over them and no new generic algorithmic tractability class.

The complete mathematics, finite-ring indices, scalar restoration, source
failure and numerical model are in `PROOF.md`. Exact-rational power controls
and independent full625-state source controls pass. All earlier completed
folders remain frozen. `ACQUISITION_COSTS.md` charges the local integral
calibration and the full squared-density readout. **Fine cold normalized-purity
inputs remain NOT_ACQUIRED; the uniform spin-two gap remains NOT_ACHIEVED.**
