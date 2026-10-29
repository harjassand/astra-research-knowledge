# Independent audit: the thermal-to-exact-counting construction

Date: 2026-10-29 UTC. Auditor: `challenge_thermal_counting_consequence`.

## Verdict and actual evidence reviewed

**Conditional PASS for the mathematical reduction**, including the uniform-width refinement described below. No fatal precision, sign, cancellation, variable-count, or space-complexity gap was found. This is not an implementation certificate and not a novelty certificate. Root's compiler tests are a separate obligation.

I actually read:

- `COUNTING_CONSTRUCTION_DRAFT.md`, SHA256 `16cd494efd752035dac42aecd6e97745b7eed1cbeb58ff772790664405af5797`;
- `PHYSICS_THEOREM.md`, SHA256 `a07dd000b83c47fbb07c4d2312a789bd4538d9d97236261ef5823fbdcae5c369`;
- `PHYSICS_AUDIT.md`, SHA256 `daab0aa45ab1005db58ae6641536b73e318c8267881d9d161389fc051ebc5a8b`;
- the theorem statement in supplied `source/openai_sat_main.tex`, SHA256 `b2e6159d4fb7ea6aa4f89ac15605152b0333a5f7cafe93323492bc20a5c066aa`.

The supplied exact-counting theorem is an **explicit assumption**, not something this audit proves or independently validates. Its sparse fixed-width statement is deterministic time `(N+C)^{O_{w,D}(1)} 2^{O_{w,D}(N/sqrt(log N))}` and polynomial bit space when `C<=DN`. The stronger sparse bound, rather than just unspecified subexponential time, is necessary for the vanishing-error consequence.

The physical proof's decisive operations check out: constant-depth support cones; `F(t)^dagger=F(-t)`; cancellation in the Hermitian part of the relative generator; singular-value Gronwall; operator-monotone logarithm; then log-trace-exp Lipschitz continuity. In particular, it does not illegally take powers in Loewner order or exponentiate an extensive norm in a local-error bound.

## Scope and input bookkeeping that must be stated

`k,Delta,J` are fixed. Each *term support*, not merely each pairwise graph edge, has size at most k, every qubit is in at most Delta term supports, and each term has spectral norm at most J. Terms are supplied as explicit rational-complex Hermitian matrices. Remove scalar/empty-support terms and add their known contribution to free-energy or ground-energy density afterward. The remaining number of terms satisfies `m<=Delta n`.

The honest bit-complexity bound is `poly(L,n) * 2^{o(n)}`, with L the supplied input bit length; it is simply `2^{o(n)}` only when that polynomial factor is subexponential, as for polynomial-length inputs. Temperature and accuracy parameters must be rational or appropriately computable, not arbitrary noncomputable real constants. They can be chosen rational in the ground-energy consequence.

The assertion concerns free-energy **density**, or ground-energy **density**. It does not provide constant relative error in Z, inverse-polynomial total-energy error, state preparation, individual local-observable estimation, or generic correlation functions. No thermodynamic limit or differentiability assumption is needed. Nonstoquastic terms and bounded-degree expander interactions are included.

## Explicit finite precision choices, without exact transcendental rounding

Write `d=2^k`, `J0=J+1`, `q<=k(Delta-1)+1`, and `K=sum_{ell=1}^q k^ell`. Take `0<epsilon<=1` and beta>0. Choose an integer r satisfying

```
r >= beta*J0*K,
r >= 2*beta*K*Delta*J0^2/sqrt(epsilon),
r >= 1.
```

All inequalities can be met using rational upper bounds and integer square roots. Put `delta=beta/r`. The physical theorem then gives free-energy-density error at most epsilon/4 for any Hamiltonian with local norm at most J0: indeed its bound is at most

`e*Delta*J0^3*K^2*beta^2/(3r^2) <= e*epsilon/(12*Delta*J0) <= epsilon/4`.

For every original term set `A=exp(-delta*h/2)` and

`eta = delta*epsilon/(32*Delta)`.

Since `delta*J<=1`, `lambda_min(A)>=exp(-1/2)>1/2`; also eta<1/4. Compute a rational Hermitian approximation S to A with spectral error at most eta/2. For example, the exact rational Taylor polynomial in `X=-delta*h/2` has norm-controlled tail `e^{||X||} ||X||^{ell+1}/(ell+1)!`. Here `||X||<=1/2`, so a polynomial number of bit operations in the supplied entry bit length and `log(1/eta)` suffices at fixed local dimension.

Choose B with `2^{-B}<=eta/(2d)`. Round the real/imaginary entries of S to this grid, copying conjugate entries and keeping diagonal entries real. This is exact rounding of rationals; there is no need to decide whether a transcendental matrix entry lies exactly on a rounding boundary. The grid contribution to spectral error is at most `d*sqrt(2)*2^{-B}/2 <= eta/(2 sqrt(2))`, hence `||G-A||<eta`.

Then G is positive definite, and the integral representation of log gives

```
||log G-log A|| <= 2*eta/a <= 4*eta, where a=exp(-delta J/2)>=1/2,
||h'-h|| <= 8*eta/delta = epsilon/(4 Delta),
h' := -(2/delta) log G.
```

Thus `||H'-H||<=n epsilon/4`, `||h'||<=J0`, and free-energy density shifts by at most epsilon/4. The support of h' is still the original local support: applying log to a positive matrix tensored with identity gives the local log tensored with identity. No explicit construction of the generally irrational h' is required.

Also `||G||<2`, so every real/imaginary numerator in `G=(u+iv)/2^B` has magnitude less than `2^{B+1}`. A selector of B+2 bits is more than enough. This supplies fully finite parameter bounds rather than just an existence assertion about constant precision.

## Exact signed counting and variable budget

Let T be the number of local gate occurrences in `(Q_G^dagger Q_G)^r`; `T=2mr`. Fix a gate ordering. Start with one path bit for each qubit, introduce at most k output bits per gate occurrence, and impose equality of the final and initial bit on each qubit. Unacted-on wires retain their current bit rather than receiving unrelated free bits. This yields at most `n+kT` wire bits and the ordinary exact trace path expansion.

For one local entry `(u+iv)/2^B`, one component bit chooses u or v. An s-bit integer selector z is accepted exactly when `0<=z<|u|` or `0<=z<|v|`, respectively. This creates exactly the desired nonnegative integer multiplicity, including zero allowed branches for a zero component. The phase increment is 0,2,1,3 respectively for positive real, negative real, positive imaginary, negative imaginary. Its value on a zero component is immaterial because that component has no accepted selector.

A two-bit cumulative phase register starts at 0 and evolves by addition modulo 4. Every transition is functional. With two bits for each phase endpoint, T component bits and sT selector bits, the non-Tseitin variable count is at most

`n+(k+s+3)T+2`.

For fixed B, a forbidden-pattern CNF of width at most `2k+s+5` is enough, with O(n) clauses. There are no auxiliary multiplicity factors: the only non-unique choices are physical wire paths, component expansion, and deliberately counted magnitude selectors. Two formula variants pin final phase to 0 and 2. Their counts C0 and C2 obey exactly

`Tr[(Q_G^dagger Q_G)^r]=(C0-C2)/2^{BT}`.

The trace is real and strictly positive because Q_G is invertible. Hence `C0-C2` is a positive integer. The counts, their difference, and the denominator exponent all have O(n) bits for fixed parameters. Exponentially severe sign cancellation is harmless to this exact subtraction; replacing exact counts by relative approximations would not be justified.

Taking the logarithm of the resulting positive rational to the required additive accuracy is polynomial-time bit arithmetic. When separately approximating `log(C0-C2)` and `BT log 2`, account for the multiplication by BT in the precision allotted to log 2. No exponentially long *precision* is needed: the count integers themselves have only as many bits as there are Boolean variables.

## Uniform width-3 refinement and vanishing density error

The full forbidden-pattern truth table must **not** be used to assert a uniform result for growing B; its size and width then grow. Instead use a deterministic binary circuit.

There are at most `2^{2k+1}` choices of local input/output bits and component. For each magnitude output bit, a hardwired lookup uses O_k(1) Boolean gates; all B+O(1) magnitude bits therefore cost O_k(B) gates. Sign lookup is O_k(1). A ripple comparison `z<magnitude` uses O(B) gates. Modulo-4 phase addition costs O(1). Use fan-in-two AND/OR/XOR/NOT gates, a fixed constant bit when needed, and enforce every output equivalence by standard Tseitin clauses of width at most 3. Every auxiliary output is uniquely determined by the original variables. Pin acceptance to 1 and close the trace with equality clauses.

This gives, **uniformly in B and r**,

```
N = O_k(n + T(B+1)) = O_{k,Delta}(n r(B+1)),
number of clauses <= D_* N + O(1),
clause width <= 3,
```

where D_* is an absolute gate-encoding constant, independent of B,r,epsilon. A constant factor depending on k occurs in variable count, not in an epsilon-dependent clause-width parameter. Consequently the supplied sparse #3SAT theorem has a fixed asymptotic constant here.

For ground-energy density choose beta=4/epsilon. The entropy bound gives `0<=E0/n-f_beta<=epsilon/4` for qubits. Choose r as above with the smallest adequate integer up to a fixed constant factor. Then

```
r=Theta_{k,Delta,J}(epsilon^{-3/2}),
delta=Theta_{k,Delta,J}(sqrt(epsilon)),
eta=Theta_{k,Delta,J}(epsilon^{3/2}),
B=O_{k,Delta,J}(log(1/epsilon)+1),
N=O_{k,Delta,J}(n epsilon^{-3/2}(log(1/epsilon)+1)).
```

Rounding, product formula, logarithm arithmetic, and the entropy inequality each receive epsilon/4. Total error is at most epsilon.

Thus a rational sequence `epsilon_n=1/ceil((ceil(log_2(n+2)))^{1/4})` gives ground-energy-density error tending to zero, with

`N=O(n (log n)^{3/8} log log n)`

and conditional counting time

`poly(L,n) 2^{O(n log log n/(log n)^{1/8})}=poly(L,n) 2^{o(n)}`,

using polynomial space. More generally `epsilon_n=Theta((log n)^{-a})` works for every fixed `0<a<1/3`. **The boundary a=1/3 is not established by these estimates** because of the extra log-log factor. Neither inverse-polynomial density error nor inverse-polynomial total-energy error follows.

## Primary comparators actually inspected; novelty not established

1. [Le Gall, *Classical Algorithms for Constant Approximation of the Ground State Energy of Local Hamiltonians*, arXiv:2410.21833v2 (2025), Theorem 2](https://arxiv.org/html/2410.21833v2): the unguided general-local-Hamiltonian algorithm is randomized, takes `2^{O(n)}` time and polynomial space for fixed error measured against the sum of local norms. For bounded incidence and strength that is density-scale accuracy. This is a substantially stronger baseline than exact diagonalization alone. The guided result needs sample/query access to a useful guide; that is not supplied here.

2. [Bravyi, Chowdhury, Gosset and Wocjan, *On the complexity of quantum partition functions*, arXiv:2110.15466v2, Sections 1 and 4](https://arxiv.org/pdf/2110.15466): their general classical relative-error partition-function algorithm is essentially `2^n` up to polynomial factors; their polynomial-time density-scale free-energy approximation assumes a dense 2-local interaction condition, unlike arbitrary bounded-degree expanders. Their statement that general free-energy estimation is polynomial-time reducible to #P does **not by itself** establish the desired volume-subexponential consequence: a polynomial-size reduction may introduce superlinear Boolean variables. Their usual QPF precision is also stronger than density precision.

3. [Childs, Su, Tran, Wiebe and Zhu, *A Theory of Trotter Error*, arXiv:1912.08854v3, Sections 3 and 4.3](https://arxiv.org/pdf/1912.08854): imaginary-time formulas, multiplicative errors, relative eigenvalue comparison, and partition-function applications are established machinery. The reviewed examples cover particular Ising/ferromagnetic algorithms. This makes an unqualified claim of a newly invented thermal product-formula method inappropriate; this audit did not find their displayed bounds already stating the present bounded-incidence, volume-uniform log-density theorem.

4. [Chia and Shen, *3-Local Hamiltonian Problem and Constant Relative Error Quantum Partition Function Approximation*, arXiv:2510.07495](https://arxiv.org/abs/2510.07495): their fine-grained statements concern a stronger relative-partition-function-error task and a QSETH assumption. They are not a density-error obstruction to this explicitly conditional construction.

The path-sum/GapP style conversion and uniquely extended circuit-to-CNF step are standard techniques. The inspected supplied SAT source states graph-counting and local-Boolean-map consequences but not this quantum thermodynamic-density consequence. That limited inspection and these comparator checks do not establish historical priority or exhaustive novelty. The defensible claim is a checked **conditional consequence with explicit linear/quasilinear Boolean-size control**, not a new foundational counting algorithm or an unconditional many-body simulation breakthrough.

## Remaining receipt boundaries

- The exact #SAT theorem remains a hypothesis here.
- Root must retain separate exact compiler regression evidence; this audit is algebraic rather than a code verification.
- No practical crossover estimate, runnable full #SAT solver, physical material model, or empirical superiority is asserted.
- For growing parameters, use the uniform width-3 circuit construction, not the constant-width truth-table wording of the initial draft.

## Frozen addendum and independent replay (17:35 UTC)

I subsequently read root's full `VANISHING_ACCURACY_ADDENDUM.md` and both test source files and results. The addendum's rational constant C, `r=ceil(C epsilon^{-3/2})`, error budget, uniform density control, and `a<1/3` threshold agree with this audit. The original draft's pending-status statements are historical; this additional receipt does not silently rewrite that reviewed draft.

I copied both test programs into `independent_replay/`, executed them successfully, and compared both resulting JSON files byte-for-byte with the root results (`cmp` returned success). The test inputs are exact rational matrices and exact Boolean logic. Actual replay confirms all four palindrome cases, including `C0=378, C2=32`, and all comparator tests for selector widths 1 through 5 plus signed lookup/phase tests. The two exact imaginary phase counts match in every palindrome case.

Precise coverage limits remain: the signed test uses whole one- and two-qubit matrices and phase-lift elimination, not a run of the imported asymptotic #SAT solver; it does not exercise partial-wire routing in larger systems. The width-3 test exercises comparator and signed-lookup/phase building blocks and exact-equivalence gate clauses. Unique extension follows by the explicit DAG/equivalence argument, not exhaustive enumeration of every auxiliary assignment. Neither test is an integrated arbitrary-Hamiltonian rounding-to-width-3-to-count implementation.

Frozen reviewed hashes:

- `VANISHING_ACCURACY_ADDENDUM.md`: `1657923ce5386c6e4f9f3b4317e60497f8e8d0359424c34e60de6d15933f35bf`
- `check_signed_cnf.py`: `6249b858a420e811c8f0725214f348d84eaf0ee2b40b6863c8e91b1ef0b5bac8`
- `check_signed_cnf.json`: `9121423d88c68db6bd8341648676fcb0ed0542ac93a842502cd78e5d0760e5b1`
- `check_unique_3cnf.py`: `5548c891bd237ba370537728bf091c592eb32d58359feb296c260077ce2c3972`
- `check_unique_3cnf.json`: `b90c4177a07e55aaf5efc07b645a698be7789ac493db692ecb55831c9cc34f73`

**Final frozen verdict:** conditional mathematical PASS for fixed accuracy and the stated logarithmically vanishing accuracy; successful independent replay of the stated, limited regression suite; imported counting premise and historical novelty remain outside the certificate.
