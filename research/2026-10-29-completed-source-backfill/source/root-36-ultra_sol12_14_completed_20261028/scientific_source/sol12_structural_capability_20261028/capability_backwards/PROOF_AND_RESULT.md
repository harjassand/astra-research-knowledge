# A moderate-flip parity control for the full five-letter separation

Status: exact constructive model comparison acquired. A new high-impact
physical operation was **NOT_ACHIEVED**. Generic lifting and generalized
detailed balance are established prior methods. External priority of the
specific finite-window lemma and application here is **UNKNOWN**.
The original N541 even-hidden-state theorem is not contradicted.

The output is a rational, irreducible, aperiodic twenty-state model with
the same complete stationary five-letter table as N541's discrete
ten-state target, and exact zero path KL under a specified hidden parity.
An explicit six-letter probability distinguishes the models. No physical
parity, heat/work semantics, equilibrium device or experimental preparation
was acquired.

## 1. Exact input and protocol

Matrices act on column functions; transition matrices are row stochastic.
Let P be supplied with positive stationary row law pi. Its stationary
adjoint is P*=diag(pi)^(-1) P^T diag(pi). The deterministic emission map h
has indicators g_a(i)=1_{h(i)=a} and projections E_a=diag(g_a). Assume

    (P-P*)g_a=0                       for every letter a,          (1)

and min_i P_ii>0. Choose 0<delta<min_i P_ii.

At pinned revision `8d51d60762b3ee28c10aaaa56e1b92da119dc1cc`, the source
supplies rational ten-state Q. The actual acquired protocol is **five
consecutive stationary discrete ticks** of

    P=I+Q/2,       pi_i=1/10,       h=(0,0,0,0,0,1,2,3,4,5).        (2)

These are uniformization/discrete indices, including virtual self steps.
No equality for exp(tQ), observations at fixed physical times, arbitrary
lags or the earlier CTMC is inferred. Although a lifted continuous-time
generator can be defined, it is not an acquired matching countercontrol.
The N507/N511 continuous-time protocols are not transported here.

Exact inputs are preserved in `sources/seed_certificate.json`; the source
proof and its audit output are copied read-only. Its universal even-hidden
inequality is source-reported, not newly fully audited here. The main
table equality needs only the finite algebra proved below.

## 2. Parity-reversible lift

On two copies of the state space put

    R_delta = [ P-delta I      delta I
                delta I       P*-delta I ],
    pi_hat=(pi/2,pi/2),
    J(+,i)=(-,i),       J(-,i)=(+,i),       h_hat(+,i)=h_hat(-,i)=h(i).

Entries are nonnegative, rows sum to one, and pi_hat R_delta=pi_hat:
blockwise, pi P=pi P*=pi. The involution J preserves pi_hat and emissions.
The stationary adjoint satisfies

    R_delta*=J R_delta J,                                        (3)

since adjunction interchanges P and P* and leaves delta I fixed. Thus

    pi_hat(x) R_delta(x,y)=pi_hat(Jy) R_delta(Jy,Jx).               (4)

Multiplication along any stationary path telescopes the stationary factors:

    pi_hat(x_0) prod_t R_delta(x_t,x_(t+1))
      =pi_hat(Jx_n) prod_t R_delta(Jx_(t+1),Jx_t).

The path law therefore equals its image under parity plus time reversal;
their KL divergence is exactly zero at every finite path length. This
uses the specified involution J. It does not identify physical entropy
production without a physical reversal and thermodynamic model.

If P is irreducible, within-copy paths and positive flips make R_delta
irreducible. Positive self loops give aperiodicity. Section 6 supplies a
stronger exact minorization for the actual instance. The orientation
function chi(+,i)=1, chi(-,i)=-1 has eigenvalue 1-2delta.

Two-replica/skew-detailed-balance methods are prior; see
[Turitsyn, Chertkov and Vucelja, Section 4](https://www.mit.edu/~turitsyn/assets/pubs/Turitsyn2011ik.pdf).
The importance of the specified reversal is also prior; see
[Maes and Redig, Section 2 and Proposition 2.1](https://fys.kuleuven.be/english/staff/christ/files/pdf/pub/10-1023-a-1026434726635.pdf).

## 3. Finite-window invariance lemma

**Lemma.** Under (1), every stationary five-letter probability of R_delta
is independent of delta. If P's five-letter law is reversal symmetric,
the two five-letter tables coincide. Shorter stationary windows agree by
marginalization.

**Proof.** Define future-two-letter conditional vectors

    f_ab(delta)=R_delta Ehat_a R_delta ghat_b.

Hats repeat emissions in the two copies. First,

    R_delta ghat_b=(Pg_b,P*g_b)=(v_b,v_b),

by (1). Applying Ehat_a still gives an even vector (u,u). For any such
vector, R_delta(u,u)=(Pu,P*u), independent of delta. Thus f_ab(delta)
is independent of delta, although its two blocks need not coincide.

Condition a stationary word (a,b,c,d,e) at its middle hidden state. By (3),
emission commutation with J, and J ghat_a=ghat_a, its past conditional is

    R_delta* Ehat_b R_delta* ghat_a=J f_ba(delta).

Consequently

    p_delta(a,b,c,d,e)
      =<Ehat_c J f_ba(delta), f_de(delta)>_(pi_hat).                (5)

This is independent of delta. At delta=0, the copies do not communicate:

    p_0(w)=(p_P(w)+p_P*(w))/2
          =(p_P(w)+p_P(reverse(w)))/2.

Both assertions follow. Evaluating delta=0 in this identity is legitimate;
the actual acquired chain has delta=1/10>0. QED.

Condition (1) is sufficient, not a characterization. There is no all-word
equality claim for positive delta: Section 6 exhibits a six-letter
difference. Both projected processes are individually reversal symmetric.

If data consist of independent stationary five-letter windows, any number
of such windows has the same law under the two models. No test of that
data can distinguish them. Dependent overlapping windows from a continuous
record can contain longer-word information; the consequence does not
apply to that richer contract. The null here is kinematic hidden-parity
reversibility, not physically acquired equilibrium.

## 4. Exact hypothesis checks on the source

Both code paths reconstruct (2) and verify nonnegativity, row/column sums,
and (1) with exact arithmetic. Uniform stationarity gives P*=P^T. Its
minimum diagonal is

    102892640873355762766245124564893327359
    /198122509475572307019443339309360640000
    =0.5193384696454292...,

so delta=1/10 leaves substantial positive self-loop slack.

Source reversal symmetry also follows structurally. Supplied H (ten by
eight), L and M (eight by eight) obey, exactly,

    QH=HL,        M=H^T H/10,        ML=L^T M,        rank(H)=8.

The constant function belongs to V=range(H). Each E_a preserves V: its
coordinate action on H is projection onto the first three coordinates for
a=0, and onto the corresponding marker coordinate for a=1,...,5. Q,
hence P, is self-adjoint on V in the stationary inner product because
ML=L^T M. The emissions are also self-adjoint. For every word,

    <1,E_a0 P E_a1 ... P E_an 1>_pi

stays in V. Taking its adjoint reverses the word and preserves the value.
Thus all observed words are reversal symmetric. The main consumer also
exhaustively checks all five-letter reversal identities independently of
this argument.

## 5. No parity on the frozen ten-state realization

The five uniquely labeled marker states must be fixed by any
emission-preserving permutation. Uniform pi adds no restriction. Of the
5!=120 within-emission permutations, 26 are involutions. All 26 fail

    P_ij=P_(theta(j),theta(i)).                                   (6)

There is also an exact structural reason. All internal-marker rates are
symmetric: P_ik=P_ki for i<5<=k. The five marker signatures
(P_i5,...,P_i9), i=0,...,4, are distinct. Applying (6) with a fixed marker k
gives

    P_ik=P_(k,theta(i))=P_(theta(i),k).

Thus theta must fix every signature and hence every internal state. It
must be the identity; P is not symmetric, so that fails too.

This excludes parities only on the **frozen supplied** representation. It
proves neither twenty-state minimality nor absence of another ten-state
realization. Dimensions eleven through nineteen and alternative
realizations were not classified.

## 6. Acquired comparisons and finite mixing

`construct_parity_control.py` saves three exact matrices in
`EXACT_MATRICES.json`: P (ten states), R_(1/10) (twenty), and ordinary
additive reversiblization A=(P+P*)/2 (ten). All receive the same supplied
P,pi and emissions. Additive reversiblization is established; see
[Aldous and Fill, Section 9.4](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch9.S4.html).
This control is not claimed to optimize a fitting criterion. The source's
stronger universal exclusion of ordinary reversible hidden models remains
a source theorem at its declared even-hidden scope.

The common integer denominator has 150 bits. The test exhausts all
6^5=7776 words, including zero-probability words. Each of the three models
has 576 positive entries. Equalities below are exact; decimals are displays.

| Quantity | P | R_(1/10) | ordinary A |
|---|---:|---:|---:|
| hidden states | 10 | 20 | 10 |
| five-word total variation from P | 0 | 0 | 0.000008278045934323998... |
| literal N541 witness mean | -0.0014863887893152726... | identical exact fraction | 54.02259857815162... |
| literal N541 second moment | 27034341276163.633... | identical exact fraction | saved in RESULT.json |

The common negative mean is exactly

    -1606733801523867092209222313325210331678860196835459
    /1080964693136600701865467242035174754467134680000000000.

The witness is reconstructed from supplied geometry, not copied as a
table: exact facet left inverse, shifted field interpolation, and the
stated constants. Its values on all words lie in the source range
[-29000000,81000000]. Its second moment is compatible with the source
upper bound 27034341276573. Whole-law equality implies every five-letter
statistic has the same distribution. This finite expectation reconstruction
does not newly certify the source's universal inequality.

Lexicographic search found a six-word difference at

    w=(1,0,0,0,0,1),
    p_R(w)-p_P(w)
      =1202639748140439253897665939307618358594090706076812970062247939
       /2280634370628436607371604810989939576608468585962137068684554403840000
      =0.0000005273268541546393... >0.

This bounds the equality scope; no efficient or optimal experimental
discriminator is claimed. Both probabilities are exact in `RESULT.json`.

Every entry of R_(1/10)^3 is positive. For uniform twenty-state U the
exact minimum gives

    R_(1/10)^3(x,.) >= beta U(.),       every x,
    beta=691471707822280134669933642662059
         /224226003951602006169694493460000000
        =0.0030838158627289752... .

Hence, from any start,

    ||law(X_t)-pi_hat||_TV <= (1-beta)^floor(t/3).

At t=3 ceil(5/beta)=4866 this is less than 0.01: 1-beta<=exp(-beta),
and sum_(j=0)^6 5^j/j!=16289/144>100 proves exp(5)>100. This is a
conservative bound, not an exact mixing time or an acquired physical
preparation. The orientation eigenvalue is exactly 4/5. A moderate
positive flip is therefore compatible with the entire five-word match.

## 7. Independent code path and resource contract

The producer uses exact Python integers in NumPy object arrays and
forward prefix propagation. `independent_operator_replay.py` imports no
producer code and uses only the standard library. It reconstructs P from
the original seed and all 400 lift entries. It verifies stochasticity,
stationarity and parity, then rebuilds the table through 36 backward
two-letter conditional vectors and the centered products in (5). All
7776 entries, ordinary-control total variation, strict three-step
minorization, and the six-word difference are reproduced exactly. This
is a second code path by the same worker, not a separate peer review or
physical verification. It does not recompute the witness formula means;
their equality already follows from the full table.

Measured on the available macOS arm64 host, Python 3.12.14:

| Computation | measured seconds |
|---|---:|
| frozen ten-state parity search | 0.00008979 |
| all three complete five-word tables | 0.00920942 |
| all literal witness values and exact expectations | 0.75883896 |
| six-word search, 7778 candidates until first difference | 0.01770313 |
| strict R^3 minorization | 0.00045813 |
| entire producer module, including NumPy import and finite input checks | 0.86582350 |
| independent standard-library operator replay | 0.03208204 |

Phase times are components of the producer total and must not be added
to it again. Standard-library imports before the timer, shell startup,
source retrieval, literature reading, implementation and report writing
are outside those timers and were not metered. A failed tool dispatch
before execution did not run a scientific computation; it is not a
discarded numerical trial. The producer was later edited only to remove
a dead expression and assert an already exactly checked equality of
second moments; the reported output is the original acquired run.

The source matrix and stationary law are supplied information. Their
original acquisition and prior proof costs are not erased or counted as
this wave's achievement. Obtaining P or pi from unknown physical data,
stationary samples, detector calibration, and physical parity realization
are unacquired. Given P and pi, the lift has 2n states and at most 4n^2
stored entries, compared with n and n^2 for ordinary reversiblization.
Its adjoint requires those stationary weights; solving for them if absent
is an additional operation. This is a supplied-model compiler, not a
passive unknown-model learner or an algorithmic speedup claim.

No GPU, paid compute, Monte Carlo, physical experiment or public write was
used. Exact output fractions, rather than a numerical tolerance or a
source hash, establish the finite identities.

## 8. Prior methods and scope of the retained result

Primary-source screening found two-replica lifting, skew detailed balance,
and reversal-dependent entropy definitions already established. They are
credited in Section 2 and `SOURCES.md`; they are not an invention here.
The ordinary additive reversiblization is also established. The direct
proof of the finite-window lemma avoids assuming any thermodynamic
theorem from those sources. A bounded search does not establish priority
for this particular lemma or this source-specific application.

The initial ambition was practical model-robust inference of hidden
dissipation from reversal-symmetric scalar records. N541 already provides
an exact even-hidden separation with very large **sufficient upper** sample
bounds, not sample-complexity lower bounds. This work has not reduced
those bounds or acquired an experimental diagnosis. Screening the prior
methods prevented promoting basic parity lifting as a new capability.

The constructive result instead exposes an actual contract boundary:
all five-letter evidence admits an explicit moderately flipping, mixing,
kinematically parity-reversible model. It defeats every test on independent
stationary five-letter windows. The supplied ten-state model has no
allowable parity, so the control is not a relabeling of that frozen
representation. Physical parity information, a justified even-state
assumption, or richer data is needed before a broader diagnosis; the
availability or sufficiency of a physical implementation remains UNKNOWN.
The six-letter difference is a concrete richer-data question, not its
acquisition or an optimal inference solution.

The full physical capability and any generic new lifting method remain
**NOT_ACHIEVED**. The declared even-hidden null, source protocol and costs
remain unchanged. There is no unrestricted CTMC or all-lag countercontrol.

## 9. Replay

From the workspace root:

```sh
work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol12_structural_capability_20261028/capability_backwards/construct_parity_control.py
work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol12_structural_capability_20261028/capability_backwards/independent_operator_replay.py
```

These commands regenerate only this folder's producer and replay JSON.
`RESULT.json`, `EXACT_MATRICES.json`, and `INDEPENDENT_REPLAY.json` retain
the acquired exact quantities and original measured timings until replay.
