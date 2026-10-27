**The strongest construction now gives polynomial-time exact counting at unbounded module rank and every nilpotent depth, for a family whose hidden representation is acquired from raw Boolean coefficients. I also proved a hardness boundary inside that same family.**

### The constructive result

The input contains \(n\) original independent bits and an explicit cubic Boolean polynomial of description length \(L\). The compiler recovers the hidden algebra
\[
A=\mathbb F_{2^d}[t]/(t^e),\qquad n=(2r+1)de,
\]
its coordinates, the affine center, and the ordinary cubic phase.

For the strongest family, a further semilinear construction manufactures coordinates in which the residue cubic is
\[
\begin{aligned}
H_0={}&\gamma\sum_{i=1}^{r}
\left(X_i^3+X_iY_i^2+Y_i^3+ZX_iY_i\right)\\
&+\gamma Z\sum_{i=1}^{r}(a_iX_i^2+b_iY_i^2)+\tau Z^3,
\end{aligned}
\]
where \(a_i,b_i\in\mathbb F_2\) and \(\gamma\ne0\). Neither these blocks nor their useful coordinates are supplied.

The construction allows arbitrary higher nilpotent cubic coefficients and an arbitrary-rank binary quadratic supported on the first \(h\) ring layers, with \(3h\le e+1\). For \(d\ge3\), \(3\nmid d\), and unbounded \(r\ge2\), the conservative bit bounds are
\[
T=O(Ln^2+n^{12})+\widetilde O(d^{31}),\qquad
S=O(L+n^6)+\widetilde O(d^{20}).
\]

The decisive reduction is that the acquired pair computations have only **eight possible joint Gaussian states**. Eight manufactured moments recover their signed multiplicities exactly. Seven moments become explicit cubic point counts in at most **eight field variables**, regardless of module rank; the remaining moment is a binary Gaussian. Exact reconstruction then restores the original count using polynomial-bit arithmetic. The finite-field complexity bound uses the established Lauder–Wan algorithm. :chatgpt-content-reference{index="0"}

**The generic Lauder–Wan engine is not implemented here.** Acquisition, hypersurface manufacture, and reconstruction are implemented and executed; the reference terminal explicitly records its field scan.

### The sharper obstruction

I then tested whether the restriction \(3\nmid d\) could be removed.

At **\(d=3,e=2\)**, the same residue family \(J_r\), with no quadratic noise, becomes #P-hard when arbitrary higher nilpotent cubic coefficients are permitted. A Boolean cubic on \(N\) variables is embedded using
\[
n=12N+18
\]
original bits, and one exact ring count recovers its signed count by an explicit affine formula.

This is stronger than hardness somewhere in the broader geometric class: it isolates a failure within the very family supporting the polynomial theorem. Raw, affinely disguised **42- and 66-bit instances** acquired the full six-dimensional centroid and recovered their source counts exactly.

### Executed evidence

- A **72-input circuit** with 25,678 supplied gates—8,380 affecting the output—preserved its exact output polynomial and returned signed count \(-549755813888\). Gate states never became independent counting variables; expansion costs are charged.
- A **100-bit raw instance** exercised depth \(5\to2\) with rank-40 quotient noise.
- An **80-bit raw instance** exercised depth \(4\to1\), arbitrary higher cubic coefficients, and rank-20 noise, matching an independently exhausted field terminal.
- **112 actual manufactured hypersurfaces** over \(\mathbb F_2\) and \(\mathbb F_4\) were exhaustively counted over **1,728,136 assignments**, agreeing with separately expanded character sums.

The proof includes description sizes, arithmetic costs, acquisition completeness, the new divisibility obstruction, and preserved failures. Historical priority and practical speed advantage remain unestablished.

:chatgpt-content-reference{index="2"}

[Astra_P3_Local_Algebra_Proofs_and_Code.zip](https://chatgpt.com/library?file_id=libfile_7e793c876b508191b979a631589dc89d&account_id=personal) — complete proof sources, executable programs, raw inputs, exact results, and independent audits. A fresh extraction reproduced the raw 36-bit count.