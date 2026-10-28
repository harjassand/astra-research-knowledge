# Independent substantive review: first actual connected thermal increment

**Disposition: ACCEPTED at the exact scope stated here.**

For the actual uniform periodic spin-two Heisenberg Hamiltonians
H_n=sum_i S_i dot S_(i+1), with unchanged boundaries and energy reference,
let Z_n(b)=Tr exp(−bH_n), T_n(b)=Z_n(2b)/Z_n(b)², and
S(n,b)=Z_(2n)(b)/Z_n(b)². The newly acquired inputs establish

    −3/100000000000
       < log T_512(3/4)−2log T_256(3/4)
       < 1/1000000000000000000000000,

    S(256,3/2)>1−3/100000000000.

This is one actual finite-model connected dyadic increment and a new actual
spatial seed. It is not an acquisition of the individual fine temporal
purities, six later increments, final T_512(96), a uniform spin-two gap,
or a physical measurement.

## Review independence and inherited accepted inputs

I whole-read the producer's thermal/PROOF.md, code/verify_first_increment_fraction.py,
code/scalar_loop_certificate.py, code/acquire_cycle_moments.py, and its
imported acquire_open_moments.py. I read the earlier continuation/CONSTRUCTION.md
and the completed spin2_review/WARM_REVIEW.md. The latter accepted the actual
compact self-adjoint history-kernel interface J_b=K_b/5, the open/vacuum
identities, complete fourth moments, A4 projection, and the degree192
open/twisted-four-site source data. Those remain scoped accepted inputs.

The companion verify_independently.py imports none of the producer code
and does not invoke its verifier. It uses standard-library Fraction
arithmetic, a different Horner summation, a fixed256-term positive
exponential series, and the independent coarse trace-tail bound
exp(x)<=3^ceil(x). REPLAY.json records every rational positivity slack.

The second companion rebuild_cycle_controls.py constructs spin-two
Hamiltonian blocks directly from literal ladder formulas and tuple states,
without the producer's base-five indexing or sector constructor. It includes
ALL signed magnetizations rather than inferring negative blocks. Its exact
output is CYCLE_CONTROL_REPLAY.json. It is a bounded construction/data check;
the entire new degree192,25-modulus six-cycle acquisition was reviewed,
not independently regenerated in full.

## 1. All rotation lists and loop multiplicities

The accepted history operator commutes with the physical SO(3) action and
hence its A4 subgroup. On the complexified history space, A4 has irreps
1,1',1'',3. Denote by I_p the complete even-power trace on the trivial
multiplicity space, by O_p the trace on EACH of 1',1'', and by N_p the
trace on the multiplicity space of the three-dimensional irrep.

The A4 character table gives the central projection traces

    I_p=(M_p+3P_p+8C_p)/12,
    O_p=(M_p+3P_p−4C_p)/12,
    3N_p=3(M_p−P_p)/4,
    M_p=I_p+2O_p+3N_p.

Here M_p=Z_p(I)/5^p, P_p=Z_p(P)/5^p, C_p=Z_p(C)/5^p. The two
120-degree A4 classes have equal traces because their SO(3) rotations
are conjugate. Their complex characters add to −1 for 1' and1'',
yielding O_p. The 3-irrep has characters3,−1,0 on identity, half turns,
and third turns, yielding its FULL trace3N_p.

Equivalently J is identity on each irrep tensor a self-adjoint operator on
its multiplicity space. Thus every N eigenvalue is represented once in N_p
and three times in the physical loop, while each O list costs its own copy.
The coefficients1,2,3 are exact representation multiplicities. No physical
magnetization, source mode, nontrivial irrep, or periodic seam is discarded.
Even powers count absolute eigenvalue powers; negative J eigenvalues need
no positive-kernel or Perron–Frobenius assumption.

## 2. Actual invariant trial and legitimate I-list subtraction

The empty-history atom v has norm1 and is fully rotation invariant.
Because J commutes with rotations, w=c0v+c1Jv+c2J²v is invariant and lies
in the I list. The accepted contraction identities supply

    m0=1, mr=<v,J^r v>=Z_open,r(b)/5^r.

Consequently G=sum c_i c_j m_(i+j)=||w||² and
H=sum c_i c_j m_(i+j+1)=<w,Jw>. A degree-two trial needs moments only
through5 for its Rayleigh quotient; acquiring moment6 does not make its
residual variance an unspoken premise. The independent rational consumer
proves G>0 and H−theta G>0 at both reported temperatures.

The compact self-adjoint spectral theorem now provides an actual positive
I eigenvalue lambda>theta. Positivity makes the supremum an attained
positive eigenvalue. Removing one occurrence of lambda from I_4 leaves

    sum_other_I |lambda_j|^4
       =I_4−lambda^4<I_4−theta^4.

This subtraction is valid in the I list because the trial was shown to
lie there; it is not a subtraction of a scalar trial from a different
physical or symmetry sector. The residual is logically nonnegative from
the spectrum, even though the arithmetic only needs an upper bound.

Similarly, each O eigenvalue has modulus bounded by O_4^(1/4), and each
N eigenvalue by N_p^(1/p), with p=4 at b3/4 and p=6 at b3/2. Exact
arithmetic verifies the deliberately rounded bounds

| b | theta, strict lower | other I radius | each O radius | each N radius |
|---|---:|---:|---:|---:|
|3/4|233/25|3|21/5|184/25, from p4|
|3/2|285|141|197|257, from p6|

All three radii are strictly below theta in both rows. Thus these data
even certify a unique dominant positive mode. The stated loop bound does
not require this extra separation: its validity follows from the complete
even masses alone. No Temple inequality, accurate eigenvector residual,
accurate pressure, finite-rank assumption, or physical gap is used.

## 3. New integer spin-two cycle acquisition reviewed

In the polynomial spin basis,

    S+|m>=(2−m)|m+1>, S−|m>=(2+m)|m−1>, Sz|m>=m|m>.

Therefore B=2H has integer diagonal terms2m_i m_j and integer exchange
coefficients(2−delta m_i)(2+delta m_j), delta=+/-1. The producer adds the
closing6-to1 bond explicitly. For P the half-turn negates its two
exchange terms and preserves SzSz. Diagonal scaling by products of
binomial basis norms gives the ordinary Hermitian spin-two Hamiltonian.
The seam term is unitarily rotated, so its local norm bound is unchanged.

Each physical pair has energies−6,−5,−3,0,4. Thus ||2H_6||<=72 and

    |Tr B^k|<=5^6 72^k.

Both I and P preserve total magnetization. Global spin inversion exchanges
S+ and S− and changes Sz to−Sz; it preserves both seam types. The +/-M
blocks therefore have the same traces, justifying the producer's factor2
for M>0. The independent builder instead explicitly retained every
M=−12,...,12. Its total dimension is15625, with largest block1751.

For each producer modulus p, a dense intermediate has entries in[0,p).
The checked row-absolute-sum bound times p<2^62 bounds every sparse
matrix-product accumulator, including its signed partial sums. The
checked block dimension times p<2^62 bounds every np.trace sum. The
subsequent trace and CRT combination are Python integers. No unsigned
wrap or floating sparse product enters this acquisition.

Independently checking all25 moduli establishes pairwise coprimality and
the stored product. Its bit length is1226, while 5^6 72^192 has bit
length1199. The product is strictly greater than twice this physical
bound. Signed CRT reconstruction is therefore unique for all193 traces.
All saved moments pass the appropriate physical bound. Primality is not
needed; the modular inverses and checked coprimality suffice.

The independent literal all-M reconstruction reproduces exactly:

    Tr B^k, k=0,...,6, I:
    15625,0,4500000,−4500000,3520800000,−11538000000,
    4304937600000;

    Tr B^k, k=0,...,6, P:
    15625,0,4500000,−4500000,3520800000,−11538000000,
    4120617600000.

It also reconstructs all193 four-cycle I/P moments modulo one49-bit
modulus. The I control uses the independent exact spin-addition spectrum
of H4=(S1+S3) dot(S2+S4), with full dimension625; the P control matches
the previously accepted full exact array. The separate Fraction consumer
checks all193 analytic moments of open chains1,2,3. These checks support
the actual construction and present input version. They are not a claim
that every new six-cycle modular multiplication was independently rerun.

The new I/P acquisition's recorded combined execution cost is431.589s.
Earlier end-spin exploratory acquisition194.429s is additionally charged
by the producer. No scientific efficiency claim follows from replay time.

## 4. Independent complete thermal trace bounds

For B physical bonds and degreeD=192, ||H||<=6B gives the standard
all-state Taylor remainder

    |Z−sum_k Tr(2H)^k(−b/2)^k/k!|
       <=5^n exp(x)x^(D+1)/(D+1)!, x=6Bb.

The independent consumer evaluates the polynomial by exact Horner
arithmetic. It bounds exp(x) by3^ceil(x): the elementary positive series
proves e<3, and monotonicity handles rational x. This is deliberately
coarser than the producer's exponential enclosure and still passes all
required inequalities. The four-cycle I partition trace is independently
summed over its exact spin-addition energy multiplicities, using fixed
positive rational exponential series and a geometric remainder; negative
exponents are enclosed by reciprocals of positive intervals.

The resulting exact interval forms verify positive trial norm, positive
Rayleigh margin, I residual bound, O fourth-moment bound, and N fourth/
sixth-moment bound. REPLAY.json stores exact rational slacks, not just
binary endpoint diagnostics. Numerical diagnostics for the final rational
tails are

    tau_256(3/4)<1.6880e−26,
    tau_256(3/2)<9.5437e−12.

The decisive comparisons were made in Fraction arithmetic:

    4tau_256(3/4)<10^−24,
    2tau_256(3/2)<3*10^−11.

This review does not certify the sharper mpmath/Chebyshev numerical
interval. Its formulas were read, but the conservative exact result above
is sufficient and independent of that interval-arithmetic implementation.

## 5. Connected cancellation, signs, and attained precision

For even n, select the same actual positive lambda in every trace at a
fixed temperature. Complete even-power counting gives

    Tr J^n=lambda^n(1+u_n), 0<=u_n<=tau_n,
    tau_n<=(rI/theta)^n+2(rO/theta)^n+3(rN/theta)^n.

The radius and total mass bound for each list justify these sums, including
infinitely many modes. Factors5^n cancel exactly in the spatial ratio.
The powers lambda^(2n) cancel exactly between Tr J^(2n) and (Tr J^n)^2.
This is cancellation of the same unknown spectral value, not subtraction
of separately rounded pressure estimates.

Because n is even, S(n,b) is the purity of the nonnegative weights
|lambda_j|^n/Tr J^n. Hence S<=1 exactly. Also

    log S(n,b)>=−2log(1+tau_n)>=−2tau_n.

Direct algebra, with the actual ring sizes retained, gives

    logT_(2n)(b)−2logT_n(b)
       =logS(n,2b)−2logS(n,b).

Thus the connected scalar lies between−2tau_n(2b) and4tau_n(b).
The exact strict tail comparisons above yield the claimed strict interval.
At b3/2, exp(−2tau)>1−2tau also gives the stated strict spatial seed.
No sign convention, pressure term, Hilbert-space normalization, or double
ring is missing from these steps.

## Disposition boundaries

The first connected input and spatial seed are accepted actual-model
mathematics, using the previously accepted transfer interface and the newly
reviewed exact six-cycle input. The main new repair is acquisition of the
connected quantity needed by the source identity; it genuinely avoids
paying for two unnecessarily precise extensive quantities separately.
The identity and group-projection theory themselves are established inputs.

Six later connected increments and final T_512(96) remain unacquired.
The retained failed b3/b6 counts are method failures, not impossibility
theorems for other representations. No new claim about world priority,
physical hardware, generic computational advantage, or a uniform gap is
certified by this review.
