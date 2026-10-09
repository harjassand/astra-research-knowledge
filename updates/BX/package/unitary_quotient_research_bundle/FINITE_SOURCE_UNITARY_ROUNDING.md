# Finite-source unitary-to-permutation rounding

9 October 2026. Complete proof candidate; the algebra, dimension bookkeeping, and primary theorem interfaces passed a focused check. Historical priority remains unestablished.

## Statement

Let G be a finite group, S a generating list with probability weights mu, and rho:G->U(d) an exact representation. Let P_s be prescribed permutation matrices. Define

 delta^2=E_s ||rho(s)-P_s||_F^2/d.

On Hom(C^d,C^d tensor C^d) put R(g)A=(rho(g) tensor rho(g))A rho(g)^*. Let Pi project onto the invariant subspace. Assume the energy gap

 E_s ||R(s)A-A||_F^2 >=kappa ||A-Pi A||_F^2

for all A, where kappa>0. Then an exact permutation action h:G->Sym(N) exists with

 d<=N<=(1+197316 delta^2/kappa)d,
 E_s d_h(P_s,h(s)) <=(1+330354/kappa)delta^2.

For N>=d, the charged metric is d_h(P,Q)=1-(number of agreeing original labels)/N. Thus all added labels are counted.

## Proof

Let Delta e_i=e_i tensor e_i. By the three-factor estimate in UNITARY_PERMUTATION_QUOTIENT_EMBEDDING.md,

 E_s ||R(s)Delta-Delta||_F^2 <=9d delta^2.

Set eta^2=||Delta-Pi Delta||_F^2/d. The gap gives eta^2<=9delta^2/kappa. Exact invariance and unitarity give, for every g in G,

 ||R(g)Delta-Delta||_F <=2eta sqrt(d).

The quotient embedding's Birkhoff inequality now gives a nearest permutation f(g) satisfying

 ||rho(g)-f(g)||_F/sqrt(d)<=2eta.

The function f is defined on the finite group G; there is no measurable-selection or compact-group issue. For every g,h,

 ||f(g)f(h)-f(gh)||_F/sqrt(d)<=6eta.

Since normalized squared Frobenius distance between permutations equals twice Hamming distance, the uniform multiplication defect of f is at most D=18eta^2.

Becker–Chapman, Theorem 1.2, applies directly to this finite source. It gives h:G->Sym(N) with

 d<=N<=(1+1218D)d,
 sup_g d_h(f(g),h(g))<=2039D.

For each generator, the triangle inequality in Frobenius norm gives

 d_H(P_s,f(s)) <= (||P_s-rho(s)||_F/sqrt(d)+2eta)^2/2.

Thus E_s d_H(P_s,f(s))<=delta^2+4eta^2. The charged Hamming metric satisfies the triangle inequality across degrees, so

 E_s d_h(P_s,h(s)) <=delta^2+(4+2039*18)eta^2
 <=(1+330354/kappa)delta^2.

The size bound is N/d-1<=1218*18eta^2<=197316delta^2/kappa. This proves the statement.

## Scope

The input rho is an exact representation. Merely having approximate permutation generators does not supply rho: they already preserve Delta exactly even when their relations fail. In FINITE_GROUP_CODE_TRANSFER.md this input is supplied by a separate, established unitary stability theorem, and its dimension changes are charged explicitly.

No efficient algorithm is claimed by this existence proof. Enumerating the finite group may be much more expensive than reading its presentation. The immediate consequence is quantitative soundness/repair existence, not a polynomial-time decoder.

## Source dependency

Becker–Chapman, *Stability of approximate group actions: uniform and probabilistic*, arXiv:2005.06652v1, Theorem 1.2, https://arxiv.org/pdf/2005.06652v1 . The finite-source case is sufficient here. Compact-Haar extensions are not used in this document or its code-presentation application.
