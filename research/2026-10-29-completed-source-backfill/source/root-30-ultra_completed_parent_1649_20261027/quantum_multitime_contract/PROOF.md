# A finite operating contract for a finite-memory quantum noise model

2026-10-27; same existing independent_opening_6 model; no new agents.
All results below are abstract constructions. No physical reset, memory
dimension, hazard bound, rational-height promise, shots, energy, or device
speed has been acquired.

## 1. What changes the acquisition question

Finite memory dimension alone does not make finite-shot calibration certify
an exact arbitrary-depth process. But it does give a finite **exact-data**
equivalence horizon if the process is homogeneous and a fixed initial
system-memory state is repeatably reset. This is an existing linear
realization fact. An explicit separation promise turns it into a finite
confidence test; its cost can be enormous.

A more informative concrete operation is possible in a specified five-state
noise-memory family. We construct a single calibration protocol that either
rejects or qualifies **every future adaptive program with a declared finite
noise-use budget H**, with a stated output-TV budget delta. Its operation
cost is O((H/delta)log(1/alpha)), and a coupling lower bound matches H/delta
up to the confidence factor. Under an additional known positive-hazard gap,
the same protocol gives an exact all-depth classification with finite
confidence. Without that gap, no finite expected-cost complete/sound
all-depth classifier exists, even though every isolated-use noise channel
is exactly the desired Phi_c.

This is a conditional model qualification operation, not a generic
non-Markovian hardware certification or a new process-tensor formalism.

## 2. The five-state family preserves the isolated channel exactly

Fix rational qubit c>c0 and s=1/(2c-1). The mandatory noise is the Pauli
mixture

    p_Y=(1+3s)/4,       p_I=p_X=p_Z=(1-s)/4.

The environment is classical with five labels F,H_I,H_X,H_Y,H_Z.
It starts in F under a supplied trusted reset. A fixed hazard p in[0,1]
controls a homogeneous CPTP noise operation:

* In F, draw P from p_P. Apply P. With probability p store H_P forever;
  otherwise retain F.
* In H_P, apply the same P and retain H_P.

This is a physical CP construction using classical random-unitary branches.
For off-diagonal environmental inputs, first dephase the environment in
these five labels. All superoperator entries are rational when c,p are
rational. There are five classical memory states regardless of how small p
is; no unbounded hidden timer is being smuggled into the dimension.

The immediate construction is one qubit noise interface. It also defines
a global five-label model on many wires if each call applies the selected
Pauli to the addressed wire with the same declared hazard/reset rule.
The coupling guarantee is dimension independent for that supplied model.
One-qubit calibration alone does not acquire this spatial/addressing promise
for a wider processor.

At deterministic call time t before the update,

    Pr[F]=(1-p)^(t-1),
    Pr[H_P]=(1-(1-p)^(t-1))*p_P.

Hence an independently prepared system input, with past observations averaged
and not used to select a biased key subensemble, sees **exactly Phi_c** at
every call time. This statement is not conditional independence from the
past: conditioning on earlier observations can bias H_P. A complete causal
break/process-tensor experiment sees that distinction.

The p=0 member is fresh independent Phi_c. For p>0 the held label is
eventually reached almost surely.

### A short exact process-tensor witness

The16 measure-and-prepare branches M_xy(X)=rho_x tr(rho_y X), with

    rho_0=I/2, rho_1=(I+X)/2, rho_2=(I+Y)/2, rho_3=(I+Z)/2,

are an informationally complete real superoperator basis. Each is a
physically admissible selected branch, with complement
rho_0 tr[(I-rho_y)X].

Start in |0>. The word of three selected M_33 branches has probability

    q^2 + p*q*(1-q),       q=(1-s)/2,

versus q^2 for fresh noise. The difference is p(1-s^2)/4.
For c=7/4,p=1/7, the exact probabilities are3/25 versus9/100.
This is an ordinary low-order process-tensor witness; it is not the
arbitrary-depth certificate.

The executable uses real Bloch coordinates (trace,x,y,z), so the Y controls
are retained exactly. It builds the20-dimensional classical-quantum
realization and the4-dimensional reference, checks the isolated-channel
identity on a linear basis, and independently runs the ordinary reachable
span algorithm on their24-dimensional direct sum. The p=0 instance has
reachable rank4 and no differing word. The p=1/7 instance has reachable
rank24 and a three-letter witness. Candidate counts are65 and385,
respectively. These are **given-model** algebraic checks, not a claim that
an unknown black box's matrices were acquired in polynomial experiments.

## 3. Indistinguishability for every finite adaptive calibration

Let a calibration protocol use arbitrary system interventions, observations,
random choices, resets, and stopping decisions. Let T be its expected total
number of local noise calls under the fresh p=0 model. Couple the two
experiments by using the same Pauli draws and controller randomness until
the first F-to-H trigger. Their complete records agree until such a trigger.
Therefore

    TV(calibration_p, calibration_0) <= p*T.

This holds also for unbounded stopping times with finite expected T:
sum over the trigger opportunities under the reference run, or use
E[1-(1-p)^N] <= p E[N]. Resets may erase a held label, but cannot increase
the probability of a first disagreement above this union bound.

In particular, if a protocol accepts p=0 with probability at least1-alpha,
then it accepts the p member with probability at least1-alpha-pT.
No selection of tomography settings or adaptive controls avoids this
inequality.

### The eventual process difference is almost maximal

Use echo blocks: prepare |0> as the first retained operation, incur noise;
apply identity, incur noise; finally read Z destructively when required.
The preparation is followed by the counted mandatory noise. It is not
an uncharged noiseless refresh.

For fresh noise each readout is0 with probability

    a=(1+s^2)/2 <=2/3.

In a held mode, two identical Pauli conjugations cancel and every block
readout is0. After K-m unobserved burn-in blocks, the probability of already
being held is1-(1-p)^(2(K-m)). Let E be the event that all last m readouts
are0. Then

    TV(future_p, future_0)
       >= 1-(1-p)^(2(K-m))-a^m.

For every p>0 this can be made arbitrarily close to1. Set k>=1,
m=2k, q=ceil(1/p), K=m+ceil(kq/2). Since
(1-p)^q <=1/(1+qp)<=1/2, the difference is at least1-2^(1-k).
For p=10^-9, k=10 this uses10,000,000,040 noise calls and yields the
rigorous lower bound511/512. A calibration with expected10^6 calls still
has record distance at most1/1000 from fresh noise.

Thus there is no finite expected-cost test that both accepts the fresh
model with high probability and rejects every p>0 member as unsuitable for
**uniform arbitrary-depth** exact simulation. All examples are homogeneous,
five-state, resettable, and have the exact same isolated Phi_c.
This is a sharp statistical obstruction, not a denial of the finite
exact-data theorem below.

## 4. A finite test that qualifies a declared future operating budget

Assume the device belongs to this five-state family, with fixed unknown p.
Assume the same trusted F reset is available before calibration and before
future operation. The Pauli probabilities and intended controls/readout are
specified as above. These are actual acquisition assumptions.

Choose an unsafe hazard threshold u in(0,1] and confidence parameter
alpha in(0,1/2). Let

    k = least integer with2^-k<=alpha,
    m =2k,
    q =ceil(1/u),
    K =m+ceil(kq/2).

Run K echo blocks, recording only the final m Z results.
**Reject if all final m results are0; otherwise issue the qualification.**

For p=0, the false rejection probability is a^m<=2^-k<=alpha.
For every p>=u, acceptance implies that no held mode was reached before
the last m blocks. Thus

    Pr_p[issue qualification] <=(1-p)^(2(K-m))
                               <=(1-u)^(kq)
                               <=2^-k<=alpha.

The last inequality is the elementary reciprocal-Bernoulli bound above.
No heralded outcome or small branch denominator is treated as free.

### Finite-program output guarantee

Let H>=1 be a maximum future number of local noise calls and delta in(0,1)
the requested output-TV budget. Put u=delta/H. If p<u, the same coupling
gives

    TV(actual, fresh reference) <=H p <delta

for **every** future adaptive quantum/classical program within that call
budget. This is a joint unconditioned transcript bound. Postselecting rare
histories can amplify it and is not granted as a free conditional guarantee.
The probability that the test issues this certificate for a device with
p>=u is at most alpha.

This is a frequentist error guarantee under the family/reset promise, not
a Bayesian probability that p<u conditional on an observed acceptance.
The exact reference frame sampler can then be used with this stated
operational model error. It is not exact simulation of an unknown continuous
physical parameter inferred from a finite sample.

The plan uses2K noise calls, K preparations, K identity updates, m destructive
readouts, one environmental reset before calibration, and another before
future operation. Only an operation counter and a Boolean/short tail counter
need be retained; the full calibration trajectory need not be stored.
Elapsed time is K times the acquired preparation-noise/identity-noise cycle
cost plus m readout costs and reset costs. No seconds, joules, or reset
fidelity have been acquired here.

Examples with c=7/4:

* H=100, delta=.1, alpha=.01:7,028 noise calls.
* H=10^6, delta=.01, alpha=.001:1,000,000,040 noise calls.

Those are computed plans, not executed physical calibrations.

### Necessary acquisition scaling

The dependence on H/delta is not a loose tomography artifact in this family.
Let 0<delta<=1/4, choose m with a^m<=delta/2, and let even H>=4m.
Take p=8delta/H. In H calls, the last-m-zero witness obeys

    TV >=1-(1-p)^(H-2m)-a^m
       >=4delta/(1+4delta)-delta/2
       >=3delta/2 >delta.

Here H-2m>=H/2 and (1-p)^n<=1/(1+np).
A qualifier that accepts the fresh model with probability>=1-alpha and
issues an invalid delta certificate with probability<=alpha must distinguish
this p model. Its calibration records have TV at least1-2alpha, while the
coupling bounds them by pT. Consequently

    T >= (1-2alpha)H/(8delta).

The constructed test is therefore within a logarithmic confidence factor
of the necessary H/delta scaling. This does not claim a new change-point or
hazard-testing algorithm; it gives a concrete operating contract and its
cost at the quantum process interface.

### Exact all-depth classification under a separated promise

If the additional supplied model promise is p=0 or p>=p_min>0, choose
u=p_min. Acceptance then identifies the exact fresh process with false
classification probability<=alpha, and the reference simulator applies at
all finite depths. At p_min=1/32, alpha=.001, the test costs360 noise calls.
The code checks its exact finite hidden-state readout law and probabilities.
The lower bound T>=(1-2alpha)/p_min follows directly from the same coupling.

Finite memory does not provide p_min. A rational digital control word does
not imply a lower physical transition rate. This promise must be supplied
from a separate physical/model argument; it was not acquired here.

## 5. General homogeneous finite-dimensional exact-data contract

For a system of Hilbert dimension h and memory dimension at most D, a
homogeneous joint CPTP transition and a fixed initial joint state have a
linear realization on Hermitian dimension r=(hD)^2.
A memoryless reference has r0=h^2. For a finite branch alphabet, write

    p(w)=beta T_(w_l)...T_(w_1) alpha.

The difference realization has dimension R<=r+r0. Its reachable spaces
V_j=span{T_w z0:|w|<=j} stabilize by j=R-1: if V_j=V_(j+1),
the span is invariant under every alphabet map. Starting with dimension1,
there can be at most R-1 strict increases.

If the trace difference annihilates every word of length<=R-1, it
annihilates the whole invariant reachable space. Hence equality of those
finitely many exact probabilities implies equality of all word probabilities.

For universal intervention slots, choose h^2 linearly independent rational
density matrices and h^2 linearly independent rational effects, and their
h^4 measure-and-prepare CP branches. Each has a physical complement.
They span real Hermiticity-preserving superoperators. Equality on all basis
words therefore extends by multilinearity to arbitrary supplied operation
branches and readout effects, including adaptive choices transcript by
transcript. Future controls must be legitimate interventions on the same
stationary process; arbitrary unmodelled gate-dependent changes to the
environment are not obtained by linear extension.

Thus a sufficient exact operational horizon is

    J=(hD)^2+h^2-1.

For a promised classical D-label memory, its block-diagonal joint state
space has dimension D h^2, improving this bound to(D+1)h^2-1.
Neither finite Hilbert dimension nor this finite realization rank implies
finite Markov order or short decaying correlations.

This is an established bilinear/quantum-machine equivalence principle,
not a new theorem of automata theory. Personally read Li–Qiu2006
arXivquant-ph/0604085v2, Section3.2, Definition4/Remark5/Theorem5:
[primary full text](https://arxiv.org/html/quant-ph/0604085v2).
The reduction to the controlled mixed-state CPTP realization is made
explicit here to state the physical assumptions.

The horizon applies per fixed system width: h=d^n for an n-site register.
A global-register bound is exponential in width, and no finite global test
for every unbounded register size follows. A local spatial-factorization
promise would be additional information.

## 6. A genuinely finite confidence contract under a rational-height promise

Suppose additionally, in a fixed rational Hermitian coordinate basis:

* all actual transition matrices T_a and the initial alpha have common
  denominator q<=Q;
* reference data have common denominator q0<=Q0;
* final trace functionals are integral;
* every calibration trial starts with an independent copy of the specified
  fixed system-memory state under the trusted reset.

The promise concerns the actual controlled transition matrices, including
the supplied intervention implementations. It is not inferred from a finite
computer's arithmetic or a rounded hardware fit.

Let J=(hD)^2+h^2-1 and S=sum_(l=1)^J(h^4)^l.
For a word of length l<=J, actual/reference denominators divide q^(l+1)
and q0^(l+1). Any nonzero probability difference therefore has magnitude
at least

    gamma=(Q Q0)^(-(J+1)).

For every one of the S words, run N independent reset trials and count the
all-selected-branches event. Hoeffding and a union bound give simultaneous
error<=gamma/4 with probability>=1-alpha when

    N >=8 gamma^-2 log(2S/alpha).

Accept iff every estimated word probability is within gamma/2 of its
reference. On the simultaneous good event, a nonzero difference cannot
pass; the finite exact-data theorem then implies exact equality for every
future depth. Conversely the exactly matching reference passes on that
event.

This is a finite-shot, finite-confidence **all-depth** certificate under a
discrete/separated model promise. Its total reset cost is S*N and noise-call
cost at most J*S*N. It is not an exact-observation oracle masquerading as a
finite measurement.

The cost calculator uses an integer upper bound on the logarithm.
Even h=2,D=1,Q=Q0=2 entails286,331,152 basis words and more than10^20 reset
trials at alpha=.01. For h=2,D=2,Q=Q0=20 the sufficient reset count has130
decimal digits. These are conservative sufficient plans, not optimal lower
bounds and not physical executions. The finite theorem is not a practical
calibration recommendation.

Without the denominator/separation promise, the continuously small-hazard
counterfamily in Sections2–3 remains admissible and defeats a uniform
finite expected-cost classifier. This is the precise boundary between
finite exact-data equivalence and finite operational acquisition.

## 7. Ordinary process-tensor comparison and status

Pollocketal2018's operational Markov criterion already uses measurement and
repreparation to expose environmental memory, and proves completeness of
linearly independent intervention controls over a specified finite horizon.
Its generalized Choi description captures multi-time correlations omitted
by channel snapshots:
[arXiv1801.09811v1, criterion and AppendixA](https://arxiv.org/html/1801.09811v1).
No claim of inventing that formalism, causal breaks, or finite-horizon
tomography is made here.

There are stronger practical and error-controlled incumbents as well.
Whiteetal2022 reconstructs and stitches conditional Markov-order process
tensors, with characterization scaling linear in the specified time span
and exponential in the chosen memory order; its model error is checked on
held-out control sequences. This does not turn a finite reconstruction into
an exact all-depth claim:
[arXiv2106.11722v2, IV and V.2](https://arxiv.org/html/2106.11722v2).
Taranto–Pollock–Modi2021 Thm1 bounds a recovered process's multi-time
observable error by its supplied memory strength and coefficient norm within
the tested instrument span. That existing positive transfer law requires
the appropriate memory-strength information; the present obstruction does
not refute it:
[arXiv1907.12583v2, Thm1](https://arxiv.org/html/1907.12583v2).

The short three-branch witness is an ordinary process-tensor measurement.
Using a fixed short witness with probability gap proportional to p requires
the usual O(p^-2 log(1/alpha)) Bernoulli estimation cost. The constructed
long echo screen instead pays O(p_min^-1 log(1/alpha)) calls under the
specific persistent-hazard family. An equally informed ordinary sequential
fault/change-point screen obtains the same hazard scaling. The gain comes
from the supplied structural model and longer temporal intervention, not
from a new general tomography speed claim.

Given transition matrices, reachable-span equivalence is polynomial in their
linear dimension. Unknown-matrix acquisition from black-box experiment is
not the same task; our general finite word contract retains the exponential
word count and its precision cost. Finite-D, fixed stationarity, trusted
controls/reset, rate/height separation, and model membership are all
unresolved physical acquisition obligations.

The general all-d root frame theorem passes the mathematical challenge in
FRAME_REVIEW.md at its snapshot scope. The new operational constructions
and code await independent review. Physical measurements, hardware speed,
energy advantage, and generic practical certification remain NOT_ACHIEVED.
