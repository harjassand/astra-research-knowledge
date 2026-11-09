# P2 Xi completed return — e95e016a

Source: https://chatgpt.com/c/6af14bcf-8cd8-83ec-8be1-647bf05ff7d2
Model: GPT-6 standard, Extra High. Exact original prompt: P2_FULL_GAP_CLASSIFICATION_AFTER_COMPRESSED_CLASS_ACCESS_XI_20261109.txt. Follow-up: `please continue.`

No producer ZIP visible.

## Visible work

Assessed spectral-gap criteria

I’ll continue from the accepted DDB1 class decomposition and exact factorial edge form. I’ll focus on whether these allow a terminating positive/zero gap test, and separate any proved extension from a still-incomplete classification.

Assessed spectral computability

Refined gap estimates and strengthened computability limits

Formulated rigorous criteria and clarified computable bounds

Established computable bounds

Searched 9 websites

## Complete response

# P2 — Physical-time Poincaré-gap classification

(Full classification unresolved)

The accepted DDB1 machinery makes the actual infinite communicating class effectively accessible, but I have not established a terminating algorithm deciding \(\lambda>0\) versus \(\lambda=0\) for every rational complex-balanced network.

There is, however, a rigorous separation between equilibrium information and kinetic information, together with an exact finite-support witness mechanism.

## 1\. A decisive obstruction: identical equilibrium laws, opposite gaps

Consider two reaction systems on species \(X,Y\), with all rate constants equal to one.

**System A**

\[
\varnothing\rightleftarrows X,\qquad
\varnothing\rightleftarrows Y.
\]

**System B**

\[
\varnothing\rightleftarrows X+Y,\qquad
Y\rightleftarrows 2Y.
\]

Both systems are detailed balanced at \(c=(1,1)\), have the actual class \(\Gamma=\mathbb Z_{\ge0}^{2}\), and have exactly the same stationary law\:

\[
\pi(x,y)=\frac{e^{-2}}{x!\,y!}.
\]

Yet their physical-time gaps differ\:

| System | Poincaré gap |
|--------|--------|
| A — independent immigration/death | \(\lambda=1\) |
| B — coupled creation with a boundary bottleneck | \(\lambda=0\) |

For System A, Poisson tensorisation gives the exact gap \(1\)\.

For System B, define the two-point set

\[
A_n=\{(n,0),(n+1,1)\}
\]

and the rational finite-support function \(f_n=\mathbf1_{A_n}\)\.

A direct boundary-flux computation gives

\[
\frac{\mathcal E(f_n,f_n)}
{\operatorname{Var}_{\pi}(f_n)}
=
\frac{2}{(n+2)(1-\pi(A_n))}.
\]

For \(n\ge1\), \(\pi(A_n)<1/2\), so

\[
\boxed{
\frac{\mathcal E(f_n,f_n)}
{\operatorname{Var}_{\pi}(f_n)}
\le\frac4{n+2}.
}
\]

Choosing \(n=4j\) gives a certified rational finite-support witness with Rayleigh quotient strictly below \(1/j\), for every \(j\ge1\)\.

This is an explicit quantitative version of the zero-gap obstruction in Anderson–Cappelletti–Fan–Kim, Example 2.4. citeturn394802view0

**Consequence\:** DDB1's exact class description, conditional-Poisson sampler, and normalisation algorithm cannot by themselves classify the physical-time gap. The two systems have identical equilibrium information. Any full classifier must examine how the reaction edges connect rare states.

## 2\. An exact uniform finite-witness procedure

There is a general computability result that follows from DDB1 and the accepted finite-support form-core theorem.

**Proposition.** For every valid input with a nonsingleton actual class, there exists a deterministic algorithm producing a decreasing sequence of positive rational numbers

\[
U_1\ge U_2\ge\cdots>0,
\qquad
\boxed{\lim_{s\to\infty}U_s=\lambda.}
\]

The numbers are computed from finite rational arithmetic and actual-class membership tests. No stationary normaliser, spectral oracle, or numerical tail approximation is required to certify each upper bound.

### Construction

Write \(w(x)=c^x/x!\)\. For an arbitrary rational finite-support function \(f\), calculate

\[
A_f=\sum_{x\in\Gamma}w(x)f(x)^2,\qquad
B_f=\sum_{x\in\Gamma}w(x)f(x)
\]

and the unnormalised energy

\[
D_f=\frac12\sum_{x\in\Gamma,r}
w(x)q_r(x)\bigl(f(x+\Delta_r)-f(x)\bigr)^2.
\]

All three are rational and involve finitely many nonzero terms.

For a finite set \(K\subseteq\Gamma\), calculate

\[
Z_K=\sum_{x\in K}w(x)\le Z_\Gamma.
\]

Whenever \(A_f-B_f^2/Z_K>0\), define

\[
\boxed{
U(f,K)=\frac{D_f}{A_f-B_f^2/Z_K}.
}
\]

Because

\[
\operatorname{Var}_\pi(f)
=\frac1{Z_\Gamma}\left(A_f-\frac{B_f^2}{Z_\Gamma}\right),
\]

we have

\[
\lambda\le
\frac{D_f}{A_f-B_f^2/Z_\Gamma}
\le U(f,K).
\]

The direction of this inequality is important: replacing the true normaliser by a rational lower bound gives a **certified upper bound**, not a lower bound.

Enumerate rational finite-support functions and finite sets \(K\), using DDB1 to decide membership. At stage \(s\), retain the smallest certified bound so far.

The accepted finite-support form core implies that these bounds converge downward to the full-domain gap.

### What this decides

For every valid nonsingleton input,

\[
\boxed{
\lambda=0
\iff
\forall j\ge1\ \exists s\ge1:
U_s<\frac1j.
}
\]

Consequently\:

- The zero-gap property has a uniform \(\Pi^0_2\) description.
- The positive-gap property has a uniform \(\Sigma^0_2\) description.
- On every zero-gap instance, a search for a finite rational witness below \(1/j\) terminates for each \(j\)\.

The latter gives a single finite witness-generating program once the zero-gap case is known.

It is **not** a total classifier: the search for a witness can run indefinitely when \(\lambda>0\)\. The \(\Pi^0_2\) upper bound is not an undecidability result, and does not establish hardness at that level.

## 3\. A further exact kinetic invariance

There is an additional structural simplification.

Fix the reaction list \(R\), actual class \(\Gamma\), and rational activity vector \(c\)\. Suppose two positive rational rate vectors \(\kappa\) and \(\widetilde\kappa\) are both complex balanced at this same \(c\)\.

Set

\[
a=\min_r\frac{\widetilde\kappa_r}{\kappa_r},
\qquad
b=\max_r\frac{\widetilde\kappa_r}{\kappa_r}.
\]

For every function in the full form domain,

\[
a\,\mathcal E_\kappa(f,f)
\le \mathcal E_{\widetilde\kappa}(f,f)
\le b\,\mathcal E_\kappa(f,f).
\]

The stationary variance is identical for both models. Hence

\[
\boxed{
a\lambda_\kappa
\le\lambda_{\widetilde\kappa}
\le b\lambda_\kappa.
}
\]

The two quadratic-form domains also coincide, since their energies are comparable.

Therefore,

\[
\boxed{
\lambda_\kappa>0
\iff
\lambda_{\widetilde\kappa}>0.
}
\]

This is an exact rational comparison theorem, with no truncation and no restriction on the molecularities, rank, or size of the actual class.

It means that, **within a fixed reaction structure and fixed equilibrium activity**, the positive-versus-zero classification is invariant under all admissible positive rate changes.

It does not permit arbitrary changes in the equilibrium vector or reaction structure, as the two-system counterexample demonstrates.

## 4\. A rank-\(\ge2\) extension by independent composition

The accepted rank-one positive-gap compiler also extends to a restricted class of higher-rank systems.

Suppose a network is the disjoint union of \(m\) independent complex-balanced subnetworks, with disjoint species sets and no cross-component reactions.

Then

\[
\Gamma=\Gamma_1\times\cdots\times\Gamma_m,
\qquad
\pi=\pi_1\otimes\cdots\otimes\pi_m,
\]

and the Dirichlet form is a sum of component forms.

By variance tensorisation and functions depending on a single component,

\[
\boxed{\lambda=\min_{1\le i\le m}\lambda_i.}
\]

Therefore, if every component has stoichiometric rank at most one, ROOT's accepted positive-gap compiler provides a rational lower bound

\[
\ell=\min_i\ell_i>0
\]

for the full system, even when the combined stoichiometric rank is arbitrarily large.

This is a valid higher-rank positive family, but it does not cover genuinely coupled higher-rank systems.

## 5\. Exact algorithmic status

| Requirement | Status |
|--------|--------|
| Exact actual-class membership and representation | Accepted DDB1 |
| Rational finite-support energies | Established |
| Uniform decreasing rational upper approximations to \(\lambda\) | Established above |
| Finite-support zero witnesses on all zero-gap instances | Conditional terminating search |
| Rational lower bounds for independent rank-one products | Established from ROOT |
| Zero/positive invariance under fixed-\(R,c\) rate changes | Established |
| Complete positive-gap certificate for arbitrary rank | Not established |
| Terminating zero/positive decision for every input | Not established |
| Computable uniform complete-bit decision bound | Not established |
| Undecidability in the specified complex-balanced class | Not established |

The finite-stage algorithms have computable complete-bit running-time bounds: DDB1 supplies terminating membership, and every subsequent operation is finite integer or rational arithmetic. For example, stage \(s\) can restrict supports to \(\Gamma\cap[0,s]^d\) and rational coefficient numerators and denominators of magnitude at most \(s\)\. This gives a finite, explicitly enumerable search, with bit costs bounded through the DDB1 membership implementation and the finite arithmetic sizes.

However, **there is no established computable bound on the stage \(s\) needed to certify the answer for an arbitrary input**\. That is the missing resource guarantee. In particular, the conditional zero-witness search does not supply the requested uniform construction-time bound as a function of input and \(j\)\.

## 6\. What remains to resolve the full theorem

The crucial unresolved question can now be stated more precisely\:

Does every zero-gap rational complex-balanced mass-action network possess a bottleneck or low-energy witness within some *computably bounded finite family of asymptotic constructions*, while every positive-gap network admits a corresponding effective full-domain coercivity certificate?

DDB1 makes the geometry of the state space finite-describable. But the unbounded reaction-rate polynomials and factorially weighted edge capacities still produce infinitely many possible scales of kinetic behaviour.

A complete result needs either a finite reduction controlling all these scales, with a proof of completeness and computable size bounds, or a reduction proving that no terminating decision procedure exists.

The current primary comparison, Anderson–Cappelletti–Fan–Kim, proves useful sufficient positive-gap conditions and provides the explicit zero-gap counterexample. It does not supply this general decision theorem. citeturn600926view0turn248618search0

**Final result of this continuation\:** A uniform upper-semicomputability theorem, exact finite-support rational witness synthesis on zero-gap instances, fixed-equilibrium kinetic invariance, and an independent-product higher-rank extension are available. The requested unrestricted total classification remains open on the arguments established here; neither a full positive algorithm nor undecidability has been proved.
