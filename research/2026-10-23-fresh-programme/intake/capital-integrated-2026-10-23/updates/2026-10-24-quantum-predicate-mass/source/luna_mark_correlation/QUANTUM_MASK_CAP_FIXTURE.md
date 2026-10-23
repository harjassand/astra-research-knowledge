# Finite \(L\)-mask fixture and classical balanced-cap comparison

Let
\[
L=\begin{pmatrix}1&1\\0&1\end{pmatrix},\qquad
|\Phi^+\rangle=(|00\rangle+|11\rangle)/\sqrt2.
\]
For a real angle \(\theta\), set \(|r_\theta\rangle=\cos\theta|0\rangle+\sin\theta|1\rangle\) and \(P_\theta=|r_\theta\rangle\langle r_\theta|\). Use Alice projectors at angles \(\alpha_0=\pi/6,\alpha_1=\pi/2\) and Bob projectors at \(\beta_0=0,\beta_1=\pi/3\). For each pair of settings, the joint rank-one probability is
\[
q_{ab}=\langle\Phi^+|P_{\alpha_a}\otimes P_{\beta_b}|\Phi^+\rangle
=\tfrac12|\langle r_{\alpha_a}|r_{\beta_b}\rangle|^2
=\tfrac12\cos^2(\alpha_a-\beta_b).
\]
The four angle differences give
\[
(q_{ab})_{a,b=0}^1=
\begin{pmatrix}3/8&3/8\\0&3/8\end{pmatrix}
=\frac38 L.
\]
Every individual Alice or Bob projector has marginal \(1/2\), since each reduced state of \(|\Phi^+\rangle\) is \(I/2\). Thus the scale recovering \(L\) from \(q\) is \(\lambda=1/(3/8)=8/3\). Using the cap convention
\[
\kappa=\frac{\max\{\max_a \Pr_A(a),\max_b \Pr_B(b)\}}{t},
\quad\text{where }q=tL,
\]
this fixture has \(t=3/8\) and \(\kappa=(1/2)/(3/8)=4/3\).

## Classical lower bound

Consider any normalized shared-randomness response model
\[
q_{ab}=\mathbb E[e_a f_b],\qquad 0\le e_0,e_1,f_0,f_1\le1,
\]
with \(q_{10}=0\) and \(q_{00}=q_{01}=q_{11}=t\). Nonnegativity implies \(e_1f_0=0\) almost surely. Pointwise on this support,
\[
e_0f_0+e_0f_1+e_1f_1\le e_0+f_1.
\]
Indeed, if \(e_1=0\), the first two terms are bounded by \(e_0\) and \(f_1\); if \(f_0=0\), the last two terms are bounded by \(e_0\) and \(f_1\). Taking expectations yields
\[
3t\le \mathbb E e_0+\mathbb E f_1
\le2\max\{\mathbb E e_0,\mathbb E e_1,\mathbb E f_0,\mathbb E f_1\}.
\]
Therefore every such classical model has cap at least \(3/2\).

Equality is attained by four equiprobable deterministic rectangles. Their row and column supports \((\{a:e_a=1\},\{b:f_b=1\})\) are
\[
(\{0\},\{0,1\}),\quad
(\{0,1\},\{1\}),\quad
(\{0\},\{0\}),\quad
(\{1\},\{1\}).
\]
Each allowed edge of \(L\) occurs in exactly two of the four rectangles, while edge \((1,0)\) occurs in none. Thus \(q_{00}=q_{01}=q_{11}=1/2\), so \(t=1/2\), and the four single-party marginals are
\[
(\mathbb E e_0,\mathbb E e_1;\mathbb E f_0,\mathbb E f_1)
=(3/4,1/2;1/2,3/4).
\]
The classical cap is \((3/4)/(1/2)=3/2\), attaining the lower bound. This gives a strict \(4/3\) versus \(3/2\) coherent/classical cap comparison for this finite fixture. It does not identify an all-quantum optimum or imply a repetition no-go.

