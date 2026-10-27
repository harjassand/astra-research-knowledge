# Independent accuracy-dependent program lower bounds

PASS for both distinct source/program tasks, with section 5 as the governing quantitative argument. The exact scalar/fidelity/relative-entropy checker replayed without producer mutation.

## Repeated retrieval and the complete error convention
Let L=floor(1/(8 zeta)), zeta<=1/16, so L>=2, L zeta<=1/8 and L>=1/(16 zeta). The independent data input is fixed. Each retrieval uses a FRESH n-copy program batch; total informative training is nL, not n. The entire circuit is a U-independent CPTP map from these programs and the fixed data. An explicit local fallback sends an erasure flag to |0>, leaving each postprocessed channel within the same unhalved diamond error zeta of the ideal inverse. This pays the composition domain without any further oracle call.

For theta=pi/(2L), the L-fold ideal inverse outputs on (|0>+|1>)/sqrt(2) are orthogonal. Telescoping L complete errors for each hypothesis gives half trace distance of the actual outputs at least 1-L zeta>=7/8 (the factor 1/2 is applied to each of the two deviations). Measurement data processing and classical Pinsker, with natural logarithms, give relative entropy at least 2(7/8)^2=49/32.

## White-reset discarded programs
The actual program is T=bI+aPhi_U, a=p/4, b=(1-p/4)/9>=1/12. Its spectral log gives EXACTLY D(T0||Ttheta)=a log(1+a/b)(1-t), t=|(1+2cos theta)/3|^2. Since log(1+a/b)<=3p and 1-t<=2theta^2/3, this is at most p^2 theta^2/2. Identical omega programs or U-independent ancillas add no relative entropy. Additivity over the nL fresh T copies and data processing yield 49/32<=n p^2 pi^2/(8L). Thus n>=49/(64 pi^2 p^2 zeta).

## Exact zero-deficit fixed-code family
For output dimension 4 with fixed 3D code, V_U=[U;0] and reset on the orthogonal fourth coordinate, the actual source has exactly zero deficit by the orthogonal success/reset split. The same labelled-program formula gives T_U=p[Phi_U/4+I9/12] direct_sum q[I3/3 tensor tau]. The weights and outside state are U-independent. Hence its relative entropy is exactly p times that of the p=1 conditional code program, at most p theta^2/2. Restrict independent data to the fixed code and repeat the same argument: n>=49/(64 pi^2 p zeta). This is a different signal scaling, not a p^-2 lower bound under every small-deficit promise.

## Independent corroborating route
The section 1 Choi argument also checks. Complete channel error gives ideal pure Choi overlap >=1-zeta/2; normalization of its environment projection gives vector error <=sqrt(zeta), and normalized vectorization gives operator error <=sqrt(3 zeta). Pure program purifications can be chosen at the exact mixed-state root fidelity while the processor ignores the purifying registers; V0*V1=rI remains exact. The opposite-phase diagonal entries imply r sin(theta)<=3sqrt(3 zeta). The two-dimensional fidelity formula, its n-copy product, Bernoulli bound r>=13/16, and sin(theta)>=5theta/6 give C=4225/248832 with the respective p^2 and p scaling. This is corroboration, not needed for section 5.

These lower bounds allow arbitrary fixed processors on the specified IID discarded T programs, but do not cover all raw labelled/adaptive training strategies, unbounded postselection, or only a decoder composed with the unknown noisy data channel. No hidden branch is exposed. The comparison with the received QPE/full-Bell upper is limited to these deterministic inverse program tasks, with all consumed copies counted; it is not a global recovery-optimality claim.
