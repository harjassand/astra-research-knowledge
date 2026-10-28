# Structured comparator, acquisition costs and prior scope

## What ordinary computation already provides

The independent literal absorbing chain has no waiting-time cutoff and no
Monte Carlo error. Its state includes the active program stack and every
retained photon count; reward equations give source/fusion/clock costs and
state/cost correlations. This is the first comparator, not a deliberately
mean-field or truncated substitute.

The stronger comparator is the same ordinary chain stored in factored form.
A held pure-death buffer and a preparing child have a Kronecker transition
Q_child tensor L_loss. Falling-factorial diagonalization of L_loss yields
the resolvents I-z lambda^s Q_child. Its contraction is exactly the scalar
compiler's shifted-PGF recursion. The proof and 250 exact components of an
explicit 65-state block establish this equivalence constructively.

Therefore a large reduction from explicit matrix dimensions is real, but it
is also available to an equally informed structured phase-type solver. No
generic lower bound, numerical separation or superiority over that solver
has been established. The output is an exact, validated specialization and
implementation for the supplied factory.

## Sizes and what is charged

Let n=2^d. The literal controller has

    M_1=1,   M_n=(n+2)M_(n/2)+(n+1)^2.

This gives 13,103,1111,20287,690847 states at n=2,4,8,16,32. Asymptotically
M_(2^d)=Theta(2^(d(d+1)/2)), hence quasipolynomial in n. Calling this an
exponential-in-n ordinary-method lower bound would be incorrect.

The root scalar compiler at z=1 caches descendant sizes m and exponents
0<=e<=2(n-m). At lambda!=1 its full unpruned recursion has

    R_n=(2n+1)d-2n+3                 argument nodes,
    V_n=[8n^2+6n(d-1)+3d+7]/3       probability entries.

It carries three numbers per probability entry (value, source derivative,
time derivative). At n4 this is 13 nodes and 165 scalar entries. These counts
exclude fusion kernels, which contain

    sum_(m=n,n/2,...,2) (m+1)^2(2m+1)=O(n^3)

entries, and the bare Fock beamsplitter cache, also O(n^3). The literal loops
admit a conservative O(n^6) arithmetic bound; that is not an optimality claim.
At lambda=1 exponents collapse, so the unpruned count is only an upper bound.
The separate z=lambda^2 comparison query increases the root exponent budget;
its time is included in the measured comparison calls below.

Every stored count ranges up to 2m for a size-m child. Omitting the p2 tail or
using only 0,...,m would undercount both the physical outputs and the states.
Every failed preparation and fusion is charged. Per trajectory T=C+J; the
final accepted fusion also spends one clock. These costs cannot be replaced
by the n nominal raw leaves or by conditioning on an accepted individual
fusion attempt. The main n4 result is C=19.3356956644045 and T=31.5560389544306.

## Precision and exact rational cost

Polynomial scalar count does not imply polynomial exact rational bit size.
The producer reports cached numerator/denominator maxima 1836/1833 bits at
n4 and 32107/32101 at n8, lambda=.999. Only n4 has been independently compared
here. The literal solver retains exact values for all start states, rewards
and an extra PGF query; its maxima are 2163/2162 bits at n4 lambda=.999 and
3272/3271 bits at lambda=.99999. These are different sets of intermediates,
not a proof of one algorithm's bit-complexity advantage.

For approximate evaluation the producer's conservative existence argument
is sound at this model scope: q=lambda/2 gives each true renewal denominator
at least q^(2n). Induction gives E[C]<=n q^(-4n), and active-output accounting
gives J<=C-1 and T<=2C. Finite-difference coefficient absolute sums and Fock
kernel coefficients are bounded by exp(poly(n,input bits)). The polynomial
arithmetic DAG therefore has exp(poly) bounds on intermediate magnitudes and
local error amplification on a sufficiently small neighborhood. Directed
rounding with poly(n,input bits)+O(log(1/epsilon)) precision suffices for a
requested absolute error epsilon. This does not assert small exact fractions
or near-optimal precision. It applies equally to the algebraically identical
structured phase-type realization.

The reviewed dyadic class uses exact integer endpoints at scale 2^b,
floor/ceiling multiplication and division, and excludes zero denominators.
The n4 256-bit run enclosed all 36 independent-chain components, with maximum
probability width 2.1011798094544784e-74. It used 12838 reported interval
operations and 0.0246 seconds for the two queried arguments. Larger producer
receipts, including n32, have not been replayed or independently certified by
this comparison.

## Observed timing, not a structured-comparator benchmark

| Exact fixture | Literal chain seconds | Producer scalar comparison seconds |
|---|---:|---:|
| n2, lambda=.999 | 0.0102 | 0.00121 |
| n4, lambda=.999 | 6.5826 | 0.02764 |
| n4, lambda=.99999 | 12.5856 | 0.03992 |
| n4, lambda=1 | 1.0427 | 0.00275 |

These are single local wall-time observations, including exact reward solves
and an additional PGF query. The literal solver uses Python Fraction and dense
fraction-free elimination; it is not an optimized sparse or factored incumbent.
The producer call uses its own scalar arithmetic graph. No benchmark of an
independently optimized structured implementation was performed. The exact
65-state waiting-block comparison took 0.929 seconds; it serves correctness
and equivalence, not a performance claim.

## Primary prior and its actual boundary

[Kuzmin et al., Scalable repeater architectures for multi-party states,
npj Quantum Information 5,115 (2019)](https://www.nature.com/articles/s41534-019-0230-3)
uses joint density-matrix/completion-time distributions, Laplace transforms,
memory evolution and geometric resummation of failed generation. This is a
direct comparator family for the claimed operation, not merely a generic
reference to Markov chains.

[Kuzmin and Vasilyev, Diagrammatic technique for simulation of large-scale
quantum repeater networks with dissipating quantum memories,
Sec. III.2](https://arxiv.org/html/2009.10415v1) explicitly derives a shifted
Laplace argument from an exponential prefactor in Eq.7 and sums failed
mergings in Eq.14. Its next-level linear-size implementation assumes new
segments are time-independent states generated by Poisson processes at their
mean rate, and explicitly labels that replacement an approximation. The
factory here retains the exact nested joint completion law. That difference
does not establish that the prior general transform machinery cannot do so;
the independent structured comparator above can.

[Goodenough, Coopmans and Towsley, On noise in swap ASAP repeater chains:
exact analytics, distributions and tight approximations,
Quantum 9,1744 (2025)](https://quantum-journal.org/papers/q-2025-05-15-1744/)
provides exact generating-function fidelity/decoherence calculations for its
repeater protocol. The [primary full text](https://arxiv.org/html/2404.07146v5)
also treats a global cutoff. Its state, schedule and noise model differ from
the present diagonal optical factory. It establishes strong existing exact
statistical methods, not an identity of the two protocols.

No comprehensive historical priority search was performed. The decisive
matched-comparator conclusion instead follows from our explicit phase-type
derivation: the ordinary method has the same finite shift closure.

## Physical and resource boundary

Source weights, absence of higher/coherent/multimode components, mode matching,
detector response, per-clock loss, reset time and passive-step time are supplied
assumptions. None was measured here. Conditional mean brightness is not a
certificate of a useful distilled non-Gaussian computing resource. The exact
model output does not establish a useful device, optimal control policy,
quantum advantage, or civilization-level scientific capability.
