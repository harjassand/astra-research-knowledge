# Matched-record rank lemma audit

## Verdict

The rank/record lemma passes for a mixed Choi state $J$ with tracial full output marginal $J_{\rm out}=I/M$ and the exact matched-record subspace in the cross partition. It requires no purity, no diagonality, and no translation invariance. Conditional on the separate exact-QCA rank-ratio premise, all constants in the proposed deficit bound check.

## Projection and marginals

Let $M=D^{2r}$ be the dimension of either cross part, with $A=L'_1R_1$ and $B=L_1R'_1$. Reorder the computational bases so a string $x\in[M]$ in $A$ is paired with the same physical input/output record in $B$. Then
$$
\Pi=\sum_x |x,x\rangle\langle x,x|,\qquad G=\Pi J\Pi,\qquad q=\operatorname{Tr}G=1-E.
$$
This $\Pi$ is the event that all $2r$ cell records match. Since $G$ is supported on the span of $|x,x\rangle$, it has the form $G=\sum_{x,y}g_{xy}|x,x\rangle\langle y,y|$. Partial trace kills its off-diagonal terms, so
$$
G_A=G_B=\sum_x g_x|x\rangle\langle x|,\qquad g_x=g_{xx}\ge0,\qquad \sum_xg_x=1-E.
$$
No assumption that $J$ itself is diagonal was used.

For each matched basis vector $|x,x\rangle$, the corresponding full output record is fixed. Its matched joint probability satisfies
$$
g_x=\langle x,x|J|x,x\rangle\le \Pr_J[\text{that full output record}]=1/M,
$$
where the final equality uses the **full** output marginal $I/M$. Therefore every diagonal difference $1/M-g_x$ is nonnegative and
$$
\|G_A-I/M\|_1=\|G_B-I/M\|_1=\sum_x(1/M-g_x)=E.
$$
The tracial hypothesis is load-bearing: a nonunital channel or a nontracial output marginal need not give this coordinatewise cap.

## Gentle projection, distance, and constants

The gentle-measurement bound applies to arbitrary mixed $J$ and the subnormalized post-projection operator $G$:
$$
\|J-G\|_1\le2\sqrt{1-q}=2\sqrt E.
$$
Partial trace is trace-norm contractive on the Hermitian difference, hence, for either cross marginal,
$$
\frac12\|J_A-I/M\|_1
\le\frac12\|J_A-G_A\|_1+\frac12\|G_A-I/M\|_1
\le\sqrt E+E/2.
$$
If $\operatorname{rank}J_A\le M/a$, then its support projector gives
$$
\frac12\|J_A-I/M\|_1\ge1-\frac{\operatorname{rank}J_A}{M}\ge1-1/a.
$$
Combining and setting $t=\sqrt E$ yields $t+t^2/2\ge1-1/a$, so
$$
E\ge\bigl(\sqrt{3-2/a}-1\bigr)^2.
$$
This bound is valid even though $G$ and its marginals have trace $1-E$, not one. The triangle inequality compares that subnormalized $G_A$ directly to the normalized $I/M$, and its trace-norm deficit is exactly $E$.

Conditional on the proposed ratio $\operatorname{rank}(J_A)/\operatorname{rank}(J_B)=\kappa^{-2}$ (or its inverse), with $a=\max(\kappa^2,\kappa^{-2})$, the rank bounds $\operatorname{rank}J_A,\operatorname{rank}J_B\le M$ imply that at least one cross marginal has rank at most $M/a$. The lemma then applies to that marginal. I have not audited the separate rank-ratio theorem.

## Error conversion and physical record

If $\epsilon_i$ is the total full-cell input/output mismatch probability at site $i$, then the all-record failure probability obeys the ordinary union bound
$$
E=\Pr[\text{some mismatch in }S]\le\sum_{i\in S}\epsilon_i.
$$
Thus with $|S|=2r$, $\frac1{2r}\sum_i\epsilon_i\ge c_a/(2r)$ and $\max_i\epsilon_i\ge c_a/(2r)$, where $c_a=(\sqrt{3-2/a}-1)^2$. For component totals, first use $\epsilon_i\le e_{A,i}+e_{B,i}$. These are total mismatch probabilities; per-label joint masses must be summed over labels before applying this step.

The event $\Pi$ is exactly the Choi all-record-match event after cross-partition reordering. Under $\alpha=\sigma^{-1}\Omega$, trace invariance maps it to the actual tags A-input $(i-1)$/output $i$ and B-input $i$/output $i$; product-maximally-mixed input on $U=[a-\max(R_\Omega,1),b+R_\Omega]$ supplies the required causal window. The result is conditional on an exact QCA Choi state and tracial output marginal, not an index assignment to a general noisy process.
