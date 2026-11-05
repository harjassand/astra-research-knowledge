# All-strength quantum experimental access from short-time control coverage

Research derivation by the `continuous_quantum` collaborator, 5 November 2026.
This note builds on the accepted P1 access model. It is a new proposed proof,
not a claim of historical priority or a working physical device.

**Scope correction after internal review:** Sections 2–3 give the sharper
constant for a global summed operator-norm decomposition, including coherent
controllers. Extending that exact constant to merely branchwise measured
feedback is not justified by nonchronological proof tags. Section 6 now gives
a separate chronological proof for the full measured-feedback scope, with
`B(t)` replaced by `k B(t)`. The fixed-`k` all-strength and matched peak/slew
scaling conclusions are unchanged. Any earlier statement in this collaborator
thread assigning the sharper coefficient to branchwise-only budgets is
superseded by this correction.

## 1. Exact model and normalization

There are source qubits `S_1,...,S_n`, initially carrying an arbitrary unknown
state; a receiver/controller `A` starts independently of that unknown input.
The noise actually present from time zero is inaccessible independent Markov
dephasing

\[
 \mathcal L_{\rm hid}=\lambda\sum_i(\operatorname{Ad}_{Z_i}-\mathrm{id}),
 \qquad \lambda>0.
\]

Every free retained operation, including all measurement records, is covariant
under every `Ad_{Z_i}`. Receiver-only operations are unrestricted. The remaining
Hamiltonian is decomposed into actual paid terms `H_a(u)` with

\[
 [H_a(u),Z_i]=0\quad(i\notin B_a),\qquad |B_a|\le k,
 \qquad h_a(u):=2\|H_a(u)\|.
\]

The P1 normalization is

\[
 \sum_{a:i\in B_a}h_a(u)\le\Omega(u),\qquad
 B(t):=\int_0^t\Omega(u)\,du.
\]

`B_a` is a commutation support, not necessarily ordinary tensor support:
unrestricted diagonal dependence on other source qubits is allowed. The source
itself is unavailable at the end. All acquired outputs and flags are included.
The original source cannot simply be handed to the decoder at time zero.

For `R` of size `w`, put

\[
 \mathcal P_R=\prod_{i\in R}\frac{\mathrm{id}-\operatorname{Ad}_{Z_i}}2,
 \qquad\|\mathcal P_R\|_\diamond\le1.
\]

The proof below treats an arbitrary finite coherent apparatus with the global
operator-norm budget. Genuine measured-feedback budgets are handled by a
different chronological recursion on the classical-record direct-sum algebra;
see Section 6. A measured-feedback controller satisfying the stronger global
decomposition budget also qualifies for Sections 2–3.

## 2. Fixed hidden-trajectory coverage lemma

Write

\[
 E_i=\frac{\mathrm{id}+\operatorname{Ad}_{Z_i}}2,
 \qquad\lambda(\operatorname{Ad}_{Z_i}-\mathrm{id})=2\lambda(E_i-\mathrm{id}).
\]

Thus the reduced joint source/apparatus evolution is an average over independent
Poisson clocks of rate `2 lambda` applying `E_i`. This is an analytical
unravelling of inaccessible noise; no clock or noise record is supplied to the
receiver.

Fix a trajectory of these clocks in `[0,t]`. Let `S` be the subset of `R` hit
at least once, and let `tau_i` be its first hit. Assume `0 < B(t) <= 1`.

**Coverage lemma.** For the complete joint source/apparatus channel on this
fixed noise trajectory,

\[
 \boxed{\|\Phi_\omega(t)\mathcal P_R\|_\diamond
       \le B(t)^{\lceil |S|/k\rceil}.}
\]

### Proof

Introduce real variables `x_i in [0,1]` for `i in S`. At time `u`, replace each
paid Hamiltonian term by

\[
 H_a^{\mathbf x}(u)=H_a(u)
       \prod_{\substack{i\in B_a\cap S\\u<\tau_i}}x_i.
\]

Every interpolated full propagator remains completely positive and trace
preserving: its Hamiltonian remains Hermitian, and its free operations and
fixed hidden jumps remain physical. With `x_i=0`, no noncommuting control on
site `i` occurs before its first `E_i`. All prior operations preserve its odd
sector, which `E_i` annihilates. Consequently `Phi_x P_R=0` on each face
`x_i=0`.

The proof recursively differentiates **one unresolved variable at a time**.
Consider a decorated trajectory: full interpolated propagators separated by
explicit commutator insertions `K_{a_j}=-i[H_{a_j},.]`, each possibly multiplied
by an interpolation coefficient of modulus at most one. Mark every source site
in `C=union_j B_{a_j}`, and let `U=S\C` be the unresolved sites. Let
`W=product_j h_{a_j}(u_j)` bound the product of insertion norms.

For every `i in U`, all inserted commutators commute with `Ad_{Z_i}`, and their
coefficients are independent of `x_i`. Therefore the decorated trajectory
still vanishes on the face `x_i=0`: the first `E_i` annihilates the odd sector
even when these explicitly inserted factors are present.

We prove by induction on `s=|U|` that its norm, with unresolved variables equal
to one and already-resolved variables at any values in `[0,1]`, is at most

\[
 W B(t)^{\lceil s/k\rceil}.
\]

For `s=0`, this is the product-norm bound using completely positive
contractions between insertions. For `s>0`, choose any `i in U` and apply the
one-variable fundamental theorem of calculus from `x_i=0` to `x_i=1`.
Existing insertions and their coefficients do not depend on `x_i`, so the
derivative acts only on full propagator segments. Duhamel's identity inserts
a new `K_a(u)` with `i in B_a` and `u<tau_i`; its scalar coefficient has modulus
at most one. Mark the entire `B_a`, not only the differentiated site. The new
residual size `s'` satisfies `s-k <= s' <= s-1`.

By induction, each new decorated term has norm at most

\[
 W h_a(u)B(t)^{\lceil s'/k\rceil}
 \le W h_a(u)B(t)^{\lceil s/k\rceil-1}.
\]

The open time intervals of all full propagator segments partition `[0,t]`
apart from insertion times of measure zero. Hence summing the new insertions
over all segments costs at most

\[
 \int_0^{\tau_i}\sum_{a:i\in B_a}h_a(u)\,du\le B(t).
\]

The integration in `x_i` has length one. Multiplication gives the claimed
induction step. Initially there are no insertions, `W=1`, and `U=S`, proving
the coverage lemma. This proof leaves all control not explicitly needed to
cover the hit sites inside physical contractions. It does not sum an unsigned
Dyson expansion over every control event.

## 3. Averaging and a time-uniform acquired-channel theorem

The clock-hit indicators on `R` are independent Bernoulli variables with
`p(t)=1-exp(-2 lambda t)`. Since
`B(t)^ceil(s/k) <= B(t)^(s/k)` for `B(t)<=1`, averaging the lemma yields

\[
 \boxed{\|\Phi(t)\mathcal P_R\|_\diamond
 \le \left[e^{-2\lambda t}+
       (1-e^{-2\lambda t})B(t)^{1/k}\right]^w.}
 \tag{1}
\]

This is a bound on the **whole joint source/apparatus** at the selected short
time. If acquisition continues beyond `t`, subsequent physical evolution and
source trace are contractions. If it stopped earlier, freeze the acquired
receiver output, set future paid source control to zero, and let the physical
source continue dephasing to `t`. The same recorded output is then the marginal
of an evolution to which (1) applies. Thus (1) bounds the eventual acquired
channel at any duration, with all heralding flags retained, under the global
decomposition budget. Stopping at a record-dependent time is represented by a
classical stop flag and freezing each stopped branch; finite caps and then
limits cover unbounded stopping. With only branchwise budgets, use Section 6.

For a constant peak envelope `Omega`, choose `t=1/(2 Omega)`, so `B(t)=1/2`.
The explicit all-strength bound is

\[
 \boxed{\|\mathcal N\mathcal P_R\|_\diamond\le f_w:=q_k^w,
 \quad q_k=e^{-\lambda/\Omega}+
       (1-e^{-\lambda/\Omega})2^{-1/k}<1.}
 \tag{2}
\]

It is valid for **every finite positive `Omega/lambda`**. If `Omega=0`, no
acquired transverse information is available. Equation (1) may be minimized
over any admissible short time rather than using the displayed convenient
choice. The original P1 weak-control bound remains stronger in part of the
weak-control range and can be combined by taking the smaller certificate.

For a constant envelope, any action level `b in (0,1)` gives

\[
 q_k(b)=e^{-2\lambda b/\Omega}
       +(1-e^{-2\lambda b/\Omega})b^{1/k}.
\]

In the strong-control asymptotic expansion, the best `b` for this bound is
`b=(k/(k+1))^k`. This gives the explicit alternative

\[
 q_k^{\rm opt}=1-\frac1{k+1}
 \left[1-\exp\left(-\frac{2\lambda}{\Omega}
                      \left(\frac k{k+1}\right)^k\right)\right],
\]

with leading loss
`[2 k^k/(k+1)^(k+1)] lambda/Omega`, asymptotic to
`2 lambda/(e k Omega)` as `k` grows. This action choice optimizes the leading
strong-control coefficient, not necessarily the exact finite-ratio bound.
The simpler `b=1/2` form is adequate for the main statements.

For fixed `k` and `Omega/lambda` large,

\[
 -\log q_k=(1-2^{-1/k})\frac\lambda\Omega
             +O_k((\lambda/\Omega)^2).
\]

Consequently downstream computation cannot eliminate an acquisition loss of
order `exp[-c_k w lambda/Omega]`, even at any fixed strong-control ratio.

## 4. Copy consequences

Here use `f_w=q_k^w` under the global decomposition budget. Under only
branchwise measured-feedback budgets, replace it by `q_(k,CQ)^w` from Section
6. All fixed-`k` scaling statements below hold for either certificate.

For a transverse Pauli `P` of weight `w`, consider
`rho_+/-=(I +/- aP)/2^n`, with `0<a<=1`. Their acquired trace distance is at most
`a f_w`. A hybrid argument over `M` fresh copies, allowing collective
ingestion, adaptive control and arbitrary protected computation, gives

\[
 M\ge\frac{1-2\zeta}{a f_w}
\]

for equal-prior discrimination error at most `zeta<1/2`.

For `rho_coh=|GHZ+><GHZ+|` versus its diagonal mixture, the purities are `1`
and `1/2`, their difference is odd under every `Z_i`, and its trace norm is
one. Therefore

\[
 M\ge 2(1-2\zeta)f_n^{-1}.
\]

This is a worst-case constant-gap purity-testing lower bound, not a statement
that every state's purity is difficult or a universal purity upper bound.
At fixed `k`, polynomial-copy testing at increasing `n` requires

\[
 \Omega/\lambda=\Omega(n/\log n)
\]

in the strong-control scaling regime. At any fixed finite `Omega/lambda`, the
copy requirement is exponential in `n`.

Requiring a fixed nonzero one-copy contrast, or a fixed number of copies,
instead requires `Omega=Omega(n lambda)` at fixed `k`; the local meter below
matches this scale. Polynomially many copies permit the logarithmic saving.

## 5. Matching peak and zero-start slew scales for promised global parity

Ordinary parallel local meters supply the strongest same-access baseline.
On each source qubit couple a protected meter by

\[
 H_i(u)=\frac{\omega(u)}2X_i\otimes Y_{A_i}.
\]

With meter initial `|0>`, the normalized contrast obeys

\[
 \dot a=\omega b,\qquad\dot b=-\omega a-2\lambda b,
 \qquad(a(0),b(0))=(0,1).
\]

For a constant pulse `omega=Omega>lambda`, write
`v=sqrt(Omega^2-lambda^2)`. The contrast at
`T=arctan(v/lambda)/v` is exactly

\[
 \beta=\exp\left[-\frac\lambda v\arctan\frac v\lambda\right]
        =\exp[-\pi\lambda/(2\Omega)+O((\lambda/\Omega)^2)].
\]

Each local outcome implements the attenuated `X_i` measurement, so the product
outcome is an unbiased contrast-`beta^n` meter of `X_1...X_n`. Estimating its
mean to a constant promised gap costs

\[
 M=O\bigl(a^{-2}\beta^{-2n}\log(1/\zeta)\bigr)
      =\exp[O(n\lambda/\Omega)]\,\operatorname{poly}(a^{-1},\log(1/\zeta)).
\]

Thus for fixed `k`, the strong-control **exponential order** matches the new
lower bound. The constants in the sample exponent are not claimed sharp.
This upper bound covers the stated parity and GHZ promises, not arbitrary
unknown-state purity estimation.

The constant pulse is the peak-controlled baseline. A finite-slew version can
start and end at zero. Suppose the *summed per-site action envelope* is
`Omega(u)<=min(Omega,K u)`. This follows, for example, if all paid terms start
at zero and their summed per-site norm-slew is bounded by `K`; merely assigning
a separate slew cap to infinitely many switchable terms would not suffice.

Let `t_*` be the earliest time the envelope's integral reaches `1/2`:

\[
 t_*=\begin{cases}
  K^{-1/2},&\Omega\ge\sqrt K,\\
  (2\Omega)^{-1}+\Omega/(2K),&\Omega<\sqrt K.
 \end{cases}
\]

Equation (1), with `B(t_*)<=1/2`, gives

\[
 f_n\le[1-(1-2^{-1/k})(1-e^{-2\lambda t_*})]^n.
\]

Its polynomial-copy consequences at fixed `k` are both

\[
 \Omega/\lambda=\Omega(n/\log n),\qquad
 K/\lambda^2=\Omega((n/\log n)^2).
\]

For a fixed number of copies these strengthen to
`Omega=Omega(n lambda)` and `K=Omega(n^2 lambda^2)`.

A local triangular/trapezoidal pulse of area `theta=pi/2`, peak `Omega` and
slew `K` has duration

\[
 T=\begin{cases}
 2\sqrt{\theta/K},&\Omega\ge\sqrt{\theta K},\\
 \theta/\Omega+\Omega/K,&\Omega<\sqrt{\theta K}.
 \end{cases}
\]

It would achieve contrast one without dephasing. Duhamel comparison of the
two-dimensional dissipative evolution with its noiseless rotation gives
`beta>=1-2 lambda T`. When `2 lambda T<=1/2`,
`beta>=exp(-4 lambda T)`, and the product meter uses
`M<=O(exp(8 n lambda T) a^-2 log(1/zeta))` copies. Since
`T=Theta(max(Omega^-1,K^-1/2))` up to constants, the peak and slew scales above
are sufficient as well as necessary for polynomial copies of these promises.

Per copy the construction pays `n` prepared protected meter qubits, `n`
parallel source interactions, pulse duration `T`, `n` meter measurements and
`O(n)` classical parity work. Source preparation, meter reset/readout latency,
calibration, physical implementation error and memory protection are added
costs. Parallel hardware does not make the total interaction work vanish.
At polynomial contrast, calibration/implementation precision needed to keep
bias below that contrast is polynomial as well; this is a control-model result,
not a finite-bandwidth laboratory implementation.

## 6. Full retained instrument and measured feedback

The lower bound applies to the full acquired instrument, including failed
flags and all records. A source-only averaged channel being `Z` covariant is
insufficient: retained `X` measurement outcomes would violate the model.

For a coherent controller, all insertion norms use the declared global
operator-norm decomposition and the proof is in ordinary diamond norm.

For genuinely measured feedback, the physical record is classical. Work on
the direct-sum algebra `oplus_m B(H_quantum)` with trace norm
`sum_m ||X_m||_1`, including an arbitrary quantum reference. Do **not** apply
Section 2's nonchronological proof tags directly: a newly chosen unresolved
site could then depend on a later record while its derivative insertion is
earlier in physical time. A sum of branchwise budgets would not justify that
step.

Instead fix the hidden trajectory on `[0,t]` and work chronologically. For an
unresolved set `U`, each of whose first hidden cuts is still in the future,
let `F_U(u)` bound the future full joint channel on its odd sector. Remove all
Hamiltonian terms touching `U` from a free propagator `V_U`. This propagator
preserves all unresolved parity sectors and annihilates the input by the first
deadline

\[
 d_U=\min_{i\in U}\tau_i.
\]

Duhamel at the first paid insertion touching `U` gives

\[
 F_U(u)\le\int_u^{d_U}\sum_{a:B_a\cap U\ne\varnothing}
 h_a(v)F_{U\setminus B_a}(v)\,dv.\tag{3}
\]

The integral after `d_U` vanishes because the free trajectory has already
been cut. Every remaining unresolved deadline is later than an insertion
time in (3). The new support and record are therefore known at that time;
subsequent recursion never chooses an earlier insertion using a future tag.

Let `b(u)=integral_u^t Omega(v) dv` and assume `k b(0)<=1`. Induction on
`s=|U|` gives

\[
 F_U(u)\le[kb(u)]^{s/k}.
\]

Indeed, if an insertion removes `j<=k` unresolved sites, then
`[kb(v)]^((s-j)/k) <= [kb(v)]^(s/k-1)`. The per-record summed budget gives
`sum_(a touching U) h_a(v)<=s Omega(v)`. Extending the integral to `t` now
yields exactly

\[
 \int_u^t s\Omega(v)[kb(v)]^{s/k-1}\,dv=[kb(u)]^{s/k}.
\]

For CQ control, apply this inequality in each physical record block and sum
the block trace norms. The choice of unresolved set and future continuation
is chronological, so its tags can be retained as classical direct sums.
Physical transitions between records are CPTP contractions. This uses
per-record budgets without summing maxima over mutually exclusive records.

Averaging the hidden hits therefore proves the fully retained CQ certificate

\[
 \boxed{\|\mathcal N\mathcal P_R\|_\diamond\le
 \left[e^{-2\lambda t}+(1-e^{-2\lambda t})
                   (kB(t))^{1/k}\right]^w,\quad kB(t)\le1.}\tag{4}
\]

For constant peak budget choose `t=1/(2k Omega)`:

\[
 q_{k,\rm CQ}=e^{-\lambda/(k\Omega)}
       +(1-e^{-\lambda/(k\Omega)})2^{-1/k}<1.
\]

This retains the full original measured-feedback scope for every finite
strength ratio. Its constants are weaker, but all fixed-`k` copy, peak and
slew scaling statements in Sections 4–5 remain valid after replacing `q_k`
by `q_(k,CQ)`. For a zero-start envelope, select the time at which its action
reaches `1/(2k)`, rather than `1/2`:

\[
 t_{*,\rm CQ}=\begin{cases}
 (kK)^{-1/2},&\Omega\ge\sqrt{K/k},\\
 (2k\Omega)^{-1}+\Omega/(2K),&\Omega<\sqrt{K/k}.
 \end{cases}
\]

No ordinary diamond-norm claim is made for hypothetical coherent
superpositions of classical record labels based solely on branchwise budgets;
the resulting initialized source-to-output channel has the operational
diamond bound. Coherent controllers are covered using the declared global
decomposition and the sharper Sections 2–3 theorem.

## 7. Scope and primary comparison sources

The new claim is the finite-window coverage proof and its all-strength
consequence in the exact accepted P1 model. It does not settle continuous
Hamiltonian output-only recovery with coherent depolarizing ports. That is a
different access model and remains open here.

The assumptions remain independent inaccessible Markov dephasing, initially
unencoded source data, bounded source commutation order, an actual summed-term
budget, full retained covariance of unpaid operations, and no direct final
source readout. Correlated noise, hidden memory, protected input encodings,
available noise purifiers and native extensive couplings change the premises.

Governing accepted source:
https://github.com/harjassand/astra-research-knowledge/blob/5cfc803599d9f95cfa0a55896fb580e77567e162/research/returns/2026-11-05-p1-experimental-access/package/Astra_P1_Quantum_Experimental_Access.tex

Its original proof explicitly leaves exponential bounds at every fixed strong
control ratio unresolved. Its existing meters supply the two-dimensional
equations used in Section 5.

Relevant external comparisons to inspect for priority and mechanism:

* Cotler, Gong, Kannan, *Noisy quantum learning theory*,
  https://arxiv.org/html/2512.10929v2 (noise-sensitive learning/purity limits;
  different access/noise placement must be compared exactly).
* Christandl, Fawzi, Goswami, *Fault-tolerant quantum input/output*,
  https://arxiv.org/abs/2408.05260 (residual input/output noise and protected
  architectures; does not grant pre-encoding of this unknown source).
* Terhal and Burkard, *Fault-tolerant quantum computation for local
  non-Markovian noise*, https://arxiv.org/abs/quant-ph/0402104 (local fault-path
  norm/resummation techniques, relevant methodological antecedent).
* Aharonov, Kitaev, Preskill, *Fault-Tolerant Quantum Computation with
  Long-Range Correlated Noise*, https://arxiv.org/abs/quant-ph/0510231 (summed
  interaction norms and local noise strength; a related proof technology,
  not claimed new here).

Historical novelty is not established merely by this derivation.

The lower/upper exponential-order and peak/slew matching claims hold at fixed
`k`. The sharper global-budget bound has strong-control exponent of order
`n lambda/(k Omega)` when `k` is large; the chronological branchwise-budget
bound has order `n lambda/(k^2 Omega)`. Independent local or block meters in
their fast regime have exponent of order `n lambda/Omega`. No matching
large-`k` interaction-order law is claimed. The original weak-control theorem
retains its separate stronger large-`k` conclusions.

## 8. Current independent review and executed checks

The parent and the `rare_interventions` collaborator independently inspected
the decorated-propagator recursion and found its boundary-vanishing,
support-marking and time-integral induction consistent under the global
budget. Later review identified the measured-feedback tagging issue; the
chronological Section 6 proof corrects that scope with a weaker constant.
This is an internal mathematical review, not peer review or a
historical-priority determination.

The adjacent program `check_coverage.py` executed 120 finite-dimensional fixed
hidden-noise trajectories, with 2–4 source qubits, interaction order 1 or 2,
action budgets 0.2/0.5/0.8, a shared receiver, piecewise paid controls, repeated
hidden hits, and strong commuting backgrounds. All satisfied the new
trajectory bound; the maximum observed trace norm divided by the bound was
0.20881396899958496. Seven strong-control meter ratios from 1.01 to 1000 agreed
with the analytic contrast to absolute error below `1e-9`. The complete data
are in `coverage_checks.json`. These floating-point examples are falsification
checks, not interval certificates, exhaustive checks or substitutes for proof.
