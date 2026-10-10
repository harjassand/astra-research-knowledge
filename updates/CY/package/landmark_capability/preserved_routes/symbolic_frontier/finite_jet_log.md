# Finite-jet logarithm for very long algebraic recurrences

Status: **correct scoped capability; novelty rejected**. The mechanism below is useful for skipping an astronomical number of steps when a recurrence is tangent to the identity on a finite local algebra. Its mathematical core is the classical logarithm of a unipotent substitution operator. The primary-source screen found direct overlap, so this is not a new result or a breakthrough claim.

## Problem class and data

Let K be a characteristic-zero field and let A be a finite-dimensional commutative local K-algebra with maximal ideal m and m^k = 0. Think of A = K[x_1,...,x_d]/(I + m^k) as the exact k-jet algebra at a fixed point; I may encode algebraic constraints, including a singular variety.

Let phi : A -> A be a K-algebra endomorphism such that, for some integer r >= 1,

    (phi - id)(m^j) is contained in m^(j+r)       for every j >= 1.

In particular, phi fixes constants and is the pullback of a recurrence map whose coordinate changes start in degree r+1. The condition makes U = phi - id nilpotent. Since phi = id + U is invertible as a linear map, it is an algebra automorphism.

The query is phi^n(g) = g composed with F^n for a chosen observable g in A and an integer n >= 0 supplied in binary. The result is returned as an element of A, so the output contains at most M = dim_K(A) basis coefficients.

## Theorem

Set L = ceil((k-1)/r), with the trivial case k <= 1 handled by phi = id. Then U^L = 0. For every integer n >= 0,

    phi^n(g) = sum_(j=0)^(L-1) binom(n,j) U^j(g).

Thus each observable has a polynomial orbit in n. More precisely, if g - g(0) has m-adic order s >= 1, terms stop at J = floor((k - s - 1)/r), so the degree is at most J; constants are fixed.

The same substitution operator has a finite logarithm

    D = log(phi) = sum_(j=1)^(L-1) (-1)^(j+1) U^j / j.

D is a derivation of A, phi = exp(D), and the orbit can equivalently be written as exp(nD)(g). The binomial form is the cheaper one for integer-index queries.

## Proof

The filtration condition gives U(m^j) subset m^(j+r), hence U^L(m) subset m^(1+Lr) = 0. Also U(1)=0, so U^L=0 on all of A.

For a scalar indeterminate t, form the polynomial operator

    phi^t = (id + U)^t = sum_(j=0)^(L-1) binom(t,j) U^j.

At every nonnegative integer t=n, this is the ordinary algebra automorphism phi^n. For fixed a,b in A, the difference phi^t(ab) - phi^t(a) phi^t(b) is a polynomial in t that vanishes at every nonnegative integer, so it is identically zero. Differentiate at t=0. Since the derivative of binom(t,j) there is (-1)^(j-1)/j for j >= 1, the derivative is D, and the differentiated multiplicativity identity is
D(ab) = D(a)b + aD(b). The finite nilpotent identities for log and exp give exp(D)=phi, then phi^n=exp(nD). The filtration bound on D gives the stated degree bound for each g.

## Algorithm and cost

Assume an explicit basis of A with dimension M, the multiplication table, and the M x M matrix of phi are supplied. A verifier can check the algebra-map identities and the filtration condition from those finite tables.

1. Form U = phi - I.
2. Starting at v_0=g, compute v_(j+1)=U v_j and accumulate binom(n,j) v_j until the filtration bound makes all later terms zero.

With a dense matrix for U, evaluating one observable takes O(J M^2) field operations, plus O(J) scalar operations for the binomial coefficients. These counts do not grow with the numerical value of n; in rational bit complexity, they do grow with the bit length of n and coefficient heights. If b=bitlength(n), and H bounds a common denominator and the scaled numerators for U and g, a crude bound for each output coefficient is O(J(H+b+log(M J))) bits. The output-size cost is unavoidable when the requested exact coefficients have that many bits. If the full polynomial orbit in n is requested, return the vectors U^j(g) in the binomial basis; this output can contain J M coefficients.

For the full k-jet in d variables before quotienting by I, M = binom(d+k-1,d). This can itself be large; the method avoids the n intermediate orbit steps, not the cost of the requested jet. To start from an implicit branch P(x,y)=0, a nonsingular Jacobian in y is needed to compile its unique local branch into the jet algebra. That branch-construction cost is additional and is not covered by the iteration bound.

## Small exact example

For F(x)=x+x^2 in Q[x]/(x^6), direct symbolic composition at each step is unnecessary. The theorem implies

    F^n(x) = x
           + n*x^2
           + n*(n-1)*x^3
           + n*(n-1)*(2*n-3)/2*x^4
           + n*(n-1)*(n-2)*(3*n-4)/3*x^5  (mod x^6).

This is an exact identity for every integer n >= 0; the degree-five jet depends on n through a polynomial of degree four. For an index with a thousand-bit binary representation, the same five coefficients are obtained with four applications of U and arithmetic on roughly four-thousand-bit integers, instead of constructing n intermediate series.

## Prior-art screen and novelty decision

The key step is already classical. Aschenbrenner's paper uses logarithms of iteration matrices and the iterative logarithm of formal power series: [arXiv:1009.5518](https://arxiv.org/abs/1009.5518). Chan, Young, and Zhang state and use that the logarithm of a unipotent algebra automorphism is a derivation (Lemma 7.12): [Algebra & Number Theory 10 (2016), publisher PDF](https://msp.org/ant/2016/10-3/ant-v10-n3-p03-p.pdf). Poonen proves analytic interpolation of iterates for a broad class of p-adic maps close to identity, with the iterate index as an analytic variable (Theorem 1): [arXiv:1307.5887](https://arxiv.org/abs/1307.5887).

The finite local-algebra input format and output-sensitive cost statement make the method easy to apply to implicit finite jets, but they are a repackaging of established unipotent-logarithm and formal-iteration results. The original-capability gate therefore fails. No claim of novelty, external validation, or transformative reach is made.
