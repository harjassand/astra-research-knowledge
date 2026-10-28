# Exact prior objects and the missing constant

The formalism is established prior. Hirche, George, Nuradha and Wilde,
[*Conditional contraction coefficients and their applications to quantum
networks*, arXiv:2608.27171v1](https://arxiv.org/html/2608.27171v1),
Definition1 equation(2.9), defines the product-reference coefficient
`eta_D^p(P,u9)=sup D((P tensor id)rho||u3 tensor rho_L)/D(rho||u9 tensor rho_L)`
for our SIC preparation channel P and uniform u9. Dephasing the label
leaves P's output and rho_L unchanged and decreases the denominator;
therefore its supremum may be restricted to the actual CQ matrix-weight
sources. The target is EXACTLY `eta_D^p(P,u9)<=1/2`.
Lemma7 equation(3.134) identifies the coefficient with quantum-auxiliary
MI contraction at fixed uniform input. This covers the formal question,
but does not evaluate the SIC coefficient. Section3.3 explicitly gives
separations from ordinary scalar coefficients in general.

Berta, Sutter and Walter, [*Quantum Brascamp--Lieb Dualities* (2023)](https://doi.org/10.1007/s00220-023-04678-w),
Corollary3.10 equations(46)--(47), supplies fixed-baseline SDPI/trace-exp
duality. It does not tensor the scalar half-constant for free. Their
conditional Shearer Proposition3.2 concerns literal tensor-subsystem
partial traces; no such SIC realization has been acquired here.

Current Astra N966, pinned at8d51d60762b3ee28c10aaaa56e1b92da119dc1cc,
requires conditional order for ALL state pairs, equivalently complete
SLD order at ALL faithful baselines. It does not identify this special
uniform product-reference coefficient with its local uniform metric.

The all-baseline half-premise is false already without quantum memory:
restrict input to two SIC labels, sigma=diag(1/2,1/2), H=diag(h,-h).
The input SLD metric is4h^2. The output sigma is(S+T)/2, with eigenvalues
3/4,1/4 on its support, and K=h(S-T). K is off-diagonal in that basis
with magnitude sqrt(3)h/2, hence its SLD metric is3h^2. The ratio is3/4.
There is also an exact FAITHFUL nine-label receiver: put probability
93/200 on each of these two labels and1/100 on each other label.
The SIC output is `(91/200)(S+T)+(3/100)I3`. Its two relevant eigenvalues
sum97/100, so the output metric is300h^2/97; the input is400h^2/93.
Their ratio is exactly279/388>1/2, without a limiting argument.
Thus N966 cannot supply c1/2 by this stronger premise. At the uniform
nine-label baseline the
local zero-reference SLD ratio is1/4 by the SIC Gram identity, but the
finite segment leaves that baseline; no global metric transfer follows.

## A genuinely complete ordinary comparator

Gao, Junge, LaRacuente and Li, [*Complete positivity order and relative
entropy decay*, Forum Math.Sigma13:e31 (2025)](https://doi.org/10.1017/fms.2024.117),
Theorem2.5 equations(2.8)--(2.10), gives complete coherence contraction
at most `1-1/(2 k_cb)` when `0.9E<=cp (Phi*Phi)^k_cb<=cp1.1E`.
For the SIC Gram Schur channel, E is diagonal pinching and
`Gamma*Gamma=(1/4)id+(3/4)E`.
Its kth power has correlation matrix `(1-t)I+tJ`, t=4^(-k), whose
eigenvalues are1-t and1+8t. Both CP inequalities hold exactly when
t<=1/80. Hence k_cb=4 and the theorem gives7/8, uniformly over memory.
This is a valid complete bound, not the requested half-contraction.

The SAME ordinary proof improves this direct7/8 specialization. At k4,
the exact CP error is epsilon1/32. Lemma2.3 gives reverse-divergence
factor `a=(1-epsilon)/(1+epsilon)-epsilon/[(1-epsilon)(2log2-1)]`.
Since log2>=2/3, `a>=31/33-3/31=862/1023`.
Iterating their entropy-difference Lemma2.1 four times yields
`D(rho||(Gamma*Gamma)^4 rho)<=4[S(Gamma rho)-S(rho)]`.
Therefore the complete coherence factor is at most1615/2046<4/5.
Translated through the exact Gram identity, an equally informed ordinary
receiver already proves `S(Q|L)>=(431/2046)H(I|L)>=H(I|L)/5` for ALL
matrix weights. The target half remains unpaid by this bound. This is
an application of that established method, not a best-known-constant or
novelty claim. It prevents presenting7/8 as the strongest readily available
ordinary comparison.
