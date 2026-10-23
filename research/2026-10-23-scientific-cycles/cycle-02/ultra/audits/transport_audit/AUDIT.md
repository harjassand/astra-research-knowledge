# Bounded independent audit of the two exact transports

Verdict: **both stated claims are valid under the exact hypotheses**. Claim B admits a useful strengthening from `min(h_a,N)` to `min(h_a,N-1)` for task-product unitaries. No universal unrestricted critical witness, output approximation statement, entanglement-cost statement, or efficient preparation claim follows from either transport alone.

This audit is independent of the proof of the reference basis inequality. That reference inequality is an explicit premise here. All steps below are finite-dimensional algebra. `check_transport.py` checks actual matrices of Hilbert dimension at most 16, with a measured CPU time below 0.02 seconds on the recorded run. The checks are falsification/sanity tests, not the justification of universal statements.

## Conventions that are load-bearing

Let `H=(C^D)^{tensor rN}`, with task `a` containing the ordered sites `1,...,N`. Let

`A_ai = I_(a,1...i) tensor B(H_(a,i+1...N)) tensor B(H_other_tasks)`

and let `E_ai` be the Hilbert-Schmidt orthogonal projection onto this algebra:

`E_ai(Z) = (I_(a,1...i)/D^i) tensor Tr_(a,1...i)(Z)`,

with tensor factors put back in their physical order. All other task factors remain present. Set `E_a0=identity`, `p_ai(X)=||E_ai(X)||_HS^2`, and `F(X)=ln(D) sum_(a=1)^r sum_(i=1)^N p_ai(X)`. The Hilbert-Schmidt inner product is the ordinary unnormalized matrix trace. Thus `p_a0(X)=1` when `Tr(X^2)=1` and `X>=0`.

The expectations satisfy `E_ai E_a1=E_ai` for `i>=1`. The reference premise is

`H(c^2) >= F(diag_e(c)) - r C`

for **every** nonnegative vector `c` with `sum c_j^2=1`, including all permutations of every such vector. The entropy convention is `0 log 0=0`.

## Claim A: first-site-invisible block mixing

Let the reference basis be partitioned into blocks, with `E_a1(|e_j><e_k|)=0` for every task `a` and distinct `j,k` in a common block. Let `W` be any unitary that preserves these blocks, and let `f_l=sum_j W_jl e_j`. Write `B_jl=|W_jl|^2`.

For `X=sum_l c_l |f_l><f_l|`, expansion inside each block gives

`X = sum_j (Bc)_j |e_j><e_j| + sum_(j != k, common block) alpha_jk |e_j><e_k|`.

Nesting annihilates every displayed off-diagonal term under every `E_ai`, `i>=1`, so the claimed exact identity holds:

`E_ai X = E_ai(diag_e(Bc))`.

The same matrix `B` works for every task and prefix. It is doubly stochastic by unitarity. Birkhoff decomposition gives `B=sum_pi w_pi P_pi`, with `w_pi>=0` and `sum w_pi=1`. Convexity of each squared Hilbert-Schmidt norm gives

`F(X) = F(diag_e(Bc)) <= sum_pi w_pi F(diag_e(P_pi c)) <= H(c^2)+rC`.

Every vector `P_pi c` is still nonnegative with norm one, and `H((P_pi c)^2)=H(c^2)`. Since the `f_l` form an orthonormal basis, `S(X^2)=H(c^2)`. This proves the **same constant** for the new basis. Importantly, `Bc` need not have norm one: the proof does not apply the reference entropy inequality directly to `Bc`; it applies it separately to the normalized permutation vectors.

This argument does not use primeness, stabilizer structure, commutation of reference compressions, or a product condition on the basis vectors. Those features may be needed to establish the reference premise, but not to transport it.

### Actual four-dimensional noncommuting example

Take `D=2`, `r=2`, `N=1`, and the computational basis ordered `00,01,10,11`. Mix the complementary pairs `{00,11}` and `{01,10}` with real rotation blocks having squared cosines `9/10` and `3/5`, respectively. For example,

`f_0=(3|00>+|11>)/sqrt(10)`.

Each pair differs on the first site of both tasks, so both partial traces kill its cross dyad. Define the actual compressed matrices by

`(K_a)_lm = Tr(E_a1(|f_l><f_l|) E_a1(|f_m><f_m|))`.

Direct partial traces give

```
K_A = (1/100) [ 41 21 29  9 ]    K_B = (1/100) [ 41 29 21  9 ]
             [ 21 26 24 29 ]                 [ 29 26 24 21 ]
             [ 29 24 26 21 ]                 [ 21 24 26 29 ]
             [  9 29 21 41 ]                 [  9 21 29 41 ]
```

Their commutator is

```
[K_A,K_B] = (3/125) [  0  1 -1  0 ]
                     [ -1  0  0  1 ]
                     [  1  0  0 -1 ]
                     [  0 -1  1  0 ],
```

with Hilbert-Schmidt norm `6 sqrt(2)/125`. Thus the noncommutation is real and occurs for the actual compressed expectations, not a freely chosen surrogate kernel.

Also `<f_0|Z tensor I|f_0>=4/5`. A pure two-qubit Pauli stabilizer state's expectation of any Pauli is `0`, `1`, or `-1`, as follows by expanding its rank-one stabilizer projector in the Pauli basis. Hence `f_0` is not a stabilizer state. Its unequal Schmidt weights are `9/10,1/10`.

### Scope and checks against overextension

- The block hypothesis is restrictive. Across any first site of dimension `D`, vanishing `Tr_site(|e_j><e_k|)` means the Schmidt support subspaces on that site are orthogonal for distinct members of a block. To see this, write coefficient matrices `M_j` with columns indexed by that site: the condition is `M_j M_k^dagger=0`, so `range(M_j^dagger)` and `range(M_k^dagger)` are orthogonal. Their positive dimensions sum to at most `D`. In particular, every block has at most `D` members. Nontrivial blocks need not exist in an arbitrary reference basis.
- Computational complement pairs do satisfy the condition for qubits: the two strings differ at the first site of every task. Varying the rotation by pair is permitted and need not preserve compressed commutation.
- If first-site cancellation is omitted, the common-shadow identity fails. Mixing `00` and `01` into `|0+>` gives `E_A(|0+><0+|)=I_A/2 tensor |+><+|`, while diagonalizing the squared amplitudes before that expectation gives `I_4/4`. The script detects Hilbert-Schmidt error `1/2`.
- The proof sums prefixes `1,...,N`. If a convention also includes prefix zero, its actual contribution is the invariant `||X||_HS^2=1`; handle that term separately. The exact shadow identity at prefix zero generally fails.
- The entropy defect remains unchanged, but arbitrary block mixing is not thereby an efficient or free physical preparation. This transport does not certify all positive matrices or all nonstabilizer bases.

## Claim B: backward suffix-algebra containment

Let `U=tensor_a U_a` and let each `h_a` be a nonnegative integer. Assume the stated backward inclusion, extended by the full algebra on all other tasks:

`Ad(U^dagger)(A_ai) subset A_(a,max(i-h_a,0))`.

On Hilbert-Schmidt operator space, `T=Ad(U)` is a unitary. Therefore

`p_ai(UXU^dagger) = ||T^(-1) E_ai T X||_HS^2 = ||P_(T^(-1)A_ai) X||_HS^2`.

The inclusion of ranges and monotonicity of orthogonal projected norm yield the exact pointwise bound

`p_ai(UXU^dagger) <= p_(a,max(i-h_a,0))(X)`.

For `0<=h_a<N`, summing gives

`sum_i p_ai(UXU^dagger) <= h_a + sum_(j=1)^(N-h_a) p_aj(X) <= sum_i p_ai(X)+h_a`.

For `h_a>=N`, use `p_ai<=p_a0=1` to obtain the advertised allowance `N`. Positivity is not needed for this projection comparison; normalization supplies `p_a0=1`.

The tensor-product hypothesis on `U` ensures that the full algebra on every other task stays full under conjugation. Thus arbitrary intertask entanglement of `X` is allowed. Tracing out those other tasks or assuming `X` factors across tasks would change the proof's contract.

### Strengthening using the invariant terminal term

For a task-product `U`, tracing the complete task yields a conjugate by the other `U_b`, so

`p_aN(UXU^dagger)=p_aN(X)`.

Apply the pointwise estimate only to `i=1,...,N-1`. With `q_a=min(h_a,N-1)` and the empty sum interpreted as zero,

`sum_(i=1)^N [p_ai(UXU^dagger)-p_ai(X)] <= q_a - sum_(j=N-q_a)^(N-1) p_aj(X) <= q_a`.

The originally claimed `min(h_a,N)` is consequently correct but loose. In particular, when `N=1`, every taskwise unitary preserves the score exactly, regardless of its nominal depth.

If a certified class satisfies `S(X^2)>=F(X)-rC`, its conjugates satisfy

`S((UXU^dagger)^2) >= F(UXU^dagger)-rC-ln(D) sum_a min(h_a,N-1)`.

Replacing `N-1` by `N` gives the advertised weaker version. The new term is an upper allowance for the score change and entropy defect, not an automatically incurred or exact implementation cost. It is horizon independent only when the chosen causal widths are bounded independently of `N`.

### Circuit claim and an orientation counterexample

A standard circuit layer consists of disjoint nearest-neighbor two-site gates on the open chain, together with one-site gates. Pulling a suffix operator backward through one such layer enlarges its support leftward by at most one site. Pulling it through `h_a` layers therefore gives the assumed inclusion with width `h_a`. Serial overlapping gates cannot all be counted as one layer. A periodic wraparound edge does not have this open-chain guarantee.

The backward orientation is essential when the output is `UXU^dagger`. A forward-only condition with the same numerical width does not imply the claimed score bound. Here is a direct counterexample to that possible misstatement:

- One four-qubit task; let the site permutation send old sites `(1,2,3,4)` to `(4,1,2,3)`.
- Its **forward** suffix images have width one. Its **backward** suffix images require width three.
- Take `X=|0><0| tensor I_(sites 2,3,4)/sqrt(8)`, a positive matrix of Hilbert-Schmidt norm one.
- Before conjugation, the four prefix scores are `(1/2,1/2,1/2,1/2)`. After conjugation, they are `(1,1,1,1/2)`.
- The score gain is `3/2`, contradicting an incorrectly inferred allowance one.

The script verifies both the forward suffix-generator support and the actual score increase. This counterexample does not challenge the claim as stated: the stated hypothesis correctly uses `U^dagger`.

The independent suffix audit additionally gives positive examples with gain `h(1-D^-2)` using depth-`h` adjacent SWAPs of one half of a Bell pair. Thus a term linear in causal width is necessary uniformly in dimension, while the finite-dimensional upper allowance need not be attained.

## Disposition

- Claim A: **PASS**, with the common doubly stochastic shadow proof and an explicit nonstabilizer, noncommuting example.
- Claim B: **PASS**, with the sharpened terminal-invariant allowance available.
- Suggested wording corrections: call the latter an allowance or bound rather than an exact physical cost; state nonnegative integer widths, the backward adjoint, all spectator factors, and conventional open-chain layer depth explicitly.
- Unrestricted critical tensor witness: **NOT ESTABLISHED BY THESE TRANSPORTS**. Reference correctness, novelty, efficient preparation, operational formation cost, and physical implementation remain separate questions.

Artifacts: `AUDIT.md`, `suffix_independent.md`, `check_transport.py`, and `CHECKS.json` in this directory. No external messages, uploads, or deliveries were performed.
