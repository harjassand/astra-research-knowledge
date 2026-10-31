# A contractive recovery frame and the remaining positive boundary problem

Principal derivation, 16 October 2026. This is an exact finite-volume reduction conditional on the pinned deterministic component-filling lemma. It is **not** a coherent-memory lifetime theorem or a novelty claim. It changes the representation of the missing estimate: a positive boundary concentration bound can replace a signed union over formal escaping histories.

## Domain and frame

Use the 4D toric code and completed pair generator specified in the pinned `PRINCIPAL_PAIR_THEOREM.md`. Write its Lindblad generator, with a bounded local Hamiltonian, as

\[
\mathcal L(X)=-i[H,X]+\sum_\alpha\left(J_\alpha XJ_\alpha^\dagger-\tfrac12\{J_\alpha^\dagger J_\alpha,X\}\right).
\]

Fix the syndrome domain \(G\) in which every primal and dual syndrome component has ambient torus diameter less than \(r=L/32\). Let \(P\) be its Hilbert-space projector and \(Q=I-P\). For every valid syndrome \(s\), choose the fixed Pauli filling \(F_s\) used by the inherited decoder. The unitary syndrome frame on the good domain is

\[
U:|\ell\rangle\otimes|s\rangle\longmapsto F_s V|\ell\rangle,
\qquad s\in G,
\]

where \(V\) encodes all six logical qubits. Every syndrome sector has dimension 64. Both sectors and all relative Pauli phases must be retained.

The deterministic local homology lemma has the following precise consequence. For every bounded-support Pauli \(E\), if its source and target syndromes belong to \(G\), then

\[
V^\dagger F_{s(E)+s}^\dagger E F_s V=a_{E,s}I_{64}.
\]

Indeed, the changed components, their old and new fillings, and the event chain lie in a contractible box of side \(2r+O(q)<L/8\). Their closed residual is a stabilizer. The phase \(a_{E,s}\) may depend on the syndrome and Pauli, but not on the logical state. Thus

\[
U^\dagger P E P U=I_{64}\otimes e_G.
\tag{1}
\]

For an arbitrary supplied bounded local Hamiltonian, expand each local term in Paulis. Equation (1) gives the same factorization for \(PHP\). Each pair jump is a Pauli times a syndrome-diagonal projector, so \(PJ_\alpha P\) factors likewise. Also \(A=\sum J_\alpha^\dagger J_\alpha\) is syndrome diagonal and commutes with \(P\). For the completed pair model, \(A=12\kappa L^4 I\). This reduction does not equate its full evolution with the active pair model.

## Genuine completely positive compression

On operators supported in \(P\), define

\[
\mathcal K(X)=P\mathcal L(X)P.
\]

Set \(j_\alpha=PJ_\alpha P\), \(H_G=PHP\), and \(A_G=PAP\). Then

\[
\mathcal K(X)=-i[H_G,X]+\sum_\alpha j_\alpha Xj_\alpha^\dagger-\tfrac12\{A_G,X\},
\]

and

\[
D_G=A_G-\sum j_\alpha^\dagger j_\alpha
=\sum PJ_\alpha^\dagger QJ_\alpha P\succeq0.
\]

Consequently \(e^{t\mathcal K}\) is completely positive and trace nonincreasing: it is a Lindblad semigroup with a positive killing term \(-\{D_G,\cdot\}/2\), or equivalently the retained block of a trace-preserving evolution with an absorbing flag. In the frame it has the exact form \(\operatorname{id}_{64}\otimes e^{t k_G}\). Starting in the code,

\[
\tau_\rho(t)=e^{t\mathcal K}(V\rho V^\dagger)
=U(\rho\otimes\sigma_t)U^\dagger,
\qquad \sigma_t\succeq0,\quad p(t)=\operatorname{Tr}\sigma_t\le1.
\tag{2}
\]

This holds with an arbitrary untouched reference. Recovery of \(\tau_\rho(t)\) is exactly \(p(t)\rho\). This compressed process is an analytical comparison, not an implemented local monitor. Its projector is global and its Hamiltonian \(PHP\) need not be geometrically local.

## Boundary flux inequality

Define

\[
\lambda(t)=\operatorname{Tr}(D_G\tau_\rho(t))=-p'(t),
\quad R=\|A\|,
\]

where \(\lambda\) is independent of \(\rho\) by the frame factorization. Define the reference-uniform Hamiltonian susceptibility

\[
\chi_*(t)=\sup_{\rho}\operatorname{Tr}\!\left[\tau_\rho(t)PHQHP\right]
=\left\|\operatorname{Tr}_{G}\!\left[(I\otimes\sqrt{\sigma_t})U^\dagger PHQHPU(I\otimes\sqrt{\sigma_t})\right]\right\|_\infty.
\]

The supremum can be taken over logical states alone because the traced expression acts trivially on the untouched reference. No input independence of \(PHQHP\) is presumed.

For every density operator, including a reference extension, Hilbert-Schmidt Cauchy-Schwarz gives

\[
\|QHP\tau_\rho\|_1\le\sqrt{p\,\chi_*}\le\sqrt{\chi_*}.
\]

The jump residual consists of its \(Q,Q\) block and two off-diagonal blocks. Summing Cauchy-Schwarz over jumps gives

\[
\|(\mathcal L-\mathcal K)\tau_\rho\|_1
\le2\sqrt{\chi_*}+\lambda+2\sqrt{R\lambda}.
\tag{3}
\]

Here the anticommutator creates no cross block because \([A,P]=0\). The \(Q,Q\) jump block is positive with trace \(\lambda\), and its retained partner has total trace at most \(Rp\le R\). Equation (3) retains jump coherences; treating jump exit as an ordinary classical stopping probability would miss the square-root cross term.

Duhamel's identity and contractivity of the full CPTP evolution and decoder now imply

\[
\begin{aligned}
\|\mathrm{Dec}\,e^{T\mathcal L}\mathrm{Enc}-\mathrm{id}\|_\diamond
&\le\min\left\{2,\int_0^T
\left[2\sqrt{\chi_*(t)}+2\sqrt{R\lambda(t)}+2\lambda(t)\right]dt\right\}.
\end{aligned}
\tag{4}
\]

One \(\lambda\) comes from (3); the other from \(1-p(T)=\int\lambda\). All bounds hold uniformly for positive reference-entangled logical inputs. The difference of the two final channels is Hermiticity preserving, so this reference-uniform state bound yields its diamond norm. Equivalently, first extend the compressed map by a fixed replacement state on its lost trace to obtain a CPTP map; the extra cost is exactly \(1-p(T)\).

## A sufficient positive concentration estimate

Let \(P_\partial\le P\) be the syndrome-diagonal projector onto good source syndromes for which at least one local Hamiltonian Pauli or correction jump can leave \(G\). It includes all exits, not just the observed ones. In formulas on the syndrome factor alone, use the same symbol for its syndrome projector, so that \(U^\dagger P_\partial U=I_{64}\otimes P_\partial\). Put

\[
q_\partial(t)=\operatorname{Tr}[P_\partial\tau_\rho(t)]
=\operatorname{Tr}[P_\partial\sigma_t].
\]

Then \(D_G\preceq R P_\partial\), and \(QHP=QHP P_\partial\), so

\[
\lambda(t)\le Rq_\partial(t),\qquad
\chi_*(t)\le\|H\|^2q_\partial(t).
\tag{5}
\]

For a bounded-degree local Hamiltonian, \(\|H\|\le c_H hL^4\), a deliberately loose extensive bound. If a new theorem establishes uniformly in \(t,L\)

\[
q_\partial(t)\le C_0 L^a e^{-c_0L}
\tag{6}
\]

at fixed small local \(h/\kappa\), equations (4)-(5) imply the desired \(C L^4(1+\kappa T)e^{-cL}\), with a smaller \(c>0\), by absorbing the fixed polynomial into the exponential. Integrable or horizon-averaged variants of (6) also suffice. This is a **conditional implication**, not evidence that (6) holds.

## Why the frontier is still open

An integrated certificate is enough; pointwise mixing is stronger than necessary. Rescale time by \(u=\kappa t\), and write \(\widehat k_G=k_G/\kappa\). If one constructs a positive syndrome operator \(F_L\) with

\[
\widehat k_G^*(F_L)\preceq-P_\partial+\varepsilon_L I,
\qquad \langle0|F_L|0\rangle\le\varepsilon_L,
\qquad \varepsilon_L\le\operatorname{poly}(L)e^{-aL},
\tag{7}
\]

positivity and trace nonincrease imply

\[
\int_0^u q_\partial(v)\,dv\le\varepsilon_L(1+u).
\]

Cauchy-Schwarz applied to (4)-(5) then gives

\[
\|\mathrm{Dec}\,e^{T\mathcal L}\mathrm{Enc}-\mathrm{id}\|_\diamond
\le\min\left\{2,(1+\kappa T)
\left[\frac{2(\|H\|+R)}{\kappa}\sqrt{\varepsilon_L}
+\frac{2R}{\kappa}\varepsilon_L\right]\right\}.
\tag{8}
\]

This closes the target if (7) is proved uniformly at a fixed positive local Hamiltonian strength. The existence and size bound for \(F_L\), rather than the elementary dual integration, are the unsolved operation.

The boundary is genuinely macroscopic: a local event changes edges only in a bounded patch \(W\) of diameter \(D\). If that event takes a safe syndrome to a component of diameter at least \(r\), some pre-event component has diameter at least \((r-D-2)/2\). Every old component in the new merged component touches the event patch; distances between two extrema are bounded by their old component diameters plus \(D+2\). Thus \(P_\partial\) is bounded by the projector for an existing component of diameter at least \(L/64-O(q)\). A positive **quantum Peierls occupation estimate**, not necessarily convergence to a unique state, would suffice. This geometry does not bound its occupation probability.

The inherited positive classical eroder theorem controls Pauli trajectories, not \(\sigma_t\) under the compressed quantum Hamiltonian. The global projection can remove interference paths and changes locality. Classical stochastic domination, the fixed-contour amplitude estimate, the number of insertions needed to reach a dark strip, and finite-size Zeno elimination do not prove (6).

A native two-strip calculation shows that the most direct diagonal classical lift fails. In the dimensionless generator, take consecutive good open strips \(s_-,s_+\), with \(s_+\) pivotal for one additional face, and a two-face Hamiltonian that couples \(s_-\) to \(s_+\). The pair-only occupation potential for the pivotal set has values \(f(s_-)=0,f(s_+)=1\) and classical drift \((0,-1)\). The principal submatrix of \(\widehat k_G^*(\operatorname{diag}f)+P_\partial-\varepsilon I\) is

\[
\begin{pmatrix}-\varepsilon&i h/\kappa\\-i h/\kappa&-\varepsilon\end{pmatrix}.
\]

Negative semidefiniteness forces \(\varepsilon\ge |h|/\kappa\), rather than an exponential in \(L\). This rules out that **unmodified classical diagonal potential**, not every diagonal halo or a coherently dressed operator. The exact geometry, a pointwise certificate variant, and a positive two-dimensional dressed effect are in `workers/positive_committor/POSITIVE_COMMITTOR_GATE.md`. The dressed local block has source of order \(h^2/\kappa\); no interacting global halo or exponentially small code expectation has been constructed.

The compression is also not the actual physical quantum first-exit process for a Hamiltonian: repeated exact projections freeze coherent escape in the Zeno limit. The explicit susceptibility in (4) charges that discrepancy rather than declaring it zero. A two-level system with \(P=|0\rangle\langle0|\), \(H=hX\), no jumps has \(p(t)=1\), \(\lambda=0\), but \(\chi_*=h^2\); the bound is \(2|h|T\), consistent with coherent escape. Any argument using only the killed trace would fail this example.

The closest reviewed coherent global resummation predecessor is [Han et al., arXiv:2609.20537v1, Appendices B and C](https://arxiv.org/html/2609.20537v1). Its fixed-depth circuit proof already handles joint large-component interpolation and saturation at diamond distance two. The CP compression itself is standard open-system Zeno dynamics: [Becker, Datta and Salzmann, *Quantum Zeno Effect in Open Quantum Systems*, Introduction, Eqs. (1.4)-(1.6)](https://doi.org/10.1007/s00023-021-01075-8), explicitly proves the trace-nonincreasing compressed generator. This campaign uses it as an analytical comparison rather than claiming a new compression operation. Duhamel and Cauchy-Schwarz are standard as well. What would change the attainable frontier is a uniform **positive quantum boundary-concentration theorem** for this recovery frame, or an architecture that supplies one. Neither is established here. External scrutiny must check (1) for every admitted local support, both CSS sectors, and the exact rate/reference quantifiers before using this reduction.
