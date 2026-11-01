# Primary prior matches and the actual comparison target

No historical novelty or comparative superiority is asserted. This branch is a
construction, not a claim that successor features or approximate LP were missing.
Sources below were opened directly, with the indicated central statements read.

## Direct established ingredients

1. **Successor features and GPI.** Barreto et al. (2017), especially Section 4
and Theorems 1--2, retain policy-dependent feature expectations and transfer them
across rewards. GPI compares favorably to retained policies; its optimal-policy
bound also depends on reward coverage. The present H is plainly a baseline
successor-feature matrix. It must not be renamed as a novel representation.
An equally informed successor-feature learner receives every baseline endpoint,
other-action endpoint, path tag and later certificate.
[Primary](https://proceedings.neurips.cc/paper/2017/file/350db081a661525235354dd3e19b8c05-Paper.pdf)

2. **ALP / constraint aggregation.** Lakshminarayanan--Bhatnagar's generalized
reduced LP, and Lakshminarayanan--Bhatnagar--Szepesvari's later linearly relaxed
ALP, explicitly reduce many constraints using positive combinations. With
feature basis H, our exact LP is a SPECIAL CASE of ordinary ALP with duplicate
constraints collapsed by W. This is not a newly invented planner. The proposed
ingredient to assess is acquiring H's needed action effects and a uniformly
valid robust constraint replacement without materializing H, then learning a
partition for which that replacement is economical. Conventional ALP plus this
acquired certificate has the same downstream capability; withholding it would
be an unfair comparison. The supplied-basis/constraint-error framework already
covers much of the deterministic architecture, so further exact prior matching
is necessary before assigning originality to the particular join.
[GRLP](https://arxiv.org/pdf/1409.3536)
[LRALP](https://sites.ualberta.ca/~szepesva/papers/2018-lralp-ieee-tac.pdf)

3. **Linear successor feature models.** Lehnert--Littman (2020), Theorem 2 and
its surrounding one-hot-feature definitions, require full action successor
statistics to be functions of the abstract state; the stated theorem obtains
bisimulation. Our condition is only that DIFFERENCES relative to a baseline
be block constant on H. The existing .405 predictive-aggregation failure and
strict nonfactorization example distinguish these equations; they do not prove
that no other theorem in the broad successor-feature literature covers the
same operation. Their general model-based/model-free bridge is established.
[Primary](https://jmlr.csail.mit.edu/papers/volume21/19-060/19-060.pdf)

4. **Successor feature sets.** Brantley--Mehri--Gordon (2021) already represent
many policies and later reward queries jointly. Its introduction and setup
explicitly address optimal policy extraction and the computational difficulty
of general exact set propagation. Thus policy coverage is not a newly identified
operation. The present restricted closure class uses a small LP rather than
materializing all policy-successor objects; that is a proposed class-specific
tractability condition, not a general separation from this literature.
[Primary](https://arxiv.org/pdf/2103.02650)

5. **Value equivalence.** Grimm et al. (2020), definitions and main formulation,
already argue for models that preserve the Bellman operations needed by a
consumer rather than state-to-state prediction. Nonpredictive usefulness is
therefore not a novel headline. The current proof uses an implicit value basis
and signed constraints rather than claiming a Markov quotient; its burden is
explicit learning, stable receiving and efficient planning after all costs.
[Primary](https://proceedings.neurips.cc/paper/2020/file/3bb585ea00014b0e3ebe4c6dd165a358-Paper.pdf)

6. **Ordinary executable LP.** The prototype uses SymPy's documented rational
simplex interface and separately checks exact primal/dual conditions. Neither
simplex nor floating LP is granted a polynomial worst-case runtime. Standard
rational LP theory supplies the polynomial consumer in the structural theorem;
this small implementation is an executable proof check, not that full backend.
[Official API](https://docs.sympy.org/latest/modules/solvers/solvers.html#sympy.solvers.simplex.linprog)

## What the current construction actually adds to this investigation

- A weaker sufficient equation than predictive aggregation, with a proof that
  policy evaluation/improvement stays in an acquired resolvent value space.
- A small signed LP with its correct acquired objective, even when WH is singular.
- Direct finite, truncated-geometric forward acquisition of all needed moments.
- A uniform posterior policy-regret certificate for arbitrary adaptive bounded
  goals, and a robust LP success theorem that pays coefficient/objective error.
- A monotone partition-refinement acquisition from native reward labels; no
  useful partition is passed as advice. Poor labels/gaps may produce rank n.

These are locally proved joins, not a claim that every ingredient is historically
new. Independent review remains pending. The real missing practical operation
is still an economical acquisition-plus-verification route on an important
many-task workload. Current tests establish algebra and receiving behavior,
not amortized economic superiority. The actual small stochastic protocol test
REFUSES the requested tolerance; the huge successful count arrays are fabricated
unit fixtures, never reported as observed data.

## Fair retaining methods and costs

A strong comparator may keep the complete endpoint/path metadata, reuse sample
statistics and policy evaluations, warm-start LPs, compress verified duplicate
constraints, use confidence sequences or sharper variance bounds, and stop early
on a goal-specific certificate. It need not relearn every goal or retain only a
single baseline policy. Our confidence/data interface and any actually derived
certificate are available equally. Sample-efficient reward-free learners and
on-demand model-based planners remain relevant; no comparison to d^N or blind
policy enumeration is a primary baseline.

The small LP removes ambient n from later core planning only AFTER full count
receiving, partition lookup construction and retention are paid. The core
certificate carries a partition hash rather than the n-label map, avoiding an
accidental O(n) per-goal hash scan. Deployment still pays sensing/mapping every
step. An independent full data audit remains O(nmr), not a cheap hash assertion.

7. **Bellman rank / realizable value classes.** Jiang et al. (2017) already
formalize learning through low-dimensional Bellman-error factorizations; their
OLIVE algorithm performs optimistic value-function selection, not a free
efficient-planner theorem for arbitrary feature classes. Under our exact
condition the explicit residual

    H w-[(1-gamma)Zg+gamma A_a H w]
      =(1-gamma)Z(w-g)-gamma ZB_a w

has an r-dimensional state-versus-candidate factorization. This is a direct
connection to that established organizing principle, not a new notion of error
rank. Our discounted/named-row/constructed-basis setting and finite constrained
LP consumer must be compared at their actual interfaces; merely saying 'low
Bellman rank' does not pay acquisition or numerical optimization. No formal
new lower bound or separation from all Bellman-rank algorithms is claimed.
[Primary](https://proceedings.mlr.press/v70/jiang17c/jiang17c.pdf)

8. **Hidden-K / generalized complementarity LP criterion (direct match).**
Morris, *Efficient Computation of a Canonical Form for a Matrix with the
generalized P-property*, Theorem 2(3) and Section 3, explicitly uses positivity
of the solution for a common right-hand side in every representative basis.
In our orientation, form a horizontal matrix with columns
(e_j-t Bhat_a[j,:]^T), grouped by j. A representative basis is M_pi^T, and
its solution for hhat^T is (hhat M_pi^-1)^T. Thus our positive objective-row
criterion is a QUANTITATIVE INSTANCE OF AN ESTABLISHED LP-solvability criterion,
not a new generic solution of P-matrix complementarity. The source also points
to earlier hidden-K work. Klaus develops the related GLCP/Grid-LP correspondence.
The proposed contribution here must be assessed at the acquisition interface:
baseline episodes, learned effect partition, imperfect moments and source-derived
uniform margins, not as invention of the abstract algebraic criterion.
[Primary theorem](https://math.gmu.edu/~wmorris/cubemdpmprev4.pdf)
[Related primary](https://arxiv.org/pdf/1405.1827)
