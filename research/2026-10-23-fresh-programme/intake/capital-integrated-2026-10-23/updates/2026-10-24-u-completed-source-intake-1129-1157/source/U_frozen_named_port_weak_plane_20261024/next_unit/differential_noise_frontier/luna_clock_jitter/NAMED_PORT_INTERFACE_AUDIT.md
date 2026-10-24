# Named-port control audit

24 October 2026. Bounded algebraic interface check of NAMED_PORT_WEAK_PLANE_OPERATION.txt; no source search or physical claim.

## Dated failed inference: the first port wording omitted \(a\)-\(b\)

The initial draft's narrower tree-port list allowed \(c\)-\(a\), \(c\)-\(b\), and \(b\)-\(e\), but omitted \(a\)-\(b\). Under that wording the displayed \(H_{\rm named}=H_{\rm bar}+N\) was not supported on the allowed graph: the broad moving-frame term contains a nonzero \(a\)-\(b\) coupling at leading order, while \(N\) has no \(a\)-\(b\) entry and the projected normal correction cannot cancel it at this order. The lead has since clarified the intended contract: the complete \(a,b,c\) graph is allowed, including \(a\)-\(b\), in addition to \(b\)-\(e\). Under that corrected contract this matrix element is allowed, so this calculation no longer blocks the named-port operation.

Check a logical-\(X=+1\) sector and use physical basis order \((c,b,a,e)\). Write the two columns of \(F\) as rows:

\[
C=(1,B,A,E)/n,\qquad
D=(-z,-(1+z)B,(1-z)A,-zE)/(n\sigma).
\]

At any fixed interior \(s\) with \(f(s)>0\), \(B=\beta f\), \(A=a_0f^2\), \(E=e_0f^2\), and as \(h\to0\),

\[
n=1+O(h^8),\quad \sigma=B(1+O(h^8)),\quad
D_b=-1+O(h^8),\quad D_a=\theta+O(h^{12}),\quad
\theta=A/B=(a_0/\beta)f=h^4f.
\]

For the stated
\[
H_0=iF'F^\dagger-iFF'^\dagger-iF(F^\dagger F')F^\dagger,
\]
the \(ba\) entry is
\[
(H_0)_{ba}=i\theta'(s)+O(h^{12})
=i h^4 f'(s)+O(h^{12}).
\]
This follows directly from the first two terms: \(F'_b\cdot F_a-F_b\cdot F'_a=\theta'+O(h^{12})\); the connection term \(F(F^\dagger F')F^\dagger\) is \(O(h^{12})\) in this entry. Since \(f\) is a nonconstant bump, \(f'\ne0\) on some interior points.

The normal correction \(ijQ[(|a\rangle\langle e|-|e\rangle\langle a|)\otimes X]Q\) does not remove this leading term. Its coefficient is set by the \(ae\) entry of \(H_0\), which is \(O(h^{17})\) for these scalings, and its \(ba\) projection is further suppressed by the small frame overlaps. The prescribed \(N\) has support only on \(ce,be,cb\), so \(N_{ba}=0\) exactly. Hence \(H_{\rm named,ba}=i h^4 f'(s)+O(h^{12})\) in the \(s\)-generator.

The physical pulse Hamiltonian divides this by \(\delta=d_0h^2\), leaving
\[
(H_{\rm named}^{\rm phys})_{ba}
= i\,h^2 f'(s)/d_0+O(h^{10}),
\]
a nonzero \(a\leftrightarrow b\) sample port. It fits fixed positive amplitude/slew budgets (its amplitude is \(O(h^2)\), its time derivative \(O(1)\)). It is excluded only by the initial tree-port wording; it belongs to the clarified complete \(a,b,c\) control graph. No synthesis workaround or redesign is needed for the corrected contract.

## Other requested interface checks

- \(N\)'s displayed terms are \(ce,be,cb\); its \(ce\) coefficient cancels the \(ce\) entry of \(H_{\rm bar}/\delta\) in the total matrix, and \(N_{ae}=N_{ad}=0\). Implementing the sum's final entries avoids physically applying a forbidden \(ce\) component as a separate action. The remaining \(be\) and \(cb\) entries are on the stated port list.
- The quotient \(v=-r_{ce}/(B\delta)\) is not an evident normalization oracle: under the asserted factorization \(r_{ce}=e_0ff'\times\) a known smooth bounded function, it reduces to a known smooth multiple of \(e_0 f'/(\beta\delta)\). It uses known protocol functions and parameters only, not a state-dependent normalization or measurement.
- With flat bump endpoints and that removable quotient, the added pulse coefficients can turn on/off smoothly. The actual finite-rate \(c\)-\(b\) meter reset remains the prior allowed reset; no instantaneous projection is introduced by this named-port note. Its duration, ramps, damping and cleanup error still need the prior paid accounting.

The lead's correction preserves the failed narrower-scope check and repairs the interface statement by allowing \(a\)-\(b\). The remaining checks above are conditional algebraic/resource observations, not a re-audit of the population or logical-multiplier estimates.
