# Random-relation variance and posterior-order comparator

Status: bounded primary comparison, 2026-10-24. No generic concentration or quantum-programming claim is made.

## Exact variance and a state-dependent consequence

Let `Gamma_e` be independent Bernoulli(`q`) variables, `T_e >= 0` fixed bounded operators, and

```text
W_Gamma = sum_e Gamma_e T_e,
S = sum_e T_e,
A_Gamma = W_Gamma - q S = sum_e (Gamma_e-q) T_e.
```

For `e != f`, independence and centering give `E[(Gamma_e-q)(Gamma_f-q)] = 0`; hence

```text
E A_Gamma^2 = q(1-q) sum_e T_e^2.
```

No commutation assumption on the `T_e` is needed: in the cross terms the scalar coefficient has zero expectation, while each diagonal term is exactly a scalar times `T_e^2`. If `sum_e T_e <= I` and `||T_e|| <= a`, positivity gives `T_e^2 <= a T_e`, and therefore

```text
E A_Gamma^2 <= q(1-q) a I.
```

For the stated `a=r/k^2`, this gives `q(1-q)r/k^2 I`.

Now let `phi` be a fixed normal state and, for every relation realization `gamma`, let `omega_gamma` be a normal state satisfying the same order domination `p omega_gamma <= phi`, with fixed `p>0`. Cauchy–Schwarz for positive functionals gives

```text
|omega_gamma(A_gamma)|^2 <= omega_gamma(A_gamma^2),
p |omega_gamma(A_gamma)|^2 <= phi(A_gamma^2).
```

The second line follows by applying the positive-functional order to the positive operator `A_gamma^2`. Averaging over the independent relation gives the exact operational consequence

```text
p E_Gamma |omega_Gamma(A_Gamma)|^2
    <= q(1-q) phi(sum_e T_e^2)
    <= q(1-q) r/k^2.
```

Thus, for `delta>0`,

```text
Pr_Gamma[ |omega_Gamma(W_Gamma-qS)| >= delta ]
    <= q(1-q) r / (p k^2 delta^2).
```

This is a second-moment/Chebyshev statement with a `1/p` postselection cost. It does not give an exponential tail, and its premise is a uniform order bound for each selected state; establishing that premise from the actual dephased-history construction is a separate step. It does not follow merely from a coherent pure Lüders branch without checking the order comparison. If `p` or the reference state varies with `gamma`, the displayed averaging step needs the corresponding weighted/order formulation and cannot be used as written.

## Closest primary concentration comparator

Tropp, “User-Friendly Tail Bounds for Sums of Random Matrices,” Theorem 6.1, is a bounded matrix Bernstein theorem. It assumes a finite independent sequence of centered self-adjoint matrices of fixed finite dimension `d`, with `lambda_max(X_e) <= R`, and variance parameter `sigma^2 = ||sum_e E X_e^2||`. It gives

```text
Pr[lambda_max(sum_e X_e) >= t]
    <= d exp(-t^2 / (2 sigma^2 + 2 R t/3)).
```

For `X_e=(Gamma_e-q)T_e`, `R <= (1-q) max_e ||T_e||` and the exact variance above supplies `sigma^2`. This is the conventional variance comparator, but the `d` prefactor and operator-norm event do not directly establish the state-dependent adaptive-posterior bound. Primary author PDF: [Tropp preprint](https://tropp.caltech.edu/papers/Tro11-User-Friendly-preprint.pdf), Theorem 6.1 (bounded case), pp. 23–24 of the PDF.

## Positive-functional Cauchy–Schwarz and DPI scope

The Cauchy–Schwarz inequality for any positive linear functional `psi` on a C*-algebra is
`|psi(b* a)|^2 <= psi(a* a) psi(b* b)`. It follows by expanding `psi((a z+b)^*(a z+b)) >= 0` for complex scalars `z`; normality is not needed. For a state and `b=1`, it gives `|psi(a)|^2 <= psi(a* a)`. Thus the variance-to-posterior step above is valid for normal states on any von Neumann algebra, including nonfaithful states; it uses bounded `A_gamma` and the assumed positive-functional order `p omega_gamma <= phi`.

For the data-processing boundary, Hiai, “Quantum f-divergences in von Neumann algebras I. Standard f-divergences,” Theorem 4.1(iv), proves `S_f(rho composed with Phi || sigma composed with Phi) <= S_f(rho||sigma)` for normal positive functionals on a general von Neumann algebra and a normal unital positive Schwarz map `Phi`. With `f(t)=t log t`, this is Araki relative-entropy DPI (Hiai Example 3.6 identifies `S_{t log t}` with relative entropy). This confirms the normal-positive-functional and nonfaithful setting; it is an entropy contraction statement, not a concentration theorem. It is also distinct from the elementary order-preservation fact: if `p omega <= phi` and `Phi` is positive, then `p(omega composed with Phi) <= phi composed with Phi`.

Primary source: Fumio Hiai, [arXiv:1805.02050](https://arxiv.org/abs/1805.02050), Theorem 4.1(iv), with the relative-entropy identification at Example 3.6.
