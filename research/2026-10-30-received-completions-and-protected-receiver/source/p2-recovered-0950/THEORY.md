# P2 working construction: uniform logical control with forward memory drift

Date: 2026-10-30. Author/reviewer scope: the current root investigation only.

This is a new working derivation, accompanied by exact finite algebra checks
and floating-point finite examples. It has no new independent review, device
validation, threshold, or established priority claim. Earlier accepted Astra
foundations and their dependencies remain accepted; none is reopened here.
The older helper's 6,208 checks and the separately scoped root checks apply to
their earlier restoration bridge, not to this construction.

## 1. The consequence and the change of attack

The useful task is a two-data-qubit entangler that works for arbitrary initial
states of the mediator, its retained environment, and an external reference.
The memory is allowed to keep evolving. Recovering or identifying its state
is not part of the task. The physical interface supplies one signed native
coupling at a time; it does not supply a perfect logical gate or a bath inverse.

For a supplied physical model, a strong ordinary subsystem optimal controller
beats the previously constructed algebraic words in the tested finite regime.
This is the operative conclusion of that comparison. The new theoretical
question is different: can one fixed native program work on an entire coarse
class of coupling geometries, without learning their precise scalar chirality,
while an unknown memory Hamiltonian continues forward?

The working theorem below says yes in a bounded, static model with repeatable
native sign and timing control. It establishes a sufficiency principle for
information about the source. The literal construction is extremely expensive
and does not establish a speed, calibration-cost, or noisy-hardware advantage.

## 2. Physical model and promises

Data are qubits 1 and 2. Complete memory is a mediator spin b and an arbitrary
environment E. Let

\[
A=X_1\otimes B_1,\qquad B=X_2\otimes B_2,\qquad C=Y_1\otimes B_3,
\]

where \(B_j=(b_j\cdot\sigma_b)\otimes I_E\), with real, unknown, static
vectors \(b_j\). Tensor identities on the unused data qubit are implicit.
Every actual native segment is

\[
H(t)=I_D\otimes H_M+s A_j,\qquad s\in\{-1,+1\},
\]

with exactly one handle active. The same unknown, time-independent \(H_M\)
acts throughout; its sign is never reversed. We assume known bounds
\(\|H_M\|\le D\), \(\|B_j\|\le B_0\), and

\[
0<c_-\le c=(b_1\times b_2)\cdot b_3\le c_+.
\]

A negative known orientation is handled by reversing one control convention.
The dimensions and initial state of E need not be known. The norm bound is
essential to the uniform proof given here. This does not automatically extend
to unbounded all-Fock memory Hamiltonians; earlier local regularity results
retain their own stated classes.

These are source promises, not acquired facts. Qualifying the Pauli coupling
form, nonzero gap, sign, stability, and native control interface is a physical
task. Exact repeatability is an ideal control premise. Any actual mismatch,
unmodeled holding Hamiltonian, switching error, or time dependence must be
included in the real evolution. A general additive Hamiltonian error contributes
at most \(\int\|\Delta H(t)\|dt\) to the joint operator error. This is a
sufficient bound, not a lower bound on the best controller's performance.

The target is \(U_\theta=\exp(i\theta P)\), \(P=Z_1X_2\). Success means
that, for every admitted physical model, a same-memory unitary \(V\) exists
with

\[
\|W-U_\theta\otimes V\|\le\epsilon.
\]

This is an operator statement covering arbitrary data/reference/memory
correlations. It neither resets memory nor declares the apparatus ready for
an unrelated next operation. Sequential use is valid only when each next
operation is itself uniformly qualified on the complete memory it receives.

## 3. The strong ordinary finite comparator

The retained-sector fixture is

\[
b_1=(.9,.2,-.1),\quad b_2=(-.2,.8,.3),\quad b_3=(.1,-.3,1.1),
\quad c=.925,
\]
\[
H_M=.23Z_b+.14Z_bZ_E+.11X_b.
\]

The static uncertainty family is

\[
H_{j,s}=I_D\otimes H_M+hX_1+
s(1+g)(1+\eta\,1_{s<0})A_j,
\]

with \(|g|\le.005\), \(|\eta|\le.001\), and \(|h|\le.001\).
The optimizer uses only the chronological pattern
\((A_+,B_+,C_+,A_-,B_-,C_-)\), repeated, with independently chosen
nonnegative durations. It has no simultaneous handle, ideal local gate,
memory reset, or state knowledge. The nominal generators and uncertainty
family are supplied classical information. Their empirical acquisition is
not included in the numerical result.

The objective permits any final memory unitary. For
\(W=(U_\theta^\dagger\otimes I)U\), maximize
\(\|\operatorname{Tr}_D W\|_*/16\), with a small duration penalty.
This is an established subsystem optimal-control approach, not a new P2
objective. The derivative uses the envelope theorem for the polar-unitary
choice. Finite-difference checks on the initial point and saved solutions
agree to about \(10^{-10}\); no global optimum is claimed.

Executed results:

| Fixed compiled controller | Segments | Total duration | Nominal joint product error | Worst tested box-corner error |
|---|---:|---:|---:|---:|
| Ordinary nominal fit | 72 | 31.4528173 | 0.000009410 | 0.05536931 |
| Ordinary robust fit | 72 | 35.1906761 | 0.00117635 | 0.01077135 |
| Expanded ordinary restart | 144 | 36.7553 | 0.00365671 | 0.0261261 |
| Long ordinary restart | 144 | 71.5597 | 0.004377 | 0.0452411 |
| Basic 96-word family, tau approximately .05 | 10,272 | 512.2121 | 0.01064083 | 0.5085800 |
| Basic 96-word family, tau approximately .02 | 159,264 | 3,184.8688 | 0.00086792 | 0.8588413 |
| Raised word, tau approximately .04 | 124,416 | 5,207.3205 | 0.00250963 | 1.3855432 |
| Integer-clock word, tau approximately .012 | 1,013,760 | 12,532.4442 | 0.00036773 | 1.3571496 |

All comparisons propagate the same joint memory throughout. Algebraic words
are compiled using their nominal coefficient, with no per-corner angle refit.
Their genuine retained-sector cancellation is preserved; it is insufficient
to win this complete fixed-program finite comparison. Longer ordinary
restarts also performed worse. These are actual controller results and
failures, not a proof that every pulse arrangement or calibration policy must
behave similarly. The special exact seven-pulse construction retains its
stronger orthogonal-coupling/zero-drift premises.

The chosen product-gauge errors in the table are upper bounds, not optimal
operator-gauge distances. A separate normalized-Choi calculation checks an
actual recipient-visible failure. With maximally mixed mediator and a fixed
initial E sector, it gives these worst-corner logical trace-distance lower
bounds: basic word at duration 512.2121, 0.44646155; raised word at duration
5207.3205, 0.93803388; integer-clock word at duration 12532.4442, 0.97106097.
Each witness uses a maximally entangled data/reference input and traces out
the physical memory. These failures therefore cannot be attributed merely
to a choice of final-memory reference. They are numerical witnesses for the
specific fixed schedules, not impossibility theorems for their entire access
class. Maximum numerical unitarity drift over these algebraic finite runs
was 6.35e-10, well below the displayed witness differences.

### A continuous-box bound rather than corner extrapolation

For the ordinary robust schedule define the normalized conditional expectation
\(E_D(W)=I_D\otimes C\), \(C=\operatorname{Tr}_D(W)/4\), and
\(R=W-I_D\otimes C\), \(r=\|R\|\). Since \(W\) is unitary,

\[
I_M=C^\dagger C+\tfrac14\operatorname{Tr}_D(R^\dagger R).
\]

The companion identity is
\(I_M=CC^\dagger+\tfrac14\operatorname{Tr}_D(RR^\dagger)\).
Together they bound C from below on both sides. Thus the polar factor is
unitary even for infinite-dimensional complete memory, rather than merely
an isometry with a possible range defect.

Thus if \(r<1\), the polar factor \(V\) of \(C\) is unitary and

\[
\|W-I_D\otimes V\|\le r+1-\sqrt{1-r^2}.
\]

Let \(L_i=\int\|\partial_iH(t)\|dt\). The Hamiltonian is affine in
each individual parameter, even though it contains a gain/imbalance cross
term. Duhamel gives \(\|\partial_i^2 U\|\le L_i^2\).
The map \(Q=I-E_D\) has operator norm at most 2. Linear interpolation on
an interval of half-width \(a_i\) therefore has residual error at most
\(a_i^2L_i^2\). Repeated interpolation in a rectangular cell and the
triangle inequality give

\[
r_{\rm box}\le\max_{\rm nodes}\|R\|+\sum_i a_i^2L_i^2.
\]

For 12, 4, 4 subdivisions of the three complete intervals, 325 nodes give

\[
\max r=0.01077123832,\quad
(L_g,L_\eta,L_h)=(34.4861113,21.0688184,35.1906761),
\]
\[
r_{\rm box}\le0.01108285503,\qquad
\|U-U_\theta\otimes V\|\le0.01114427176.
\]

The interpolation argument is analytic. The reported node calculations and
constants use floating point, with maximum unitarity drift \(1.13\times
10^{-13}\). This is not an interval-certified rounding enclosure. The
result is appropriately described as an analytic whole-box bound evaluated
numerically, not as an independently certified hardware guarantee.

## 4. Pure-control powers of the chirality

Write the anti-Hermitian generators
\(a=-iA\), \(b=-iB\), \(c_0=-iC\), \(d=-iI_D\otimes H_M\).
Pauli algebra gives

\[
\ell=[c_0,[a,b]]=i4cP\otimes I_M.
\]

Because \(P\) anticommutes with \(A\),

\[
\operatorname{ad}_{\ell}^{2}(a)=-64c^2a.
\]

Consequently the homogeneous Lie polynomials

\[
L_n=[c_0,[\operatorname{ad}_{\ell}^{2n}(a),b]]
=i4(-64)^n c^{2n+1}P\otimes I_M
\tag{1}
\]

have degrees \(k_n=6n+3\). They produce all odd chirality powers and
are invariant under the even-sign group

\[
G=\{(+,+,+),(+,-,-),(-,+,-),(-,-,+)\}.
\]

Each is odd under flipping C alone. Equation (1) is an algebraic identity;
it is not yet a physical simulation protocol. In particular, one cannot
implement a nominal clean logical macro, ignore its accompanying memory
unitary, and then take its commutator with a bare native coupling. That
would reintroduce precisely the returning-memory dependence this work must
keep. The construction below extracts each polynomial as a flat native word.

The general odd-chirality construction also permits scalar identity offsets
in B1 and B2, with their norms included in the supplied bounds. These offsets
drop out of [B1,B2], and the identity ad_ell squared(a) = -64 c squared a uses
the data anticommutation with P, not that A squared is scalar. B3 must retain
its stated traceless Pauli form: an outer identity offset contributes a
memory-dependent logical term, preserving the earlier negative case. The
degree-five example below uses the more specific traceless B1 fixture when
identifying ad_a squared(ell) with a clean scalar term. An always-on h X1
holding error is not an identity offset that follows the native A sign and
is not covered by this extension.

## 5. Forward-drift extraction lemma

**Working lemma.** Suppose an odd-degree pure-control Lie polynomial L of
degree k evaluates to a memory-independent multiple of P, is G-invariant,
and is odd under C sign reversal. A finite word with explicitly scaled native
couplings can be constructed
whose logarithm has no nonmemory coefficient below k, whose degree-k
nonmemory coefficient is a nonzero known scalar multiple of L, and whose
first possible remaining nonmemory term has degree k+2. The memory drift
is forward in every segment. These are exact coefficient identities for the
intermediate amplitude-extended representation. Rational amplitude scalings
can then be approximated to any specified finite accuracy from the same
signed-only interface as in Section 7; that compilation is not claimed to
preserve the exact coefficients at a fixed PWM subdivision count.

### 5.1 Starting commutator word

For a chronological word u, let inv(u) mean reverse its order and flip every
control sign. At zero drift this is its inverse. At actual nonzero drift it
is simply another physical forward-drift word; no inverse claim is made.
The chronological word

\[
\operatorname{commword}(u,v)=\operatorname{inv}(v),
\operatorname{inv}(u),v,u
\]

has the desired leading commutator at zero drift. Recursively use this to
build a word for L. Append its reversed chronological list, without sign
flips. This palindrome has twice the odd-degree leading term at zero drift,
and its full logarithm is odd in the common duration parameter tau.
Its first-order control sum vanishes; the first-order term is memory-only.

### 5.2 Projection of the first surviving data coefficient

Concatenate the four G variants and then their reverse order. Every subword
is a palindrome, so the result remains a palindrome. If all lower-degree
nonmemory terms vanish, the first nonmemory coefficient is the sum of its
G variants. Cross-commutators of lower memory-only terms remain memory-only.

The generated data algebra contains only the second-qubit factors I and X2.
A monomial has data parity determined by the counts of A, B, and C. G
projection leaves only parity 000 and 111. Their data factors are I and P,
respectively. Flipping C leaves memory coefficients unchanged and reverses
P coefficients. These facts also follow from formal conjugations by data
Paulis. The Pauli conjugations are an algebraic argument, not extra physical
pulses.

### 5.3 Removal of lower data degrees

At successive odd m=3,5,...,k-2, first apply the projection. If the current
first data coefficient is \(\tau^mP\otimes Q\), use

\[
S_+(\tau)S_-(2^{1/m}\tau)S_+(\tau),
\tag{2}
\]

where minus flips C and all durations remain positive. The coefficient of
the degree-m data term is \(2-(2^{1/m})^m=0\). Lower memory terms do not
create data below that degree. Palindromicity removes the next even degree.
At zero drift the source word still has no terms below k, and its target
degree-k coefficient is multiplied by
\(2-2^{k/m}\ne0\). Its sign and magnitude are known compiler constants.

For k>3, the projected degree-three coefficient is already zero: a P
monomial requires all three controls, hence cannot contain D at total degree
three, and the source zero-drift coefficient vanishes below k. No cancellation
block is needed at that first stage. Continue until all data terms below k
are removed, then project once more at degree k.

The induction is an identity for arbitrary control generators of the specified
data support, not for a chosen numerical model. It therefore remains true
when every controlled coupling is multiplied by any common amplitude lambda.

### 5.4 Amplitude-degree filter removes the remaining drift at degree k

After the preceding steps, the degree-k data coefficient has the form

\[
\lambda^k\gamma L+
\sum_{\substack{3\le j<k\\j\text{ odd}}}\lambda^j P\otimes Q_j.
\tag{3}
\]

All drift-containing monomials have fewer than k controlled letters. G
invariance requires odd counts of A, B, C and hence an odd controlled degree
of at least three. The pure-control term is precisely the known multiple
of L inherited from the zero-drift starting word.

Choose distinct positive rational amplitudes \(\lambda_i\le1\) and
rational weights, scaled to signed integers \(n_i\), so that

\[
\sum_i n_i\lambda_i^j=0\quad(j=3,5,...,k-2),\qquad
\sum_i n_i\lambda_i^k\ne0.
\tag{4}
\]

Existence is the nonsingularity of a Vandermonde matrix in \(\lambda_i^2\).
Execute \(|n_i|\) copies at amplitude \(\lambda_i\), flipping C if
\(n_i<0\), and append the reverse block order. The lower log coefficients
are memory-only, so they cannot generate data through degree k. The degree-k
data coefficient is the weighted sum (3), twice, and (4) removes all its
drift-containing terms. This proves the algebraic lemma.

The proof is deliberately a flat native-word construction. It never treats
a memory-evolving block as a reusable bare logical Hamiltonian while it is
interleaved with unqualified native interactions.

## 6. Executed exact instance and literal resource count

The first exact instance uses

\[
L_5=\operatorname{ad}_a^2\ell
=-i16c\|b_1\|^2P.
\]

The raw commutator word has 46 segments; its palindrome has 92. Two eight-word
G projections are followed by an amplitude filter: eight copies at amplitude
1/2 with C flipped, one copy at amplitude 1, and then the reverse block order.
The exact noncommutative rational expansion through degree five establishes

\[
\log W=\text{memory terms}+192\tau^5L_5+O(\tau^7),
\]

with every drift-containing nonmemory coefficient through degree five equal
to zero. The represented amplitude-extended word has **105,984 segments**,
before signed-only PWM compilation. For the retained
fixture its coefficient of iP is exactly \(-305472/125\). The certificate
is a hierarchical series calculation, not a device execution of those pulses.

For \(L_1\) in (1), the c-cubed primitive has degree nine. The raw source
has 262 segments, its palindrome 524. Projection at degree 3, projection and
(2) at degrees 5 and 7, and a final projection at degree 9 require 19,316,736
segments before the amplitude filter. A concrete exact filter is

\[
(\lambda_i)=(1/4,1/2,3/4,1),\quad
(n_i)=(-672,168,-32,3).
\]

Its moments at 3,5,7 vanish; its moment at 9 is 945/1024. The palindromic
filter uses 1,750 copies, producing **33,804,288,000 amplitude-extended
segments per literal cycle**, before signed-only amplitude compilation and repetitions
to obtain a finite gate angle. The exact moments are checked. The entire
degree-nine free-word expansion has not been computed; its justification is
the induction above. This cost is an explicit warning against reading an
existence theorem as an efficient protocol.

### A shorter weighted-duration filter, constructed after the initial count

The integer multiplicities in (4) need not be implemented as separate copies
when general positive duration ratios are allowed. For each signed weight
n_i, execute one subword at duration scale \(|n_i|^{1/k}\), with amplitude
lambda_i and C flipped for negative n_i, and then reverse the block list.
All lower data coefficients are zero, so mixed lower-order contributions are
memory-only. The degree-k data coefficient is still weighted by n_i, exactly.

For the degree-five example, use the half-amplitude C-flipped subword at
scale r, r^5=8, and the unscaled full-amplitude subword, followed by their
reverse. This reduces the count to **23,552 amplitude-extended segments**.
weighted_filter_certificate.py expands the complete noncommutative series
through degree five over Q[r]/(r^5-8). It verifies the same 192 L5 coefficient
and exact disappearance of all drift-containing data terms through that
degree. The positive algebraic time ratio is an actual control premise,
which can be rounded only with its error charged.

The corresponding degree-nine filter uses eight subwords rather than 1,750.
Its derived count is **154,533,888 amplitude-extended segments per cycle**,
with the same useful coefficient. Its duration multiplier over the unfiltered
word is 12.8559978. The lower-memory-only composition argument and exact
moments establish this variant; a complete degree-nine free-word expansion
has not been executed. The integer-multiplicity construction remains valid
under its simpler timing ratios. Neither count includes the additional
signed-only PWM switching or finite-angle repetitions. The shorter variant
is still far from an operational advantage.

## 7. Removing the extra amplitude interface

The proof temporarily uses a segment \(H_M+\lambda A_j\), for rational
\(0\le\lambda\le1\). This is not silently added to the native access.
Put \(p=(1+\lambda)/2\), \(q=(1-\lambda)/2\), and

\[
X=-ip(I_D\otimes H_M+A_j),\qquad
Y=-iq(I_D\otimes H_M-A_j).
\]

One Strang cell

\[
e^{\delta X/2}e^{\delta Y}e^{\delta X/2}
\]

uses only the original signed handles, with positive physical durations
\(p\delta/2,q\delta,p\delta/2\), summing to delta. It matches
\(e^{\delta(X+Y)}\) through second order. Both paths have integrated
generator norm at most \(L\delta\), \(L=D+B_0\). The unitary Dyson
third-order remainder bounds each path by \((L\delta)^3/6\), so the
cell difference is at most \((L\delta)^3/3\). Repeating r cells over a
segment of length t gives

\[
\epsilon_{\rm PWM}\le\frac{L^3t^3}{3r^2}.
\]

Errors add over segments. For any finite compiled word and accuracy budget,
a finite r suffices. Total physical duration is unchanged, but the switch
count and required timing resolution increase. Actual timing and sign
errors remain in the physical budget. This approximation is used at a
chosen finite target accuracy, not asserted to preserve the formal
coefficient identities at a fixed r as tau tends to zero.

## 8. Uniform finite accuracy and composition

For any one finite extracted word, let its segment durations be \(s_j\tau\)
and define \(\Lambda=\sum_js_j(D+B_0)\). For complex tau with
\(|\tau|\le r_0=\log(3/2)/\Lambda\), the product satisfies
\(\|W-I\|\le1/2\) and its analytic logarithm has norm at most log 2.
Cauchy bounds and \(\|I-E_D\|\le2\) give, for real
\(|\tau|\le r_0/2\),

\[
\|Q\log W-\gamma\tau^kL\|
\le4\log2\,(|\tau|/r_0)^{k+2}.
\tag{5}
\]

The memory part \(E_D\log W\) is anti-Hermitian and commutes with the
clean data term. The unitary Duhamel bound converts (5) to a joint product
operator bound of the same size. The constants are uniform in the memory
dimension and admitted physical models, but can be extremely large.

For a desired coefficient alpha multiplying \(c^{2n+1}P\), use N copies
with \(N\beta\tau^{k_n}=\alpha\), where beta is the known compiler
coefficient. Flip C if a sign change is needed. A suitable integer N makes
tau sufficiently small. The accumulated error is O(tau squared); the
physical duration is O(tau to the power 1-k). For the bare degree-nine
construction this is O(epsilon to the power -4), before counting its large
constants and PWM switches. Better formulas may exist; this derivation
does not establish their absence.

Each completed extracted operation has a product bound on arbitrary complete
memory input. Fully qualified completed operations may therefore be composed:
their errors add, their logical targets multiply, and their memory unitaries
multiply in the actual causal order. No fresh bath is inserted. This safe
composition is distinct from the invalid bare-native commutator shortcut
noted after (1).

This statement concerns a fixed, classically prescribed sequence. It does
not make the memory references independent of a future choice of pulse
program. Coherently controlling distinct programs can record that choice in
their distinct memory evolutions and needs its own physical construction.
A record controlling a logical choice belongs in the intended circuit, with
its errors charged. The fixed-program product reference here does not replace
the earlier causal reference across future logical choices.

## 9. Coarse promises suffice for a uniform target angle

Let \(\kappa=c_+/c_-\), \(r=1-\kappa^{-2}\). Define the odd polynomial

\[
p_m(c)=\frac{c}{c_+}\sum_{n=0}^{m}
\frac{\binom{2n}{n}}{4^n}
\left(1-\frac{c^2}{c_+^2}\right)^n.
\tag{6}
\]

The binomial series for \((1-z)^{-1/2}\) shows, uniformly on the
positive chirality interval,

\[
0\le1-p_m(c)\le\kappa^2r^{m+1}.
\tag{7}
\]

Expand (6) in odd monomials. For each coefficient, compile the corresponding
fully qualified operation from (1) and Sections 5-8. All desired logical
generators are multiples of P and commute. Their composition approximates
\(e^{i\theta p_m(c)P}\) uniformly, and its distance from
\(e^{i\theta P}\) is at most \(|\theta|\kappa^2r^{m+1}\).
Allocate the remaining error budget to physical synthesis and PWM. Every
schedule depends only on the coarse bounds, the requested angle, and the
accuracy, not on the actual chirality or memory state.

**Working theorem.** Under Section 2's promises, every requested finite
epsilon admits one finite signed-only native program that approximates the
same entangler \(e^{i\theta P}\), uniformly over the source class, while
all memory drift remains forward. No precision-dependent point estimate of
c or microscopic memory history is required by the construction.

The degree needed by the simple bound (7) is
O(kappa squared times log(kappa squared/epsilon)). That is a polynomial-degree
statement, not a runtime or pulse-count statement. The nested native words
and accuracy budget can grow far faster. Classical polynomial ensemble
control is prior; the contribution attempted here is an explicit
forward-memory native extraction under the stated restricted access.

## 10. Orientation is a real information boundary

The coarse promise cannot simply omit chirality orientation if the source
class then includes mirror-related coupling triads. Consider the allowed
zero-drift subclass and the reflection \(R(x,y,z)=(x,-y,z)\).
Let \(\Theta=(Y_1Y_2\otimes I_b)K\). For each signed native segment,
antiunitarity and the data spin flip give

\[
U_{Rb}=\Theta U_b\Theta^{-1}
\]

for the same chronological program. With initially maximally mixed mediator,
the reduced data channels obey the corresponding conjugation relation.
Since \(\Theta_D P\Theta_D^{-1}=P\), antiunitarity maps
\(U_\theta\) to \(U_{-\theta}\).

If one open-loop program had worst-input data trace-distance error at most
epsilon to the same target on both mirror sources, the triangle inequality
would give

\[
2\epsilon\ge\max_\rho
\tfrac12\|U_\theta\rho U_\theta^\dagger-
U_{-\theta}\rho U_{-\theta}^\dagger\|_1.
\]

For theta=pi/4 the right side is 1 (take a state with orthogonal P image).
Therefore epsilon is at least 1/2. This is a scoped obstruction to one
unconditioned program on that two-orientation class. It is not an inability
to acquire a sign, use measurement and feedback, or enlarge the physical
access. The earlier coplanar obstruction remains separately valid.

The source information required by the positive theorem is not literally
only one bit: the algebra, bounds, stability and nonzero gap are also
promises requiring qualification. Conditional on those, an orientation sign
is qualitatively different from an epsilon-accurate magnitude estimate.

## 11. Calibration, holding, and what has not been acquired

An ordinary controller with the same coarse information may use established
ensemble control, numerical minimax control, dynamically corrected gates,
or stronger native constructions. The positive theorem does not exclude
those alternatives. The supplied-model ordinary controller already wins the
finite fixture; its performance must not be compared against a structural-only
protocol while granting its model acquisition for free.

For an illustrative scalar calibration using bounded binary outcomes with
a locally nonzero signal slope s, estimating an angle to tolerance delta at
failure probability zeta by sample averaging requires order
\(s^{-2}\delta^{-2}\log(1/\zeta)\) samples under independent sampling
premises. This is an upper-bound method, not a quantum estimation lower bound.
Coherent long probes, prior information, adaptive estimation, correlated
samples, and SPAM uncertainty can change the accounting. A full unknown
physical dilation is not acquired by a scalar tolerance. No such physical
calibration experiment has been supplied here.

For R uses of a compiled gate the comparison should include

\[
T_{\rm task}=T_{\rm qualify}+T_{\rm acquire}+T_{\rm compile/test}
+R T_{\rm gate}+T_{\rm required\ holding/readout/reset}.
\]

Classical compilation time is distinct from hardware time. Source preparation,
measurement, reset duration and entropy export enter where the selected
calibration or computation actually needs them. The new unitary existence
construction itself neither resets the bus nor needs an entropy outlet, but
that does not grant free preparation/readout/control qualification. Unknown
data holding is not removed by the memory-only drift theorem. For the literal
long words its allowed residual budget can be exceptionally tight.

The useful conclusion is that precise parameter identification is not always
a necessary information contract for a logical gate. The unanswered efficiency
question is whether that contract can be exploited with practical native
control and holding errors, rather than paid for by enormous control words.

## 12. Preserved failures, scope, and primary context

The old dirty-register and dirty-input repair failures remain actual failures.
No reset is inserted in this argument. Logical release and apparatus readiness
remain different events. The scalar-calibration ordinary winner and the
retained-sector logical witness are both preserved. The latter is a real error
of the unmodified family, not an impossibility for all controllers. The
integer-clock alternative removes one irrational-duration requirement while
retaining its longer execution and actual timing-noise obligations. The
precision-limited smallest old numerical row is not promoted into evidence.

All old whole-lifetime/non-Markovian bounds retain their original initialization
and support hypotheses. This document neither constructs a threshold nor
supplies a reliable native controller for noisy hardware. It does not claim
universal computation from the three stated handles alone; adding reliable
single-qubit data gates would be a separate physical premise.

Selected primary context (the new algebra is derived above, not attributed to
these sources):

- Li and Khaneja, *Control of inhomogeneous quantum ensembles*, Physical
  Review A 73, 030302 (2006), https://doi.org/10.1103/PhysRevA.73.030302.
  Noncommutativity, Lie algebra, and compensation for parameter dispersion
  are prior. The abstract was inspected.
- Sakai, Soeda, Murao and Burgarth, *Robust controllability of two-qubit
  Hamiltonian dynamics*, Physical Review A 100, 042305 (2019),
  https://doi.org/10.1103/PhysRevA.100.042305. Robust unknown-parameter gate
  control, including restricted one-qubit control, is prior. The abstract
  was inspected; the observed full-text sign-in wall was not bypassed.
- *Environment-invariant measure of distance between evolutions of an open
  quantum system*, New Journal of Physics 12, 015001 (2010),
  https://doi.org/10.1088/1367-2630/12/1/015001. The arbitrary-environment-unitary
  objective is established. Search material was available; the denied full
  retrieval was not retried or replaced with another transfer.
- *High-fidelity spin entanglement using optimal control*, Nature
  Communications 5, 3371 (2014), https://www.nature.com/articles/ncomms4371.
  Subsystem optimal control is an active ordinary comparator.
- Khodjasteh and Viola, *Dynamical quantum error correction of unitary
  operations with bounded controls*, Physical Review A 80, 032314 (2009),
  https://doi.org/10.1103/PhysRevA.80.032314. Established dynamically corrected
  gates retain their full strength under matching premises.

No new external transfer, Library upload, worker, chat, model change, or
message to Capital is part of this work. New files are ordinary local working
proofs and runnable checks. No new independent reviewer is implied.

## 13. Executed next attack: necessary control action for unknown gain

The very large constructive pulse count above is not an impossibility result.
This section gives a separate necessary bound that applies to every finite
open-loop native word in a continuous unknown-gain subclass. Its logarithmic
accuracy dependence is much weaker than the literal construction's cost.

Fix any admitted noncoplanar reference triad and replace every coupling by
\(xB_j\), with \(x\in[a,b]\), \(0<a<b\). Allow any fixed physical
memory Hamiltonian and any initial memory state. The same chosen finite
native program must implement the target for every x in this interval.
Write its Hamiltonian as

\[
H_x(t)=I_D\otimes H_M+xG(t),\qquad
\mathcal A=\int_0^T\|G(t)\|dt.
\]

Here G includes the selected signs and any admitted bounded control
envelopes. The action \(\mathcal A\) is dimensionless in units with
hbar=1. If \(\|G(t)\|\le K\), then \(\mathcal A\le KT\).

For data input \(|00\rangle\), define the real response

\[
f(x)=\operatorname{Tr}\left[Z_2U_x
(|00\rangle\langle00|\otimes\sigma_M)U_x^\dagger\right].
\]

For the target \(e^{i\pi P/4}\), the desired response is zero. At x=0,
the physical program acts only on memory, so f(0)=1. If the program has
worst-input reduced-data trace-distance error at most epsilon for every x
in [a,b], then \(|f(x)|\le2\epsilon\) on that interval.

Repeated Duhamel differentiation gives

\[
\|\partial_x^n U_x\|\le\mathcal A^n,
\qquad |f^{(n)}(x)|\le(2\mathcal A)^n
\tag{8}
\]

for every real x. The first inequality follows from the n! time-ordered
insertion terms and the ordered-simplex integral; Leibniz's rule gives the
second. The statement is independent of memory dimension and memory-state
purity. It does not require a bath inverse.

### 13.1 Exact uniform implementation is impossible at finite action

The finite bounded-generator evolution has an analytic continuation in x.
If epsilon were zero on a nonempty open interval, the identity theorem
would make f identically zero, contradicting f(0)=1. Thus no fixed finite
native program exactly produces the entangler across the continuous gain
class. This does not preclude approximation to every positive accuracy,
parameter-dependent calibration, adaptive acquisition, or additional native
resources. It is consistent with Section 9's approximate positive theorem.

### 13.2 Explicit logarithmic accuracy lower bound

For n at least one, choose n+1 Chebyshev extrema mapped onto [a,b], and let
\(p_n\) interpolate f at those nodes. At the exterior point 0, the
absolute sum of the Lagrange interpolation weights is

\[
\left|T_n\left(-\frac{a+b}{b-a}\right)\right|
\le\rho^n,
\qquad
\rho=\frac{\sqrt b+\sqrt a}{\sqrt b-\sqrt a}>1.
\]

To see the equality for the absolute weight sum, order the extrema and
observe that the exterior Lagrange weights alternate in sign. Their signs
agree, up to a common factor, with the alternating values of the degree-n
Chebyshev polynomial. Interpolation reproduces that polynomial exactly.

The real interpolation remainder and (8), including the interval from 0 to
b, give

\[
1\le2\epsilon\rho^n+
\frac{(2\mathcal A b)^{n+1}}{(n+1)!}.
\tag{9}
\]

Choose \(N=n+1=\lceil4e\mathcal A b\rceil+2\). The factorial
bound \(N!\ge(N/e)^N\) makes the remainder no larger than
\(2^{-N}\le1/4\). Also \(n\le4e\mathcal A b+2\). Hence

\[
\epsilon\ge\frac38\rho^{-(4e\mathcal A b+2)},
\]

or equivalently

\[
\boxed{\quad
\mathcal A\ge
\max\left\{0,
\frac{\log(3/(8\epsilon))-2\log\rho}
{4eb\log\rho}\right\}.
\quad}
\tag{10}
\]

The first derivative alone also gives
\(\mathcal A\ge(1-2\epsilon)/(2a)\). The stronger of these two
bounds may be used. They are conservative but genuinely necessary for
this program class. A supplied controller already optimized around a known
model, or a controller with parameter-dependent acquired information,
belongs to a different premise set unless required to serve the whole
continuous gain interval with the same program.

The numerical values in uniform_control_certificate.json show the bounds
are far below the present word costs. Thus the cost gap remains an actual
open problem. Neither (10) nor the earlier sufficient Hamiltonian-error
bill supports a claim that the enormous constructive overhead is unavoidable.

## 14. Further consequences and operational boundaries of the information contract

### 14.1 Finite digital timing description

Irrational dilation in (2) is not essential to the existence result. The
palindrome

\[
S_+(\tau)^{2^{m-1}}S_-(2\tau)S_+(\tau)^{2^{m-1}}
\]

cancels degree m because \(2^m-2^m=0\), while the desired degree-k
coefficient is multiplied by \(2^m-2^k\ne0\). It has a larger number
of subwords but uses integer dilation. Rational amplitude PWM can then be
placed on a common rational grid. At any requested finite accuracy, the
remaining absolute times can be rounded to a sufficiently fine rational
grid using the bound \((D+B_0)\sum_j|\Delta t_j|\). This provides a
finite classical description and finite switching resolution at the expense
of a possibly enormous precision and control burden. It does not eliminate
actual clock jitter or sign asymmetry.

### 14.2 A conditional orientation-acquisition construction with retained memory

The positive theorem takes orientation as a supplied promise. If one ALSO
has independently qualified data preparation in |00> and Y2 readout, then
its sign can be learned without a precise magnitude estimate. This paragraph
does not acquire those additional operations from the three Hamiltonian
handles. Preparation, readout, duration, error and any entropy disposal must
be included physically; dirty-register reuse is not idealized into a reset.

Use the leading clean chirality primitive to implement a weak probe
\(\exp(i\alpha cP)\), with \(\alpha=\pi/(8c_+)\), on either
orientation class and with joint operator error at most \(1/(8\kappa)\).
For the ideal probe,

\[
\langle Y_2\rangle=\sin(\pi c/(4c_+)),\qquad
|\langle Y_2\rangle|\ge1/(2\kappa).
\]

The joint operator error changes the expectation by at most \(1/(4\kappa)\).
After charging any qualified preparation/readout errors, a positive
conditional mean margin \(\mu\) therefore suffices for sign estimation.

Memory need not be reset or independently sampled between trials. If the
uniform probe and qualified preparation/readout guarantees hold on every
conditional retained-memory state, each observed value \(Y_r\in\{-1,+1\}\)
has \(\operatorname{sign}(c)\mathbb E[Y_r\mid\mathcal F_{r-1}]\ge\mu\).
The conditional Hoeffding bound then gives

\[
\Pr[\text{wrong majority sign}]\le e^{-N\mu^2/2}.
\]

Thus N at least \(2\mu^{-2}\log(1/\delta)\) bounds the sign error by
delta without an independent-bath assumption. In the ideal additional
interface, one can take \(\mu=1/(4\kappa)\), giving
\(N\ge32\kappa^2\log(1/\delta)\). An exact symmetry, gap and native
control promise is still needed; this is not total source qualification by
one bit. The readout/preparation premise is deliberately explicit because
otherwise this would repeat the dirty-register failure in another form.

This separates three resources: a physical source-class promise, confidence
in a discrete orientation, and continuous native control action. It supplies
neither a free detector nor a reset. The ordinary controller is entitled to
the same promise, probe interface, coherent access, and data from acquisition.

## 15. Subsequent local-regularity extension

The complete working derivation in LOCAL_REGULARITY.md replaces the total
memory-Hamiltonian norm by finite-order norms of its action on the native
couplings. It gives an explicit derivative-majorant remainder and signed-only
amplitude compilation. An endpoint spin chain with on-site and bond terms
bounded by J satisfies h_r <= B0 (4J)^r r!, independently of chain length.
Thus one program serves arbitrarily large retained local baths under the
declared source promises. This extension has the same root-only working
status and does not remove the control, holding, qualification, or timing
costs. Unqualified all-Fock sources remain outside the claim.
