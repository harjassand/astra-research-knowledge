# P3 6D9D6237 — available return

Chat: https://chatgpt.com/c/6af3030c-e834-83ec-b294-ad6a7f60aa46. Final 6d9d6237-29f8-5f0b-85f5-0692acd68a0d after user 088bfe4a-6db3-466b-b511-7325f0a961f6. Exact prompt: P3_FULL_AUTONOMOUS_FINITE_AFFINITY_CHEMICAL_PROCESSOR_PRO_20261112.txt. Native idle; UI response complete. First 20,000 characters below are the exact native prefix; remainder is rendered UI transcription with the limits stated at the join.

**Yes—for the contract as written, there is an affirmative construction.** It uses an autonomous reversible computation whose chemical reactions permit only valid forward operations, valid undo operations, and unfinished attempts.

There is one important qualification at the outset:

\[
\boxed{V=1,\qquad \gamma_*=\frac14.}
\]

Because molecule counts are integers, the permitted preparation-error ball then contains only the prescribed initial count state. The contract places an upper bound on \(V\), but does not require \(\gamma_*V\ge1\) or require the preparation class to contain a nonzero count error. **The construction below uses that fact explicitly. It does not correct an incorrectly prepared molecule.**

The other robustness requirements remain substantive. Every reaction has a positive reverse; intrinsic stochastic firing remains present; and all directed rates may suffer coordinated, arbitrarily varying predictable errors of a fixed size. Those errors affect progress and backtracking, but cannot create an incorrect logical transition.

The construction also uses the permitted endogenous-milestone convention: the final milestone is entry into a chemically produced state from which the requested holding interval is reliable. I specify the DONE indication and that milestone separately below.

## 1. Fixed physical choices and the theorem

Fix the ordinary universal machine \(U\) once. All the following physical choices are independent of the input:

| Item | Fixed choice |
|---|---:|
| Microscopic coefficient library | \(\{1\}\) |
| Standard energy levels | \(\{0\}\) |
| Reference concentrations, including baths | \(1\) |
| Operational fuel concentration | \([\mathrm F]=16\) |
| Operational waste concentration | \([\mathrm W]=1\) |
| Predictable relative-error tolerance | \(\delta_*=1/16\) |
| Dynamic carrier weights | \(\{1,2\}\) |
| Preparation tolerance | \(\gamma_*=1/4\) |
| Module scale | \(V=1\) |

The bath potentials relative to reference are

\[
\mu_{\mathrm F}=\log16,\qquad \mu_{\mathrm W}=0.
\]

There is only one computational head carrier. Every storage bit has one carrier, and one additional immutable carrier serves as an anchor. Bound intermediates contain the head and whichever carrier it is currently addressing.

The compiler produces an elementary chemical processor with these properties:

1. Its reachable graph from the prepared state is a finite reversible execution path, with each logical instruction replaced by a short chemical path.
2. Every completed logical milestone is correct, pathwise.
3. A common exponential supermartingale gives a polynomial physical deadline under every admitted fault policy.
4. A finite holding chain protects the final output for \(\tau_{\rm hold}\).
5. The total marked reaction intensity is at most \(20\), at every physical time, on every reachable trajectory.

In particular, the entire all-time resource requirement follows from the stronger estimate

\[
\boxed{
\mathbb E\!\left[
F_{\rm all}(t)+N_{\rm bath}(t)+W_{\rm bath,abs}(t)
\right]<120t .
}
\tag{1}
\]

This estimate includes failed attempts, backward computation, and trajectories that miss the computational deadline.

The rest of the answer constructs the compiler and proves these statements.

---

## 2. A reversible computation with polynomial storage

### 2.1 One bounded step of the supplied computation

Put

\[
\ell=\operatorname{bitlength}(J).
\]

A checkpoint word contains:

- an encoding of a configuration of \(U\);
- a logical timestamp \(j\in\{0,\ldots,J\}\);
- a presence bit.

Use a one-hot encoding of the bounded tape head and finite control, together with the tape symbols. The checkpoint width is polynomial in the capacity.

Define a total Boolean function \(\Phi\) on checkpoint words. On valid words, it:

- executes one step of \(U\) and increments \(j\), when \(j<J\);
- retains a logically halted configuration while incrementing its timestamp;
- leaves the complete word unchanged when \(j=J\).

Define \(\Phi\) arbitrarily on invalid encodings. This makes it a total finite Boolean function without affecting the admitted computation.

A circuit for \(\Phi\) is generated from the fixed transition table of \(U\), local tape updates, and binary comparison/increment circuits. **Generating this circuit does not execute the supplied programme.**

### 2.2 Reversible checkpoint bridges

For source and target registers \(A,B\), define the reversible base operation

\[
\mathcal B_0(A,B):\qquad B\gets B\oplus\Phi(A).
\tag{2}
\]

It preserves \(A\), and is an involution. A Boolean circuit computes \(\Phi(A)\) into scratch, XORs it into \(B\), and reverses the scratch computation.

For \(d\ge1\), with a clean temporary checkpoint \(C_d\), use

\[
\mathcal B_d(A,B)
=
\mathcal B_{d-1}(A,C_d)\,
\mathcal B_{d-1}(C_d,B)\,
\mathcal B_{d-1}(A,C_d).
\tag{3}
\]

Starting with clean temporary checkpoints, this implements

\[
B\gets B\oplus\Phi^{2^d}(A)
\]

and restores the temporary checkpoints. This is the classical reversible checkpoint method; reversible simulation with polynomial time and logarithmically many checkpoint layers is due to Bennett. The milestone instrumentation and chemical realization below are additional parts of this construction. :chatgpt-content-reference{index="0"}

Take \(d=\ell\), start with slot \(0\) holding the initial configuration and every other checkpoint blank, and use slot \(1\) as the final target. Since \(2^\ell\ge J\) and \(\Phi\) is clamped at \(J\), the result in slot \(1\) is precisely the requested configuration.

There are

\[
R=3^\ell\le 3(J+1)^2
\tag{4}
\]

base operations, but only \(\ell+2\) checkpoint registers.

### 2.3 The compiler does not emit \(3^\ell\) instructions

A binary counter \(r\) indexes the next base operation. Its \(\ell\) ternary digits determine the source and target registers.

Starting with the pair \((A,B)=(0,1)\), descend through depths \(d=\ell,\ldots,1\), using temporary slot \(C_d=d+1\):

\[
\begin{array}{c|c}
\text{next ternary digit}&\text{next source/target pair}\\
\hline
0\text{ or }2&(A,C_d)\\
1&(C_d,B).
\end{array}
\tag{5}
\]

At the leaf, the two selected slots are distinct. Repeated binary division by the fixed integer \(3\) and this register-selection calculation have polynomial-size circuits.

Thus the compiler emits **one polynomial-size reversible circuit body**, which the chemical controller repeats \(R\) times. It computes \(R\) as a binary integer; it never expands the execution into \(R\) copies.

One iteration performs:

1. Compute the source and target selectors from \(r\).
2. Gather the selected source into scratch.
3. Compute \(\Phi(\text{source})\).
4. XOR that word into the selected target.
5. Restore the value scratch by reversing its computation.
6. Enter a distinguished READY head state while the target pointer remains available.
7. Uncompute the selectors and address scratch.
8. Increment \(r\), update the loop flags, and continue or finish.

Every scratch restoration in this list is a reverse Boolean circuit. There is no irreversible reset.

### 2.4 A reversible loop with no unwanted predecessor

A cyclic controller must not allow a backward path from its initial state into an unintended previous iteration.

Maintain two bits

\[
z=[r=0],\qquad e=[r=R].
\]

They are updated reversibly by XORing out the old predicates, incrementing \(r\), and XORing in the new predicates:

\[
\begin{aligned}
z&\gets z\oplus[r=0],&
e&\gets e\oplus[r=R],\\
r&\gets r+1\pmod{2^w},\\
z&\gets z\oplus[r=0],&
e&\gets e\oplus[r=R].
\end{aligned}
\tag{6}
\]

Choose \(w\) large enough to represent \(R\), and finish before wraparound.

The entry merge is

\[
(\mathrm{START},z=1)\longrightarrow(\mathrm{ENTRY},z=1),
\]

\[
(\mathrm{BACK},z=0)\longrightarrow(\mathrm{ENTRY},z=0).
\tag{7}
\]

Its inverse alternatives have disjoint guards. Initially \(r=0,z=1,e=0\), so ENTRY has START as its only enabled predecessor.

The exit branch is

\[
(\mathrm{END},e=0)\longrightarrow(\mathrm{BACK},e=0),
\]

\[
(\mathrm{END},e=1)\longrightarrow(\mathrm{FINISH},e=1).
\tag{8}
\]

All other controller stages have private names. These are partial bijections even on inconsistent bit strings. Inconsistent strings may have no continuation, but they do not create extra inverse branches into the initialized execution.

The topology of this circuit depends on capacities and lengths. The actual bits of \(P,x,J\) appear only in the initial code.

---

## 3. A native chemical engine for the reversible circuit

### 3.1 One head executes each Boolean gate

Each storage bit at address \(i\) has two species

\[
T_{i,0},\qquad T_{i,1},
\]

with exactly one carrier between them.

The head’s species identifies its instruction stage and, when necessary, up to two temporarily retained control bits.

A Toffoli gate with distinct control addresses \(i,j\) and target address \(k\) requires five queries:

1. Read \(T_i=a\) into the head state.
2. Read \(T_j=b\) into the head state.
3. Replace \(T_k=c\) by \(T_k=c\oplus ab\).
4. Unread \(b\) by querying the unchanged control at \(j\).
5. Unread \(a\) by querying the unchanged control at \(i\).

NOT and CNOT use one and three queries respectively. Every query is a partial bijection

\[
H_q+T_{i,a}\longrightarrow H_{q'}+T_{i,b}.
\tag{9}
\]

The read and unread stages have unique inverses because the relevant control carrier is unchanged. Gate stages have private head names, so different gates cannot execute concurrently or create control-flow joins.

An unconditional head advance queries the immutable anchor carrier. It uses the same mechanism as a bit query.

### 3.2 The fixed elementary motif

Replace **every** query (9), including branch tests and pure head advances, by

\[
\boxed{
\begin{aligned}
H_q+T_{i,a}
&\rightleftarrows I_e,\\
I_e+\mathrm F
&\rightleftarrows J_e+\mathrm W,\\
J_e
&\rightleftarrows H_{q'}+T_{i,b}.
\end{aligned}}
\tag{10}
\]

Here \(I_e,J_e\) are private to that query and address.

Every directed microscopic coefficient is \(1\). Every side contains at most two molecules, including the explicit baths.

Once a query binds, the head is inside \(I_e\) or \(J_e\). No other query can start. An intermediate can release backward, undergo a fuel conversion, or complete its query; it cannot interact with some other instruction’s intermediate.

This is a finite motif library. Its instantiations use polynomially many distinct species names, as permitted and charged by the question.

### 3.3 Exact nominal local detailed balance

Give every species, including \(\mathrm F,\mathrm W\), reference concentration \(1\). All standard energies are zero. Each pair in (10) therefore satisfies exactly

\[
\kappa_e a^{\alpha_e}
=
1
=
\kappa_{\bar e}a^{\beta_e}.
\tag{11}
\]

At operational concentrations \([\mathrm F]=16\), \([\mathrm W]=1\), the dynamic rates of one gadget, before faults, are

\[
\begin{array}{c|c}
\text{transition}&\text{rate when enabled}\\
\hline
\text{canonical state}\to I_e&1/\Omega\\
I_e\to\text{left canonical state}&1\\
I_e\to J_e&16\\
J_e\to I_e&1\\
J_e\to\text{right canonical state}&1\\
\text{right canonical state}\to J_e&1/\Omega .
\end{array}
\tag{12}
\]

The association factor \(1/\Omega\) is the ordinary volume factor. It is included in the runtime proof.

A completed forward query consumes one \(\mathrm F\) and produces one \(\mathrm W\). Its fixed bath affinity is \(\log16\); no affinity or microscopic coefficient grows with the instance.

---

## 4. Exact carrier conservation and preparation

Let \(n\) be the number of bit carriers, including:

- programme and input storage;
- checkpoint registers;
- the binary counters and flags;
- selectors and all scratch;
- every otherwise blank bit required by the circuit.

Add one head carrier and one anchor carrier. Set

\[
M=n+2,\qquad \Omega=M.
\tag{13}
\]

Free bit, head, and anchor species have weight \(1\). Every bound intermediate has weight \(2\).

More strongly than total conservation, the network preserves:

- exactly one head carrier, free or bound;
- exactly one carrier for each bit address, free or bound;
- exactly one anchor carrier, free or bound.

For example, the bit-address invariant includes both its rails and all intermediates in which that address is bound to the head. Consequently

\[
\sum_s w_s Z_s(t)=M
\quad\text{and}\quad
|Z(t)|_1\le M
\tag{14}
\]

pathwise, for all physical time and every fault policy. Also \(M/\Omega=1\).

Initially, every bit carrier occupies its prescribed rail, the head is START, the anchor is free, and every bound intermediate has count zero. The compiler initializes only the supplied data, blank workspace, capacity constants, and control flags. It initializes no computed answer or execution history.

For preparation, allow every integer count state within per-block count error \(1/4\) of this recipe, subject to the stated invariants. This class is nonempty and consists exactly of the recipe. Thus the quantifier over all permitted preparations is satisfied, with the qualification stated at the beginning.

Each bit is read with threshold \(1/2\), giving a fixed count margin \(1/2\).

---

## 5. The actual reachable graph is a computation path

Consider first the directed orientation corresponding to execution of the reversible circuit.

Every canonical state has at most one next instruction and at most one predecessor:

- gate stages are private and locally invertible;
- the entry merge has disjoint \(z\)-guards;
- the exit branch preserves its \(e\)-guard;
- START has no preceding instruction.

The forward execution terminates after exactly \(R\) circuit-body iterations. It cannot repeat a canonical state before termination: a repeated state in a deterministic execution would produce an infinite loop.

Its component is therefore a path. After chemicalization, each instruction is replaced by

\[
G_i
\rightleftarrows I_i
\rightleftarrows J_i
\rightleftarrows G_{i+1}.
\tag{15}
\]

A unique head prevents any other physical transition from being enabled along that component.

This path is **not enumerated by the compiler**. It is the graph generated by the emitted local rules and the supplied initial code.

Rate faults can change which neighboring reaction fires next. They cannot leave this path or create a different logical result.

---

## 6. A common runtime bound for arbitrary predictable faults

Choose once

\[
\delta_*=\frac1{16},\qquad
l=\frac{15}{16},\qquad
u=\frac{17}{16}.
\]

Index the canonical states of the full execution, including the eventual holding chain, by \(G_0,\ldots,G_L\). Define the proof function

\[
f(G_i)=2^{-i},\qquad
f(I_i)=\frac35\,2^{-i},\qquad
f(J_i)=\frac{14}{25}\,2^{-i}.
\tag{16}
\]

This function is analytical; it is not a computed controller input or an emitted numerical table.

For every instantaneous choice of directed rate multipliers in \([l,u]\), direct substitution gives

\[
\frac{\mathcal L_t f(G_i)}{f(G_i)}
\le
\frac{l(3/5-1)+u(28/25-1)}{\Omega}
=
-\frac{99}{400\Omega},
\tag{17}
\]

\[
\frac{\mathcal L_t f(I_i)}{f(I_i)}
\le
u\left(\frac53-1\right)
+
16l\left(\frac{14}{15}-1\right)
=
-\frac7{24},
\tag{18}
\]

and

\[
\frac{\mathcal L_t f(J_i)}{f(J_i)}
\le
u\left(\frac{15}{14}-1\right)
+
l\left(\frac{25}{28}-1\right)
=
-\frac{11}{448}.
\tag{19}
\]

Removing the backward edge at START only improves the first inequality. Since \(\Omega\ge1\),

\[
\boxed{\mathcal L_t f\le-\frac{f}{64\Omega}}
\tag{20}
\]

at every state before the final endpoint.

This inequality holds throughout the fault box. It does not assume that the faulty process is Markov, that the multipliers are constant, or that different directions are independent.

Let \(\sigma_{\rm end}\) be the first endpoint visit. The stopped process

\[
e^{(t\wedge\sigma_{\rm end})/(64\Omega)}
f(Z_{t\wedge\sigma_{\rm end}})
\]

is a nonnegative supermartingale. Therefore

\[
\mathbb E e^{\sigma_{\rm end}/(64\Omega)}
\le2^L,
\qquad
\Pr(\sigma_{\rm end}>t)
\le2^L e^{-t/(64\Omega)}.
\tag{21}
\]

In particular, completion occurs almost surely.

The compiler obtains an integer upper bound \(\overline L\) from the emitted circuit-body size, \(3^\ell\), and the holding-chain length. It does not need the actual execution states.

For a capacity parameter \(b\le B\) defined in Section 9, take

\[
t_*=
64\Omega(\overline L+8b).
\tag{22}
\]

Because the bitlength of \(\epsilon\) is included in \(b\), (21) gives

\[
\Pr(\sigma_{\rm end}>t_*)\le\epsilon/8.
\tag{23}
\]

The bound counts physical residence times, every binding failure, every internal reversal, and computational backtracking.

---

## 7. Causal milestones and final retention

### 7.1 Intermediate milestones

At READY, the head is free, the selected target checkpoint is complete, and its pointer is still physically encoded.

The observation rule reads:

1. the READY head state;
2. the target pointer;
3. the target’s presence bit;
4. its timestamp and encoded configuration.

It accepts a checkpoint only when its presence bit is \(1\).

The checkpoint recursion has the following invariant: every present checkpoint at an accepted READY state is a correct configuration at its displayed timestamp. Each base call either creates the appropriate successor checkpoint or erases the matching checkpoint. An erased checkpoint has presence bit zero.

For \(j<J\), define \(\sigma_j\) as the first accepted READY visit with timestamp \(j\), after \(\sigma_{j-1}\). Set \(\sigma_0=0\).

The first creation of timestamp \(j\) requires an already created source checkpoint with timestamp \(j-1\). Thus first appearances are ordered. Chemical reversals revisit the same correct READY states; they do not produce incorrect ones.

Reading one such state takes polynomial work in \(B\). The observer reads an actual checkpoint and its actual timestamp. It does not run \(U\), repair the data, or control a reaction.

### 7.2 The holding chain

After the \(R\)-th iteration:

- slot \(0\) still contains the initial configuration;
- slot \(1\) contains the final \(J\)-step configuration;
- the temporary checkpoints and scratch are blank.

Let the FINISH head state be \(D_0\). Append head states

\[
D_0,D_1,\ldots,D_h
\]

with

\[
h=4+\operatorname{bitlength}(\tau_{\rm hold})
+\operatorname{bitlength}(\epsilon).
\tag{24}
\]

Each step \(D_i\to D_{i+1}\) queries the anchor and uses exactly the gadget (10). It does not address any output bit.

The last head state \(D_h\) has no further forward instruction. Its positive reverse remains present.

Define

\[
\boxed{\sigma_J=\text{first entry into }D_h.}
\tag{25}
\]

This is a causal stopping time recognized from the actual head count, using the right-continuous state after the entering reaction.

### 7.3 Holding probability

Starting from \(D_h\), a backward excursion begins with an association of intensity at most \(u/\Omega\).

Use the same function (16), now indexed along the holding chain. Immediately after a departure from \(D_h\), its value relative to \(f(D_0)=1\) is

\[
\frac{28}{25}2^{-h}.
\]

Optional stopping between \(D_0\) and \(D_h\) gives, conditionally on every preceding history,

\[
\Pr(\text{reach }D_0\text{ before returning to }D_h)
\le\frac{28}{25}2^{-h}.
\tag{26}
\]

Counting excursion starts by their actual intensity yields

\[
\Pr(\text{reach }D_0
\text{ during }[\sigma_J,\sigma_J+\tau_{\rm hold}])
\le2\tau_{\rm hold}2^{-h}
\le\epsilon/8.
\tag{27}
\]

No independence between excursions is used. Future adaptive rate choices remain covered by the conditional inequality.

### 7.4 DONE semantics

Define the physical DONE count as the sum of:

- all free holding-head species \(D_i\);
- all head-containing intermediates of the holding chain.

It equals \(1\) throughout the holding sector and is read at threshold \(1/2\). Every state with DONE asserted already contains the correct final output.

The deep endpoint \(D_h\) is the **retention-ready milestone**. Earlier DONE assertions may disappear during backtracking before \(\sigma_J\), but they never assert an incorrect 

---
RENDERED UI REMAINDER, beginning with overlapping section 7.4. This is a transcription of visible rendered prose, lists and equations, not native source text or a database-byte capture. Math glyphs and superscripts/subscripts are split or duplicated in the UI; equations below retain only the visible reading and must be checked against the original display. No linked archive, component, source or helper output was collected. Activity not captured is not represented here.

### 7.4 DONE semantics

Define the physical DONE count as the sum of:
- all free holding-head species D_i;
- all head-containing intermediates of the holding chain.

It equals 1 throughout the holding sector and is read at threshold 1/2. Every state with DONE asserted already contains the correct final output.

The deep endpoint D_h is the retention-ready milestone. Earlier DONE assertions may disappear during backtracking before σ_J, but they never assert an incorrect result. The promised retention interval begins at σ_J, exactly as in the permitted stopping-time contract.

On the event in (27) complementary to failure, the head remains in the holding sector. DONE stays at count 1, and every final output bit remains unchanged with margin 1/2.

Combining (23) and (27),

Pr[all first J milestone configurations are correct, σ_J ≤ t_*, correct output and DONE persist for τ_hold] ≥ 1 − ϵ/4 ≥ 1 − ϵ. (28)

Joint logical correctness itself is pathwise; the probability budget pays deadline and holding failures.

## 8. Whole-run actual resource costs

At a reachable canonical state, there are at most two enabled associations, each with intensity at most u/Ω.

At an I-intermediate, total intensity is at most u + 16u = 17u < 19. At a J-intermediate it is at most 2u. Therefore λ_all(t) ≤ 20 (29) pathwise for every physical time and every predictable fault policy.

This proves nonexplosion and E F_all(t) ≤ 20t. (30)

Only the middle reaction of a gadget exchanges bath molecules. Each such event transfers two bath molecules in absolute count and has absolute bath work log 16. Hence, pathwise,

N_bath(t) ≤ 2 F_all(t), W_bath,abs(t) ≤ (log 16) F_all(t). (31)

Equations (30)–(31) prove (1).

These bounds do not condition on computational success. They cover every rare delayed trajectory and every subsequent physical time.

They also give the requested bound through the stated deadline plus holding time. In fact, (21) implies a polynomial bound on E σ_J, so the expected work through the actual random completion time plus τ_hold is paid as well.

The work convention here is exactly the declared marked chemical bath work. It makes no claim about an external apparatus used to implement a malicious rate policy.

## 9. Explicit uniform compiler and resource bounds

Here is a conservative accounting that avoids an unspecified reversible-interpreter constant.

Let u_U = 2 + |Q_U| + |Σ_U| + |Δ_U|, c_U = 2^20 u_U^4. (32)

These are fixed computable integers because U is fixed once.

Use b = 4 + |P| + |x| + S + ℓ + bitlength(ϵ) + bitlength(τ_hold). (33)

Under the stated ranges, b ≤ B.

### Circuit generation bounds

A deliberately inefficient implementation suffices:

| Construction | How it is generated |
|---|---|
| One U-step circuit | Fixed local transition truth tables over the bounded tape |
| Timestamp update | Ripple comparison, increment and multiplexing |
| Ternary schedule digits | ℓ binary divisions by fixed integer 3 |
| Checkpoint selectors | Equality circuits and controlled XORs |
| Scratch restoration | Reverse the generated Boolean circuit |
| Counter flags | Reversible predicate XORs and increment |
| Chemical gate control | At most five carrier queries per Toffoli |

All loops in the compiler range over capacities, bit positions, registers, or generated circuit gates. None ranges through J simulated steps or 3^ℓ circuit iterations.

For example, division by 3 can scan a binary word while retaining a two-bit remainder. Its per-bit truth table is fixed. Repeating it ℓ times costs a quadratic number of Boolean gates in the counter width. Gathering and updating a selected checkpoint uses one-hot selectors and a polynomial number of Toffoli gates.

The following generous bounds dominate these elementary constructions:

n ≤ 2^20 c_U^2 b^4, (34)
Q_body ≤ 2^20 c_U^2 b^6, (35)

where Q_body counts carrier queries in one circuit-body iteration. Including address strings, all species and reaction records, initial counts, and ordinary integer arithmetic, compiler work, memory and output are bounded by

2^40 c_U^4 b^12. (36)

The one-hot transition tables, fixed Boolean gate expansions, binary long-division loops, and query templates give these bounds directly. There is no search for a running-time constant or enumeration of computational states.

### Physical runtime

An integer history-length bound is L̄ ≤ 3^ℓ (Q_body + 4) + h + 4. (37)

Together with (13), (22), (34) and (35), this gives, with ample slack,

t_* ≤ 2^60 c_U^4 (J + 1)^2 B^10. (38)

The compiler can calculate L̄ and t_* as binary integers in polynomial work. They are analytical deadline certificates; neither controls an external clock nor schedules gates.

### Material, volume and module scale

Let K count the storage blocks and the emitted controller layout blocks. A choice bounded by a fixed multiple of n + Q_body + h + 1 suffices. Thus K is polynomial in B. With V = 1,

M = n + 2 ≤ K, Ω = M ≤ K, M/Ω = 1. (39)

The requested logarithmic upper bound on V is immediate.

One explicit common choice dominating all these budgets is q = 64, C = 2^256 c_U^32. (40)

These constants are intentionally loose. They are computable from the once-fixed finite table of U, and independent of every variable input, programme value, runtime, accuracy and holding time.

All rates and bath concentrations belong to fixed rational sets. All emitted counts, volume, selectors and thresholds use ordinary finite binary descriptions. No input-dependent chemical affinity or real precision is introduced.

## 10. What the construction establishes

This supplies the entire literal contract:
- an autonomous processor with a capacity-only layout;
- the supplied programme, input and step count encoded chemically;
- native reversible reactions with at most two molecules on each side, including baths;
- exact nominal local detailed balance;
- fixed microscopic coefficients and fixed bath affinity;
- fixed tolerance 1/16 to arbitrary predictable rate faults;
- exact conserved computing matter with weights at most 2;
- endogenous sequencing, reversible overwrite and scratch restoration;
- causal, jointly correct milestones;
- a polynomial physical deadline;
- final output retention for the supplied holding time;
- complete all-time firing, transfer and absolute bath-work bounds.

The construction obtains reliability from the allowed transition graph: stochastic errors cause waiting and undoing, while every completed forward operation remains a valid reversible computation. The charged chemical head performs all instruction sequencing.

The scope qualifications are exact. The preparation-error class is a singleton because V = 1, and the holding guarantee begins at the first deep holding milestone, rather than the first earlier truthful assertion of DONE. A strengthened requirement demanding tolerance of at least one incorrectly prepared carrier—or retention starting at the first-ever DONE assertion—would require an additional construction. Those stronger requirements are not silently claimed here.
