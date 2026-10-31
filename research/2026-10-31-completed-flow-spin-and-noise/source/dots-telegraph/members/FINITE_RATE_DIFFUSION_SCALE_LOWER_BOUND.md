# Finite-rate lower bound on the diffusion resource scale

Lemma, 31 October 2026; independently mathematically checked after the whole simulator review. This is a scale check for the same black-box model, not a historical novelty claim. Related Gaussian dephasing optimality is already reported in the accessible abstract of Gao, Ji and Liu, PRL137,160405 (2026).

Let mu=lambda*T>=1, gamma*T>0, and W=sqrt(gamma*lambda) integral_0^T xi(s)ds for stationary symmetric telegraph noise. Its two-point correlation is exp(-2lambda|t-s|), so

E W^2 = gamma*T [1-(1-exp(-2mu))/(2mu)] >= gamma*T/2.

For ordered t1<t2<t3<t4, the four-point correlation is exp[-2lambda((t2-t1)+(t4-t3))]. Integrating t1 and t3 over their ordered ranges each costs at most 1/(2lambda), while the remaining ordered pair t2<t4 has area T^2/2. Therefore

E W^4 <= 24(gamma*lambda)^2*T^2/(8lambda^2) = 3(gamma*T)^2.

Set delta=1/sqrt(gamma*T). Since cos x<=1-x^2/2+x^4/24 for all real x,

E cos(delta W) <= 1-1/4+1/8 = 7/8.

Consider a qubit, H0=0, and the two alternatives A0=0 and A1=delta|1><1|. On input |+>, the first output remains pure and the second has its off-diagonal entries multiplied by the real characteristic value E cos(delta W). Their output trace-norm separation is at least 1/8, uniformly over mu>=1.

Let the supplied block-encoding normalization satisfy alphaA>=2delta. Use the exact unitary block encodings

U(B) = [[B, sqrt(I-B^2)], [sqrt(I-B^2), -B]], B=A/alphaA.

For these diagonal B, ||U(B1)-U(0)||<=2delta/alphaA. This follows directly from the scalar two-by-two blocks: 1-sqrt(1-r^2)<=r for 0<=r<=1/2. Controlled queries and inverse queries obey the same bound.

A Q-query algorithm has output trace-norm separation at most 2Q||U(B1)-U(0)||<=4Qdelta/alphaA, by the query hybrid and contractivity. If it approximates both target channels with error epsilon<=1/32, its two outputs must remain separated by at least 1/8-2epsilon>=1/16. Hence

Q >= alphaA/(64delta) = alphaA*sqrt(gamma*T)/64.

The lower bound is on block-encoding queries, including normalization overhead. It holds in the no-control special case and therefore also constrains a universal controlled-process simulator. It does not establish optimality of the candidate compiler's polynomial dependence on the physical resource scale; it shows that the scale cannot be removed altogether. It supplies no lower bound linear in lambda*T and is compatible with the proposed polylogarithmic rate dependence. Cases alphaA*sqrt(gamma*T)<2 give no nontrivial asymptotic claim from this construction.

## Separate review completion
The variance, ordered four-point integral, cosine inequality, output separation and controlled/inverse block-encoding hybrid were independently checked. Distances above use trace norm, not half trace norm. The bound concerns black-box access to A; an additional classical description of A could reveal which instance was supplied and is not part of this oracle lower bound. The normalization alphaA may be loose. This receipt covers the mathematical derivation, not an executed query lower-bound experiment or novelty.
