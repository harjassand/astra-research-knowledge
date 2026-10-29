# Complete frozen-control laws need not determine chronological control

29 October 2026, Brisbane. Complementary construction for Astra P1's
intervention-information question. This note is a finite mathematical
counterexample and a conventional discriminating assay, not a physical
source claim. Earlier sufficient mean records remain valid at their scope.

## 1. Two actual controlled Markov sources

There are three hidden live states, labelled 1,2,3 only in the producer,
and one observed absorbing state D. A reset prepares the known uniform
law alpha=(1,1,1)/3. It does not reveal the sampled hidden state. The
observer may retain every native jump time and distinguish the terminal
absorption from a nonterminal jump. Hidden state identities are not read.

Fix 0<r<1. Let E_ij be the three-by-three matrix unit. At control u in
[0,1], the first source has killed generator

    Q(u)=-I+r[(1-u)E_12+u E_23].                      (1)

The second source has killed generator Qbar(u)=Q(u)^T. Complete each
generator by the absorption column q(u)=-Q(u)1 and an absorbing last row.
The column is different in the two sources; it must not be held fixed
when transposing. Explicitly,

    q(u)    =(1-r(1-u), 1-ru, 1)^T,
    qbar(u) =(1, 1-r(1-u), 1-ru)^T.                  (2)

All off-diagonal rates are nonnegative, every live total native departure
intensity is exactly 1 for every u in both sources, and every killing
hazard is at least 1-r. Thus these are positive finite CTMCs with the
same known native holding clock and known reset, not merely signed
linear realizations. The known clock is the TOTAL departure intensity;
the hidden destination/absorption branching law is not supplied.

## 2. Every frozen-control experiment agrees exactly

Write B(u)=Q(u)+I. Since B(u)^3=0,

    alpha exp[tQ(u)]1
      = exp(-t)[1+rt/3+r^2 u(1-u)t^2/6].             (3)

Scalar transposition shows alpha exp[t Qbar(u)]1 equals (3) for every
u and t. Therefore the complete absorption-time law is identical under
EVERY constant control, including all real mixtures u in [0,1].

Even observing all native nonterminal jump times does not repair this
frozen experiment. At a fixed u the live embedded kernel is B(u), and
the probability of surviving k native jumps is alpha B(u)^k 1. Those
numbers agree by transposition. The total holding times are independent
unit exponentials, so the complete sequence of native tick times up to
absorption, with its terminal mark, has the same law. Resetting and
choosing a new constant u adaptively from previous frozen experiments
also leaves the two data laws identical by induction.

## 3. A two-pulse protocol separates the sources

Use A: u=0 for time t1, then B: u=1 for time t2. Row distributions evolve
chronologically by right multiplication. The source survivals are

    S_AB = exp[-(t1+t2)] [1+r(t1+t2)/3+r^2 t1 t2/3],
    Sbar_AB = exp[-(t1+t2)] [1+r(t1+t2)/3].           (4)

Their difference is

    Delta=exp[-(t1+t2)] r^2 t1 t2/3 > 0.            (5)

The cross term records the chronological route 1->2->3. Transposition
reverses the required route order. The source under the reversed pulse
order BA has the transposed source's AB survival and conversely.

At r=3/4 and t1=t2=1,

    S_AB=27 exp(-2)/16,
    Sbar_AB=3 exp(-2)/2,
    Delta=3 exp(-2)/16 > 1/40.                       (6)

Consequently complete frozen-control laws, a known uniform reset and
known total departure clocks do not universally supply a switched law.
This remains an information failure after infinitely many exact frozen
experiments. The missing information is chronological and joint, not a
more accurate estimate of any frozen marginal.

## 4. General algebraic explanation

For a common known native clock lambda and substochastic live kernels
B_a, frozen randomized action weights u_a produce B(u)=sum_a u_a B_a.
The data alpha B(u)^k 1 determine the COMMUTATIVE coefficients

    sum_{words w with letter-count vector m} alpha B_w 1.              (7)

These are sums over different chronological words. Knowing the entire
polynomial for every u does not generally recover each ordered
coefficient alpha B_a1 ... B_ak 1. The pair above exchanges AB and BA
while preserving every sum in (7).

This is an application of the distinction between noncommutative
input-output series and their commutative specialization. The algebraic
idea itself is classical bilinear/weighted-automaton realization theory;
the note claims the explicit positive, equal-clock counterexample and
its scope as a useful construction, not priority for that theory.

## 5. What actually suffices and its conventional cost

An ordered controlled input-output law is sufficient for all protocols
at its declared interface. For a finite action/observation alphabet,
matrices indexed jointly by actions and observations give path
probabilities as ordered products. Feedback policies weight those same
paths by their conditional action probabilities, so equality of the
complete controlled word law implies equality under every such policy.
Finite linear rank gives the familiar PSR/observable-operator quotient.
This exact representation is not a new Astra theorem or an acquisition
shortcut. Singular directions, histories of small probability, model
positivity and the completeness of a finite core remain real obligations.

For the declared TWO-HYPOTHESIS source class in this note, a much simpler
equally informed procedure suffices: repeat the AB protocol and count
survival at time 2. The decision threshold is

    midpoint=51 exp(-2)/32.

With N independent resets, a threshold test has error at most
exp(-N Delta^2/2) under either hypothesis by Hoeffding. The weaker exact
bound Delta>1/40 gives error <exp(-N/3200). This is ordinary binary
testing. It acquires the additional ordered experiment instead of
pretending that frozen-law information already contains it.

The executable performs N=65536 separate native trajectories from EACH
source under AB, retaining event times, terminal/censor marks and elapsed
time. Thus 131072 reset preparations and their actual source time are
charged. Every path is censored at time 2; nominal scheduled horizon is
262144 clock units, while absorption can stop earlier. The ideal-law
error bound is <exp(-20.48)<2e-9 per source. The simulation uses standard
floating exponential and categorical generation; no physical assay or
full floating-distribution proof is claimed. Hidden start identities are
not included in the consumer record. Exact symbolic checks, rather than
finite Monte Carlo, prove agreement for all frozen controls.

The saved execution used 133648 native jumps and 134074.82196274836
elapsed source clock units. The forward source produced 14920 survivors
out of 65536; the transpose source produced 13465. Both ordinary threshold
decisions were correct. Two retained NPZ files contain individual visible
records; exact rational brackets determine the decision threshold. This
small experiment validates the declared assay construction and does not
upgrade the mathematical model class or identify an arbitrary source.

## 6. Composable finite-horizon stopping without hidden-state identification

For the common-clock interface, suppose actual action/outcome word laws
have been acquired exactly through K native ticks. Apply any admissible
feedback policy and stop prediction after K ticks. Coupling the true and
prepared stopped output histories gives the general residual bound

    TV(full law on [0,T], stopped law on [0,T])
       <= Pr{Poisson(lambda T)>K}.                   (8)

The counted ticks must be those of an actually supplied uniformization
or common native-clock interface; an unobserved auxiliary clock is not
free experimental access. The stopped process can be represented by a
history tree, requiring exponentially many words in K in general. An
acquired finite-rank quotient may compress this tree but does not erase
rank acquisition, conditioning or coefficient precision costs. Equation
(8) is a standard coupling consequence, included to make the finite
scope explicit; it is not a claim of an efficient universal learner.

## 7. Astra and primary antecedents inspected

Astra N713's current capsule was fetched through all three continuation
pages, with governing source lines 81--130. It supplies controlled
autonomy from a calibrated closure Gram and a controlled-path bound
under explicit mixing and actuator assumptions. Its current N718/N736
notices retain product-control and occupation-law qualifications. This
note does not reprove or strengthen that theorem and does not infer its
actuator contract here.

Singh, James and Rudary, UAI 2004, Predictive State Representations:
A New Theory for Modeling Dynamical Systems, describes controlled-test
prediction states and finite system-dynamics rank. Search snippets and
the arXiv PDF's Sections 1--2 were read. The author-hosted PDF timed out,
then the arXiv PDF supplied the primary text.
https://arxiv.org/abs/1207.4167

Kiefer, Murawski, Ouaknine, Wachter and Worrell, Language Equivalence for
Probabilistic Automata, CAV 2011: author PDF Section 2 and the basis
algorithm were read. It supplies conventional finite-dimensional
equivalence tests and exact weighted-word representations, with explicit
numerical stability discussion. This is a stronger equally informed
baseline than enumeration when both finite models are supplied.
https://people.mpi-sws.org/~joel/publications/langeqprobaut11.pdf

No historical priority, autonomous hidden-model acquisition or generic
control advantage is asserted. The consequential lesson for the main
research is that intervention information must be closed under temporal
composition; complete families of frozen laws can still miss that closure.
