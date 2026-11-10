# P1 Xi return — Wright–Fisher transition observations

Source: https://chatgpt.com/c/6af1a606-c6c8-83ec-b948-b552107573bf
Response: 13a08d35-c627-478e-82ff-6a8a1966f483; latest human turn: 6f8572b7-1caf-4bcc-b5b1-3422f5603b4d (“continue”).
Original question: work/astra-renewed-pro-programmes-20261103/P1_FULL_WF_FINITE_OBSERVATION_AFTER_CAC733_WARM_XI_20261110.txt; posted content SHA-256 24197df387106fe7c16c5a95d3fc558547ce052dcd953a4fdf7b367dd0c0576a.
Model shown: Extra High. Captured 2026-11-10 approximately 03:58 UTC. No ZIP was identified in the visible return.

## Available visible activity

Previous activity: Refined dual simulation, graphical dual construction, and complexity analysis.

Worked for 21m 11s:
Planned analysis using a dual approach. Tested dual efficiency and refined the simulation plan. Assessed mixing and searched for justification. Studied spectral behavior and finalized neutral sampling simulation. Searched the web.

ChatGPT said: A tractable subproblem is now closed: in the neutral case S = 0, a finite Kingman coalescent with parent-independent mutation generates the entire shared-latent observation row, including boundary starts. Combining a polynomial-time finite-horizon simulation with an absorption-time cutoff handles arbitrarily large binary times. I’m checking whether the selection ancestry can be truncated with a polynomial—not exponential—dependence on S.

Analyzed selection coupling, bounds, duality, and finite-horizon simulations. Assessed tractable simulation regimes and formulated neutral genealogical sampling. Bounded simulation cost and developed an algorithm. Searched the web. Assessed the algorithm. Computed rigorous ASG mixing and sampling bounds. Quantified the reduction. Proved ASG limits and sampling algorithm.

## Complete native response

# Wright–Fisher transition observations: scientific continuation

## 1\. New result: a uniform quantitative mixing certificate

I obtain a positive result for the full \(K\)\-allele model with arbitrary genic selection and positive mutation, but the resulting complexity bound has an exponential dependence on selection strength \(S\)\. It therefore does **not** yet establish the requested polynomial-in-\(V\) theorem.

The main new ingredient is an explicit mixing-time certificate derived from an ancestral selection graph.

Let \(\mathcal O_{t,x}^{(r)}\) denote the required joint distribution of the \(r\) observations at time \(t\), and let \(\mathcal O_\infty^{(r)}\) denote their stationary joint distribution.

Define

\[
\boxed{
H(\alpha_0,S)
=4e^S(1+\alpha_0^{-1})^2(1+S).
}
\]

Then, for every \(K\ge2\), \(r\ge0\), every initial \(x\) including the simplex boundary, and every \(t\ge0\),

\[
\boxed{
\operatorname{TV}\left(
\mathcal O_{t,x}^{(r)},\mathcal O_\infty^{(r)}
\right)
\le
2^{-\lfloor t/(2H(\alpha_0,S))\rfloor}.
}
\tag{1}
\]

The striking property is that the certificate is **independent of the number of alleles, the observation count and the individual mutation parameters**, except through \(\alpha_0\)\.

This is a uniform upper bound, not an assertion that the actual mixing time is exponentially large in \(S\)\.

It already provides an all-time algorithm with certified whole-row error and finite-bit computation whose cost is polynomial in the ordinary input size, numerical selection strength, inverse mutation, accuracy and \(e^S\)\.

In particular, it yields a complete polynomial-resource affirmative result on the nontrivial subfamily

\[
\boxed{
S\le \left\lfloor\log_2(1+L+V)\right\rfloor.
}
\tag{2}
\]

This includes \(S=0\), all \(K\), all \(r\), arbitrarily small positive mutation, every rational initial boundary point, and arbitrarily large or small binary times.

The unrestricted strong-selection endpoint remains to be settled.

## 2\. Proof of the mixing certificate

### Ancestral representation

Use the classical ancestral selection graph (ASG) representation of the Wright–Fisher diffusion. Its branching–coalescing structure is established in the ancestral-selection literature. citeturn281901search1turn281901search2

Begin with \(r\) active ancestral lineages, one for each requested observation.

When there are \(n\) active lineages, run the following backward transitions\:

| Event | Total rate | Effect |
|--------|--------|--------|
| Coalescence | \(n(n-1)/2\) | Merge two uniformly chosen lineages |
| Mutation | \(n\alpha_0/2\) | Resolve one lineage to a label \(i\) with probability \(\alpha_i/\alpha_0\) |
| Selection | \(nS/2\) | Split one lineage into continuing and incoming potential ancestors |

At a selection branch, the incoming ancestor replaces the continuing ancestor with probability \(\sigma_i/S\), where \(i\) is the incoming ancestor's eventual type. The decision is resolved when the graphical ancestry has been assigned types.

This rule gives exactly the requested genic-selection drift: if the two potential parental types are independently distributed with frequencies \(x\), the change in the probability of choosing type \(i\) at a branch is

\[
\frac{x_i(\sigma_i-\boldsymbol{\sigma}\cdot x)}{S}.
\]

Multiplication by the branch rate \(S/2\) produces

\[
\frac12x_i(\sigma_i-\boldsymbol{\sigma}\cdot x).
\]

Similarly, the coalescence and mutation mechanisms reproduce the diffusion and parent-independent mutation terms of the stated generator.

The generator identity holds for the joint sample monomials \(\prod_{j=1}^r x_{y_j}\), not merely for the one-label probabilities. Consequently, this graphical construction represents the **entire joint observation law**\.

At backward time \(t\), independently assign Cat\((x)\) types to unresolved ancestral lineages, and propagate all types forward through the recorded graph.

Mutation events eliminate dependence on ancestry earlier than that mutation. If no active lineages remain, the resulting output is independent of \(x\)\.

### The active-lineage birth–death chain

Let \(N_u\) be the number of unresolved potential ancestors at backward time \(u\)\. Its transition rates are

\[
b_n=\frac{Sn}{2},\qquad
d_n=\frac{n(n-1+\alpha_0)}2,
\tag{3}
\]

with state \(0\) absorbing.

Let \(T_n\) denote the time to absorption from \(n\), and put

\[
e_n=\mathbb E T_n,\qquad
\Delta_n=e_n-e_{n-1}.
\]

The first-step equations give

\[
\Delta_n=\frac1{d_n}+\frac{b_n}{d_n}\Delta_{n+1}.
\]

The minimal nonnegative solution is

\[
\Delta_n=
\sum_{j=n}^{\infty}
\frac1{d_j}
\prod_{\ell=n}^{j-1}
\frac{S}{\ell-1+\alpha_0}.
\tag{4}
\]

For \(n\ge2\), elementary factorial domination gives

\[
\Delta_n\le\frac{2e^S}{n(n-1)}.
\]

For \(n=1\),

\[
\Delta_1\le
\frac2{\alpha_0}
\left(1+\frac{S}{\alpha_0}e^S\right).
\]

Summing these inequalities yields

\[
\boxed{
\sup_{n\ge1}\mathbb E T_n
\le4e^S(1+\alpha_0^{-1})^2(1+S)=H.
}
\tag{5}
\]

This proves finite expected extinction time independently of the initial number of lineages.

### From expected extinction to exponential mixing

Markov's inequality gives, uniformly in the current number of unresolved lineages,

\[
\Pr_n(T_n>2H)\le\frac12.
\]

Apply the strong Markov property successively over intervals of length \(2H\)\:

\[
\boxed{
\Pr_n(T_n>t)
\le2^{-\lfloor t/(2H)\rfloor}.
}
\tag{6}
\]

Couple the ancestry stopped at time \(t\) with the same ancestry continued to complete resolution.

On the event that every lineage has been resolved before \(t\), their observation rows agree regardless of the initial \(x\)\.

The completely resolved genealogy has the stationary observation law, since the Wright–Fisher diffusion with positive parent-independent mutation has the stated unique tilted-Dirichlet stationary distribution. citeturn858726view0

The coupling inequality and (6) prove (1).

No dimension-dependent minorisation constant, continuous-state density evaluation or interior-start assumption is used.

---

## 3\. A single finite-bit algorithm for all parameters

The mixing theorem can be combined with the accepted stationary compiler and a new rational finite-horizon graphical simulator.

This produces one algorithm valid for **every** input in the full mathematical model. Its limitation is resource complexity, not correctness or termination.

Define the integer

\[
B=1+L+V,\qquad E=4^{\lceil S\rceil}.
\]

Notice that \(E\) can be constructed exactly as the integer \(2^{2\lceil S\rceil}\), using only \(O(S)\) output bits. No numerical evaluation of \(e^S\) is needed.

Choose

\[
T_{\rm cut}=256EB^4.
\]

The algorithm has three branches.

1. **At \(r=0\) or \(t=0\)\:** Return the empty row or \(r\) independent Cat\((x)\) draws, respectively. Both are exact.
2. **At \(t\ge T_{\rm cut}\)\:** Use the accepted N1795 stationary observation compiler at tolerance \(\epsilon/4\)\.
3. **At \(0<t<T_{\rm cut}\)\:** Simulate the ancestral selection graph to time \(t\), with a certified finite-lineage truncation and rational uniformisation described below.

### Finite-horizon truncation

The expected active-lineage count satisfies

\[
\frac{d}{du}\mathbb E N_u
\le
\frac12(S+1)\mathbb EN_u
-\frac12(\mathbb EN_u)^2.
\]

Therefore

\[
\sup_{u\ge0}\mathbb EN_u
\le\max\{r,S+1\}\le2B.
\]

The expected number of selection births before time \(t\) is consequently at most

\[
\mathbb E[\text{births by }t]\le B^2t.
\tag{7}
\]

Set the integer lineage cap

\[
H_{\rm line}=2^{15}EB^8.
\]

Since each birth increases the active-lineage count by at most one, (7) and Markov's inequality give

\[
\Pr\left(\sup_{u\le t}N_u>H_{\rm line}\right)
\le\frac{\epsilon}{64}.
\tag{8}
\]

The simulator returns any valid fallback row if it would cross this cap. That fallback is explicitly included in the error budget.

### Rational uniformisation without exponential clocks

Choose the integer dominating rate

\[
\Lambda=2H_{\rm line}^2.
\]

For every state below the cap, the true total jump rate is at most \(\Lambda\)\.

Ordinary continuous-time uniformisation represents the ancestral graph using a Poisson number of proposals with mean

\[
\mu=\Lambda t.
\]

Instead of sampling that Poisson variable using unbounded real arithmetic, set

\[
M=2^{85}E^6B^{41}
\]

and generate \(M\) independent Bernoulli trials with the rational success probability

\[
p=\frac{\mu}{M}.
\]

Each success applies one step of the rational uniformised graphical transition kernel; a self-loop leaves the graph unchanged.

This is a completely finite-bit simulation. For the chosen parameters,

\[
\mu\le2^{39}E^3B^{20}.
\]

Le Cam's Poisson approximation inequality gives

\[
\operatorname{TV}\left(
\operatorname{Bin}(M,\mu/M),\operatorname{Pois}(\mu)
\right)
\le\frac{2\mu^2}{M}
\le\frac{\epsilon}{64}.
\tag{9}
\]

Coupling the uniformised event counts and using identical event choices whenever those counts agree bounds the entire graph-law error, not just its moments.

Finally, assign the time-zero ancestral types using Cat\((x)\), resolve the recorded mutation and selection decisions and read the \(r\) ordered leaves.

### Complete TV certificate

For the finite-time branch,

\[
\operatorname{TV}(\mathcal L(Y),\mathcal O_{t,x}^{(r)})
\le
\underbrace{\frac{\epsilon}{64}}_{\text{lineage cap}}
+
\underbrace{\frac{\epsilon}{64}}_{\text{Poisson approximation}}
\le\frac{\epsilon}{32}.
\tag{10}
\]

For the large-time branch, (5) implies

\[
H\le32EB^3.
\]

Hence, at \(t\ge256EB^4\),

\[
\frac{t}{2H}\ge4B,
\]

so

\[
\operatorname{TV}(\mathcal O_{t,x}^{(r)},\mathcal O_\infty^{(r)})
\le2^{-4B}\le\frac{\epsilon}{8}.
\]

Adding the stationary compiler's \(\epsilon/4\) error gives

\[
\operatorname{TV}(\mathcal L(Y),\mathcal O_{t,x}^{(r)})
\le\frac{3\epsilon}{8}.
\tag{11}
\]

Thus every branch satisfies the required whole-row TV accuracy.

## 4\. Finite-bit resource accounting

The algorithm uses exact rational and integer operations throughout. To sample a rational Bernoulli probability \(a/b\), draw a uniform integer on \(\{0,\ldots,b-1\}\) using fair-bit rejection and compare it with \(a\)\. Every such choice has fewer than two rejection rounds in expectation.

The construction charges the following operations\:

- Parsing and exact construction of \(\alpha_0,\sigma,S,B,E\), all caps and rational probabilities.
- Every uniformisation proposal, graph transition, active-lineage selection and mutation-label choice.
- The complete ancestral graph, including potential ancestors and selection decisions.
- Rational fair-bit selection, time-zero labels and ordered output construction.
- The accepted stationary compiler's integer convolutions, backtracking and Pólya urn.

Using schoolbook arithmetic and a linear-space graphical representation, conservative universal bounds are

\[
\boxed{
\begin{aligned}
\mathbb E[\text{total bit operations}]&\le2^{200}(B+E)^{128},\\
\mathbb E[\text{fair bits}]&\le2^{200}(B+E)^{128},\\
\text{peak memory bits}&\le2^{200}(B+E)^{128}.
\end{aligned}
}
\tag{12}
\]

The same bound covers the explicit \(r\)\-label output work.

These deliberately loose constants follow from the displayed integer \(M\), the fact that each graphical proposal requires polynomially many operations on integers of polynomial bit length in \(B+\log E\), and the accepted stationary compiler's polynomial bounds.

Crucially, **there is no polynomial dependence on the numerical value of \(t\)**\. Only its binary encoding is processed, and the threshold branch handles times of arbitrarily large magnitude.

However, since \(E=4^{\lceil S\rceil}\), (12) is exponential in \(S\)\.

### Polynomial-resource corollary

If

\[
S\le\lfloor\log_2B\rfloor,
\]

then

\[
E\le4B^2.
\]

Consequently (12) implies the explicit bound

\[
\boxed{
\mathbb E[\text{bit work}],\
\mathbb E[\text{fair bits}],\
\text{peak memory},\
\text{output work}
\le 2^{600}B^{256}.
}
\tag{13}
\]

This is a computably uniform polynomial-resource algorithm satisfying every other clause of the requested contract throughout that restricted selection range.

For neutral selection \(S=0\), this gives a complete all-time, all-dimension, all-boundary, shared-latent observation algorithm without needing the stationary compiler's selection machinery.

---

## 5\. Why the same construction does not close unrestricted strong selection

The exponential \(e^S\) factor above is not merely an artefact of a careless inequality for the **unpruned** ancestry.

Consider \(K=2\), \(\alpha_1=\alpha_2=1/2\), \(r=1\), and fitness coefficients \((S,0)\)\.

Then \(\alpha_0=1\), and the active-lineage rates become

\[
b_n=\frac{Sn}{2},\qquad d_n=\frac{n^2}{2}.
\]

The exact expected time to eliminate all potential ancestral lineages, beginning with one, is

\[
\mathbb E_1T
=
2\sum_{k=0}^\infty
\frac{S^k}{(k+1)^2k!}.
\]

If \(Z\sim\operatorname{Pois}(S)\), this is

\[
\mathbb E_1T
=2e^S\mathbb E\frac1{(Z+1)^2}.
\]

By Jensen's inequality,

\[
\boxed{
\mathbb E_1T\ge\frac{2e^S}{(S+1)^2}.
}
\tag{14}
\]

Moreover, since at least one lineage remains active until absorption, the expected number of selection births is at least

\[
\frac S2\mathbb E_1T
\ge\frac{Se^S}{(S+1)^2}.
\tag{15}
\]

Thus simulating the complete unpruned potential ancestry can require exponentially many events as selection grows.

**This is a rigorous obstruction to that particular computational mechanism, not a lower bound for the original Wright–Fisher observation problem.** The true diffusion may lose dependence on its initial condition much earlier, because many potential ancestral branches can become irrelevant after their types are resolved.

A successful unrestricted algorithm could exploit such pruning, a different transition dual, or a sharper mixing mechanism.

## 6\. Scientific conclusion

Established in this continuation

The new mathematical result is an explicit dimension- and observation-count-independent total-variation mixing certificate, together with a fully finite-bit, whole-observation transition algorithm whose cost is independent of the numerical time magnitude.

It gives a complete polynomial-resource affirmative theorem for \(S\le\lfloor\log_2(1+L+V)\rfloor\), while permitting arbitrary dimension, positive mutation scales, boundary starts and shared-latent observation lengths.

The exponential ancestral-extinction calculation explains precisely why this construction alone cannot deliver a polynomial bound for unrestricted numerical \(S\)\.

Still unresolved

The full user-defined capability requires universal \(C,p\) with cost bounded by \(C(1+L+V)^p\) even for \(S\) polynomially large in \(V\)\. I have not proved that bound or a complexity-theoretic obstruction to it.

The recent Sant–Jenkins–Ruggiero gamma-dual representation supplies a distinct exact multiallelic transition representation, but its published practical initialization and Gaussian approximations do not establish the uniform finite-bit resource bound required here. citeturn678519view3

**Final status: a constructive, certified all-time result with exponential selection dependence, a complete polynomial subfamily, and a rigorous ancestry-method obstruction. The universal polynomial-selection endpoint remains open.**
