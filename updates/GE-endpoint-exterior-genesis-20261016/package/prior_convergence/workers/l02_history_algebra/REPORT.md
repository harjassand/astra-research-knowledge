# Exact finite-history path-map closure

This worker builds and replays a finite-dimensional verification target for a finite classical controller coupled to quantum Kraus edges. The computation is exact over the Gaussian-rational field `Q(i)`. The main result is a finite saturation procedure for path-map spans, then separate exact checks of (i) Knill–Laflamme recoverability and (ii) a prescribed decoder's actual branch action.

The replay is [replay.json](replay.json); the executable source is [history_closure.py](history_closure.py). Run it from this directory or any other working directory with:

```sh
python3 history_closure.py
```

The script uses SymPy and regenerates `replay.json`. It includes assertions for the three requested cases, exact instrument completeness, and the stated acceptance probabilities.

## Closure argument

Let `Q` be the finite controller-state set, `D` the physical Hilbert-space dimension, `k` the code dimension, and `f` a bounded primitive-fault budget. For each state `q` and exact fault count `b <= f`, define `L_(q,b)` as a linear subspace of `D x k` matrices. Seed the initial location with the encoding isometry `V`. For each edge `e:q->q'` with Kraus matrix `K_e` and fault cost `c_e`, close by sending every `A` in `L_(q,b)` to `K_e A` in `L_(q', b+c_e)` when `b+c_e <= f`.

Every insertion in the worklist is linearly independent within its location. The direct sum of all locations has dimension at most

```text
|Q| (f+1) D k.
```

Therefore the worklist terminates after at most that many independent insertions. Induction on path length shows that every finite history map `K_path V` lies in the saturated spaces. Conversely, every generated vector lies in the linear span of finite history maps, since edges act linearly and each inserted reduced vector is a linear combination of existing reachable vectors. Thus saturation computes exactly the span of all finite path maps, including histories of unbounded length, loops, reuse, and noncommuting edges. It does not enumerate or bound history length.

For one observable terminal flag, let `A_i` range over a basis of the union of accepting path-map spaces across all allowed fault counts. The standard Knill–Laflamme condition is

```text
A_i† A_j = c_ij I_k   for every pair i,j.
```

If output flags are trusted, this test is applied separately per flag and each flag may use its own recovery. If a flag is forgotten or untrusted, the map families are combined before testing. For a prescribed decoder with Kraus maps `D_r` and intended logical unitary `U`, this worker additionally checks the stronger execution-specific condition

```text
D_r A_i = alpha_(r,i) U   for every decoder branch r and every terminal-span basis map A_i.
```

Linearity extends that condition from the basis to every map in the span. Knill–Laflamme only establishes existence of a recovery for a correctable span; it does not certify that an arbitrary selected decoder or controller implements that recovery.

## Exact demonstrations

The seed is the standard five-qubit perfect `[[5,1,3]]` stabilizer code with generators `XZZXI`, `IXZZX`, `XIXZZ`, and `ZXIXZ`. The encoder `V` is built exactly from the stabilizer projector. Its two columns have rational entries and satisfy `V†V=I_2`.

**Unbounded one-qubit histories pass.** A cold controller state has two zero-cost loops applying `X_1/2` and `S_1/2`, where `S=diag(1,i)`, a primitive fault edge `X_1/2` to a persistent hot-latch state, and an accepting edge `I/2`. The hot state retains the two zero-cost loops and has two accepting Kraus outcomes `I/2`. The loops do not commute: `X_1 S_1 != S_1 X_1`. The one-fault budget is enough to enter the hot state; arbitrarily many further gates then cost zero budget.

The exact closure inserts 16 independent vectors across `cold|faults=0`, `hot|faults=1`, and the two accepting budget layers. Each layer has dimension 4, the accepting union has dimension 4, and the general insertion bound is 384. The accepting span passes all Knill–Laflamme pair tests. It also passes all `16 x 4` checks against the explicit five-qubit syndrome decoder below.

The decoder uses the 16 representatives `I` and the 15 single-site `X`, `Y`, and `Z` errors. For representative `E_r`, it sets `P_r = E_r V V† E_r†` and `D_r = V† E_r† P_r`. The replay verifies the syndrome projectors are pairwise orthogonal, sum to `I_32`, and `sum_r D_r†D_r = I_32`. Since the loop algebra is the full single-qubit matrix algebra on site 1, this decoder maps each terminal-span basis map to a scalar multiple of `I_2` on every syndrome branch.

Instrument completeness and acceptance are checked separately from path-span saturation. At each nonterminal state the outgoing `sum K_e†K_e` is exactly identity. In the cold state, loop probability is `1/2`, fault-transition probability is `1/4`, and direct-accept probability is `1/4`. In the hot state, loop probability is `1/2` and total accept probability is `1/2`. Solving the exact controller hitting equations gives acceptance probability `1` from both cold and hot. The closure calculation alone supplies no termination guarantee; this separate graph calculation does.

**An unrecorded logical loop fails.** The second graph adds a zero-cost logical `X_L = X⊗5` loop. Its edge weights are `1/3`, with parallel accepting Kraus outcomes chosen so every local instrument remains exactly TP. The closure still saturates within the dimension bound, but Knill–Laflamme fails. The explicit path pair `A=V`, `B=X_L V` has

```text
V† X_L V = [[0, 1], [1, 0]],
```

which is not a scalar multiple of `I_2`. The prescribed single-qubit syndrome decoder also fails: at least one decoder branch returns a nonscalar logical-X action. This is an exact negative control, not a claim about a physical implementation.

**Remembered parity passes; erased parity fails.** A one-step controller sends the `I` branch to trusted flag `parity-0` and the `X_L` branch to trusted flag `parity-1`. Each flag has a one-dimensional path-map span and passes the separate Knill–Laflamme check. Fixed decoders `V†` and `V†X_L†`, respectively, map their conditioned branch maps to scalar multiples of `I_2`. When the flag is forgotten, the combined set contains both `V` and `X_LV`; the pairwise Gram has a logical-X witness and fails. The four outgoing half-amplitude Kraus outcomes make this one-step instrument TP, and all its outcomes are accepting.

## Scope and limits

This replay verifies finite exact matrix identities for the supplied graphs and code. It establishes neither a new general theorem nor a scalable architecture. Finite-dimensional saturation and the Knill–Laflamme criterion are standard ingredients; no novelty or priority claim is made. The calculation does not establish a threshold, asymptotic fault tolerance, a physical realization, or correctness under controller edges and flag semantics not represented here. The fixed-decoder checks concern the named decoder maps only. TP completeness and almost-sure acceptance are separate obligations and are reported independently of the closure algorithm.
