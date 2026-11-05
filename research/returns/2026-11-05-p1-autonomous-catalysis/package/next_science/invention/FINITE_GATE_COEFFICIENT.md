# Constructive coefficient for a general finite gate

Root's thermal-projection result need not leave its general-gate constant as an unspecified functional inequality. For a supplied finite irreducible bath generator B, stationary distribution nu, and Poisson-corrected observable w satisfying nu·w=0, solve the finite linear equation Bf=w with one additive normalization. Assume positive reverse rates on every included edge.

For any gate distribution p,

\[
E_pw=\sum_{x<y}(p_xb_{xy}-p_yb_{yx})(f_y-f_x).
\]

Let L(a,b)=(a−b)/(log a−log b), with the continuous value at a=b and L(a,0)=0. The standard entropy-production/Cauchy–Schwarz argument gives

\[
|E_pw|^2\le D_B(p)\sum_{x<y}L(p_xb_{xy},p_yb_{yx})(f_y-f_x)^2.
\]

Here D_B(p) is the sum over resolved undirected channel pairs of (forward flow−reverse flow)log(forward flow/reverse flow). The factor after D_B is a valid state-dependent coefficient. Since L(a,b)≤(a+b)/2, a directly computable uniform choice is

\[
C={1\over2}\max_x\sum_y b_{xy}(f_y-f_x)^2.
\]

This closes a finite algorithm: compute nu, solve a linear Poisson system, evaluate finite row sums. The root's global bound then uses sum_i mu_i C_i (or max_i C_i). It supplies no physical bath states or rates that were not acquired.

A stronger uniform choice maximizes the logarithmic-mean sum over the probability simplex. The objective is continuous and concave because the logarithmic mean is jointly concave, so this is a finite convex optimization in the standard maximize-concave convention. Its value upper-bounds the optimal observable/entropy ratio; Cauchy–Schwarz can still be loose for multiple edges. For a binary bath the coefficient becomes exactly

\[
{w_{diff}^2\over\gamma(1+q)}{p-t\over\operatorname{logit}p-\operatorname{logit}t},
\]

recovering root's sharp c(t) after maximization.

This is established current/entropy inequality machinery applied after a bath Poisson solve. It is a constructive completion and a useful way to avoid an uncomputed functional-inequality oracle, not a new thermodynamic mechanism. A source comparison remains necessary before claiming novelty for any particular composition.

## Exact primary comparison

Nagayama, Yoshimura and Ito, *Infinite variety of thermodynamic speed limits with general activities*, Physical Review Research 7, 013307 (2025), DOI [10.1103/PhysRevResearch.7.013307](https://doi.org/10.1103/PhysRevResearch.7.013307), [arXiv:2412.20690](https://arxiv.org/abs/2412.20690), was read at equations (22), (26), (30), (31), Appendix E's logarithmic-mean quadratic dissipation, and Appendix F. Its general edge-current/entropy framework contains the Cauchy–Schwarz step above. The extra Poisson solve translates a state observable into that established edge-current form; this should not be called a new entropy inequality. The downloaded PDF/text are `primary/nagayama_general_activities.*`, PDF SHA256 c781322f35498f827631fd3a73312ff91a3d88ba455ed1c2e1a222ad7ec81ade.
